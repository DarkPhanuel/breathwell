import os
import uuid
from datetime import timedelta

import joblib
import numpy as np
import pandas as pd
import requests
from django.conf import settings
from django.utils import timezone
from loguru import logger
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from data_collection.models import ProcessedData
from users.models import User
from users.services import send_pollution_alert_email

from .models import ModelTrainingHistory, Prediction, PredictionModel


class ModelService:
    def __init__(self):
        self.model_dir = settings.MODELS_DIR
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Load the active model if available
        self.model = None
        self.scaler = None
        self.load_active_model()
    
    def load_active_model(self):
        """Load the currently active model."""
        try:
            model_obj = PredictionModel.objects.filter(is_active=True).latest('created_at')
            model_path = model_obj.file_path
            
            # Check if model file exists
            if not os.path.exists(model_path):
                logger.error(f"Model file not found: {model_path}")
                self.download_remote_model()
                return
            
            # Load model and scaler
            model_data = joblib.load(model_path)
            self.model = model_data.get('model')
            self.scaler = model_data.get('scaler')
            
            logger.info(f"Loaded active model: {model_obj.name} v{model_obj.version}")
            
        except PredictionModel.DoesNotExist:
            logger.warning("No active model found")
            self.download_remote_model()
        
        except Exception as e:
            logger.error(f"Error loading active model: {e}")
            self.download_remote_model()

    def download_remote_model(self):
        """Download and load a model from Supabase Storage (private)."""
        remote_url = settings.REMOTE_MODEL_URL
        supabase_api_key = settings.SUPABASE_API_KEY

        if not remote_url or not supabase_api_key:
            logger.error("Remote model URL or Supabase API key not set")
            return False

        try:
            logger.info(f"Downloading model from {remote_url}")

            headers = {
                "apikey": supabase_api_key,
                "Authorization": f"Bearer {supabase_api_key}"
            }

            response = requests.get(remote_url, headers=headers)
            response.raise_for_status()

            # Generate a unique filename and save the model
            filename = f"model_{timezone.now().strftime('%Y%m%d%H%M%S')}.joblib"
            filepath = os.path.join(self.model_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            # Load the model (assumed to be an XGBRegressor instance)
            model = joblib.load(filepath)

            # Create model record in the database
            model_obj = PredictionModel.objects.create(
                name='remote_model',
                version=timezone.now().strftime('%Y%m%d%H%M%S'),
                file_path=filepath,
                metrics={},  # Optionnel : tu peux calculer les métriques plus tard
                is_active=True,
                is_remote=True
            )

            # Deactivate other models
            PredictionModel.objects.exclude(id=model_obj.id).update(is_active=False)

            # Set model and scaler (None in this case)
            self.model = model
            self.scaler = None

            logger.info(f"Downloaded and activated remote model: {model_obj.name} v{model_obj.version}")
            return True

        except Exception as e:
            logger.error(f"Error downloading remote model: {e}")
            return False

    def prepare_data_for_prediction(self, location=None, custom_data=None):
        """Prepare data for prediction from either location or custom data."""
        if custom_data:
            # Use the provided custom data
            data = {
                'temperature': custom_data.get('temperature', 20),
                'humidity': custom_data.get('humidity', 50),
                'wind_speed': custom_data.get('wind_speed', 5),
                'pressure': custom_data.get('pressure', 1013),
                'cloud_cover': custom_data.get('cloud_cover', 0),
                'pm25': custom_data.get('pollutant_pm25', 10),
                'pm10': custom_data.get('pollutant_pm10', 20),
                'o3': custom_data.get('pollutant_o3', 30),
                'no2': custom_data.get('pollutant_no2', 10),
                'so2': custom_data.get('pollutant_so2', 5),
                'co': custom_data.get('pollutant_co', 0.5),
                'location': custom_data.get('location', 'custom'),
                'latitude': custom_data.get('latitude', 0),
                'longitude': custom_data.get('longitude', 0),
            }
            
            # Create DataFrame
            df = pd.DataFrame([data])
            return df
        
        elif location:
            # Get the latest processed data for the location
            try:
                latest_data = ProcessedData.objects.filter(location=location).latest('timestamp')
                
                # Extract data
                weather = latest_data.data.get('weather', {})
                pollution = latest_data.data.get('pollution', {})
                
                data = {
                    'temperature': weather.get('temperature', 20),
                    'humidity': weather.get('humidity', 50),
                    'wind_speed': weather.get('wind_speed', 5),
                    'pressure': weather.get('pressure', 1013),
                    'cloud_cover': weather.get('clouds', 0),
                    'pm25': pollution.get('pm25', 10),
                    'pm10': pollution.get('pm10', 20),
                    'o3': pollution.get('o3', 30),
                    'no2': pollution.get('no2', 10),
                    'so2': pollution.get('so2', 5),
                    'co': pollution.get('co', 0.5),
                    'location': location,
                    'latitude': latest_data.latitude,
                    'longitude': latest_data.longitude,
                }
                
                # Create DataFrame
                df = pd.DataFrame([data])
                return df
                
            except ProcessedData.DoesNotExist:
                logger.error(f"No processed data found for location: {location}")
                return None
        
        return None
    
    def make_prediction(self, location, hours_ahead=24):
        """Make a prediction for a specific location."""
        if not self.model:
            logger.error("Model or scaler not available")
            self.load_active_model()
            if not self.model:
                return None
        
        # Prepare data
        df = self.prepare_data_for_prediction(location=location)
        if df is None:
            return None
        
        # Save location info
        loc_info = {
            'location': df['location'].iloc[0],
            'latitude': df['latitude'].iloc[0],
            'longitude': df['longitude'].iloc[0],
        }
        
        # Drop non-feature columns
        df = df.drop(['location', 'latitude', 'longitude'], axis=1)
        
        # Scale features
        #scaled_features = self.scaler.transform(df)
        scaled_features = df.values


        # Make prediction
        try:
            # Get current model
            model_obj = PredictionModel.objects.filter(is_active=True).latest('created_at')
            
            # Get prediction time
            prediction_time = timezone.now() + timedelta(hours=hours_ahead)

            feat =[scaled_features[0][:7]]

            logger.info(f"voilà feat: {feat}")

            # Make prediction
            prediction = self.model.predict(feat)[0]
            
            # Create prediction object
            pred_obj = Prediction.objects.create(
                model=model_obj,
                input_data=df.to_dict(orient='records')[0],
                output_data={'prediction': float(prediction)},
                location=loc_info['location'],
                latitude=loc_info['latitude'],
                longitude=loc_info['longitude'],
                timestamp=timezone.now(),
                prediction_time=prediction_time
            )
            
            # Check if prediction exceeds user thresholds and send alerts
            self.check_and_send_alerts(pred_obj)
            
            # Return prediction data
            return {
                'prediction': float(prediction),
                'location': loc_info['location'],
                'timestamp': timezone.now().isoformat(),
                'prediction_time': prediction_time.isoformat(),
                'model': f"{model_obj.name} v{model_obj.version}"
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
    
    def make_custom_prediction(self, custom_data):
        """Make a prediction using custom input data."""
        if not self.model or not self.scaler:
            logger.error("Model or scaler not available")
            self.load_active_model()
            if not self.model or not self.scaler:
                return None
        
        # Prepare data
        df = self.prepare_data_for_prediction(custom_data=custom_data)
        if df is None:
            return None
        
        # Save location info
        loc_info = {
            'location': df['location'].iloc[0],
            'latitude': df['latitude'].iloc[0],
            'longitude': df['longitude'].iloc[0],
        }
        
        # Drop non-feature columns
        df = df.drop(['location', 'latitude', 'longitude'], axis=1)
        
        # Scale features
        scaled_features = self.scaler.transform(df)
        
        # Make prediction
        try:
            # Get current model
            model_obj = PredictionModel.objects.filter(is_active=True).latest('created_at')
            
            # Make prediction
            prediction = self.model.predict(scaled_features)[0]
            
            # Create prediction object
            pred_obj = Prediction.objects.create(
                model=model_obj,
                input_data=df.to_dict(orient='records')[0],
                output_data={'prediction': float(prediction)},
                location=loc_info['location'],
                latitude=loc_info['latitude'],
                longitude=loc_info['longitude'],
                timestamp=timezone.now(),
                prediction_time=timezone.now()  # Custom predictions are for current time
            )
            
            # Check if prediction exceeds user thresholds and send alerts
            self.check_and_send_alerts(pred_obj)
            
            # Return prediction data
            return {
                'prediction': float(prediction),
                'location': loc_info['location'],
                'timestamp': timezone.now().isoformat(),
                'model': f"{model_obj.name} v{model_obj.version}"
            }
            
        except Exception as e:
            logger.error(f"Error making custom prediction: {e}")
            return None
    
    def check_and_send_alerts(self, prediction):
        """Check if prediction exceeds thresholds and send alerts to users."""
        try:
            # Get prediction value
            pred_value = prediction.output_data.get('prediction', 0)
            
            # Get users who want alerts
            users = User.objects.filter(receive_alerts=True)
            
            for user in users:
                # Check if prediction exceeds user's threshold
                if pred_value > user.pollution_threshold:
                    # Prepare alert data
                    alert_data = {
                        'location': prediction.location,
                        'pollutant': 'AQI',  # Adjust based on your model
                        'value': pred_value,
                        'time': prediction.prediction_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Send alert
                    try:
                        send_pollution_alert_email(user, alert_data)
                        logger.info(f"Sent pollution alert to {user.email}")
                    except Exception as e:
                        logger.error(f"Error sending pollution alert to {user.email}: {e}")
            
        except Exception as e:
            logger.error(f"Error checking thresholds: {e}")
    
    def prepare_training_data(self, days=30):
        """Prepare data for model training."""
        # Get data from the past N days
        cutoff_date = timezone.now() - timedelta(days=days)
        
        try:
            # Get processed data
            data = ProcessedData.objects.filter(timestamp__gte=cutoff_date)
            
            if data.count() < 100:  # Need enough data for training
                logger.warning(f"Not enough data for training: {data.count()} records")
                return None
            
            # Prepare features and target
            records = []
            
            for item in data:
                try:
                    # Extract weather and pollution data
                    weather = item.data.get('weather', {})
                    pollution = item.data.get('pollution', {})
                    
                    # Create record
                    record = {
                        'temperature': weather.get('temperature', 20),
                        'humidity': weather.get('humidity', 50),
                        'wind_speed': weather.get('wind_speed', 5),
                        'pressure': weather.get('pressure', 1013),
                        'cloud_cover': weather.get('clouds', 0),
                        'pm25': pollution.get('pm25', 10),
                        'pm10': pollution.get('pm10', 20),
                        'o3': pollution.get('o3', 30),
                        'no2': pollution.get('no2', 10),
                        'so2': pollution.get('so2', 5),
                        'co': pollution.get('co', 0.5),
                        # Target is typically one of the pollution values
                        # Here we'll use pm25 as an example
                        'target': pollution.get('pm25', 10),
                    }
                    
                    records.append(record)
                    
                except Exception as e:
                    logger.error(f"Error processing data record: {e}")
            
            if not records:
                logger.warning("No valid records for training")
                return None
            
            # Create DataFrame
            df = pd.DataFrame(records)
            
            # Handle missing values
            df = df.fillna(method='ffill').fillna(method='bfill').fillna(0)
            
            return df
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return None

    def train_model(self, days=30):
        """Train or fine-tune the model with new data."""
        # Prepare data
        df = self.prepare_training_data(days)
        if df is None:
            return None

        # Split features and target
        X = df.drop('target', axis=1)
        y = df['target']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create scaler
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Get metrics of current model if available
        metrics_before = {}
        if self.model and self.scaler:
            # Evaluate current model
            y_pred = self.model.predict(X_test_scaled)
            metrics_before = {
                'mae': mean_absolute_error(y_test, y_pred),
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred)
            }

        # Train new model or fine-tune existing one
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate new model
        y_pred = model.predict(X_test_scaled)
        metrics_after = {
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }

        # Calculate improvement
        improvement = None
        should_update = False

        if metrics_before:
            # Calculate improvement in RMSE (lower is better)
            if metrics_before['rmse'] > 0:
                improvement = ((metrics_before['rmse'] - metrics_after['rmse']) / metrics_before['rmse']) * 100

                # Determine if we should update the model (5% improvement threshold)
                should_update = improvement >= 5
        else:
            # No previous model, so always update
            should_update = True

        # Create model file
        model_data = {
            'model': model,
            'scaler': scaler,
            'metrics': metrics_after,
            'features': list(X.columns),
            'created_at': timezone.now().isoformat()
        }

        # Generate unique filename
        filename = f"model_{uuid.uuid4().hex}.joblib"
        filepath = os.path.join(self.model_dir, filename)

        # Save model
        joblib.dump(model_data, filepath)

        # Create model record
        model_obj = PredictionModel.objects.create(
            name='local_model',
            version=timezone.now().strftime('%Y%m%d%H%M%S'),
            file_path=filepath,
            metrics=metrics_after,
            is_active=should_update,
            is_remote=False
        )

        # If new model is better, set it as active
        if should_update:
            # Deactivate other models
            PredictionModel.objects.exclude(id=model_obj.id).update(is_active=False)

            # Update instance variables
            self.model = model
            self.scaler = scaler

            logger.info(f"Activated new model with {improvement:.2f}% improvement")

        # Create training history record
        history = ModelTrainingHistory.objects.create(
            model=model_obj,
            training_data_start=timezone.now() - timedelta(days=days),
            training_data_end=timezone.now(),
            metrics_before=metrics_before,
            metrics_after=metrics_after,
            improvement=improvement,
            remote_updated=False
        )

        # If significant improvement, update remote model
        if should_update and improvement and improvement >= 10:
            self.update_remote_model(filepath)
            history.remote_updated = True
            history.save()

        return history
    
    def update_remote_model(self, model_path):
        """Update the remote model with the local one."""
        # This is a placeholder for the actual implementation
        # In a real scenario, you would upload the model to a remote storage
        logger.info(f"Updating remote model with {model_path}")
        
        # Here you would implement the upload logic
        # For example, using AWS S3, Google Cloud Storage, etc.
        
        return True
    
    def force_remote_model_update(self):
        """Force an update of the remote model with the current active model."""
        try:
            model_obj = PredictionModel.objects.filter(is_active=True).latest('created_at')
            return self.update_remote_model(model_obj.file_path)
        except PredictionModel.DoesNotExist:
            logger.error("No active model found for remote update")
            return False
        except Exception as e:
            logger.error(f"Error forcing remote model update: {e}")
            return False
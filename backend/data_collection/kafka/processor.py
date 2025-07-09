import json

import pandas as pd
from confluent_kafka import Consumer, Producer
from django.conf import settings
from django.utils import timezone
from loguru import logger

from data_collection.models import ProcessedData, RawData


class KafkaProcessor:
    def __init__(self):
        # Setup consumer
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'data-processor',
            'auto.offset.reset': 'latest'
        })
        self.consumer.subscribe([settings.KAFKA_RAW_DATA_TOPIC])
        
        # Setup producer
        self.producer = Producer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'client.id': 'data-processor'
        })
        self.output_topic = settings.KAFKA_PROCESSED_DATA_TOPIC
        
        # Delivery callback
        def delivery_callback(err, msg):
            if err:
                logger.error(f'Message delivery failed: {err}')
            else:
                logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')
        
        self.delivery_callback = delivery_callback
    
    def process_openweather_data(self, raw_data):
        """Process OpenWeather data into a structured format."""
        try:
            data = raw_data['data']
            
            # Extract relevant weather information
            processed = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'clouds': data['clouds']['all'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'source': 'openweather'
            }
            
            # Add rain and snow if available
            if 'rain' in data:
                processed['rain_1h'] = data['rain'].get('1h', 0)
            else:
                processed['rain_1h'] = 0
                
            if 'snow' in data:
                processed['snow_1h'] = data['snow'].get('1h', 0)
            else:
                processed['snow_1h'] = 0
            
            return processed
            
        except KeyError as e:
            logger.error(f"Error processing OpenWeather data: {e}")
            return None

    def process_openaq_data(self, raw_data):
        """Process OpenAQ data into a structured format."""
        try:
            # Debug log to inspect raw data structure
            logger.debug(f"Processing OpenAQ data: {json.dumps(raw_data, indent=2)}")

            # Initialize processed data structure
            processed = {
                'source': 'openaq',
                'measurements': {},
                'metadata': {
                    'location': raw_data.get('location', 'unknown'),
                    'coordinates': {
                        'latitude': raw_data.get('latitude'),
                        'longitude': raw_data.get('longitude')
                    }
                }
            }

            # Process each measurement in the list
            for measurement in raw_data['data']:
                try:
                    param_name = measurement.get('parameter', {}).get('name', '').lower()
                    value = measurement.get('value')

                    if param_name and value is not None:
                        # Store the measurement value
                        processed['measurements'][param_name] = value

                        # Optionally store additional metadata for each parameter
                        processed['measurements'][f'{param_name}_units'] = measurement.get('parameter', {}).get('units',
                                                                                                                '')

                except Exception as e:
                    logger.warning(f"Error processing measurement {measurement}: {str(e)}")
                    continue

            return processed

        except Exception as e:
            logger.error(f"Error processing OpenAQ data: {str(e)}")
            return None
    
    def merge_data(self, weather_data, pollution_data, location_name):
        """Merge weather and pollution data for the same location."""
        if not weather_data or not pollution_data:
            return None
        
        merged = {
            'location': location_name,
            'timestamp': timezone.now().isoformat(),
            'weather': weather_data,
            'pollution': pollution_data.get('measurements', {})
        }

        return merged
    
    def store_processed_data(self, processed_data, raw_data_ids):
        """Store processed data in the database."""
        try:
            # Create ProcessedData object
            processed_obj = ProcessedData.objects.create(
                data=processed_data,
                location=processed_data['location'],
                latitude=float(processed_data.get('latitude', 0)),
                longitude=float(processed_data.get('longitude', 0)),
                timestamp=timezone.now()
            )
            
            # Link to raw data
            for raw_id in raw_data_ids:
                try:
                    raw_data = RawData.objects.get(id=raw_id)
                    processed_obj.raw_data.add(raw_data)
                except RawData.DoesNotExist:
                    logger.warning(f"Raw data with ID {raw_id} not found")
            
            processed_obj.save()
            return processed_obj
            
        except Exception as e:
            logger.error(f"Error storing processed data: {e}")
            return None
    
    def convert_to_dataframe(self, processed_data):
        """Convert processed data to a pandas DataFrame."""
        try:
            # Flatten the nested structure
            flat_data = {
                'location': processed_data['location'],
                'timestamp': processed_data['timestamp'],
                'latitude': processed_data.get('latitude', 0),
                'longitude': processed_data.get('longitude', 0),
            }
            
            # Add weather data
            for key, value in processed_data.get('weather', {}).items():
                flat_data[f'weather_{key}'] = value
            
            # Add pollution data
            for key, value in processed_data.get('pollution', {}).items():
                flat_data[f'pollution_{key}'] = value
            
            # Create DataFrame with a single row
            df = pd.DataFrame([flat_data])
            return df
            
        except Exception as e:
            logger.error(f"Error converting to DataFrame: {e}")
            return None
    
    def run(self):
        """Main method to run the processor service."""
        logger.info("Starting Kafka Processor for data transformation")
        
        # Storage for latest data by location
        latest_data = {}
        
        while True:
            try:
                # Poll for messages
                msg = self.consumer.poll(1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue
                
                # Process the message
                try:
                    raw_data = json.loads(msg.value())
                    location = raw_data.get('location')
                    source = raw_data.get('source')
                    
                    # Skip if missing critical data
                    if not location or not source:
                        logger.warning("Skipping message with missing location or source")
                        continue
                    
                    # Process based on source
                    if source == 'openweather':
                        logger.debug(' source openweather')
                        processed = self.process_openweather_data(raw_data)
                        if processed:
                            if location not in latest_data:
                                latest_data[location] = {'raw_ids': []}
                            latest_data[location]['weather'] = processed
                            latest_data[location]['raw_ids'].append(raw_data.get('id'))
                            latest_data[location]['latitude'] = raw_data.get('latitude')
                            latest_data[location]['longitude'] = raw_data.get('longitude')
                    
                    elif source == 'openaq':
                        logger.debug('source openaq')
                        processed = self.process_openaq_data(raw_data)
                        if processed:
                            if location not in latest_data:
                                latest_data[location] = {'raw_ids': []}
                            latest_data[location]['pollution'] = processed
                            latest_data[location]['raw_ids'].append(raw_data.get('id'))
                            latest_data[location]['latitude'] = raw_data.get('latitude')
                            latest_data[location]['longitude'] = raw_data.get('longitude')
                    
                    # Check if we have both weather and pollution data for this location
                    if location in latest_data and 'weather' in latest_data[location] and 'pollution' in latest_data[location]:
                        # We have both data types, merge and send to output topic
                        merged_data = self.merge_data(
                            latest_data[location]['weather'],
                            latest_data[location]['pollution'],
                            location
                        )
                        
                        if merged_data:
                            logger.debug('merged_data')
                            # Add coordinates
                            merged_data['latitude'] = latest_data[location]['latitude']
                            merged_data['longitude'] = latest_data[location]['longitude']
                            
                            # Store in database
                            processed_obj = self.store_processed_data(
                                merged_data,
                                latest_data[location]['raw_ids']
                            )
                            
                            if processed_obj:
                                # Convert to DataFrame for ML model
                                logger.debug('Start converting dataFrame for ML model')
                                df = self.convert_to_dataframe(merged_data)
                                
                                if df is not None:
                                    # Send to output topic for ML model
                                    output_message = {
                                        'id': processed_obj.id,
                                        'data': merged_data,
                                        'dataframe': df.to_json(orient='records')
                                    }
                                    logger.debug(self.output_topic)
                                    logger.debug(output_message)

                                    self.producer.produce(
                                        self.output_topic,
                                        key=location,
                                        value=json.dumps(output_message),
                                        callback=self.delivery_callback
                                    )
                            
                            # Clear the data for this location
                            latest_data[location] = {'raw_ids': []}
                
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding message: {e}")
                
                # Flush producer
                self.producer.flush()
                
            except Exception as e:
                logger.error(f"Error in processor service: {e}")
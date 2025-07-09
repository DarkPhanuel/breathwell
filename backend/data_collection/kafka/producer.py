import json
import time
from datetime import datetime

import requests
from confluent_kafka import Producer
from django.conf import settings
from django.utils import timezone
from loguru import logger

from data_collection.models import Location, RawData


class KafkaProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'client.id': 'data-collector'
        })
        self.topic = settings.KAFKA_RAW_DATA_TOPIC
        self.openweather_api_key = settings.OPENWEATHER_API_KEY
        self.openaq_api_key = settings.OPENAQ_API_KEY
        
        # Delivery callback
        def delivery_callback(err, msg):
            if err:
                logger.error(f'Message delivery failed: {err}')
            else:
                logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')
        
        self.delivery_callback = delivery_callback
    
    def fetch_openweather_data(self, location):
        """Fetch weather data from OpenWeather API for a location."""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': location.latitude,
            'lon': location.longitude,
            'appid': self.openweather_api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save to database
            timestamp = timezone.now()
            raw_data = RawData.objects.create(
                source='openweather',
                data=data,
                location=location.name,
                latitude=location.latitude,
                longitude=location.longitude,
                timestamp=timestamp
            )
            
            # Prepare message for Kafka
            message = {
                'id': raw_data.id,
                'source': 'openweather',
                'data': data,
                'location': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'timestamp': timestamp.isoformat()
            }
            
            # Send to Kafka
            self.producer.produce(
                self.topic,
                key=f"openweather-{location.name}",
                value=json.dumps(message),
                callback=self.delivery_callback
            )
            
            logger.info(f"Fetched OpenWeather data for {location.name}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching OpenWeather data for {location.name}: {e}")
            return None

    def fetch_openaq_data(self, location):
        """Fetch daily pollution measurements from multiple OpenAQ sensors around a location."""
        base_url = "https://api.openaq.org/v3"

        headers = {}
        if self.openaq_api_key:
            headers['X-API-Key'] = self.openaq_api_key

        try:
            # Étape 1 : Chercher plusieurs stations proches
            stations_response = requests.get(
                f"{base_url}/locations",
                params={
                    'coordinates': f"{location.latitude},{location.longitude}",
                    'radius': 10000,
                    'limit': 5,
                    'sort': 'asc'
                },
                headers=headers
            )
            stations_response.raise_for_status()
            stations_data = stations_response.json()

            if not stations_data.get('results'):
                logger.warning(f"Aucune station OpenAQ trouvée près de {location.name}")
                return None

            all_measurements = []
            seen_params = set()

            # Étape 2 : Parcourir les stations et capteurs
            for station in stations_data['results']:
                sensors = station.get('sensors', [])
                for sensor in sensors:
                    param_name = sensor.get("parameter", {}).get("name")
                    if param_name in seen_params:
                        continue  # on a déjà un capteur pour ce paramètre

                    sensor_id = sensor['id']
                    sensor_response = requests.get(
                        f"{base_url}/sensors/{sensor_id}/measurements/daily",
                        params={
                            "limit": 1,
                            "sort": "desc"
                        },
                        headers=headers
                    )
                    sensor_response.raise_for_status()
                    sensor_data = sensor_response.json()

                    if sensor_data.get("results"):
                        measurement = sensor_data["results"][0]
                        all_measurements.append(measurement)
                        seen_params.add(param_name)

                if len(seen_params) >= 5:  # tu peux ajuster ce seuil selon tes besoins
                    break

            if not all_measurements:
                logger.warning(f"Aucune mesure trouvée pour les capteurs autour de {location.name}")
                return None

            # Étape 3 : Sauvegarde en base
            timestamp = timezone.now()
            raw_data = RawData.objects.create(
                source='openaq',
                data=all_measurements,
                location=location.name,
                latitude=location.latitude,
                longitude=location.longitude,
                timestamp=timestamp
            )

            # Étape 4 : Envoi à Kafka
            message = {
                'id': raw_data.id,
                'source': 'openaq',
                'data': all_measurements,
                'location': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'timestamp': timestamp.isoformat()
            }

            self.producer.produce(
                self.topic,
                key=f"openaq-{location.name}",
                value=json.dumps(message),
                callback=self.delivery_callback
            )

            logger.info(f"Mesures journalières complètes OpenAQ récupérées pour {location.name}")
            return all_measurements

        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la récupération des mesures journalières OpenAQ pour {location.name} : {e}")
            return None

    def run(self):
        """Main method to run the producer service."""
        logger.info("Starting Kafka Producer for data collection")
        
        while True:
            try:
                # Get all active locations
                locations = Location.objects.filter(is_active=True)
                
                if not locations:
                    logger.warning("No active locations found, waiting 60 seconds")
                    time.sleep(60)
                    continue
                
                for location in locations:
                    # Fetch data from both APIs
                    self.fetch_openweather_data(location)
                    self.fetch_openaq_data(location)
                    
                    # Small delay between locations to avoid rate limits
                    time.sleep(1)
                
                # Flush to ensure all messages are sent
                self.producer.flush()
                
                # Wait before next collection cycle (5 minutes)
                logger.info("Data collection cycle complete, waiting 30 secondes")
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in producer service: {e}")
                time.sleep(60)  # Wait a bit before retrying
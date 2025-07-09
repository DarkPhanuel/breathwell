import json
from datetime import timedelta

import pandas as pd
from confluent_kafka import Consumer
from django.conf import settings
from django.utils import timezone
from loguru import logger
import xgboost

from predictions.services import ModelService


class KafkaConsumer:
    def __init__(self):
        # Setup consumer
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'model-consumer',
            'auto.offset.reset': 'latest'
        })
        self.consumer.subscribe([settings.KAFKA_PROCESSED_DATA_TOPIC])
        
        # Initialize model service
        self.model_service = ModelService()
        
        # Track when we last trained the model
        self.last_training = timezone.now()
    
    def process_message(self, message):
        """Process a message from Kafka."""
        logger.debug("Start processing")
        try:
            # Parse message
            data = json.loads(message.value())
            
            # Extract the DataFrame
            if 'dataframe' in data:
                logger.debug("Getting the data frame")

                df_json = data['dataframe']
                df = pd.read_json(df_json, orient='records')
                
                # Use the data for predictions
                location = data['data']['location']
                
                # Make prediction
                prediction = self.model_service.make_prediction(location)
                
                if prediction:
                    logger.info(f"Made prediction for {location}: {prediction['prediction']}")
                
                # Check if we should train the model
                self.check_and_train_model()
            
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def check_and_train_model(self):
        """Check if we should train the model based on time interval."""
        now = timezone.now()
        interval = timedelta(seconds=settings.MODEL_UPDATE_INTERVAL)
        
        if now - self.last_training >= interval:
            logger.info("Training model based on scheduled interval")
            
            # Train model with data from the last 30 days
            self.model_service.train_model(days=30)
            
            # Update last training time
            self.last_training = now
    
    def run(self):
        """Main method to run the consumer service."""
        logger.info("Starting Kafka Consumer for model predictions")
        
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
                self.process_message(msg)
                logger.debug("finish")

            except Exception as e:
                logger.error(f"Error in consumer service: {e}")
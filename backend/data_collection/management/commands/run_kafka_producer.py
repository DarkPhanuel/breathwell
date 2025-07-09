from django.core.management.base import BaseCommand
from loguru import logger

from data_collection.kafka.producer import KafkaProducer


class Command(BaseCommand):
    help = 'Run the Kafka Producer to collect data from OpenWeather and OpenAQ'

    def handle(self, *args, **options):
        logger.info('Starting Kafka Producer')
        producer = KafkaProducer()
        producer.run()
from django.core.management.base import BaseCommand
from loguru import logger

from predictions.kafka.consumer import KafkaConsumer


class Command(BaseCommand):
    help = 'Run the Kafka Consumer to process data and make predictions'

    def handle(self, *args, **options):
        logger.info('Starting Kafka Consumer')
        consumer = KafkaConsumer()
        consumer.run()
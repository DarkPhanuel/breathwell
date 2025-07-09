from django.core.management.base import BaseCommand
from loguru import logger

from data_collection.kafka.processor import KafkaProcessor


class Command(BaseCommand):
    help = 'Run the Kafka Processor to transform raw data'

    def handle(self, *args, **options):
        logger.info('Starting Kafka Processor')
        processor = KafkaProcessor()
        processor.run()
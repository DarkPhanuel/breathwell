from django.db import models


class RawData(models.Model):
    """
    Model to store raw data collected from external APIs.
    """
    source = models.CharField(max_length=100)  # 'openaq' or 'openweather'
    data = models.JSONField()
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    collected_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['source']),
            models.Index(fields=['location']),
            models.Index(fields=['timestamp']),
        ]
        
    def __str__(self):
        return f"{self.source} data for {self.location} at {self.timestamp}"


class ProcessedData(models.Model):
    """
    Model to store processed data after Kafka transformation.
    """
    raw_data = models.ManyToManyField(RawData, related_name='processed_data')
    data = models.JSONField()
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['timestamp']),
        ]
        
    def __str__(self):
        return f"Processed data for {self.location} at {self.timestamp}"


class Location(models.Model):
    """
    Model to store locations for data collection.
    """
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('latitude', 'longitude')
        
    def __str__(self):
        return f"{self.name}, {self.country}"
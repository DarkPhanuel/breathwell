from django.db import models


class PredictionModel(models.Model):
    """
    Model to track ML models and their versions.
    """
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255)
    metrics = models.JSONField(default=dict)
    is_active = models.BooleanField(default=False)
    is_remote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'version')
        
    def __str__(self):
        return f"{self.name} v{self.version}"


class Prediction(models.Model):
    """
    Model to store predictions made by the ML model.
    """
    model = models.ForeignKey(PredictionModel, on_delete=models.CASCADE, related_name='predictions')
    input_data = models.JSONField()
    output_data = models.JSONField()
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    prediction_time = models.DateTimeField()  # When the prediction is for
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['prediction_time']),
        ]
        
    def __str__(self):
        return f"Prediction for {self.location} at {self.prediction_time}"


class ModelTrainingHistory(models.Model):
    """
    Model to track training history and performance improvements.
    """
    model = models.ForeignKey(PredictionModel, on_delete=models.CASCADE, related_name='training_history')
    training_data_start = models.DateTimeField()
    training_data_end = models.DateTimeField()
    metrics_before = models.JSONField(default=dict)
    metrics_after = models.JSONField(default=dict)
    improvement = models.FloatField(null=True, blank=True)  # Percentage improvement
    remote_updated = models.BooleanField(default=False)  # Whether remote model was updated
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Training for {self.model} at {self.created_at}"
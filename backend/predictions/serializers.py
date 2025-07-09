from rest_framework import serializers

from .models import ModelTrainingHistory, Prediction, PredictionModel


class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionModel
        fields = ('id', 'name', 'version', 'metrics', 'is_active', 'is_remote', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class PredictionSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    model_version = serializers.CharField(source='model.version', read_only=True)
    
    class Meta:
        model = Prediction
        fields = ('id', 'model', 'model_name', 'model_version', 'input_data', 'output_data', 
                 'location', 'latitude', 'longitude', 'timestamp', 'prediction_time', 'created_at')
        read_only_fields = ('id', 'created_at')


class ModelTrainingHistorySerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    model_version = serializers.CharField(source='model.version', read_only=True)
    
    class Meta:
        model = ModelTrainingHistory
        fields = ('id', 'model', 'model_name', 'model_version', 'training_data_start', 
                 'training_data_end', 'metrics_before', 'metrics_after', 
                 'improvement', 'remote_updated', 'created_at')
        read_only_fields = ('id', 'created_at')


class PredictionRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True)
    hours_ahead = serializers.IntegerField(default=24, min_value=1, max_value=168)  # 1 hour to 7 days


class CustomPredictionRequestSerializer(serializers.Serializer):
    temperature = serializers.FloatField(required=False)
    humidity = serializers.FloatField(required=False)
    wind_speed = serializers.FloatField(required=False)
    pressure = serializers.FloatField(required=False)
    cloud_cover = serializers.FloatField(required=False)
    pollutant_pm25 = serializers.FloatField(required=False)
    pollutant_pm10 = serializers.FloatField(required=False)
    pollutant_o3 = serializers.FloatField(required=False)
    pollutant_no2 = serializers.FloatField(required=False)
    pollutant_so2 = serializers.FloatField(required=False)
    pollutant_co = serializers.FloatField(required=False)
    location = serializers.CharField(required=True)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
from django.contrib import admin

from .models import ModelTrainingHistory, Prediction, PredictionModel


@admin.register(PredictionModel)
class PredictionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active', 'is_remote', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_remote')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('location', 'model', 'timestamp', 'prediction_time', 'created_at')
    list_filter = ('location', 'model')
    search_fields = ('location',)
    date_hierarchy = 'prediction_time'
    readonly_fields = ('created_at',)


@admin.register(ModelTrainingHistory)
class ModelTrainingHistoryAdmin(admin.ModelAdmin):
    list_display = ('model', 'training_data_start', 'training_data_end', 'improvement', 'remote_updated', 'created_at')
    list_filter = ('model', 'remote_updated')
    search_fields = ('model__name',)
    readonly_fields = ('created_at',)
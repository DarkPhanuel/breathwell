from django.urls import path

from .views import (ActiveModelDetailView, CustomPredictionView,
                    ForceModelDownloadView, ForceModelUpdateView,
                    GetPredictionView, ManualModelTrainingView,
                    ModelEvaluationView, ModelTrainingHistoryListView,
                    PredictionListView, PredictionModelListView)

urlpatterns = [
    path('models/', PredictionModelListView.as_view(), name='model-list'),
    path('models/active/', ActiveModelDetailView.as_view(), name='active-model'),
    path('list/', PredictionListView.as_view(), name='prediction-list'),
    path('get/', GetPredictionView.as_view(), name='get-prediction'),
    path('custom/', CustomPredictionView.as_view(), name='custom-prediction'),
    path('training/history/', ModelTrainingHistoryListView.as_view(), name='training-history'),
    path('training/manual/', ManualModelTrainingView.as_view(), name='manual-training'),
    path('evaluation/', ModelEvaluationView.as_view(), name='model-evaluation'),
    path('models/update-remote/', ForceModelUpdateView.as_view(), name='update-remote-model'),
    path('models/download-remote/', ForceModelDownloadView.as_view(), name='download-remote-model'),
]
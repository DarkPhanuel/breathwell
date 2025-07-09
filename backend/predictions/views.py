from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdminUser

from .models import ModelTrainingHistory, Prediction, PredictionModel
from .serializers import (CustomPredictionRequestSerializer,
                          ModelTrainingHistorySerializer,
                          PredictionModelSerializer, PredictionRequestSerializer,
                          PredictionSerializer)
from .services import ModelService


class PredictionModelListView(generics.ListAPIView):
    serializer_class = PredictionModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PredictionModel.objects.all().order_by('-created_at')


class ActiveModelDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            model = PredictionModel.objects.filter(is_active=True).latest('created_at')
            serializer = PredictionModelSerializer(model)
            return Response(serializer.data)
        except PredictionModel.DoesNotExist:
            return Response({"error": "No active model found"}, status=status.HTTP_404_NOT_FOUND)


class PredictionListView(generics.ListAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Prediction.objects.all().order_by('-prediction_time')
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location=location)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(prediction_time__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(prediction_time__lte=end_date)
        
        # Limit results
        limit = self.request.query_params.get('limit', 100)
        try:
            limit = int(limit)
        except ValueError:
            limit = 100
        
        return queryset[:limit]


class GetPredictionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            hours_ahead = serializer.validated_data['hours_ahead']
            
            model_service = ModelService()
            prediction = model_service.make_prediction(location, hours_ahead)
            
            if prediction:
                return Response(prediction)
            else:
                return Response({"error": "Could not make prediction"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPredictionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CustomPredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            model_service = ModelService()
            prediction = model_service.make_custom_prediction(serializer.validated_data)
            
            if prediction:
                return Response(prediction)
            else:
                return Response({"error": "Could not make prediction"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelTrainingHistoryListView(generics.ListAPIView):
    serializer_class = ModelTrainingHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ModelTrainingHistory.objects.all().order_by('-created_at')
        
        # Filter by model
        model_id = self.request.query_params.get('model_id')
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        return queryset


class ManualModelTrainingView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        days = request.data.get('days', 30)
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "Days must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if days < 1:
            return Response({"error": "Days must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)
        
        model_service = ModelService()
        result = model_service.train_model(days)
        
        if result:
            return Response({"message": "Model training initiated", "training_id": result.id})
        else:
            return Response({"error": "Could not initiate model training"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelEvaluationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        days = request.query_params.get('days', 7)
        try:
            days = int(days)
        except ValueError:
            days = 7
        
        # Get model metrics for the past N days
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get latest model
        try:
            model = PredictionModel.objects.filter(is_active=True).latest('created_at')
        except PredictionModel.DoesNotExist:
            return Response({"error": "No active model found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get training history
        training_history = ModelTrainingHistory.objects.filter(
            model=model,
            created_at__gte=cutoff_date
        ).order_by('-created_at')
        
        # Calculate average improvement
        improvements = [h.improvement for h in training_history if h.improvement is not None]
        avg_improvement = sum(improvements) / len(improvements) if improvements else 0
        
        # Get latest metrics
        latest_metrics = model.metrics if model else {}
        
        return Response({
            'model': PredictionModelSerializer(model).data,
            'average_improvement': avg_improvement,
            'training_count': training_history.count(),
            'latest_metrics': latest_metrics
        })


class ForceModelUpdateView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        model_service = ModelService()
        success = model_service.force_remote_model_update()
        
        if success:
            return Response({"message": "Remote model update initiated"})
        else:
            return Response({"error": "Could not initiate remote model update"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForceModelDownloadView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        model_service = ModelService()
        success = model_service.download_remote_model()
        
        if success:
            return Response({"message": "Remote model download initiated"})
        else:
            return Response({"error": "Could not initiate remote model download"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.utils import timezone
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdminUser

from .models import Location, ProcessedData, RawData
from .serializers import (LocationSerializer, ProcessedDataSerializer,
                          RawDataSerializer)


class RawDataListView(generics.ListAPIView):
    serializer_class = RawDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['source', 'location']
    ordering_fields = ['timestamp', 'collected_at']
    
    def get_queryset(self):
        queryset = RawData.objects.all().order_by('-timestamp')
        
        # Filter by source
        source = self.request.query_params.get('source')
        if source:
            queryset = queryset.filter(source=source)
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location=location)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset


class ProcessedDataListView(generics.ListAPIView):
    serializer_class = ProcessedDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['location']
    ordering_fields = ['timestamp', 'processed_at']
    
    def get_queryset(self):
        queryset = ProcessedData.objects.all().order_by('-timestamp')
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location=location)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        # Limit results
        limit = self.request.query_params.get('limit', 100)
        try:
            limit = int(limit)
        except ValueError:
            limit = 100
        
        return queryset[:limit]


class LatestDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        location = request.query_params.get('location')
        if not location:
            return Response({"error": "Location parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the latest processed data for the location
        try:
            latest_data = ProcessedData.objects.filter(location=location).latest('timestamp')
            return Response(ProcessedDataSerializer(latest_data).data)
        except ProcessedData.DoesNotExist:
            return Response({"error": "No data available for this location"}, status=status.HTTP_404_NOT_FOUND)


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # Only admins can create locations
        if not request.user.is_admin:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().post(request, *args, **kwargs)


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        # Only admins can update locations
        if not request.user.is_admin:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        # Only admins can update locations
        if not request.user.is_admin:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        # Only admins can delete locations
        if not request.user.is_admin:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().delete(request, *args, **kwargs)


class DataStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get statistics about the collected data
        
        # Total counts
        raw_data_count = RawData.objects.count()
        processed_data_count = ProcessedData.objects.count()
        location_count = Location.objects.count()
        
        # Data by source
        openaq_count = RawData.objects.filter(source='openaq').count()
        openweather_count = RawData.objects.filter(source='openweather').count()
        
        # Data from last 24 hours
        last_24h = timezone.now() - timezone.timedelta(hours=24)
        last_24h_count = RawData.objects.filter(timestamp__gte=last_24h).count()
        
        return Response({
            'total_raw_data': raw_data_count,
            'total_processed_data': processed_data_count,
            'total_locations': location_count,
            'openaq_data': openaq_count,
            'openweather_data': openweather_count,
            'last_24h_data': last_24h_count,
        })


class AdminDataPurgeView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        # Purge old data (only for admins)
        days = request.data.get('days', 30)
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "Days must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        if days < 1:
            return Response({"error": "Days must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)
        
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        # Delete old raw data
        raw_deleted = RawData.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        
        # Delete old processed data
        processed_deleted = ProcessedData.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        
        return Response({
            'message': f'Successfully purged data older than {days} days',
            'raw_data_deleted': raw_deleted,
            'processed_data_deleted': processed_deleted,
        })
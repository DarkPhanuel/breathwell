from django.urls import path

from .views import (AdminDataPurgeView, DataStatisticsView, LatestDataView,
                    LocationDetailView, LocationListCreateView,
                    ProcessedDataListView, RawDataListView)

urlpatterns = [
    path('raw/', RawDataListView.as_view(), name='raw-data-list'),
    path('processed/', ProcessedDataListView.as_view(), name='processed-data-list'),
    path('latest/', LatestDataView.as_view(), name='latest-data'),
    path('locations/', LocationListCreateView.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('statistics/', DataStatisticsView.as_view(), name='data-statistics'),
    path('purge/', AdminDataPurgeView.as_view(), name='admin-data-purge'),
]
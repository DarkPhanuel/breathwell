from django.contrib import admin

from .models import Location, ProcessedData, RawData


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ('source', 'location', 'timestamp', 'collected_at')
    list_filter = ('source', 'location', 'collected_at')
    search_fields = ('location',)
    date_hierarchy = 'timestamp'


@admin.register(ProcessedData)
class ProcessedDataAdmin(admin.ModelAdmin):
    list_display = ('location', 'timestamp', 'processed_at')
    list_filter = ('location', 'processed_at')
    search_fields = ('location',)
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('raw_data')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'latitude', 'longitude', 'is_active', 'created_at')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'city', 'country')
    list_editable = ('is_active',)
from rest_framework import viewsets

from .models import Crime
from .serializers import CrimeSerializer


class CrimeViewSet(viewsets.ModelViewSet):
    serializer_class = CrimeSerializer

    def get_queryset(self):
        queryset = Crime.objects.last_data()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from is not None:
            queryset = queryset.filter(report_date__gte=date_from)
        if date_to is not None:
            queryset = queryset.filter(report_date__lte=date_to)
        return queryset

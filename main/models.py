from django.db import models


class CrimeManager(models.Manager):
    def last_data(self):
        return self.order_by('date')


class Crime(models.Model):
    crime_id = models.CharField(blank=True, null=True, max_length=9)
    original_crime_type_name = models.CharField(blank=True, null=True, max_length=255)
    objects = CrimeManager()

    class Meta:
        managed = False
        db_table = 'Crime'


class Date(models.Model):
    report_date = models.DateField(blank=True, null=True, max_length=255)
    call_date = models.DateField(blank=True, null=True, max_length=255)
    offense_date = models.DateField(blank=True, null=True, max_length=255)
    call_time = models.CharField(blank=True, null=True, max_length=5)
    call_date_time = models.DateField(blank=True, null=True, max_length=255)
    crime = models.OneToOneField(Crime, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Date'


class Location(models.Model):
    disposition = models.CharField(blank=True, null=True, max_length=255)
    address = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=255)
    state = models.CharField(blank=True, null=True, max_length=255)
    agency_id = models.CharField(blank=True, null=True, max_length=255)
    address_type = models.CharField(blank=True, null=True, max_length=255)
    common_location = models.CharField(blank=True, null=True, max_length=255)
    crime = models.OneToOneField(Crime, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Location'

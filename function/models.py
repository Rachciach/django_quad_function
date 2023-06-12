from django.db import models
from django.contrib.auth.models import User


class QuadFunction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    example = models.CharField(max_length=32, blank=False)
    plot = models.ImageField(upload_to="plots", null=True, blank=True)
    start_x = models.SmallIntegerField(null=True, blank=True, default=-5) # To się odnosi do zakresu towrzenia y na podstawie
    end_x = models.SmallIntegerField(null=True, blank=True, default=5)
    range_plot = models.FloatField(null=True, blank=True, default=0.1)
    x1_range = models.SmallIntegerField(null=True, blank=True)
    x2_range = models.SmallIntegerField(null=True, blank=True)
    y1_range = models.SmallIntegerField(null=True, blank=True)
    y2_range = models.SmallIntegerField(null=True, blank=True)
    private = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.example} {self.date}"

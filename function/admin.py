from django.contrib import admin
from .models import QuadFunction

@admin.register(QuadFunction)
class QuadAdmin(admin.ModelAdmin):
    list_display = ["id", "user","example","private","date", "start_x", "end_x", "range_plot",
                    "x1_range", "x2_range", "y1_range", "y2_range"]
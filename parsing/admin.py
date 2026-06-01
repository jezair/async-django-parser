from django.contrib import admin
from parsing.models import ParserRun


@admin.register(ParserRun)
class ParserRunAdmin(admin.ModelAdmin):
    list_display = ("id","parser_name","status","started_at","finished_at")
    list_filter = ("status",)


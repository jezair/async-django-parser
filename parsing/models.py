from datetime import timezone
from django.utils import timezone
from django.db import models

class ParserRun(models.Model):
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_FINISHED = "finished"
    STATUS_PAUSED = "paused"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RUNNING, "Running"),
        (STATUS_FINISHED, "Finished"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_FAILED, "Failed"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    current_page = models.PositiveIntegerField(default=1)
    total_pages = models.PositiveIntegerField(null=True,blank=True)



    parser_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.parser_name} - {self.status}"


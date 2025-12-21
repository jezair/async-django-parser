from django.db import models

class ParserRun(models.Model):
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RUNNING, "Running"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
    ]

    parser_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.parser_name} #{self.id} - {self.status}"

class Book(models.Model):

    parser_run = models.ForeignKey(ParserRun, on_delete=models.CASCADE, related_name="books")

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.PositiveIntegerField()
    availability = models.BooleanField()
    category = models.CharField(max_length=100)
    detail_url = models.URLField(max_length=500, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["price"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return self.title
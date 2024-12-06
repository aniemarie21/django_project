from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    breed = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.breed if self.breed else 'Unknown'} - {self.uploaded_at}"

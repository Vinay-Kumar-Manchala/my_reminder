from django.db import models


class Jobs(models.Model):
    job_id = models.CharField(primary_key=True)
    email_id = models.CharField(max_length=100)
    cron_schedule = models.CharField(max_length=25)
    created_at = models.DateField()
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"Job ID: {self.job_id}, Email: {self.email_id}"


class Accounts(models.Model):
    email_id = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    created_at = models.DateField()
    is_verified = models.IntegerField(default=0)


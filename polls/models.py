
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class EstimatedWaitTime(models.Model):
	etaMessage = models.CharField(max_length=200)
	pub_date = models.DateTimeField("date published")
	waitingTime = models.IntegerField(default=0)
	def __str__(self):
		return self.etaMessage
	def getWaitEstimate(self):
		return self.waitEstimate
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

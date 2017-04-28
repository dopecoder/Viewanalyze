from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TempRegistration(models.Model):
	user = models.ForeignKey(User)
	email = models.EmailField(null=True, blank=True)
	activation_code = models.CharField(max_length=1000)
	registered_on = models.DateField(auto_now_add=True, auto_now=False)
	activation_status = models.CharField(max_length=5)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s %s -> %s" % (self.user.first_name, self.activation_status, self.registered_on)
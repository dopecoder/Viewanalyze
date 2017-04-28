from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PasswordReset(models.Model):
	user = models.ForeignKey(User)
	email = models.EmailField()
	reset_code = models.CharField(max_length=1000)
	reset_status = models.CharField(max_length=5)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return "%s : %s -> %s" % (self.user.first_name, self.email, self.reset_status)
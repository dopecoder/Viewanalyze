from django.db import models
from django.contrib.auth.models import User
from discussion.models import Analyser
# Create your models here.

class SearchData(models.Model):
	analyser = models.ForeignKey(Analyser, null=True, blank=False)
	search_term = models.CharField(max_length=100)

	def __unicode__(self):
		if self.analyser:
			return "%s -> %s" % (self.analyser.user.email, self.search_term)
		else:
			return "%S -> %s" % ('ANONYMOUS USER', self.search_term)

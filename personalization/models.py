from django.db import models
from discussion import models as disModels

# Create your models here.

#using the Analyser-> we can save the user most wanted or visited tag so that we can show the most wanted tags.

class VisitedTags(models.Model):
	Analyser = models.OneToOneField(disModels.Analyser)
	category = models.ManyToManyField(disModels.Category)
	secondaryTag = models.ManyToManyField(disModels.SecondaryTag)
	tertiaryTag = models.ManyToManyField(disModels.TertiaryTag)



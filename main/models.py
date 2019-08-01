from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User

class Hierarchy(models.Model):
	hierarchy_name = models.CharField(max_length=100)
	description = models.TextField(blank=True, default="scientific taxonomy hierarchy")

	class Meta:
		verbose_name_plural = "Hierarchies"

	def __str__(self):
		return str(self.hierarchy_name)



class Category(models.Model):
	# category
	category_name = models.CharField(max_length=200)
	category_parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
	# timestamp/author
	created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	create_date = models.DateTimeField("Date Created", default=now())

	# taxonomy/description/more...
	hierarchy = models.ForeignKey(Hierarchy, blank=True, null=True, on_delete=models.CASCADE)
	description = models.TextField(blank=True, default="")

	# image/source/credit...
	image_address = models.CharField(max_length=200, blank=True, default="none")
	image_description = models.CharField(max_length=400, default="")
	


	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return str(self.category_name)

#TODO define new Image Model so that image can be added freely


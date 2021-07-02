from django.db import models
from django.core.validators import MinValueValidator


class Complete(models.Model):
	name = models.CharField(max_length=200)
	price = models. FloatField(blank=True, default=0)
	
	url = models.URLField(
		verbose_name= 'url'
	)

	class Meta:
		verbose_name = 'Complete Price'
		verbose_name_plural = 'Complete Prices'


	def __str__(self):
		return f'Name: {self.name}, price: {self.price}'

  
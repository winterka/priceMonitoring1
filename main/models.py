from django.db import models
from django.core.validators import MinValueValidator


class Complete(models.Model):
	name = models.CharField(max_length=200)
	pub_date = models.BigIntegerField(blank=True, default=0)
	price = models. BigIntegerField(blank=True, default=0)

	class Meta:
		verbose_name = 'Complete Price'
		verbose_name_plural = 'Complete Prices'


	def __str__(self):
		return f'Name: {self.name}, date: {self.pub_date}, price: {self.price}'

  
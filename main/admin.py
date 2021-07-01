from django.contrib import admin
from .models import Complete

admin.site.register(Complete)
class ProdAdmin(admin.ModelAdmin):
	list_display = ('title', 'price', 'url')

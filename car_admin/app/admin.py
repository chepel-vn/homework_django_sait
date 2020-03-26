from django.contrib import admin

from .models import Car, Review
from .forms import ReviewAdminForm


class CarAdmin(admin.ModelAdmin):
    fields = ['brand', 'model']
    list_display = ('brand', 'model', 'review_count')
    list_filter = ['brand', 'model']
    search_fields = ('brand', 'model')


class ReviewAdmin(admin.ModelAdmin):
    fields = ['car', 'title', 'text']
    list_display = ('car', 'title')
    list_filter = ['car', 'title']
    search_fields = ('car__brand', 'title')

    form = ReviewAdminForm


admin.site.register(Car, CarAdmin)
admin.site.register(Review, ReviewAdmin)

from django.contrib import admin
from .models import auction,watchlist,Comment, categories
# Register your models here.
admin.site.register(auction)
admin.site.register(watchlist)
admin.site.register(Comment)
admin.site.register(categories)
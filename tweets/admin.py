from django.contrib import admin

# Register your models here.
from .models import Tweet, TweetLike

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ['id', 'content', 'user']

admin.site.register(Tweet, TweetAdmin)
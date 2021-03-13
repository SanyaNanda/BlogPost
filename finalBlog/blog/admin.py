from django.contrib import admin
from .models import Post, Profile,Comment
from mptt.admin import MPTTModelAdmin
# Register your models here.
admin.site.register((Post,Profile))

admin.site.register(Comment, MPTTModelAdmin)

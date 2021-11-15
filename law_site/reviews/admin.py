from django.contrib import admin

# Register your models here.
from .models import Reviews, Acc

admin.site.register(Reviews)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email', 'is_staff')
    list_per_page = 25


admin.site.register(Acc, UserAdmin)
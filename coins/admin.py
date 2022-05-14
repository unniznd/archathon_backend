from django.contrib import admin

from coins.models import ProfileModel, WatchListModel


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','cash_in_hand']

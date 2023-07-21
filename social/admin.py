from django.contrib import admin

from social.models import CustomUser, FundsObject


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "telegram", "points")
    search_fields = ("username", "telegram")
    readonly_fields = ("invite_id", "chat_id", "password")


@admin.register(FundsObject)
class FundsObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "investment_fund", "prize_fund")
    readonly_fields = ("investment_fund", "prize_fund")

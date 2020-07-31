from django.contrib import admin

from webscrapping.models import Type, Dollar


class TypeAdmin(admin.ModelAdmin):
    pass


class DollarAdmin(admin.ModelAdmin):
    list_display = ('origin', 'dollar_type', 'issue_date', 'buy_price', 'sell_price')
    list_filter = ('origin', 'dollar_type__name', 'issue_date')
    search_fields = ('origin', 'buy_price', 'sell_price')


admin.site.register(Type, TypeAdmin)
admin.site.register(Dollar, DollarAdmin)
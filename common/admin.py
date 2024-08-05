from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage


class FlatPageAdmin(FlatPageAdmin):
    """Плоская страница"""

    fieldsets = (
        (None, {'fields': ('url', 'title', 'sites')}),
        (
            ('Advanced options'),
            {
                'fields': ('template_name',),
            },
        ),
    )
    list_display = ('title', 'url')
    list_display_links = ('title',)
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

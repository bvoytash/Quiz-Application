from django.contrib import admin

from explorebg.design.models import Design, LikeDesign


class DesignAdmin(admin.ModelAdmin):
    list_display = ('name', 'design_image')


admin.site.register(Design, DesignAdmin)
admin.site.register(LikeDesign)

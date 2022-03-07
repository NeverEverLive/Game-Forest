from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from forum.models import *


@admin.register(Game)
class GameAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(UserGameRelation)
class UserGameRelationAdmin(ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    pass


@admin.register(Developer)
class DeveloperAdmin(ModelAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(ModelAdmin):
    pass


@admin.register(Sponsor)
class SponsorAdmin(ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    pass


@admin.register(Award)
class AwardAdmin(ModelAdmin):
    pass


@admin.register(AwardGameRelation)
class AwardGameRelationAdmin(ModelAdmin):
    pass


class ScreenshotAdmin(ModelAdmin):
    readonly_fields = ['preview']

    @admin.display(description='Preview')
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.file.url}">')


admin.site.register(Screenshot, ScreenshotAdmin)

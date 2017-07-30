from django.contrib import admin

# Register your models here.
from apps.blog.models import Topic, Category, Tag


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'gmt_created', 'is_deleted')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'creator', 'gmt_created', 'gmt_modified', 'is_deleted')
        }),)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user.username
        super(TopicAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        return ['gmt_created', 'gmt_modified', 'creator']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'gmt_created', 'is_deleted')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'creator', 'gmt_created', 'gmt_modified', 'is_deleted')
        }),)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user.username
        super(CategoryAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        return ['gmt_created', 'gmt_modified', 'creator']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'gmt_created', 'is_deleted')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'creator', 'gmt_created', 'gmt_modified', 'is_deleted')
        }),)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user.username
        super(TagAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        return ['gmt_created', 'gmt_modified', 'creator']







admin.site.register(Topic, TopicAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)


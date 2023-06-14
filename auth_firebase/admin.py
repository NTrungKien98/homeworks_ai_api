from django.contrib import admin
from .models import Question, Choice, Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'name', 'grade', 'level', 'subject')
    list_display_links = ['name']
    def get_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]

admin.site.register(Question, admin.ModelAdmin)
admin.site.register(Choice, admin.ModelAdmin)

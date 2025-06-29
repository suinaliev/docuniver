from django.contrib import admin
from .models import Document, Page, File, Teacher, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'get_level_display', 'get_documents_count', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']
    
    def get_level_display(self, obj):
        return f"{'—' * obj.get_level()} Уровень {obj.get_level() + 1}"
    get_level_display.short_description = 'Уровень'
    
    def get_documents_count(self, obj):
        return obj.get_documents_count()
    get_documents_count.short_description = 'Документов'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'get_file_type_display', 'is_important', 'created_by', 'created_at']
    list_filter = ['category', 'is_important', 'created_at', 'created_by']
    search_fields = ['name', 'notes', 'tags']
    list_editable = ['is_important']
    date_hierarchy = 'created_at'
    
    def get_file_type_display(self, obj):
        file_info = obj.get_file_type()
        return f"{file_info['icon']} {file_info['type']}"
    get_file_type_display.short_description = 'Тип файла'
    
    def save_model(self, request, obj, form, change):
        if not change:  # При создании нового документа
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'position']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'department']
    list_filter = ['department', 'position']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent', 'show_like_document', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['parent', 'show_like_document', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'show_like_sub_document', 'created_at']
    search_fields = ['title']
    list_filter = ['page', 'show_like_sub_document', 'created_at']
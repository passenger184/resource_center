from django.contrib import admin
from .models import UploadedFile, Category, Folder, FileSharing, Tag, FileVersion, Reminder


admin.site.register(Category)
admin.site.register(FileVersion)


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'category', 'uploaded_at')  # Include 'category' in the list display
    list_filter = ('category',)  # Add filter for categories in the admin page

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')  

admin.site.register(Folder, FolderAdmin)
admin.site.register(Tag)


@admin.register(FileSharing)
class FileSharingAdmin(admin.ModelAdmin):
    list_display = ('file', 'shared_by', 'shared_to', 'get_shared_to_email', 'shared_at', 'share_type', 'message')
    search_fields = ('shared_by__username', 'shared_to__username', 'shared_to__email', 'file__name', 'message')
    list_filter = ('share_type', 'shared_at')

    def get_shared_to_email(self, obj):
        return obj.shared_to.email
    get_shared_to_email.short_description = 'Shared to (Email)'

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('file', 'remind_at', 'repeat', 'note', 'user')
    list_filter = ('repeat', 'remind_at')
    search_fields = ('note', 'file__name', 'user__username')
    ordering = ('-remind_at',)


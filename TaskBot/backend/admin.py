from django.contrib import admin

from backend.models import Role, TelegramUser, Task, TaskUser


class CreatedTasksInline(admin.TabularInline):
    verbose_name = "Созданная задача"
    verbose_name_plural = "Созданные задачи"
    model = Task
    fields = ["pretty_info", "status", "lost_deadline_count"]
    readonly_fields = ["pretty_info", "status", "lost_deadline_count"]
    show_change_link = True
    can_delete = False
    extra = 0


class UserTasksInline(admin.TabularInline):
    model = TaskUser
    fields = ["user", "role", "is_done", "is_not_deadline_lost"]
    readonly_fields = ["user", "role", "is_done", "is_not_deadline_lost"]
    can_delete = False
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    list_display = ("short_task", "status", "is_done")
    list_display_links = ("short_task",)
    inlines = (UserTasksInline,)

    def short_task(self, obj):
        return obj.pretty_info

    short_task.short_description = "Задача"


class ExecutorTasksAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "task", "is_done", "is_not_deadline_lost",)
    list_display_links = ("user",)


class TelegramUserAdmin(admin.ModelAdmin):
    inlines = (CreatedTasksInline,)


admin.site.register(Role)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskUser, ExecutorTasksAdmin)

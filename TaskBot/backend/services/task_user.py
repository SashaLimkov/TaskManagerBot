from backend.models import TelegramUser, Task, TaskUser, Role


def create_or_delete_task_user(user: TelegramUser, task: Task, role):
    r = TaskUser.objects.filter(task=task, user=user).first()
    print(r)
    if r:
        r.delete()
    else:
        ro = Role.objects.filter(name=role).first()
        print(ro)
        TaskUser.objects.create(
            user=user,
            task=task,
            role=ro
        )


def create_role(name: str):
    return Role.objects.create(name=name)

import logging
from django.dispatch import receiver
from django.core.mail import send_mail
from app.plugins.signals import task_completed, task_failed, task_removed
from app.plugins.functions import get_current_plugin
from . import email as notification
from . import config
from app.models import Task, Setting

logger = logging.getLogger('app.logger')


@receiver(task_completed)
def handle_task_completed(sender, task_id, **kwargs):
    logger.info("TaskNotification: Task Completed >>>>>>>>>>>>>>>>")
    
    if get_current_plugin(only_active=True) is None:
        return

    config_data = config.load()
    if config_data.get("notify_task_completed") == True:
        task = Task.objects.get(id=task_id)
        settings = Setting.objects.first()

        notification_app_name = config_data['notification_app_name'] or settings.app_name
        task_project_name = task.project.name
        task_name = task.name
        task_status = "task_completed"
        console_output = reverse_output(task.console.output())
        notification.send(notification_app_name, task_project_name, task_name,
                          task_id, task_status, console_output, config_data)


@receiver(task_removed)
def handle_task_removed(sender, task_id, **kwargs):
    logger.info("TaskNotification: Task Removed >>>>>>>>>>>>>>>>")

    if get_current_plugin(only_active=True) is None:
        return

    config_data = config.load()
    if config_data.get("notify_task_removed") == True:
        settings = Setting.objects.first()
        notification_app_name = config_data['notification_app_name'] or settings.app_name
        task_project_name = ""
        task_name = ""
        task_status = "task_removed"
        console_output = ""
        notification.send(notification_app_name, task_project_name, task_name, task_id, task_status, console_output, config_data)


@receiver(task_failed)
def handle_task_failed(sender, task_id, **kwargs):
    logger.info("TaskNotification: Task Failed >>>>>>>>>>>>>>>>")
    
    if get_current_plugin(only_active=True) is None:
        return

    config_data = config.load()
    if config_data.get("notify_task_failed") == True:
        task = Task.objects.get(id=task_id)
        settings = Setting.objects.first()

        notification_app_name = config_data['notification_app_name'] or settings.app_name
        task_project_name = task.project.name
        task_name = task.name
        task_status = "task_failed"
        console_output = reverse_output(task.console.output())
        notification.send(notification_app_name, task_project_name, task_name, task_id, task_status, console_output, config_data)

def hours_minutes_secs(milliseconds):
    if milliseconds == 0 or milliseconds == -1:
        return "-- : -- : --"

    ch = 60 * 60 * 1000
    cm = 60 * 1000
    h = milliseconds // ch
    m = (milliseconds - h * ch) // cm
    s = round((milliseconds - h * ch - m * cm) / 1000)
    pad = lambda n: '0' + str(n) if n < 10 else str(n)

    if s == 60:
        m += 1
        s = 0
    if m == 60:
        h += 1
        m = 0

    return ':'.join([pad(h), pad(m), pad(s)])


def reverse_output(output_string):
    # Split the output string into lines, then reverse the order
    lines = output_string.split('\n')
    lines.reverse()

    # Join the reversed lines back into a single string with newlines
    reversed_string = '\n'.join(lines)

    return reversed_string

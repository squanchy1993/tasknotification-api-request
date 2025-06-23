def load():
    from app.plugins.functions import get_current_plugin
    plugin = get_current_plugin(only_active=True)
    data_store = plugin.get_global_data_store()

    smtp_configuration = {
        'smtp_to_address': data_store.get_string('smtp_to_address', default=""),
        'notification_app_name': data_store.get_string('notification_app_name', default=""),
        'notify_task_completed': data_store.get_bool('notify_task_completed', default=False),
        'notify_task_failed': data_store.get_bool('notify_task_failed', default=False),
        'notify_task_removed': data_store.get_bool('notify_task_removed', default=False)
    }
    return smtp_configuration


def save(data: dict):
    from app.plugins.functions import get_current_plugin
    plugin = get_current_plugin(only_active=True)
    data_store = plugin.get_global_data_store()

    data_store.set_string('smtp_to_address', data.get('smtp_to_address')),
    data_store.set_string('notification_app_name',
                          data.get('notification_app_name')),
    data_store.set_bool('notify_task_completed',
                        data.get('notify_task_completed')),
    data_store.set_bool('notify_task_failed', data.get('notify_task_failed')),
    data_store.set_bool('notify_task_removed', data.get('notify_task_removed'))

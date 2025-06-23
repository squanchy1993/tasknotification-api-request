import logging
from . import config
from urllib import request, parse
import json

logger = logging.getLogger('app.logger')


def send(notification_app_name: str,
         task_project_name: str,
         task_name: str,
         task_id: str,
         task_status: str,
         console_output: str,
         data_config: dict = None):
    if not data_config:
        data_config = config.load()

    # 从表单获取实际数据
    to_address = data_config.get('smtp_to_address')

    # 构建GET请求参数
    data = {
        "notification_app_name": notification_app_name,
        "task_project_name": task_project_name,
        "task_name": task_name,
        "task_id": str(task_id),
        "task_status": task_status,
        "console_output": console_output,
    }

    # 将数据编码为 URL 格式（application/x-www-form-urlencoded）
    try:
        json_data = json.dumps(data).encode('utf-8')
    except Exception as e:
        logger.info(
            "TaskNotification: send error >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>1.2.6"
        )
        logger.info(e)
    # 创建请求对象（指定 URL 和 POST 数据）
    req = request.Request(
        url=to_address,
        data=json_data,  # POST 数据
        method='POST'  # 指定请求方法（默认是 GET）
    )
    # 设置 Content-Type 为 application/json
    req.add_header('Content-Type', 'application/json')

    # 编码参数并构建完整URL
    # 发送请求
    return request.urlopen(req)

from django.conf import settings
from task_sender import TaskSender
from sparrow_cloud.registry.service_discovery import consul_service
from sparrow_cloud.restclient.exception import HTTPException

from functools import lru_cache

#
# @lru_cache(maxsize=None)
# def get_tasks_sender_object(message_backend):
#     task_sender = TaskSender(message_backend)
#     return task_senderml


def get_settings_value(name):
    """获取settings中的配置"""
    value = getattr(settings, name, None)
    if value == '' or value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def send_task(exchange, routing_key, message_code, *args, **kwargs):
    """
    发送实时任务
        参数：
            exchange/routing_key/message_code, 创建消息服务时返回的配置信息
            *args
            **kwargs
        settings配置：

        MESSAGE_SENDER_CONF = {
            "SERVICE_CONF": {
                "ENV_NAME": "DLJFLS_LSDK_LDKEND",
                "VALUE": "xxxxx-svc",
            },
            "API_PATH": "/api/sparrow_task/producer/send/",
        }

    """

    message_conf = get_settings_value("MESSAGE_SENDER_CONF")
    service_addr = consul_service(message_conf['SERVICE_CONF'])
    message_backend = "http://{}{}".format(service_addr, message_conf['API_PATH'])

    task_sender = TaskSender(message_backend)
    try:
        task_resutl = task_sender.send_task(
                exchange=exchange,
                routing_key=routing_key,
                message_code=message_code,
                *args,
                **kwargs
            )
        return task_resutl
    except Exception as ex:
        raise HTTPException(ex)


import logging
from homeassistant.components.notify import BaseNotificationService
from .const import (
    DOMAIN,  # ← ДОБАВЛЕНО
    ATTR_FORMAT,
    ATTR_DISABLE_LINK_PREVIEW,
    ATTR_NOTIFY,
    ATTR_ATTACHMENTS
)

_LOGGER = logging.getLogger(__name__)

async def async_get_service(hass, config, discovery_info=None):
    """Возвращает сервис уведомлений для конкретного чата."""
    if not discovery_info:
        return None
    
    chat_id = discovery_info["chat_id"]
    chat_name = discovery_info["chat_name"]
    api_client = hass.data[DOMAIN]["api_client"]  # ← ОБНОВЛЕНО
    
    return MaxNotificationService(api_client, chat_id, chat_name)

class MaxNotificationService(BaseNotificationService):
    """Сервис уведомлений для одного чата MAX."""
    
    def __init__(self, api_client, chat_id: int, chat_name: str):
        self._api_client = api_client
        self._chat_id = chat_id
        self._chat_name = chat_name
        _LOGGER.debug("Сервис создан для чата: %s (ID: %s)", chat_name, chat_id)
    
    async def async_send_message(self, message="", **kwargs):
        """Отправляет сообщение в чат."""
        if not message:
            _LOGGER.warning("Пустое сообщение для чата %s", self._chat_id)
            return
        
        format_type = kwargs.get(ATTR_FORMAT)
        disable_link_preview = kwargs.get(ATTR_DISABLE_LINK_PREVIEW, False)
        notify = kwargs.get(ATTR_NOTIFY, True)
        
        result = await self._api_client.send_message(
            chat_id=self._chat_id,
            message=message,
            format_type=format_type,
            disable_link_preview=disable_link_preview,
            notify=notify
        )
        
        if result:
            _LOGGER.debug("Сообщение в чат '%s' отправлено", self._chat_name)
        else:
            _LOGGER.error("Не удалось отправить сообщение в чат '%s'", self._chat_name)
        
        return result

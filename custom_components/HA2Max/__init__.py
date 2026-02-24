import logging
import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform

from .max_api import MaxApiClient

DOMAIN = "ha2max"  # ← ОБНОВЛЕНО
CONF_CHAT_NAMES = "chat_names"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({  # ← ОБНОВЛЕНО
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Optional(CONF_CHAT_NAMES, default={}): vol.Schema({
            cv.positive_int: cv.string,
        }),
    })
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Настройка компонента из configuration.yaml."""
    if DOMAIN not in config:  # ← ОБНОВЛЕНО
        return True

    conf = config[DOMAIN]  # ← ОБНОВЛЕНО
    access_token = conf[CONF_ACCESS_TOKEN]
    
    api_client = MaxApiClient(access_token)
    
    bot_info = await api_client.get_bot_info()
    if not bot_info:
        _LOGGER.error("Не удалось получить информацию о боте. Проверьте токен.")
        return False
    
    bot_name = bot_info.get("first_name", "Unknown")
    _LOGGER.info("Бот '%s' успешно авторизован", bot_name)
    
    chats = await api_client.get_chats()
    if not chats:
        _LOGGER.warning("Бот не состоит ни в одном групповом чате")
        chats = []
    
    hass.data[DOMAIN] = {  # ← ОБНОВЛЕНО
        "api_client": api_client,
        "bot_info": bot_info,
        "chats": chats,
        "chat_names": conf[CONF_CHAT_NAMES]
    }
    
    for chat in chats:
        chat_id = chat.get("id")
        if not chat_id:
            continue
            
        chat_name = chat.get("name", f"Чат {chat_id}")
        if chat_id in conf[CONF_CHAT_NAMES]:
            chat_name = conf[CONF_CHAT_NAMES][chat_id]
        
        await async_load_platform(
            hass,
            "notify",
            DOMAIN,  # ← ОБНОВЛЕНО
            {
                "chat_id": chat_id,
                "chat_name": chat_name,
                "chat_data": chat
            },
            config
        )
    
    _LOGGER.info("Создано %s сервисов уведомлений", len(chats))
    
    async def async_update_chats(call):
        """Сервис для обновления списка чатов."""
        new_chats = await api_client.get_chats()
        hass.data[DOMAIN]["chats"] = new_chats  # ← ОБНОВЛЕНО
        _LOGGER.info("Список чатов обновлён. Найдено %s чатов", len(new_chats))
    
    hass.services.async_register(DOMAIN, "update_chats", async_update_chats)  # ← ОБНОВЛЕНО
    
    return True

async def async_unload(hass: HomeAssistant) -> bool:
    """Выгрузка компонента."""
    hass.data.pop(DOMAIN, None)  # ← ОБНОВЛЕНО
    return True

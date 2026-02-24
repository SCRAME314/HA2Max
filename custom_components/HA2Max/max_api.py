import logging
import aiohttp
from typing import List, Dict, Any, Optional

_LOGGER = logging.getLogger(__name__)

class MaxApiClient:
    """Клиент для работы с API MAX."""
    
    def __init__(self, access_token: str):
        self._access_token = access_token
        self._headers = {
            "Authorization": self._access_token,
            "Content-Type": "application/json"
        }
        self._base_url = "https://platform-api.max.ru"
    
    async def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """Получение информации о боте (GET /me)."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self._base_url}/me",
                    headers=self._headers
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    _LOGGER.error("Ошибка получения информации о боте: %s", resp.status)
                    return None
        except Exception as e:
            _LOGGER.error("Ошибка: %s", e)
            return None
    
    async def get_chats(self) -> List[Dict[str, Any]]:
        """Получение списка всех групповых чатов (GET /chats)."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self._base_url}/chats",
                    headers=self._headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("chats", [])
                    _LOGGER.error("Ошибка получения чатов: %s", resp.status)
                    return []
        except Exception as e:
            _LOGGER.error("Ошибка: %s", e)
            return []
    
    async def send_message(
        self,
        chat_id: int,
        message: str,
        format_type: Optional[str] = None,
        disable_link_preview: bool = False,
        notify: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Отправка сообщения в чат (POST /messages)."""
        url = f"{self._base_url}/messages"
        params = {"chat_id": chat_id}
        
        if disable_link_preview:
            params["disable_link_preview"] = "true"
        
        payload = {
            "text": message,
            "notify": notify
        }
        
        if format_type:
            payload["format"] = format_type
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers=self._headers,
                    params=params
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    response_text = await resp.text()
                    _LOGGER.error(
                        "Ошибка отправки: HTTP %s. Ответ: %s",
                        resp.status, response_text
                    )
                    return None
        except Exception as e:
            _LOGGER.error("Ошибка: %s", e)
            return None

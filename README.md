markdown

# MAX Messenger для Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Интеграция для отправки уведомлений из Home Assistant в мессенджер MAX.

## Установка

### Через HACS (рекомендуется)
1. Добавьте этот репозиторий как пользовательский в HACS
2. Найдите "MAX Messenger" в разделе Integrations
3. Установите и перезагрузите Home Assistant

### Вручную
1. Скопируйте папку `HA2Max` в `custom_components/`
2. Перезагрузите Home Assistant

## Конфигурация

Добавьте в `configuration.yaml`:

```yaml
max_messenger:
  access_token: "ВАШ_ТОКЕН_БОТА"
  # Опционально: пользовательские имена для чатов
  chat_names:
    123456789: "Важные оповещения"
    987654321: "Логи системы"
Получение токена

    Перейдите на MAX для партнёров

    Создайте бота

    Получите токен в разделе "Интеграция → Получить токен"

    Добавьте бота в нужные групповые чаты

Использование

После установки интеграция автоматически найдёт все чаты с ботом и создаст сервисы:

    notify.max_chat_123456789

    notify.max_chat_987654321

Пример автоматизации:
yaml

automation:
  - alias: "Уведомление о движении"
    trigger:
      platform: state
      entity_id: binary_sensor.motion
      to: "on"
    action:
      service: notify.max_chat_123456789
      data:
        message: "⚠️ Обнаружено движение в {{ now().strftime('%H:%M') }}"
        format: "markdown"

Поддерживаемые параметры сообщений
yaml

service: notify.max_chat_123456789
data:
  message: "Текст сообщения"
  format: "markdown"  # или "html"
  disable_link_preview: true  # без превью ссылок
  notify: false  # без звукового уведомления

Логирование

При проблемах включите расширенное логирование:
yaml

logger:
  default: warning
  logs:
    custom_components.max_messenger: debug

text


**`hacs.json`:**
```json
{
  "name": "MAX Messenger",
  "render_readme": true,
  "homeassistant": "2023.8.0",
  "zip_release": true,
  "filename": "max_messenger.zip",
  "country": ["RU", "BY", "KZ", "UA"],
  "icon": "mdi:chat"
}

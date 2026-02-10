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
1. Скопируйте папку `max_messenger` в `custom_components/`
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

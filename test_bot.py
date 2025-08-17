#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности Telegram бота
"""

import asyncio
from telegram_bot import start, get_name, get_age, cancel, help_command
from telegram import Update, User, Message, Chat
from telegram.ext import ContextTypes
from unittest.mock import AsyncMock, MagicMock

class MockUpdate:
    """Мок для Update объекта"""
    def __init__(self, text="", user_first_name="Тест"):
        self.message = MockMessage(text, user_first_name)

class MockMessage:
    """Мок для Message объекта"""
    def __init__(self, text="", user_first_name="Тест"):
        self.text = text
        self.effective_user = MockUser(user_first_name)
        self.reply_text = AsyncMock()

class MockUser:
    """Мок для User объекта"""
    def __init__(self, first_name="Тест"):
        self.first_name = first_name

class MockContext:
    """Мок для Context объекта"""
    def __init__(self):
        self.user_data = {}
    
    def clear(self):
        self.user_data.clear()

async def test_bot_functions():
    """Тестируем основные функции бота"""
    print("🧪 Тестирование функций Telegram бота...\n")
    
    # Тест 1: Команда start
    print("1. Тестируем команду /start")
    update = MockUpdate()
    context = MockContext()
    
    result = await start(update, context)
    print(f"   Результат: {result}")
    print(f"   Сообщение отправлено: {update.message.reply_text.called}")
    print()
    
    # Тест 2: Получение имени
    print("2. Тестируем получение имени")
    update = MockUpdate("Иван")
    context = MockContext()
    
    result = await get_name(update, context)
    print(f"   Результат: {result}")
    print(f"   Имя сохранено: {context.user_data.get('name')}")
    print(f"   Сообщение отправлено: {update.message.reply_text.called}")
    print()
    
    # Тест 3: Получение корректного возраста
    print("3. Тестируем получение корректного возраста")
    update = MockUpdate("25")
    context = MockContext()
    context.user_data['name'] = 'Иван'
    
    result = await get_age(update, context)
    print(f"   Результат: {result}")
    print(f"   Сообщение отправлено: {update.message.reply_text.called}")
    print()
    
    # Тест 4: Получение некорректного возраста
    print("4. Тестируем получение некорректного возраста")
    update = MockUpdate("abc")
    context = MockContext()
    context.user_data['name'] = 'Иван'
    
    result = await get_age(update, context)
    print(f"   Результат: {result}")
    print(f"   Сообщение отправлено: {update.message.reply_text.called}")
    print()
    
    # Тест 5: Команда help
    print("5. Тестируем команду /help")
    update = MockUpdate()
    context = MockContext()
    
    await help_command(update, context)
    print(f"   Сообщение отправлено: {update.message.reply_text.called}")
    print()
    
    # Тест 6: Команда cancel
    print("6. Тестируем команду /cancel")
    update = MockUpdate()
    context = MockContext()
    context.user_data['name'] = 'Иван'
    
    result = await cancel(update, context)
    print(f"   Результат: {result}")
    print(f"   Данные очищены: {len(context.user_data) == 0}")
    print(f"   Сообщение отправлено: {update.message.reply_text.called}")
    print()
    
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    # Запускаем тесты
    asyncio.run(test_bot_functions())
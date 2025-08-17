#!/bin/bash

# Скрипт для запуска Telegram бота

echo "🤖 Запуск Telegram бота для сбора имени и возраста..."
echo "=================================================="

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.7+"
    exit 1
fi

# Проверяем наличие pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip3"
    exit 1
fi

# Проверяем наличие файла конфигурации
if [ ! -f "config.py" ]; then
    echo "❌ Файл config.py не найден"
    exit 1
fi

# Проверяем, настроен ли токен
if grep -q "YOUR_BOT_TOKEN" config.py; then
    echo "⚠️  ВНИМАНИЕ: Токен бота не настроен!"
    echo "   Откройте файл config.py и замените 'YOUR_BOT_TOKEN' на ваш токен"
    echo "   Получить токен можно у @BotFather в Telegram"
    echo ""
    echo "   Пример настройки:"
    echo "   BOT_TOKEN = '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz'"
    echo ""
    read -p "Продолжить без настройки токена? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Запуск отменен"
        exit 1
    fi
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Ошибка установки зависимостей"
    exit 1
fi

echo "✅ Зависимости установлены"
echo ""

# Запускаем бота
echo "🚀 Запуск бота..."
python3 telegram_bot.py
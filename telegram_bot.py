import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from config import BOT_TOKEN, LOG_LEVEL, LOG_FORMAT

# Включаем логирование
logging.basicConfig(
    format=LOG_FORMAT,
    level=getattr(logging, LOG_LEVEL)
)

# Получаем логгер
logger = logging.getLogger(__name__)

# Состояния для разговора
NAME, AGE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинаем разговор и запрашиваем имя"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я бот для сбора информации. Давайте познакомимся!\n\n"
        "Как вас зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получаем имя и запрашиваем возраст"""
    user_name = update.message.text
    context.user_data['name'] = user_name
    
    await update.message.reply_text(
        f"Приятно познакомиться, {user_name}! 😊\n\n"
        "Теперь скажите, сколько вам лет?",
        reply_markup=ReplyKeyboardRemove()
    )
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получаем возраст и завершаем разговор"""
    try:
        age = int(update.message.text)
        if age < 0 or age > 150:
            await update.message.reply_text(
                "Пожалуйста, введите корректный возраст (от 0 до 150 лет)."
            )
            return AGE
        
        name = context.user_data.get('name', 'Неизвестно')
        
        await update.message.reply_text(
            f"Отлично! 📝\n\n"
            f"Ваши данные:\n"
            f"• Имя: {name}\n"
            f"• Возраст: {age} лет\n\n"
            f"Спасибо за информацию! 🙏\n\n"
            f"Чтобы начать заново, используйте команду /start",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Очищаем данные пользователя
        context.user_data.clear()
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "Пожалуйста, введите возраст числом (например: 25)."
        )
        return AGE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяем разговор"""
    await update.message.reply_text(
        "Разговор отменен. До свидания! 👋\n\n"
        "Чтобы начать заново, используйте команду /start",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показываем справку"""
    help_text = """
🤖 **Справка по боту**

**Доступные команды:**
/start - Начать разговор и ввести данные
/help - Показать эту справку
/cancel - Отменить текущий разговор

**Как использовать:**
1. Отправьте /start
2. Введите ваше имя
3. Введите ваш возраст
4. Получите подтверждение введенных данных

**Возможности:**
• Сбор имени и возраста
• Валидация введенных данных
• Простой и понятный интерфейс
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Запускаем бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаем обработчик разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))

    # Запускаем бота
    print("Бот запущен...")
    print(f"Используется токен: {BOT_TOKEN[:10]}...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from random import randint

# Вставь сюда свой токен
TOKEN = "8004356050:AAFOFNMsrne6nPWkXd-m0n21q8GfeLcCeUg"


# Функция для команды /start
async def start(update: Update, context) -> None:
    await update.message.reply_text("Привет! Я ваш бот.")


# Функция для команды /help
async def help_command(update: Update, context) -> None:
    help_text = (
        "/start - Начать общение с ботом\n"
        "/help - Показать это сообщение\n"
        "/random <число1> <число2> - Сгенерировать случайное число в диапазоне от числа1 до числа2\n"
        "Просто отправьте текст, и бот повторит его."
    )
    await update.message.reply_text(help_text)


# Функция обработки команды /random с диапазоном
async def random_command(update: Update, context) -> None:
    try:
        # Получаем аргументы команды (диапазон чисел)
        args = context.args
        if len(args) != 2:
            raise ValueError("Нужно указать два числа, например: /random 1 100")

        a, b = map(int, args)

        if a > b:
            raise ValueError("Первое число должно быть меньше или равно второму.")

        # Генерируем случайное число в диапазоне [a, b]
        random_number = randint(a, b)
        await update.message.reply_text(f"Ваше случайное число: {random_number}")

    except ValueError as e:
        # В случае ошибки сообщаем пользователю, что ввод некорректен
        await update.message.reply_text(f"Ошибка: {e}. Пожалуйста, введите два целых числа через пробел.")


# Функция обработки текстовых сообщений (эхо бот)
async def echo(update: Update, context) -> None:
    await update.message.reply_text(update.message.text)  # Отправляем то же сообщение обратно


# Установка доступных команд для отображения в виде всплывающего меню
async def set_commands(application):
    commands = [
        BotCommand("start", "Начать общение с ботом"),
        BotCommand("help", "Показать описание доступных команд"),
        BotCommand("random", "Сгенерировать случайное число, укажите диапазон (например, /random 1 100)")
    ]
    await application.bot.set_my_commands(commands)


# Основная функция для запуска бота
if __name__ == "__main__":
    # Создаем приложение с использованием ApplicationBuilder
    app = ApplicationBuilder().token(TOKEN).build()


    # Добавляем команду установки доступных команд при старте
    async def on_startup(application):
        await set_commands(application)


    # Обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))  # Обработчик команды /help
    app.add_handler(CommandHandler("random", random_command))  # Обработчик команды /random
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # Обработчик текстовых сообщений (эхо)

    # Запускаем установку команд через job_queue
    app.job_queue.run_once(on_startup, 0)

    # Запускаем polling
    app.run_polling()

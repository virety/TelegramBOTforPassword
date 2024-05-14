import threading
import logging
import keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_bot():
    try:
        keyboard.bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"An error occurred in the bot polling: {e}")


if __name__ == '__main__':
    try:
        threading.Thread(target=run_bot).start()
    except Exception as e:
        logger.error(f"An error occurred while starting the bot thread: {e}")

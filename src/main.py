import os
import sys

from telegram import Update
from telegram.ext import Application
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.logging.helpers import create_logger
from core.logging.handlers import ErrorHandlerTG
from core.database.mongodb import ping_mongo_server
from core.settings import config
from app import bot_handlers


logger = create_logger("telegram")


async def init_application(application: Application) -> None:
    """Функция, которая вызывается при запуске бота

    :param application: Класс со всеми видами обновлений бота
    :type application: Application
    """
    logger.addHandler(ErrorHandlerTG())
    await ping_mongo_server()


def main():
    """Главная функция запуска бота
    """
    builder = Application.builder()
    builder.token(config.TG_TOKEN).post_init(init_application)

    application = builder.build()
    application.add_handlers(bot_handlers)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


class MyHandler(FileSystemEventHandler):
    """Handler для отслеживания изменения файлов проекта
    """
    def on_modified(self, event):
        if not (event.src_path.endswith('.py') or event.src_path.endswith('.env')):
            return
        
        if not config.RELOAD:
            return
        
        logger.warning(f"Restarting app, changes in: {event.src_path}")
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        main()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()    
        
from .telegram.start import start_handlers as __start_handlers
from .telegram.agregate import agregate_handlers as __agregate_handlers


bot_handlers = [
    *__start_handlers,
    *__agregate_handlers
]
from tg.config import PREFIX
from tg.tdlib import Tdlib
from tg.models import Model

from typing import Callable, Dict


class message:
    _registry: Dict[str, Callable] = {}

    def __init__(
        self, message: str, telegram: Tdlib, model: Model, prefix: str = PREFIX
    ) -> None:
        self.telegram = telegram
        self.message = message.strip()
        self.prefix = prefix
        self.model = model

    @classmethod
    def command(cls, *names: str):
        def decorator(func: Callable):
            for name in names:
                cls._registry[name] = func
            return func

        return decorator

    def dispatch(self) -> bool:
        """Возвращает True, если команда была выполнена, False иначе"""
        if not self.message.startswith(self.prefix):
            return False

        parts = self.message[len(self.prefix) :].split()
        if not parts:
            return False

        cmd_name, *args = parts
        if cmd_name in self._registry:
            self._registry[cmd_name](self.telegram, self.model, *args)
            return True
        return False

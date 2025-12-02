import time
import logging
import threading
from tg.core.weather import get_weather
from tg.models import Model
from tg.tdlib import Tdlib, ChatAction
from tg.commands import message
from tg.core.system import get_system_info
from tg.accounts import AccountManager

log = logging.getLogger(__name__)


@message.command("typing")
def typing_handler(telegram: Tdlib, model: Model, *args) -> None:
    chat_id = model.chats.id_by_index(model.current_chat)

    duration = 60

    if args:
        try:
            duration = int(args[0])
        except ValueError:
            return

    def typing_simulation():
        """
        Кароче функция для того что-бы фейково печатать в чате
        """
        start = time.time()
        if isinstance(chat_id, int):
            while time.time() - start < duration:
                telegram.send_chat_action(
                    chat_id=chat_id, action=ChatAction.chatActionTyping
                )
                time.sleep(3)
        if isinstance(chat_id, int):
            telegram.send_chat_action(
                chat_id=chat_id, action=ChatAction.chatActionCancel
            )

    threading.Thread(target=typing_simulation, daemon=True).start()


@message.command("note")
def note_handler(telegram: Tdlib, model: Model, *args) -> None:
    chat_id = model.chats.id_by_index(model.current_chat)

    duration = 60

    if args:
        try:
            duration = int(args[0])
        except ValueError:
            return

    def note_simulation():
        start = time.time()
        if isinstance(chat_id, int):
            while time.time() - start < duration:
                telegram.send_chat_action(
                    chat_id=chat_id, action=ChatAction.chatActionRecordingVideoNote
                )
                time.sleep(3)

            telegram.send_chat_action(
                chat_id=chat_id, action=ChatAction.chatActionCancel
            )

    threading.Thread(target=note_simulation, daemon=True).start()


@message.command("system")
def system_handler(telegram: Tdlib, model: Model) -> None:
    chat_id = model.chats.id_by_index(model.current_chat)
    log.info(f"📤 Отправляем в фиксированный chat_id: {chat_id}")

    system = get_system_info()
    caption = "<b>System Info:</b>\n<pre>"
    for key, value in system.items():
        caption += f"{key:<15}: {value}\n"
    caption += "</pre>"
    if isinstance(chat_id, int):
        telegram.send_message(chat_id=chat_id, text=caption, parse_mode="HTML")


@message.command("weather")
def weather_handler(telegram: Tdlib, model: Model, *args) -> None:
    chat_id = model.chats.id_by_index(model.current_chat)

    def get_weather_thread():
        if isinstance(chat_id, int):
            if not args:
                telegram.send_message(chat_id, "Укажите город: /weather <город>")
                return

            city: str = " ".join(args)

            weather_info = get_weather(city=city)

            telegram.send_message(
                chat_id=chat_id,
                text=f"<pre>{weather_info}</pre>",
                parse_mode="HTML",
            )

    threading.Thread(target=get_weather_thread, daemon=True).start()


@message.command("account")
def account_handler(telegram: Tdlib, model: Model, *args) -> None:
    """Manage accounts: /account list|add|remove <phone>|set <phone>"""
    manager = AccountManager()

    if not args:
        chat_id = model.chats.id_by_index(model.current_chat)
        if isinstance(chat_id, int):
            current_phone, _ = manager.get_current_account()
            text = f"Current account: {current_phone}\n\n"
            text += "Available accounts:\n"
            for phone in manager.get_all_accounts():
                text += f"  • {phone}\n"
            text += "\nUsage:\n"
            text += "  /account list - list all accounts\n"
            text += "  /account add <phone> - add new account\n"
            text += "  /account set <phone> - switch account\n"
            text += "  /account remove <phone> - remove account\n"
            telegram.send_message(chat_id, text)
        return

    action = args[0]
    chat_id = model.chats.id_by_index(model.current_chat)

    if not isinstance(chat_id, int):
        return

    if action == "list":
        text = "Available accounts:\n"
        current_phone, _ = manager.get_current_account()
        for phone in manager.get_all_accounts():
            marker = "✓" if phone == current_phone else " "
            text += f"  [{marker}] {phone}\n"
        telegram.send_message(chat_id, text)

    elif action == "add" and len(args) > 1:
        phone = args[1]
        if not phone.startswith("+"):
            phone = "+" + phone
        manager.add_account(phone)
        telegram.send_message(
            chat_id,
            f"Account added: {phone}\nNote: You need to restart the client to use this account.",
        )

    elif action == "set" and len(args) > 1:
        phone = args[1]
        if not phone.startswith("+"):
            phone = "+" + phone
        if manager.set_current_account(phone):
            telegram.send_message(
                chat_id,
                f"Account switched to: {phone}\nNote: You need to restart the client to apply changes.",
            )
        else:
            telegram.send_message(chat_id, f"Account not found: {phone}")

    elif action == "remove" and len(args) > 1:
        phone = args[1]
        if not phone.startswith("+"):
            phone = "+" + phone
        manager.remove_account(phone)
        telegram.send_message(chat_id, f"Account removed: {phone}")

    else:
        text = "Invalid usage. Try:\n"
        text += "  /account list\n"
        text += "  /account add <phone>\n"
        text += "  /account set <phone>\n"
        text += "  /account remove <phone>\n"
        telegram.send_message(chat_id, text)

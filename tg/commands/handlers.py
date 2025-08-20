import threading
import time
from tg.models import Model
from tg.tdlib import Tdlib, ChatAction
from tg.commands import message


@message.command("typing")
def moon_handler(telegram: Tdlib, model: Model) -> None:
    chat_id = model.chats.id_by_index(model.current_chat)

    def typing_simulation():
        start = time.time()
        while time.time() - start < 60:
            telegram.send_chat_action(
                chat_id=chat_id, action=ChatAction.chatActionTyping
            )
            time.sleep(3)

        telegram.send_chat_action(chat_id=chat_id, action=ChatAction.chatActionCancel)

        # model.send_message(text=f"*Chat id: {chat_id}*")

    threading.Thread(target=typing_simulation, daemon=True).start()

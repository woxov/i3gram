import logging.handlers
import signal
import threading
from curses import window, wrapper
from functools import partial
from types import FrameType
from typing import Optional

from tg import config, update_handlers, utils
from tg.accounts import AccountManager
from tg.account_selector import AccountSelector
from tg.controllers import Controller
from tg.models import Model
from tg.tdlib import Tdlib
from tg.views import ChatView, MsgView, StatusView, View

log = logging.getLogger(__name__)


def run(tg: Tdlib, stdscr: window) -> None:
    # handle ctrl+c, to avoid interrupting tg when subprocess is called
    def interrupt_signal_handler(sig: int, frame: Optional[FrameType]) -> None:
        # TODO: draw on status pane: to quite press <q>
        log.info("Interrupt signal is handled and ignored on purpose.")

    signal.signal(signal.SIGINT, interrupt_signal_handler)

    model = Model(tg)
    status_view = StatusView(stdscr)
    msg_view = MsgView(stdscr, model)
    chat_view = ChatView(stdscr, model)
    view = View(stdscr, chat_view, msg_view, status_view)
    controller = Controller(model, view, tg)

    # hanlde resize of terminal correctly
    signal.signal(signal.SIGWINCH, controller.resize_handler)

    for msg_type, handler in update_handlers.handlers.items():
        tg.add_update_handler(msg_type, partial(handler, controller))

    thread = threading.Thread(target=controller.run)
    thread.daemon = True
    thread.start()

    controller.draw()


def parse_args() -> None:
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version"):
        import tg

        print("Terminal Telegram client")
        print("Version:", tg.__version__)
        exit(0)


def select_account(stdscr: window) -> Optional[str]:
    """Show account selector and return selected phone"""
    manager = AccountManager()
    
    if not manager.has_accounts():
        return None
    
    accounts = manager.get_all_accounts()
    if len(accounts) == 1:
        return accounts[0]
    
    selector = AccountSelector(accounts)
    return selector.run(stdscr)


def main() -> None:
    parse_args()
    utils.cleanup_cache()
    
    # Initialize account manager
    manager = AccountManager()
    
    # If no accounts, create from config
    if not manager.has_accounts():
        phone = config.PHONE
        if not phone:
            print("Enter your phone number in international format (including country code)")
            phone = input("phone> ")
            if not phone.startswith("+"):
                phone = "+" + phone
        
        enc_key = config.ENC_KEY if hasattr(config, 'ENC_KEY') else ""
        manager.add_account(phone, enc_key)
    
    # Show account selector if multiple accounts
    if manager.has_accounts():
        accounts = manager.get_all_accounts()
        if len(accounts) > 1:
            selected_phone = wrapper(select_account)
            if selected_phone == "quit" or selected_phone is None:
                exit(0)
            manager.set_current_account(selected_phone)
        else:
            manager.set_current_account(accounts[0])
    
    phone, enc_key = manager.get_current_account()
    if not phone:
        print("No account selected")
        exit(1)
    
    tg = Tdlib(
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        phone=phone,
        database_encryption_key=enc_key,
        files_directory=config.FILES_DIR,
        tdlib_verbosity=config.TDLIB_VERBOSITY,
        library_path=config.TDLIB_PATH,
    )
    tg.login()

    utils.setup_log()
    utils.set_shorter_esc_delay()

    wrapper(partial(run, tg))


if __name__ == "__main__":
    main()

"""Account manager for multi-account support"""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple

from tg import config

log = logging.getLogger(__name__)

ACCOUNTS_FILE = os.path.join(config.CONFIG_DIR, "accounts.json")


class AccountManager:
    """Manages multiple Telegram accounts"""

    def __init__(self) -> None:
        self.accounts: Dict[str, str] = {}  # phone -> enc_key mapping
        self.current_phone: Optional[str] = None
        self._load_accounts()

    def _load_accounts(self) -> None:
        """Load accounts from file"""
        if os.path.exists(ACCOUNTS_FILE):
            try:
                with open(ACCOUNTS_FILE, "r") as f:
                    data = json.load(f)
                    self.accounts = data.get("accounts", {})
                    self.current_phone = data.get("current_phone")
            except Exception as e:
                log.warning(f"Failed to load accounts: {e}")
                self.accounts = {}

    def _save_accounts(self) -> None:
        """Save accounts to file"""
        os.makedirs(config.CONFIG_DIR, exist_ok=True)
        try:
            with open(ACCOUNTS_FILE, "w") as f:
                json.dump({
                    "accounts": self.accounts,
                    "current_phone": self.current_phone,
                }, f, indent=2)
        except Exception as e:
            log.error(f"Failed to save accounts: {e}")

    def add_account(self, phone: str, enc_key: str = "") -> None:
        """Add a new account"""
        if not phone.startswith("+"):
            phone = "+" + phone
        self.accounts[phone] = enc_key
        if not self.current_phone:
            self.current_phone = phone
        self._save_accounts()
        log.info(f"Account added: {phone}")

    def remove_account(self, phone: str) -> None:
        """Remove an account"""
        if phone in self.accounts:
            del self.accounts[phone]
            if self.current_phone == phone:
                self.current_phone = next(iter(self.accounts), None)
            self._save_accounts()
            log.info(f"Account removed: {phone}")

    def set_current_account(self, phone: str) -> bool:
        """Set current active account"""
        if phone in self.accounts:
            self.current_phone = phone
            self._save_accounts()
            return True
        return False

    def get_current_account(self) -> Tuple[Optional[str], str]:
        """Get current account phone and encryption key"""
        if not self.current_phone:
            return None, ""
        return self.current_phone, self.accounts.get(self.current_phone, "")

    def get_all_accounts(self) -> List[str]:
        """Get list of all account phone numbers"""
        return list(self.accounts.keys())

    def has_accounts(self) -> bool:
        """Check if there are any accounts"""
        return len(self.accounts) > 0

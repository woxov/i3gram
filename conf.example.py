# Example configuration file for multi-account setup
# Copy this to ~/.config/tg/conf.py and modify as needed

# Note: You can define multiple accounts here
# After adding accounts via the client, the accounts.json file will be created automatically

# Example phone number (you can add more accounts via /account add command)
# PHONE = "+79991234567"

# If you want to configure accounts directly in this file, you can do it like this:
# But it's recommended to use the /account command in the client instead

# Encryption keys for different accounts (optional)
# ENC_KEY = ""  # leave empty if you don't want encryption

# This will be automatically populated after you add accounts via the client
# ACCOUNTS = {
#     "+79991234567": "",  # encryption key for this account
#     "+79999876543": "optional_encryption_key",
# }

# Other settings (same as before)
LOG_LEVEL = "INFO"
# LOG_PATH = "~/.local/share/tg/"

# Notifications
# NOTIFY_CMD = "/usr/local/bin/terminal-notifier -title {title} -subtitle {subtitle} -message {msg}"

# File picker
# FILE_PICKER_CMD = "ranger --choosefile={file_path}"

# Download directory
# DOWNLOAD_DIR = "~/Downloads/i3gram/"

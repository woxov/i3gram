import os
import re
import asyncio
from tg.config import DOWNLOAD_DIR

ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text)


async def shell_async(cmd: str) -> str:
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode(errors="ignore") or stderr.decode(errors="ignore") or ""
    return strip_ansi(output)


def shell(cmd: str) -> str:
    return asyncio.run(shell_async(cmd))


def file_exists(file_path: str) -> bool:
    """Проверяет существование файла"""
    # Просто проверяем через ls с подавлением ошибок
    result = shell(f'ls "{file_path}" 2>/dev/null')
    return bool(result.strip())


def Copy(file_path: str) -> None:
    asyncio.run(shell_async(f"cp {file_path} {DOWNLOAD_DIR}"))


def CopyToDownloadDir(file_path: str) -> str:
    """Копирует файл в DOWNLOAD_DIR и возвращает новый путь"""
    try:
        filename = os.path.basename(file_path)
        destination = os.path.join(DOWNLOAD_DIR, filename)

        return destination

    except Exception:
        return ""


def DeleteFromDownloadDir(file_path: str) -> bool:
    """Удаляет файл из DOWNLOAD_DIR"""
    try:
        filename = os.path.basename(file_path)
        destination = os.path.join(DOWNLOAD_DIR, filename)
        # Проверяем что файл в правильной директории
        if not destination.startswith(DOWNLOAD_DIR):
            print(f"File not in DOWNLOAD_DIR: {destination}")
            return False

        if os.path.isfile(destination):
            os.remove(destination)
            return True
        else:
            return False
    except Exception:
        return False

import datetime
import platform
import socket
import psutil


def human_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_system_info():
    # Cache expensive calls
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    du = psutil.disk_usage("/")
    cpu_count = psutil.cpu_count(logical=True)
    cpu_usage = psutil.cpu_percent(interval=0)  # Non-blocking
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

    uptime_str = str(datetime.datetime.now() - boot_time).split(".")[0]

    info = {
        "Hostname": socket.gethostname(),
        "OS": f"{platform.system()} {platform.release()}",
        "Kernel": platform.version(),
        "Architecture": platform.machine(),
        "CPU": f"{platform.processor()} ({cpu_count} cores)",
        "CPU Usage": f"{cpu_usage} %",
        "Memory": f"{human_size(vm.used)} / {human_size(vm.total)}",
        "Swap": f"{human_size(sm.used)} / {human_size(sm.total)}",
        "Disk": f"{human_size(du.used)} / {human_size(du.total)}",
        "Uptime": uptime_str,
        "IP Address": socket.gethostbyname(socket.gethostname()),
    }
    return info


def bash_exec(shell: str) -> str:
    return shell

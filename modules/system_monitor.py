import psutil


def status_sistema():

    cpu = psutil.cpu_percent(interval=1)

    memoria = psutil.virtual_memory().percent

    disco = psutil.disk_usage("/").percent

    return f"CPU: {cpu}% | MEMÓRIA: {memoria}% | DISCO: {disco}%"
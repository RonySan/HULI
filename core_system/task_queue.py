from core_system.task import Task


class TaskQueue:
    def __init__(self):
        self.fila = []
        self.historico = []

    def adicionar(self, task: Task):
        self.fila.append(task)
        return task

    def proxima(self):
        if not self.fila:
            return None
        return self.fila.pop(0)

    def concluir(self, task):
        self.historico.append(task)

    def status(self):
        return {
            "pendentes": len(self.fila),
            "historico": len(self.historico),
            "fila": [t.to_dict() for t in self.fila],
            "ultimas": [t.to_dict() for t in self.historico[-5:]],
        }


task_queue = TaskQueue()


def obter_task_queue():
    return task_queue
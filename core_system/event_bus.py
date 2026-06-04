from datetime import datetime


class EventBus:

    def __init__(self):
        self.eventos = []

    def emitir(self, evento, origem="sistema", dados=None):

        item = {
            "evento": evento,
            "origem": origem,
            "dados": dados,
            "data": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M:%S")
        }

        self.eventos.append(item)

        if len(self.eventos) > 100:
            self.eventos = self.eventos[-100:]

    def listar(self):
        return self.eventos[-20:]

    def ultimo(self):
        if not self.eventos:
            return None

        return self.eventos[-1]


event_bus = EventBus()


def emitir_evento(evento, origem="sistema", dados=None):
    event_bus.emitir(evento, origem, dados)


def listar_eventos():
    return event_bus.listar()


def ultimo_evento():
    return event_bus.ultimo()
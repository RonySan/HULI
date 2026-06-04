class SkillManager:

    def __init__(self):

        self.skills = {

            "memoria": {
                "descricao": "Gerencia memórias, lembretes e histórico.",
                "modulos": [
                    "memory.py",
                    "smart_memory.py"
                ]
            },

            "voz": {
                "descricao": "Reconhecimento e síntese de voz.",
                "modulos": [
                    "voice.py",
                    "voice_listener.py",
                    "voice_natural.py"
                ]
            },

            "visao": {
                "descricao": "Leitura de tela e OCR.",
                "modulos": [
                    "vision.py",
                    "vision_advanced.py",
                    "vision_actions.py"
                ]
            },

            "automacao": {
                "descricao": "Mouse, teclado e automações.",
                "modulos": [
                    "automation.py",
                    "pc_control.py"
                ]
            },

            "missoes": {
                "descricao": "Missões e tarefas automáticas.",
                "modulos": [
                    "missions.py"
                ]
            },

            "jarvis": {
                "descricao": "Modo operacional avançado.",
                "modulos": [
                    "jarvis_mode.py"
                ]
            },

            "ia": {
                "descricao": "IA local e online.",
                "modulos": [
                    "brain.py",
                    "ia_router.py"
                ]
            }
        }

    def listar(self):
        return list(self.skills.keys())

    def obter(self, nome):
        return self.skills.get(nome.lower())


skill_manager = SkillManager()


def listar_skills():
    return skill_manager.listar()


def obter_skill(nome):
    return skill_manager.obter(nome)
class SkillManager:

    def __init__(self):
        self.skills = {
            "core": {
                "descricao": "Núcleo principal da H.U.L.I. Controla inicialização, execução, loops e comandos.",
                "modulos": [
                    "core/huli.py",
                    "core_system/kernel.py",
                    "core_system/context.py",
                    "core_system/router.py",
                    "core_system/brain.py",
                    "core_system/event_bus.py",
                ],
                "comandos": [
                    "status kernel",
                    "contexto",
                    "eventos",
                ]
            },

            "voz": {
                "descricao": "Controle de fala, escuta manual, escuta natural e voz da H.U.L.I.",
                "modulos": [
                    "voice.py",
                    "voice_mode.py",
                    "voice_listener.py",
                    "voice_natural.py",
                    "services/voice_service.py",
                ],
                "comandos": [
                    "ativar voz",
                    "desativar voz",
                    "status voz",
                    "voz",
                    "ouvir",
                    "ouvir natural",
                ]
            },

            "visao": {
                "descricao": "Leitura de tela, OCR, identificação de textos e clique por texto.",
                "modulos": [
                    "vision.py",
                    "vision_advanced.py",
                    "vision_actions.py",
                    "vision_ai.py",
                    "services/vision_service.py",
                ],
                "comandos": [
                    "tirar print",
                    "ler tela",
                    "o que tem na tela",
                    "encontrar na tela entrar",
                    "clicar quando aparecer entrar",
                ]
            },

            "automacao": {
                "descricao": "Controle de mouse, teclado, atalhos, digitação e ações físicas no PC.",
                "modulos": [
                    "automation.py",
                    "services/automation_service.py",
                ],
                "comandos": [
                    "clicar",
                    "duplo clique",
                    "clique direito",
                    "mover mouse para 500 300",
                    "digitar texto",
                    "pressionar enter",
                ]
            },

            "sistema": {
                "descricao": "Controle do Windows, programas, sites, som, Wi-Fi, Bluetooth e status do sistema.",
                "modulos": [
                    "pc_control.py",
                    "windows_control.py",
                    "system_control.py",
                    "system_monitor.py",
                    "services/system_service.py",
                ],
                "comandos": [
                    "abrir chrome",
                    "abrir vscode",
                    "abrir bluetooth",
                    "conectar bluetooth MUNDIAL",
                    "abrir wifi",
                    "abrir som",
                    "status sistema",
                ]
            },

            "ia": {
                "descricao": "Camada de IA online/offline, fallback inteligente e respostas naturais.",
                "modulos": [
                    "ai.py",
                    "nlp.py",
                    "services/ai_service.py",
                ],
                "comandos": [
                    "perguntas abertas",
                    "conversa natural",
                    "resumo da conversa",
                    "limpar contexto",
                ]
            },

            "memoria": {
                "descricao": "Memória simples, categorizada, tarefas, ideias, agenda e lembranças.",
                "modulos": [
                    "memory.py",
                    "knowledge.py",
                    "services/memory_service.py",
                ],
                "comandos": [
                    "anota comprar pão",
                    "mostra tarefas",
                    "mostra ideias",
                    "mostra agenda",
                    "o que voce lembra",
                    "aprenda que",
                ]
            },

            "memoria_inteligente": {
                "descricao": "Memória de pessoas, preferências e contexto pessoal.",
                "modulos": [
                    "smart_memory.py",
                    "services/memory_service.py",
                ],
                "comandos": [
                    "lembre que gisele é minha namorada",
                    "quem é gisele",
                    "listar pessoas",
                    "memoria inteligente",
                ]
            },

            "lembretes": {
                "descricao": "Lembretes reais com horário, monitoramento e alerta automático.",
                "modulos": [
                    "reminder_engine.py",
                    "scheduler.py",
                    "services/reminder_service.py",
                ],
                "comandos": [
                    "me lembre de tomar agua as 18:30",
                    "listar lembretes",
                    "apagar lembretes",
                ]
            },

            "medicamentos": {
                "descricao": "Cálculo de horários de medicamentos, doses, dias, PDF e TXT.",
                "modulos": [
                    "medication.py",
                ],
                "comandos": [
                    "remedio de 8 em 8 horas a partir das 6:30 por 10 dias",
                    "gerar pdf de remedio de 8 em 8 horas",
                    "exportar horarios de remedio em txt",
                ]
            },

            "missoes": {
                "descricao": "Execução de missões rápidas, salvas e multietapas.",
                "modulos": [
                    "missions.py",
                    "multi_missions.py",
                ],
                "comandos": [
                    "missao pesquisar python",
                    "missao abrir github",
                    "abrir github depois pesquise python",
                    "listar missoes",
                ]
            },

            "rotinas": {
                "descricao": "Rotinas nomeadas para abrir vários recursos e executar sequências.",
                "modulos": [
                    "routines.py",
                ],
                "comandos": [
                    "criar rotina trabalho com chrome, vscode",
                    "modo trabalho",
                    "listar rotinas",
                    "mostrar rotina trabalho",
                ]
            },

            "habitos": {
                "descricao": "Aprendizado de padrões, sugestões e autoexecução baseada em comportamento.",
                "modulos": [
                    "habits.py",
                    "autoexec.py",
                    "autopilot.py",
                ],
                "comandos": [
                    "mostrar habitos",
                    "limpar habitos",
                    "listar autoexecucoes",
                    "limpar autoexecucoes",
                ]
            },

            "seguranca": {
                "descricao": "Proteção, confirmação de comandos sensíveis e controle de permissões.",
                "modulos": [
                    "protection.py",
                    "identity.py",
                    "core/security.py",
                ],
                "comandos": [
                    "protecao on",
                    "protecao off",
                    "status protecao",
                ]
            },

            "perfil": {
                "descricao": "Perfil do usuário, preferências e configurações pessoais.",
                "modulos": [
                    "user_profile.py",
                    "settings_manager.py",
                ],
                "comandos": [
                    "definir nome rony",
                    "meu perfil",
                    "mostrar configuracoes",
                    "definir empresa Impulso Digital",
                    "definir bluetooth padrao MUNDIAL",
                ]
            },

            "logs_backup": {
                "descricao": "Registro de logs, histórico, backups e rastreabilidade operacional.",
                "modulos": [
                    "logger.py",
                    "history.py",
                    "backup.py",
                ],
                "comandos": [
                    "mostrar logs",
                    "limpar logs",
                    "historico",
                    "criar backup",
                    "listar backups",
                ]
            },

            "documentos": {
                "descricao": "Busca em documentos internos e base de conhecimento.",
                "modulos": [
                    "docs.py",
                    "knowledge.py",
                ],
                "comandos": [
                    "buscar docs",
                    "o que voce sabe sobre",
                    "listar conhecimento",
                ]
            },

            "jarvis": {
                "descricao": "Modo operacional avançado com voz, contexto e comportamento mais ativo.",
                "modulos": [
                    "jarvis_mode.py",
                    "core_system/kernel.py",
                ],
                "comandos": [
                    "ativar jarvis",
                    "desativar jarvis",
                    "status jarvis",
                    "status kernel",
                ]
            },

            "social": {
                "descricao": "Interações sociais, cumprimentos, apresentações e recados.",
                "modulos": [
                    "social.py",
                ],
                "comandos": [
                    "huli se apresenta para gisele",
                    "huli cumprimenta gisele",
                    "huli diz oi pra gisele",
                    "huli elogia gisele",
                    "huli mande um recado para gisele dizendo que eu amo ela",
                ]
            },

            "emocional": {
                "descricao": "Modo emocional/íntimo leve, médio e intenso, com tom mais humano.",
                "modulos": [
                    "intimate_mode.py",
                ],
                "comandos": [
                    "modo intimo",
                    "nivel intimidade medio",
                    "nivel intimidade intenso",
                    "status intimidade",
                ]
            },

            "painel": {
                "descricao": "Painel visual, status geral e painel neural da H.U.L.I.",
                "modulos": [
                    "status_center.py",
                    "huli_panel.py",
                ],
                "comandos": [
                    "status geral",
                    "status huli",
                    "painel neural",
                ]
            },
        }

    def listar(self):
        return list(self.skills.keys())

    def obter(self, nome):
        return self.skills.get(nome.lower().strip())

    def status(self):
        return {
            "total_skills": len(self.skills),
            "skills": list(self.skills.keys())
        }


skill_manager = SkillManager()


def listar_skills():
    return skill_manager.listar()


def obter_skill(nome):
    return skill_manager.obter(nome)


def status_skills():
    return skill_manager.status()
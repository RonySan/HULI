from core_system.task import Task
from core_system.task_queue import obter_task_queue
from core_system.intent_analyzer import analisar_intencao
from core_system.event_bus import emitir_evento


def criar_tasks_por_intencao(comando):
    analise = analisar_intencao(comando)
    intencao = analise.get("intencao")
    dados = analise.get("dados", {})

    tasks = []

    if intencao == "trabalho":
        tasks.append(Task(
            nome="Executar rotina de trabalho",
            descricao="Iniciar ambiente de trabalho do Rony",
            intencao=intencao,
            prioridade="alta",
            dados=dados
        ))

    elif intencao == "documentacao":
        tasks.append(Task(
            nome="Gerar documentação",
            descricao="Gerar documentação automática da H.U.L.I",
            intencao=intencao,
            prioridade="normal"
        ))

    elif intencao == "reflexao_projeto":
        tasks.append(Task(
            nome="Refletir sobre projeto",
            descricao="Gerar estado atual do projeto H.U.L.I",
            intencao=intencao,
            prioridade="normal"
        ))

    elif intencao == "planejamento_dia":
        tasks.append(Task(
            nome="Planejar o dia",
            descricao="Gerar resumo de agenda, tarefas e pendências",
            intencao=intencao,
            prioridade="normal"
        ))

    return analise, tasks


def executar_task(task):
    task.iniciar()

    try:
        if task.intencao == "trabalho":
            from modules.routines import executar_rotina
            from modules.pc_control import abrir_programa, abrir_site, abrir_pasta, executar_comando_terminal, abrir_arquivo

            ok, resposta = executar_rotina(
                task.dados.get("rotina", "trabalho"),
                abrir_programa,
                abrir_site,
                abrir_pasta,
                executar_comando_terminal,
                abrir_arquivo
            )

            task.concluir(resposta)
            return resposta

        if task.intencao == "documentacao":
            from core_system.auto_documentation import gerar_documentacao_md
            resposta = gerar_documentacao_md()
            task.concluir(resposta)
            return resposta

        if task.intencao == "reflexao_projeto":
            from core_system.reflection_engine import estado_do_projeto
            resposta = estado_do_projeto()
            task.concluir(resposta)
            return resposta

        if task.intencao == "planejamento_dia":
            from services.planner_service import resumo_do_dia
            resposta = resumo_do_dia()
            task.concluir(resposta)
            return resposta

        task.falhar("Intenção não suportada.")
        return "Não consegui executar essa intenção ainda."

    except Exception as e:
        task.falhar(e)
        return f"Erro ao executar task '{task.nome}': {e}"


def orquestrar(comando):
    analise, tasks = criar_tasks_por_intencao(comando)

    if not tasks:
        return None

    fila = obter_task_queue()

    emitir_evento(
        "orchestrator_intencao_detectada",
        origem="orchestrator",
        dados=analise
    )

    respostas = "🧠 Orchestrator H.U.L.I\n\n"
    respostas += f"Intenção detectada: {analise.get('intencao')}\n"
    respostas += f"Confiança: {int(analise.get('confianca', 0) * 100)}%\n\n"

    for task in tasks:
        fila.adicionar(task)
        resposta = executar_task(task)
        fila.concluir(task)

        respostas += f"✅ Task: {task.nome}\n"
        respostas += f"Resultado: {resposta}\n\n"

    return respostas


def status_orchestrator():
    fila = obter_task_queue()
    dados = fila.status()

    resposta = "🧠 Status do Orchestrator\n\n"
    resposta += f"Tasks pendentes: {dados['pendentes']}\n"
    resposta += f"Tasks no histórico: {dados['historico']}\n\n"

    if dados["ultimas"]:
        resposta += "Últimas tasks:\n"
        for task in dados["ultimas"]:
            resposta += f"• {task['nome']} — {task['status']}\n"

    return resposta
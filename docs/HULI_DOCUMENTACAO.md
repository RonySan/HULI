# H.U.L.I — Documentação Automática

Humano Único Leal Inteligente

Gerado em: 21/06/2026 17:26:36

## 1. Status do Kernel

- **usuario**: Rony
- **proprietario**: True
- **modo_conversa**: False
- **escuta_continua**: False
- **jarvis**: False
- **voz**: False
- **ultimo_comando**: None
- **threads**: ['agendamentos', 'lembretes']
- **uptime**: 0:00:08.714123

## 2. Contexto Atual

- **usuario_atual**: Rony
- **proprietario**: True
- **visitante**: False
- **empresa**: Impulso Digital
- **assistente**: H.U.L.I
- **voz_ativa**: False
- **modo_jarvis**: False
- **modo_conversa**: False
- **escuta_continua**: False
- **modo_protecao**: INATIVO
- **personalidade**: huli
- **bluetooth_padrao**: mundial
- **ultimo_comando**: None
- **ultima_resposta**: None
- **ultima_intencao**: None
- **iniciado_em**: 21/06/2026 17:26:28
- **uptime_kernel**: 0:00:08.715704
- **threads**: ['agendamentos', 'lembretes']

## 3. Skills Registradas

Total de skills: 21

### CORE

Núcleo principal da H.U.L.I. Controla inicialização, execução, loops e comandos.

**Módulos:**
- core/huli.py
- core_system/kernel.py
- core_system/context.py
- core_system/router.py
- core_system/brain.py
- core_system/event_bus.py

**Comandos principais:**
- `status kernel`
- `contexto`
- `eventos`

### VOZ

Controle de fala, escuta manual, escuta natural e voz da H.U.L.I.

**Módulos:**
- voice.py
- voice_mode.py
- voice_listener.py
- voice_natural.py
- services/voice_service.py

**Comandos principais:**
- `ativar voz`
- `desativar voz`
- `status voz`
- `voz`
- `ouvir`
- `ouvir natural`

### VISAO

Leitura de tela, OCR, identificação de textos e clique por texto.

**Módulos:**
- vision.py
- vision_advanced.py
- vision_actions.py
- vision_ai.py
- services/vision_service.py

**Comandos principais:**
- `tirar print`
- `ler tela`
- `o que tem na tela`
- `encontrar na tela entrar`
- `clicar quando aparecer entrar`

### AUTOMACAO

Controle de mouse, teclado, atalhos, digitação e ações físicas no PC.

**Módulos:**
- automation.py
- services/automation_service.py

**Comandos principais:**
- `clicar`
- `duplo clique`
- `clique direito`
- `mover mouse para 500 300`
- `digitar texto`
- `pressionar enter`

### SISTEMA

Controle do Windows, programas, sites, som, Wi-Fi, Bluetooth e status do sistema.

**Módulos:**
- pc_control.py
- windows_control.py
- system_control.py
- system_monitor.py
- services/system_service.py

**Comandos principais:**
- `abrir chrome`
- `abrir vscode`
- `abrir bluetooth`
- `conectar bluetooth MUNDIAL`
- `abrir wifi`
- `abrir som`
- `status sistema`

### IA

Camada de IA online/offline, fallback inteligente e respostas naturais.

**Módulos:**
- ai.py
- nlp.py
- services/ai_service.py

**Comandos principais:**
- `perguntas abertas`
- `conversa natural`
- `resumo da conversa`
- `limpar contexto`

### MEMORIA

Memória simples, categorizada, tarefas, ideias, agenda e lembranças.

**Módulos:**
- memory.py
- knowledge.py
- services/memory_service.py

**Comandos principais:**
- `anota comprar pão`
- `mostra tarefas`
- `mostra ideias`
- `mostra agenda`
- `o que voce lembra`
- `aprenda que`

### MEMORIA_INTELIGENTE

Memória de pessoas, preferências e contexto pessoal.

**Módulos:**
- smart_memory.py
- services/memory_service.py

**Comandos principais:**
- `lembre que gisele é minha namorada`
- `quem é gisele`
- `listar pessoas`
- `memoria inteligente`

### LEMBRETES

Lembretes reais com horário, monitoramento e alerta automático.

**Módulos:**
- reminder_engine.py
- scheduler.py
- services/reminder_service.py

**Comandos principais:**
- `me lembre de tomar agua as 18:30`
- `listar lembretes`
- `apagar lembretes`

### MEDICAMENTOS

Cálculo de horários de medicamentos, doses, dias, PDF e TXT.

**Módulos:**
- medication.py

**Comandos principais:**
- `remedio de 8 em 8 horas a partir das 6:30 por 10 dias`
- `gerar pdf de remedio de 8 em 8 horas`
- `exportar horarios de remedio em txt`

### MISSOES

Execução de missões rápidas, salvas e multietapas.

**Módulos:**
- missions.py
- multi_missions.py

**Comandos principais:**
- `missao pesquisar python`
- `missao abrir github`
- `abrir github depois pesquise python`
- `listar missoes`

### ROTINAS

Rotinas nomeadas para abrir vários recursos e executar sequências.

**Módulos:**
- routines.py

**Comandos principais:**
- `criar rotina trabalho com chrome, vscode`
- `modo trabalho`
- `listar rotinas`
- `mostrar rotina trabalho`

### HABITOS

Aprendizado de padrões, sugestões e autoexecução baseada em comportamento.

**Módulos:**
- habits.py
- autoexec.py
- autopilot.py

**Comandos principais:**
- `mostrar habitos`
- `limpar habitos`
- `listar autoexecucoes`
- `limpar autoexecucoes`

### SEGURANCA

Proteção, confirmação de comandos sensíveis e controle de permissões.

**Módulos:**
- protection.py
- identity.py
- core/security.py

**Comandos principais:**
- `protecao on`
- `protecao off`
- `status protecao`

### PERFIL

Perfil do usuário, preferências e configurações pessoais.

**Módulos:**
- user_profile.py
- settings_manager.py

**Comandos principais:**
- `definir nome rony`
- `meu perfil`
- `mostrar configuracoes`
- `definir empresa Impulso Digital`
- `definir bluetooth padrao MUNDIAL`

### LOGS_BACKUP

Registro de logs, histórico, backups e rastreabilidade operacional.

**Módulos:**
- logger.py
- history.py
- backup.py

**Comandos principais:**
- `mostrar logs`
- `limpar logs`
- `historico`
- `criar backup`
- `listar backups`

### DOCUMENTOS

Busca em documentos internos e base de conhecimento.

**Módulos:**
- docs.py
- knowledge.py

**Comandos principais:**
- `buscar docs`
- `o que voce sabe sobre`
- `listar conhecimento`

### JARVIS

Modo operacional avançado com voz, contexto e comportamento mais ativo.

**Módulos:**
- jarvis_mode.py
- core_system/kernel.py

**Comandos principais:**
- `ativar jarvis`
- `desativar jarvis`
- `status jarvis`
- `status kernel`

### SOCIAL

Interações sociais, cumprimentos, apresentações e recados.

**Módulos:**
- social.py

**Comandos principais:**
- `huli se apresenta para gisele`
- `huli cumprimenta gisele`
- `huli diz oi pra gisele`
- `huli elogia gisele`
- `huli mande um recado para gisele dizendo que eu amo ela`

### EMOCIONAL

Modo emocional/íntimo leve, médio e intenso, com tom mais humano.

**Módulos:**
- intimate_mode.py

**Comandos principais:**
- `modo intimo`
- `nivel intimidade medio`
- `nivel intimidade intenso`
- `status intimidade`

### PAINEL

Painel visual, status geral e painel neural da H.U.L.I.

**Módulos:**
- status_center.py
- huli_panel.py

**Comandos principais:**
- `status geral`
- `status huli`
- `painel neural`


## 4. Arquitetura Atual

- Kernel
- Context
- Event Bus
- Session Memory
- Skill Manager
- Planner Service
- Personality Engine
- Conversational Brain
- Reflection Engine
- Auto Help Engine
- Neural Scanner

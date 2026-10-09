# Monitoramento — runtime do worker

```text
ID = MON-WORKER
STATUS = ARCHITECTURAL CONTRACT
PRODUCTION_WORKER = NOT_IMPLEMENTED / NOT_DEPLOYED
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL PROCESS
IMPLEMENTER_TARGET = LUNA
RUNTIME_CONTRACT_REVIEW = MON-RUNTIME-CONTRACT-CLOSURE / 2026-10-09
LOCAL_RUNTIME_CLOSURE = CLOSED / CONTRACT_ONLY / implementation and validation absent
CONTRACT_STATUS = CLOSED
CURRENT_ADJUDICATION = MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION / final section below
READY_NOW = NO / dependencies and operational gates remain
```

## Separação de execução

Probe contínuo pertence a processo/worker dedicado, independente de request/response web. Django/browser exibe estado persistido e pode solicitar leituras; não varre câmeras, não mantém conexão contínua nem dispara probe ao renderizar tela. Captura permanece fluxo separado e sob demanda.

## Ciclo do runtime

O núcleo local implementa scheduler due-based com fila limitada, concorrência limitada, timeout, ciclo de drain/shutdown, idempotência por alvo, estado operacional e lease/fencing portável. O runtime de produção deverá: descobrir candidatos elegíveis em lote; agendar due com jitter; adquirir ownership; executar adapter; reduzir resultado; persistir completion com fencing; liberar lease; registrar telemetria sanitizada; e fechar de forma previsível ao desligar.

ADR-019 não escolheu tecnologia de fila, processo, cron/scheduler externo, Celery/Redis/RQ, supervisor, quantidade de instâncias ou política de restart. O BC-02 abaixo escolhe somente o processo/entrypoint local; deployment de produção continua não comprovado. O serviço não deve executar como root nem conta admin, e precisa de egress e identidade próprios.

## Readiness e falha

Saúde de processo/worker é diferente de estado de câmera. Falha ao iniciar, ausência de heartbeat, banco indisponível ou fila saturada deve aparecer como falha do subsistema e deixar estado da câmera envelhecer para stale; não gerar OFFLINE em massa. Readiness deve impedir admissão se configuração de segurança/DB/adapters não estiver pronta. Stop controla admissão, drena ou cancela dentro de deadline e nunca interpreta cancelamento como falha de probe.

Referências: ADR-019/020/021; `cameras/monitoramento/scheduler.py`; `config/asgi.py`/`wsgi.py` não comprovam deployment dedicado.

## BC-02 — entrypoint e loop local

Implementar management command `run_monitoring_worker` como processo separado
de WSGI/ASGI, com um event loop asyncio e `DueScheduler` existente. Um
processo recebe `worker_id` aleatório não secreto no startup; não aceita
`owner_id`, destino, URL ou segredo em argumento CLI. Cada ciclo carrega
configuração tipada, lista candidatos em lote, aplica eligibility/perfil/
target policy, agenda due com jitter/queue bounds existentes, reclama lease,
executa adapter dentro do deadline, reduz e persiste completion com
owner/epoch/config_generation. Fechar conexões Django em fronteiras sync/async
e após falha. Só uma instância local é default; múltiplas dependem de teste
PostgreSQL/topologia. Nenhum probe roda em request web.

Readiness antes de admitir: DB acessível, `MonitoringConfig` válido, policy
de destino válida, provider de chave funcional para targets autenticados,
adapter exigido disponível e compatibilidade SUPPORTED. Ausência falha
fechado com estado operacional do worker, sem OFFLINE de câmera. Liveness
local é processo ativo e loop responsivo; heartbeat monotônico/UTC em
observability a cada `heartbeat_seconds`. Um supervisor externo decide restart
com backoff em produção; command termina com exit não zero em falha fatal de
preflight, sem loop de restart interno infinito. Erro transitório de DB
pausa admissão, registra falha, tenta novo ciclo após intervalo bounded e
deixa freshness envelhecer; não inventa resultados.

SIGTERM/SIGINT pedem shutdown do scheduler, param admissão, aguardam
`shutdown_timeout_seconds`, cancelam restantes, liberam lease condicionalmente
e fecham adapters/DB. CANCELLED é neutro. `--once` e dependências injetáveis
são apenas mecanismo de teste local, não modo de operação produtivo. Logs
estruturados usam MON-OBS. Deploy, conta de serviço, egress e supervisor
reais pertencem a PROD-TOPO.

```text
MODEL_CHANGE = NONE; EstadoMonitoramento/lease already exist
MIGRATION_REQUIRED = NO
EXPECTED_MODELS = EstadoMonitoramento existing
RELATIONSHIPS = existing Camera/lease
CONSTRAINTS = owner/epoch/config_generation already enforced
INDEXES = existing due/lease indexes
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = stop command; do not mutate camera state on stop
EXPECTED_PRIMARY_FILES = cameras/monitoramento/scheduler.py;
                         cameras/monitoramento/repository.py
EXPECTED_NEW_FILES = cameras/management/commands/run_monitoring_worker.py;
                     cameras/monitoramento/runtime.py
EXPECTED_TEST_FILES = cameras/test_monitoramento_worker_runtime.py;
                      cameras/test_monitoramento_scheduler_laboratorio.py
SHARED_FILES = monitoring scheduler/repository; no concurrent writer in wave
STOP_AND_ESCALATE_TO_SOL_IF = scheduler cannot honor bounded shutdown/lease;
                              production process topology becomes necessary locally
```

Acceptance criteria:

1. Com fakes e config válida, `--once` admite due, respeita queue/concurrency,
   persiste somente completion autoritativa e emite heartbeat/sinais seguros.
2. Sem DB/key/policy/adapter obrigatório, preflight falha fechado sem socket,
   sem OFFLINE e com exit/diagnóstico operacional identificável.
3. Em SIGTERM durante tentativa, admissão cessa, cancelamento é neutro e
   owner antigo não libera lease de novo owner; restart não duplica transição.

## MON-RUNTIME-CONTRACT-CLOSURE — revisão de 2026-10-09

```text
SCOPE = DOCUMENTATION_ONLY / LOCAL RUNTIME
SOURCE_HEAD = 5bd22b06891a9cfa3886aa2dd2fbe0bf97e125c9
SOURCE_BRANCH = codex/mon-runtime-contract-closure
SOURCE_BASELINE = origin/master / locally recorded ref equals SOURCE_HEAD
EXECUTION_MODE = DIRECT
IMPLEMENTATION_AUTHORIZED = NO
PRODUCTION_CODE_AND_TESTS_CHANGED = NO
REAL_CAMERA_ACCESS = NO
COMMIT_AND_PUSH = NOT_AUTHORIZED
MATERIAL_DECISIONS = MR-01; MR-02; MR-03
MATERIAL_DECISION_STATUS = RECONCILED_PROPOSAL / NOT_FINAL_APPROVAL
MR_01_REVIEW = APPROVABLE_WITH_CONSTRAINTS / clauses below
MR_02_REVIEW = CHANGES_REQUIRED / bounded retirement boundary pending
MR_03_REVIEW = APPROVABLE_WITH_CONSTRAINTS / clauses below
CONTRACT_STATUS = OPEN / NOT_CLOSED
LOCAL_ARCHITECTURAL_CLOSURE = PENDING_USER_ADJUDICATION
```

Este adendo distingue requisitos derivados do core e das authorities vigentes
de recomendações novas. Não promove recomendação a decisão humana. O texto
BC-02 acima continua sendo a arquitetura local aprovada; suas afirmações de
readiness não comprovam execução contínua, dependências integradas ou produção.
O parecer humano desta revisão é APPROVABLE_WITH_CONSTRAINTS para MR-01/MR-03
e CHANGES_REQUIRED para MR-02. Ele autoriza a reconciliação documental, não
constitui aprovação final das cláusulas novas. A redação reconciliada abaixo
substitui a proposta de reciclagem obrigatória a cada 10.000 tentativas,
retirada por ausência de justificativa mensurável. Após aprovação explícita,
registrar a adjudicação antes de declarar fechamento arquitetural. A aprovação
documental não autoriza implementar.

### Evidência no checkout e limites de prontidão

| Fonte | Fato observado | Consequência para o contrato |
|---|---|---|
| `cameras/monitoramento/scheduler.py`, `DueScheduler` | Scheduler síncrono; não cria nem supervisiona tasks de probe; `complete()`/`cancel()` também podem iniciar tentativas da fila | Runtime deve reconciliar `active_attempts` após cada mutação, além de `TickReport.started` |
| Mesmo arquivo, `_start_from_queue()` | Impede início em DRAINING/STOPPED; não impede por si só em DEGRADED | Runtime precisa impedir I/O de novos probes enquanto readiness falhar; testar tentativas promovidas internamente |
| Mesmo arquivo, `request_shutdown()`/`cancel()` | Cancelam bookkeeping/liberam ownership; não cancelam task nem fecham adapter | Shutdown exige coordenação explícita entre scheduler, tasks e recursos |
| Mesmo arquivo, `_attempts`/`_candidate_by_attempt` | Registros terminais permanecem até `restart()`; mapas por câmera também permanecem no processo | Queue/concurrency bounded não comprovam memória bounded de um processo contínuo |
| `repository.py`, `list_due()` | Retorna até `limit`, mas itera queryset sem filtro SQL de vencimento nem paginação bounded; pode chamar `enter_scope()` | Descoberta não é estritamente somente leitura; limitar retorno não prova custo de leitura ou fairness |
| `repository.py`, `store()` | Persistência transacional de memória, estado, transição e intervalo; com lease compara owner/epoch e geração exata, e libera lease no mesmo update | Uma única completion autoritativa pelo scheduler; não implementar segundo reducer ou segundo escritor |
| `schemas.py`, `MonitoringConfig` | Objeto imutável; scheduler recebe configuração no construtor; sem API pública de hot reload | Recarregar configuração a cada ciclo requer contrato de substituição, não alteração privada do objeto |
| `confirmation.py`, `reduce_confirmation()` | Memória versionada, timestamps fora de ordem/iguais e categorias fechadas | Reusar `ConfirmationMemory` persistida e política existente, preservando a ordem e barreiras atuais |
| `integracao/configuration.py` | Configuração técnica/IP têm produtores de geração; isso não é a versão de política de confirmação nem epoch de ownership | Capturar geração do alvo e revalidá-la; não reutilizar geração como identidade de processo/policy |

Neste HEAD não foram encontrados command `run_monitoring_worker`, runtime MON,
provider `MonitoringTelemetry` ou `CameraHealthSnapshot`/integração automática
A-D. A implementação RTSP existente não satisfaz sozinha CAM-INT-05/CAM-HEALTH.
O DAG em `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md`
exige MON-OBS + CAM-INT-05 + CAM-HEALTH + core MON antes de MON-WORKER.
CAM-INT-04 e worktree MON-OBS externos não foram consultados; nenhum status
externo foi promovido a implementação neste checkout.

### Contrato de composição derivado das authorities atuais

1. Manter o command separado de WSGI/ASGI, um event loop e uma instância local
   por default. Reusar `DueScheduler`, `DjangoMonitoringRepository`,
   `ConfirmationPolicy` e `ConfirmationMemory`. Não adicionar fila externa,
   modelos, migrations ou writer paralelo nesta slice.
2. Injetar a mesma instância de repository em `confirmation_port` e
   `ownership_port`; `DueScheduler.__init__` exige essa identidade para
   completion/release atômicos. Gerar `service_instance_id` por startup;
   o scheduler acrescenta UUID ao seu owner interno. Não aceitar owner/epoch
   fornecidos por CLI/browser e não forçar equivalência entre worker ID e owner.
3. Serializar mutações do scheduler e chamadas de repository em uma fronteira
   ORM síncrona controlada, fora do event loop de I/O. Não compartilhar conexão
   Django entre threads nem manter transação aberta enquanto o adapter roda.
   Fechar conexões nas fronteiras de execução e após falha. A forma concreta
   da ponte sync/async será validada na implementação autorizada.
4. Manter registro de tasks por `attempt_id`, com uma task por tentativa ACTIVE
   e no máximo `concurrency` probes simultâneos. Reconciliar a coleção pública
   `active_attempts` depois de tick, completion e cancelamento. Tentativas
   promovidas internamente têm o mesmo preflight antes de qualquer socket.
   Não criar uma task por câmera candidata nem acessar mapas privados.
   Liberar referências de tasks/results ao encerrar cada tentativa, conforme
   MR-02; concorrência bounded não dispensa limite de retenção no scheduler.
5. Separar descoberta, eligibility persistente e readiness transitória.
   `PRODUCAO + cadastro_completo` do repository é apenas o filtro local inicial.
   Antes do probe exigir configuração ativa, profile SUPPORTED, capability,
   target policy/porta, adapter e referência de credencial quando necessária.
   Revalidar destino e geração após claim e imediatamente antes do I/O.
   Ausência transitória de DB/chave/adapter pausa execução, não retira escopo
   nem fecha intervalo como SAIU_DO_ESCOPO (ADR-021 §4.1.1).
6. Converter apenas D PASS automático em SUCCESS via CAM-INT-05. Preservar
   categorias e confirmação atuais. Erro operacional, DB, decoder ou perda
   de readiness não vira TIMEOUT/CONNECTION_REFUSED de câmera. Timeout/refusal
   só entra como evidência direcional quando o adapter comprova a classificação.
   Teste manual nunca entra neste caminho de completion.
7. Finalizar por `scheduler.complete()` uma vez, mantendo tratamento explícito
   de dispositions. O repository libera lease no store aceito; o scheduler
   libera condicionalmente nos descartes/cancelamentos. Não fazer release
   incondicional adicional. Expiry sozinha não invalida completion; takeover
   com epoch novo invalida. Não introduzir renovação de lease nesta slice.
8. Stop fecha admissão antes do drain; runtime mantém processamento das tasks
   já em voo, heartbeat e ticks de shutdown. No deadline cancela tasks reais,
   coordena cancelamento do scheduler e cleanup do adapter, sem completar
   duas vezes. Callback tardio não inicia nova completion; escrita DB já em
   andamento tem desfecho reconciliado como MR-03, nunca presumido desfeito
   por cancellation. UTC persiste evidência; relógio
   monotônico mede budgets/esperas. Não alegar que o deadline UTC do core
   sozinho garante shutdown diante de salto do relógio civil.
9. Preservar UNKNOWN/ONLINE/OFFLINE, SUSPECT efêmero, stale derivado,
   streak/versão persistidos, histórico e campos legados. O scheduler descarta
   CANCELLED antes do reducer; o reducer puro tem sua barreira de CANCELLED.
   Preservar ambos os comportamentos atuais, sem criar nova semântica de streak.
   Recovery recarrega due/memória do banco; falha/stop não produz OFFLINE em
   massa e não inicia captura. Telemetria usa MON-OBS, sem secrets/payload.

### Cláusulas finais propostas — reconciliação do parecer humano

Registro da revisão anterior. A adjudicação final ao fim deste documento
prevalece sobre status de aprovação e autorização de descarte desta seção.
Em especial, aposentadoria/descarte de registros necessários à deduplicação
não está autorizado pela aprovação de limites de memória.

"Finais propostas" descreve a redação entregue para adjudicação; não afirma
que as decisões materiais já foram aprovadas ou implementadas.

#### MR-01 — configuração e substituição coordenada

1. Ler e validar snapshot tipado/versionado no ciclo existente. Não criar
   watcher, broker, endpoint de hot reload ou infraestrutura externa. Snapshot
   inalterado não recria scheduler; não mutar `_config` nem política privada.
2. Mudança válida fecha admissão e inicia um único drain coordenado. As tasks
   ACTIVE conservam a configuração/policy capturada, `attempt_id`, geração,
   owner e epoch originais. Não transferir tentativa em voo para novo owner,
   não incrementar geração do alvo por reload operacional e não resetar epoch.
   Completion continua sujeita aos gates correntes do repository; alteração
   independente da configuração da câmera pode legitimamente rejeitá-la.
3. Tentativas QUEUED que ainda não executaram não iniciam durante o drain;
   são retiradas da fila local de forma neutra e redescobertas pelo due
   persistido. O prazo global monotônico é `shutdown_timeout_seconds` da
   configuração antiga e não reinicia por novo pedido de reload. Novas versões
   não acumulam fila de reloads: após quiescência, validar o snapshot mais recente.
4. Dentro desse prazo, preservar execução natural das ACTIVE enquanto houver
   readiness. Reservar tempo finito para cancellation/cleanup; timeout de uma
   tarefa não torna a câmera OFFLINE. Solicitar cancelamento, aguardar seu
   término efetivo e liberar lease apenas condicionalmente, conforme MR-03.
5. Criar substituto somente depois de provar ausência de tasks/adapter/ORM
   ainda executando e reconciliar writes de desfecho incerto. O scheduler novo
   recebe snapshot imutável e recarrega due/ConfirmationMemory do repository;
   nenhum estado/intervalo é reconstruído por suposição. Não coexistem dois
   schedulers admitindo trabalho. O owner novo é técnico e distinto; epochs
   continuam exclusivamente sob claim monotônico do banco.
6. Snapshot inválido fecha admissão e sinaliza configuração operacional
   inválida. Tarefas existentes só drenam sob o snapshot antigo enquanto suas
   dependências/destinos permanecerem autorizados e prontos. Sem snapshot
   válido ao final, terminar com diagnóstico fatal/exit não zero; não reabrir
   silenciosamente com configuração antiga. Falha de construção/preflight do
   substituto também não reabre admissão nem reinicia tentativas antigas.
7. Se prazo expirar com operação ainda executando, substituição é FAILED /
   INCOMPLETE: manter admissão fechada, identificar operação pendente com
   campos seguros e aplicar MR-03. Não anunciar reload concluído ou iniciar
   substituto para contornar uma tarefa/ORM que não terminou.

#### MR-02 — descoberta e retenção bounded, sem reciclagem periódica

1. Remover reciclagem obrigatória por contagem; nenhum limiar de 10.000 integra
   a decisão reconciliada. Priorizar extensão pública delimitada do repository
   para descoberta paginada com limite no banco, ordenação due/ID e cursor
   estável, excluindo ACTIVE/QUEUED. Filtrar vencimento no banco; tratar câmera
   sem estado e entrada no escopo sem perder a semântica atual de `enter_scope`.
2. O tamanho da página não excede a capacidade disponível de admissão
   (`queue_bound - queued_count`). Não materializar queryset/parque/histórico
   completo. Cada ciclo tem orçamento finito de páginas e retoma cursor no
   ciclo seguinte quando esse orçamento terminar. Reavaliar eligibility por
   página/alvo; futuros, incompletos ou bloqueados não impedem progresso dos
   demais. Reinício do cursor e revisita de itens mutáveis devem demonstrar
   fairness em validação, sem cache ilimitado de IDs vistos.
3. Limitar tasks de probe vivas a `concurrency`, fila a `queue_bound` e página
   ao limite acima. Tasks, callbacks, resultados, candidates e exceptions são
   liberados assim que processamento/cleanup terminam e todos os consumidores
   conhecidos os entregam. Histórico e ConfirmationMemory persistidos não são
   cache de processo nem alvo desse descarte. Mapas de due/epoch por câmera
   também precisam de limite/eviction seguro usando due persistido; a época
   local de jitter não deve ser confundida com ownership epoch.
4. No scheduler, propor API pública de aposentadoria de tentativa terminal:
   elegível só depois de resultado/cancelamento contabilizado, transação com
   desfecho conhecido, lease tratada e task/adapter/callbacks realmente
   encerrados. Nunca remover ACTIVE/QUEUED ou operação de DB incerta para
   satisfazer o limite. Não editar mapas privados a partir do runtime.
5. A fronteira de dispatch proposta só encaminha completion para tentativa
   ainda rastreada. Duplicadas enquanto rastreadas mantêm as dispositions
   existentes. Após aposentadoria, callback desconhecido/tardio é descartado
   com diagnóstico sanitizado e nenhum store/claim/transição; não reconstruir
   a tentativa e não chamar `complete()` com ID que o scheduler esqueceu.
   O callback carrega a identidade da instância de origem; nunca é roteado ao
   scheduler substituto. Não introduzir nova categoria de ProbeResult.
6. **Decisão material aberta MR-02-A:** aprovar a fronteira acima e o término
   da retenção do resultado/disposition em memória após aposentadoria. Hoje
   `complete()` reconhece DUPLICATE/OLD_ATTEMPT pelos registros retidos e lança
   KeyError para ID desconhecido. Prometer essa resposta para todo UUID passado
   indefinidamente e, ao mesmo tempo, memória finita não está sustentado pelo
   core atual. Preservar idempotência de escrita no banco é obrigatório;
   alterar a duração da resposta de API exige adjudicação explícita. A API
   direta existente não será reinterpretada silenciosamente.
7. **Gate material MR-02-B:** definir capacidades finitas de retenção terminal,
   mapas por câmera e páginas/ciclo a partir do envelope local medido. Sem
   capacity definida e sem consumidor confirmando aposentadoria, parar
   admissão antes de ultrapassar o limite e diagnosticar; não fazer eviction
   insegura. Validar estabilidade de contagens/bytes ao repetir muitos ciclos
   com o mesmo parque e ao substituir câmeras, incluindo callbacks tardios,
   falha DB, cancelamento e reinício, preservando due/streak/owner/epoch/histórico.
8. Reciclagem fica alternativa excepcional: só retornar à discussão mediante
   causa demonstrada por perfis de retenção/contagens ou recurso nativo não
   liberável, limite derivado da medição, comparação com descarte localizado
   e testes dos invariantes de MR-01/RT-04/05/07. Não é workaround presumido
   para ausência de bounded discovery ou de descarte público seguro.

#### MR-03 — recovery, deadlines e shutdown verificável

1. Falha transitória de infraestrutura fecha admissão e marca DEGRADED; não
   muda escopo/estado da câmera. Uma recuperação por vez; delay da tentativa
   `n >= 0` é `min(cycle_interval_seconds, b0 * 2**n)`, com
   `b0 = min(heartbeat_seconds, cycle_interval_seconds)` e cálculo saturado.
   Sem loop imediato, re-probe automático por erro DB ou retry cego de store.
2. Erro fatal de segurança/configuração/schema encerra recovery imediatamente.
   Falhas transitórias repetidas tornam-se persistentes ao consumir um budget
   total monotônico finito de recovery, explicitamente configurado e validado
   antes de operação; ao esgotá-lo, admissão permanece fechada e segue shutdown
   com diagnóstico fatal/exit não zero. Não inventar default desse budget nem
   deduzi-lo do tempo de lease. A escolha operacional do budget permanece gate.
3. Recovery só é bem-sucedido após revalidar DB/configuração/policy/provider/
   adapter, reconciliar operações anteriores e reler due/ConfirmationMemory.
   Então zerar contador/backoff e retornar ao delay inicial no próximo episódio.
   Heartbeat vivo sozinho não é recuperação. Se shutdown já começou, nenhuma
   recuperação reabre admissão. Reexecução após commit incerto exige reconciliação
   do estado persistido; não reapresentar o resultado como nova evidência.
4. Deadline de probe usa `probe_timeout_seconds`, connect usa
   `connect_timeout_seconds`; operação DB exige limite positivo finito de
   connect/lock/statement/transaction aplicável ao backend, mais limite finito
   de espera da ponte sync/async. Cleanup tem orçamento explícito. Limites e
   capacidades do backend devem ser demonstrados no ambiente da operação;
   await timeout/cancelamento de thread não prova término de DB/native adapter.
5. Stop fecha admissão imediatamente e nunca admite a fila durante drain.
   Fixar deadline monotônico único `stop_started + shutdown_timeout_seconds`;
   reservar cleanup dentro dele e limitar cada espera ao restante. Pedido
   repetido não estende prazo. Tarefas já em execução concluem naturalmente
   apenas enquanto houver tempo/readiness; depois recebem cancelamento neutro.
6. Confirmar encerramento real de tasks, sockets/pipelines e operações ORM.
   Só liberar ownership quando o produtor/escritor cessou, comparando owner e
   epoch. Cancelar bookkeeping e liberar lease antes de confirmar parada do
   produtor pode permitir novo probe enquanto o anterior ainda roda; o core
   atual exige coordenação adicional nesse ponto. Não suprimir fencing nem
   redefinir lease expiry como invalidação automática.
7. Operação DB já submetida pode ter commit apesar do timeout do chamador:
   marcar desfecho UNKNOWN, proibir novo store/retry dessa tentativa e bloquear
   substituição/reabertura até reconciliação. Dados já gravados legitimamente
   não são apagados para fingir cancelamento. Falha no release deixa lease
   para takeover futuro; não manter thread/escritor anterior e assumir que a
   expiry o encerrou. Operação não encerrada deve aparecer como pendente.
8. `SHUTDOWN_RESULT = SUCCESS` exige evidência de tasks encerradas, adapters
   fechados, conexões locais encerradas, nenhuma operação ORM em voo e leases
   liberadas ou explicitamente destinadas a expiração sem escritor anterior.
   `SchedulerLifecycle.STOPPED` isolado não basta. Prazo esgotado com operação
   pendente resulta `INCOMPLETE`, diagnóstico seguro e exit não zero quando
   o processo puder terminar. Se operação impede a saída, informar processo
   ainda vivo; não afirmar sucesso/exit ou cancelar à força por suposição.
   Escalonamento para supervisor/terminação de processo pertence a PROD-TOPO
   e requer authority própria; nenhuma ação desse tipo é executada nesta revisão.

Os parâmetros novos de retenção, páginas/ciclo, timeout DB, cleanup e budget
total de recovery não existem hoje em `MonitoringConfig`. Esta redação exige
definição tipada/finita e capacidade validada, mas não introduz valores ou
campos por conta própria. Sem essa definição, a prontidão permanece pendente.

### Conflitos, tensões e pendências perante a authority MON

| Item | Confronto | Adjudicação / destino |
|---|---|---|
| Leitura de config por ciclo versus imutabilidade do scheduler | BC-02 exige leitura; core não tem hot reload | MR-01 propõe drain/substituição simples, preservando a leitura e os tokens; sem conflito com estados MON |
| Memória finita versus resposta de idempotência retida | Core usa histórico local de attempts para DUPLICATE/OLD_ATTEMPT e rejeita ID desconhecido | MR-02-A OPEN; boundary pública de aposentadoria/dispatch proposta precisa aprovação; idempotência persistida MON-REC continua obrigatória |
| Descarte de fila/mapas por câmera versus due/jitter | Remoção privada pode perder due, deixar heap/referências retidos ou mudar sequência de jitter | MR-02-B e RT-03: API pública e medição; due persistido prevalece, não alterar ownership epoch; não comprovado no HEAD |
| Cancelamento/release do core versus operação real em voo | `cancel()` libera lease e STOPPED não supervisiona tasks/ORM; UTC do core não prova budget monotônico | MR-03 exige término antes do release e diagnóstico INCOMPLETE; ajuste futuro coordenado no core se necessário, não mudança silenciosa de MON-OWN |
| Timeouts de DB/recovery/cleanup versus schema atual | MON-OBS/MonitoringConfig só oferecem budgets parciais | Gate de configuração operacional aberto; valores/backend não homologados, sem promessa de shutdown bem-sucedido |
| Readiness/health versus domínio de câmera | MON-REC/AV e ADR-021 preservam estado/freshness em falha do subsistema | Sem conflito: pausa/timeout operacional não cria OFFLINE, SAIU_DO_ESCOPO, nova captura ou transição falsa |

Nenhuma cláusula autoriza mudança de estado estável, ProbeResult, schema,
renovação de lease ou topologia produtiva. MR-02-A, os limites operacionais
e a aprovação final MR-01..03 mantêm `CONTRACT_STATUS = OPEN`.

### Aceite da implementação futura e stop conditions

| Gate | Evidência exigida em fakes/banco isolado |
|---|---|
| RT-01 — composição | Command separado, preflight fail-closed, repository único e nenhuma rede antes de autorização do target; `--once` conclui um lote finito admitido, não faz varredura do parque |
| RT-02 — tasks | Completion/cancelamento que promove fila inicia exatamente uma task; nenhum probe novo enquanto DEGRADED/DRAINING; queue/concurrency permanecem bounded |
| RT-03 — recursos | Descoberta limitada no banco/cursor/páginas e fairness com futuros/ocupados/bloqueados; tasks/fila/retidos/mapas dentro de caps definidos; contagens/bytes sem crescimento por total histórico de probes; retirement pública e callback tardio sem write; sem reciclagem obrigatória ou perda de due/streak/histórico |
| RT-04 — fencing | Geração/owner/epoch antigos não gravam estado nem snapshot; release antigo não libera owner novo; expiry sem takeover não rejeita por si só; completion aceita libera lease atomicamente |
| RT-05 — confirmação | Restart preserva streak/policy/due; duplicado/atrasado não duplica transição/intervalo; manual A-D e capture não promovem disponibilidade; CANCELLED mantém caminho existente |
| RT-06 — recovery | Falhas transitórias usam backoff capped/serial e reset após recuperação completa; persistentes esgotam budget e falham; commit incerto não provoca retry de completion; readiness transitória não chama leave_scope |
| RT-07 — shutdown | Sem admissão nova; drain/cleanup no budget monotônico, inclusive salto UTC; tasks/adapter/ORM realmente encerrados antes de release; operação presa/commit incerto produz INCOMPLETE, nunca SUCCESS presumido |
| RT-08 — configuração/telemetria | Reload sem infraestrutura extra preserva tokens/snapshot das ACTIVE, sem sobreposição de schedulers; config inválida/drain timeout/construção falha não reabre admissão; heartbeat e logs seguros |

RT-04 para health exige que CAM-INT-05 ofereça boundary de escrita consistente
entre `CameraHealthSnapshot` e completion de disponibilidade. O runtime não
deve criar segundo store desprotegido. Atomicidade/fencing entre esses writes
é gate de integração a comprovar na slice predecessora, não fato deste HEAD.

Parar antes de implementar se MR-01..03 não estiverem aprovadas; se MON-OBS,
CAM-INT-05 ou CAM-HEALTH não estiverem integradas; se classificação de resultado
exigir nova categoria/estado; se timeouts reais invalidarem shutdown bounded;
ou se houver necessidade de schema, renovação, multi-worker/topologia produtiva.
PostgreSQL, egress/conta/supervisor, thresholds reais, capacidade, retenção e
LIVE continuam nos gates próprios de PROD-PERSIST/TOPO/CAP.

```text
DOCUMENTARY_REVIEW = PREPARED / SOURCE_GROUNDED
RECONCILIATION_REVIEW = PREPARED / HUMAN_CRITERIA_INCORPORATED
CONTRACT_STATUS = OPEN / NOT_CLOSED
ARCHITECTURAL_AND_OPERATIONAL_DECISION_CLOSURE = PENDING / MR-02-A; operational caps/deadlines; final approval MR-01..03
WORKER_IMPLEMENTED = NO
TESTS_RUN = NO / DOCUMENTATION_ONLY
NEXT_ACTIVITY = USER_ADJUDICATION_OF_MR-01..03
NEXT_IMPLEMENTATION = NOT_AUTHORIZED / WAITING_DEPENDENCIES_AND_GATES
```

## MON-RUNTIME-CONTRACT-FINAL-ADJUDICATION — 2026-10-09

Snapshot histórico supersedido pela decisão de consolidação ao fim do arquivo.
Sua prova descreve o core existente, não a janela local autorizada posteriormente.

```text
MODEL_REQUESTED = SOL / HIGH
MODE = CONTRACT_ONLY
EXECUTION_MODE = DIRECT
IMPLEMENTATION = FORBIDDEN
CODE_CHANGE = FORBIDDEN
TEST_CHANGE = FORBIDDEN
GIT_OPERATIONS_THIS_REVIEW = NOT_EXECUTED / forbidden
SOURCE_HEAD = 5bd22b0 / previously verified, not revalidated in this review
MR_01 = APPROVED
MR_02_MEMORY_BOUNDING = APPROVED
MR_02_PERSISTENT_RETIREMENT = DEFERRED
MR_02_DEDUPLICATION_PROOF = INSUFFICIENT / after retirement; scoped fencing proof below
MR_03_RECOVERY_MODEL = APPROVED
MR_03_OPERATIONAL_BUDGETS = PENDING
OWNERSHIP_RELEASE_SAFETY = UNRESOLVED / temporal producer termination not proven by core
MONITORING_CONFIG_CONTRACT = PENDING
CONTRACT_STATUS = PROPOSED_PENDING_APPROVAL
```

### MR-01 aprovado — invariantes e limite da prova

Preservar tasks ACTIVE e seus snapshot/attempt_id/generation/owner/epoch,
sem transferir trabalho antigo ao novo scheduler. Fechar admissão, drain
coordenado bounded e substitution somente após operações efetivamente
encerradas; pedir cancellation não comprova encerramento. Nenhum release
explícito enquanto o produtor/escritor ainda puder produzir efeitos. Falha,
timeout ou write de desfecho incerto mantém admissão fechada e impede
substitution. Não acrescentar watcher/broker/infraestrutura de hot reload.

Prova estática: `DueScheduler.complete()` compara geração corrente e
eligibility; `DjangoMonitoringRepository.store()` com ownership exige owner,
epoch e geração exatamente iguais no update transacional. Sucesso grava
memória/estado/transição/intervalo e limpa owner/expiry atomicamente. Claim
usa expiry no relógio DB e incrementa epoch; release só compara owner/epoch,
sem reduzir epoch. Isso cerca writes obsoletos. Não cancela I/O nem impede
que dois produtores façam rede após expiry/takeover. A liberação transacional
pressupõe que o adapter já encerrou; essa ligação ainda não existe no runtime.

`cancel()` e `_discard()` do scheduler chamam release sem supervisionar task
ou ORM; `_finish_shutdown_if_due()` pode fazê-lo ao vencer seu deadline UTC.
O futuro runtime precisa impedir esse caminho prematuro ou ajustar a
coordenação pública do core, sem alterar fencing. Até demonstrar término
antes desse release, `OWNERSHIP_RELEASE_SAFETY = UNRESOLVED`.

### MR-02 — quatro responsabilidades distintas

| Responsabilidade | Autoridade atual / destino |
|---|---|
| IN_MEMORY_OBJECT_RELEASE | Liberar resultados, exceptions, tasks e referências externas após todos os consumidores/cleanup e DB terem terminado é aprovado. Registro `_attempts` usado para dedup não é referência temporária dispensável por suposição |
| PERSISTENT_ATTEMPT_RETIREMENT | Não há ledger/modelo persistido por attempt UUID no core inspecionado. Estado, owner/epoch, geração, streak e última observação pertencem à câmera. Nenhuma exclusão autorizada; retirement persistente DEFERRED, sem criar ledger novo |
| DUPLICATE_REJECTION_AUTHORITY | `_attempts`/estado terminal/current ID no scheduler para dispositions; owner/epoch/generation no repository para escrita; timestamps/memória no reducer para ordem. Não confundir as três fronteiras |
| AUDIT_RETENTION | Estado técnico, transições/indisponibilidades e eventos de auditoria têm autoridade própria. Não recebem TTL ou expurgo por liberação de memória; MON-HIST mantém retenção não adjudicada e probes normais não criam auditoria de usuário |

### Prova de deduplicação por cenário — leitura estática, sem executar testes

| Cenário | Garantia no código existente | Limite da conclusão |
|---|---|---|
| Mesmo UUID enquanto registro terminal existe | `complete()` retorna DUPLICATE ou OLD_ATTEMPT antes de store | PASS nesse escopo; remover o registro muda lookup para KeyError, não preserva a resposta da API |
| Reapresentar store com lease já consumida por commit | O primeiro commit limpa owner; update posterior com owner/epoch antigo não encontra writer válido | Rejeição persistente do token antigo; não prova aposentadoria arbitrária de dados usados pelo scheduler |
| Resultado tardio após takeover/restart | Claim novo incrementa epoch, scheduler novo ganha owner distinto; store/release com token antigo não afetam owner novo | Fencing protege domínio; não recriar tentativa antiga nem reassociar resultado a novo claim/token |
| Lease expirou sem takeover | store não filtra expiry; mesmo owner/epoch/generation pode concluir | Expiry sozinha não rejeita duplicata nem cancela produtor; não usá-la como prazo de retirement |
| Geração da câmera mudou | Scheduler revalida; store leased exige igualdade exata | CONFIG_CHANGED sem transição/intervalo; geração não substitui attempt ID ou ownership epoch |
| Timestamp atrasado/igual, memória recarregada | reducer retorna OUT_OF_ORDER/AMBIGUOUS_ORDER e preserva memória estável | Não é exatamente-once por UUID; store ainda pode atualizar due/campos operacionais e consumir lease |
| Retry após commit de desfecho incerto | Commit confirmado consumiria lease; rollback poderia manter token/memória | Não repetir cegamente; terminar operação anterior e reconciliar DB. O código não oferece receipt persistente por UUID para comprovar qualquer outcome |
| Apagar `_attempts` e receber callback antigo | Scheduler lança KeyError para ID ausente | Não há retirement API/dispatch comprovado. Sem proof, não autorizar essa exclusão nem declarar dedup pós-retirement PASS |

`cameras/test_monitoramento_mon09c.py` contém cenários de expiry sem takeover,
takeover/epoch, stale generation, release de owner antigo e rollback; foram
somente lidos, não executados. Não estender sua cobertura a retirement não
implementado ou a PostgreSQL/multiprocessos. Caminho sem ownership de store
faz CAS de geração, sem receipt por UUID: não habilitá-lo no worker com lease.

### Limites concretos propostos de memória — derivados, sem TTL arbitrário

Usar C/Q do MonitoringConfig existente (default C=20, Q=40; máximos C=50,
Q=10*C=500). Esses valores limitam cardinalidade, não bytes/RSS de objetos.

| Recurso | Limite proposto | Justificativa / saturação |
|---|---|---|
| Tasks de probe vivas | C = 20 default, até 50 | Uma task por ACTIVE; sem task por candidato |
| Candidates queued | Q = 40 default, até 500 | Reusar fila limitada; overflow deferred |
| Página de descoberta resident | min(Q, slots livres) = até 40 default | Uma página por vez e limite aplicado no banco; sem guardar páginas anteriores |
| Páginas por ciclo | 1, cursor retomado no próximo ciclo | Menor lote que usa a fila atual; fairness da revisita ainda precisa validação, sem novo campo |
| Resultados/referências externas terminais | 0 após consumo/cleanup comprovados; antes disso até C | Não manter resultados por histórico de probes; operação pendente ocupa slot |
| Registros locais de tentativa e mapas por câmera | Teto protetivo proposto C+Q = 60 default, até 550; não é autorização de eviction | Derivado do envelope ACTIVE+QUEUED existente; ao atingir, fechar admissão e diagnosticar retenção pendente. Não esquecer terminal, baixar contagem ficticiamente ou reciclar automaticamente |
| Estado/dados persistidos necessários à idempotência | Nenhuma exclusão/TTL autorizado | Retention não se deduz de P, expiry ou shutdown; autoridade persistida preservada |

O teto protetivo explicita uma parada segura, não resolve a retenção contínua
do core. MR-02 memory bounding é aprovado como requisito; descarte dos
registros de dedup e mecanismo público correspondente continuam pendentes.
Não inventar retirement persistente para corrigir memória local. Sem prova
da necessidade e das garantias de descarte, deferir retirement; sem solução
segura de retention contínua, não declarar o worker pronto. Bytes/RSS e
fairness precisam de medição futura autorizada, sem reciclagem por contagem.

### MR-03 — modelo aprovado e configuração mínima proposta

Recovery serial usa DEGRADED, capped exponential backoff, dois limites finitos
(tentativas e elapsed) e reset só após recuperação completa. Stop fecha
admissão, DRAINING e drain/cleanup sob deadline único. Não introduzir RECOVERING.
Falha fatal encerra recovery; transitório esgotado vira diagnóstico persistente.
Operação sem término comprovado é INCOMPLETE, nunca shutdown SUCCESS.

A matriz dos oito parâmetros e seus ranges, fonte, relações, failure behavior
e testes futuros está somente em
`MONITORING_OBSERVABILITY_CONFIG_CONTRACT.md`, seção
MON-RUNTIME-CONTRACT-FINAL-ADJUDICATION. Proposta mínima: três novos campos
DB deadline/recovery attempts/recovery elapsed; demais budgets derivados
ou existentes. Não implementar extensão ou alegar que já integra MonitoringConfig.

### Pendências indispensáveis e resultado da adjudicação

1. Provar descarte local seguro sem perder dedup/callback fencing e fechar
   retention contínua do scheduler; retirement persistente fica DEFERRED.
2. Aprovar valores/relações da matriz e extensão mínima de MonitoringConfig.
3. Definir coordenação de shutdown que impeça release prematuro, inclusive
   cancel/_discard/deadline automático do core, e confirmar capacidade de
   DB/adapter de encerrar operações; não contornar operação presa com novo owner.

Predecessores MON-OBS/CAM-INT-05/CAM-HEALTH continuam gates de integração,
sem alteração de HTTP Snapshot/RTSP/IMG-CAP. DueScheduler, ConfirmationMemory,
DjangoMonitoringRepository e UNKNOWN/ONLINE/OFFLINE são preservados.

```text
MR_01 = APPROVED
MR_02_MEMORY_BOUNDING = APPROVED
MR_02_PERSISTENT_RETIREMENT = DEFERRED
MR_02_DEDUPLICATION_PROOF = INSUFFICIENT
MR_03_RECOVERY_MODEL = APPROVED
MR_03_OPERATIONAL_BUDGETS = PENDING
OWNERSHIP_RELEASE_SAFETY = UNRESOLVED
MONITORING_CONFIG_CONTRACT = PENDING
MATERIAL_DECISIONS_PENDING = safe local retention/dedup; matrix values/config extension; termination-before-release coordination
CONTRACT_STATUS = PROPOSED_PENDING_APPROVAL
NEXT_ACTIVITY = adjudicate minimal budgets and safe retention/release boundaries / contract only
IMPLEMENTATION = FORBIDDEN
CODE_AND_TEST_EXECUTION = NOT_PERFORMED
GIT_OPERATIONS = NOT_PERFORMED
```

## MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION — V1 (2026-10-09)

Esta seção incorpora a instrução humana vigente e prevalece sobre propostas
e status anteriores neste arquivo. Fecha o contrato local, sem declarar
implementação, prova dinâmica ou autorização de executar o worker. A decisão
humana autoriza janela local finita, dispensando classificação histórica exata
fora dela. Não autoriza exclusão persistente, ledger ou novo estado RECOVERING.

### MR-01 — término comprovado antes de release

Fechar admissão uma única vez; preservar snapshot, attempt_id, generation,
owner e epoch de cada ACTIVE. Drain coordenado até o deadline definido em
MON-OBS; depois solicitar cancellation e cleanup no restante do budget global.
Substituir scheduler somente após tasks, adapter e chamadas ORM anteriores
terem efetivamente terminado e writes incertos terem desfecho reconciliado.
Não acumular pedidos de reload nem acrescentar watcher/broker.

Nenhum release explícito antes de comprovar que o produtor não pode mais
produzir efeitos. Deadline vencido não é comprovação. Timeout de drain ou
shutdown é INCOMPLETE, mesmo se cleanup terminar depois; registrar o término
posterior separadamente. Nunca reabrir admissão ou reportar SUCCESS enquanto
operação anterior estiver em voo. Cancellation não gera OFFLINE ou transição.

Crash não executa release presumido: lease permite takeover, claim aumenta
epoch e completion/release preservam seus gates existentes. Expiry sem
takeover não invalida token por si só; fencing protege escrita e não promete
exclusão de I/O físico concorrente. Completion aceita continua consumindo a
lease no mesmo commit do domínio, após término do adapter e sem writer paralelo.

### MR-02 — janela local finita e descarte fail-closed

A janela é por **quantidade de tentativas terminais**, não tempo civil:
`W = concurrency + queue_bound`. Default W=60; máximo W=550 pelos ranges
existentes. Ordenar por sequência local de finalização, mantendo as últimas
W tentativas COMPLETED/CANCELLED. Essa definição usa o envelope corrente de
trabalho e não adiciona configuração ou limiar de reciclagem.

Dentro da janela, conservar o Attempt terminal mínimo e aplicar exatamente
as regras atuais de DUPLICATE/OLD_ATTEMPT em `complete()`. Fora dela, ID
desconhecido mantém a rejeição KeyError antes de load/reducer/store; o runtime
a trata como diagnóstico sanitizado de callback rejeitado. Não criar Attempt,
não reclamar nova lease e não reapresentar resultado com token novo. Callback
de instância anterior nunca é encaminhado à instância substituta. Não criar
nova categoria de ProbeResult ou exigir disposition histórica após eviction.

Somente tentativa verdadeiramente finalizada é elegível à janela: adapter,
task, consumidores conhecidos e ORM terminados; persistência reconciliada;
lease consumida/liberada condicionalmente ou destinada a expiry sem produtor
anterior. Operação pendente permanece pinned e ocupa seu slot de concorrência;
não é aposentada para satisfazer limite. Finalização e housekeeping são
serializados com as mutações do scheduler, evitando race entre eviction e callback.

| Estrutura local | Bound V1 e regra |
|---|---|
| Produtores/tasks reais, inclusive cancelamento/ORM pendente | C = concurrency; manter slot até término real, não somente até fim do bookkeeping |
| Fila lógica e heap físico | Q = queue_bound; discard precisa remover/compactar entradas mortas, sem heap crescente oculto |
| Tentativas ACTIVE+QUEUED e candidatos vivos | <= C+Q; terminal não conserva candidato, resultado bruto, exception ou traceback |
| Janela terminal e índice de ordem | W = C+Q; eviction mais antiga ao inserir W+1, apenas entre terminais elegíveis |
| `_attempts` total | <= C+Q+W = 2*(C+Q); default 120, máximo 1100 |
| `_candidate_by_attempt`, ACTIVE/current indices | <= C+Q; remover candidate na finalização comprovada; registros de índices ativos nunca são evicted |
| Cache por câmera `_next_due`/`_schedule_epoch` | <= C+Q; manter câmeras ACTIVE/QUEUED pinned e evict somente inativas; próximo candidato vem do due persistido, sem reuso de snapshot antigo |
| Página de descoberta | <= min(Q, slots de fila livres); uma página residente, uma página por ciclo e cursor retomado; sem conjunto ilimitado de IDs visitados |
| Referências runtime de tasks/results/callbacks concluídos | 0 após consumo/cleanup; até C enquanto pendentes; nenhuma task por candidato ou fila de resultados ilimitada |

Cada cache por câmera tem o mesmo conjunto limitado de chaves; eviction
remove os dois valores coordenadamente. `_schedule_epoch` é época local de
jitter, não ownership epoch: reset em cache miss já tem precedente em
`restart()`. Preservar algoritmo/range de jitter; nunca retroceder due
persistido nem alterar fencing por eviction. Se slots estiverem pinned,
adiar novas admissões, sem sobrepor produtores.

IN_MEMORY_OBJECT_RELEASE é autorizado nesses bounds. PERSISTENT_ATTEMPT_RETIREMENT
permanece DEFERRED; não existe ledger por UUID a excluir no core atual.
DUPLICATE_REJECTION_AUTHORITY é scheduler dentro da janela e rejeição fechada
fora dela; domínio continua cercado por repository/ConfirmationMemory.
AUDIT_RETENTION e histórico MON-HIST não mudam. Não apagar estado, streak,
epoch, generation, transição, intervalo ou auditoria; não criar ledger adicional.
Bounds são de cardinalidade. Não alegar RSS produtivo aprovado; não reter
payloads/media em terminal, e validar bytes/contagens em execução longa futura.

### MR-03 — defaults V1 e relações

Defaults aprovados: probe 5 s; DB 5 s; shutdown 30 s; drain S/2;
recovery 5 tentativas/900 s; backoff inicial min(heartbeat,cycle_interval),
máximo cycle_interval. Recovery é serial, usa DEGRADED e reseta contador/delay
somente após recuperação completa; falha fatal termina imediatamente e
transitório esgotado segue desligamento observável. Não criar RECOVERING.

Matriz, fontes/ranges e validação cruzada permanecem na seção de consolidação
de `MONITORING_OBSERVABILITY_CONFIG_CONTRACT.md`. Deadline de espera síncrona
não comprova cancellation/rollback. Operação incerta bloqueia nova admissão
e retry; encerramento real e reconciliação são requisitos, não suposições.

### Menor extensão necessária do core — especificação, não implementação

1. `MonitoringConfig`: três campos DB/recovery descritos em MON-OBS e validação
   cruzada. Janela/cache/paginação derivam de C/Q; não precisam de campo novo.
2. `DueScheduler`: adicionar confirmação explícita de término do produtor à
   fronteira pública de finalização/cancelamento; para tentativa com ownership,
   omissão não comprova término. Sem confirmação, manter pinned, sem release,
   sem promoção que ultrapasse C e sem STOPPED por bookkeeping. `complete()`
   só persiste após término do adapter; calls ORM são serializadas até seu
   retorno efetivo. Falha DB de desfecho incerto não deve passar pelo release
   automático de `_discard()` antes da reconciliação. Queued sem produtor e
   claim negado não exigem cancelamento de adapter inexistente.
3. `request_shutdown()` fixa início uma única vez; deadline e `_finish_shutdown_if_due()`
   não cancelam/liberam ACTIVE não confirmada. Deadline expirado deixa resultado
   INCOMPLETE e admissão fechada; STOPPED só após quiescência comprovada.
   Não acrescentar enum de estado técnico; usar sinais operacionais seguros.
4. Housekeeping público e serializado mantém janela W, descarta candidatos
   terminais e aplica eviction segura aos caches/heap. Preservar a rejeição
   atual de UUID desconhecido; não mudar `DjangoMonitoringRepository.store/release`
   ou o reducer para implementar dedup histórica ilimitada. Runtime não toca
   mapas privados. Chamadores laboratoriais futuros precisarão declarar que
   seus fakes já terminaram; o booleano/ack não substitui prova real no runtime.
5. `DjangoMonitoringRepository.list_due`: descoberta paginada com limite no DB,
   due/cursor/ID e exclusão de queued/active bounded; tratar entrada de escopo
   conforme comportamento existente. Sem ledger, migration ou writer novo.

### Critérios verificáveis para implementação futura autorizada

| Gate | Cenário e asserções obrigatórias |
|---|---|
| DC-01 — janela | Finalizar W, W+1 e muitos múltiplos de W; últimas W mantidas na ordem de finalização; total attempts <= 2*(C+Q), sem retenção de candidates/results/tracebacks terminais |
| DC-02 — callbacks | Dentro da janela repetir UUID: disposition atual e nenhum segundo store. Evict UUID antigo e enviar callback: rejeição antes de load/claim/store, estado/streak/due/histórico inalterados; callback de scheduler antigo não alcança o novo |
| DC-03 — recursos | Repetir ciclos, churn de câmeras e queued cancellations; todos os mapas, heap físico, tasks e páginas nos bounds. Due persistido preservado após cache eviction; jitter dentro do range, sem starvation pelos mesmos itens |
| DC-04 — fencing | Token/generation antigos, takeover após expiry e release antigo não afetam novo owner; expiry sem takeover conserva semântica atual; restart recarrega memória sem transição/intervalo duplicado; não retry cego após commit incerto |
| DC-05 — shutdown | Adapter/ORM continuam produzindo efeitos após cancellation solicitada: nenhuma release/substitution, slot pinned, admissão fechada, resultado INCOMPLETE. Após término confirmado, release condicional; salto UTC não estende budget monotônico |
| DC-06 — recovery/config | Defaults válidos; bool/NaN/inf/range/relações inválidos rejeitados antes de I/O; recovery serial/capped, dois limites finitos e reset após recuperação completa; nenhum retry além do budget |
| DC-07 — falhas | Claim negado, config/eligibility perdida, DB incerto e timeout automático não disparam release prematuro por `_discard/cancel`; nenhuma falha do subsistema vira OFFLINE ou expurgo persistente |

Compatibilidade: core atual tem retenção ilimitada e release sem confirmação;
são lacunas de implementação explicitamente endereçadas pela extensão acima,
não fatos já corrigidos. A nova duração de classificação local é decisão
humana explícita; owner/epoch/generation, memory/reducer, UNKNOWN/ONLINE/OFFLINE,
freshness, history e separação de captura permanecem. Não há contradição material
não adjudicada com a authority MON. PostgreSQL/multi-worker/real deadlines e
capacidade continuam gates futuros; ausência de prova dinâmica não concede operação.

```text
CONTRACT_STATUS = CLOSED / LOCAL V1 DECISIONS ONLY
MATERIAL_DECISIONS_PENDING = NONE_FOR_THIS_LOCAL_CONTRACT
CORE_EXTENSION = SPECIFIED / NOT_IMPLEMENTED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
WORKER_IMPLEMENTED = NO
TESTS_WRITTEN_OR_EXECUTED = NO
PERSISTENT_RETIREMENT = DEFERRED / NOT_REQUIRED_FOR_LOCAL_WINDOW
HTTP_SNAPSHOT_RTSP_IMG_CAP_CHANGED = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
NEXT_ACTIVITY = explicit authorization of core/runtime implementation after predecessor integration and validation plan
```

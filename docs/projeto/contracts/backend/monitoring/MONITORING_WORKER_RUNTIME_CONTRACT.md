# Monitoramento — runtime do worker

```text
ID = MON-WORKER
STATUS = ARCHITECTURAL CONTRACT
PRODUCTION_WORKER = NOT_IMPLEMENTED / NOT_DEPLOYED
BC02_STATUS_AS_PUBLISHED = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING / HISTORICAL CLASSIFICATION
BC02_IMPLEMENTATION_READINESS_AS_PUBLISHED = YES / LOCAL CONTRACT BASELINE
CURRENT_CONTRACT_STATUS = CLOSED / LOCAL V1
MON_WORKER_IMPLEMENTATION = COMPLETE / LOCAL
MON_WORKER_LOCAL_VALIDATION = PASS / FULL_REGRESSION 921 PASS
MON_WORKER_BRANCH_PUBLICATION = PENDING_UNTIL_REMOTE_CONFIRMATION
MON_WORKER_MASTER_INTEGRATION = PENDING
IMPLEMENTATION_READINESS = PASS / contract baseline reconciled
OPERATIONAL_READINESS = NOT_ESTABLISHED
POSTGRESQL_HOMOLOGATION = PENDING
MULTI_WORKER_HOMOLOGATION = PENDING
REAL_CAMERA_HOMOLOGATION = PENDING
IMPLEMENTER_TARGET = LUNA
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

### Interfaces e heartbeat independente

A execução V1 reusa `DueScheduler`, `active_attempts`, `tick`, `complete`, `request_shutdown`; `DjangoMonitoringRepository.list_due/claim/release/load/store/current_generation/is_eligible`; `MonitoringConfig`, `ConfirmationPolicy/Memory`; `MonitoringTelemetry`, `LoggingTelemetry`, `record_heartbeat`; `run_automatic_camera_diagnostic` com `ConnectionTestResult`; e `CameraHealthSnapshot`/projeção CAM-HEALTH. Não criar writer/reducer paralelo; completion atômica continua no mesmo repository.

`HEARTBEAT_OWNER = WORKER_RUNTIME`. O worker emite heartbeat em `heartbeat_seconds`, independente dos ciclos do scheduler, inclusive enquanto vivo em drain/recovery. Esse sinal é telemetria operacional; não renova ownership. Cancelamento continua neutro. O worker ainda não foi implementado.

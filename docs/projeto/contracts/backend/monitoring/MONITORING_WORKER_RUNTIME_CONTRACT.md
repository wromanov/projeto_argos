# Monitoramento — runtime do worker

```text
ID = MON-WORKER
STATUS = ARCHITECTURAL CONTRACT
PRODUCTION_WORKER = NOT_IMPLEMENTED / NOT_DEPLOYED
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL PROCESS
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

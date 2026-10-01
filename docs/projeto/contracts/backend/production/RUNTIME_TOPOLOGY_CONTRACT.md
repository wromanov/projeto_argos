# Topologia de runtime

```text
ID = PROD-TOPO
STATUS = ACTIVE / ARCHITECTURAL BOUNDARY
TOPOLOGY = NOT SELECTED / NOT DEPLOYED
BC02_STATUS = PRODUCTION_ONLY
CONTRACT_READY = NO / replica, supervisor, network and service-account decisions
IMPLEMENTATION_NOW = NO
VALIDATION_ENVIRONMENT = homologation / production
```

## Componentes e fronteiras necessárias

Web Django atende interação e leituras/mutações autorizadas. Worker dedicado executa monitoramento contínuo, isolado de HTTP, com identidade, banco e egress de rede de menor privilégio. Serviço de captura sob demanda deve ser fronteira separada (pode compartilhar runtime do worker somente mediante decisão e isolamento adequados) e nunca é implicitamente acionado por probe. Banco e storage privado são dependências explícitas e observáveis. Browser não se conecta à câmera.

## Requisitos de deployment

Definir processos/replicas, scheduler, distribuição de trabalho, limites de concorrência, startup/readiness/liveness, heartbeat, rolling update, shutdown/drain/cancel, restart/backoff, clock, secrets, egress, firewall e deploy/migration ordering. Um worker parado não produz OFFLINE em massa; freshness torna evidência stale. Duplicação de worker exige ownership/lease/fencing no banco alvo. Contas de serviço não são contas humanas e não executam como root.

## Não decisões

ADR-019 explicitamente não escolhe Celery, Redis, RQ, asyncio, threads, cron, filas, SSE/WebSocket ou outros mecanismos. O código atual contém núcleo de scheduler assíncrono testável e WSGI/ASGI Django, mas nenhum processo/service/deployment dedicado confirmado. Não deduzir topologia da presença do código. Seleção exige capacity, operação, segurança e banco acordados; não habilita LIVE ou homologação por si só.

Referências: ADR-019; ADR-021 §§5–6, 9; `cameras/monitoramento/scheduler.py`; `config/wsgi.py`, `config/asgi.py`.

## BC-02 — topologia lógica fechada, operação futura

Topologia lógica: processo Django web para interações; management command
`run_monitoring_worker` em processo separado para probes; command
`run_capture_worker` em processo separado para captura; PostgreSQL e storage
privado como dependências externas. Compartilhar host é possível em ambiente
local, mas fila, orçamento e identidade de captura não são os do monitoramento.
Web não faz probe/captura bloqueante nem recebe egress de CFTV por default.
Worker de monitoramento e worker de captura usam identidades de serviço,
credenciais DB, chaves e egress próprios conforme necessidade. Quantidade de
réplicas, supervisor, deploy/migration ordering, firewall/VLAN e budgets
dependem da operação e não são escolhidos aqui. Se houver mais de um worker
de monitoramento, validar fencing/lease em PostgreSQL sob contenção real.

```text
MODEL_CHANGE = NONE
MIGRATION_REQUIRED = NO
EXPECTED_MODELS = NONE NEW
RELATIONSHIPS = processes use database and storage ports
CONSTRAINTS = runtime isolation and egress policy
INDEXES = NONE
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = stop workers with drain; retain persisted state
EXPECTED_PRIMARY_FILES = deployment/service configuration (future)
EXPECTED_NEW_FILES = supervisor/runbook (future)
EXPECTED_TEST_FILES = process lifecycle, restart, multi-worker and egress tests
SHARED_FILES = production config, one operational owner
STOP_AND_ESCALATE_TO_SOL_IF = deployment requires merging web/probe/capture
                              or changes lease/secret trust boundary
```

Gate futuro: processo web não conecta a câmera, workers têm readiness/
heartbeat/shutdown observáveis, egress restrito e restart sem OFFLINE em
massa ou duplicação de histórico. Nenhum gate LIVE é liberado pelo BC-02.

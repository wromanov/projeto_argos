# Monitoramento — configuração e observabilidade

```text
ID = MON-OBS
STATUS = ACTIVE / LOCAL CONFIG SCHEMA
OPERATIONAL VALUES = NOT_HOMOLOGATED
BC02_STATUS = IMPLEMENTATION_READY
IMPLEMENTATION_READY = YES / LOCAL OBSERVABILITY PORT
IMPLEMENTER_TARGET = LUNA
MON_RUNTIME_DECISION_CONSOLIDATION = 2026-10-09 / V1 section below
MONITORING_CONFIG_CONTRACT = CLOSED / specification only, extension not implemented
```

## Configuração

`MonitoringConfig` valida valores tipados e bounded para concorrência, intervalo de ciclo, timeout de probe/connect, fila, jitter (máximo 20%), freshness, shutdown, heartbeat e lease. Defaults e ranges no código são proteções reversíveis do core, não SLOs aprovados. Deploy futuro deve carregar valores por ambiente a partir de configuração confiável e versionar política de confirmação; nenhum segredo deve entrar nesse objeto/log.

Rejeitar booleano no lugar de número, NaN/inf, valores fora do range ou timeout de conexão superior ao timeout total. Fila limitada; overflow é deferred/diagnóstico, nunca crescimento ilimitado de memória. Jitter determinístico deve espalhar cadência sem mudar o intervalo contratual de domínio.

## Sinais mínimos

Estado de lifecycle, heartbeat, início/fim do último ciclo, duração, elegíveis/due/admitidos/deferred/queued/active, counts de tentativas iniciadas/concluídas/canceladas, falhas operacionais, ownership acquired/denied/lost e stale completion rejected. Percentis de latência/idade de evidência, backlog, freshness stale, DB error e distribuição de categorias podem ser agregados. Definir retenção/cardinalidade e limiares somente com SLO/observação do ambiente.

## Sigilo

Logs/traces não contêm segredo, username, URL/RTSP path, conteúdo, headers auth ou configuração sensível. Códigos de erro são allowlisted/sanitizados; não guardar stack trace com material do request secreto. Telemetria de serviço não é `EventoAuditoria` por probe normal.

Fonte: `cameras/monitoramento/schemas.py`, `scheduler.py`; ADR-021 §8. Métricas, backend e alarmes operacionais ainda não estão implantados.

## BC-02 — interface local e sinais objetivos

`MonitoringTelemetry` é port injetável com `emit_event(name, fields)`,
`increment(name, labels)`, `gauge(name, value, labels)` e
`observe_seconds(name, value, labels)`. Implementações locais: `NoopTelemetry`
para testes e `LoggingTelemetry` com JSON estruturado usando `logging` do
Python; nenhuma dependência de collector externo. Eventos/nomes/labels são
allowlisted, tipos JSON escalares finitos, cardinalidade limitada a estágio
A/B/C/D, resultado fechado e adapter/profile version. Não incluir camera_id
como label de métrica; correlação por ID opaco só em log restrito. Não incluir
IP, URI, path, username, segredo, SDP, frame, ciphertext nem traceback cru.

Sinais mínimos: cycle duration, eligible/due/admitted/deferred, queue/backlog/
active, outcomes e cancelamentos, stage A/B/C/D failures, heartbeat e idade,
DB failure, ownership acquired/denied/lost, stale completion rejection,
readiness e shutdown. `MonitoringConfig` existente é a fonte tipada de
intervalos/limits; snapshot sanitizado registra apenas nomes e valores
operacionais não secretos, hash/version da policy e status, nunca chave,
CIDR/credencial ou target. Falha da telemetria não muda resultado de probe,
estado de câmera ou transação de domínio; registra erro operacional seguro.
Retenção, alertas, SLO e backend final são PROD-CAP/TOPO posteriores.

```text
MODEL_CHANGE = NONE
MIGRATION_REQUIRED = NO
EXPECTED_MODELS = NONE NEW
RELATIONSHIPS = NONE
CONSTRAINTS = allowlist in port/provider
INDEXES = NONE
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = switch provider to Noop without state mutation
EXPECTED_PRIMARY_FILES = cameras/monitoramento/scheduler.py;
                         cameras/monitoramento/schemas.py
EXPECTED_NEW_FILES = cameras/monitoramento/observability.py
EXPECTED_TEST_FILES = cameras/test_monitoramento_observability.py
SHARED_FILES = scheduler instrumentation, owned before MON-WORKER integration
STOP_AND_ESCALATE_TO_SOL_IF = requested metric requires secret/high-cardinality
                              data or changes domain/audit semantics
```

Acceptance criteria:

1. Com fake cycle, sink recebe duration, queue, outcomes, stage failures,
   heartbeat e lease contention com nomes/labels fechados.
2. Com segredo/URI injetados em exception/config, serialização não os emite;
   valor não finito ou label fora da allowlist é rejeitado.
3. Com sink indisponível, scheduler mantém resultado de domínio e reporta
   falha operacional segura; nenhum `EventoAuditoria` nasce de probe normal.

## MON-RUNTIME-CONTRACT-FINAL-ADJUDICATION — matriz operacional

Matriz da proposta anterior. A seção de consolidação V1 abaixo prevalece
sobre status de aprovação/defaults e explicita a validação da configuração.

O modelo de recovery serial/capped/finito foi aprovado pelo usuário. Os
valores novos abaixo são propostas locais para aprovação, não configuração
implementada ou SLO homologado. Não executar código/testes para este parecer.
`C = concurrency`, `Q = queue_bound`, `P = probe_timeout_seconds`,
`S = shutdown_timeout_seconds`, `H = heartbeat_seconds`,
`I = cycle_interval_seconds`. Todos os tempos são segundos e budgets
monotônicos, exceto timestamps civis UTC de evidência persistida.

| PARAMETER | DEFAULT | MINIMUM | MAXIMUM | CONFIGURATION_SOURCE | TIMEOUT_RELATIONSHIP | FAILURE_BEHAVIOR | TEST_REQUIRED |
|---|---|---|---|---|---|---|---|
| PROBE_TIMEOUT | 5 | 1 | 30 | `MonitoringConfig.probe_timeout_seconds` EXISTING | connect_timeout <= P; para prontidão de runtime P <= DRAIN_DEADLINE | Cancelar execução, confirmar cleanup; só resultado de transporte classificado pelo adapter conta para confirmação; falha operacional não vira OFFLINE | timeout de probe/connect, adapter não cooperativo e cancelamento neutro |
| DATABASE_OPERATION_DEADLINE | 5 PROPOSED | 0.1 PROPOSED | 30 PROPOSED | `db_operation_deadline_seconds` NEW PROPOSED | deadline total da chamada lógica ORM, não um novo timeout por query; DB <= S - DRAIN_DEADLINE; na parada usar min(DB, budget restante) | Fechar admissão; timeout de espera não prova rollback ou término; marcar write incerto e reconciliar sem retry cego | connect/lock/statement bloqueados, transação multiquery, timeout do await com thread ainda viva, commit incerto |
| DRAIN_DEADLINE | S/2 = 15 | 0.5 derivado de S >= 1 | 150 derivado de S <= 300 | DERIVED from existing `shutdown_timeout_seconds`; no new field | fase de drain até stop_started + S/2; metade restante reservada a cancellation/cleanup/release | Suspender admissão, preservar ACTIVE; ao vencer pedir cancelamento e comprovar término; não substituir scheduler enquanto houver operação pendente | tasks ACTIVE, fila não admitida, reload repetido não estende prazo, drain vencido |
| SHUTDOWN_DEADLINE | 30 | 1 | 300 | `MonitoringConfig.shutdown_timeout_seconds` EXISTING | deadline global stop_started + S; inclui drain, cleanup e ORM; runtime exige P <= S/2 e DB <= S/2 | INCOMPLETE quando houver operação sem término comprovado; diagnóstico fatal, exit não zero apenas quando saída real for possível | salto UTC, tasks/adapter/ORM presos, releases sequenciais consumindo budget, STOPPED sem cleanup |
| RECOVERY_MAX_ATTEMPTS | 5 PROPOSED | 1 PROPOSED | 10 PROPOSED | `recovery_max_attempts` NEW PROPOSED | primeiro limite consumido entre tentativas e elapsed encerra recovery; cada tentativa tem deadline DB e pré-requisitos bounded | Fatal imediato para erro de segurança/config/schema; transitório esgotado vira falha persistente, mantém admissão fechada e inicia shutdown | contagem exata, sem recovery paralelo, fatal versus transitório, reset após sucesso completo |
| RECOVERY_MAX_ELAPSED | 900 PROPOSED | 1 PROPOSED | 3600 PROPOSED | `recovery_max_elapsed_seconds` NEW PROPOSED | contado da primeira falha até readiness restaurada; espera e operações consomem budget; desligamento tem seu próprio S | Não começar recovery depois do deadline; operação anterior ainda viva impede reabertura mesmo após timeout do chamador | deadline durante backoff/operação, nenhuma tentativa além do restante, nenhuma falsa recuperação |
| BACKOFF_INITIAL | min(H,I) = 30 | 10 derivado | 300 derivado | DERIVED from existing heartbeat/cycle; no new field | primeira tentativa só após b0; seguinte delay min(I, b0 * 2**n), cálculo saturado | Uma espera cancelável; stop interrompe backoff; sucesso completo reseta n=0 | primeira espera, exponencial capped, cancellation, reset entre episódios |
| BACKOFF_MAXIMUM | I = 300 | 30 | 3600 | DERIVED from existing `cycle_interval_seconds`; no new field | <= tempo restante de recovery para esperar; não estender elapsed para acomodar delay | Budget esgotado fecha recovery sem novo retry; não confundir com intervalo de evidência de câmera | teto e elapsed menor que delay, ausência de busy loop |

Extensão mínima proposta: somente três campos tipados, sem secrets ou
componente novo: `db_operation_deadline_seconds`, `recovery_max_attempts` e
`recovery_max_elapsed_seconds`. Drain, cleanup e backoff são derivados dos
campos existentes. Rejeitar bool, NaN/inf, valores fora do range e combinações
que violem os budgets. Não alterar silenciosamente ranges do core: a relação
P/DB <= S/2 é gate adicional de readiness do runtime, explicitamente proposto.

Justificativa dos valores novos: DB default 5/max 30 reaproveita o envelope
local existente de probe como ponto de partida reversível; mínimo 0.1 permite
budgets positivos curtos, sem alegar capacidade do banco. São escolhas locais,
não garantias derivadas de fencing. Com defaults, cinco tentativas DB de até
5 s e esperas 30/60/120/240/300 consomem no máximo 775 s, abaixo do budget
proposto de 900 s; outros pré-requisitos também consomem esse budget e podem
encerrar recovery antes. Os limites 10 tentativas/3600 s restringem input e
evitam recovery infinito; aprovação e validação operacional ainda necessárias.
A reserva S/2 prioriza drain e deixa cleanup finito sem outro parâmetro.

O contrato de DB deve provar que backend/driver conseguem aplicar o deadline
à operação lógica; timeouts de lock/query individual não garantem isso em
transação multiquery. Quando faltar mecanismo capaz de interromper/comprovar
término, readiness fica pendente e shutdown pode ser INCOMPLETE. Não usar
timeout de await como prova de encerramento nem acrescentar infraestrutura
para esconder essa limitação. Operações/release sequenciais usam o mesmo
deadline global; leases de produtores já parados podem expirar se não houver
tempo/DB para release, sem emitir falsa liberação.

Não criar estado RECOVERING: usar DEGRADED/DRAINING e sinais operacionais
existentes. Revalidar DB/config/policy/provider/adapter, resolver writes incertos
e reler memória/due antes de resetar backoff e admitir. Falha da telemetria
não altera domínio. Defaults/ranges de C, Q, jitter/freshness/lease permanecem
os de `schemas.py`, sem homologação produtiva implícita.

```text
MR_03_RECOVERY_MODEL = APPROVED
MR_03_OPERATIONAL_BUDGETS = PENDING / matrix values and relationships proposed
MONITORING_CONFIG_CONTRACT = PENDING / three-field extension proposed
PARAMETER_TESTS = REQUIRED_FOR_FUTURE_IMPLEMENTATION / NOT_EXECUTED
NEW_INFRASTRUCTURE = NONE
```

## MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION — configuração V1

O usuário adotou os defaults V1 abaixo. Reusar os ranges existentes e as
proteções da matriz anterior para os três campos novos, com validação cruzada
explícita. Isto é contrato da futura extensão, não mudança em `schemas.py`,
homologação de DB ou prova de shutdown. Não criar infraestrutura nova.

| PARAMETER | DEFAULT V1 | MINIMUM | MAXIMUM | CONFIGURATION_SOURCE | TIMEOUT_RELATIONSHIP | FAILURE_BEHAVIOR | TEST_REQUIRED |
|---|---|---|---|---|---|---|---|
| PROBE_TIMEOUT | 5 s | 1 s | 30 s | existing `probe_timeout_seconds` | 1 <= connect <= P; P <= S/2 | Timeout classificado pelo adapter; operacional/cancellation não gera OFFLINE; comprovar cleanup | defaults, connect/P e adapter não cooperativo |
| DATABASE_OPERATION_DEADLINE | 5 s | 0.1 s | 30 s | new `db_operation_deadline_seconds` | DB <= S/2; chamada lógica inteira e min(DB, budget global restante), nunca timeout renovado a cada query | Pausar admissão; ORM ainda viva permanece pinned; write incerto reconciliado sem retry cego | connect/lock/statement/multiquery, await expirado com thread viva, commit incerto |
| DRAIN_DEADLINE | S/2 = 15 s | 0.5 s derivado | 150 s derivado | derived from existing S | absoluto stop_started + S/2; metade restante para cancellation/cleanup/release | Timeout produz INCOMPLETE; não liberar ownership nem substituir por timeout presumido | drain vencido e término posterior, reload repetido sem extensão |
| SHUTDOWN_DEADLINE | 30 s | 1 s | 300 s | existing `shutdown_timeout_seconds` | absoluto stop_started + S; drain e toda espera/cleanup/release dentro do mesmo budget | Operação não terminada => INCOMPLETE; sem falsa saída/SUCCESS; admissão fechada | operação presa, salto UTC, deadlines globais e release condicionado |
| RECOVERY_MAX_ATTEMPTS | 5 | 1 | 10 | new `recovery_max_attempts` | contar somente chamadas de recovery, excluindo a falha inicial; stop no primeiro limite attempts/elapsed | Esgotado => falha persistente, admissão fechada e shutdown observável | contagem, fatal imediato, serialidade e reset |
| RECOVERY_MAX_ELAPSED | 900 s | 1 s | 3600 s | new `recovery_max_elapsed_seconds` | contado da primeira falha; > b0; DB <= recovery elapsed; esperas/ops limitadas pelo restante | Sem retry além do deadline; término não comprovado não permite reabertura | elapsed durante backoff/DB, commit incerto e ausência de falsa recuperação |
| BACKOFF_INITIAL | min(H,I) = 30 s | 10 s derivado | 300 s derivado | derived from existing heartbeat/cycle | b0=min(H,I); delay_n=min(I,b0*2**n), cálculo saturado, n=0 no primeiro recovery | Espera cancelável; reset n=0 somente após recuperação completa | sequência capped e episódios com reset |
| BACKOFF_MAX | I = 300 s | 30 s | 3600 s | derived from existing cycle interval | espera no máximo tempo restante de elapsed; não estender budget para caber delay | Elapsed esgotado interrompe recovery; não busy loop | teto, restante menor que delay, cancellation |

Validação antes de I/O: rejeitar bool em campos numéricos, NaN/inf, ranges
violados, connect>P, P>S/2, DB>S/2, DB>recovery elapsed ou recovery elapsed<=b0.
Ranges isolados não tornam toda combinação válida: S=1 com P=5 é rejeitada,
assim como DB=30 com S=30. Defaults completos passam: P=5, connect=3, DB=5,
drain=15, S=30, attempts=5, elapsed=900, b0=30, backoff max=300.

Extensão mínima de MonitoringConfig: `db_operation_deadline_seconds`,
`recovery_max_attempts`, `recovery_max_elapsed_seconds`, validação de tipos/
ranges e relações acima. Nenhum campo de drain/backoff/janela adicional.
Cinco recoveries DB <=5 s com esperas 30/60/120/240/300 somam <=775 s;
outros pré-requisitos e esperas também consomem elapsed. Isso demonstra
consistência do envelope default, não performance real ou cancelabilidade DB.

Deadline limita a espera autorizada e nova admissão, não garante término de
operação síncrona/native. Após timeout, não liberar slot/ownership enquanto
produtor puder produzir efeitos. Resultados de desfecho incerto exigem término
e reconciliação antes de retry. Success de recovery exige revalidação completa
e ausência de operação anterior pendente; DEGRADED/DRAINING são suficientes,
sem novo estado RECOVERING. Falha fatal não espera retries; transitório serial
usa os dois limites e o backoff aprovado, com reset após recuperação completa.

Fonte de configuração: snapshot tipado confiável do processo, carregado na
fronteira do command e versionado para substituição coordenada. CLI/browser
não fornecem owner, destino ou secrets; não criar provider/collector novo.
Cada espera respeita o deadline absoluto monotônico do seu episódio/fase.
Deadline de drain/shutdown vencido permanece INCOMPLETE, mesmo que cleanup
termine posteriormente; registrar resolução posterior sem reclassificar timeout
como graceful success. MON-OBS observa falhas sem alterar estado de câmera.

```text
DEFAULTS_V1 = ADOPTED_BY_USER
MONITORING_CONFIG_CONTRACT = CLOSED / LOCAL V1 SPECIFICATION
CONFIG_EXTENSION = THREE_FIELDS / NOT_IMPLEMENTED
MR_03_RECOVERY_MODEL = ADOPTED
OPERATIONAL_CAPABILITY_VALIDATION = REQUIRED_LATER / NOT_EXECUTED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
TESTS_CHANGED_OR_EXECUTED = NO
NEW_INFRASTRUCTURE = NONE
```

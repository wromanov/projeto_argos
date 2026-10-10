# Monitoramento — configuração e observabilidade

```text
ID = MON-OBS
STATUS = ACTIVE / LOCAL CONFIG SCHEMA
OPERATIONAL VALUES = NOT_HOMOLOGATED
BC02_STATUS = IMPLEMENTATION_READY
IMPLEMENTATION_READY = YES / LOCAL OBSERVABILITY PORT
IMPLEMENTER_TARGET = LUNA
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

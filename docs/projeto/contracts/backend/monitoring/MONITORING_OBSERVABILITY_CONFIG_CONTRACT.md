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
   falha operacional segura; nenhum `EventoAuditoria` nasce de probe normal.

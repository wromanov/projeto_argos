# Monitoramento — ownership de escrita

```text
ID = MON-OWN
STATUS = ACTIVE / LOCAL DATABASE CONTRACT
PRODUCTION DISTRIBUTED OWNERSHIP = NOT VALIDATED
BC02_STATUS = ALREADY_IMPLEMENTED / LOCAL CORE
IMPLEMENTATION_READY = NOT_APPLICABLE / PostgreSQL validation later
IMPLEMENTER_TARGET = LUNA for future integration
```

## Invariantes

No máximo um owner vigente por câmera pode finalizar uma tentativa de forma autoritativa. `monitoring_owner_id` é identidade técnica não secreta; `monitoring_lease_expires_at` é janela de claim; `monitoring_ownership_epoch` cresce monotonicamente e é o fencing token. Coerência entre owner e expiry é constraint persistente. Claim avalia expiry pelo relógio do banco; release/completion compara owner e epoch.

Com lease, completion exige ownership atual e geração de configuração idêntica. Sem lease, compare-and-set impede geração mais antiga de sobrescrever estado mais novo. Falha no gate retorna disposition explícita (`OWNERSHIP_LOST` ou `CONFIG_CHANGED`) e não grava transição/intervalo. A atomic completion atualiza estado, transição e intervalo dentro de transação.

## Responsabilidades

Cada instância recebe service instance ID não secreto, claim por alvo, heartbeat/renovação conforme futuro runtime, liberação condicional e métricas de denied/lost/stale completion. ID não é credencial de autenticação e não substitui restrição de banco. Nunca aceitar owner/epoch do browser.

## Limites

O modelo e repository implementam lease/fencing em SQLite local; não há deployment multi-worker/multi-host homologado. Sem PostgreSQL, contenção concorrente real e processo operacional, não afirmar lock distribuído de produção. Fonte: migration 0012; `DjangoMonitoringRepository` e `DueScheduler`; ADR-021 §§5–6.

## BC-02 — contrato de integração

`MODEL_CHANGE = NONE`; `MIGRATION_REQUIRED = NO`; `EXPECTED_MODELS =
EstadoMonitoramento existing`; `RELATIONSHIPS/CONSTRAINTS/INDEXES = migration
0012`; `DATA_MIGRATION = NO`; `ROLLBACK_CONSIDERATION = never regress epoch`.
Ownership: `cameras/monitoramento/repository.py`, `scheduler.py`; testes
`cameras/test_monitoramento_mon09b.py`, `test_monitoramento_mon09c.py`;
shared files com MON-WORKER. Critério: claim/release/completion sempre com
owner+epoch; worker obsoleto não altera domínio. PostgreSQL real permanece
validação externa. Escalar a Sol se concorrência real exigir alterar fencing.

## MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION — término e release V1

Nenhuma liberação explícita enquanto produtor real/ORM anterior ainda puder
produzir efeitos. Cancellation solicitada, timeout ou STOPPED de bookkeeping
não são comprovação. Completion aceita continua consumindo lease no commit
transacional cercado por owner/epoch/generation; após término do adapter e
sem outro escritor da tentativa. Release explícito continua condicionado a
owner/epoch, sem zerar epoch. Crash usa expiry/takeover/epoch já existentes;
expiry sozinha não invalida completion nem garante ausência de I/O antigo.

Coordenação de término, tentativa pinned e remoção de release automático
prematuro do scheduler são extensão **não implementada** especificada em
`MONITORING_WORKER_RUNTIME_CONTRACT.md`, seção de consolidação V1. Não altera
schema, tokens, repository CAS ou validação futura PostgreSQL/multi-worker.
Timeout de drain/shutdown é INCOMPLETE; não autoriza novo owner por suposição.

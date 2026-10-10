# Monitoramento — recuperação de falhas

```text
ID = MON-REC
STATUS = ACTIVE / LOCAL FAILURE SEMANTICS
MULTI_INSTANCE PRODUCTION = NOT VALIDATED
BC02_STATUS = ALREADY_IMPLEMENTED / LOCAL CORE
IMPLEMENTATION_READY = NOT_APPLICABLE / production validation later
IMPLEMENTER_TARGET = LUNA for future integration
```

## Falha de tentativa e do processo

Timeout/refusal entra na política de confirmação; resultado neutro, cancellation, erro operacional do adapter e falha de persistência não podem ser colapsados em indisponibilidade confirmada. Falha do worker ou banco interrompe avanço; a última evidência permanece e freshness torna estado efetivo desconhecido quando vence. Recovery retoma due work sem repetição de transição, sem duplicar intervalo aberto e sem captura automática.

## Completion atrasada e restart

`config_generation` impede gravação de completion obsoleta depois que configuração mudou; ownership epoch atua como fencing token quando lease está habilitada. Completion só atualiza estado se geração e owner/epoch continuarem atuais. Resultado antigo ou duplicado não regride observação. A gravação do estado/transição/intervalo ocorre transacionalmente; constraint limita um intervalo aberto por câmera.

No restart, confirmação persistida inclui estado estável, streaks, última observação e versão de política. Mudança de versão da política deve reinicializar confirmação segundo reducer; dados inválidos/órfãos bloqueiam completion e exigem diagnóstico. Lease expirável permite takeover, mas epoch monotônico, não a duração da lease, decide validade do writer anterior.

## Limites

Idempotência, stale-generation CAS, fencing e cenários de restart foram exercitados localmente com SQLite/simulação, inclusive escala sintética de cerca de 2.300 ativos. Isso não comprova PostgreSQL, múltiplos processos, particionamento de rede ou falhas reais. Recovery distribuído precisa de validação específica no banco/topologia alvo.

Referências: migrations `0010_estado_monitoramento.py`–`0012_monitoring_ownership_lease.py`; `repository.py`; evidência MON-08C/09 em `PROJECT_STATE.md`.

## BC-02 — ownership e aceite preservados

`MODEL_CHANGE = NONE`; `MIGRATION_REQUIRED = NO`; `EXPECTED_MODELS =
EstadoMonitoramento/TransicaoEstadoMonitoramento/Indisponibilidade existing`;
`RELATIONSHIPS/CONSTRAINTS/INDEXES = migrations 0010–0012`; `DATA_MIGRATION =
NO`; `ROLLBACK_CONSIDERATION = preserve history and owner epoch`. Ownership:
`cameras/monitoramento/repository.py`, `scheduler.py`; testes
`cameras/test_monitoramento_mon08c.py`, `test_monitoramento_mon09c.py`;
shared files com MON-WORKER, portanto integração sequencial. Critério:
generation/owner antigo não escreve nem fecha intervalo de novo owner;
restart não duplica transição. PostgreSQL/multi-worker exige validação futura.
Escalar a Sol se o banco alvo invalidar atomic completion/fencing.

## MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION — recovery V1

Recovery V1 é serial e bounded pelos campos `recovery_max_attempts` e `recovery_max_elapsed_seconds` definidos na matriz vigente de MON-OBS; usa DEGRADED e reseta somente após recuperação completa. Esgotamento é falha persistente observável. Não criar estado `RECOVERING`, repetir store de desfecho incerto, nem liberar ownership enquanto o término do produtor não estiver comprovado. Falhas operacionais, cancelamento e erro de banco não geram `OFFLINE`.

A classificação terminal é local e limitada a `W = C + Q`; tentativas totais não excedem `2(C+Q)`. Após eviction, callback desconhecido é rejeitado antes de load/claim/store, sem ledger, expurgo persistente ou mudança de memória de confirmação/histórico. Fencing por owner/epoch/config_generation, expiry sem takeover e completion atômica via repository mantêm a semântica V1. Critérios DC-01..07 e limites PostgreSQL/multi-worker, rede/câmera, capacidade e deploy são gates futuros, não evidência de implementação.

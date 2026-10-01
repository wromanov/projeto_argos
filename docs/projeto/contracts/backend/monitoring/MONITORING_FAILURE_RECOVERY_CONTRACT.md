# Monitoramento — recuperação de falhas

```text
ID = MON-REC
STATUS = ACTIVE / LOCAL FAILURE SEMANTICS
MULTI_INSTANCE PRODUCTION = NOT VALIDATED
```

## Falha de tentativa e do processo

Timeout/refusal entra na política de confirmação; resultado neutro, cancellation, erro operacional do adapter e falha de persistência não podem ser colapsados em indisponibilidade confirmada. Falha do worker ou banco interrompe avanço; a última evidência permanece e freshness torna estado efetivo desconhecido quando vence. Recovery retoma due work sem repetição de transição, sem duplicar intervalo aberto e sem captura automática.

## Completion atrasada e restart

`config_generation` impede gravação de completion obsoleta depois que configuração mudou; ownership epoch atua como fencing token quando lease está habilitada. Completion só atualiza estado se geração e owner/epoch continuarem atuais. Resultado antigo ou duplicado não regride observação. A gravação do estado/transição/intervalo ocorre transacionalmente; constraint limita um intervalo aberto por câmera.

No restart, confirmação persistida inclui estado estável, streaks, última observação e versão de política. Mudança de versão da política deve reinicializar confirmação segundo reducer; dados inválidos/órfãos bloqueiam completion e exigem diagnóstico. Lease expirável permite takeover, mas epoch monotônico, não a duração da lease, decide validade do writer anterior.

## Limites

Idempotência, stale-generation CAS, fencing e cenários de restart foram exercitados localmente com SQLite/simulação, inclusive escala sintética de cerca de 2.300 ativos. Isso não comprova PostgreSQL, múltiplos processos, particionamento de rede ou falhas reais. Recovery distribuído precisa de validação específica no banco/topologia alvo.

Referências: migrations `0010_estado_monitoramento.py`–`0012_monitoring_ownership_lease.py`; `repository.py`; evidência MON-08C/09 em `PROJECT_STATE.md`.

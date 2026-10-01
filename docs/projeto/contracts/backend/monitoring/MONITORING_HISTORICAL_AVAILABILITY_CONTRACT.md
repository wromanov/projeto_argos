# Monitoramento — histórico de disponibilidade

```text
ID = MON-HIST
STATUS = ACTIVE / DOMAIN AND READ CONTRACT
BC02_STATUS = ALREADY_IMPLEMENTED / LOCAL CORE
IMPLEMENTATION_READY = NOT_APPLICABLE / no new standalone slice
IMPLEMENTER_TARGET = LUNA for future integration
```

## Modelo histórico

`TransicaoEstadoMonitoramento` armazena apenas mudança de estado estável por câmera, estado anterior/atual e instante observado. Repetição de probe no mesmo estado não cria linha. `Indisponibilidade` representa intervalo técnico confirmado: no máximo um aberto por câmera; abertura associada 1:1 à transição para OFFLINE; fechamento por transição ONLINE (`RECUPERADA`) ou retirada do escopo (`SAIU_DO_ESCOPO`, sem transição fictícia). Intervalo é histórico técnico, não evento de usuário.

Tempo de abertura/fechamento deve ser aware UTC; fim não antecede início. Indisponibilidade iniciada como `UNKNOWN -> OFFLINE` usa `INITIAL_OFFLINE`; `ONLINE -> OFFLINE` usa `ONLINE_TO_OFFLINE`. Saída do escopo fecha intervalo atual sem dizer que a câmera recuperou. Retorno ao escopo começa em UNKNOWN.

## Consulta

Read service devolve projeção allowlisted, status/freshness/escopo e resumo de intervalo aberto. Histórico por câmera é ordenado mais recente primeiro e paginado com limite máximo 100; consumidor não carrega histórico integral em tela de listagem. Erros e dados de configuração/credencial ficam fora da projeção.

## Retenção

O contrato não fixa retenção/expurgo do histórico. Não excluir intervalo/transição automaticamente sem decisão de retenção, legal/operacional e governança. Fonte: ADR-020 §§8–9, 13; models `EstadoMonitoramento`, `TransicaoEstadoMonitoramento`, `Indisponibilidade`; migration 0011; `MonitoringReadService`.

## BC-02 — semântica preservada

`MODEL_CHANGE = NONE`; `MIGRATION_REQUIRED = NO`; `EXPECTED_MODELS =
TransicaoEstadoMonitoramento/Indisponibilidade existing`; `RELATIONSHIPS/
CONSTRAINTS/INDEXES = migration 0011`; `DATA_MIGRATION = NO`;
`ROLLBACK_CONSIDERATION = preserve historical rows`. Ownership:
`cameras/monitoramento/read_service.py`, `repository.py`; testes
`cameras/test_monitoramento_indisponibilidade.py` e
`test_monitoramento_read_service.py`; shared files com MON-WORKER integração
sequencial. Critério: teste manual A-D não cria transição/intervalo; OFFLINE
confirmado abre no máximo um intervalo e recuperação o fecha uma vez.
Escalar a Sol se surgir política de retenção/expurgo fora do escopo.

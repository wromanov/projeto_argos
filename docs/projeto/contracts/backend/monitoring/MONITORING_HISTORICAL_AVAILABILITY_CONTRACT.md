# Monitoramento — histórico de disponibilidade

```text
ID = MON-HIST
STATUS = ACTIVE / DOMAIN AND READ CONTRACT
```

## Modelo histórico

`TransicaoEstadoMonitoramento` armazena apenas mudança de estado estável por câmera, estado anterior/atual e instante observado. Repetição de probe no mesmo estado não cria linha. `Indisponibilidade` representa intervalo técnico confirmado: no máximo um aberto por câmera; abertura associada 1:1 à transição para OFFLINE; fechamento por transição ONLINE (`RECUPERADA`) ou retirada do escopo (`SAIU_DO_ESCOPO`, sem transição fictícia). Intervalo é histórico técnico, não evento de usuário.

Tempo de abertura/fechamento deve ser aware UTC; fim não antecede início. Indisponibilidade iniciada como `UNKNOWN -> OFFLINE` usa `INITIAL_OFFLINE`; `ONLINE -> OFFLINE` usa `ONLINE_TO_OFFLINE`. Saída do escopo fecha intervalo atual sem dizer que a câmera recuperou. Retorno ao escopo começa em UNKNOWN.

## Consulta

Read service devolve projeção allowlisted, status/freshness/escopo e resumo de intervalo aberto. Histórico por câmera é ordenado mais recente primeiro e paginado com limite máximo 100; consumidor não carrega histórico integral em tela de listagem. Erros e dados de configuração/credencial ficam fora da projeção.

## Retenção

O contrato não fixa retenção/expurgo do histórico. Não excluir intervalo/transição automaticamente sem decisão de retenção, legal/operacional e governança. Fonte: ADR-020 §§8–9, 13; models `EstadoMonitoramento`, `TransicaoEstadoMonitoramento`, `Indisponibilidade`; migration 0011; `MonitoringReadService`.

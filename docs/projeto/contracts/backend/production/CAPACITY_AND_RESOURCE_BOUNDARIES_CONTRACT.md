# Capacidade e fronteiras de recursos

```text
ID = PROD-CAP
STATUS = ACTIVE / EVIDENCE-BOUNDED BASELINE
PRODUCTION_CAPACITY = NOT_VALIDATED
```

## Evidência disponível

Os checkpoints MON-08 exercitaram SQLite local, uma instância, probes sintéticos/determinísticos, cerca de 2.300 ativos e concorrência observada/configurada de 20, incluindo falha/recovery, restart/idempotência e stale-generation/CAS. Evidência não equivale a benchmark de rede/equipamento real ou previsão de SLA. Consulte os registros MON no `PROJECT_STATE.md` e os documentos MON-08/09 para métricas exatas; não generalize o envelope.

## Limites de recurso

Todo probe/capture tem timeout e limite de concorrência; fila é bounded; respostas HTTP/bytes/imagens e decode de pixels têm limites; histórico é paginado; queries para listas são em lote quando implementado. Backpressure não deve causar memória sem limite. Captura, decode e storage nunca atrasam o ciclo de monitoramento. No overload, adiar trabalho e emitir métrica; não remover limites nem gravar transição falsa.

`MonitoringConfig` local valida ranges: concorrência 1–100; ciclo 5–86400 s; timeout de probe 1–30 s; connect entre 1 e timeout total; fila padrão 2× concorrência e máximo 10×; jitter até 20%; freshness configurável entre ciclo e 86400 s; shutdown 1–300 s; heartbeat 10–300 s; lease configurável bounded. Defaults são guardrails de código, não valores de capacidade aprovados para operação real.

## Fronteiras não validadas

PostgreSQL, múltiplas instâncias/workers, lease distribuída sob contenção, rede/VLAN/firewall real, câmeras/credenciais reais, throughput de adapters, performance de produção, consumo de CPU/memória, storage growth, retenção, RPO/RTO, SLO/alertas e limites formais de capacidade. Qualquer operação depende de medição no ambiente alvo e budget humano aprovado. Fonte: ADR-019/021; `MonitoringConfig`; checkpoints MON-08/09.

# Monitoramento — configuração e observabilidade

```text
ID = MON-OBS
STATUS = ACTIVE / LOCAL CONFIG SCHEMA
OPERATIONAL VALUES = NOT_HOMOLOGATED
```

## Configuração

`MonitoringConfig` valida valores tipados e bounded para concorrência, intervalo de ciclo, timeout de probe/connect, fila, jitter (máximo 20%), freshness, shutdown, heartbeat e lease. Defaults e ranges no código são proteções reversíveis do core, não SLOs aprovados. Deploy futuro deve carregar valores por ambiente a partir de configuração confiável e versionar política de confirmação; nenhum segredo deve entrar nesse objeto/log.

Rejeitar booleano no lugar de número, NaN/inf, valores fora do range ou timeout de conexão superior ao timeout total. Fila limitada; overflow é deferred/diagnóstico, nunca crescimento ilimitado de memória. Jitter determinístico deve espalhar cadência sem mudar o intervalo contratual de domínio.

## Sinais mínimos

Estado de lifecycle, heartbeat, início/fim do último ciclo, duração, elegíveis/due/admitidos/deferred/queued/active, counts de tentativas iniciadas/concluídas/canceladas, falhas operacionais, ownership acquired/denied/lost e stale completion rejected. Percentis de latência/idade de evidência, backlog, freshness stale, DB error e distribuição de categorias podem ser agregados. Definir retenção/cardinalidade e limiares somente com SLO/observação do ambiente.

## Sigilo

Logs/traces não contêm segredo, username, URL/RTSP path, conteúdo, headers auth ou configuração sensível. Códigos de erro são allowlisted/sanitizados; não guardar stack trace com material do request secreto. Telemetria de serviço não é `EventoAuditoria` por probe normal.

Fonte: `cameras/monitoramento/schemas.py`, `scheduler.py`; ADR-021 §8. Métricas, backend e alarmes operacionais ainda não estão implantados.

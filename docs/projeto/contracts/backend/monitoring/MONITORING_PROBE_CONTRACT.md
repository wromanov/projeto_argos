# Monitoramento — contrato de probe

```text
ID = MON-PROBE
STATUS = ACTIVE / CORE IMPLEMENTED, ADAPTERS NOT HOMOLOGATED
```

## Pipeline

`ProbeRequest` é destino já resolvido e possui `camera_id`, IPv4, porta, `adapter_key`, timeout positivo e endpoint relativo opcional sem userinfo/URL. `ProbeAdapter` é protocol assíncrono. `ProbeResult` é imutável, timestamp aware UTC, duração finita não negativa e categoria/error code validados. Interface do adapter não define como destinos/segredos são autorizados; isso é pré-condição CAM-INT-01/02/07.

Categorias fechadas atuais: `SUCCESS`, `TIMEOUT`, `CONNECTION_REFUSED`, `AUTH_FAILURE`, `TLS_ERROR`, `PROTOCOL_ERROR`, `CONFIG_ERROR`, `TARGET_BLOCKED`, `CANCELLED`, `INCONCLUSIVE`. Não acrescentar código sem compatibilizar reducer, métricas, logs e política de confirmação.

## Confirmação e ordem

Reducer puro de `confirmation.py` mantém somente uma direção de streak por vez, ignora resultados fora de ordem e trata timestamp duplicado como ambíguo. Cancelamento e resultados neutros funcionam como barreira; auth/TLS/protocolo/configuração/bloqueio não são prova de indisponibilidade. Thresholds são configuração versionada; OFFLINE exige ao menos duas falhas pela validação atual e ONLINE ao menos um sucesso, sem afirmar que tais valores estão homologados para ambiente real.

Probe executa fora do ciclo HTTP. Timeout/cancelamento é bounded, não persiste conteúdo bruto e não chama captura. Real endpoint/adapters, frequência de execução, timeouts por protocolo e associação vendor/firmware requerem homologação.

Fontes: `cameras/monitoramento/contracts.py`, `confirmation.py`, `schemas.py`; ADR-020/021.

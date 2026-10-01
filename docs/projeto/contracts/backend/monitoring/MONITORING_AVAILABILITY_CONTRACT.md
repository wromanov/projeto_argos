# Monitoramento — disponibilidade técnica

```text
ID = MON-AV
STATUS = ACTIVE / DOMAIN BASELINE
SOURCE_AUTHORITY = ADR-020; ADR-019
```

## Estado e escopo

Os estados técnicos estáveis são `UNKNOWN`, `ONLINE` e `OFFLINE`. `SUSPECT` é estado transitório do reducer; `STALE` qualifica freshness; nenhum deles é estado persistido adicional. Situação operacional da câmera é dimensão distinta. Elegibilidade inicial exige situação `PRODUCAO` e configuração suficiente; estoque, desativada e cadastro incompleto ficam fora do escopo e não devem gerar OFFLINE.

`ONLINE/OFFLINE` persistido representa última confirmação estável. Se a evidência envelhece, o estado efetivo corrente é `UNKNOWN (stale)`, sem apagar o estado histórico, abrir incidente ou registrar transição. O limite `stale_after` é configurável no schema local, mas precisa ser homologado na operação. Estado de saúde do worker é distinto de saúde da câmera.

## Transições

Somente confirmação de evidência segundo política anti-flapping pode mudar o estado estável. `UNKNOWN -> ONLINE`, `UNKNOWN -> OFFLINE`, `ONLINE -> OFFLINE` e `OFFLINE -> ONLINE` são transições relevantes. Falha isolada, timeout sem confirmação, erro de auth/configuração, cancellation, worker parado ou falta de evidência fresca não bastam. Entrada no escopo reinicia a verdade corrente em `UNKNOWN`; saída do escopo não é recuperação técnica.

## Estado observado

`EstadoMonitoramento` implementa estado, evidência útil, prazo, geração de configuração, streaks, versão de política, elegibilidade e ownership. Campos antigos `Camera.status`, `status_em` e `ultima_verificacao` coexistem no cadastro; não devem ser confundidos com produtor canônico do subsistema novo. Leitura canônica está em `MonitoringReadService`; browser consome estado conhecido e nunca executa probe.

Captura de imagens não ocorre em primeira detecção, retorno a ONLINE ou evento de disponibilidade. Fonte: ADR-019/020; `cameras/models.py`, `cameras/monitoramento/read_service.py`.

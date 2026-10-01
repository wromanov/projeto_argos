# Monitoramento — runtime do worker

```text
ID = MON-WORKER
STATUS = ARCHITECTURAL CONTRACT
PRODUCTION_WORKER = NOT_IMPLEMENTED / NOT_DEPLOYED
```

## Separação de execução

Probe contínuo pertence a processo/worker dedicado, independente de request/response web. Django/browser exibe estado persistido e pode solicitar leituras; não varre câmeras, não mantém conexão contínua nem dispara probe ao renderizar tela. Captura permanece fluxo separado e sob demanda.

## Ciclo do runtime

O núcleo local implementa scheduler due-based com fila limitada, concorrência limitada, timeout, ciclo de drain/shutdown, idempotência por alvo, estado operacional e lease/fencing portável. O runtime de produção deverá: descobrir candidatos elegíveis em lote; agendar due com jitter; adquirir ownership; executar adapter; reduzir resultado; persistir completion com fencing; liberar lease; registrar telemetria sanitizada; e fechar de forma previsível ao desligar.

Nenhuma tecnologia de fila, processo, cron/scheduler externo, Celery/Redis/RQ, supervisor, quantidade de instâncias ou política de restart está escolhida pelo ADR-019. Não há command/deployment de worker comprovado no checkout. O serviço não deve executar como root nem conta admin, e precisa de egress e identidade próprios.

## Readiness e falha

Saúde de processo/worker é diferente de estado de câmera. Falha ao iniciar, ausência de heartbeat, banco indisponível ou fila saturada deve aparecer como falha do subsistema e deixar estado da câmera envelhecer para stale; não gerar OFFLINE em massa. Readiness deve impedir admissão se configuração de segurança/DB/adapters não estiver pronta. Stop controla admissão, drena ou cancela dentro de deadline e nunca interpreta cancelamento como falha de probe.

Referências: ADR-019/020/021; `cameras/monitoramento/scheduler.py`; `config/asgi.py`/`wsgi.py` não comprovam deployment dedicado.

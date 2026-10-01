# Topologia de runtime

```text
ID = PROD-TOPO
STATUS = ACTIVE / ARCHITECTURAL BOUNDARY
TOPOLOGY = NOT SELECTED / NOT DEPLOYED
```

## Componentes e fronteiras necessárias

Web Django atende interação e leituras/mutações autorizadas. Worker dedicado executa monitoramento contínuo, isolado de HTTP, com identidade, banco e egress de rede de menor privilégio. Serviço de captura sob demanda deve ser fronteira separada (pode compartilhar runtime do worker somente mediante decisão e isolamento adequados) e nunca é implicitamente acionado por probe. Banco e storage privado são dependências explícitas e observáveis. Browser não se conecta à câmera.

## Requisitos de deployment

Definir processos/replicas, scheduler, distribuição de trabalho, limites de concorrência, startup/readiness/liveness, heartbeat, rolling update, shutdown/drain/cancel, restart/backoff, clock, secrets, egress, firewall e deploy/migration ordering. Um worker parado não produz OFFLINE em massa; freshness torna evidência stale. Duplicação de worker exige ownership/lease/fencing no banco alvo. Contas de serviço não são contas humanas e não executam como root.

## Não decisões

ADR-019 explicitamente não escolhe Celery, Redis, RQ, asyncio, threads, cron, filas, SSE/WebSocket ou outros mecanismos. O código atual contém núcleo de scheduler assíncrono testável e WSGI/ASGI Django, mas nenhum processo/service/deployment dedicado confirmado. Não deduzir topologia da presença do código. Seleção exige capacity, operação, segurança e banco acordados; não habilita LIVE ou homologação por si só.

Referências: ADR-019; ADR-021 §§5–6, 9; `cameras/monitoramento/scheduler.py`; `config/wsgi.py`, `config/asgi.py`.

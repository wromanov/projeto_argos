# ADR-019 — Monitoramento de Disponibilidade e Gestão de Imagens

**Status:** Aprovado
**Data:** 11/08/2026

## Contexto

O ARGOS administra inventário e governança de câmeras e deverá evoluir para acompanhar a disponibilidade técnica de aproximadamente 2.300 ativos. Essa evolução não pode transformar o servidor web Django nem o navegador em agentes de monitoramento contínuo.

O projeto também reavaliou a política anterior de snapshots automáticos relacionados a eventos de disponibilidade. A operação passa a exigir evidências visuais sob controle explícito do operador.

## Decisão

### Monitoramento de disponibilidade

O monitoramento futuro será executado por processo(s) ou worker(s) independentes do ciclo HTTP da aplicação web. O ARGOS Web consultará o estado conhecido e persistido pelo ARGOS; o navegador não fará probes diretos no parque de câmeras.

O estado deverá abranger, conforme o contrato futuro, status técnico atual, última vez ONLINE, última vez OFFLINE, momento de mudança e histórico de indisponibilidades ou transições quando aplicável. A persistência deve se concentrar em mudanças relevantes, sobretudo `ONLINE -> OFFLINE` e `OFFLINE -> ONLINE`, e não em cada probe normal repetido.

O futuro motor deverá conter mecanismos anti-flapping, concorrência controlada, parâmetros configuráveis e validação de escala. **Status técnico não é situação operacional**: uma câmera em `PRODUÇÃO` pode estar tecnicamente `OFFLINE`.

### Gestão de imagens

Não haverá captura automática baseada na primeira detecção, no retorno `OFFLINE -> ONLINE`, nem em outra mudança automática de disponibilidade. A operação futura será exclusivamente sob demanda do operador:

- **Capturar imagem**: tentativa de obter imagem diretamente da câmera;
- **Importar imagem**: envio de arquivo que o backend deverá validar efetivamente.

A proveniência será preservada, distinguindo conceitualmente `CAPTURA_CAMERA` e `UPLOAD_MANUAL`. A nomenclatura definitiva de modelos, campos e enums permanece em aberto.

### Desacoplamento

Monitoramento e captura de imagens são responsabilidades independentes. Captura lenta, indisponível ou com falha não deve bloquear nem degradar a operação de monitoramento.

## Consequências e trade-offs

Benefícios: a aplicação web deixa de concentrar trabalho de I/O do parque; estado e transições tornam-se consultáveis com eficiência; evidências visuais passam a ter autoria e proveniência controláveis; e monitoramento e imagens podem evoluir separadamente.

Custos: serão necessários discovery técnico, processo operacional para worker(s), testes de carga, regras de segurança para credenciais e uploads, e contrato posterior de retenção e histórico visual.

## Requisitos substituídos

Para o trabalho futuro, estão substituídos:

- captura automática no retorno `OFFLINE -> ONLINE`;
- captura automática na primeira detecção;
- snapshots automáticos acoplados ao monitoramento;
- rotação automática das três últimas imagens baseada nesses eventos.

Esses requisitos permanecem preservados nos documentos históricos que os registram em seu contexto original.

## Itens deliberadamente em aberto

`MON-01` e as fases de imagens deverão definir, com evidência:

- tecnologia de worker, fila e scheduler;
- protocolo e estratégia de probe;
- limites de concorrência, intervalos, timeouts e retries;
- critérios quantitativos de anti-flapping;
- mecanismo de atualização da interface;
- método padrão de captura direta, que poderá variar por capacidade do equipamento;
- storage, retenção, imagem principal e integridade das imagens.

Este ADR não escolhe Celery, Redis, RQ, asyncio, threads, ICMP, TCP, HTTP, RTSP, WebSocket, SSE ou valores fixos de execução.

## Referências

- [Roadmap ARGOS v5](ROADMAP_ARGOS_V5.md)
- [Arquitetura](03_arquitetura.md)
- [Índice de decisões arquiteturais](07_decisoes_arquiteturais.md)

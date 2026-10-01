# Diagnóstico de saúde técnica da câmera

```text
STATUS = ACTIVE / DOMAIN CONTRACT
REAL_PROBE_VALIDATION = NOT_PERFORMED
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / A-B-C-D PROJECTION
IMPLEMENTER_TARGET = LUNA
```

## Semântica

Saúde técnica responde apenas à evidência produzida pelo mecanismo de probe contratado. Não equivale a situação operacional (`PRODUCAO/ESTOQUE/DESATIVADA`), qualidade de vídeo, gravação no VMS, imagem atual, gravação contínua ou integridade física completa do equipamento.

Estados estáveis: `UNKNOWN`, `ONLINE`, `OFFLINE`. `SUSPECT` é estado efêmero do reducer; freshness é qualificador separado (`FRESH/STALE`); fora de escopo e configuração incompleta são condições de elegibilidade, não estado técnico. `STALE` projeta estado efetivo desconhecido sem apagar último estado estável nem criar OFFLINE.

## Elegibilidade, confirmação e apresentação

Escopo conceitual requer câmera em produção e configuração técnica válida, autorizada e suportada. Estoque, desativada e configuração incompleta não são falha de rede. A implantação local de leitura atualmente deriva elegibilidade de `situacao_operacional == PRODUCAO` e `cadastro_completo`; perfil, capability, allowlist e credencial ainda não existem, portanto isso não habilita probes reais.

O usuário recebe estado efetivo, frescor, instante da última evidência útil, instante desde a transição estável, condição de escopo e indisponibilidade aberta. Resultado isolado de probe nunca deve promover estado. Auth/configuração/bloqueio, cancellation, inconclusivo ou evidência stale não se traduzem automaticamente em OFFLINE.

## Limites

Histórico e leitura são do domínio de monitoramento, não `EventoAuditoria` de usuário por probe. Saúde não inicia captura e imagem não confirma saúde. Fonte: ADR-020 §§3–9, 13–15; ADR-021 §§4 e 8; `MonitoringReadService`.

## BC-02 — leitura de health em quatro estágios

Expor A NETWORK_REACHABILITY, B RTSP_REACHABILITY, C MEDIA_DESCRIPTION e
D MEDIA_DELIVERY da última `CameraHealthSnapshot` automática com instante,
frescor e `PASS/FAIL/NOT_RUN`, sem inferir PASS de estágio não observado.
`ONLINE` efetivo somente após D PASS automático confirmado pelo reducer e
enquanto fresco; teste manual A-D PASS não promove ONLINE. A/B/C PASS sem D
não prova disponibilidade de mídia. Snapshot ausente ou obsoleto é
UNKNOWN/stale na projeção sem apagar último estado estável. Diagnóstico
detalhado exige `view_camera_diagnostic`; resumo de status acompanha
`view_camera`. Nenhum path, URI completa, username ou segredo é exposto.

```text
MODEL_CHANGE = NONE beyond CameraHealthSnapshot in CAM-INT-05
MIGRATION_REQUIRED = NO IN THIS SLICE
EXPECTED_MODELS = CameraHealthSnapshot; EstadoMonitoramento existing
RELATIONSHIPS = Camera 1:1 Snapshot
CONSTRAINTS = inherited from CAM-INT-05
INDEXES = inherited from CAM-INT-05
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = fall back to existing UNKNOWN/ONLINE/OFFLINE projection
EXPECTED_PRIMARY_FILES = cameras/monitoramento/read_service.py
EXPECTED_NEW_FILES = NONE REQUIRED
EXPECTED_TEST_FILES = cameras/test_monitoramento_read_service.py;
                      cameras/test_camera_diagnostics.py
SHARED_FILES = monitoring read service; integration after CAM-INT-05
STOP_AND_ESCALATE_TO_SOL_IF = UI requires health semantic beyond A-D/stale
```

Acceptance criteria: D PASS manual não altera status; D PASS automático
confirmado pode resultar ONLINE; A-C PASS/D NOT_RUN mostra health incompleto;
snapshot stale mostra UNKNOWN efetivo sem transição falsa; usuário sem
permissão de diagnóstico não recebe detalhe técnico.

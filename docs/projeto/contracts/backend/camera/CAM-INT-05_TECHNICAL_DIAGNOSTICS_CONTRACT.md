# CAM-INT-05 — Diagnósticos técnicos de integração

```text
STATUS = ACTIVE / CONTRACT BASELINE
PROBE_ADAPTERS = FAKE/LAB BOUNDARY ONLY; NO REAL CAMERA HOMOLOGATION
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / STAGE SCHEMA AND LOCAL INTEGRATION
IMPLEMENTER_TARGET = LUNA
```

## Observação e resultado

Tentativa de probe é evidência transitória; não é estado de disponibilidade nem incidente. O contrato local `ProbeResult` exige código fechado, instante aware convertido a UTC, duração finita e não negativa e `error_code` curto sem URL. `SUCCESS` não pode levar erro. Categorias atuais: `SUCCESS`, `TIMEOUT`, `CONNECTION_REFUSED`, `AUTH_FAILURE`, `TLS_ERROR`, `PROTOCOL_ERROR`, `CONFIG_ERROR`, `TARGET_BLOCKED`, `CANCELLED`, `INCONCLUSIVE`.

Na redução atual, somente sucesso e falha de transporte classificadas conforme política aprovada contam como evidência direcional; auth/TLS/protocolo/configuração/bloqueio/inconclusivo funcionam como barreira neutra, e cancelamento não é falha do dispositivo. Resultado atrasado não pode reverter observação mais recente; timestamp igual é ambíguo. Uma tentativa isolada não promove estado: confirmação produz `UNKNOWN/ONLINE/OFFLINE` e sequência interna não vira status público.

## Sanitização e armazenamento

Erro diagnóstico comunica categoria/código seguro e, quando necessário, correlação opaca. Nunca conter senha, username, URL completa, query string, path com token, header, resposta de autenticação, payload de imagem ou detalhe de rede sensível. Probe repetido normal não cria evento de auditoria de usuário nem indisponibilidade adicional. Métricas agregadas podem incluir latência e contagens sem identificação secreta.

## Limite de evidência

O código tem adapter protocol e fakes; não prova conector RTSP/HTTP real, câmera suportada ou significado operacional universal de `SUCCESS`. O diagnóstico deve declarar camada testada (IP/porta, HTTP, autenticação, sessão RTSP, imagem decodificada) e o que não foi testado. Fonte: ADR-020 §§3–5; ADR-021 §§4, 8; `cameras/monitoramento/contracts.py`, `confirmation.py`.

## BC-02 — estágios A/B/C/D e teste manual

`HealthStageResult` imutável por estágio tem `stage` (`A/B/C/D`),
`state` (`PASS/FAIL/NOT_RUN`), `observed_at` UTC, duração finita ≥0 e
`error_code` allowlisted opcional. A = NETWORK_REACHABILITY (TCP ao IP/porta
autorizados); B = RTSP_REACHABILITY (negociação RTSP válida); C =
MEDIA_DESCRIPTION (DESCRIBE/SDP de vídeo com codec identificado); D =
MEDIA_DELIVERY (frame/mídia decodificada válida recebida). `ConnectionTestResult`
agrupa os quatro em ordem, config version, fonte `MANUAL/AUTOMATIC` e
correlation ID opaco. FAIL em A/B/C torna os seguintes NOT_RUN; D só pode
PASS se A/B/C PASS. `SUCCESS` do `ProbeResult` automático exige D PASS.
Auth/config/policy/decoder/protocolo não são falha direcional de câmera; não
geram OFFLINE. Timeout/refusal entram na confirmação existente apenas quando
classificados como evidência de transporte válida pelo contrato de probe.

`CameraHealthSnapshot` 1:1 com Camera guarda somente a última sequência
**automática** A-D sanitizada, observed_at, config_generation e estágio
alcançado, sem SDP, frame, URI ou segredo. Atualização usa CAS de geração e
ownership existente; resultado stale/obsoleto não sobrescreve snapshot.
Teste MANUAL chama o mesmo port de adapter via service autorizado, mas não
atualiza snapshot automático, `EstadoMonitoramento`, streak, transição ou
indisponibilidade. Resposta manual é efêmera, não cacheável, auditada com
resultado sanitizado. Teste pode ocorrer em profile UNVERIFIED para discovery
sob policy aprovada; não habilita automaticamente monitoring/capture.

```text
MODEL_CHANGE = CameraHealthSnapshot
MIGRATION_REQUIRED = YES
EXPECTED_MODELS = CameraHealthSnapshot
RELATIONSHIPS = Camera 1:1 Snapshot
CONSTRAINTS = one snapshot/camera; config_generation > 0; stage enum/coherence
INDEXES = (observed_at); camera unique by OneToOne
DATA_MIGRATION = NO; old status fields do not imply A/B/C/D
ROLLBACK_CONSIDERATION = drop derived snapshots only; preserve monitoring history
EXPECTED_PRIMARY_FILES = cameras/models.py; cameras/monitoramento/contracts.py;
                         cameras/monitoramento/repository.py
EXPECTED_NEW_FILES = cameras/integracao/diagnostics.py
EXPECTED_TEST_FILES = cameras/test_camera_diagnostics.py; cameras/test_monitoramento_probe.py
SHARED_FILES = cameras/models.py/migrations; monitoring integration port
STOP_AND_ESCALATE_TO_SOL_IF = a new stage/state is required; D evidence cannot
                              be represented without changing ADR-020
```

Acceptance criteria:

1. A-D PASS automático gera um único `ProbeResult.SUCCESS`; A-C PASS/D FAIL
   ou NOT_RUN nunca gera SUCCESS; auth/config/policy/decoder falham neutros.
2. Teste manual com qualquer sequência retorna estágios sanitizados e audita,
   sem alterar snapshot automático, estado, streak ou incidente.
3. Completion com generation/owner obsoleto não sobrescreve snapshot; log,
   resposta e DB não guardam frame, SDP, URI completa ou segredo.

# ARGOS E3 RTSP — handoff Casa → Trabalho

```text
ACTIVITY_ID = ARGOS-E3-RTSP-CONTRACT-CHECKPOINT-01
CHECKPOINT_DATE = 2026-10-19
CHECKPOINT_STATUS = PREPARED_FOR_COMMIT_AND_REMOTE_VERIFICATION
REPOSITORY = https://github.com/wromanov/projeto_argos.git
TARGET_BRANCH = codex/hom-v1-integration
BASE_COMMIT_SHA = fe3c54f721257a7dd8dc9e5f45ce05f8cde7525f
PUBLICATION_COMMIT = THIS_CHECKPOINT_COMMIT / full SHA recorded in activity closure report
PUBLICATION_METHOD = normal push; no force push
WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos_e3_p0_reconciliation
WORKTREE_STATE_AT_CREATION = detached HEAD at BASE_COMMIT_SHA; isolated publication worktree
ORIGINAL_WIP = PRESERVED_PER_P0_AUDIT / NOT_REINSPECTED_IN_THIS_ACTIVITY
ORIGINAL_WORKTREE_MUTATION = NONE
```

## Aprovação e publicação

```text
USER_AMENDMENT_APPROVAL = APPROVED / C01-C06
PREFLIGHT_ADJUDICATION = CONTINUE_DOCUMENTATION_ONLY
CONTRACT_PROMOTION = LOCAL / DOCUMENTATION_ONLY
CANONICAL_CONTRACTS_PUBLISHED = YES once origin SHA matches PUBLICATION_COMMIT
P0_RECONCILIATION = COMPLETE / PUBLISHED
ROUND_1_AUTHORIZATION = NOT_GRANTED
NEXT_ACTIVITY = ARGOS-E3-RTSP-ROUND-1-P1 / PLANNED / NOT_AUTHORIZED
```

A aprovação formal do usuário cobre os amendments C01–C06. `CONTINUE_DOCUMENTATION_ONLY` foi a adjudicação operacional de preflight e não deve ser atribuída ao usuário. O commit e o push normal deste checkpoint estão autorizados. A publicação só estará concluída após confirmar que `origin/codex/hom-v1-integration` aponta para o SHA completo do commit desta publicação.

O histórico anterior foi preservado; não houve force push. O trabalho de publicação foi feito no worktree isolado em detached HEAD, sem mover a branch local associada a outro worktree. O WIP doméstico em seu worktree original foi preservado conforme a auditoria da P0; este checkpoint não afirma nova inspeção desse conteúdo.

## Contratos promovidos

Amendments C01–C06 aprovados formalmente e preparados nos contratos canônicos IMG-CAP/BC-02 e CAM-INT-03. O estado técnico da promoção está em `ARGOS_E3_RTSP_PRIMARY_RECOVERY_AMENDMENTS.md`, `IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` e `CAM-INT-03_RTSP_CONNECTION_CONTRACT.md`.

- C01: `RTSP_FRAME` é o método primário quando elegível e configurado; HTTP Snapshot continua independente e explicitamente selecionável; fallback silencioso é proibido.
- C02: diagnósticos RTSP A/B/C/D permanecem; extração de frame/JPEG usa API complementar, distinta do resultado booleano de diagnóstico.
- C03: preservar `CameraImageRecord`, proveniência, storage privado, auditoria e consumidores E4 existentes.
- C04: decisão de modelagem técnica permanece pendente para P2; não antecipar cardinalidade, schema, API ou migration.
- C05: preservar credenciais protegidas e Target Policy. RTSP convencional usa esquema `rtsp`, porta default 554; RTSPS e certificado HTTPS não são requisitos.
- C06: preservar F02/F03 com seus IDs, escopos e estados atuais.
- P1 ainda não está autorizada.

Direção RTSP registrada:

```text
PRIMARY_CAPTURE_METHOD = RTSP_FRAME
SECONDARY_CAPTURE_METHOD = HTTP_SNAPSHOT
DEFAULT_RTSP_PORT = 554
RTSP_SCHEME = rtsp
SILENT_FALLBACK = PROHIBITED
RTSPS_REQUIRED = NO
HTTPS_CERTIFICATE_REQUIRED_FOR_RTSP = NO
```

Objetivo funcional: `RTSP → FRAME → JPEG → STORAGE → CAMERA_IMAGE_RECORD → GALERIA E4`.

## Estado da homologação — reportado anteriormente, não revalidado

- A VM HML permanece no release `d44e4e6f`, conforme estado previamente reportado.
- Migrations E3 0020/0021 foram reportadas como aplicadas.
- A aplicação web foi reportada como operacional.
- Worker contínuo de captura não está habilitado.
- Captura RTSP real ainda não foi homologada.
- Galeria E4 com imagem real ainda não foi homologada.
- Hikvision RF0420 permanece como equipamento de teste operacional previsto.
- Esta atividade não acessou VM, câmera ou credenciais e não revalidou esses itens.

Não registrar nem transportar credenciais, chaves ou segredos.

## Retomada na estação de trabalho

Ambiente de trabalho esperado: `C:\Users\walacedelgado\PycharmProjects\projeto_argos`.

No início da retomada:

1. Confirmar repositório, branch, HEAD e status local.
2. Executar fetch do remoto e confirmar o commit publicado neste checkpoint.
3. Preservar o WIP existente na estação de trabalho.
4. Não executar pull/merge indiscriminadamente sobre worktree com alterações; reconciliar o checkout de forma segura.
5. Revisar este checkpoint e os contratos promovidos.
6. Solicitar autorização explícita antes de começar P1.

Não transportar `.env`, bancos, credenciais, arquivos `.local`, chaves ou ambientes virtuais entre estações.

## Próxima atividade planejada

`ARGOS-E3-RTSP-ROUND-1-P1` — `PLANNED / NOT_AUTHORIZED`.

A P1 será dedicada à extração de frame RTSP, decodificação H.264/H.265 e entrega JPEG, começando com testes sintéticos e fluxos codificados offline. Não inclui captura real nem integração com a VM sem autorizações posteriores.

## Escopo e evidência deste checkpoint

P0 de reconciliação concluída e publicada antes desta atividade. Esta publicação trata apenas dos documentos contratuais e de continuidade autorizados; nenhuma alteração de código, migration ou VM foi feita. A verificação final deve confirmar os documentos staged, `git diff --cached --check`, ancestralidade do commit, ausência de arquivos funcionais e igualdade do SHA remoto com o commit publicado. O checkpoint não declara a publicação remota concluída antes dessa confirmação.

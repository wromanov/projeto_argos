# ARGOS E3 RTSP — checkpoint de transferência Trabalho → Casa

ACTIVITY_ID = ARGOS-E3-RTSP-HANDOFF-01
STATUS = HISTORICAL / SUPERSEDED_BY ARGOS-E3-RTSP-CONTRACT-PROMOTION-01
AMENDMENTS_C01_C06 = APPROVED / CANONICALLY_PROMOTED LOCALLY
NEXT_GATE = CANONICAL_PUBLICATION_REVIEW
REPOSITORY = https://github.com/wromanov/projeto_argos.git
BRANCH = codex/hom-v1-integration
DOCUMENTATION_CHECKPOINT = df582ade547358953cb1dee8113850ee5e186cb9
HML_RELEASE = d44e4e6f5556cef8b9db00637c40fbd08259f2f3 (reportado; distinto do checkpoint documental)

O conteúdo abaixo preserva o handoff antes da adjudicação e deve ser lido como
registro histórico. Os estados de revisão/aprovação de amendments foram
supersedidos por `PROJECT_STATE.md` §169, Roadmap §28 e Sprints §25; não usar
suas instruções de retomada como gate atual.

## Estado confirmado/reportado

Release HML informado: `d44e4e6f`. O aplicativo web está operacional; PostgreSQL e migrations E3 foram aplicadas; smoke de login, dashboard, inventário, navegação e arquivos estáticos foi aprovado. Backup e rollback permanecem na VM. O worker de captura não está habilitado continuamente. Não houve homologação de captura real nem da galeria E4 com imagem real nesta atividade.

Câmera: Hikvision RF0420, modelo DS-2CD2143G2-IS, IP `10.143.108.79`, Camera ID `4`. A configuração de conexão HML está ausente e o perfil operacional RTSP Frame não foi provisionado. Credenciais protegidas e Target Policy aguardam preparação. A permissão QA `capture_camera_image` foi confirmada. Este checkpoint não contém credenciais.

## Decisão e documentação

```text
PRIMARY_CAPTURE_METHOD = RTSP_FRAME
RTSP_SCHEME = rtsp
DEFAULT_RTSP_PORT = 554
HTTP_SNAPSHOT = SECONDARY / INDEPENDENT
SILENT_FALLBACK = PROHIBITED
RTSPS_REQUIRED = NO
HTTPS_CERTIFICATE_REQUIRED_FOR_RTSP = NO
FLOW = RTSP → FRAME → JPEG → STORAGE → DATABASE → GALERIA E4
```

Documentos principais: `ARGOS_E3_RTSP_PRIMARY_RECOVERY_PLAN.md`, `ARGOS_E3_RTSP_ROUND_1_PLAN.md` e `ARGOS_E3_RTSP_PRIMARY_RECOVERY_AMENDMENTS.md`. A atividade documental original é `ARGOS-E3-RTSP-DOC-01`; a reconciliação P0 corrente é `ARGOS-E3-HOME-RECONCILIATION-01`; a atividade futura de implementação P1 será `ARGOS-E3-RTSP-ROUND-1-P1`. Revisão humana pendente. Amendments propostos não foram aprovados nem promovidos a contratos canônicos.

F02 — recuperação de jobs órfãos — e F03 — decisão dos códigos de erro — continuam pendentes. Também aguardam execução: diagnóstico/runtime GStreamer; extração e integração de RTSP Frame ao worker; configuração técnica/perfis; Target Policy e credenciais; fluxo administrativo; homologação com a Hikvision; validação real da galeria E4.

## Recuperação no checkout doméstico

Checkout com WIP doméstico: C:\Users\walac\desenvolvimento\projeto_argos_hom_integration (preservar sem alterações). Worktree isolado P0: C:\Users\walac\desenvolvimento\projeto_argos_e3_p0_reconciliation, derivado de df582ade547358953cb1dee8113850ee5e186cb9.

1. Antes de atualizar, confirmar raiz, branch, `git status --short`, `git status --branch` e HEAD local. Preservar/reconciliar WIP encontrado; não presumir árvore limpa.
2. Conferir o remoto `origin` e atualizar referências. Localizar o commit publicado do checkpoint no topo de `origin/codex/hom-v1-integration` e avançar somente após confirmar a relação de ancestralidade e preservar mudanças locais.
3. Ler PROJECT_STATE.md §168, AGENT_CONTINUITY.md §20.125, ACTIVE_DOCUMENT_MAP.md §128, este checkpoint e os documentos de plano, amendments e relatório de reconciliação.
4. Realizar revisão humana do pacote e dos amendments. Só então decidir explicitamente se autoriza `ARGOS-E3-RTSP-ROUND-1-P1`.
5. Até essa adjudicação: não iniciar implementação da P1, não alterar VM e não habilitar worker recorrente.

P0_DOCUMENTATION = READY_FOR_FINAL_ACCEPTANCE
ACTIVITY_COMPLETE = YES / technical documentation complete; human acceptance and publication decision pending
HUMAN_CONTENT_REVIEW = PENDING
AMENDMENTS_APPROVED = NO
ROUND_1_AUTHORIZED = NO
ROUND_1_IMPLEMENTATION = NOT_STARTED

## Baseline reconciliada

Em df582ade, CameraCaptureJob, migrations 0020/0021, capture_service.py e run_capture_worker existem. Serviço/worker atual executa HTTP Snapshot; RTSP continua no adapter diagnóstico, com A/B/C/D e retorno booleano, sem bytes/JPEG. Não confundir presença no repositório, estado HML reportado (d44e4e6f), validação e aceite. Captura RTSP real e galeria E4 com imagem real continuam pendentes. Amendments são propostas não canônicas; P1 não autorizada nem iniciada.

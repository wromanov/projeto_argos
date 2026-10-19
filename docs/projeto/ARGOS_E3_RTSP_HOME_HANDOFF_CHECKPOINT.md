# ARGOS E3 RTSP — checkpoint de transferência Trabalho → Casa

ACTIVITY_ID = ARGOS-E3-RTSP-HANDOFF-01
STATUS = DOCUMENTATION_PREPARED / HUMAN_CONTENT_REVIEW_PENDING
REPOSITORY = https://github.com/wromanov/projeto_argos.git
BRANCH = codex/hom-v1-integration
REMOTE_BASE_SHA = d44e4e6f5556cef8b9db00637c40fbd08259f2f3
RECOVERY_COMMIT = topo publicado de origin/codex/hom-v1-integration após este checkpoint

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

Documentos principais: `ARGOS_E3_RTSP_PRIMARY_RECOVERY_PLAN.md`, `ARGOS_E3_RTSP_ROUND_1_PLAN.md` e `ARGOS_E3_RTSP_PRIMARY_RECOVERY_AMENDMENTS.md`. A rodada documental `ARGOS-E3-RTSP-DOC-01` foi preparada; revisão humana pendente. Amendments propostos não foram aprovados nem promovidos a contratos canônicos.

F02 — recuperação de jobs órfãos — e F03 — decisão dos códigos de erro — continuam pendentes. Também aguardam execução: diagnóstico/runtime GStreamer; extração e integração de RTSP Frame ao worker; configuração técnica/perfis; Target Policy e credenciais; fluxo administrativo; homologação com a Hikvision; validação real da galeria E4.

## Recuperação no checkout doméstico

Destino: `C:\Users\walac\desenvolvimento\projeto_argos`.

1. Antes de atualizar, confirmar raiz, branch, `git status --short`, `git status --branch` e HEAD local. Preservar/reconciliar WIP encontrado; não presumir árvore limpa.
2. Conferir o remoto `origin` e atualizar referências. Localizar o commit publicado do checkpoint no topo de `origin/codex/hom-v1-integration` e avançar somente após confirmar a relação de ancestralidade e preservar mudanças locais.
3. Ler `PROJECT_STATE.md` §166, `AGENT_CONTINUITY.md` §20.123, `ACTIVE_DOCUMENT_MAP.md` §126, este checkpoint e os três documentos E3 referenciados acima.
4. Realizar revisão humana do pacote e dos amendments. Só então decidir explicitamente se autoriza `ARGOS-E3-RTSP-ROUND-1-P1`.
5. Até essa adjudicação: não iniciar implementação da P1, não alterar VM e não habilitar worker recorrente.

ACTIVITY_COMPLETE = CHECKPOINT_PUBLICATION_AND_REMOTE_VERIFICATION_REQUIRED
HUMAN_CONTENT_REVIEW = PENDING
AMENDMENTS_APPROVED = NO
ROUND_1_AUTHORIZED = NO

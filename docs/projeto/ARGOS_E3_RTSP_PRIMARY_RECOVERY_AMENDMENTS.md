# ARGOS E3 RTSP — amendments e supersession C01–C06

STATUS = APPROVED / CANONICALLY_PROMOTED LOCALLY; REMOTE_PUSH_PENDING
ACTIVITY_ID = ARGOS-E3-RTSP-CONTRACT-PROMOTION-01
SOURCE_ACTIVITY_ID = ARGOS-E3-RTSP-DOC-01
RECONCILIATION_ACTIVITY_ID = ARGOS-E3-HOME-RECONCILIATION-01
FOLLOW_ON_ACTIVITY_ID = ARGOS-E3-RTSP-ROUND-1-P1
USER_AMENDMENT_APPROVAL = APPROVED / C01-C06
PREFLIGHT_ADJUDICATION = CONTINUE_DOCUMENTATION_ONLY
CANONICAL_PROMOTION = LOCAL / DOCUMENTATION_ONLY
REMOTE_PUBLICATION = PENDING
ROUND_1_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED

A aprovação explícita do usuário é `USER_AMENDMENT_APPROVAL = APPROVED / C01-C06`.
A decisão operacional de preflight `PREFLIGHT_ADJUDICATION = CONTINUE_DOCUMENTATION_ONLY`
foi uma instrução de execução, não uma decisão do usuário. As cláusulas indicadas
na matriz abaixo estão promovidas localmente e passam a ser canônicas no escopo
de cada amendment; a publicação remota depende do commit e push normal desta
atividade. Esta promoção não autoriza implementação P1, alteração de código/schema,
câmera real ou VM.

## Matriz reconciliada: contrato atual → decisão → proposta → consequência

| ID | Contrato/estado atual | Decisão registrada | Amendment aprovado / disposição | Consequência técnica |
|---|---|---|---|---|
| C01 — Seleção | IMG-CAP/BC-02 priorizava HTTP Snapshot sem preferência | Aprovado: RTSP_FRAME primário; HTTP secundário independente; sem fallback silencioso | Sem preferência, selecionar RTSP apenas quando elegível/configurado. Se indisponível, retornar resultado explícito; seleção HTTP é independente e explícita. | Promovido em IMG-CAP/BC-02; método/origem no job/auditoria; sem captura secundária automática. |
| C02 — Adapter | CAM-INT-03 define diagnóstico A/B/C/D; receive_one_frame retorna booleano | Aprovado: preservar A/B/C/D e especificar API complementar de frame/JPEG | DTO/port bounded para bytes de frame e metadados seguros; decodificar e codificar JPEG; API distinta do diagnóstico. Não sobrecarregar booleano sem inventariar consumidores. | Promovido em CAM-INT-03; diagnóstico e callers compatíveis; extração explícita e sanitizada. |
| C03 — Domínio de imagens | IMG-CAP integra ao domínio existente; galeria E4 publicada | Aprovado: preservar CameraImageRecord, proveniência, storage privado, auditoria, Quick Detail e galeria | Convergir RTSP e HTTP no pipeline existente. Sem tabela/domínio paralelo e sem reescrever histórico/aceites. | Promovido em IMG-CAP; E4 mantém regras aprovadas. |
| C04 — Configuração | CameraConnectionConfig/perfis atuais não representam integração de captura RTSP operacional | Aprovado manter decisão de modelagem pendente na P2 | Pendente decidir configuração independente dos métodos ou campos/entidade/API distintos. Não inferir que compartilhar endpoint/perfil satisfaça ambos. Decidir antes de schema/API; nenhuma migration nesta rodada. | P2 pendente; RTSP_DISCOVERY_V1 e diagnóstico não são perfil operacional de captura; elegibilidade requer configuração explícita por método. |
| C05 — Segurança | Credenciais cifradas e Target Policy são requisitos; TLS pode ser generalizado indevidamente | Aprovado: preservar segredo protegido e Target Policy; RTSP convencional não requer HTTPS/RTSPS | Credencial fora da URI e logs; validar destino antes de rede; `rtsp://`, default 554; `RTSPS_REQUIRED=NO`; HTTPS não é pré-requisito. | Promovido em CAM-INT-03; controles de segredo/destino preservados, protocolos distintos. |
| C06 — F02/F03 | F02/F03 têm IDs/escopos/estados próprios e não estão adjudicadas | Aprovado preservar IDs, escopos e estados atuais | Não redefinir recuperação/idempotência (F02) nem catálogo/semântica de erro/cancelamento (F03). Worker recorrente permanece gated. | Promovido como preservação explícita; nenhum item fechado/reaberto; P1 segue não autorizada. |

## Precisão sobre a baseline

No HEAD df582ade, CameraCaptureJob e migrations 0020/0021 existem. capture_service.py e run_capture_worker também existem, mas o fluxo aceita apenas HTTP Snapshot; RTSP não está integrado à execução/persistência do job. O GStreamer implementa diagnóstico A/B/C/D e recebimento booleano, sem bytes/JPEG. O amendment descreve essa lacuna sem alegar que os componentes-base estão ausentes.

## Condições e estados

    PRIMARY_CAPTURE_METHOD = RTSP_FRAME / CANONICAL
    SECONDARY_CAPTURE_METHOD = HTTP_SNAPSHOT / INDEPENDENT
    RTSP_SCHEME = rtsp
    DEFAULT_RTSP_PORT = 554
    RTSPS_REQUIRED = NO
    SILENT_FALLBACK = PROHIBITED
    F02 = PRESERVE_CURRENT_ID_SCOPE_AND_STATUS
    F03 = PRESERVE_CURRENT_ID_SCOPE_AND_STATUS
    CANONICAL_CONTRACT_SUPERSESSION = LOCAL / C01-C06
    REMOTE_PUBLICATION = PENDING
    ROUND_1_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED

A promoção documental local C01–C06 está concluída nos contratos indicados nesta matriz. A publicação remota permanece pendente do commit e push normal autorizados nesta atividade. P1, alterações funcionais/schema, homologação, VM e câmera real continuam fora da autorização.

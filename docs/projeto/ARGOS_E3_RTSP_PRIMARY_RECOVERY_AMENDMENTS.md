# ARGOS E3 RTSP — propostas de amendment/supersession

STATUS = PROPOSED / HUMAN_ACCEPTANCE_PENDING
ACTIVITY_ID = ARGOS-E3-RTSP-DOC-01
RECONCILIATION_ACTIVITY_ID = ARGOS-E3-HOME-RECONCILIATION-01
FOLLOW_ON_ACTIVITY_ID = ARGOS-E3-RTSP-ROUND-1-P1
CANONICAL_PROMOTION = NOT_AUTHORIZED

A direção registrada para a proposta é RTSP_FRAME primário; HTTP_SNAPSHOT secundário independente; esquema RTSP convencional rtsp://, porta default 554, RTSPS não obrigatório e fallback silencioso proibido. Os contratos atuais continuam canônicos até aceite humano explícito.

## Matriz reconciliada: contrato atual → decisão → proposta → consequência

| ID | Contrato/estado atual | Decisão registrada | Amendment candidato | Consequência técnica |
|---|---|---|---|---|
| C01 — Seleção | IMG-CAP/BC-02 prioriza HTTP Snapshot sem preferência | RTSP_FRAME primário; HTTP secundário independente; sem fallback silencioso | Sem preferência, selecionar RTSP apenas quando elegível/configurado. Se indisponível, retornar resultado explícito; seleção HTTP é independente e explícita. | Método/origem ficam registrados no job/auditoria; não há captura secundária automática. |
| C02 — Adapter | CAM-INT-03 define diagnóstico A/B/C/D; receive_one_frame retorna booleano | Preservar A/B/C/D como diagnóstico; captura precisa entregar imagem validável | Definir DTO/port bounded para bytes de frame e metadados seguros; decodificar e codificar JPEG; API de captura distinta do resultado diagnóstico. Não sobrecarregar o booleano existente sem inventariar consumidores. | Probe não é captura; consumidores diagnósticos permanecem compatíveis; erro de extração é explícito e sanitizado. |
| C03 — Domínio de imagens | IMG-CAP integra ao domínio existente; galeria E4 publicada | Preservar CameraImageRecord, proveniência, storage privado, seleção, Quick Detail e galeria | Convergir RTSP e HTTP no pipeline existente de validação, persistência privada, auditoria e registro. Sem tabela/domínio paralelo e sem reescrever histórico/aceites. | Uma imagem validada alimenta os serviços E4 existentes, sem alterar suas regras aprovadas. |
| C04 — Configuração | CameraConnectionConfig/perfis atuais não representam integração de captura RTSP operacional | Perfil deve declarar capability/evidência e configuração validadas | Pendente decidir se `CameraConnectionConfig` comporta RTSP e HTTP Snapshot configurados independentemente, ou se requer campos/entidade/API distintos. Não inferir que compartilhar endpoint/perfil satisfaça os dois métodos. Registrar a decisão em atividade própria antes de schema/API; nenhuma migration nesta rodada. | RTSP_DISCOVERY_V1 e diagnóstico não são tratados como perfil de captura operacional; cada método só pode ser elegível pela sua configuração explícita. |
| C05 — Segurança | Credenciais cifradas e Target Policy são requisitos; TLS pode ser generalizado indevidamente | Preservar segredo cifrado/efêmero e Target Policy; RTSP convencional não requer HTTPS/RTSPS | Manter credencial fora da URI e logs; validar destino antes de rede; rtsp:// e porta default 554; RTSPS_REQUIRED=NO; HTTPS não é pré-requisito. | Controles de destino e segredo permanecem, sem confundir protocolos. |
| C06 — F02/F03 | F02/F03 têm IDs/escopos/estados próprios e não estão adjudicadas | Preservar IDs, escopos e estados atuais | Não redefinir recuperação de jobs órfãos/idempotência (F02) nem catálogo/semântica de erros e cancelamento (F03). Worker recorrente permanece gated. | Nenhuma pendência é fechada ou reaberta por este amendment; P1 limita-se a extração sintética. |

## Precisão sobre a baseline

No HEAD df582ade, CameraCaptureJob e migrations 0020/0021 existem. capture_service.py e run_capture_worker também existem, mas o fluxo aceita apenas HTTP Snapshot; RTSP não está integrado à execução/persistência do job. O GStreamer implementa diagnóstico A/B/C/D e recebimento booleano, sem bytes/JPEG. O amendment descreve essa lacuna sem alegar que os componentes-base estão ausentes.

## Condições e estados

    PRIMARY_CAPTURE_METHOD = RTSP_FRAME / PROPOSED_CANONICAL_AMENDMENT
    SECONDARY_CAPTURE_METHOD = HTTP_SNAPSHOT / INDEPENDENT
    RTSP_SCHEME = rtsp
    DEFAULT_RTSP_PORT = 554
    RTSPS_REQUIRED = NO
    SILENT_FALLBACK = PROHIBITED
    F02 = PRESERVE_CURRENT_ID_SCOPE_AND_STATUS
    F03 = PRESERVE_CURRENT_ID_SCOPE_AND_STATUS
    CANONICAL_CONTRACT_SUPERSESSION = PENDING_HUMAN_ACCEPTANCE
    ROUND_1_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED

A publicação deste documento não altera contratos canônicos. Promoção somente após revisão e aceite humano explícito.

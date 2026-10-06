# DSCR-UIV2-003 — Evolução de patterns compartilhados para 2.1.0

ID = DSCR-UIV2-003-SHARED-PATTERNS-2.1.0
STATUS = APPROVED / USER_DECISION_RECORDED
APPROVAL = USER_APPROVED / 2026-10-05
ACTIVITY = P5-VR-DSCR-01 — Design System 2.1.0 Change Request / Versioning Canonicalization
SOURCE_ASSESSMENT = P5-VR-S1A — Shared Pattern / Design System Gap Assessment; findings also summarized in PROJECT_STATE.md section 44

## Pedido de mudança

```text
CHANGE = Data Pair primitive; Data Group extension; Compact Empty State variant; Button Danger variant
REASON = corrigir gaps compartilhados identificados pela P5-VR-S1A sem recorrer a workarounds page-local
AFFECTED_COMPONENTS = Button; Empty State; novos Data Pair e Data Group primitives/composition
AFFECTED_SCREENS = SCR-CAM-DETAIL-001 (consumer previsto); SCR-DASH-001 (consumer previsto); SCR-CAM-QUICK-001 (label/value pattern considered, existing functional semantics protected)
VERSION_IMPACT = MINOR
CURRENT_VERSION = 2.0.2
TARGET_VERSION = 2.1.0
COMPATIBILITY = BACKWARD_COMPATIBLE / ADDITIVE
BACKWARD_COMPATIBILITY = PRESERVED
USER_REAPPROVAL_REQUIRED = SATISFIED / USER_APPROVED (2026-10-05)
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_DOCUMENT
STAT_GROUP = DEFERRED / OUTSIDE_THIS_DSCR
```

Os consumidores acima são os previstos para avaliação/adoção, não uma autorização
de implementação nem uma declaração de que as telas já usam os novos contracts.
Quick Detail permanece funcionalmente protegido; o primitive não altera sua
semântica.

### Mudanças aprovadas no assessment e registradas neste DSCR

A proposta de versão foi aprovada pelo usuário em 2026-10-05. A implementação
continua sem autorização; a aprovação deste DSCR satisfaz a reaprovação da
mudança, mas não autoriza iniciar P5-VR-S1B.

1. **Data Pair primitive** — primitive semântico compartilhado para associação
   label/value; deve garantir associação estável, reset consistente de margens,
   conteúdo longo, alinhamento de valor vazio, uso de tokens existentes e
   responsividade coerente.
2. **Data Group extension** — composição de Data Pairs, reutilizando primitives
   existentes sempre que possível; heading opcional quando aplicável; agrupamento
   e quebra responsiva; sem impor card, border, background ou shadow. A página/
   domínio controla seleção e ordem dos campos.
3. **Compact Empty State variant** — variante do Empty State para texto curto e
   ação opcional dentro de seções, sem superfície própria ou altura mínima
   artificial, reutilizando tokens existentes.
4. **Button Danger variant** — variante destrutiva do Button V2 com estados
   default, hover, focus e disabled quando aplicável. Não criar níveis ou
   variantes sem consumidor demonstrado.

### Reuso e itens diferidos

```text
REUSE_EXISTING = Page Header; Section Heading; Status / Badge
REUSE_RATIONALE = os patterns já existem no DS; os problemas registrados são principalmente de Page Composition / adoção
NEW_EQUIVALENTS = PROHIBITED_BY_THIS_DSCR
STAT_GROUP_STATUS = DEFERRED
STAT_GROUP_RATIONALE = a necessidade concreta no Dashboard não demonstra reutilização suficiente em outras superfícies
STAT_GROUP_DS_CONTRACT = NONE
STAT_GROUP_API_OR_CLASSES = NONE_RESERVED
STAT_GROUP_DURING_P5-VR-S3 = use existing primitives/tokens; reavaliar promoção se houver reutilização real em outras superfícies
```

### Regra pós-freeze

```text
DESIGN_SYSTEM_STATE = PINNED / READ_ONLY
MATERIAL_DS_GAP -> DS_CHANGE_REQUEST
DS_CHANGE_REQUEST -> ADJUDICATION
UNADJUDICATED_DS_CHANGE -> IMPLEMENTATION_PROHIBITED
BLOCKED_BY_DS_CHANGE -> NO_LOCAL_WORKAROUND
CSS_EDIT_CAPABILITY -> DOES_NOT_TRANSFER_AUTHORITY
```

Este DSCR registra a aprovação humana da proposta. A aprovação não promove 2.1.0
a versão implementada/ativa, não altera o estado pinned/read-only e não autoriza
implementação, workaround local, mudança de tela ou alteração de CSS.

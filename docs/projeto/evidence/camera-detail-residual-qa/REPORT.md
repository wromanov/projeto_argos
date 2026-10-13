# HOM-01 Camera Detail — revisão residual de evidências

```text
PROJECT = projeto_argos
ACTIVITY = HOM-01-CAMERA-DETAIL-RESIDUAL-QA-CLOSURE
MODE = DIRECT
SCOPE = EVIDENCE_REVIEW_ONLY
REVIEW_DATE = 2026-10-13
ACTIVITY_STATUS = CLOSED_WITH_LIMITATIONS
ACTIVITY_COMPLETION_PERCENT = 100%
USER_DECISION = APPROVED
RESIDUAL_QA_DISPOSITION = ACCEPTED_WITH_LIMITATIONS
CAMERA_DETAIL_PRIOR_APPROVAL = PRESERVED
RESIDUAL_QA_STATUS = CLOSED_WITH_LIMITATIONS
HUMAN_LIMITATION_ACCEPTANCE = APPROVED
PROJECT_STATE_UPDATE = PASS / closure with accepted limitations recorded
GIT_DIFF_CHECK = PASS
ACTIVITY_COMPLETE = YES / bounded residual QA closure with limitations
WORKSPACE = .
BRANCH = codex/hom-v1-integration
HEAD_AT_REVIEW = e91e4499d43211722b7eadba9adab842e3c75aeb
SOURCE_CODE_CHANGE = NO
NEW_BRANCH = NO
MERGE_TO_MASTER = NO
HUMAN_APPROVAL = APPROVED / accepted the residual QA limitations
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
```

## Inventário da evidência

A pasta esperada não existia no início da revisão. A listagem integral de
`docs/projeto/evidence/` encontrou evidências de Dashboard V7 e sidebar, mas
nenhuma pasta ou captura de Camera Detail. Nenhuma imagem desta atividade foi
aberta, alterada ou criada. Não houve nova tentativa de automação do navegador.

| Viewport CSS solicitado | Captura manual Camera Detail | Resultado |
|---|---|---|
| 1920×1080 | ausente | `NOT_VERIFIED` |
| 1440×900 | ausente | `NOT_VERIFIED` |
| 1366×768 | ausente | `NOT_VERIFIED` |
| 390×844 | ausente | `NOT_VERIFIED` |

DPR e zoom efetivos não estão documentados para capturas de Camera Detail nesta
pasta. Não foram inferidos de outras páginas ou atividades.

## Matriz residual

| Critério | Resultado desta revisão | Evidência/limite |
|---|---|---|
| Cabeçalho e badges | `NOT_VERIFIED` | sem captura de Camera Detail |
| Monitoramento técnico | `NOT_VERIFIED` | sem captura de Camera Detail |
| “Fora do escopo” somente no campo Escopo | `NOT_VERIFIED` | decisão aprovada permanece registrada em `PROJECT_STATE.md` §92; a presença/uniquidade atual não pode ser confirmada sem captura |
| Diagnóstico A–D | `NOT_VERIFIED` | aprovação anterior de rótulos e comportamento UNKNOWN permanece no escopo documentado em `PROJECT_STATE.md` §99; a apresentação residual não foi reavaliada |
| Imagens e operações complementares | `NOT_VERIFIED` | sem captura de Camera Detail |
| Histórico | `NOT_VERIFIED` | sem captura de Camera Detail |
| Responsividade nos quatro viewports | `NOT_VERIFIED` | nenhum viewport da Camera Detail tem captura nesta pasta |
| Teclado e foco | `NOT_VERIFIED` | sem registro manual de navegação/foco da Camera Detail |
| Permissões QA | `PASS / evidência histórica limitada` | `PROJECT_STATE.md` §94 registra 5 permissões explícitas do perfil visual, 7 do operacional e testes de renderização condicionada. Isso não demonstra a apresentação atual em capturas manuais. |
| Botão “Enviar imagem” | aceite anterior preservado; residual `NOT_VERIFIED` | aceito anteriormente apenas quanto à apresentação; a submissão continua não comprovada (`PROJECT_STATE.md` §95–96) |

## Findings

```text
P1_FINDINGS = NONE_PROVEN
P2_FINDINGS = NONE_PROVEN
P3_FINDINGS = NONE_PROVEN
NOT_VERIFIED = all four Camera Detail viewports; current residual visual criteria; keyboard/focus; current rendered permission-conditioned actions
DESIGN_QA_GLOBAL = NOT_DECLARED_PASS
```

A ausência das capturas é uma limitação de evidência aceita explicitamente pelo
usuário, não uma regressão do produto. Nenhuma regressão material foi
comprovada. Permanecem `NOT_VERIFIED` a matriz atual nos quatro viewports,
teclado/foco, renderização atual por perfil e comparação visual integral com
P5. Não se exige comparação pixel a pixel com a referência P5 histórica
indisponível. Os aceites anteriores da composição Camera Detail e do
Diagnóstico A–D são preservados, sem reabertura.

## Continuidade

O estado final foi registrado em `PROJECT_STATE.md` §109,
`AGENT_CONTINUITY.md` §20.69 e `ACTIVE_DOCUMENT_MAP.md` §73. O usuário aceitou
explicitamente as limitações e encerrou esta auditoria residual. HOM-01 segue
`IN_PROGRESS`, HOM-02 permanece bloqueada e nenhum status global de DESIGN QA
foi aprovado. O WIP preexistente foi preservado.

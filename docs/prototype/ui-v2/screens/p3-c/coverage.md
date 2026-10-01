# P3-C — cobertura e readiness técnico

Data: 2026-09-28
Base imutável: `9943e20d9b1e04159e067c72aa4dd70eab2bdb36`
Branch/worktree: `codex/ui-v2-p3-c-governance-audit`
Design System: 2.0.0 na autoria original; propagação e revalidação visual/regressiva concluídas sobre 2.0.1.

## Ownership e paths canônicos

Matriz P3-0 conferida em `P3_PROTOTYPE_HARNESS.md` e `SCREEN_COVERAGE.md`. Ownership validado, sem drift ou conflito. A matriz atribui os três `SCR-SUB-*` ao P3-B; nenhum foi implementado aqui.

| Grupo | SCREEN_ID | PROTOTYPE_PATH canônico | Resultado local |
|---|---|---|---|
| C1 Activities | `SCR-ACT-LIST-001` | `docs/prototype/ui-v2/screens/p3-c/scr-act-list-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C1 Activities | `SCR-ACT-CREATE-001` | `docs/prototype/ui-v2/screens/p3-c/scr-act-create-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C1 Activities | `SCR-ACT-EDIT-001` | `INHERITED` — sem página nova; modo prefilled de `scr-act-create-001.html?mode=edit` | `INHERITED / TECHNICALLY_VALIDATED` |
| C2 Governance | `SCR-GOV-STATE-001` | `docs/prototype/ui-v2/screens/p3-c/scr-gov-state-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C2 Governance | `SCR-GOV-DISABLE-001` | `docs/prototype/ui-v2/screens/p3-c/scr-gov-disable-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C2 Governance | `SCR-GOV-REACTIVATE-001` | `docs/prototype/ui-v2/screens/p3-c/scr-gov-reactivate-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C2 Governance | `SCR-GOV-SUBSTITUTE-001` | `docs/prototype/ui-v2/screens/p3-c/scr-gov-substitute-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C3 Events/Audit | `SCR-EVENT-LIST-001` | `docs/prototype/ui-v2/screens/p3-c/scr-event-list-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C3 Events/Audit | `SCR-EVENT-DETAIL-001` | `docs/prototype/ui-v2/screens/p3-c/scr-event-detail-001.html` | `TECHNICAL_READY_FOR_REVIEW` |
| C3 Events/Audit | `SCR-EVENT-CAMERA-001` | `docs/prototype/ui-v2/screens/p3-c/scr-event-camera-001.html` | `TECHNICAL_READY_FOR_REVIEW` |

As nove composições HTML próprias cobrem os dez IDs canônicos, contando o modo herdado de edição.

## Fixtures e interações

Fixture determinística e fictícia: `docs/prototype/ui-v2/fixtures/p3-c/fixtures.json`. Inclui variação longa para nomes, identificadores, relações, texto de eventos/atividades e datas. Não cria persistência ou pseudo-database. Todas as ações permanecem demonstrativas e não chamam endpoint, API, Django ou serviço.

O formulário de atividade preserva os campos factuais `tipo`, `titulo`, `descricao`, `ocorrida_em` e `responsavel`; a câmera permanece como contexto. Categorias e origens da auditoria seguem as opções factuais atuais. Governança separa situação operacional do estado técnico e preserva histórico na desativação/substituição.

## Cobertura de estados

| SCREEN_ID | Casos capturados além dos quatro defaults |
|---|---|
| `SCR-ACT-LIST-001` | `empty`, `long` |
| `SCR-ACT-CREATE-001` | `focus`, `error`, `success`, `long` |
| `SCR-ACT-EDIT-001` | `selected`, `error`, `success`, `long` |
| Os quatro `SCR-GOV-*` | `focus`, `error`, `success`, `long` |
| `SCR-EVENT-LIST-001` | `selected`, `empty`, `error`, `long` |
| `SCR-EVENT-DETAIL-001` | `long` |
| `SCR-EVENT-CAMERA-001` | `empty`, `long` |

Os estados adicionais são estáticos/determinísticos. `loading` não foi incluído: a cobertura específica P3-C não o exige e estas composições locais não iniciam requisições. O foco foi capturado com eventos de teclado confiáveis do browser para acionar `:focus-visible` compartilhado.

## Responsive e visual QA

Evidência: `docs/prototype/ui-v2/evidence/screenshots/p3-c/`, organizada em `C1-activities`, `C2-governance` e `C3-events-audit`.

- 84 capturas; 40 defaults, 20 casos longos (1440×900 e 390×844 por ID) e 24 estados especiais.
- Defaults de todos os dez SCREEN_IDs em 1920×1080, 1440×900, 1366×768 e 390×844; zoom 100%, DPR 1.
- PNG dimensions iguais ao viewport solicitado em 84/84; falhas do capturador: 0.
- Overflow horizontal global: 0/84. As três tabelas (atividades, auditoria global e auditoria da câmera) preservam colunas em regiões locais roláveis, com `role=region`, nome acessível e `tabindex=0`; paginação permanece disponível.
- Long values quebram linha e permanecem legíveis; inspeção visual incluiu substituição em mobile e telas longas desktop/mobile.
- Os cinco estados `focus` (atividade + quatro ações de governança) têm `:focus-visible` ativo e contorno DS de 3 px/offset 2 px após navegação por teclado.

## Baseline de acessibilidade

Resultado local: `PASS` (baseline; não representa certificação WCAG).

- títulos presentes, um `h1` e um `main` em cada captura; headings e landmarks sem duplicação;
- navegação `nav` nomeada, `aria-current="page"`, skip link e nomes acessíveis para marca/controles;
- tabelas semânticas; regiões de overflow alcançáveis por teclado;
- todos os controles com label; controles inválidos com `aria-describedby`;
- foco visível testado com teclado; alvos móveis e paginação usam o mínimo compartilhado de 44 px;
- suporte a `prefers-reduced-motion` vem do DS compartilhado; P3-C não adiciona movimento.

## Requests e limites de escopo

`DS_CHANGE_REQUESTS = 0` — não há componente visual ausente nem workaround de componente.
ROOT_CHANGE_REQUESTS = 1 (RESOLVED) — ROOT-REQ-P3-C-001 foi resolvido pelo patch root 8121ed38cc15e1ff6e72cb46bbb2ca865100bce0, aplicado como commit ad7926b. O CSS compartilhado 2.0.1 mantém .argos-alert/.argos-state compatíveis com [hidden]; o workaround JavaScript local foi removido.
BLOCKED_BY_DS_CHANGE = NONE — [hidden] foi verificado no navegador sem correção local.

ROOT_OWNED_FILES_CHANGED = YES (authorized root patch 8121ed3) · CROSS_FAMILY_FILES_CHANGED = NO · PRODUCTION_CHANGED = NO · STATIC/CSS/UI-V2_CHANGED = YES (root patch 8121ed3) · PRODUCTION_UI_V2_INTEGRATION_STARTED = NO.

Aprovação visual humana: PENDING. PROJECT_STATE_UPDATE = DEFERRED_NO_AUTHORITY; ACTIVITY_COMPLETE = NO. Este relatório cobre apenas a família P3-C; a consolidação de PROJECT_STATE.md permanece com o root owner.

## Revalidação pós-patch — Design System 2.0.1

- Patch autorizado 8121ed38cc15e1ff6e72cb46bbb2ca865100bce0, cherry-pick ad7926bce2f099230d1d4857723018aceafc329d; branch familiar codex/ui-v2-p3-c-governance-audit.
- ROOT-REQ-P3-C-001 = RESOLVED_BY_DS_2_0_1; o teste confirmou zero elementos [hidden] visíveis e zero dependência de style.display inline.
- POST_DS_DESIGN_QA = PASS; POST_DS_REGRESSION = PASS. O relatório contém 75 medições dos dez SCREEN_IDs: estados default, empty, loading, error, fixtures default e long, e viewports 1440×900 e 390×844. Estados de sucesso da governança e filtros selecionados da auditoria também passaram.
- Zero overflow horizontal, erros de console, requests externos e requests não-GET.
- 84 capturas históricas preservadas sem alteração. Evidência nova: 20 capturas pós-patch (10 IDs em desktop e mobile), três comparativos visuais e post-ds-regression.json em docs/prototype/ui-v2/evidence/screenshots/p3-c/post-ds-2.0.1/.
- Resultado técnico: dez IDs TECHNICAL_READY_FOR_REVIEW; SCR-ACT-EDIT-001 é o modo herdado validado. A aprovação visual humana segue pendente.

## Propagação e regressão direcionada — Design System 2.0.2 (2026-09-29)

`DESIGN_SYSTEM_VERSION = 2.0.2` nos arquivos compartilhados. Patch raiz `8a480a50a338ef3961a242e9dce0ccaf09cdf49b`, propagado como `f8cd8cea0e1f0cbd1ff072aafa341cbcf5c8c732`. O DCR ROOT `DSCR-UIV2-002-MOBILE-TABLE-READABILITY.md` permanece ausente desta família; `DSCR-002 = CONSUMED / REGRESSION PASS`.

Os três consumidores de tabela passaram a regressão focal em 390×844 e 1440×900. No mobile, overflow global = NO, scroll local = FUNCTIONAL e fragmentação destrutiva de palavras/badges = NO; as regiões são nomeadas e alcançáveis por teclado, e os links/ações têm nomes. No desktop, tabelas cabem em 1088px e as linhas medidas permanecem em 64px, sem scroll horizontal ou regressão material de largura/altura. Valores detalhados, incluindo fixture longa e ressalva do viewport Edge, estão no relatório pós-2.0.2.

Spot checks sem overflow global: form Activities, ação Governance e detalhe Event em mobile/desktop. Sem elemento `[hidden]` visível, sem estilo inline de display reintroduzido e sem alteração de persistência.

A validação ROOT do mesmo DCR registra `CROSS_FAMILY_REGRESSION = PASS / 7 of 7`; P3-C não alterou arquivos de P3-A/B/D. Evidência 2.0.2 persistente = DEFERRED_BY_WORKSTATION_CAPABILITY. As 107 capturas/comparativos anteriores seguem preservados. Aprovação visual humana = PENDING.

Finding não funcional: metadados e selos visíveis das nove páginas P3-C ainda anunciam Design System 2.0.1, embora a implementação compartilhada seja 2.0.2. PROJECT_STATE_UPDATE permanece `DEFERRED_NO_AUTHORITY`; ACTIVITY_COMPLETE = NO.

## Aprovação humana e status final da família — 2026-09-30

Este bloco é o status corrente e supersede os registros anteriores de aprovação pendente e de metadata 2.0.1. As linhas originais permanecem para rastreabilidade da QA histórica.

```text
DESIGN_SYSTEM_VERSION = 2.0.2
STALE_DS_2_0_1_CURRENT_METADATA = RESOLVED
STALE_METADATA_STATUS = RESOLVED
P3_C_DS_2_0_2_REGRESSION = PASS
HUMAN_VISUAL_APPROVAL = PASS
USER_VISUAL_APPROVAL = PASS
P3_C_VISUAL_REVIEW = PASS_WITH_NONBLOCKING_LIMITATIONS
P3_C_OWNED_SCREENS = USER_APPROVED / FROZEN
BLOCKING_FINDINGS = NONE
P3_C_SPECIFIC_BLOCKING_FINDINGS = NONE
SURFACE_REFINEMENT_REQUIRED = NO
DESIGN_SYSTEM_CHANGE_REQUIRED = NO
P3_C_COMPLETE = YES
P3_C_STATUS = USER_APPROVED / FROZEN / CLOSED / PUBLISHED
REMAINING_P3_C_GATES = NONE / integrated validation remains the next global gate
PROJECT_STATE_UPDATE = PASS / ROOT integration recorded in PROJECT_STATE.md section 40
```

Os dez IDs pertencem à família e estão tecnicamente prontos: `SCR-ACT-LIST-001`, `SCR-ACT-CREATE-001`, `SCR-ACT-EDIT-001` (modo herdado/prefilled), `SCR-GOV-STATE-001`, `SCR-GOV-DISABLE-001`, `SCR-GOV-REACTIVATE-001`, `SCR-GOV-SUBSTITUTE-001`, `SCR-EVENT-LIST-001`, `SCR-EVENT-DETAIL-001` e `SCR-EVENT-CAMERA-001`.

A aprovação humana foi baseada no pacote atual de seis PNGs DS 2.0.2, com os arquétipos listados em `HUMAN_REVIEW_PACKAGE.md`, e na QA técnica já concluída para a família. Não se afirma uma captura nova para cada tela nesta aprovação.

```text
GLOBAL_HORIZONTAL_OVERFLOW = NONE
MOBILE_TABLE_LOCAL_SCROLL = FUNCTIONAL
DESTRUCTIVE_WORD_FRAGMENTATION = NONE
TABLE_ACTIONS_KEYBOARD_REACHABLE = PASS
MOBILE_DS_BADGE_NOT_IN_FRAME = EXPECTED / NONBLOCKING
MOBILE_FULL_PAGE_COMPOSITION = NOT_REVALIDATED_BY_THIS_SPECIFIC_SCREENSHOT
```

A imagem mobile foi posicionada na tabela e não revalida a composição integral da página; o metadata DS 2.0.2 foi validado antes da captura. Essa limitação não cria blocker. As capturas históricas DS 2.0.1 permanecem inalteradas.

A adjudicação `P3_C_COMPLETE = YES` é local à família. O estado global foi consolidado em `PROJECT_STATE.md`, seção 40; a validação integrada continua pendente.

# P3-C — cobertura e readiness técnico

Data: 2026-09-28
Base imutável: `9943e20d9b1e04159e067c72aa4dd70eab2bdb36`
Branch/worktree: `codex/ui-v2-p3-c-governance-audit`
Design System: `2.0.0` (consumido; sem alterações)

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
`ROOT_CHANGE_REQUESTS = 1 (OPEN)` — `ROOT-REQ-P3-C-001`: estilos compartilhados de `.argos-alert` (`display:flex`) e `.argos-state` (`display:grid`) podem sobrepor o comportamento nativo de `[hidden]`. O JS específico P3-C mantém variantes e feedback ocultos como o harness espera. Solicita-se correção compartilhada para honrar `[hidden]`; nenhum arquivo root/shared/DS foi alterado.
`BLOCKED_BY_DS_CHANGE = NONE` — o comportamento requerido está mitigado no escopo permitido; o request é follow-up compartilhado não bloqueante.

`ROOT_OWNED_FILES_CHANGED = NO` · `CROSS_FAMILY_FILES_CHANGED = NO` · `PRODUCTION_CHANGED = NO` · `STATIC/CSS/UI-V2_CHANGED = NO` · `PRODUCTION_UI_V2_INTEGRATION_STARTED = NO`.

Aprovação visual humana: `PENDING`. Este relatório cobre apenas a família P3-C; consolidação de `PROJECT_STATE.md` permanece com o root owner.
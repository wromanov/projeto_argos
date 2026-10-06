# DSCR-UIV2-006 — Section Surface 2.4.0

```text
ID = DSCR-UIV2-006-SECTION-SURFACE-2.4.0
ACTIVITY = P5-VR-S2A-R3 / DSG-SURFACE-01
STATUS = APPROVED_BY_EXPLICIT_USER_REQUEST / IMPLEMENTED_LOCALLY / NOT_PUBLISHED
CURRENT_VERSION = 2.3.0
TARGET_VERSION = 2.4.0
VERSION_IMPACT = MINOR
COMPATIBILITY = BACKWARD_COMPATIBLE / ADDITIVE
CHANGE = public neutral macro grouping surface
REASON = INSUFFICIENT_MACRO_VISUAL_GROUPING na Camera Detail
AFFECTED_COMPONENTS = new .argos-section-surface / patterns layer
AFFECTED_SCREENS = Camera Detail only
USER_REAPPROVAL_REQUIRED = human Camera Detail visual review / PENDING
IMPLEMENTATION_AUTHORITY = explicit current user request S2A-R3
```

## Contrato público

`.argos-section-surface` define somente `background`, `border`, `border-radius`
e `padding`. Reutiliza `--argos-color-surface`, `--argos-border-width`,
`--argos-color-border`, `--argos-radius-surface` e `--argos-space-6` (24px).
Não define layout, tipografia, estados interativos, sombra, cabeçalho colorido,
accent bar ou gradiente. Nenhum token é criado ou alterado.

A classe é definida uma única vez no layer compartilhado `patterns`.
A adição preserva os consumidores 2.3.0 e não exige migração.
O CSS da página continua responsável apenas pela composição.

## Consumo S2A-R3

Dados principais, Operação, Governança cadastral e Histórico recebem uma surface
por macro região. Histórico possui uma única surface envolvendo seus quatro
subgrupos. Hero, subgrupos, itens de histórico e estados vazios ficam sem surface.
Upload permanece sem surface nesta execução; nenhuma variante compacta é criada.
Controles e badges mantêm suas surfaces intrínsecas existentes.

Rotas, permissões, CSRF, formulários, IDs, atributos de dados, ordenação e limites
dos históricos permanecem preservados. Backend e JS não são alterados.
Quick Detail e P3-B permanecem protegidos. Nenhum breakpoint é adicionado.

## Validação e gates

Validação técnica e estática registrada em `PROJECT_STATE.md`, seção 51.
Aprovação visual humana permanece pendente e não decorre dos testes.
Staging, commit e push não estão autorizados nesta atividade.

# P3-A — Product Design / design QA

```text
PRODUCT_DESIGN_STATUS = AVAILABLE
PRODUCT_DESIGN_SKILLS_LOADED = get-context, design-qa
PRODUCT_DESIGN_GET_CONTEXT = COMPLETE
PRODUCT_DESIGN_DESIGN_QA = BLOCKED_BY_DS_CHANGE
DESIGN_QA_COMPLETE = NO
USER_VISUAL_APPROVAL = PENDING
```

## Contexto de implementação

O contexto de `$get-context` foi construído a partir dos contratos P3-0, foundation e Style Lab C aprovados, fluxo factual das telas atuais e fronteiras de ownership P3-A. O alvo é ARGOS Hybrid no DS 2.0.0: quatro composições novas — Início, Dashboard, Inventário e Detalhe da câmera — com fixtures locais; Quick Detail continua protegido/herdado. A revisão não autoriza alteração do Design System nem produção.

Referências visuais/factuais consultadas:

- Foundation visual C: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`.
- Shell aprovado: `docs/prototype/ui-v2/evidence/screenshots/shell/shell__1440x900__default__default.png`.
- Composição renderizada observada em Edge: `http://127.0.0.1:8766/docs/prototype/ui-v2/screens/p3-a/scr-portal-001.html?state=default`.

## Evidência e escopo desta passagem

Preview servido por HTTP local no worktree P3-A. O Edge conectado abriu as quatro telas novas no estado `default` e as capturas de página completa foram inspecionadas visualmente no fluxo da sessão. Foi observada a colisão de estados em todas: Portal mistura os módulos com acesso vazio; Dashboard mostra o painel vazio junto aos indicadores/atividade; Inventário mostra tabela junto a vazio, loading e error; Detalhe mostra histórico junto ao estado de histórico vazio.

As capturas foram apresentadas inline, mas não persistidas como PNG no diretório de evidências; portanto não constituem evidência nomeada do contrato P3-A. Os alvos Style Lab C e shell foram consultados separadamente, não em um artefato combinado normalizado. A passagem não registrou dimensões CSS do viewport nem zoom via instrumentação; não reivindica QA em 1920×1080, 1440×900, 1366×768 ou 390×844.

Não foram verificados os demais estados isoladamente, fixture longa, interações, Quick Detail protegido, estratégia responsiva/tabela ou baseline acessível. Não há screenshots de evidência nomeados persistidos. `DESIGN_QA_COMPLETE` permanece `NO`.

## Finding bloqueador

**F-01 — Variantes de estado `hidden` continuam renderizadas**

**Resultado:** bloqueador para state coverage e para o gate técnico P3-A.


Nas quatro telas renderizadas em `?state=default`, conteúdos de estado alternativo permanecem visíveis simultaneamente com o conteúdo default. O harness alterna variantes usando o atributo/propriedade HTML `hidden`; regras author `display` em patterns/componentes canônicos prevalecem sobre o estilo user-agent de `[hidden]`. Os seletores observados incluem `.argos-state`, `.argos-two-column`, `.argos-alert` e `.argos-docs-nav a`; deve-se validar o conjunto canônico completo.

Isso invalida a distinção visual entre as variantes e pode misturar conteúdos de estado em telas que dependem do mesmo mecanismo. Não é uma inconsistência a corrigir por override local: DS e harness são root-owned/read-only para P3-A. A solicitação está registrada como `DS_CHANGE_REQUEST` em `coverage.md`, com decisão de versão e reaprovação do usuário pendentes.

**Próximo passo de QA:** após adjudicação e eventual correção compartilhada pelo owner, repetir a matriz completa de estados, fixture longa, interação e os quatro viewports; salvar screenshots com naming canônico no diretório de evidence P3-A; então completar revisão visual de tipografia, hierarquia, espaçamento, densidade, alinhamento, imagens, overflow/over-stretch, navegação e acessibilidade baseline. Não declarar conformidade WCAG completa.

## Estado dos gates

```text
FOUR_DEFAULT_RENDERS = OBSERVED_WITH_BLOCKING_STATE_COLLISION
COMPOSITION_REVIEW = PARTIAL; viewport normalizado e comparação pareada pendentes
REQUIRED_STATES = BLOCKED_BY_DS_CHANGE
RESPONSIVE_QA = NOT_RUN
ACCESSIBILITY_BASELINE = NOT_RUN
NAMED_SCREENSHOT_EVIDENCE = NOT_GENERATED
TECHNICAL_READY_FOR_REVIEW = NO
DESIGN_QA_COMPLETE = NO
```

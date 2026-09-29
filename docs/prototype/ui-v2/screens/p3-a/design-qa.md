# P3-A — Product Design / design QA

## Retomada pós-DS 2.0.1 — QA técnico (2026-09-28)

**final result: blocked**

```text
F01 = RESOLVED / DS 2.0.1 hidden semantics regression PASS
F02 = OPEN / mobile inventory table readability / ROOT adjudication required
F03 = OPEN / evidence capture mechanism blocked
PORTAL = QA EXECUTED
DASHBOARD = QA EXECUTED
INVENTORY = QA EXECUTED WITH F02
CAMERA_DETAIL = QA EXECUTED
QUICK_DETAIL = PROTECTED / INHERITED
EVIDENCE_CAPTURE_STATUS = BLOCKED
P3_A_FINAL_COMPLETION_COMMIT = NOT_CREATED / technical gate did not pass
BLOCKED_CHECKPOINT_COMMIT = AUTHORIZED / family-owned records only; SHA reported after creation
PUSH_AUTHORIZED = YES / codex/ui-v2-p3-a-core-inventory only
USER_VISUAL_APPROVAL = PENDING
```

### Fonte visual e evidência

- Direção ARGOS HYBRID: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`.
- Referência do shell: `docs/prototype/ui-v2/evidence/screenshots/shell/shell__1440x900__default__default.png`.
- Implementação: preview HTTP local em `http://127.0.0.1:8766/docs/prototype/ui-v2/screens/p3-a/`.
- Viewports inspecionados: 1920×1080, 1440×900, 1366×768 e 390×844, zoom 100%.
- Capturas de implementação foram vistas no browser para as quatro telas e estados relevantes; os PNGs não puderam ser persistidos. O caminho `docs/prototype/ui-v2/evidence/screenshots/p3-a/` não contém as capturas nomeadas requeridas.
- Não houve comparação visual pareada arquivada com fonte e implementação no mesmo artefato. Portanto, a revisão de fidelidade permanece parcial.

### Resultado das verificações

- F-01: PASS. Em Portal, Dashboard, Inventário e Detalhe, todos os elementos com `[hidden]` computaram `display: none`; cada estado solicitado ficou isolado. `hidden="until-found"` não é consumido por P3-A.
- Estados: Portal default/empty/long; Dashboard default/empty/long; Inventário default/empty/loading/error/long (página 2) e seleção por Enter; Detalhe default com freshness stale, empty, error e long. Nenhuma colisão de estado foi observada.
- Responsivo: não houve overflow global nas quatro larguras. A tabela preservou rolagem horizontal interna, mas a composição móvel perdeu densidade e scanability.
- Acessibilidade baseline: títulos e um H1 por tela; landmarks `main`/`nav` nomeados; imagens com `alt`; filtros rotulados; Skip Link focável com outline sólido de 3px; seleção da linha via Enter anunciou o resultado. Isso não é declaração de conformidade WCAG.
- Interação/filtros: busca sem resultado exibiu empty state; limpar filtros restaurou três linhas; página 2 expôs os registros longos. Quick Detail continua apenas apontando ao baseline protegido, sem nova página.
- Console: sem erros ou warnings durante a revisão.
- Comparação visual de desktop: cores, shell escuro, fundo claro, cards, hierarquia de títulos e tratamento de estados seguem a direção da fonte. A composição usa conteúdo próprio P3-A e a fonte Style Lab é uma referência de direção, não um mock por tela; sem pareamento salvo não certifica fidelidade final.

### Findings

- **[P2] Linhas do Inventário ficam excessivamente altas em 390px.** A tabela mede 859px dentro de um wrapper de 345px; a coluna de ações cai para 61px e as três linhas visíveis medem 283px cada por quebra intensa de texto. O usuário precisa rolar horizontalmente e também percorre muito espaço vertical para comparar câmeras. O sizing pertence ao pattern compartilhado; registrar como `DSCR-UIV2-002-MOBILE-TABLE-READABILITY` para revisão ROOT. P3-A não introduziu CSS local ou override.
- **Bloqueio de evidência:** não foi possível gravar os PNGs nomeados exigidos no caminho P3-A. O browser recusou a navegação `data:` usada para salvar a imagem e sua política bloqueia contornar a recusa. Capturas mostradas durante a execução não substituem os arquivos persistidos para o gate.

### Histórico de comparação

F-01 foi o bloqueador anterior. O cherry-pick do patch ROOT `8121ed38cc15e1ff6e72cb46bbb2ca865100bce0` corrigiu a semântica global; a regressão atual passou. Nenhum finding P0/P1 foi observado. O finding P2 de densidade móvel e a falta de evidência nomeada permanecem, então o resultado final continua `blocked`.

### Checklist de handoff

- [x] Confirmar DS 2.0.1 e F-01 resolvido em runtime.
- [x] Retestar estados e interação de Inventário.
- [x] Inspecionar os quatro viewports e baseline de acessibilidade.
- [ ] Revisar o request ROOT de sizing da tabela móvel.
- [ ] Persistir screenshots nomeados no diretório canônico.
- [ ] Completar comparação visual pareada e repetir o gate técnico.
- [ ] Apresentar as telas para revisão visual humana.

O relatório anterior abaixo permanece como histórico do checkpoint que estava bloqueado por F-01.

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

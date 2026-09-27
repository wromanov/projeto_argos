# ARGOS UI V2 — Prototype-Driven Visual Modernization

```text
STATUS = CANONICAL / ACTIVE
DOCUMENT_TYPE = PROJECT_UI_V2_OPERATIONAL_AUTHORITY
PROJECT = ARGOS
LANGUAGE = pt-BR
TRACK = ARGOS UI V2 — PROTOTYPE-DRIVEN VISUAL MODERNIZATION
NEXT_UI_ACTIVITY = UI-V2-P0 — SCREEN CENSUS
NEXT_UI_ACTIVITY_STATUS = PLANNED / NOT_STARTED / NOT_AUTHORIZED_BY_THIS_DOCUMENT
IMPLEMENTATION_AUTHORIZED = NO
```

## 1. Objetivo e autoridade

Modernizar visualmente todas as superfícies reais do ARGOS por protótipos
revisáveis antes de qualquer implementação visual em produção. Este plano é a
authority operacional de escopo, sequência, critérios e gates da trilha UI V2.
Ele não substitui contratos funcionais, arquitetura, segurança, continuidade,
roadmap ou a especificação detalhada do Design System.

```text
ARGOS OWNS STRUCTURE, FLOWS, NAMES, ROUTES, RULES AND INFORMATION ARCHITECTURE.
DESIGN SYSTEM OWNS VISUAL LANGUAGE.
PROTOTYPES BECOME VISUAL AUTHORITY AFTER EXPLICIT USER APPROVAL.
IMPLEMENTATION FOLLOWS THE APPROVED PROTOTYPE.
BACKEND AND UI-V2 MAY PROGRESS IN PARALLEL.
```

Precedência por assunto:

- estrutura, rotas, nomes, dados, fluxos e regras funcionais: ARGOS e seus
  contratos canônicos;
- linguagem visual e tokens: referência visual aprovada e decisões registradas
  para UI V2;
- protótipo: authority visual da tela/família somente depois da aprovação
  explícita do usuário;
- Quick Detail e seu contrato funcional: `ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`;
- ownership e remediação CSS: `ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md`,
  subordinada a este processo quanto a mudanças visuais futuras.

Conflitos devem ser identificados, classificados e encaminhados para adjudicação;
nenhuma referência, protótipo ou documento transfere authority funcional.

## 2. Estratégia e limites

```text
SELECTIVE VISUAL RETROFIT
+ SELECTIVE INTERACTION PATTERN ADOPTION
```

UI V2 não é redesenho integral, migração integral de Design System, substituição
do shell ou migração de framework. Preservar a stack factual do ARGOS:

```text
Django SSR
Django Templates
HTML semântico
CSS customizado
JavaScript Vanilla
Progressive Enhancement
componentes nativos do navegador
Design System próprio do ARGOS
```

Não introduzir como solução estrutural React, Vue, Angular, Svelte, Tailwind,
Bootstrap, shadcn/ui obrigatório, SPA ou bundler obrigatório. Referências podem
ser estudadas sem instalar suas stacks.

Podem mudar, após protótipo aprovado, tokens e apresentação de superfícies,
camadas, cards, bordas, tipografia, hierarquia, espaçamento, densidade,
controles, tabelas, filtros, paginação, estados, iconografia compatível e
responsividade. Permanecem com sua semântica e função: card, filtro, tabela,
sidebar, rota, dado, estado e fluxo. Não reorganizar o produto para copiar um
Design System externo.

## 3. Referências visuais

O pacote existente `camera-inventory-design-system-v1.0.1` permanece como
referência aprovada para contratos visuais, semantic tokens, anatomia de
componentes, padrões de interação, acessibilidade, padrões de página e
princípios de aceitação. Não copiar seu código cegamente.

Na futura P1, poderão ser comparadas referências como shadcn/ui, PatternFly,
IBM Carbon, Ant Design, Fluent 2, MUI/MUI X e outras descobertas pertinentes.
São candidatas de pesquisa, não adoções. A decisão visual final ocorrerá por
protótipo e aprovação humana. Esta atividade não seleciona um Design System
definitivo.

## 4. Fluxo prototype-driven

### P0 — UI-V2-P0 — Screen Census

Levantar, de forma factual, URLs, views, templates, páginas, estados relevantes,
formulários, dialogs/drawers e fluxos visuais. Agrupar superfícies por famílias;
não inventar telas ausentes. A entrega deverá registrar, quando aplicável:

```text
URL/ROUTE; VIEW; TEMPLATE; PARTIALS/COMPONENTS; CSS_OWNERSHIP; JS_BEHAVIOR;
PAGE_FAMILY; FUNCTIONAL_PURPOSE; CURRENT_VISUAL_STATE; RESPONSIVE_RELEVANCE;
PROTOTYPE_REQUIRED; DEPENDENCIES; NOTES
```

P0 é a próxima atividade UI e ainda não foi executada neste checkpoint.

### P1 — Visual Style Lab

Pesquisar e reconciliar referências. Produzir direções visuais comparáveis para
paleta, surfaces, layers, cards, controles, tabelas, filtros, badges, tipografia,
espaçamento, densidade e estados. Registrar a escolha do usuário; não declarar
um sistema final antes dessa decisão.

### P2 — Visual Foundation Prototype

Prototipar shell, sidebar, topbar, page header, tipografia, botões, campos,
selects, cards/KPIs, badges, tabelas, filtros, paginação, alertas, tabs,
dialog/modal, drawer e estados loading, empty, error, stale, focus, hover e
selected.

### P3 — Screen Prototypes

Prototipar todas as telas reais descobertas em P0, preservando estrutura,
hierarquia funcional, rotas, nomes, dados, fluxos e capacidades. As mudanças
priorizam linguagem visual. A lista inicial de famílias está na seção 6 e não
substitui o census factual. Para o Quick Detail, P3 referencia a baseline
aprovada existente; não cria uma direção visual alternativa sem nova autorização.

### P4 — User Visual Approval

Nenhuma tela ou família entra em implementação visual sem aprovação explícita do
usuário. Registrar `PROTOTYPE_VISUAL_ACCEPTANCE = PASS` somente depois dessa
aprovação, com escopo e versão aprovados identificáveis.

### P5 — Implementation

Implementar na stack factual, reproduzindo o protótipo aprovado sem
reinterpretar livremente o design. Preservar contratos de backend, arquitetura
CSS, acessibilidade e responsividade. A aprovação de uma família não aprova
automaticamente outra.

### P6 — Runtime Visual Validation

Comparar protótipo aprovado com ARGOS real em runtime. Validar fidelidade,
funcionalidade, responsividade, acessibilidade e regressões. Registrar
`POST_IMPLEMENTATION_VISUAL_ACCEPTANCE = PASS` somente após aprovação explícita
do usuário.

### P7 — Canonicalization

Canonicalizar tokens, componentes, baseline visual, screenshots/referências
aprovadas, documentação, ownership CSS e estado final da UI V2.

## 5. Gates de aceitação

```text
PROTOTYPE_VISUAL_ACCEPTANCE = PENDING
IMPLEMENTATION_BEFORE_APPROVED_PROTOTYPE = PROHIBITED
POST_IMPLEMENTATION_VISUAL_ACCEPTANCE = PENDING
USER_APPROVAL_REQUIRED_AT_P4 = YES
USER_APPROVAL_REQUIRED_AT_P6 = YES
```

Validação técnica ou screenshot produzido pelo agente não equivale à aprovação
humana. Mudança de layout ou estética depois da aprovação requer novo protótipo
e aprovação da revisão afetada.

## 6. Famílias iniciais conhecidas

Lista inicial, sujeita à descoberta P0: shell; dashboard; inventário; Quick
Detail; detalhe completo da câmera; criar/editar câmera; atividades; situação;
desativação/reativação; substituição e histórico de substituições; eventos;
auditoria; governança; formulários operacionais; perfil e edição; alteração de
senha; login/autenticação; páginas 403/404/500; estados vazios, loading e erro.
Não é lista definitiva nem confirmação de que todas as telas/estados existem.

## 7. Quick Detail — baseline protegido

```text
QUICK_DETAIL_VISUAL_BASELINE = APPROVED
QUICK_DETAIL_REDRAW_WITHOUT_NEW_EXPLICIT_AUTHORIZATION = PROHIBITED
```

O Quick Detail atual tem baseline visual explicitamente aprovado pelo usuário.
UI V2 deve preservá-lo como referência real de densidade, cards, espaçamento,
imagem, badges, footer e integração visual. P0 registra a superfície e pode
marcar `PROTOTYPE_REQUIRED = NO_FOR_REDESIGN` enquanto essa proteção vigorar.
P3 registra a baseline aprovada como referência daquela superfície; não produz
redesign sem nova autorização. Uma reprodução documental do baseline não
autoriza alteração visual. A decisão funcional do `CameraQuickDetailPanel`
segue a specification de UI-DS. A aprovação deste baseline visual não encerra
automaticamente a aceitação de produto de UI-3.

## 8. Relação com a remediação CSS e o roadmap existente

A auditoria UI-AUD-01 e a diretriz de remediação continuam sendo evidência e
guardrails técnicos. As fases concluídas — Phase 0 e Batch A — permanecem
fechadas. Os escopos pendentes do Batch B (Inventário, Dashboard e Quick Detail)
permanecem registrados como achados e necessidades, mas qualquer alteração
visual correspondente segue P0–P6 e a aprovação do protótipo aplicável. Isso
reconcilia a sequência futura sem reabrir a remediação já concluída nem apagar
seus resultados.

Ownership CSS pretendido:

| Arquivo | Ownership |
|---|---|
| `design-system.css` | tokens, tipografia base, botões, inputs, selects, cards genéricos, badges, tabelas genéricas, foco, estados compartilhados, sizing de controles, spacing primitives e semantic component tokens |
| `argos.css` | shell, sidebar, topbar, main, page container, navegação global e shell responsivo |
| `portal.css` | composição do Dashboard, grids, seções e cards de métricas |
| `inventario.css` | composição de inventário, filtros, tabela, ações, responsividade e seção local do Quick Detail |
| `governanca.css` | composição específica de Governança |

Regra permanente: remover ou consolidar antes de adicionar regras. O plano não
reabre trabalho de remediação concluído nem autoriza patches CSS.

Os marcos A2 — Visual 5, A3 — Visual 6 e A4 — Visual 7 mantêm seus objetivos
funcionais. Suas entregas visuais passam a ser planejadas, prototipadas e
aceitas pela trilha UI V2, sem renumerar nem invalidar esses marcos.

## 9. Paralelismo com o backend

UI V2 é uma trilha paralela à trilha backend. Uma não bloqueia artificialmente a
outra. Criar dependência apenas quando uma tela precisar apresentar capability
backend ainda inexistente.

```text
MON-AVAIL-01 = BLOCKED_HISTORICAL_COVERAGE_GAP
MON-AVAIL-01_EVIDENCE_PROVENANCE = CURRENT_USER_INSTRUCTION; NOT_FOUND_IN_REPOSITORY_SEARCH
MON-AVAIL-02 = RECOMMENDED / NOT_AUTHORIZED
```

O bloqueio reportado é a falta de evidência histórica suficiente para
reconstruir escopo e períodos `UNKNOWN` e calcular availability 30d sem inventar
dados. Não fabricar percentuais, coverage ratio ou estados históricos.
`MON-AVAIL-02` é a recomendação de fundação mínima para reconstrução factual de
eligible, online, offline e unknown duration, coverage e availability;
Indisponibilidade continua sendo fonte canônica dos intervalos OFFLINE
existentes, sem duplicar o histórico integral de estados.

O mapa de sprints ainda registra `IMG-04` como candidata backend/imagens não
autorizada. O repositório não registra uma decisão de sequência entre essa
candidata e `MON-AVAIL-02`; ambas permanecem distintas e sem autorização. O
estado atual deve ser lido em `PROJECT_STATE.md` e `SPRINTS_ARGOS_V5.md`.

## 10. Estado atual e próxima atividade

```text
UI_V2_TRACK_STATUS = DOCUMENTED
NEXT_UI_ACTIVITY = UI-V2-P0 — SCREEN CENSUS
P0_STATUS = PLANNED / NOT_STARTED / NOT_AUTHORIZED_BY_THIS_DOCUMENT
P0_EXECUTED_IN_THIS_ACTIVITY = NO
IMPLEMENTATION_AUTHORIZED = NO
STAGE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
```

Esta autoridade registra processo e sequência. A próxima atividade deverá
executar apenas o census autorizado por instrução própria. Após concluir a
reconciliação documental, parar; não iniciar P0, protótipos ou implementação.

## 11. Authorities relacionadas

- Estado recuperável e próxima atividade: `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`.
- Direção macro: `docs/projeto/ROADMAP_ARGOS_V5.md`.
- Sequência e gates: `docs/projeto/SPRINTS_ARGOS_V5.md`.
- UI V2 prototype-driven: este documento.
- Design System/CameraQuickDetailPanel e contrato visual-funcional: `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`.
- Auditoria e guardrails CSS: `docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md` e `docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md`.

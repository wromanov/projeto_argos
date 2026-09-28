# UI V2 P3 — Prototype Harness & Composition Contract

```text
STATUS = P3-0 / TECHNICAL PASS / USER REVIEW PENDING
PROJECT = ARGOS
ACTIVITY = UI-V2-P3-0
BASELINE_HEAD = 7702b4c14cac6f7338625ccd08730e8d89fb9495
DESIGN_SYSTEM_VERSION = 2.0.0 / PINNED
SELECTED_DIRECTION = C — ARGOS HYBRID
PROTOTYPE_ROOT = docs/prototype/ui-v2/screens/
PREVIEW_MODE = HTTP_LOCAL
P3_FAMILY_IMPLEMENTATION_STARTED = NO
MERGE = NO
PUSH = NO
```

Este contrato estabelece o harness compartilhado e os limites para o trabalho posterior das famílias P3. A autoridade de domínio continua no ARGOS; a autoridade visual compartilhada continua em `static/css/ui-v2/`. Composição de uma tela só se torna baseline de implementação após aprovação humana explícita, conforme `ARGOS_UI_V2_VISUAL_CONTRACT.md`.

## 1. Baseline e authorities

| Fato | Baseline de entrada |
|---|---|
| Repositório canônico | `C:\Users\walacedelgado\PycharmProjects\projeto_argos` — confirmado por `git rev-parse --show-toplevel` |
| Branch e HEAD de entrada | `master` / `7702b4c14cac6f7338625ccd08730e8d89fb9495` |
| `origin/master` e divergência | mesmo SHA / `0 0` |
| Worktree de entrada | limpo; staging vazio |
| Branch de trabalho P3-0 | `codex/ui-v2-p3-0-prototype-harness` |
| Checkout/worktree desta execução | Repositório canônico factual; branch P3-0 isolada, sem editar `master` |
| Design System | `static/css/ui-v2/`, versão `2.0.0`, pinada |
| Direção | `C — ARGOS HYBRID`, aprovada |
| Quick Detail | `APPROVED / PROTECTED`; sem redraw ou migração nesta atividade |
| Django Admin | `INHERITED`; sem redesign customizado por padrão |

Authorities funcionais: `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md` e `docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md`. Authorities visuais e de cobertura: `ARGOS_UI_V2_VISUAL_CONTRACT.md`, `COMPONENT_CATALOG.md`, `STATE_MATRIX.md` e `SCREEN_COVERAGE.md`. As quatro folhas canônicas são carregadas diretamente pelo HTML; não são copiadas nem alteradas.

O checkout estava alinhado e limpo, mas o `ACTIVE_DOCUMENT_MAP.md`, o roadmap e o sprint ainda continham snapshots anteriores a P2. O checkpoint final mais recente em `PROJECT_STATE.md` (seção 35) e `AGENT_CONTINUITY.md` (seção 20.5) confirma P2 fechado, Design System 2.0.0 pinado e P3 não iniciado. A autorização atual cobre somente P3-0.

## 2. Ownership e authority

- **ARGOS** define domínio, conteúdo, permissões, regras, fluxos, rotas, estrutura conceitual e itens reais de navegação. Quando visibilidade depende de permissão, o protótipo registra essa dependência e não simula uma matriz de acesso.
- **Design System ARGOS UI V2 2.0.0** define tokens, primitivas, componentes, patterns, espaçamento, densidade, superfícies, tipografia, estados visuais, active treatment e focus treatment.
- **Protótipo de tela** define composição, hierarquia, agrupamento, layout e uso dos componentes, sujeito à aprovação humana antes da implementação produtiva.
- **Quick Detail** herda a baseline visual aprovada e protegida; o owner registra a referência, sem criar alternativa visual.
- **Django Admin** permanece herdado e sem protótipo customizado por padrão.

O shell combina a arquitetura de informação factual do ARGOS com o vocabulário visual da UI V2. Não reproduz CSS V1 e não muda a IA.

## 3. Root, artefatos e CSS

```text
PROTOTYPE_ROOT = docs/prototype/ui-v2/screens/
PREVIEW_ENTRYPOINT = docs/prototype/ui-v2/screens/index.html
SHARED_SHELL = index.html
SHARED_HARNESS_JS = docs/prototype/ui-v2/screens/harness.js
FIXTURE_ROOT = docs/prototype/ui-v2/fixtures/
DESIGN_SYSTEM_FILES = static/css/ui-v2/{tokens,base,components,patterns}.css
DESIGN_SYSTEM_MODIFIED = NO
```

O índice é simultaneamente a entrada única do P3 e a demonstração do shell compartilhado `SCR-SHELL-001`. Ele contém apenas catálogo, navegação demonstrativa e explicação do harness; não é a implementação de telas P3-A/B/C/D.

O HTML referencia diretamente os quatro CSS canônicos por links relativos. Estilos adicionais de produto não são permitidos. CSS local só poderá documentar ou identificar o chrome do harness; não poderá redefinir Button, Card, Table, tokens ou linguagem visual. Uma lacuna visual real abre `DS_CHANGE_REQUEST` com `CHANGE`, `REASON`, `AFFECTED_COMPONENTS`, `AFFECTED_SCREENS`, `VERSION_IMPACT` e `USER_REAPPROVAL_REQUIRED`; a parte dependente fica `BLOCKED_BY_DS_CHANGE` até adjudicação. Neste checkpoint: nenhum pedido aberto.

`P3 != SECOND PRODUCTION APPLICATION`: sem Django runtime, templates produtivos, Python, backend, APIs reais, banco, persistência, autenticação real, monitoramento real, lógica funcional completa ou CSS V1. Nenhuma tela P3 foi iniciada.

## 4. Shell e navegação

Os links demonstrativos do shell reproduzem os itens e rotas da navegação principal existente em `templates/components/navegacao_principal.html` e no Screen Census:

| Item ARGOS | Rota conceitual | Destino local do índice | Observação |
|---|---|---|---|
| Início | `/` | `#screen-scr-portal-001` | item base |
| Dashboard | `/dashboard/` | `#screen-scr-dash-001` | visível conforme permissão `cameras.view_camera` |
| Inventário | `/cameras/` | `#screen-scr-inv-001` | visível conforme permissão `cameras.view_camera` |
| Governança | `/cameras/substituicoes/` | `#screen-scr-sub-list-001` | permissão factual de consulta a substituições |
| Eventos | `/eventos/` | `#screen-scr-event-list-001` | visível conforme permissão factual de consulta a eventos |

Os caminhos em `href` são âncoras relativas à página estática. `data-conceptual-route` registra a rota ARGOS, sem navegar para um backend. Itens do menu de conta podem apontar a telas por âncoras equivalentes; logout não executa ação. Links entre páginas P3 usam arquivos HTML relativos, com retorno para `../index.html` a partir de `screens/p3-<family>/`. Não adicionar SPA, router, redirect, framework ou servidor customizado.

`aria-current="page"` identifica o item ativo. Títulos, landmark `nav`, skip link, nomes acessíveis e `:focus-visible` devem permanecer semânticos. Em largura móvel, o pattern canônico do shell reorganiza o sidebar em navegação horizontal rolável; não há toggle ou JS necessário. Navegação tem de continuar alcançável por teclado e apresentar foco visível.

## 5. Preview

```text
PREVIEW_MODE = HTTP_LOCAL
PREVIEW_ENTRYPOINT = docs/prototype/ui-v2/screens/index.html
HTML_HOST_LITERAL = PROHIBITED
HTML_PORT_LITERAL = PROHIBITED
ABSOLUTE_WINDOWS_PATH_IN_HTML = PROHIBITED
```

Pré-visualizar pela raiz do checkout com um servidor estático simples, por exemplo `python -m http.server <port> -d .`, e abrir o caminho relativo do entrypoint no browser. `file://` não é preview válido. Porta concreta pode variar e não faz parte do contrato. Todo CSS, imagem, fixture, página e link de retorno deve ser relativo ao arquivo que o consome; não fixar `localhost`, `127.0.0.1`, portas ou caminhos absolutos em HTML.

## 6. Estado e fixtures

Uma página representa variações pela query string e fixtures determinísticas. O `harness.js` compartilhado, marcado `PROTOTYPE_ONLY`, normaliza os dois parâmetros para a lista permitida e expõe a seleção como `data-argos-prototype-state` e `data-argos-prototype-fixture` no elemento raiz. Ele alterna somente variantes marcadas com `data-argos-state-variant` e `data-argos-fixture-variant`; não carrega dados, chama APIs, persiste nem executa regra de domínio. Um formulário GET ou links simples podem selecionar a query string, sem router customizado.

```text
state = default | empty | loading | error
fixture = default | long
```

Exemplos: `inventory.html?state=empty`, `inventory.html?state=default&fixture=long`. Parâmetros omitidos e valores não reconhecidos retornam ao `default`. Estado de interface não cria estado de domínio. Não gerar um HTML por estado quando a própria página pode representar a variação. Um estado específico adicional exige justificativa semântica.

O mínimo reaproveitável fica em `docs/prototype/ui-v2/fixtures/`. `camera-inventory.json` fornece conteúdo fictício estável para `default` e `long`. A variante longa contém nome da câmera, fabricante, modelo, localização/setor, identificador e rótulo extensos. Não usar nomes de pessoas reais, usuários, endereços IP sensíveis, credenciais ou dados operacionais reais. Estados `empty`, `loading` e `error` são representações da página; não exigem fixture de registro.

Cada família deve classificar cada estado aplicável como `SUPPORTED`, `TESTED` ou `NOT_APPLICABLE`; o teste é registrado separadamente de suporte. Default e long content são o mínimo por tela. Empty/loading/error seguem Census e semântica da tela. Não fabricar estado artificial. O JSON atual disponibiliza fixture longa; o estado de tela que a consome permanece planejado até a implementação da família.

## 7. Metadata

Todo HTML de tela inclui:

```html
<meta name="argos-ui-version" content="2.0.0">
<meta name="argos-screen-id" content="SCR-...">
<meta name="argos-screen-family" content="...">
<meta name="argos-prototype-status" content="PLANNED">
```

O índice usa `SCR-SHELL-001`, `SHELL` e `TECHNICAL_READY_FOR_REVIEW`. O metadata P3 usa o status do contrato (`PLANNED`, `IN_PROGRESS`, `TECHNICAL_READY_FOR_REVIEW`, `USER_APPROVED`, `INHERITED`, `PROTECTED` ou `NOT_APPLICABLE`). `USER_APPROVED` só é permitido após aprovação humana explícita.

O registro da tela também informa `RESPONSIVE_STATUS`, `STATE_COVERAGE`, `USER_APPROVAL` e `OWNER`. Esses campos ficam em documentação/evidence da família; nenhum parser ou framework de metadata é necessário.

## 8. Evidence e QA

Screenshots vão para `docs/prototype/ui-v2/evidence/screenshots/<family>/` com nomes determinísticos:

```text
<screen-slug>__<viewport>__<state>__<fixture>.png
```

Exemplos: `inventory__1920x1080__default__default.png`, `inventory__1366x768__default__long.png`, `inventory__390x844__empty__default.png`. `screen-slug` é uma chave estável documentada pela família para o `SCREEN_ID`; não usar nomes ad hoc como `final.png`.

No shell compartilhado, `shell` identifica `SCR-SHELL-001`. A evidência inicial do P3-0 usa `shell__1920x1080__default__default.png`, `shell__1440x900__default__default.png`, `shell__1366x768__default__default.png` e `shell__390x844__default__default.png` em `docs/prototype/ui-v2/evidence/screenshots/shell/`.

Viewports obrigatórios a 100% de zoom: `1920x1080` wide desktop, `1440x900` primary desktop, `1366x768` compact desktop e `390x844` mobile. `320px` é opcional quando necessário. QA avalia overflow e também over-stretch, espaço em branco, densidade, max-width, proporção de shell, alinhamento e hierarquia.

Baseline de acessibilidade: título do documento; heading hierarchy; landmarks; navegação semântica; `aria-current` ou equivalente; nome acessível para controles com ícone; teclado e foco visível; touch targets; reduced motion quando aplicável. Verificações de dialog só se houver dialog. Este baseline não declara conformidade WCAG completa.

Fluxo de QA da família: renderizar; validar os quatro viewports; validar estados requeridos; validar long content; capturar screenshots com nomes determinísticos; executar o QA de design disponível; corrigir achados técnicos; registrar `TECHNICAL_READY_FOR_REVIEW`; aguardar revisão humana; marcar `USER_APPROVED` somente após aprovação explícita.

Product Design está disponível; `$get-context` e `$design-qa` foram carregadas. O contexto local foi conferido contra o Census, a navegação ARGOS, a foundation e o Design System pinado. O QA comparou capturas de mesma viewport e estado lado a lado; o resultado e suas evidências ficam em `design-qa.md` e em `docs/prototype/ui-v2/evidence/screenshots/shell/`. `DESIGN_QA_COMPLETE = YES` para o shell compartilhado; isso não revisa nem aprova as futuras telas de família.

## 9. Ownership matrix por SCREEN_ID

Fonte da partição: roster canônico do Census, conferido contra as 35 linhas do master `SCREEN_COVERAGE.md`. Cada `SCREEN_ID` aparece uma vez e tem um owner. Paths de família são destinos planejados, não arquivos existentes; não criar diretórios vazios. Arquivos usam o SCREEN_ID em lowercase.

| SCREEN_ID | SCREEN_NAME | FAMILY | OWNER | PROTOTYPE_PATH | STATUS |
|---|---|---|---|---|---|
| SCR-SHELL-001 | Shell autenticado | SHELL | ROOT | `docs/prototype/ui-v2/screens/index.html` | TECHNICAL_READY_FOR_REVIEW |
| SCR-PORTAL-001 | Início / portal | OTHER | P3-A | `docs/prototype/ui-v2/screens/p3-a/scr-portal-001.html` | PLANNED |
| SCR-DASH-001 | Dashboard | DASHBOARD | P3-A | `docs/prototype/ui-v2/screens/p3-a/scr-dash-001.html` | PLANNED |
| SCR-INV-001 | Inventário de câmeras | INVENTORY | P3-A | `docs/prototype/ui-v2/screens/p3-a/scr-inv-001.html` | PLANNED |
| SCR-CAM-DETAIL-001 | Detalhe da câmera | CAMERA_DETAIL | P3-A | `docs/prototype/ui-v2/screens/p3-a/scr-cam-detail-001.html` | PLANNED |
| SCR-CAM-QUICK-001 | Quick Detail | CAMERA_DETAIL | P3-A | INHERITED — baseline aprovada e protegida; sem novo arquivo | PROTECTED |
| SCR-CAM-CREATE-001 | Nova câmera | CAMERA_FORMS | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-cam-create-001.html` | PLANNED |
| SCR-CAM-EDIT-001 | Editar câmera | CAMERA_FORMS | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-cam-edit-001.html` | PLANNED |
| SCR-MON-HISTORY-001 | Histórico de monitoramento | MONITORING | P3-B | `docs/prototype/ui-v2/screens/p3-b/scr-mon-history-001.html` | PLANNED |
| SCR-ACT-LIST-001 | Atividades da câmera | ACTIVITIES | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-act-list-001.html` | PLANNED |
| SCR-ACT-CREATE-001 | Registrar atividade | ACTIVITIES | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-act-create-001.html` | PLANNED |
| SCR-ACT-EDIT-001 | Editar atividade | ACTIVITIES | P3-C | INHERITED — Census marca a superfície como herdada; confirmar necessidade dentro da família | INHERITED |
| SCR-GOV-STATE-001 | Alterar situação | GOVERNANCE | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-gov-state-001.html` | PLANNED |
| SCR-GOV-DISABLE-001 | Desativar câmera | GOVERNANCE | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-gov-disable-001.html` | PLANNED |
| SCR-GOV-REACTIVATE-001 | Reativar câmera | GOVERNANCE | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-gov-reactivate-001.html` | PLANNED |
| SCR-GOV-SUBSTITUTE-001 | Substituir câmera | GOVERNANCE | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-gov-substitute-001.html` | PLANNED |
| SCR-SUB-LIST-001 | Substituições | SUBSTITUTIONS | P3-B | `docs/prototype/ui-v2/screens/p3-b/scr-sub-list-001.html` | PLANNED |
| SCR-SUB-DETAIL-001 | Detalhe da substituição | SUBSTITUTIONS | P3-B | `docs/prototype/ui-v2/screens/p3-b/scr-sub-detail-001.html` | PLANNED |
| SCR-SUB-CAMERA-001 | Substituições da câmera | SUBSTITUTIONS | P3-B | `docs/prototype/ui-v2/screens/p3-b/scr-sub-camera-001.html` | PLANNED |
| SCR-EVENT-LIST-001 | Eventos de auditoria | EVENTS_AUDIT | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-event-list-001.html` | PLANNED |
| SCR-EVENT-DETAIL-001 | Detalhe do evento | EVENTS_AUDIT | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-event-detail-001.html` | PLANNED |
| SCR-EVENT-CAMERA-001 | Eventos da câmera | EVENTS_AUDIT | P3-C | `docs/prototype/ui-v2/screens/p3-c/scr-event-camera-001.html` | PLANNED |
| SCR-ACCOUNT-PROFILE-001 | Perfil | PROFILE_ACCOUNT | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-account-profile-001.html` | PLANNED |
| SCR-ACCOUNT-EDIT-001 | Editar perfil | PROFILE_ACCOUNT | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-account-edit-001.html` | PLANNED |
| SCR-ACCOUNT-PASSWORD-001 | Alterar senha | PROFILE_ACCOUNT | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-account-password-001.html` | PLANNED |
| SCR-AUTH-LOGIN-001 | Login ARGOS | AUTH | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-auth-login-001.html` | PLANNED |
| SCR-ERROR-403-001 | Acesso negado | ERROR_PAGES | P3-D | `docs/prototype/ui-v2/screens/p3-d/scr-error-403-001.html` | PLANNED |
| SCR-ADMIN-LOGIN-001 | Login Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-INDEX-001 | Índice Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-APP-001 | Lista de app Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-CHANGE-LIST-001 | Changelist Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-FORM-001 | Formulário Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-HISTORY-001 | Histórico Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-DELETE-001 | Confirmação Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |
| SCR-ADMIN-PASSWORD-001 | Troca de senha Admin | ADMIN | P3-D | INHERITED — Django Admin; sem redesign customizado | INHERITED |

Contagem: 35 IDs únicos; ROOT 1; P3-A 5; P3-B 4; P3-C 10; P3-D 15. Os 24 `PROTOTYPE_REQUIRED=YES` ficam todos atribuídos. As 11 superfícies `INHERITED` do Census continuam rastreadas; Quick Detail tem status mais específico `PROTECTED`. Conflitos de ownership: nenhum conhecido.

## 10. Partição e plano de paralelização

| Família | Census families | Owner exclusivo |
|---|---|---|
| P3-A — Core / Inventory | OTHER, DASHBOARD, INVENTORY, CAMERA_DETAIL | P3-A |
| P3-B — Monitoring / Operational | MONITORING, SUBSTITUTIONS | P3-B |
| P3-C — Governance / Audit / Activities | ACTIVITIES, GOVERNANCE, EVENTS_AUDIT | P3-C |
| P3-D — Forms / Account / Auth / Secondary | CAMERA_FORMS, PROFILE_ACCOUNT, AUTH, ERROR_PAGES, ADMIN | P3-D |
| Shared root | SHELL | ROOT |

Não existe atribuição dupla ou tela elegível sem owner. `BACKEND_PARALLELISM = ALLOWED` em worktree separado: backend não toca artefatos de protótipo; P3 não toca backend; conflitos funcionais são reportados, não resolvidos silenciosamente.

Fan-out ainda não liberado. Depois do gate canônico, P3-A/B/C/D recebem branches e worktrees próprios, todas partindo exatamente do mesmo `FAN_OUT_BASE_COMMIT`. Cada família altera somente suas páginas, JS/fixtures exclusivos, screenshots e relatório local de coverage. Family agents não alteram index, harness compartilhado, Design System, `SCREEN_COVERAGE.md` master, PROJECT_STATE, AGENT_CONTINUITY, roadmap ou sprints.

## 11. Integração e gates

Esta branch P3-0 fecha tecnicamente o harness; nesta execução inicial não há merge, push ou rebase. Após revisão humana P3-0, a integração canônica é uma atividade separada: merge autorizado para master; validação pós-integração; publicação autorizada; confirmação `HEAD == origin/master` e divergência `0/0`. Só então registrar `FAN_OUT_BASE_COMMIT` e avaliar `FAN_OUT_READY`.

No futuro, integrar uma família por vez. Para cada família: revisar; validar ownership; merge; resolver e validar conflitos; executar QA integrado; consolidar seus relatórios locais no `SCREEN_COVERAGE.md` master; só então seguir à próxima. `USER_APPROVED` exige aprovação humana por família. Nenhuma aprovação é automática.

## 12. Screen Coverage integration model

`docs/prototype/ui-v2/contracts/SCREEN_COVERAGE.md` master é owned por ROOT/Integrator. Este contrato define owner, path planejado, estado inicial, versão, responsive e semântica dos estados. No fan-out, cada família entrega relatório local; o root consolida os resultados depois da integração, sem permitir concorrência artificial no master. Estados devem registrar `SUPPORTED`, `TESTED` ou `NOT_APPLICABLE`; `LONG_CONTENT` só passa após teste visual da tela.

## 13. Estado de P3-0 e próximo gate

```text
DESIGN_SYSTEM_VERSION = 2.0.0
DESIGN_SYSTEM_2_0_0_PINNED = YES
DESIGN_SYSTEM_MODIFIED = NO
PRODUCTION_CHANGED = NO
PRODUCTION_UI_V2_INTEGRATION_STARTED = NO
QUICK_DETAIL_PROTECTED = YES
ADMIN_SCOPE_PRESERVED = YES
P3_FAMILY_IMPLEMENTATION_STARTED = NO
PRODUCT_DESIGN_STATUS = AVAILABLE
PRODUCT_DESIGN_GET_CONTEXT = PASS / loaded and aligned with local canonical sources
PRODUCT_DESIGN_DESIGN_QA = PASS / rendered shell compared with approved foundation
DESIGN_QA_COMPLETE = YES
FAN_OUT_READY = NO
```

O estado técnico final, a conclusão da validação e o commit desta atividade são registrados em `PROJECT_STATE.md`, `AGENT_CONTINUITY.md` e no relatório final da execução. Próximo gate: revisão humana P3-0 e integração canônica autorizada separadamente.

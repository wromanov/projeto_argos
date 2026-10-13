# HOM-01-DASHBOARD-V7-INTEGRATED-DESIGN-QA

**Estado atual:** ACEITE VISUAL HUMANO PASS — quatro capturas integradas aprovadas pelo usuário nos viewports registrados. DPR observado 0,9; zoom 100% não verificado; comparação pixel a pixel não reivindicada. Os registros anteriores de execução e recuperação abaixo foram preservados como histórico.

## Identificação e método

- Projeto: `projeto_argos`
- Branch: `codex/hom-v1-integration`
- HEAD antes/depois: `e91e4499d43211722b7eadba9adab842e3c75aeb`
- Worktree: limpa antes da auditoria; nenhum arquivo de código-fonte foi alterado.
- Origem: página real Django `http://127.0.0.1:8765/dashboard/` no launcher QA.
- Conta: `Perfil QA operacional` (perfil local não administrativo; credencial temporária não registrada).
- Banco: SQLite QA isolado, cinco câmeras sintéticas, sem workers, probes ou integrações externas.
- Dashboard: abriu após autenticação; CSS `/static/css/dashboard-v7.css` respondeu HTTP 200 (13.792 bytes).
- Captura visual disponível: screenshot inline do navegador durante a sessão, imagem de 1265 × 711 px. A interface de navegador desta sessão não expôs controle para fixar nem comprovar viewport CSS/DPR; esta captura não representa nenhum dos quatro viewports requeridos e não foi salva como arquivo.
- Zoom: 100% não foi alterado; DPR e viewport CSS real não foram verificáveis.
- Horário da inspeção: 13/10/2026, aproximadamente 13:15–13:19 BRT.

## Referência

A autoridade de composição é `docs/prototype/new_ui_dashboard/prototype/ARGOS_DASHBOARD_AJUSTADO_V7.html`, com aceite humano do protótipo registrado em `handoff/VISUAL_CONTRACT_V7.md`. Foram consultados também `handoff/IMPLEMENTATION_HANDOFF.md`, `handoff/DESIGN_QA_V7.md` e `ARGOS_DASHBOARD_V7_VISUAL_CONTRACT.md`.

Precedência preservada: “Monitoramento e completude”, “Desconhecido” e “Câmeras com IP duplicado” são nomenclaturas funcionais posteriormente aprovadas; não são bugs. A métrica de IP duplicado representa câmeras afetadas por endereços repetidos. `UNKNOWN` não foi tratado como `STALE`.

## Matriz obrigatória

| Viewport | Resultado | Observação |
|---|---|---|
| 1920 × 1080 | NOT_VERIFIED | Sem controle para configurar/comprovar viewport CSS e DPR. |
| 1440 × 900 | NOT_VERIFIED | Capturas anteriores em `PROJECT_STATE.md` §104 são evidência histórica, não recaptura desta auditoria. |
| 1366 × 768 | NOT_VERIFIED | Não inspecionado nesta auditoria. |
| 390 × 844 | NOT_VERIFIED | Não inspecionado nesta auditoria. |

A captura inline observada em 1265 × 711 px mostrou todo o shell e as seções do Dashboard, mas não substitui nenhum tamanho obrigatório.

## Observações da captura inline (sem equivalência formal de viewport)

- Cabeçalho: kicker, título, descrição e ações “Abrir inventário” e “Nova câmera” presentes; ambas as ações ficaram lado a lado.
- Monitoramento: “Estado não confirmado” destacado na primeira coluna; Online, Offline e Não monitorada distribuídos nas células seguintes; faixa de frescor independente presente.
- Inventário: total como âncora à esquerda; números e rótulos secundários distribuídos em grade 2×2; atalhos “Ver câmeras” preservam filtros funcionais.
- Qualidade cadastral: “Cadastros completos” em destaque; Incompletos e “Câmeras com IP duplicado” na coluna secundária.
- Atividade recente: dois painéis lado a lado no desktop observado; estado vazio à esquerda e cinco câmeras sintéticas à direita. Altura acompanhou a lista vista.
- Resumo contém “Câmeras exibidas 5”, conforme a implementação e o contrato que proíbe reinterpretar a contagem de itens visíveis como total do inventário. Nenhuma métrica foi adicionada ou alterada.
- Dados sintéticos vistos: 5 câmeras; 2 com estado desconhecido, 0 online, 0 offline, 3 não monitoradas; frescor desatualizado em 2; 4 cadastros completos, 1 incompleto, 0 afetadas por IP duplicado.
- Nenhuma consulta, total ou estado foi alterado para esta auditoria.

## Sidebar e topbar

No screenshot inline, sidebar e topbar mantiveram a composição do shell existente; Dashboard estava ativo, conteúdo alinhado abaixo da topbar e ações acessíveis. Comparação visual qualitativa com `docs/projeto/evidence/sidebar-active-recovery/dashboard-current.png` não mostrou regressão evidente no shell observado. A verificação é parcial por não cobrir os quatro viewports. Nenhum arquivo de shell foi alterado.

## Acessibilidade direcionada

- Tab alcançou primeiro “Pular para o conteúdo principal”; o foco era visível.
- Sequência observada: marca ARGOS, Início, Dashboard, Inventário, Governança, Eventos, menu da conta e “Abrir inventário”.
- O contorno de foco também ficou visível na ação “Abrir inventário”.
- Ordem lógica aparente; não foi executada uma auditoria WCAG global nem verificada a sequência completa de todas as listas.
- Resultado: PARCIAL.

## Findings

Nenhum finding P1, P2 ou P3 foi aberto nesta execução parcial: os viewports especificados não foram comprovados, então não atribuí severidade nem declarei conformidade por inferência. Itens responsivos, overflow, cortes, dimensões comparativas e comportamento mobile permanecem `NOT_VERIFIED`.

- P1: NOT_ASSESSED
- P2: NOT_ASSESSED
- P3: NOT_ASSESSED
- Divergências funcionais aprovadas: nomenclaturas protegidas conforme contrato; nenhum finding.

## Estado final

```text
V7_REFERENCE_VERIFIED = YES / aprovada, arquivos e precedência confirmados
DJANGO_QA_ENVIRONMENT = PASS / launcher local e banco sintético segregado
DJANGO_DASHBOARD_HTTP = PASS / página autenticada renderizada; CSS HTTP 200
VIEWPORT_1920x1080 = NOT_VERIFIED
VIEWPORT_1440x900 = NOT_VERIFIED_THIS_ACTIVITY
VIEWPORT_1366x768 = NOT_VERIFIED
VIEWPORT_390x844 = NOT_VERIFIED
VISUAL_CONFORMANCE = PARTIAL / captura inline fora dos tamanhos obrigatórios
RESPONSIVE_CONFORMANCE = NOT_VERIFIED
MONITORING_SECTION = PARTIAL
INVENTORY_SECTION = PARTIAL
REGISTRATION_QUALITY_SECTION = PARTIAL
RECENT_ACTIVITY_SECTION = PARTIAL
SIDEBAR_REGRESSION = NONE_OBSERVED_AT_CAPTURED_SIZE / outros tamanhos NOT_VERIFIED
TOPBAR_REGRESSION = NONE_OBSERVED_AT_CAPTURED_SIZE / outros tamanhos NOT_VERIFIED
METRIC_SEMANTICS_PRESERVED = YES / inspeção e nenhum dado alterado
APPROVED_TERMINOLOGY_PRESERVED = YES
KEYBOARD_FOCUS_QA = PARTIAL_PASS
SCREENSHOTS_SAVED = NO / apenas captura inline; limitação do navegador desta sessão
P1_FINDINGS = NOT_ASSESSED
P2_FINDINGS = NOT_ASSESSED
P3_FINDINGS = NOT_ASSESSED
SOURCE_CODE_CHANGED = NO
HUMAN_DJANGO_VISUAL_APPROVAL = PENDING
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = NOT_PERFORMED / atividade parcial; gate de encerramento não atingido
NEXT_RECOMMENDED_ACTION = repetir captura em navegador que permita viewports CSS/DPR explícitos e salvar os quatro screenshots reais antes da adjudicação visual humana
```

## Recuperação de captura — investigação de automação (13/10/2026)

```text
ACTIVITY = HOM-01-DASHBOARD-V7-QA-CAPTURE-RECOVERY
BROWSER = Microsoft Edge / instalado e em execução
PLAYWRIGHT = NOT_AVAILABLE / ausente no `.venv` e não resolvido pelo Node do projeto
SELENIUM = NOT_AVAILABLE / pacote Python e `selenium-webdriver` ausentes
PUPPETEER = NOT_AVAILABLE / pacote Node ausente
EDGE_WEBDRIVER = NOT_AVAILABLE / `msedgedriver` não encontrado no PATH
CHROMEDRIVER = NOT_AVAILABLE / `chromedriver` não encontrado no PATH
ALTERNATIVE = Windows Computer Use / disponível, mas interrompido antes de inspecionar DevTools
BLOCKER = o controle do Edge não conseguiu determinar a URL atual da janela com confiança suficiente para aplicar a política de navegação
LOGIN_AUTOMATION = NOT_PERFORMED / será necessária autenticação manual pelo usuário
QA_LAUNCHER = PASS / verificação concluída, cinco registros sintéticos, sem migrations pendentes
QA_DASHBOARD = NOT_VERIFIED_IN_THIS_RECOVERY / Edge abriu a tela de login; autenticação manual pendente
VIEWPORT_MATRIX = NOT_VERIFIED
DPR_CONFIRMED = NO
SCREENSHOTS_SAVED = NO
SOURCE_CODE_CHANGED = NO
REPORT_UPDATED = YES / este adendo preserva o relatório parcial anterior
PROJECT_STATE_UPDATED = NO / critérios de conclusão ainda não satisfeitos
HUMAN_VISUAL_APPROVAL = PENDING
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
NEXT_ACTION = autenticar manualmente no Edge e capturar os quatro viewports pelo DevTools responsivo, ou disponibilizar uma sessão de navegador cujo URL possa ser validado pela ferramenta
```

O launcher local continua ativo em `127.0.0.1:8765` para a etapa manual. Nenhuma senha ou sessão foi incluída neste relatório. As ferramentas ausentes não foram instaladas e nenhuma dependência do projeto foi alterada.

## Correção da investigação de navegador — integração Edge disponível (13/10/2026)

A conclusão anterior de que não havia automação de navegador foi incorreta. A integração de navegador do Edge estava disponível nesta sessão e foi confirmada diretamente: ela lista abas do Edge, controla a aba existente via Playwright, permite avaliar métricas no contexto da página, configurar um viewport explícito e capturar screenshots. A ausência local de Playwright/Selenium/Puppeteer e de drivers no PATH não significava ausência da integração do navegador.

A aba Edge encontrada estava em `http://127.0.0.1:8765/login/?next=/dashboard/`. A navegação para `/dashboard/` redirecionou para a mesma tela de login. Portanto, a matriz de viewports e as capturas do dashboard continuam não verificadas nesta recuperação por falta de sessão autenticada disponível no Edge. Nenhuma credencial foi inserida ou solicitada pela ferramenta. A integração em si está validada; a autenticação é o bloqueio atual.

```text
EDGE_BROWSER_INTEGRATION = AVAILABLE_AND_CONFIRMED
EDGE_TAB_CONTROL = PASS / aba local controlada com DOM snapshot
VIEWPORT_OVERRIDE = AVAILABLE / capability viewport documentada para dimensões CSS explícitas
PAGE_METRICS_EVALUATION = AVAILABLE / Playwright evaluate em escopo somente leitura
BROWSER_SCREENSHOT = AVAILABLE / captura da viewport da aba
DASHBOARD_AUTH_SESSION = NOT_AVAILABLE / rota redireciona para login
VIEWPORT_MATRIX = NOT_VERIFIED / autenticação pendente
SCREENSHOTS_SAVED = NO / dashboard não autenticado
SOURCE_CODE_CHANGED = NO
```

Como prova da integração, a aba de login expôs as métricas reais da janela no momento da verificação: `innerWidth=1145`, `innerHeight=448`, `devicePixelRatio=1.125`, `documentElement.scrollWidth=1128`, `documentElement.clientWidth=1128`, `visualViewport.width=1128`, `visualViewport.height=448` e `visualViewport.scale=1`. Esses valores descrevem somente a tela de login e não substituem a matriz do Dashboard.

Este adendo corrige e prevalece sobre a afirmação anterior de indisponibilidade geral do navegador. O acesso autenticado ainda é necessário para concluir as capturas; após autenticação do usuário nesta aba local, a integração poderá continuar a validação. Não houve alteração de código-fonte nem de dependências.

## Retomada do ambiente QA — credencial operacional rotacionada (13/10/2026)

A sessão anterior do servidor foi encerrada a pedido do usuário. O launcher oficial preparou novamente o banco SQLite QA isolado, confirmou cinco câmeras sintéticas, preservou a identidade visual e rotacionou a senha da identidade operacional. O launcher encontrou uma colisão `PATH`/`Path` ao iniciar o processo filho no Windows, após concluir a preparação; o Django foi então iniciado diretamente com as mesmas variáveis e settings locais de QA, sem alteração de código. O endpoint de login respondeu HTTP 200 e a autenticação da conta operacional foi validada sem registrar a senha.

```text
OLD_QA_SERVER = STOPPED
QA_DATABASE = PASS / SQLite isolado, 5 registros sintéticos
OPERATIONAL_QA_CREDENTIAL = ROTATED / entregue diretamente ao usuário, não registrada no relatório
DJANGO_QA_SERVER = RUNNING / 127.0.0.1:8765
LOGIN_HTTP = PASS / 200
OPERATIONAL_QA_AUTH = PASS
SOURCE_CODE_CHANGED = NO
DEPENDENCIES_CHANGED = NO
DASHBOARD_VIEWPORT_MATRIX = NOT_VERIFIED / aguarda autenticação e continuação da auditoria
```

## Capturas autenticadas — matriz de viewports (13/10/2026)

Após a autenticação de `Perfil QA operacional`, a integração do Edge abriu a página Django real `/dashboard/`, com sidebar, topbar e todas as quatro regiões do painel presentes. O conteúdo mostrou os cinco registros sintéticos, sem alteração de dados. Foram configuradas dimensões CSS explícitas e capturadas as quatro imagens requeridas. O DPR/zoom não é configurável pela capability disponível, que expõe apenas largura e altura; os valores efetivos foram registrados sem presumir DPR 1 ou zoom 100%. `visualViewport.scale=1` é o valor observado, não uma confirmação independente do zoom do navegador.

| Viewport CSS (innerWidth × innerHeight) | DPR efetivo | scrollWidth / clientWidth | visualViewport (largura × altura; scale) | PNG físico | Horário da captura (BRT) |
|---|---:|---:|---|---:|---|
| 1920 × 1080 | 0,900000 | 1903 / 1903 | 1903,111 × 1080; 1 | 2114 × 1200 | 14:12:24 |
| 1440 × 900 | 0,900000 | 1423 / 1423 | 1423,111 × 900,444; 1 | 1581 × 1000 | 14:12:25 |
| 1366 × 768 | 0,900000 | 1349 / 1349 | 1349,333 × 768; 1 | 1499 × 853 | 14:12:25 |
| 390 × 844 | 0,900000 | 373 / 373 | 373,333 × 844,444; 1 | 414 × 938 | 14:12:25 |

Capturas de viewport: `current-1920x1080.png`, `current-1440x900.png`, `current-1366x768.png` e `current-390x844.png`. A captura adicional `current-390x844-full.png` registra as seções abaixo da dobra mobile (414 × 2116 px). Todas foram verificadas como arquivos PNG válidos. Em todos os quatro viewports, `documentElement.scrollWidth == documentElement.clientWidth`; não foi observado overflow horizontal global. A navegação horizontal rolável da sidebar no mobile é prevista pelo contrato responsivo V7.

## Comparação responsiva e adjudicação

O contrato V7 e as regras responsivas do HTML aprovado foram consultados como referência. As capturas atuais mostram os elementos contratados: cabeçalho e ações, monitoramento com estado não confirmado em destaque e faixa de frescor independente, inventário com total âncora e grade secundária 2×2, qualidade cadastral com cadastros completos em destaque e atividade recente em dois painéis no desktop, empilhados no mobile. Os dados e rótulos funcionais protegidos permanecem conforme as aprovações posteriores. Sidebar e topbar mantiveram o shell integrado observado anteriormente; nenhum código do shell foi alterado.

A política da integração do navegador bloqueou navegação para a referência local por protocolo `file:`. O HTML e o contrato foram inspecionados como documentos, sem tentar contornar o bloqueio com outra superfície de navegador. Por isso, esta execução registra aderência visual qualitativa ao contrato, mas não afirma comparação pixel a pixel entre duas renderizações. Não foram identificados findings P1/P2/P3 nas telas atuais; aprovação visual humana e comparação direta permanecem pendentes.

```text
ACTIVITY = HOM-01-DASHBOARD-V7-QA-CAPTURE-RECOVERY
BROWSER = Microsoft Edge / integração de navegador
CAPTURE_METHOD = viewport explícito via browser capability; screenshot da página Django autenticada
VIEWPORT_1920x1080 = PASS / innerWidth 1920, innerHeight 1080
VIEWPORT_1440x900 = PASS / innerWidth 1440, innerHeight 900
VIEWPORT_1366x768 = PASS / innerWidth 1366, innerHeight 768
VIEWPORT_390x844 = PASS / innerWidth 390, innerHeight 844
ZOOM = NOT_VERIFIED / capability não expõe controle/medição de zoom
DPR_CONFIRMED = YES / DPR observado 0.900000 em todos os viewports; não configurável pela capability disponível
SCREENSHOTS_SAVED = YES / quatro PNGs requeridos mais full-page mobile
JAVASCRIPT_CONSOLE_ERRORS = 0 / Edge tab logs na página atual
VISUAL_CONFORMANCE = QUALITATIVE_PASS / composição visível consistente com o contrato; pixel comparison não realizada
RESPONSIVE_CONFORMANCE = PASS / seções desktop em colunas, mobile empilhado; sem overflow horizontal global
SIDEBAR_REGRESSION = NONE_OBSERVED / navegação móvel rolável conforme contrato; shell protegido
TOPBAR_REGRESSION = NONE_OBSERVED
KEYBOARD_FOCUS_QA = PARTIAL_PASS / evidência anterior mantida
P1_FINDINGS = NONE_OBSERVED
P2_FINDINGS = NONE_OBSERVED; comparação pixel a pixel pendente
P3_FINDINGS = NONE_OBSERVED; comparação pixel a pixel pendente
SOURCE_CODE_CHANGED = NO
DEPENDENCIES_CHANGED = NO
REPORT_UPDATED = YES
PROJECT_STATE_UPDATED = NO / atividade não encerra HOM-01 nem substitui aceite humano
HUMAN_VISUAL_APPROVAL = PENDING
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
ACTIVITY_COMPLETE = NO / DPR/zoom e adjudicação visual humana permanecem pendentes
```

## Adjudicação humana — aceite visual (13/10/2026)

O usuário confirmou: “Eu validei e está ok.” Este aceite registra as quatro
capturas atuais (`current-1920x1080.png`, `current-1440x900.png`,
`current-1366x768.png` e `current-390x844.png`) nos viewports CSS
1920×1080, 1440×900, 1366×768 e 390×844.

```text
ACTIVITY = HOM-01-DASHBOARD-V7-VISUAL-ACCEPTANCE
USER_DECISION = APPROVED
DASHBOARD_V7_HUMAN_VISUAL_APPROVAL = PASS
APPROVED_VIEWPORTS = 1920x1080, 1440x900, 1366x768, 390x844
DPR_OBSERVED = 0.9
ZOOM_100_PERCENT = NOT_VERIFIED
PIXEL_PERFECT_COMPARISON = NOT_CLAIMED
VISUAL_COMPOSITION = PRESERVE / no new visual adjustments
AUDIT = NOT_REPEATED
SOURCE_CODE_CHANGE = NO
ACTIVITY_COMPLETION_PERCENT = 100%
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §108
```

O status desta atividade documental de aceite prevalece sobre os campos
históricos `HUMAN_VISUAL_APPROVAL = PENDING` e `ACTIVITY_COMPLETE = NO` no
relatório da auditoria anterior. As ressalvas de zoom e comparação visual
permanecem. O aceite não encerra HOM-01 nem autoriza o início de HOM-02.

## Sanitização do identificador da conta

As cinco capturas foram sanitizadas somente na área do identificador da conta
QA: nome no cabeçalho desktop e iniciais do avatar no cabeçalho mobile. As
máscaras são opacas e locais. As dimensões foram preservadas, e a comparação
com os originais privados confirmou identidade de todos os pixels fora dessas
áreas. Os originais permanecem em evidência privada excluída do repositório.

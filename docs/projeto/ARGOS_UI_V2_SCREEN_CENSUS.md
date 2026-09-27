# ARGOS UI V2 — UI-V2-P0 — Screen Census

**Status do artefato:** PASS_WITH_FINDINGS
**Data do censo:** 2026-09-27
**Atividade:** ARGOS UI V2 — PROTOTYPE-DRIVEN VISUAL MODERNIZATION
**Escopo:** inspeção estática, estritamente read-only para o código-fonte; criação somente deste documento.

## 1. Purpose

Registrar as superfícies visuais existentes no checkout e fornecer uma base factual para a futura atividade UI-V2-P1 — VISUAL STYLE LAB. Este censo descreve rotas, views, templates, componentes, CSS, JavaScript, estados, dependências, responsividade e necessidade de prototipação.

Princípios preservados:

- ARGOS OWNS STRUCTURE.
- DESIGN SYSTEM OWNS VISUAL LANGUAGE.
- PROTOTYPES BECOME VISUAL AUTHORITY AFTER USER APPROVAL.
- IMPLEMENTATION FOLLOWS APPROVED PROTOTYPE.

A UI V2 modernizará a apresentação visual sem reconstruir a arquitetura de informação, os nomes, os fluxos, as rotas, as regras funcionais ou as estruturas conceituais existentes.

## 2. Scope

Incluídos: rotas e superfícies HTML do ARGOS, shell compartilhado, resposta 403, diálogo Quick Detail, templates do Django Admin e os componentes e recursos que alimentam essas superfícies.

Fora do censo de telas: rotas de logout e upload como ações, endpoints JSON e de imagem como páginas independentes, assets sem superfície própria, templates de e-mail ou não encontrados, e estados que não estejam representados no código.

O Admin foi contado por oito arquétipos visuais do Django contrib.admin; suas URLs são geradas pelo Django e não aparecem como declarações individuais em config/urls.py.

## 3. Repository baseline

| Campo | Valor factual |
|---|---|
| REPOSITORY_ROOT | C:/Users/walac/desenvolvimento/projeto_argos |
| BRANCH | master |
| BASELINE_HEAD | b35b766076ac62955be6bf52cdb4c5fdd5098780 |
| UPSTREAM | origin/master @ 47c6965f3a60c0026117584dae21ca8a280986a5 |
| DIVERGENCE | 30 à frente / 0 atrás |
| WORKTREE | limpo no preflight; sem alterações anteriores à atividade |
| STAGING | vazio no preflight |
| WORKTREES | checkout principal e quatro worktrees vinculadas; não foram alteradas |
| TARGET | docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md não existia no preflight |

O HEAD factual difere dos baselines históricos registrados nos documentos de continuidade. O snapshot de PROJECT_STATE registra 323bfb0856a0bedc2b1b17cb07cb60dbcdd7c816 e divergência de 16/0; o HEAD observado agora é b35b766076ac62955be6bf52cdb4c5fdd5098780 e está 30/0. Essa diferença fica documentada, sem reconciliar nem modificar a continuidade nesta atividade.

## 4. Method

Inspeção estática do roteamento, views, configurações de middleware, templates, referências a folhas CSS e scripts, formulários, includes, ações e estados expressos no código. Foram lidos também os documentos canônicos listados abaixo. Nenhuma view foi invocada, nenhuma tela foi capturada em navegador e nenhum teste ou alteração de implementação foi executado.

A contagem usa composições visuais, não somente arquivos: 24 páginas HTML roteadas + 1 página 403 + 1 diálogo Quick Detail + 1 shell compartilhado + 8 arquétipos Admin = 35 superfícies. O shell é compartilhado, a resposta 403 não tem rota declarada própria e o diálogo Quick Detail está embutido em cameras/templates/cameras/lista.html.

### Autoridades inspecionadas

- AGENTS.md.
- docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md.
- docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md.
- docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md.
- docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md.
- Políticas canônicas de independência analítica, prompts, uso de skills/plugins e multiagentes indicadas pelo AGENTS.md.
- docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md.
- docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md.
- docs/projeto/ROADMAP_ARGOS_V5.md.
- docs/projeto/SPRINTS_ARGOS_V5.md.
- docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md.
- docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md.
- Fontes de config, core, cameras, usuarios, templates e static listadas nas seções seguintes.

## 5. Application shell

O shell HTML vem de templates/base.html e é herdado pelas páginas autenticadas da aplicação. A estrutura inclui sidebar e navegação principal, cabeçalho/topbar, menu do usuário, mensagens e região de conteúdo. O shell importa globalmente design-system.css, argos.css e portal.css; páginas acrescentam folhas locais por bloco extra_css. O portal.css participa do shell global mesmo sendo também dono de regras específicas do portal/dashboard.

O login é uma composição própria e não estende base.html. O Django Admin usa seu shell e templates contrib.admin.

## 6. Route census

Há 30 declarações de rota: o mount do Admin e 29 rotas da aplicação. As rotas root, core, usuarios, cameras e eventos usam namespaces conforme app_name em seus módulos incluídos. Todas as rotas da aplicação, exceto login, passam por LoginRequiredMiddleware; quick detail e previews explicitam login_not_required e executam verificações próprias. As permissões abaixo refletem decorators ou gates observados no código.

| ROUTE | URL_NAME | NAMESPACE | VIEW | VIEW_TYPE / APP | AUTH_REQUIRED | PERMISSION_REQUIRED |
|---|---|---|---|---|---|---|
| /admin/… | admin:* | admin | AdminSite.urls | gerado / Django Admin | varia; login Admin | is_staff e permissões de modelo |
| / | core:inicio | core | inicio | função / core | sim | nenhuma fixa; módulos condicionados por permissões |
| /dashboard/ | core:dashboard | core | dashboard | função / core | sim | cameras.view_camera |
| /login/ | usuarios:login | usuarios | ArgosLoginView | classe / usuarios | não | nenhuma |
| /logout/ | usuarios:logout | usuarios | logout_argos | função / usuarios | sim | nenhuma; POST encerra sessão |
| /perfil/ | usuarios:perfil | usuarios | perfil | função / usuarios | sim | usuário autenticado |
| /perfil/editar/ | usuarios:editar_perfil | usuarios | editar_perfil | função / usuarios | sim | usuário autenticado |
| /perfil/alterar-senha/ | usuarios:alterar_senha | usuarios | alterar_senha | função / usuarios | sim | usuário autenticado |
| /cameras/ | cameras:lista | cameras | lista_cameras | função / cameras | sim | cameras.view_camera |
| /cameras/nova/ | cameras:criar | cameras | criar_camera | função / cameras | sim | cameras.add_camera |
| /cameras/substituicoes/ | cameras:lista_substituicoes | cameras | lista_substituicoes | função / cameras | sim | cameras.consultar_substituicoescamera |
| /cameras/substituicoes/<pk>/ | cameras:detalhe_substituicao | cameras | detalhe_substituicao | função / cameras | sim | cameras.consultar_substituicoescamera |
| /cameras/<pk>/editar/ | cameras:editar | cameras | editar_camera | função / cameras | sim | cameras.change_camera |
| /cameras/<pk>/desativar/ | cameras:desativar | cameras | desativar_camera_view | função / cameras | sim | cameras.desativar_camera |
| /cameras/<pk>/reativar/ | cameras:reativar | cameras | reativar_camera_view | função / cameras | sim | cameras.reativar_camera |
| /cameras/<pk>/alterar-situacao/ | cameras:alterar_situacao | cameras | alterar_situacao_camera_view | função / cameras | sim | cameras.alterar_situacao_camera |
| /cameras/<pk>/substituir/ | cameras:substituir | cameras | substituir_camera_view | função / cameras | sim | cameras.registrar_substituicao_camera |
| /cameras/<pk>/eventos/ | cameras:eventos_camera | cameras | eventos_camera | função / cameras | sim | cameras.consultar_eventos |
| /cameras/<pk>/monitoramento/historico/ | cameras:historico_monitoramento | cameras | historico_monitoramento | função / cameras | sim | cameras.view_camera |
| /cameras/<pk>/imagens/upload/ | cameras:upload_imagem | cameras | upload_imagem_camera | função / cameras | sim | cameras.view_camera e cameras.add_cameraimagerecord |
| /cameras/<pk>/imagens/ultima-captura/<variant>/ | cameras:preview_ultima_captura | cameras | preview_ultima_captura | função / cameras | verificação própria | cameras.view_camera; variante validada |
| /cameras/<pk>/imagens/exibicao/<variant>/ | cameras:preview_exibicao | cameras | preview_exibicao | função / cameras | verificação própria | cameras.view_camera; variante validada |
| /cameras/<pk>/quick-detail/ | cameras:quick_detail | cameras | quick_detail_camera | função JSON / cameras | verificação própria | cameras.view_camera; GET sem parâmetros |
| /cameras/atividades/<pk>/editar/ | cameras:editar_atividade | cameras | editar_atividade_camera | função / cameras | sim | cameras.change_atividadecamera |
| /cameras/<camera_pk>/atividades/nova/ | cameras:criar_atividade | cameras | criar_atividade_camera | função / cameras | sim | cameras.add_atividadecamera |
| /cameras/<camera_pk>/substituicoes/ | cameras:lista_substituicoes_camera | cameras | lista_substituicoes_camera | função / cameras | sim | cameras.consultar_substituicoescamera |
| /cameras/<camera_pk>/atividades/ | cameras:lista_atividades | cameras | lista_atividades_camera | função / cameras | sim | cameras.view_atividadecamera |
| /cameras/<pk>/ | cameras:detalhe | cameras | detalhe_camera | função / cameras | sim | cameras.view_camera |
| /eventos/ | eventos:lista | eventos | lista_eventos | função / cameras | sim | cameras.consultar_eventos |
| /eventos/<pk>/ | eventos:detalhe | eventos | detalhe_evento | função / cameras | sim | cameras.consultar_eventos |

As duas rotas de preview retornam bytes de imagem, quick detail retorna JSON, upload aceita ação POST e redireciona, e logout encerra a sessão e redireciona. Não são páginas. Os previews e quick detail alimentam componentes visuais e estão ligados às telas correspondentes na matriz.

Não foram encontrados handler404 ou handler500 de projeto. Existe core/templates/403.html; testes e decorators confirmam resposta 403 customizada. Não há templates de projeto 404/500 identificados.

## 7. View census

Foram inspecionados 29 handlers roteados da aplicação. O contexto é resumido pelos dados principais; efeitos descrevem comportamento implementado nos métodos, sem execução.

| VIEW | PURPOSE / MAIN_CONTEXT_DATA | ACTIONS / FORMS | SIDE_EFFECTS / RELATED_SURFACES |
|---|---|---|---|
| core.views.inicio | Portal, nome exibido e módulos conforme permissões | Navegar para módulos/perfil | leitura de permissões; sem gravação |
| core.views.dashboard | Indicadores de câmeras, completude, monitoramento, substituições e atividades recentes | Links para telas relacionadas | consultas agregadas; sem gravação |
| usuarios.views.ArgosLoginView | Autenticação | formulário de login | autentica, mensagens e redirecionamento |
| usuarios.views.logout_argos | Encerrar sessão | POST com CSRF pelo menu | logout e redirect |
| usuarios.views.perfil | Dados, perfil, grupos e permissões do usuário | abrir edição, senha e, se staff, Admin | leitura |
| usuarios.views.editar_perfil | dados_form e perfil_form | forms de dados pessoais e perfil | atualiza usuário/perfil; mensagens |
| usuarios.views.alterar_senha | formulário de troca de senha | PasswordChangeForm | atualiza credencial; mensagens |
| cameras.views.lista_cameras | query, filtros, ordenação, paginação, status de monitoramento/imagem | busca GET, filtros, abrir detalhe/Quick Detail e ações autorizadas | consultas; endpoint quick detail e preview_exibicao |
| cameras.views.criar_camera | CameraCriacaoForm | cadastrar câmera | cria câmera e evento de auditoria; redirect para detalhe |
| cameras.views.editar_camera | câmera e CameraEdicaoForm | salvar alterações | atualiza câmera e evento se houver mudança |
| cameras.views.detalhe_camera | câmera, monitoramento, prévia de indisponibilidade, atividades e dados autorizados | editar, governança, imagens, eventos e históricos conforme permissões | leitura; upload usa rota própria |
| cameras.views.quick_detail_camera | payload privado e limitado de câmera | chamado GET assíncrono | JSON; valida sessão, permissão, método, query e existência |
| cameras.views.preview_ultima_captura | bytes da última captura | imagem inline | entrega de imagem com estados HTTP próprios |
| cameras.views.preview_exibicao | bytes da imagem atualmente selecionada para exibição | imagem inline | entrega de imagem com estados HTTP próprios |
| cameras.views.upload_imagem_camera | câmera e formulário/arquivo enviado | upload manual POST | grava imagem via serviço, mensagem e redirect |
| cameras.views.historico_monitoramento | câmera e itens de indisponibilidade paginados | navegação de páginas | consulta |
| cameras.views.desativar_camera_view | câmera e DesativarCameraForm | confirmar desativação | operação de governança, auditoria/mensagem e redirect |
| cameras.views.reativar_camera_view | câmera e ReativarCameraForm | confirmar reativação | operação de governança, auditoria/mensagem e redirect |
| cameras.views.alterar_situacao_camera_view | câmera e AlterarSituacaoCameraForm | alterar destino operacional | operação de governança, auditoria/mensagem e redirect |
| cameras.views.substituir_camera_view | câmera e SubstituirCameraForm | registrar substituição | transferência operacional via serviço; histórico e auditoria |
| cameras.views.lista_substituicoes | filtros por texto/período e lista paginada | filtros GET e limpar | consulta |
| cameras.views.detalhe_substituicao | registro e câmeras relacionadas | navegar às câmeras/histórico | consulta |
| cameras.views.lista_substituicoes_camera | histórico paginado da câmera | paginação | consulta |
| cameras.views.lista_atividades_camera | atividades paginadas da câmera | navegação e edição autorizada | consulta |
| cameras.views.criar_atividade_camera | câmera e AtividadeCameraForm | registrar atividade | grava atividade e evento; redirect |
| cameras.views.editar_atividade_camera | atividade, câmera e AtividadeCameraForm | editar atividade | atualiza atividade e registra alterações; redirect |
| cameras.views.lista_eventos | filtros por texto, categoria, origem, período e paginação | filtros GET e limpar | consulta |
| cameras.views.detalhe_evento | evento, usuário e câmera | navegação relacionada | consulta |
| cameras.views.eventos_camera | eventos filtrados e paginados para câmera | filtros GET e paginação | consulta |

Os sete ModelAdmin próprios são CameraAdmin, AtividadeCameraAdmin, EventoAuditoriaAdmin, SubstituicaoCameraAdmin, PerfilUsuarioAdmin, ArgosUserAdmin e ArgosGroupAdmin. Suas superfícies usam os templates padrão do Django Admin; os campos, filtros e ações variam por classe. As rotas internas são geradas pelo Admin.

## 8. Template census

Foram encontrados 40 templates HTML do projeto: 23 templates de página, 14 componentes, 2 fragmentos de formulário e 1 layout base. O Quick Detail é um dialog embutido, não um arquivo de template separado. Não foram encontrados templates de e-mail no escopo HTML inspecionado.

### Páginas

Todos os templates de página estendem templates/base.html, exceto usuarios/templates/usuarios/login.html, que é independente.

| TEMPLATE_PATH | TITLE / PURPOSE | MAIN_SECTIONS / COMPONENTS |
|---|---|---|
| core/templates/core/inicio.html | Início — ARGOS; seletor de módulos | saudação, cards de módulos, estado sem acesso operacional |
| core/templates/core/dashboard.html | Dashboard — ARGOS; indicadores | cartões/KPIs, painel de atividade recente, câmeras recentes, estados vazios |
| core/templates/403.html | Acesso negado — ARGOS | mensagem 403 e ação de retorno |
| usuarios/templates/usuarios/login.html | Entrar — ARGOS | marca, formulário e erros de autenticação |
| usuarios/templates/usuarios/perfil.html | Meu Perfil — ARGOS | cabeçalho/ações, cartões pessoais/conta/perfis/permissões, estados vazios |
| usuarios/templates/usuarios/editar_perfil.html | Editar meu perfil | seções Dados pessoais e Contato, forms e resumo de erros |
| usuarios/templates/usuarios/alterar_senha.html | Alterar minha senha | credenciais, erros, cancelar e enviar |
| cameras/templates/cameras/lista.html | Câmeras — ARGOS | busca/filtros GET, filtros ativos, tabela, badges, miniaturas, paginação, vazios e dialog |
| cameras/templates/cameras/detalhe.html | Detalhe da câmera | status/imagem, identidade, localização, rede, gravação, monitoramento, atividades, ações e eventos conforme permissão |
| cameras/templates/cameras/formulario.html | Nova/Editar câmera | formulário segmentado de identidade, localização, rede, gravação e operação; erros e ações |
| cameras/templates/cameras/monitoramento/historico.html | Histórico técnico | tabela de indisponibilidades e paginação |
| cameras/templates/cameras/atividades/lista.html | Histórico de atividades | lista/tabela de atividades, badges, vazios e paginação |
| cameras/templates/cameras/atividades/formulario.html | Registrar/Editar atividade | formulário, erros e ações; mesmo template para criação e edição |
| cameras/templates/cameras/governanca/alterar_situacao.html | Alterar situação operacional | formulário via governanca_action_shell, aviso e confirmação |
| cameras/templates/cameras/governanca/desativar.html | Desativar câmera | formulário via governanca_action_shell, aviso e confirmação |
| cameras/templates/cameras/governanca/reativar.html | Reativar câmera | formulário via governanca_action_shell, aviso e confirmação |
| cameras/templates/cameras/governanca/substituir.html | Substituir câmera | formulário via governanca_action_shell, aviso de preservação e confirmação |
| cameras/templates/cameras/substituicoes/lista.html | Substituições — ARGOS | filtros por texto/período, filtros ativos, registros, estados vazios e paginação |
| cameras/templates/cameras/substituicoes/detalhe.html | Detalhe da substituição | câmeras de origem/destino e dados históricos |
| cameras/templates/cameras/substituicoes/lista_camera.html | Histórico de substituições da câmera | registros históricos e paginação |
| cameras/templates/cameras/eventos/lista.html | Eventos de auditoria | filtros, filtros ativos, tabela, paginação e estado vazio |
| cameras/templates/cameras/eventos/detalhe.html | Detalhe do evento | identificação/categoria, dados do evento, origem e relações |
| cameras/templates/cameras/eventos/camera.html | Eventos de uma câmera | tabela, estado vazio e paginação |

Formulários e listas podem renderizar estados de erro, validação, vazio e sucesso por mensagens/condicionais. Imagens aparecem na lista e no detalhe da câmera; miniaturas usam loading lazy e a prévia remota usa o endpoint de imagem. Nenhum drawer independente foi encontrado. O dialog Quick Detail é o único dialog de tela identificado.

### Componentes e fragmentos

- Layout base: templates/base.html.
- Componentes em templates/components: sidebar.html, navegacao_principal.html, cabecalho.html, menu_usuario.html, mensagens.html, brand.html, paginacao.html, filtros_ativos.html, filtro_multisselecao.html, estado_vazio.html, governanca_action_shell.html.
- Fragmentos de formulário: campo_formulario.html e resumo_erros_formulario.html.
- Componentes de domínio: cameras/partials/_status_badge.html, _monitoring_badge.html e _atividade_tipo_badge.html.
- Outros elementos observados diretamente em páginas: cards/métricas, module-card, cartões de seção, botões/ações, filtros, tabelas, miniaturas e diálogo nativo.

Classificação: BASE_LAYOUT para templates/base.html; PAGE para as 23 páginas; COMPONENT para os 14 componentes; FORM_FRAGMENT para os dois fragmentos. Não foram identificados templates DRAWER, EMAIL ou NON_UI no conjunto HTML encontrado.

## 9. Screen families

Famílias principais classificadas pela superfície:

| FAMILY | SCREENS |
|---|---|
| SHELL | shell compartilhado |
| OTHER | portal Início |
| DASHBOARD | Dashboard |
| INVENTORY | lista de câmeras |
| CAMERA_DETAIL | detalhe e Quick Detail |
| CAMERA_FORMS | criar/editar câmera |
| MONITORING | histórico de indisponibilidades |
| ACTIVITIES | lista/criação/edição de atividades |
| GOVERNANCE | alterar situação, desativar, reativar e substituir |
| SUBSTITUTIONS | listas global e por câmera; detalhe |
| EVENTS_AUDIT | lista, detalhe e eventos por câmera |
| PROFILE_ACCOUNT | perfil, edição de perfil e senha |
| AUTH | login ARGOS |
| ERROR_PAGES | resposta 403 |
| ADMIN | oito arquétipos Django Admin |

TOTAL_FAMILIES = 15. Cada tela tem uma família principal na matriz.

## 10. Screen census

Complexidade considera densidade, componentes, filtros, tabelas, formulários, interações, imagens, estados e risco funcional. Relevância responsiva indica a importância de tratar a composição em diferentes larguras; não especifica breakpoints.

Abreviações na matriz: DS = design-system.css; Shell = argos.css; Portal = portal.css; Inv = inventario.css; Gov = governanca.css; Ev = eventos.css; Perfil = perfil.css; Auth = autenticacao.css. As três folhas DS, Shell e Portal são carregadas globalmente por base.html; folhas de domínio indicam o owner local. Admin usa folhas contrib.admin do Django.

| SCREEN_ID | SCREEN_NAME | FAMILY | ROUTE | URL_NAME | VIEW | TEMPLATE | PURPOSE | PRIMARY_COMPONENTS | CSS_OWNER | JS_BEHAVIOR | DOMAIN_STATES | UI_STATES | RESPONSIVE_RELEVANCE | PROTOTYPE_REQUIRED | PROTOTYPE_COMPLEXITY | KNOWN_DEPENDENCIES | NOTES |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SCR-SHELL-001 | Shell autenticado | SHELL | compartilhado | — | base/layout | templates/base.html | estrutura global da aplicação | sidebar, topbar, menu, mensagens | Shell | nenhum; menu usa details/POST nativo | permissão de módulo | default, focus, mensagens | HIGH | INHERITED | MEDIUM | DS, rotas, sessão | herdado por páginas ARGOS |
| SCR-PORTAL-001 | Início / portal | OTHER | / | core:inicio | inicio | core/templates/core/inicio.html | escolher módulo disponível | cards de módulo, vazio de acesso | Portal | nenhum | permissões de módulos | default, focus, empty | MEDIUM | YES | MEDIUM | auth, permissões, navegação | links variam por permissão |
| SCR-DASH-001 | Dashboard | DASHBOARD | /dashboard/ | core:dashboard | dashboard | core/templates/core/dashboard.html | indicadores e atividade recente | KPI, painéis, listas recentes | Portal | nenhum | PRODUCAO, ESTOQUE, DESATIVADA, completude, monitoramento | default, empty | HIGH | YES | HIGH | MonitoringReadService, modelos | agregações de leitura |
| SCR-INV-001 | Inventário de câmeras | INVENTORY | /cameras/ | cameras:lista | lista_cameras | cameras/templates/cameras/lista.html | localizar e administrar câmeras | filtros, tabela, badges, thumbs, paginação | Inv + Gov | filtros.js, camera-thumbnails.js, camera-quick-detail.js | operação, completude, monitoramento, imagem | default, hover, focus, selected, empty, loading, error | HIGH | YES | HIGH | query GET, quick detail JSON, previews | modal/dados são baseline; consultar permissão |
| SCR-CAM-DETAIL-001 | Detalhe da câmera | CAMERA_DETAIL | /cameras/<pk>/ | cameras:detalhe | detalhe_camera | cameras/templates/cameras/detalhe.html | consultar dados e histórico da câmera | cards de seção, badges, imagem, ações | Inv + Gov | nenhum | operação, completude, monitoramento, indisponibilidade, imagem | default, empty, error, stale | HIGH | YES | HIGH | imagem, eventos, atividades, substituições | blocos variam com permissão |
| SCR-CAM-QUICK-001 | Quick Detail | CAMERA_DETAIL | /cameras/<pk>/quick-detail/ | cameras:quick_detail | quick_detail_camera | cameras/templates/cameras/lista.html | prévia resumida sem sair do inventário | dialog, resumo, imagem, navegação | Inv | quick-detail.js; JSON assíncrono e imagem | disponibilidade da câmera/imagem, status | loading, error, focus, open/closed | HIGH | INHERITED | HIGH | JSON quick detail, preview_exibicao | VISUAL_BASELINE APPROVED; REDESIGN_AUTHORIZED NO |
| SCR-CAM-CREATE-001 | Nova câmera | CAMERA_FORMS | /cameras/nova/ | cameras:criar | criar_camera | cameras/templates/cameras/formulario.html | cadastrar câmera | formulário longo, seções, campos, ações | Inv + Gov | camera-form.js alterna campos customizados | operação, completude | default, focus, error, success | HIGH | YES | HIGH | CameraCriacaoForm, auditoria | farm/codec/retenção customizados |
| SCR-CAM-EDIT-001 | Editar câmera | CAMERA_FORMS | /cameras/<pk>/editar/ | cameras:editar | editar_camera | cameras/templates/cameras/formulario.html | atualizar cadastro da câmera | formulário longo, seções, campos, ações | Inv + Gov | camera-form.js alterna campos customizados | operação, completude | default, focus, selected, error, success | HIGH | YES | HIGH | CameraEdicaoForm, auditoria | mesma página-base, conjunto de campos pode variar |
| SCR-MON-HISTORY-001 | Histórico de monitoramento | MONITORING | /cameras/<pk>/monitoramento/historico/ | cameras:historico_monitoramento | historico_monitoramento | cameras/templates/cameras/monitoramento/historico.html | consultar indisponibilidades | tabela, paginação, volta ao detalhe | Inv | nenhum | incidente aberto/fechado; origem e motivo de fechamento | default, empty, stale | HIGH | YES | MEDIUM | MonitoringReadService | close_reason informa recuperação; não é enum RECOVERING |
| SCR-ACT-LIST-001 | Atividades da câmera | ACTIVITIES | /cameras/<camera_pk>/atividades/ | cameras:lista_atividades | lista_atividades_camera | cameras/templates/cameras/atividades/lista.html | histórico de atividades | tabela/lista, badge, vazio, paginação | Inv | nenhum | tipos de atividade | default, empty | HIGH | YES | MEDIUM | AtividadeCamera, paginação | ações condicionadas por permissão |
| SCR-ACT-CREATE-001 | Registrar atividade | ACTIVITIES | /cameras/<camera_pk>/atividades/nova/ | cameras:criar_atividade | criar_atividade_camera | cameras/templates/cameras/atividades/formulario.html | criar registro de atividade | formulário, erros, ações | Inv | nenhum | tipo e data da atividade | default, focus, error, success | HIGH | YES | MEDIUM | AtividadeCameraForm, auditoria | data inicial usa hora local |
| SCR-ACT-EDIT-001 | Editar atividade | ACTIVITIES | /cameras/atividades/<pk>/editar/ | cameras:editar_atividade | editar_atividade_camera | cameras/templates/cameras/atividades/formulario.html | editar registro existente | formulário, erros, ações | Inv | nenhum | tipo e data da atividade | default, selected, error, success | MEDIUM | INHERITED | MEDIUM | AtividadeCameraForm, auditoria | mesma composição de criação; modo edição |
| SCR-GOV-STATE-001 | Alterar situação | GOVERNANCE | /cameras/<pk>/alterar-situacao/ | cameras:alterar_situacao | alterar_situacao_camera_view | cameras/templates/cameras/governanca/alterar_situacao.html | mudar destino operacional | form, aviso, ação confirmada | Inv + Gov | nenhum | PRODUCAO, ESTOQUE, DESATIVADA | default, focus, error, success | HIGH | YES | MEDIUM | AlterarSituacaoCameraForm | situação não altera estado técnico |
| SCR-GOV-DISABLE-001 | Desativar câmera | GOVERNANCE | /cameras/<pk>/desativar/ | cameras:desativar | desativar_camera_view | cameras/templates/cameras/governanca/desativar.html | retirar de operação sem excluir histórico | form, aviso, confirmação | Inv + Gov | nenhum | DESATIVADA | default, focus, error, success | MEDIUM | YES | MEDIUM | DesativarCameraForm, serviço | preserva registro histórico |
| SCR-GOV-REACTIVATE-001 | Reativar câmera | GOVERNANCE | /cameras/<pk>/reativar/ | cameras:reativar | reativar_camera_view | cameras/templates/cameras/governanca/reativar.html | retornar câmera à operação | form, aviso, confirmação | Inv + Gov | nenhum | PRODUCAO, ESTOQUE, completude | default, focus, error, success | MEDIUM | YES | MEDIUM | ReativarCameraForm, completude | completude validada antes da reativação |
| SCR-GOV-SUBSTITUTE-001 | Substituir câmera | GOVERNANCE | /cameras/<pk>/substituir/ | cameras:substituir | substituir_camera_view | cameras/templates/cameras/governanca/substituir.html | transferir operação e preservar histórico | form longo, aviso, confirmação | Inv + Gov | nenhum | operação, substituição registrada | default, focus, error, success | HIGH | YES | HIGH | SubstituirCameraForm, serviço transacional, auditoria | dados físicos da substituta são preservados |
| SCR-SUB-LIST-001 | Substituições | SUBSTITUTIONS | /cameras/substituicoes/ | cameras:lista_substituicoes | lista_substituicoes | cameras/templates/cameras/substituicoes/lista.html | pesquisar histórico global | filtros, filtros ativos, tabela/cards, paginação | Gov | nenhum | registros de substituição, período inválido | default, selected, empty, error | HIGH | YES | HIGH | query GET, histórico de substituição | período inválido sinalizado |
| SCR-SUB-DETAIL-001 | Detalhe da substituição | SUBSTITUTIONS | /cameras/substituicoes/<pk>/ | cameras:detalhe_substituicao | detalhe_substituicao | cameras/templates/cameras/substituicoes/detalhe.html | consultar registro imutável | dados das duas câmeras e histórico | Gov | nenhum | câmera anterior e substituta | default | MEDIUM | YES | MEDIUM | SubstituicaoCamera | histórico sem edição/exclusão pela tela |
| SCR-SUB-CAMERA-001 | Substituições da câmera | SUBSTITUTIONS | /cameras/<camera_pk>/substituicoes/ | cameras:lista_substituicoes_camera | lista_substituicoes_camera | cameras/templates/cameras/substituicoes/lista_camera.html | consultar substituições relacionadas | registros, relações, paginação | Inv + Gov | nenhum | papel da câmera na substituição | default, empty | HIGH | YES | HIGH | SubstituicaoCamera, paginação | scoped por câmera |
| SCR-EVENT-LIST-001 | Eventos de auditoria | EVENTS_AUDIT | /eventos/ | eventos:lista | lista_eventos | cameras/templates/cameras/eventos/lista.html | filtrar e consultar auditoria | filtros, chips ativos, tabela, paginação | Ev | filtros.js | categoria e origem de evento | default, selected, empty, error | HIGH | YES | HIGH | filtros GET, EventoAuditoria | filtros por texto/categoria/origem/período |
| SCR-EVENT-DETAIL-001 | Detalhe do evento | EVENTS_AUDIT | /eventos/<pk>/ | eventos:detalhe | detalhe_evento | cameras/templates/cameras/eventos/detalhe.html | consultar um evento | cabeçalho, categoria, dados e relações | Ev | nenhum | categoria e origem de evento | default | MEDIUM | YES | MEDIUM | EventoAuditoria, câmera/usuário | somente leitura |
| SCR-EVENT-CAMERA-001 | Eventos da câmera | EVENTS_AUDIT | /cameras/<pk>/eventos/ | cameras:eventos_camera | eventos_camera | cameras/templates/cameras/eventos/camera.html | auditar eventos de uma câmera | tabela, vazio, paginação | Ev | nenhum | categoria e origem de evento | default, empty | HIGH | YES | MEDIUM | EventoAuditoria, câmera | usa filtros da lista global |
| SCR-ACCOUNT-PROFILE-001 | Perfil | PROFILE_ACCOUNT | /perfil/ | usuarios:perfil | perfil | usuarios/templates/usuarios/perfil.html | consultar conta e acesso | cards, dados, grupos, permissões, ações | Perfil | nenhum | ativa/inativa, grupos e permissões | default, empty | HIGH | YES | MEDIUM | auth, grupos, permissões | Admin aparece para staff |
| SCR-ACCOUNT-EDIT-001 | Editar perfil | PROFILE_ACCOUNT | /perfil/editar/ | usuarios:editar_perfil | editar_perfil | usuarios/templates/usuarios/editar_perfil.html | alterar dados pessoais/contato | forms, fieldsets, erros, ações | Perfil | nenhum | validação de dados | default, focus, error, success | HIGH | YES | MEDIUM | dados_form, perfil_form | username/cargo/setor somente leitura |
| SCR-ACCOUNT-PASSWORD-001 | Alterar senha | PROFILE_ACCOUNT | /perfil/alterar-senha/ | usuarios:alterar_senha | alterar_senha | usuarios/templates/usuarios/alterar_senha.html | trocar credencial | credenciais, erros e ações | Perfil | nenhum | validação de senha | default, focus, error, success | MEDIUM | YES | LOW | PasswordChangeForm | formulário nativo |
| SCR-AUTH-LOGIN-001 | Login ARGOS | AUTH | /login/ | usuarios:login | ArgosLoginView | usuarios/templates/usuarios/login.html | autenticar usuário | marca, campos, erro | Auth | nenhum | autenticação aceita/negada | default, focus, error | MEDIUM | YES | LOW | Django auth | composição isolada do base |
| SCR-ERROR-403-001 | Acesso negado | ERROR_PAGES | resposta 403 | — | PermissionDenied handler | core/templates/403.html | explicar falta de permissão | mensagem, botão voltar | Shell | nenhum | usuário sem permissão | default | LOW | YES | LOW | middleware/decorators, core:inicio | sem template 404/500 localizado |
| SCR-ADMIN-LOGIN-001 | Login Admin | ADMIN | /admin/login/ | admin:login | Django Admin | contrib.admin login template | autenticar administração | formulário Admin | Django Admin | nativo Django | autenticação staff | default, focus, error | MEDIUM | INHERITED | LOW | Django contrib.admin | escopo padrão herdado; sem redesenho customizado |
| SCR-ADMIN-INDEX-001 | Índice Admin | ADMIN | /admin/ | admin:index | Django Admin | contrib.admin index template | navegar modelos autorizados | grupos de modelos, links | Django Admin | nativo Django | permissões de modelo | default, focus | MEDIUM | INHERITED | MEDIUM | sete ModelAdmin próprios | gerado pelo Django |
| SCR-ADMIN-APP-001 | Lista de app Admin | ADMIN | /admin/<app_label>/ | admin:app_list | Django Admin | contrib.admin app_index template | navegar modelos de um app | links de modelos | Django Admin | nativo Django | permissões de modelo | default, focus, empty | MEDIUM | INHERITED | LOW | Django Admin | arquétipo gerado |
| SCR-ADMIN-CHANGE-LIST-001 | Changelist Admin | ADMIN | /admin/<app>/<model>/ | admin:<app>_<model>_changelist | ModelAdmin changelist | contrib.admin change_list template | localizar e administrar registros | tabela, filtros, busca, paginação, ações | Django Admin | nativo Django | estados/modelos e permissões | default, selected, empty | HIGH | INHERITED | HIGH | custom ModelAdmin | estrutura varia por modelo |
| SCR-ADMIN-FORM-001 | Formulário Admin | ADMIN | /admin/<app>/<model>/add/ e /change/<id>/ | admin:<app>_<model>_add / _change | ModelAdmin add/change | contrib.admin change_form template | criar ou editar registro | campos, validação, ações | Django Admin | nativo Django | campos e permissões do modelo | default, focus, error, success | HIGH | INHERITED | HIGH | custom ModelAdmin/forms | add e change contados como um arquétipo |
| SCR-ADMIN-HISTORY-001 | Histórico Admin | ADMIN | /admin/<app>/<model>/<id>/history/ | admin:<app>_<model>_history | ModelAdmin history | contrib.admin object_history template | consultar histórico administrativo | lista de alterações | Django Admin | nativo Django | histórico disponível | default, empty | MEDIUM | INHERITED | MEDIUM | histórico Django | arquétipo gerado |
| SCR-ADMIN-DELETE-001 | Confirmação Admin | ADMIN | /admin/<app>/<model>/<id>/delete/ | admin:<app>_<model>_delete | ModelAdmin delete | contrib.admin delete_confirmation template | confirmar exclusão autorizada | resumo e ações | Django Admin | nativo Django | confirmação e dependências | default, focus, error | MEDIUM | INHERITED | LOW | permissões e relações | arquétipo gerado |
| SCR-ADMIN-PASSWORD-001 | Troca de senha Admin | ADMIN | /admin/password_change/ | admin:password_change | Django Admin | contrib.admin password_change_form template | alterar senha na área Admin | campos e ações | Django Admin | nativo Django | validação de senha | default, focus, error, success | MEDIUM | INHERITED | MEDIUM | Django auth/Admin | arquétipo gerado |

### Totais calculados da matriz

- TOTAL_USER_FACING_SCREENS = 35
- TOTAL_FAMILIES = 15
- PROTOTYPE_REQUIRED_YES = 24
- PROTOTYPE_REQUIRED_INHERITED = 11
- PROTOTYPE_REQUIRED_NO = 0
- HIGH_COMPLEXITY_SCREENS = 12
- HIGH_RESPONSIVE_RELEVANCE_SCREENS = 20

YES significa protótipo próprio; INHERITED significa herdar visualmente um padrão de mesma família. Os oito arquétipos Admin herdam os templates nativos do Django; por padrão não terão redesenho customizado. Quick Detail é INHERITED / BASELINE_EXISTING e não tem redesenho autorizado.

## 11. Shared component inventory

| COMPONENT_NAME | CURRENT_IMPLEMENTATION | USED_BY | CURRENT_OWNER | REUSABLE | VISUAL_PROTOTYPE_REQUIRED |
|---|---|---|---|---|---|
| Application shell | base layout e includes | páginas ARGOS autenticadas | argos.css | sim | sim, uma composição compartilhada |
| Sidebar / navegação | partial HTML | shell | argos.css | sim | sim |
| Topbar / cabeçalho | partial HTML | shell | argos.css | sim | sim |
| Menu do usuário | details, links e form POST | shell | argos.css | sim | sim |
| Mensagens | partial Django messages | telas com feedback | argos.css | sim | sim |
| Brand | partial com marca/imagem | login | autenticacao.css | sim | herdado da marca aprovada |
| Botões e controles | HTML semântico/classes próprias | telas e formulários | design-system.css + owners locais | sim | sim, pelo Style Lab |
| Campo de formulário | partial field | câmera, atividade e perfil | design-system.css + owners locais | sim | sim |
| Resumo de erros | partial de validação | forms câmera, atividade e perfil | owners locais | sim | sim |
| Filtro multisseleção | details, summary e checkboxes | inventário/eventos | inventario.css/eventos.css | sim | sim |
| Filtros ativos | chips/links removíveis | inventário, eventos e substituições | owners de domínio | sim | sim |
| Tabela de dados | table semântica e wrappers | inventário, históricos, eventos e Admin | owners locais/Admin | sim | sim |
| Paginação | partial de links | listas paginadas | design-system.css + owners locais | sim | sim |
| Estado vazio | partial com texto e ação opcional | inventário, atividades e listas | owners locais | sim | sim |
| Card / KPI / módulo | elementos HTML de templates | portal e Dashboard | portal.css | sim | sim |
| Badges de câmera | três partials de domínio | inventário/detalhe/atividades | inventario.css | sim | sim |
| Governance action shell | partial de formulário/aviso/ação | quatro fluxos de governança | governanca.css | sim | sim |
| Thumbnail de câmera | img nativo e fallback JS | inventário | inventario.css | sim | sim |
| Quick Detail | dialog HTML nativo | inventário | inventario.css + camera-quick-detail.js | sim | INHERITED / baseline aprovada |
| Imagem de prévia | img nativo servido por endpoint | inventário/detalhe/Quick Detail | inventario.css | sim | sim, preservando contrato de estado |

Componentes marcados foram encontrados em templates/fontes, não inferidos como biblioteca completa. A implementação concreta de tokens e primitives permanece em design-system.css e no inventário de CSS abaixo.

## 12. CSS ownership map

Há oito folhas CSS próprias. O mapa desejado no master plan é comparado ao uso factual observado.

| CSS_FILE | OWNER / USO OBSERVADO |
|---|---|
| static/css/design-system.css | tokens/primitives compartilhados; carregado pelo base e pelo login |
| static/css/argos.css | shell e estrutura da aplicação; carregado globalmente |
| static/css/portal.css | portal e Dashboard; também carregado globalmente pelo base |
| static/css/inventario.css | inventário, detalhe, formulários, monitoramento e atividades |
| static/css/governanca.css | governança, substituições e também inventário/detalhe/formulário de câmera |
| static/css/eventos.css | listas/detalhes de auditoria e eventos por câmera |
| static/css/perfil.css | perfil, edição e senha |
| static/css/autenticacao.css | login ARGOS |

GLOBAL_CSS factual: design-system.css, argos.css, portal.css no base.html; login carrega design-system.css separadamente. PAGE_CSS e DOMAIN_CSS são as folhas locais dos templates. DESIGN_SYSTEM_DEPENDENCY: todas as páginas ARGOS, direta ou via base, exceto as páginas do Django Admin, cujo runtime tem seus próprios estilos.

Divergência factual: a arquitetura desejada do plano central destaca cinco owners (Design System, Argos shell, Portal/Dashboard, Inventory/Quick Detail e Governance). O checkout também tem eventos.css, perfil.css e autenticacao.css, e portal.css está global no shell. governance.css participa de páginas de inventário e formulário além das telas de governança. Este registro mapeia o uso, não propõe reorganização.

## 13. JavaScript / interaction map

Quatro scripts próprios foram encontrados; páginas sem script usam HTML nativo e processamento no servidor.

| JS_FILE | BEHAVIOR / PAGES | PROGRESSIVE_ENHANCEMENT / REQUIRES_JS | NATIVE_BROWSER_COMPONENT | ASYNC_REQUESTS | FOCUS / KEYBOARD / STATE |
|---|---|---|---|---|---|
| static/js/filtros.js | aprimora filtro multisseleção em inventário e eventos | aprimora details/checks e GET nativo; filtros continuam submetíveis sem script | details, summary, checkbox, form GET | não | fecha fora/Escape; um filtro aberto; estado de filtro preservado na query |
| static/js/camera-form.js | alterna campos farm/codec/retenção personalizados | interação customizada depende de JS | controles HTML/select/checkbox | não | foco para campo revelado |
| static/js/camera-thumbnails.js | esconde miniatura se load da imagem falhar e mostra indisponibilidade | img existe sem script; fallback visual aprimorado | img lazy | requisição nativa de imagem | sem gestão de foco |
| static/js/camera-quick-detail.js | abre dialog, busca dados, carrega imagem, anterior/próxima e fecha | dialog visual depende de JS | dialog nativo | fetch JSON e imagem | gerenciamento/restauração de foco; Escape e clique no backdrop |

Não foram encontrados scripts compartilhados em base.html. JS_FILE por tela está anotado na matriz; upload de imagem é POST servidor e a troca de página/feedback é HTML.

## 14. Visual state inventory

### Estados de domínio observados

- Situação operacional da câmera: PRODUCAO, ESTOQUE, DESATIVADA.
- Completude: completa/incompleta, derivada dos campos requeridos.
- Monitoramento: ONLINE, OFFLINE, UNKNOWN e OUT_OF_SCOPE; projeções também distinguem evidência stale.
- Indisponibilidade: registro aberto/fechado, origem e close_reason; recuperação aparece como razão de fechamento, não como enum separado RECOVERING.
- Imagem: AVAILABLE, NO_CAPTURE_AVAILABLE, UNAVAILABLE, ERROR.
- Endpoints: UNAUTHENTICATED, FORBIDDEN, METHOD_NOT_ALLOWED, INVALID_REQUEST/INVALID_VARIANT, NOT_FOUND/CAMERA_NOT_FOUND.
- Atividades, eventos e substituições: tipos/categorias/origens definidos pelos domínios; não foram inventados novos estados.

### Estados de interface que protótipos devem cobrir quando aplicáveis

DEFAULT, HOVER, FOCUS_VISIBLE, SELECTED, DISABLED, LOADING, EMPTY, ERROR e mensagens de sucesso. ONLINE/OFFLINE/UNKNOWN/OUT_OF_SCOPE, stale e estados de imagem são apresentados como estados de domínio; não devem ser confundidos com hover/seleção ou outros estados visuais. Os formulários expõem validação/erro e mensagens de sucesso por HTML/server-rendering.

## 15. Prototype requirement matrix

A coluna PROTOTYPE_REQUIRED da matriz é o inventário. Distribuição: YES 24; INHERITED 11; NO 0. Complexity: LOW, MEDIUM ou HIGH por tela. A contagem de complexidade HIGH é 12 e não expressa avaliação estética.

Quick Detail permanece PROTOTYPE_REQUIRED = INHERITED / BASELINE_EXISTING; VISUAL_BASELINE = APPROVED; REDESIGN_AUTHORIZED = NO. O baseline existente pode informar linguagem visual aprovada e não é proposta de redesign.

## 16. Responsive relevance matrix

A coluna RESPONSIVE_RELEVANCE na matriz contém a classificação por tela. Resultado: HIGH = 20 telas; MEDIUM e LOW são discriminados individualmente na matriz. A classificação decorre de tabelas, filtros, dashboard, dialog, cards, forms longos e shell, sem propor breakpoints.

## 17. Design-system dependency matrix

| FAMILY | PRIMITIVES / DEPENDÊNCIAS VISUAIS FACTUAIS |
|---|---|
| SHELL | layout, sidebar, navegação, topbar, mensagens, menu e botões |
| OTHER / portal | tipografia, espaçamento, cards de módulos, ícones e ações |
| DASHBOARD | cards/KPI, badges, botões, tipografia, tabelas/listas e espaçamento |
| INVENTORY | filtros, tabela, input, checkbox, badge, miniatura, paginação e dialog |
| CAMERA_DETAIL | cards/seções, definition lists, badges, imagem, ações, estados técnicos |
| CAMERA_FORMS | input, select, checkbox, validação, fieldsets/seções e barra de ações |
| MONITORING | tabela, estados de indisponibilidade, datas, paginação |
| ACTIVITIES | badge de tipo, lista/tabela, campos, estado vazio, paginação |
| GOVERNANCE | seções/form, aviso, validação, confirmação e ações |
| SUBSTITUTIONS | filtros, filtros ativos, tabelas/listas, histórico, paginação |
| EVENTS_AUDIT | filtro, tabela, categoria/origem, detalhe, paginação |
| PROFILE_ACCOUNT | cartões, dados de conta, grupos/permissões, forms e credenciais |
| AUTH | marca, controles de credencial, validação e botão |
| ERROR_PAGES | mensagem de erro, status e ação de retorno |
| ADMIN | templates e controles contrib.admin; customizações dos sete ModelAdmin |

A matriz registra dependências necessárias para o futuro Style Lab. Não escolhe aparência final nem altera tokens.

## 18. Known approved visual baselines

- Quick Detail: baseline visual APPROVED e PROTECTED conforme autoridades UI V2 e estado de continuidade. REDESIGN_AUTHORIZED = NO.
- Nenhuma outra baseline foi marcada neste censo como aprovada para redesenho. Screenshots de runtime não foram capturadas nesta atividade.

## 19. Findings

1. A stack factual coincide com Django SSR, Django Templates, HTML semântico, CSS próprio, JavaScript Vanilla, progressive enhancement, componentes nativos e Design System próprio.
2. PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE deve ser preservado como requisito para P1 e fases seguintes; não foi implementado neste P0.
3. 30 declarações de rota incluem o mount Admin; 29 handlers são rotas da aplicação. 24 rotas renderizam páginas HTML. Login é página; logout e upload são ações; Quick Detail é JSON e as duas rotas de preview retornam imagem.
4. 40 templates HTML de projeto: 23 páginas, 14 componentes, 2 fragmentos de formulário e 1 base layout.
5. O Admin expõe sete classes ModelAdmin próprias e foi inventariado em oito arquétipos nativos.
6. O checkout tem oito folhas CSS e quatro scripts. Há três folhas de domínio adicionais em relação à arquitetura desejada de cinco owners, e portal.css é globalmente importado.
7. O Quick Detail é composição de dialog dentro da lista de câmeras, usa endpoints JSON/imagem e continua baseline aprovada protegida.
8. Não há drawer separado nem template de projeto 404/500 localizado; o template 403 do projeto está presente.
9. HEAD local está 30 commits à frente e 0 atrás do upstream; a documentação PROJECT_STATE registra baseline mais antiga. Este documento reflete o checkout efetivamente inspecionado.

## 20. Risks

- A prototipação será baseada no checkout master em HEAD b35b7660..., que diverge 30 commits do origin/master; decisões de implementação devem manter esse baseline explícito.
- Folhas globais e de domínio se sobrepõem. Um futuro contrato visual deve respeitar o owner real e os guardrails CSS documentados antes de sugerir alteração.
- O Admin usa templates e CSS externos do Django; por padrão permanece rastreado como herdado, sem redesenho customizado. Ampliação do escopo visual exige autorização explícita.
- O censo é estático: não valida estados renderizados em runtime, dados reais, screenshots, viewport, acessibilidade executada ou comportamento em navegador.
- Os endpoints de imagem/JSON têm estados HTTP e autorização próprios; protótipos não devem tratá-los como páginas independentes.

## 21. Gaps / unknowns


- Capturar screenshots/referências factuais se P1 necessitar comparação runtime; nenhum screenshot foi criado aqui.
- Sem executar navegador, não foi validada a renderização de cada estado condicional.
- Não há handler/template de projeto 404/500 localizado; comportamento visual do framework nesses erros segue não documentado pelo projeto.
- A divergência entre o snapshot de continuidade anterior e o baseline do census foi registrada no checkpoint de fechamento da seção 29; valide Git diretamente para o estado atual.

## 22. Proposed P1 inputs

UI-V2-P1 — VISUAL STYLE LAB deverá receber:

- este Screen Census;
- Design System e semantic CSS tokens/primitives atuais;
- visual baselines aprovadas, preservando o Quick Detail;
- guardrails da arquitetura CSS e evidências de ownership;
- screenshots/referências factuais necessárias;
- lista de primitives necessárias;
- famílias prioritárias escolhidas pelo usuário;
- escopo Admin padrão: rastreado como herdado, sem redesenho customizado por padrão; qualquer ampliação requer autorização explícita;
- gate PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE.

Nenhuma atividade P1 foi iniciada.

## 23. Next activity

UI-V2-P1 — VISUAL STYLE LAB. Aguardar autorização explícita do usuário após revisão deste censo. STOP após P0.

## 24. Validation and final report

Comandos de validação solicitados após a criação: git diff --check; git diff --name-status; git diff --stat; git status --short --branch. O arquivo novo é untracked e, sem stage (não autorizado), comandos git diff comuns não o exibem; a conferência do conteúdo e do escopo deve incluir o status do arquivo não rastreado. Nenhum outro arquivo deve aparecer como alterado pela atividade.

| FIELD | RESULT |
|---|---|
| STATUS | PASS_WITH_FINDINGS |
| ACTIVITY_COMPLETION_PERCENT | 95% |
| COMPLETION_BASIS | inspeção e documento concluídos; fechamento formal depende do gate de continuidade |
| REPOSITORY_ROOT | C:/Users/walac/desenvolvimento/projeto_argos |
| BRANCH | master |
| BASELINE_HEAD | b35b766076ac62955be6bf52cdb4c5fdd5098780 |
| UPSTREAM | origin/master @ 47c6965f3a60c0026117584dae21ca8a280986a5 |
| DIVERGENCE | ahead 30 / behind 0 |
| READ_ONLY_SOURCE_INSPECTION | PASS |
| AUTHORITIES_INSPECTED | AGENTS, continuidade, políticas, plano, spec, roadmap, sprints, auditoria frontend e diretriz CSS |
| ROUTES_INSPECTED | 30 declarações: mount Admin + 29 rotas de aplicação |
| VIEWS_INSPECTED | 29 handlers roteados; sete ModelAdmin próprios |
| TEMPLATES_INSPECTED | 40 HTML do projeto: 23 PAGE, 14 COMPONENT, 2 FORM_FRAGMENT, 1 BASE_LAYOUT |
| CSS_FILES_INSPECTED | 8 |
| JS_FILES_INSPECTED | 4 |
| TOTAL_USER_FACING_SCREENS | 35 |
| TOTAL_FAMILIES | 15 |
| PROTOTYPE_REQUIRED_YES | 24 |
| PROTOTYPE_REQUIRED_INHERITED | 11 |
| PROTOTYPE_REQUIRED_NO | 0 |
| HIGH_COMPLEXITY_SCREENS | 12 |
| HIGH_RESPONSIVE_RELEVANCE_SCREENS | 20 |
| QUICK_DETAIL_BASELINE | APPROVED_PRESERVED |
| STACK_FIDELITY_REQUIREMENT | DOCUMENTED |
| SCREEN_CENSUS_DOCUMENT | docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md |
| ONLY_ALLOWED_FILE_CHANGED | YES; status contém somente este arquivo novo |
| DIFF_CHECK | PASS; git diff --check limpo e whitespace do arquivo novo validado |
| SOURCE_CODE_CHANGED | NO |
| CSS_CHANGED | NO |
| TEMPLATES_CHANGED | NO |
| JAVASCRIPT_CHANGED | NO |
| STAGE_PERFORMED | NO |
| COMMIT_PERFORMED | NO |
| PUSH_PERFORMED | NO |
| PROJECT_STATE_UPDATE | DEFERRED_NO_AUTHORITY; proibido pelo escopo P0 |
| ACTIVITY_COMPLETE | NO; gate AGENTS.md exige PROJECT_STATE_UPDATE = PASS antes do encerramento formal |
| FINDINGS | baseline Git do checkout difere do snapshot; 30 commits à frente; ADMIN exige decisão de escopo em P1 |
| GAPS | sem runtime screenshots; sem templates/handlers 404/500 próprios localizados |
| BLOCKERS | atualização de continuidade está fora de autoridade nesta atividade |
| NEXT_ACTIVITY | UI-V2-P1 — VISUAL STYLE LAB |
| FINAL_VERDICT | censo produzido; encerramento formal aguardará checkpoint de continuidade autorizado |

## 25. Checkpoint de fechamento — UI-V2-P0 (2026-09-27)

O checkpoint documental autorizado após a produção deste censo fechou
formalmente UI-V2-P0. A tabela da seção 24 registra o relatório original da inspeção; seus campos de conclusão e bloqueio descrevem o estado anterior a este checkpoint e são supersedidos por esta seção. As métricas e fatos de inspeção permanecem válidos. A métrica de 95% registra o estado
no fim da inspeção, antes da reconciliação de continuidade; o estado atual do
fechamento está registrado em PROJECT_STATE.md, seção 29.

```
UI-V2-P0 = CLOSED_PASS
ACTIVITY_COMPLETE = YES
PROJECT_STATE_UPDATE = PASS
SCREEN_CENSUS_AUTHORITY = docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md
ADMIN_UI_V2_SCOPE = TRACKED_AS_INHERITED / NO_CUSTOM_REDESIGN_BY_DEFAULT
QUICK_DETAIL_VISUAL_BASELINE = APPROVED / PROTECTED
BATCH_B_POST_INTEGRATION_VISUAL_GATE = PENDING_USER_REVIEW
PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE
NEXT_UI_ACTIVITY = UI-V2-P1 — VISUAL STYLE LAB
P1_STARTED = NO
P1_AUTHORIZED = NO
```

Esta decisão de planejamento sobre o Admin não altera as contagens nem a
classificação herdada das oito superfícies no census. O Quick Detail permanece
preservado; a aceitação visual de origem não substitui a revisão visual
pós-integração do Batch B.

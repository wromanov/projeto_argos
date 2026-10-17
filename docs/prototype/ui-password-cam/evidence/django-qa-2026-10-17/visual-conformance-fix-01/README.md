# ARGOS-CRED-UI-01 — correção visual

[Voltar ao índice histórico](../README.md)


Capturas da aplicação Django real em cópia descartável da base QA, com identidade e credencial inteiramente sintéticas. O clone foi removido depois da validação. Nenhum segredo aparece nas capturas ou neste índice.

Os nomes indicam o viewport CSS configurado no navegador. A imagem inclui a área de conteúdo do browser; a largura raster é alguns pixels menor por causa da barra de rolagem e da moldura do navegador.

## Viewports exigidos — credencial sintética ativa

| Viewport CSS | Captura | Resultado observado |
| --- | --- | --- |
| 390×844 | [Card mobile](ARGOS_CRED_UI_01_DJANGO_CARD_390x844.jpg) | Rede → Credenciais → Gravação; ações acessíveis na ordem Revelar, Revogar, Substituir; sem overflow horizontal. |
| 1366×768 | [Card 1366](ARGOS_CRED_UI_01_DJANGO_CARD_1366x768.jpg) | Card no ponto contratado; shell e Design System ARGOS da aplicação real. |
| 1440×900 | [Card 1440](ARGOS_CRED_UI_01_DJANGO_CARD_1440x900.jpg) | Card e ações em linha; sem overflow horizontal. |
| 1920×1080 | [Card 1920](ARGOS_CRED_UI_01_DJANGO_CARD_1920x1080.jpg) | Card e ações em linha; sem overflow horizontal. |

## Estados

- [Configurar — mobile](ARGOS_CRED_UI_01_DJANGO_DIALOG_CONFIGURE_390x844.jpg)
- [Substituir — desktop](ARGOS_CRED_UI_01_DJANGO_DIALOG_CONFIGURE_1440x900.jpg)
- [Revogar — desktop](ARGOS_CRED_UI_01_DJANGO_DIALOG_REVOKE_1440x900.jpg)
- [Alterações cadastrais não salvas](ARGOS_CRED_UI_01_DJANGO_DIRTY_DIALOG_1440x900.jpg)
- [Fallback SSR sem JavaScript](ARGOS_CRED_UI_01_DJANGO_NOJS_FALLBACK_1440x900.jpg)
- [Erro sanitizado de reautenticação no reveal](ARGOS_CRED_UI_01_DJANGO_REVEAL_ERROR_1440x900.jpg)
- [Configurar sem credencial ativa — mobile](../ARGOS_CRED_UI_01_DJANGO_CONFIGURE_EMPTY_390x844.jpg)
- [Foco de teclado visível — mobile](../ARGOS_CRED_UI_01_DJANGO_KEYBOARD_FOCUS_390x844.jpg)

## Verificações

- **Posição e ordem:** DOM efetivamente renderizado e árvore acessível indicam Rede → Credenciais → Gravação. As ações visuais e acessíveis seguem a V1: Revelar → Revogar → Substituir. No mobile elas empilham para manter alvos legíveis/tocáveis; desktop conserva a linha.
- **Estrutura HTML e payload:** zero forms aninhados e zero IDs duplicados. Formulário cadastral associado apenas aos campos de cadastro; formulários POST de substituir/revogar/reveal não incluem campos cadastrais. Labels resolvem corretamente. Nenhuma solicitação de credencial submete o cadastro.
- **Fallback SSR:** JavaScript foi desabilitado no navegador. Os formulários SSR de substituir e revogar permanecem visíveis e exigem confirmação explícita de que as alterações cadastrais foram salvas em separado ou podem ser descartadas. O formulário SSR foi submetido na cópia e o fluxo PRG confirmou sucesso. Não se alegou detecção dinâmica de dirty state sem JavaScript. O reveal informa que requer JavaScript e não imprime a resposta JSON.
- **Dirty state com JavaScript:** uma edição local em Terminal abriu o aviso antes de uma ação de credenciais. “Voltar ao cadastro” preservou o valor não salvo; “Descartar e continuar” restaurou o valor persistido e abriu a ação pendente.
- **Diálogos e teclado:** foco inicial vai ao primeiro campo; Tab percorre usuário → senha → confirmação; Escape fecha e devolve foco ao acionador. Foco visível usa outline de 3 px. O diálogo usa o mecanismo nativo do browser e não aparece no HTML como aberto sem JavaScript.
- **Contraste observado:** texto secundário 4,71:1; badge 7,36:1; texto do botão primário 6,15:1; texto do botão secundário 14,15:1, calculados sobre as cores computadas no estado mostrado. Status inclui texto, não depende apenas de cor. A auditoria de leitor de tela não foi executada.
- **Reveal protegido:** o endpoint existente permaneceu POST + CSRF + permissão + reautenticação + no-store + auditoria sanitizada. Erro de senha inválida foi sanitizado e nenhum segredo ficou visível na captura. O teste de falha/rollback da auditoria consta da evidência canônica do Gate B; este checkpoint visual não repete nem amplia essa alegação.
- **Persistência e concorrência:** validação da cópia confirmou cadastro preservado em operações independentes, ponteiro ativo consistente, versão anterior aposentada e auditoria sem valores secretos. POST repetido, double submit e concorrência mantêm a política documentada no contrato canônico: PRG/bloqueio visual não provam idempotência; replace repetido pode gerar nova versão/evento, revoke repetido responde conflito; não houve stress concorrente PostgreSQL.
- **Redução de movimento:** a regra existente `prefers-reduced-motion: reduce` remove transições dos controles aplicáveis.
- **Baseline:** protótipo V1 permaneceu intacto (SHA-256 `69be00debc4bed45dfbe73d4702ad33faa2db4bad34b2df9f640ed0f780e1e1d`). Não foram importados shell ou controles demonstrativos do protótipo.

## Estado do gate

`HTML_FORM_STRUCTURE_VALIDATED = PASS` · `NO_JS_FALLBACK_VALIDATED = PASS` · `DIRTY_FORM_BEHAVIOR = PASS` · `REVEAL_REGRESSION = PASS` · `DJANGO_VISUAL_CONFORMANCE = PASS`.

`DJANGO_HUMAN_VISUAL_APPROVAL = PASS`: o usuário aprovou as evidências em 2026-10-17. Gate D concluído; E2 continua bloqueado e exige decisão separada. Veja `PROJECT_STATE.md` §136 e `AGENT_CONTINUITY.md` §20.94.

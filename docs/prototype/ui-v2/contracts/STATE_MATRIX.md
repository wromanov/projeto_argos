# ARGOS UI V2 — State Matrix

Fonte factual: Screen Census, documentação funcional, models e serviços atuais. A matriz define tratamento visual; não cria enum, transição, permissão ou ação.

| DOMAIN / UI STATE | SOURCE / SEMANTICS | VISUAL TREATMENT P2 | TEXT / ICON | ACTIONS | LOADING / ERROR |
|---|---|---|---|---|---|
| ONLINE | estado técnico monitorado já existente | success: foreground #145E42 sobre surface #DFF3E8 | texto Online; cor nunca é único canal; sem novo ícone | ações atuais da tela e permissões | não muda a semântica de carregamento |
| OFFLINE | estado técnico monitorado já existente | danger: foreground #922C3E sobre surface #F9E5E8 | texto Offline; sem novo ícone | ações atuais da tela e permissões | erro de requisição permanece separado |
| UNKNOWN | estado estável do monitoramento | neutral #1D4F86 sobre #E8F2FA | texto Desconhecido | nenhuma ação inferida | falha da requisição é estado da interface |
| OUT_OF_SCOPE | projeção de escopo no Screen Census; serviço também expõe em_escopo como boolean separado | neutral; não representar como OFFLINE; Camera Detail usa Opção A aprovada: badge técnico sem texto auxiliar e contexto somente no campo Escopo | badge “NÃO MONITORADA”; “Fora do escopo” permanece visível em Escopo | não inferir ação | independente de loading/error |
| STALE | projeção de frescor, não estado técnico estável | warning #80500B sobre #FFF0D7 | texto de dados desfasados e, quando existente, idade da atualização | ações atuais | recuperar frescor não altera condição de domínio |
| PRODUCAO / ESTOQUE / DESATIVADA | Camera.SituacaoOperacional | badge neutral ou contexto explicitamente definido pela tela; não equivale a saúde técnica | texto de situação operacional | ações autorizadas pelo domínio | independente de loading/error |
| COMPLETO / INCOMPLETO | completude calculada a partir de campos requeridos | success / warning como apresentação de completude | texto Cadastro completo / incompleto | ações seguem validação do domínio | erros de formulário não alteram enum operacional |
| INDISPONIBILIDADE ABERTA / FECHADA | incidente possui open/closed, origin e close_reason | manter texto explícito; usar tratamento neutro sem inferir recuperação como novo estado | texto de incidente, origem e motivo; nenhum ícone novo | ações seguem permissões e fluxo atual | não criar enum RECOVERING |
| Captura: AVAILABLE / NO_CAPTURE_AVAILABLE / UNAVAILABLE / ERROR | LatestCameraCaptureStatus | disponível success; ausência/unavailable neutral; erro usa Error State | texto explícito; sem inferir inexistência da câmera | nenhuma ação inferida | IMAGE_LOADING é estado de interface, se o componente o usar |
| Exibição: AVAILABLE / NO_IMAGE_AVAILABLE / UNAVAILABLE / ERROR | DisplayImageState, conforme serviço atual | mesma semântica visual da captura, preservando o nome do estado da API/código | texto específico de exibição; sem unificar nomes | nenhuma ação inferida | feedback de falha da requisição é separado |
| Preview: AVAILABLE / NO_CAPTURE_AVAILABLE / UNAVAILABLE / ERROR | PreviewState, conforme serviço atual | mesma apresentação sem alterar o nome do contrato consumido | texto específico da prévia | nenhuma ação inferida | carregamento só enquanto a requisição estiver ativa |
| DEFAULT / HOVER / FOCUS_VISIBLE / SELECTED / DISABLED | interação visual | estilos de componente; focus-visible com contorno 3px e offset 2px | rótulo semântico do controle permanece | disabled não sugere que a ação foi executada | independente do domínio |
| LOADING / EMPTY / ERROR / SUCCESS | estado de interface ou mensagem | spinner com texto; Empty State; Error State; confirmação preserva texto de origem | não inventar estados de domínio nem usar cor como único canal | ação disponível só se contrato atual permite | reduced motion remove animação do spinner |

## Divergência documental de origem

O Screen Census usa NO_CAPTURE_AVAILABLE para estado de imagem, enquanto o serviço DisplayImageState usa NO_IMAGE_AVAILABLE; PreviewState usa NO_CAPTURE_AVAILABLE. Esta divergência de vocabulário é preservada por consumidor e origem. P2 não escolhe um nome canônico de domínio e não altera runtime. Os contratos de cada serviço continuam sob authority funcional.

A fonte técnica também distingue SituacaoOperacional (PRODUCAO, ESTOQUE, DESATIVADA), status técnico ONLINE/OFFLINE e escopo em_escopo. Não os combinar numa badge genérica. Recuperação aparece como close_reason de um incidente fechado, não como enum RECOVERING.

### Cores do fallback informativo

A paleta de informação da especificação anterior fica disponível somente como fallback quando já houver mensagem informativa: foreground #3B82C4 sobre #E3F0FA. Não criar status INFO no domínio.

# ARGOS-CRED-UI-01 — handoff de prototipação visual (DRAFT)

```text
STATUS = DRAFT / FOR UI-UX REVIEW
HTTP_CONTRACT = DRAFT / HUMAN_APPROVAL_PENDING
PROTOTYPE_MODE = INDEPENDENT HTML + CSS + VANILLA JS (OPTIONAL)
MOCK_STATES = DEMONSTRATIONS_ONLY / NOT_REAL_HTTP_INTEGRATION
DJANGO_IMPLEMENTATION = NOT_STARTED
```

Este handoff fornece limites funcionais e visuais para prototipar a gestão de credenciais junto à edição de câmera. Não é especificação final nem autorização de implementação. Não utilizar credencial operacional real. Qualquer dado usado no protótipo deve ser sintético e não secreto.

## 1. Propósito funcional

Explorar uma experiência SSR para consultar estado mínimo de configuração, substituir ou revogar credencial e solicitar reveal explícito/reautenticado pela rota existente. A pessoa consultora propõe visual e interação; não decide permissões, semântica de domínio ou contrato técnico.

## 2. Estrutura existente da edição de câmera

A tela atual é `editar_camera`, rota `/<pk>/editar/`, template `cameras/templates/cameras/formulario.html`, baseada em `CameraEdicaoForm`; stylesheet identificado `static/css/ui-v2/camera-form.css`. Preservar estrutura, campos, ordem e regiões protegidas da tela cadastrada. O protótipo deve mostrar manager como seção irmã, não dentro do formulário da Camera.

## 3. Operações suportadas

- GET existente da edição: metadata condicionado a `view_camera_credential` e `change_camera`.
- POST replace proposto `/<camera_id>/credentials/`, `replace_camera_credential`, `change_camera_credential`; campos username/password.
- POST revoke proposto `/<camera_id>/credentials/revoke/`, `revoke_camera_credential`, sem payload.
- Reveal existente `POST /<camera_id>/credentials/reveal/`, `reveal_camera_credential`; confirmação da senha atual por requisição e exibição apenas transitória.

Replace e revoke são `NOT_IMPLEMENTED`. Metadata SSR e esta composição também não afirmam integração realizada. Reveal é o único endpoint HTTP existente.

## 4. Matriz de usuários/permissões

| Papel/capacidade | Interface proposta |
|---|---|
| Sem `change_camera` | GET da edição negado 403. |
| `change_camera`, sem `view_camera_credential` | Edita cadastro conforme permissão; não recebe painel nem estado de credential. |
| `view_camera_credential` | Pode ver somente projeção mínima autorizada; não pode alterar/revogar/revelar sem permissões próprias. |
| `change_camera_credential` | Pode replace/revoke via POST CSRF; permissão é revalidada no servidor. |
| `reveal_camera_credential` | Pode acionar reveal explícito via POST CSRF e reautenticação a cada requisição. |
| Técnico/Admin | Defaults indicados por BC-AUTH; sempre respeitar permissões efetivas Django, não inferir pelo rótulo do papel. |

Não usar esconder/desabilitar botão como enforcement. Estado de erro não deve confirmar existência de credencial a ator sem permissão.

## 5. Dados seguros visíveis

Proposta inicial de metadata: apenas estado booleano/genérico ativo configurado. Não distinguir revogada de nunca configurada. Gaps atuais impedem aprovação final dessa projeção: o service devolve também username, `key_version`, versão e timestamp e não separa estado revogado.

## 6. Dados proibidos

Não colocar segredo, username, ciphertext, chave, versão, `key_version`, senha ou valor operacional em HTML de carga inicial, hidden fields, atributos `data-*`, URL, fixtures, logs ou armazenamento browser-side. Reveal pode apresentar username/password apenas depois da ação explícita autorizada, por tempo de tela limitado e sem persistência; o protótipo deve usar placeholders fictícios, claramente identificados.

## 7. Estados e transições

Mostrar estados de: painel oculto por permissão; configuração ativa; nenhum estado ativo/desconhecido (sem afirmar revogada); loading; sucesso replace; erro de validação; proibido 403; recurso indisponível 404; conflito 409 para revoke stale state; indisponibilidade operacional; confirmação de revoke; formulário Camera com mudanças não salvas; reveal aguardando senha atual; reveal transitório.

Mock de estado e fluxo é permitido, mas cada tela, badge, payload fictício e transição simulada deve ser rotulado de forma visível como **DEMONSTRAÇÃO — MOCK; sem integração HTTP real**. Não simular credencial real nem sugerir persistência real.

## 8. Feedback e mensagens

Usar mensagens genéricas e seguras: sucesso de alteração/revogação; validação sem repetir senha; acesso negado; estado mudou/atualize; serviço temporariamente indisponível; confirmação antes de revogar; confirmação de formulário não salvo. Não exibir exceção, detalhe de chave, stack, existência de credencial para usuário não autorizado ou payload. Textos finais aguardam review do contrato.

## 9. Tratamento de formulário cadastral não salvo

Antes de replace, revoke ou reveal, avisar se o formulário cadastral estiver dirty; orientar salvar ou descartar explicitamente, sem perda silenciosa. Prototipar também fluxo sem JavaScript como navegação/submit convencional com confirmação.

## 10. Independência dos formulários

Usar formulários irmãos, nunca nested forms. Submit de credential não submete nem salva campos de `CameraEdicaoForm`. Botões concorrentes podem ser temporariamente bloqueados visualmente, mas não alegar idempotência de servidor.

## 11. Ações autorizadas e restrições

Ações autorizadas para explorar: preencher username/password para substituição; confirmação explícita e POST de revoke; reautenticação e reveal explícito; navegação da edição já existente. Não incluir criar câmeras, modificar conexão/URI, testar câmera, administrar segredo operacional, restaurar versões revogadas ou configurar chave/provider. Nenhuma ação mock deve chamar endpoint real.

## 12. Componentes existentes do Design System

Referenciar foundation visual UI V2 aprovado e componentes registrados em `ARGOS_UI_V2_VISUAL_CONTRACT.md`, `COMPONENT_CATALOG.md`, `STATE_MATRIX.md`: Page/Section Header, Card, Button, Input, Alert, Loading/Error State. Usar namespace ARGOS existente no protótipo conforme convenções do catálogo. Direção visual C — ARGOS HYBRID permanece aprovada; Quick Detail e áreas protegidas permanecem intocados.

## 13. Fronteiras HTML/CSS

Prototipar em arquivos independentes HTML/CSS e vanilla JS se necessário, sem alterar templates, código Django ou CSS global. `camera-form.css` é referência contextual, não autorização para editá-lo. Não incorporar protótipo na produção nem criar API de mock que possa ser confundida com backend.

## 14. Expectativas responsivas

Apresentar layouts desktop, tablet e mobile; manter campos fluidos, ações com quebra/empilhamento e targets de toque de pelo menos 44px conforme catálogo.

## 15. Teclado e acessibilidade

Garantir ordem de tab previsível, labels associados, foco visível, confirmação acessível, status com texto além de cor, erros associados ao campo, mensagens anunciáveis e suporte a teclado sem depender de hover. Considerar reduced motion. Isso é critério de protótipo, não declaração de conformidade WCAG.

## 16. Regiões existentes protegidas

Preservar formulário e composição cadastral atual, estrutura do cabeçalho, navegação e áreas protegidas do UI V2; não redesenhar Quick Detail nem outras telas. Não modificar CSS global/tokens/componentes. A composição final e quaisquer mudanças da tela existente dependem da revisão visual humana.

## 17. Cenários para prototipar

1. Técnico autorizado abre edição com credencial ativa e vê estado genérico mínimo.
2. Usuário sem metadata vê edição sem painel.
3. Usuário sem permissão direta tenta ação e recebe mock 403 genérico.
4. Substituição válida demonstra loading e redirect/sucesso genérico.
5. Validação de username/password falha sem refletir senha.
6. Replace duplicado mostra que a UI não promete deduplicação.
7. Revogação abre confirmação, conclui e retorna status genérico.
8. Revogação em estado stale apresenta conflito e pedido de atualização.
9. Serviço indisponível mostra feedback seguro.
10. Formulário Camera dirty alerta antes de gestão/reveal.
11. Reveal exige senha atual em fluxo explícito e remove valor mostrado após tempo/fechamento.
12. Layout estreito, navegação apenas teclado e mensagens de erro/acessibilidade.

Todos esses cenários são mocks; não provam requests, permissões reais, auditoria nem persistência.

## 18. Revisão e aprovação

Revisar fidelidade à tela de edição, separação de formulários, estados e permissões, clareza de mock, segurança de conteúdo, responsividade, teclado e aderência ao Design System. A aprovação visual humana permanece `PENDING`. HTTP contract final permanece `PENDING_USER`; nenhuma aprovação do protótipo autoriza por si a implementação Django.

## 19. Questões abertas

- Deve username ser mostrado a Técnico/Admin? Recomendação adjudicada: omitir por padrão, decisão humana pendente.
- Será necessária distinção visual entre revogada e nunca configurada? Hoje a fonte não suporta; qualquer diferenciação requer fechamento contratual e possível mudança de serviço.
- Texto e fluxo final de confirmação de revoke e aviso de formulário dirty.
- Status final e apresentação dos erros operacionais.
- Fluxo exato de reveal transitório e acessível, mantendo endpoint atual.
- Fechamento do gap de atomicidade auditoria/mutação.

## 20. Referências

- Contrato técnico relacionado: `docs/projeto/contracts/backend/camera/ARGOS-CRED-UI-01_HTTP_SSR_INTEGRATION_CONTRACT_DRAFT.md`
- `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md`; `CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`; `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md`
- `cameras/views.py`; `cameras/urls.py`; `cameras/credential_views.py`; `cameras/integracao/credentials.py`
- `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`; `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md`; `COMPONENT_CATALOG.md`; `STATE_MATRIX.md`
- `docs/projeto/ARGOS_DELIVERY_EXECUTION_PLAN_V1.md`; `docs/projeto/ROADMAP_ARGOS_V5.md` §25; `docs/projeto/SPRINTS_ARGOS_V5.md` §22

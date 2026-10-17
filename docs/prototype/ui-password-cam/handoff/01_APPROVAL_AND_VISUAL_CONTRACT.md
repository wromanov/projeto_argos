# ARGOS-CRED-UI-01 — Contrato visual V1 e registro de aprovação

**Projeto:** `projeto_argos`
**Etapa:** E1 — Credenciais por câmera
**Referência:** `prototype/ARGOS_CRED_UI_01_PROTOTIPO_V1.html`
**Aprovação humana:** `PASS — V1, ALTERNATIVA A`
**Método selecionado:** `CARD_IN_EDIT_CAMERA + NATIVE_DIALOG`
**Alternativa B:** `NOT_SELECTED / REFERENCE_ONLY`
**Estado do contrato HTTP:** `DRAFT / HUMAN_APPROVAL_PENDING`
**Integração Django:** `NOT_STARTED / NOT_AUTHORIZED_BY_THIS_APPROVAL`

## 1. Decisão humana

O usuário aprovou expressamente a alternativa **A — card integrado à página Editar câmera e diálogo nativo para gerenciamento de credenciais**. Esta aprovação encerra a escolha de composição visual para a E1, no escopo do protótipo V1. O HTML aprovado é a **autoridade visual** para a nova seção, não fonte de implementação do backend e nem substituto dos contratos CAM-INT-02, CAM-INT-02-R1, BC-AUTH.

A alternativa B (formulário expansível) permanece dentro do arquivo HTML para fins de comparação histórica, **não autorizada como padrão de implementação**. Os controles “Demonstração — mock”, seletor de alternativas e seletor de cenários são exclusivamente laboratoriais; **não devem aparecer na aplicação produtiva**.

## 2. Localização e arquitetura visual aprovadas

- **Página:** Editar câmera (`editar_camera`, template `cameras/templates/cameras/formulario.html`).
- **Ponto de inserção:** **entre os cards Rede e Gravação**, acompanhando largura, ordem e respiro da pilha existente.
- **Seção:** “Credenciais de acesso”, card de superfície neutra e borda discreta, com cabeçalho/título/descrição coerentes com ARGOS Hybrid.
- **Visualização resumida:** símbolo discreto, informação mínima de estado de configuração, descrição concisa e ações condicionadas às permissões.
- **Operação principal:** Configurar ou Substituir credencial, em **`<dialog>` nativo** independente.
- **Ações secundárias:** Revogar e Revelar somente quando os contratos funcionais e permissões confirmarem disponibilidade; ações separadas com confirmação/reautenticação.
- **Diálogo:** cabeçalho, texto objetivo, campos vazios para novo username e password, aviso contextual, rodapé com Cancelar e Confirmação. Fechar restaura foco; Escape/cancelamento não persiste nada.
- **Responsividade:** manter agrupamentos compactos; campos fluidos e ações acessíveis em mobile; diálogo utilizável sem overflow horizontal.
- **Estética:** ARGOS Hybrid — enterprise operational, tipografia hierárquica, bordas sutis, baixo ruído; evitar enfeites, cards duplicados, excessos e sombras decorativas.

## 3. Restrições visuais de integração

`SIDEBAR = LOCKED`
`TOPBAR = LOCKED`
`EXISTING_CAMERA_FORM = PRESERVED`
`QUICK_DETAIL = LOCKED`
`DASHBOARD_V7 = PROTECTED`
`OTHER_SCREENS = PROTECTED`

Não redesenhar a tela Editar câmera; apenas incorporar a seção ao layout aprovado. **Não copiar** o shell desenhado no HTML de demonstração para o Django. Não importar CSS global do protótipo nem alterar tokens globais. Usar o Design System canônico e CSS de escopo local.

## 4. Segurança refletida no desenho

- Status “Configurada” significa apenas configuração ativa, **não autenticação validada ou conexão testada**.
- Sem credencial ativa é um estado genérico; **não distinguir “nunca configurada” de “revogada”** sem suporte contratual.
- Não exibir username armazenado no resumo padrão, nem senha, chaves, versões ou cifrados.
- Não preencher senha existente com máscara falsa (`******`).
- Novos campos username/password devem iniciar vazios e ser reintroduzidos na substituição.
- Mostrar/ocultar a **nova senha digitada** não autoriza revelar a senha armazenada.
- Reveal somente mediante autorização e **reautenticação por solicitação**, com resultado transitório e sem persistência.
- Não mostrar painel para quem não dispõe da permissão de metadata, sem permitir inferências sobre existência de credencial.
- Dados e mensagens do mock **não são evidência de endpoints implementados**.

## 5. O que a aprovação não autoriza

- Implementar endpoints HTTP propostos sem adjudicar as pendências do contrato DRAFT.
- Modificar criptografia, resolver, modelos, migrations, services MON ou matriz de autorização por conveniência visual.
- Exibir username ou segredos armazenados na página comum.
- Fazer deploy, utilizar câmera/credencial real, ou promover o protótipo diretamente para templates produtivos.
- Declarar a E1 operacionalmente homologada ou iniciar E2.

## 6. Congelamento

`VISUAL_BASELINE = ARGOS-CRED-UI-01_V1_OPTION_A`
`VISUAL_APPROVAL = PASS`
`IMPLEMENTATION_READINESS = CONDITIONAL_ON_HTTP_CONTRACT`
`DJANGO_VISUAL_ACCEPTANCE = PENDING`

Alterações visuais materiais após o aceite exigem novo finding e aprovação humana. Ajustes técnicos necessários para fidelidade Django devem ser demonstrados com comparação de telas.

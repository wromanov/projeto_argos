# ARGOS — E3/E4 | Contrato visual proposto para Operações de Imagem

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
RELATED_FUTURE_STAGE = E4 / IMG-06
ACTIVITY = ARGOS-E3-IMAGE-OPERATIONS-UI-PROTOTYPE
DOCUMENT = ARGOS_E3_IMAGE_OPERATIONS_VISUAL_CONTRACT_DRAFT.md
STATUS = DRAFT / PENDING_HUMAN_VISUAL_APPROVAL
RECOMMENDED_ALTERNATIVE = B / CAPTURE_BUTTON_PLUS_VISIBLE_GALLERY_ACTION
PROTOTYPE = ARGOS_E3_IMAGE_OPERATIONS_PROTOTYPE_V1.html
DJANGO_IMPLEMENTATION = NOT_AUTHORIZED
E4_IMPLEMENTATION = NOT_AUTHORIZED
```

## 1. Base de análise e fronteira do trabalho

Referência visual: captura atual da seção **Operações complementares** da página de detalhes completos da câmera, fornecida pelo usuário em 17/10/2026. A região existente é uma seção aberta, separada por divisor superior, contendo a operação **Enviar imagem manualmente**, texto explicativo, seletor nativo de arquivo e botão primário **Enviar imagem**. Há uma área livre à direita. A marcação vermelha na captura é uma anotação de inspeção e **não é um componente do ARGOS**.

As referências de domínio já fornecidas são `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` (§26: até três imagens ativas na apresentação de Camera Detail; ordenação de galeria `recorded_at ASC, immutable_id ASC`), `IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` (captura explícita em job assíncrono, permissões, processamento separado do monitoramento) e as autoridades vigentes de UI V2/ARGOS Hybrid. Este documento **não** autoriza mudanças em models, rotas, fila, worker, endpoints, permissões ou modelos de imagem. Os detalhes de implementação E3 devem ser reconciliados com os contratos técnicos pelo agente principal.

**Observação de fidelidade:** a referência fornecida é screenshot, não o CSS computado, nem o código atual da tela. Os valores abaixo são especificações visuais candidatas com base na captura; o agente deve mapear para tokens e componentes canônicos reais na integração. A sidebar, topbar, seções anteriores, histórico e footer representados no HTML independente são **contexto ilustrativo, não alterações autorizadas**.

## 2. Diagnóstico visual da seção atual

**Pontos fortes:** o título é discreto e integrado ao fluxo da página; o formulário de upload é conhecido e operacional; o `input type=file` nativo reduz complexidade; o botão azul identifica a confirmação da operação; a superfície neutra mantém a linguagem enterprise operacional.

**Problemas/oportunidades:** há grande espaço horizontal à direita da operação; não existe affordance para captura direta; captura e upload são ações conceitualmente diferentes e não devem compartilhar um único input/submit; o estado de processamento assíncrono ainda não está representado; a futura consulta E4 precisa ser encontrável, mas sem aparentar já estar disponível na E3.

**Direção:** preservar a seção aberta, dividir o conteúdo em **duas zonas operacionais irmãs** e utilizar uma divisória neutra interna, sem cartões novos, sombras, faixas coloridas ou painel vazio. Na quebra para telas menores, empilhar as zonas e substituir a divisória vertical por horizontal.

## 3. Alternativas comparadas

| Critério | A — Capturar + menu `⋯` | B — Capturar + `Ver imagens` |
|---|---|---|
| Descoberta da visualização | Inferior: ação escondida | Superior: ação legível |
| Densidade | Pouco mais compacta | Compacta, sem sobrecarga |
| Teclado/acessibilidade | Exige menu, Escape, foco e ARIA | Botão/link secundário direto |
| Escalabilidade | Melhor se surgirem várias ações autorizadas | Melhor com uma única ação secundária |
| Clareza E3 versus E4 | Requer abrir menu | Distinção direta, com rótulo E4 no laboratório |
| Risco de menu vazio/inócuo na E3 | Maior | Menor |

**Recomendação:** **Alternativa B**, porque uma única ação secundária não justifica um menu de overflow. O botão de captura é a ação explícita da E3; `Ver imagens` é um comando secundário condicionado à E4. Não inserir um botão E4 ativo nem um menu inerte na produção E3. A alternativa A permanece explorável no HTML, mas não é a composição recomendada.

## 4. Geometria e composição visual proposta

- `CONTENT_WIDTH_TARGET`: preservar exatamente o contêiner principal do Camera Detail. No HTML independente, referência visual `max-width: 1120px`, somente para demonstração.
- `SECTION`: reaproveitar **Operações complementares**, sem cartão/superfície adicional ao redor.
- `SECTION_TOP_DIVIDER`: borda neutral 1px, conforme o padrão existente.
- `SECTION_TITLE`: manter posição, peso e tonalidade do título atual.
- `DESKTOP_LAYOUT`: duas zonas lado a lado, aproximadamente `1.45fr 1fr`, com divisória vertical interna na zona de captura e `22px` de separação visual. A proporção final deve respeitar os controles reais e evitar compressão do file input.
- `UPLOAD_ZONE`: manter rótulo **Enviar imagem manualmente**, explicação vigente, label **Imagem**, input nativo e botão **Enviar imagem**. Não alterar semântica nem o endpoint existente.
- `CAPTURE_ZONE`: título **Captura direta da câmera**; texto de apoio curto; botão azul **Capturar imagem** com ícone de câmera; zona para feedback do job sem deslocamentos excessivos.
- `E4_ACTION`: somente após E4 aprovada/implementada, botão secundário explícito **Ver imagens**, adjacente ao botão de captura, com superfície neutra, ícone de imagens e nome acessível. O badge **E4** no protótipo é etiqueta de laboratório, não elemento produtivo obrigatório.
- `DIVIDERS`: mesma cor e espessura dos divisores locais. Não criar caixas individuais nem bordas decorativas.
- `SPACING_REFERENCE`: título da seção até conteúdo ~12–14px; título da operação até descrição ~5–7px; descrição até ações ~10px; gap entre ações ~7–8px; feedback abaixo das ações ~10–12px. Converter para tokens do Design System quando possível.
- `COLORS`: somente cores semânticas e tokens já existentes: primário azul para ação autorizada, secundário neutro, sucesso verde, falha vermelha e advertência âmbar **apenas para feedback**.
- `TYPE`: seguir fonte e hierarquia tipográfica do ARGOS, sem introduzir novas fontes, sombras ou padrões globais.

### Breakpoints a validar na aplicação real

- **Desktop amplo** (ex.: 1920/2048): duas zonas lado a lado, aproveitamento da área livre.
- **Notebook** (1366 e 1440): layout lado a lado somente enquanto o upload e a captura tiverem larguras confortáveis; a zona do upload pode colocar texto acima do seletor.
- **Tablet/estreito** (proposta: `<= 860px` de viewport no HTML): empilhar operações; divisória interna horizontal; manter upload antes da captura.
- **Mobile** (390×844; verificar 320px): ações fluidas, file input legível, alvos de toque preferencialmente ≥ 44px nos controles produtivos quando o catálogo assim exigir, menus não cortados, ausência de overflow horizontal e feedback lido após as ações.
- Não forçar largura fixa nem modificar o shell protegido para encaixar a seção.

## 5. Regras de operação E3

**Ação:** `Capturar imagem` é explícita e separada do upload manual. O ato de clicar pode criar *solicitação* de captura, não significa que a imagem já exista. O backend futuro deve confirmar elegibilidade/capability, perfil, permissão (`cameras.capture_camera_image`), estado do job e integridade. O frontend não determina permissões nem instancia conexões ao dispositivo.

**Estados de interface candidatos:**

| Estado | Tratamento visual | Observação |
|---|---|---|
| `IDLE` | Ação disponível se servidor confirmar autorização e elegibilidade | Ausência de evidência de elegibilidade não deve ser convertida em pronto operacional |
| `QUEUED` | “Solicitação registrada” / “Aguardando processamento” | Ainda não há resultado ou imagem nova |
| `RUNNING` | “Captura em processamento” | Não anunciar sucesso |
| `SUCCEEDED` | “Captura concluída” | Somente após resultado verdadeiro de job no Django; eventuais previews são outra decisão |
| `FAILED` | “Não foi possível capturar a imagem” | Erro público sanitizado; monitoramento permanece independente |
| `CANCELLED` | Mensagem de cancelamento quando o contrato habilitar este estado na UI | Não acrescentar ação cancelar sem contrato HTTP |
| `UNAVAILABLE / INELIGIBLE` | Controle indisponível e mensagem explicativa, quando informação puder ser exposta | Não presumir câmera online ⇒ capturável |
| `PERMISSION_DENIED` | Não renderizar ação não autorizada e proteger endpoint no backend | Estado de QA pode ser simulado sem inferir dados privados |

**Feedback:** usar `role=status`/`aria-live=polite` para transições ordinárias; erros acessíveis com texto e sem depender apenas de cor. Evitar um banner permanente quando não existe job. Não exigir polling em alta frequência, autorretry ou temporizadores produtivos não contratados. O HTML V1 acelera automaticamente as fases **somente como mock**, sem persistência ou chamadas reais.

**Idempotência:** o fluxo de request/job usa contrato técnico E3. Não deduplicar pelo conteúdo da imagem ou por comportamento inventado no frontend. Não mostrar resultado `SUCCEEDED` antes do processamento concluir. Não atualizar estado ONLINE/OFFLINE, incidentes ou frescor técnico a partir do resultado de captura.

## 6. Regra de convivência com upload manual

Upload existente continua sendo fluxo distinto (`UPLOAD_MANUAL`) e sua proveniência não é promovida a `CAPTURA_CAMERA`. Não substituir input nativo por componente JavaScript falso; manter formato/validações/CSRF existentes na aplicação real. O protótipo não lê nem envia bytes de arquivos; clicar “Enviar imagem” apresenta apenas retorno demonstrativo.

## 7. Preparação conceitual E4 / IMG-06

A E4 **não** está pronta nem autorizada nesta atividade. No laboratório V1, `Ver imagens` abre um `<dialog>` nativo com **três placeholders sintéticos** e identificação de proveniência. Isso não é backend, galeria produtiva, acesso a storage ou autorização de E4. O máximo de três imagens ativas e a ordenação de galeria devem obedecer ao contrato canônico §26; a UI não recria ordenação pelo nome/EXIF do arquivo.

**Na produção E3:** não expor botão `Ver imagens` funcional nem `⋯` inerte. Quando a E4 estiver efetivamente autorizada e implementada, adicionar a ação visível secundária ou navegar para o consumidor aprovado. Não antecipar rotas nem desenhar captura automática.

## 8. Interação da alternativa A (não recomendada)

Menu pequeno aberto por botão `⋯`, `aria-haspopup="menu"`, `aria-expanded` coerente, item único `Ver imagens` com foco por teclado, Escape fecha, clique externo fecha. A desvantagem prática é ocultar uma única ação; reservar menu para cenário futuro em que outras operações legítimas justifiquem overflow. Um menu desnecessário não deve ser incorporado apenas para “parecer enterprise”.

## 9. Design QA / Acessibilidade

Verificar:

1. Ação de captura não se confunde com o envio manual; labels, descrições e separadores claros.
2. Captura é opcional/autorizada, não disparada por renderização, troca de câmera, upload ou abrir menu.
3. Permissão e elegibilidade verificadas no servidor, não apenas por `disabled` visual.
4. Estado `QUEUED`/`RUNNING` não afirma captura concluída.
5. Estados `FAILED`/`UNAVAILABLE` não expõem URLs, credenciais, códigos internos ou detalhes de câmera/storage.
6. E4 claramente futura no protótipo e ausente da produção E3.
7. Ordem de tab, foco visível, rótulo acessível, Escape/retorno de foco em menu/diálogo quando aplicável.
8. Contraste e tamanho de targets conforme Design System.
9. Layout sem overflow horizontal em 2048×742, 1440×900, 1366×768 e 390×844, incluindo texto longo e erros.
10. Shell, histórico, Camera Detail, Quick Detail e todas as áreas protegidas permanecem intactos.

### QA executado no HTML independente (17/10/2026)

- Renderização sem erro de JavaScript e sem overflow horizontal global: **2048×742, 1440×900, 1366×768 e 390×844**.
- Alternativas A e B alternáveis; menu A abre/fecha; diálogo E4 abre por ambos, apresenta três placeholders e fecha por botão/Escape; controle de cenário desabilita a captura nos casos `ineligible`; sequência simulada **QUEUED → RUNNING → SUCCEEDED** foi exercitada em cada viewport.
- Capturas locais produzidas. Esses resultados comprovam **somente o mock HTML**, não conformidade WCAG completa, implementação Django, endpoint/job real, permissões ou revisão humana.
- `PROTOTYPE_QA = PASS_WITH_LIMITATIONS`; `HUMAN_VISUAL_APPROVAL = PENDING`.

## 10. Regras de integração futura Django

- Compor nova região exclusivamente nos templates/CSS locais da tela de detalhes da câmera, preservando as autoridades canônicas e o layout atual.
- Reutilizar classes, tokens e ícones já disponíveis no ARGOS, sem copiar CSS global ou reconstruir sidebar/topbar do HTML independente.
- Não alterar a UI de upload além dos ajustes materiais aprovados; preservar seu fluxo real.
- Não implementar E4 na E3; descrever dependências e isolar a futura extensão.
- Toda interação assíncrona deve receber dados do endpoint/job real e seguir segurança/autorização, CSRF e estados do contrato técnico.
- Executar regressão dos componentes irmãos da Camera Detail e comparar screenshot renderizado com a referência visual aprovada.
- **Aprovação visual do protótipo ≠ autorização de implementação ≠ aceite visual Django integrado**.

## 11. Decisões humanas e próximos gates

```text
ALTERNATIVE_A = AVAILABLE_FOR_COMPARISON / NOT_RECOMMENDED
ALTERNATIVE_B = RECOMMENDED / PENDING_HUMAN_APPROVAL
E3_VISUAL_STATUS = DRAFT
E3_RUNTIME_STATUS = NOT_STARTED_BY_THIS_PROTOTYPE
E4_GALLERY = CONCEPT_ONLY / NOT_AUTHORIZED
SIDEBAR_TOPBAR = LOCKED
QUICK_DETAIL = LOCKED
CURRENT_CAMERA_DETAIL_LAYOUT = PROTECTED
CONTRACT_STATUS = DRAFT / PENDING_HUMAN_VISUAL_APPROVAL
NEXT_GATE = USER_VISUAL_REVIEW
```

O usuário deverá avaliar a descoberta da ação, a distribuição das duas zonas, densidade da linha e mensagens. Somente após aceite visual deve ser produzido um handoff de conformidade final ao agente ARGOS. Esse aceite não ratifica contratos técnicos de E3/E4 por si só.

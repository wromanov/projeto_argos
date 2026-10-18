# Contrato visual aprovado — Operações complementares / E3 V1

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
RELATED_FUTURE_STAGE = E4 / IMG-06
PROTOTYPE = prototype/ARGOS_E3_IMAGE_OPERATIONS_PROTOTYPE_V1.html
APPROVED_VARIANT = B / VISIBLE_ACTIONS
HUMAN_VISUAL_APPROVAL = PASS
VISUAL_COMPOSITION = FROZEN
DJANGO_IMPLEMENTATION = NOT_PERFORMED_BY_UI_CONSULTANT
DJANGO_HUMAN_ACCEPTANCE = PENDING
E4_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_APPROVAL
```

## 1. Aprovação e fonte de verdade

A decisão explícita do usuário foi manter e aprovar a **alternativa B do HTML original**, sem novas mudanças. Para o desktop, o arranjo é **UPLOAD MANUAL À ESQUERDA** e **CAPTURA DIRETA À DIREITA**, com `Ver imagens` como ação secundária de apresentação conceitual E4. O código do HTML original é a baseline visual congelada; eventuais imagens geradas posteriormente, notas de discussão e versão A não substituem a versão selecionada.

**Importante:** E4 está representada **somente no protótipo**; o texto `Ver imagens` integra a intenção visual aprovada, mas não autoriza um botão E4 habilitado na produção E3 antes de existir rota, permissão, consumidor e aprovação técnica próprios.

## 2. Composição imutável aprovada

- Posição: na **seção já existente “Operações complementares”**, abaixo da superfície de Histórico em Detalhes completos da câmera.
- Manter o cabeçalho discreto e a linha divisória superior da seção. **Não criar novos cards**, grandes superfícies, sombras decorativas ou faixas coloridas.
- Desktop: duas zonas irmãs (upload esquerda, captura direita), com divisor neutro interno, alinhamentos consistentes e aproveitamento da largura livre. Grid de referência no laboratório: aproximadamente `1.45fr 1fr` (o CSS real deve preservar a aparência, não copiar pixels cegamente).
- Upload: título `Enviar imagem manualmente`, legenda existente, seletor nativo de arquivos com label `Imagem` e botão `Enviar imagem`; manter fluxo Django existente.
- Captura: título `Captura direta da câmera`, descrição curta de processamento em segundo plano, botão `Capturar imagem` com ícone coerente e feedback de execução imediatamente próximo ao botão.
- Evolução E4: `Ver imagens` como ação visual secundária junto ao botão Capturar imagem; na produção E3, **não introduzir controle inerte** nem fingir capacidade E4.
- Mobile/estreito: zonas empilhadas **upload antes de captura**, divisor horizontal; largura fluida, alvos adequados, ações não espremidas, sem overflow.
- Mesmos tokens, tipografia, bordas e botões do Design System atual; os valores específicos do HTML são referência, não autorização para criar tokens globais.

## 3. Características que não são componentes produtivos

Não transportar do laboratório: shell/sidebar/topbar sintéticos, rótulos `MOCK`, seletor de variantes A/B, controle de cenários, dados falsos, animação de sucesso por temporizador, galeria fictícia E4, footers e legendas de teste.

## 4. Proteções

```text
SIDEBAR = LOCKED
TOPBAR = LOCKED
QUICK_DETAIL = LOCKED
CAMERA_DETAIL_EXISTING_REGIONS = PROTECTED
HISTORICO = PROTECTED
UPLOAD_BACKEND = PRESERVE_EXISTING
GLOBAL_CSS_CHANGE = NOT_AUTHORIZED
NEW_DESIGN_SYSTEM = FORBIDDEN
```

A implementação deve usar **Django SSR + HTML semântico + CSS customizado + JavaScript vanilla quando necessário**, sem introduzir SPA/framework/bundler obrigatório.

## 5. Critérios para fidelidade visual integrada

1. Upload segue à esquerda e captura à direita no desktop.
2. Cabeçalhos, campos, ações e divisórias mantêm o alinhamento e densidade aprovados.
3. O upload existente não perde autorização, CSRF, validação, nem comportamento de seleção de arquivo.
4. O botão Capturar aciona somente fluxo E3 autorizado; não dispara captura ao renderizar/navegar.
5. Os estados de job surgem **sem transformar a seção num card grande** e sem competir visualmente com o upload.
6. A galeria E4 não fica operacional na E3 antes de autorização e integração.
7. Sem regressão na página completa, shell, Quick Detail e demais superfícies.
8. Comparar screenshots reais do Django com a V1 em 2048×742, 1440×900, 1366×768 e 390×844, usando zoom 100%.
9. Registrar limitações, alterações justificadas e evidências; aprovação humana do Django permanece pendente.

## 6. Precedência

Os contratos de domínio de imagem, captura, segurança e autorização prevalecem sobre qualquer comportamento funcional simulado no HTML. Este documento governa somente a **composição e a experiência visual aprovada**, no escopo E3 e da preparação visual E4.

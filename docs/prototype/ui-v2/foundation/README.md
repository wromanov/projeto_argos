# ARGOS UI V2 — Visual Foundation P2

- ACTIVITY: UI-V2-P2 — Visual Foundation
- DESIGN_STRATEGY: CODE_FIRST / STACK_NATIVE / PROTOTYPE_DRIVEN
- CANONICAL_DESIGN_SYSTEM: static/css/ui-v2/
- DESIGN_SYSTEM_VERSION: 2.0.0 — versão aprovada e pinada
- CANONICAL_TOKEN_COUNT: 74 variáveis CSS transversais usadas pela foundation
- SELECTED_DIRECTION: C — ARGOS HYBRID
- SCOPE: VISUAL_ONLY
- FIGMA_ROLE: OPTIONAL / INFORMATIVE / NON-CANONICAL
- P2_USER_APPROVAL: PASS

## Páginas executáveis

Abra index.html para navegar pela fundação. As páginas colors.html, typography.html, spacing.html, controls.html, data-display.html, feedback.html e responsive.html consomem os quatro arquivos canônicos em static/css/ui-v2/. Não há cópia de CSS visual neste diretório nem JavaScript necessário para a navegação.

O CSS fica em assets estáticos reais do repositório, mas nenhum template de produção foi alterado, a aplicação não o carrega e nenhum comportamento de runtime foi modificado.

## Authority e ownership

- ARGOS domain: domínio, informação, permissões, regras, fluxos, rotas e estrutura conceitual.
- Design System: tokens, primitives, componentes compartilhados, densidade e estados visuais.
- Protótipo de tela aprovado: composição, hierarquia, agrupamento e layout.
- Contratos funcionais: comportamento, permissões, semântica e workflows.
- Figma: representação informativa e opcional.
- Quick Detail: baseline aprovada e protegida; nenhuma migração foi feita.
- Django Admin: herdado; sem redesenho próprio por padrão.
- P3: não iniciado.

Veja ../contracts/ para o contrato visual, catálogo de ownership, estados e cobertura factual do Screen Census. A fonte visual é ../style-lab/README.md, ../style-lab/styles.css e ../style-lab/screenshots/argos-style-c.png; o significado do domínio permanece sob a documentação ARGOS e o código atual. A especificação anterior continua aplicável onde não foi supersedida visualmente.

## Divergências visuais

Cada resolução abaixo altera apenas a apresentação. Semântica, condição, persistência, transição e texto funcional permanecem sob a autoridade ARGOS.

### D1 — Hierarquia tipográfica

- OLD_AUTHORITY: docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md, baseline anterior: título 28px/700, seção 20px/600, métrica 28–32px/700, body 14px/400, label 14px/500, cabeçalho de tabela 12–13px/600, caption 12px/400.
- NEW_VISUAL_AUTHORITY: Style Lab C — ARGOS HYBRID: h1 clamp(27px, 3vw, 34px), h2 18px, métrica 24px, body 14px, label 11px, cabeçalho de tabela 10px, célula 12px, caption 10px; Inter.
- RESOLUTION: P2 usa a hierarquia de C; conteúdo e semântica não mudam.
- SCOPE: VISUAL_ONLY
- DOMAIN_BEHAVIOR_CHANGED: NO
- RUNTIME_BEHAVIOR_CHANGED: NO
- PRODUCTION_CHANGED: NO

### D2 — Escala, padding e densidade

- OLD_AUTHORITY: especificação anterior: escala 4/8/12/16/20/24/32/40/48px, page padding 24px desktop e 16px mobile, cards 16–20px, tabela 52–56px.
- NEW_VISUAL_AUTHORITY: Style Lab C — ARGOS HYBRID: 29px no topo, 30px lateral e 48px inferior no desktop; 20px/14px/35px no mobile; gap 20px; painel 20px; tabela 64px com 13px inline e 9px block.
- RESOLUTION: P2 usa a densidade de C; escala comum 4/8/12/16/20/24/32px. Linha compacta de 56px só por variante explícita.
- SCOPE: VISUAL_ONLY
- DOMAIN_BEHAVIOR_CHANGED: NO
- RUNTIME_BEHAVIOR_CHANGED: NO
- PRODUCTION_CHANGED: NO

### D3 — Radius de controls, surfaces e badges

- OLD_AUTHORITY: especificação anterior: 6/8/10/12px e pill 999px; controls 8px; badges em pill.
- NEW_VISUAL_AUTHORITY: Style Lab C — ARGOS HYBRID: surface 7px; controls e badges 5px.
- RESOLUTION: P2 usa os raios de C. Forma não determina status, severidade ou interação.
- SCOPE: VISUAL_ONLY
- DOMAIN_BEHAVIOR_CHANGED: NO
- RUNTIME_BEHAVIOR_CHANGED: NO
- PRODUCTION_CHANGED: NO

### D4 — Paleta semântica dos estados

- OLD_AUTHORITY: especificação anterior: online #16A36A/#DDF5EA; warning #E59B22/#FFF1D6; offline #D64545/#FCE3E3; maintenance #7C5CC4/#EEE8FB; disabled #81909C/#E8EDF0; info #3B82C4/#E3F0FA.
- NEW_VISUAL_AUTHORITY: Style Lab C — ARGOS HYBRID: success #145E42/#DFF3E8; warning #80500B/#FFF0D7; danger #922C3E/#F9E5E8; neutral #1D4F86/#E8F2FA; info preservado como fallback.
- RESOLUTION: muda apenas a apresentação de status já existentes: ONLINE usa success, OFFLINE danger, frescor stale warning e ausência de classificação específica neutral. INFO é fallback visual. Maintenance/disabled não criam estados ou mapeamentos. Divergência de nomes de estados de imagem fica documentada no STATE_MATRIX.md, sem reconciliação silenciosa.
- SCOPE: VISUAL_ONLY
- DOMAIN_BEHAVIOR_CHANGED: NO
- RUNTIME_BEHAVIOR_CHANGED: NO
- PRODUCTION_CHANGED: NO

### D5 — Elevação

- OLD_AUTHORITY: especificação anterior: card 0 1px 2px rgba(18,48,71,.04), elevated 0 4px 14px rgba(18,48,71,.08), sheet 0 8px 30px rgba(18,48,71,.12).
- NEW_VISUAL_AUTHORITY: Style Lab C — ARGOS HYBRID: card 0 2px 5px rgb(14 43 64 / .04), 0 10px 28px rgb(14 43 64 / .035).
- RESOLUTION: P2 usa elevação Raised de C em cards; overlay conserva o fallback anterior enquanto C não apresenta amostra equivalente.
- SCOPE: VISUAL_ONLY
- DOMAIN_BEHAVIOR_CHANGED: NO
- RUNTIME_BEHAVIOR_CHANGED: NO
- PRODUCTION_CHANGED: NO

## Figma — estado factual

Arquivo de referência parcial: [ARGOS UI V2 — Design System](https://www.figma.com/design/K9kMQ2QfictNGczgAEHSkQ). Até o limite mensal ser atingido, foram criadas quatro collections com 204 variables, nove text styles, dois effect styles e as três páginas 00 Cover & Getting Started, 01 Foundations e 02 Components & Utilities. A composição dessas páginas ficou incompleta. Isso registra estado, não authority.

- FIGMA_STATUS: PARTIAL_REFERENCE
- FIGMA_RATE_LIMIT: EXTERNAL_CONSTRAINT
- FIGMA_BLOCKS_P2: NO
- A sync futura ao Figma ocorre somente depois da aprovação de tokens/componentes. P2 não aguarda a renovação.

## Origem de assets e compatibilidade

- Logo local: ../style-lab/argos-icon.svg.
- Inter e os pesos Regular, Medium, Semi Bold e Bold foram verificados na fonte da referência. CSS declara Inter com fallback de sistema; nenhuma fonte é carregada da rede.
- Compatível com Django SSR, templates semânticos, CSS próprio e vanilla JS progressivo.
- O espécime usa apenas o asset local argos-icon.svg. Não há rotas, rede, mutação de dados ou fluxo funcional.
## P2 aprovado e fechado — 2026-09-28

USER_VISUAL_ACCEPTANCE = PASS
USER_FOUNDATION_APPROVAL = PASS
P2_STATUS = CLOSED / PASS
DESIGN_SYSTEM_VERSION = 2.0.0
DESIGN_SYSTEM_VERSION_PINNED = YES
PROJECT_STATE_UPDATE = PASS
P2_ACTIVITY_COMPLETE = YES
ACTIVITY_COMPLETE = NO / integração canônica e push pendentes
P3_STARTED = NO
NEXT_ACTIVITY = UI-V2-P3 — NAVIGABLE SCREEN PROTOTYPES / NOT STARTED

A aprovação fecha a Visual Foundation e promove a versão para 2.0.0. P3 permanece separado, não iniciado e sem qualquer alteração de runtime ou template produtivo. O relatório de QA e as capturas revisadas permanecem em ../../../../design-qa.md e screenshots/.
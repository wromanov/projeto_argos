# ARGOS-CRED-UI-01 — Evidências e Design QA do protótipo V1

**Artefato validado:** `ARGOS_CRED_UI_01_PROTOTIPO_V1.html` (cópia **sem alterações**)
**Alvo:** protótipo independente, não o Django real.
**Aprovação de composição:** V1 alternativa A — `PASS` pelo usuário.

## Testes automatizados executados nesta consolidação

Playwright/Chromium headless (conteúdo HTML carregado diretamente em memória; sem requisições HTTP). Foram executadas **16 combinações**: quatro viewports × quatro cenários (`configured`, `empty`, `readonly`, `noaccess`).

| Viewport | Estados | Resultado |
|---|---|---|
| 1920×1080 | Configurada / Sem ativa / Somente leitura / Sem metadata | 4/4 PASS |
| 1440×900 | Configurada / Sem ativa / Somente leitura / Sem metadata | 4/4 PASS |
| 1366×768 | Configurada / Sem ativa / Somente leitura / Sem metadata | 4/4 PASS |
| 390×844 | Configurada / Sem ativa / Somente leitura / Sem metadata | 4/4 PASS |

Critérios verificados: ausência de exceções JS capturadas, ausência de overflow horizontal global, ausência de formulário HTML aninhado e visibilidade do painel conforme cenário (mock). **Total: 16/16 PASS**.

Fluxos exercitados no desktop: diálogo de substituição abre, envio com valores demonstrativos apresenta feedback; aviso de cadastro dirty abre antes de ação independente; cenário sem permissão omite painel; variante B expansível funciona **somente como comparação histórica**. Testes de interação observados sem exceção JS.

## O que ainda NÃO foi validado

- **Nenhum teste Django**, backend, service, banco, CSRF, autorização real, audit trail, servidor, HTTPS, cache ou persistência foi executado neste protótipo.
- Nenhuma garantia de que as rotas HTTP propostas existam.
- Revisão manual completa de leitor de tela, WCAG ou percurso 100% por teclado não foi efetuada nesta consolidação.
- Capturas anexadas são do **mock**, não da aplicação integrada.
- O HTML dispõe de seletor da alternativa B e controles de cenário apenas para auditoria; não importar na implementação.

## Índice de capturas

- `evidence/ARGOS_CRED_UI_01_V1_FOCUS_1440x900.png` — card de credenciais integrado à página.
- `evidence/ARGOS_CRED_UI_01_V1_FOCUS_390x844.png` — contexto de visualização mobile.
- `evidence/ARGOS_CRED_UI_01_V1_DIALOG_PREVIEW.png` — diálogo nativo da alternativa A, aprovada.
- `evidence/ARGOS_CRED_UI_01_V1_PREVIEW_1366x768.png` — viewport desktop compacto.
- `evidence/ARGOS_CRED_UI_01_V1_PREVIEW_1440x900.png` — viewport desktop.
- `evidence/ARGOS_CRED_UI_01_V1_PREVIEW_390x844.png` — viewport mobile.
- `evidence/REFERENCE_ONLY_NOT_SELECTED_EXPANSIVEL.png` — alternativa B **não escolhida**.

A aprovação visual humana é um ato explícito posterior à prototipação e está registrada em `01_APPROVAL_AND_VISUAL_CONTRACT.md`. `DJANGO_VISUAL_QA = NOT_PERFORMED`.

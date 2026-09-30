# P3-C — pacote compacto para revisão visual humana

Data: 2026-09-30

```text
DESIGN_SYSTEM_VERSION = 2.0.2
STALE_METADATA = RESOLVED
P3_C_DS_2_0_2_REGRESSION = PASS
PRODUCT_DESIGN_TARGETED_QA = PASS
HUMAN_VISUAL_APPROVAL = PENDING
NEXT_GATE = P3-C HUMAN VISUAL REVIEW
```

O pacote cobre os arquétipos principais; não reabre os dez estados nem refaz a QA histórica.

| Arquétipo | Página atual | Captura/evidência de apoio |
|---|---|---|
| Activities — lista | [SCR-ACT-LIST-001](scr-act-list-001.html) | `../../evidence/screenshots/p3-c/post-ds-2.0.1/scr-act-list-001__1440x900__default__default.png` |
| Activities — formulário | [SCR-ACT-CREATE-001](scr-act-create-001.html) | `../../evidence/screenshots/p3-c/post-ds-2.0.1/scr-act-create-001__1440x900__default__default.png` |
| Governance — estado/ação | [SCR-GOV-STATE-001](scr-gov-state-001.html) | `../../evidence/screenshots/p3-c/post-ds-2.0.1/scr-gov-state-001__1440x900__default__default.png` |
| Events — lista | [SCR-EVENT-LIST-001](scr-event-list-001.html) | `../../evidence/screenshots/p3-c/post-ds-2.0.1/scr-event-list-001__1440x900__default__default.png` |
| Events — detalhe | [SCR-EVENT-DETAIL-001](scr-event-detail-001.html) | `../../evidence/screenshots/p3-c/post-ds-2.0.1/scr-event-detail-001__1440x900__default__default.png` |
| Mobile — tabela de Events | [SCR-EVENT-LIST-001](scr-event-list-001.html), viewport 390×844; role até a seção “Eventos registrados” | [Relatório de regressão DS 2.0.2](../../evidence/screenshots/p3-c/post-ds-2.0.2/post-ds-regression.md), medições mobile e acessibilidade |

## Leitura visual direcionada

- ARGOS Hybrid: shell navy, superfícies claras e semântica visual consistente.
- Activities: lista escaneável; formulário mantém contexto da câmera, agrupamento de campos e ação demonstrativa.
- Governance: contexto, impacto operacional e confirmação permanecem hierarquizados.
- Events: filtros e tabela são legíveis; o detalhe destaca registro imutável, identificação do evento e entidades relacionadas.
- Mobile: o consumidor de tabela permanece dentro da página, com região local rolável; a inspeção 2.0.2 e os critérios de fragmentação e acesso por teclado constam no relatório vinculado.

## Estado das capturas

As imagens persistidas em `post-ds-2.0.1/` são históricas e mostram o selo 2.0.1; servem como referência de composição, não como prova do selo atualizado. A pré-visualização atual das páginas mostra `Design System 2.0.2` e foi revisada visualmente no browser local. Nenhuma captura PNG 2.0.2 foi persistida neste workstation; o relatório técnico pós-2.0.2 continua sendo a fonte das medições. Aprovação visual humana permanece pendente.
# P3-B — coverage local e checkpoint de pausa

**Atividade:** UI-V2-P3-B — Monitoring / Substitutions\
**Fan-out base:** 9943e20d9b1e04159e067c72aa4dd70eab2bdb36\
**Branch:** codex/ui-v2-p3-b-monitoring-activities\
**Worktree:** C:/Users/walacedelgado/PycharmProjects/projeto_argos_ui_v2_p3_b\
**Status:** QA_PARTIAL — WIP checkpoint para retomada\
**Conclusão estimada:** 88%\
**Design System:** 2.0.0, consumido diretamente; sem alteração.

## Ownership canônico

A matriz de P3_PROTOTYPE_HARNESS.md e SCREEN_COVERAGE.md confirma:

| SCREEN_ID | Path canônico | Estado |
|---|---|---|
| SCR-MON-HISTORY-001 | docs/prototype/ui-v2/screens/p3-b/scr-mon-history-001.html | QA_PARTIAL |
| SCR-SUB-LIST-001 | docs/prototype/ui-v2/screens/p3-b/scr-sub-list-001.html | QA_PARTIAL |
| SCR-SUB-DETAIL-001 | docs/prototype/ui-v2/screens/p3-b/scr-sub-detail-001.html | QA_PARTIAL |
| SCR-SUB-CAMERA-001 | docs/prototype/ui-v2/screens/p3-b/scr-sub-camera-001.html | QA_PARTIAL |

Ownership drift = NO. Conflitos = NONE.

## Conteúdo e interações

- Monitoramento mostra incidentes abertos/fechados, início/fim, duração fictícia, origem e motivo de fechamento. Stale é evidência distinta; o estado efetivo aparece como Desconhecido e preserva o último estado estável como evidência.
- Substituições são histórico somente para consulta. A lista global aceita busca e período; período invertido é erro de validação; o detalhe não oferece mutação.
- A consulta por câmera identifica o papel desempenhado em cada relação histórica.
- Links, filtros e paginação são locais/conceituais. Não há persistência, backend ou integração produtiva.
- Fixtures sintéticas e determinísticas estão em docs/prototype/ui-v2/fixtures/p3-b.json.

## Estados e QA renderizado

| Tela | Estados implementados e exercitados no DOM | Estado do QA |
|---|---|---|
| Monitoramento | default, empty, stale, fixture long | DOM validado; screenshots default nos 4 viewports; empty/stale em 1440×900 e empty em 390×844; long em 1440×900. Stale mobile precisa recaptura correta. |
| Lista global | default, selected (q=CAM), empty, erro de período, fixture long | DOM validado; screenshots default nos 4 viewports; selected em 1440×900; empty e long em 390×844. Capturas de error/empty/long desktop e selected mobile pendentes. |
| Detalhe | default, fixture long | DOM validado; screenshot default nos 4 viewports; long pendente. |
| Consulta por câmera | default, empty, fixture long | DOM validado; default capturado nos 4 viewports; empty e long pendentes. |

**Viewports:** defaults verificados em 1920×1080, 1440×900, 1366×768 e 390×844. Em todos, a largura do documento ficou dentro da largura CSS medida. Cenários de estado em 390×844 também não tiveram overflow global. Tabelas mantêm colunas essenciais com rolagem horizontal local.

**Acessibilidade:** inspeção estática anterior observou títulos, H1, landmarks, labels e semântica de tabelas. Keyboard, foco visível, nomes acessíveis e touch targets permanecem pendentes. Não declarar conformidade WCAG.

**Design QA:** parcial. Style Lab C foi comparado com os quatro defaults mobile. Direção ARGOS Hybrid, paleta, tipografia e cartões são coerentes. O gate formal design-qa não está completo; zoom 100%, variantes restantes e revisão integral pendem.

## Evidências

- Diretório: docs/prototype/ui-v2/evidence/screenshots/p3-b/
- 23 PNGs canônicos estão incluídos no checkpoint.
- Um PNG local não canônico, scr-mon-history-001__390x844__stale__default.png, registra uma captura feita em 1698×757 CSS. Está excluído do checkpoint; recapturar stale mobile em 390×844.
- O Edge expirou chamadas Page.captureScreenshot nas variantes sub-list error/empty/long desktop e selected mobile; esses screenshots não estão disponíveis. Outras variantes marcadas pendentes na tabela acima não foram capturadas antes da pausa.
- Fonte visual: docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png.

## Findings e escopo

- Quatro arquivos HTML permanecem com argos-prototype-status=IN_PROGRESS.
- Product Design get-context: realizado. Product Design design-qa: parcial, sem PASS.
- DS_CHANGE_REQUESTS = NONE. ROOT_CHANGE_REQUESTS = NONE.
- DESIGN_SYSTEM_MODIFIED = NO; ROOT_OWNED_FILES_CHANGED = NO; CROSS_FAMILY_FILES_CHANGED = NO; PRODUCTION_CHANGED = NO.
- USER_VISUAL_APPROVAL = PENDING.
- Este relatório é local à família P3-B; não editar SCREEN_COVERAGE.md mestre nem outros arquivos root-owned.

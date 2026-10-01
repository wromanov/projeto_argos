# P3-B — cobertura de regressão e evidências

**Atividade:** UI-V2-P3-B — Browser Regression + Evidence Refresh + Final Design QA
**Data:** 2026-09-30
**Branch:** codex/ui-v2-p3-b-monitoring-activities
**Worktree:** C:\Users\walac\desenvolvimento\projeto_argos_ui_v2_p3_b
**HEAD inicial:** 7b879b890a1c0254c52234d0391589348bda6526
**HEAD remoto inicial:** 7b879b890a1c0254c52234d0391589348bda6526
**Divergência inicial:** 0 / 0; worktree limpo
**Design System validado:** 2.0.2; propagação P3-B 466504bfaec68c04c4a1c53daa64764053844181

## Escopo e ownership

| Screen ID | Rota canônica | Resultado |
|---|---|---|
| SCR-MON-HISTORY-001 | screens/p3-b/scr-mon-history-001.html | PASS |
| SCR-SUB-LIST-001 | screens/p3-b/scr-sub-list-001.html | PASS |
| SCR-SUB-DETAIL-001 | screens/p3-b/scr-sub-detail-001.html | PASS |
| SCR-SUB-CAMERA-001 | screens/p3-b/scr-sub-camera-001.html | PASS |

As quatro telas pertencem a P3-B. P3-A, P3-C, P3-D, shared DS, produção e backend permaneceram fora das alterações.

## Evidências PNG atuais

Capturas feitas pelo mecanismo autorizado: Node + Playwright + Chrome local, servindo o protótipo por HTTP em 127.0.0.1, viewport CSS explícito e deviceScaleFactor 1. Cada PNG foi aberto e inspecionado depois de salvo. Todos medem exatamente a dimensão indicada no nome.

Diretório: docs/prototype/ui-v2/evidence/screenshots/p3-b/.

| Tela | Estado / viewport | Arquivo |
|---|---|---|
| Monitoramento | default / 1440×900 | scr-mon-history-001__1440x900__default__default.png |
| Monitoramento | default / 390×844 | scr-mon-history-001__390x844__default__default.png |
| Monitoramento | empty / 390×844 | scr-mon-history-001__390x844__empty__default.png |
| Monitoramento | stale (freshness=stale) / 390×844 | scr-mon-history-001__390x844__stale__default.png |
| Lista global | default / 1440×900 | scr-sub-list-001__1440x900__default__default.png |
| Lista global | default / 390×844 | scr-sub-list-001__390x844__default__default.png |
| Lista global | empty / 390×844 | scr-sub-list-001__390x844__empty__default.png |
| Lista global | long / 390×844, tabela em foco visual | scr-sub-list-001__390x844__default__long.png |
| Detalhe | default / 1440×900 | scr-sub-detail-001__1440x900__default__default.png |
| Detalhe | default / 390×844 | scr-sub-detail-001__390x844__default__default.png |
| Detalhe | long / 390×844, informações históricas | scr-sub-detail-001__390x844__default__long.png |
| Consulta por câmera | default / 1440×900 | scr-sub-camera-001__1440x900__default__default.png |
| Consulta por câmera | default / 390×844 | scr-sub-camera-001__390x844__default__default.png |
| Consulta por câmera | empty / 390×844 | scr-sub-camera-001__390x844__empty__default.png |

SCR-SUB-DETAIL-001 não define variante empty/error canônica no fixture/harness atual; esse estado não foi inventado.

## Regressão browser

**Resultado geral:** PASS.

| Check | Resultado |
|---|---|
| hidden inativo | PASS — zero elementos ocultos visíveis indevidamente nas 14 capturas |
| Overflow horizontal global | PASS — zero nas quatro telas/estados cobertos |
| Rolagem local de tabela | PASS — conteúdo largo permanece em .argos-table-region com overflow-x:auto em mobile; em desktop a tabela cabe na região |
| Fragmentação de palavras | PASS — zero palavras comuns quebradas em fragmentos; identificadores longos podem quebrar em separadores, conforme DS 2.0.2 |
| Ações por teclado | PASS — todos os links de ação visíveis nas listas e consultas foram alcançados por Tab |
| Foco visível | PASS — controles focáveis distintos e ações de tabela apresentaram foco visível |
| Scroll local ao focar ações | PASS — a região da tabela revelou horizontalmente a coluna de ações em mobile |
| Busca | PASS — consulta sem correspondências mostra empty e zero linhas |
| Período inválido | PASS — alerta visível e dois campos com aria-invalid=true |
| Link lista → detalhe | PASS — abre o detalhe do registro selecionado |
| Paginação por câmera | PASS — página 2 contém o papel “Entrou como substituta” |
| Detalhe histórico | PASS — aviso somente para consulta visível; sem ações de edição/exclusão |
| Monitor stale | PASS — freshness=stale mostra estado efetivo “Desconhecido”, aviso stale e último estado estável |
| Erros de console/página | PASS — 0 |
| Requests externos | PASS — 0 |
| Requests não-GET | PASS — 0 |
| Respostas HTTP de erro ou requests falhos | PASS — 0 |
| Persistência real | PASS — 0 writes observados em localStorage, sessionStorage, IndexedDB e cookies; protótipo carrega fixture estática local |

As requests da execução eram somente GET para o preview local e arquivos de fixture/estilo/script. Não houve chamadas ao backend ou mudança persistente.

## Design System e finding
TOP_BADGE = Design System 2.0.2
FOOTER = DS 2.0.2
PRIVACY_SANITY_CHECK = PASS

DESIGN_SYSTEM_VERSION = 2.0.2. P3B_REV_01 = RESOLVED. STALE_VISIBLE_DS_METADATA = RESOLVED. STALE_FOOTER_OCCURRENCES_FOUND = 4. STALE_FOOTER_OCCURRENCES_CORRECTED = 4. VISIBLE_DS_METADATA_CONSISTENT = YES — metadados argos-ui-version, badges e rodapés exibem 2.0.2 nas quatro superfícies.

DESKTOP_EVIDENCE_REFRESHED = YES — quatro PNGs desktop 1440×900 default foram recapturados. A captura SUB-CAMERA inclui o rodapé e mudou somente pixels na pequena área do texto; nos outros três frames default o rodapé fica abaixo da viewport e os novos arquivos são pixel idênticos aos anteriores. Sem regressão de layout. MOBILE_EVIDENCE_REUSED = YES — dez PNGs mobile preservados; nenhum mostra o rodapé no frame. PRIVACY_SANITY_CHECK = PASS — inspeção visual dos 14 PNGs e conferência das fixtures; somente conteúdo de demonstração, sem credenciais, tokens, chaves privadas ou dados pessoais reais observados.

BLOCKING = NONE
NON_BLOCKING = NONE
KNOWN_SHARED = NONE
PRODUCT_DESIGN_QA = PASS
USER_VISUAL_APPROVAL = PASS

## Estado da atividade

BROWSER_REGRESSION = PASS / targeted desktop post-fix: 4/4 surfaces, no global overflow, no console/page or HTTP errors
EVIDENCE_CAPTURE = PASS / 14 PNGs atuais; quatro desktops refreshed, dez mobiles reutilizados; dimensões verificadas
PROJECT_STATE_UPDATE = PASS / checkpoint P3-B nos relatórios familiares; PROJECT_STATE.md root-owned inalterado
SCREEN_SOURCE_CHANGED = YES (somente metadata visual nos quatro HTMLs P3-B)
SHARED_DESIGN_SYSTEM_CHANGED = NO
OTHER_FAMILIES_CHANGED = NO
PRODUCTION_CHANGED = NO
FAMILY_TECHNICAL_STATUS = PASS / USER_APPROVED / FROZEN / CLOSED / PUBLISHED
NEXT_GATE = P3 ROOT INTEGRATED VALIDATION

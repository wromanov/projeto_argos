# P3-B — cobertura local e checkpoint de recuperação

**Atividade:** UI-V2-P3-B — Monitoring / Substitutions
**Branch:** `codex/ui-v2-p3-b-monitoring-activities`
**Worktree:** `C:/Users/walac/.codex/worktrees/ui-v2-p3-b/projeto_argos`
**Base recebida:** `b57ad0044722a838e761f987eeb0aa556c6646b0`
**Patch DS 2.0.1:** `8121ed38cc15e1ff6e72cb46bbb2ca865100bce0`, ancestral de `origin/master`; cherry-pick local `94da3b6`
**Estado:** QA parcial; evidência pendente; autorização para Playwright local concedida neste checkpoint.
**PROJECT_STATE_UPDATE:** PASS — atualização restrita a este relatório e ao HANDOFF da família; arquivos root-owned permanecem intocados.

## Ownership

A matriz canônica atribui estas quatro telas a P3-B. Nenhum desvio de ownership ou conflito foi encontrado.

| SCREEN_ID | Path canônico | Metadado atual |
|---|---|---|
| SCR-MON-HISTORY-001 | `docs/prototype/ui-v2/screens/p3-b/scr-mon-history-001.html` | `IN_PROGRESS` |
| SCR-SUB-LIST-001 | `docs/prototype/ui-v2/screens/p3-b/scr-sub-list-001.html` | `IN_PROGRESS` |
| SCR-SUB-DETAIL-001 | `docs/prototype/ui-v2/screens/p3-b/scr-sub-detail-001.html` | `IN_PROGRESS` |
| SCR-SUB-CAMERA-001 | `docs/prototype/ui-v2/screens/p3-b/scr-sub-camera-001.html` | `IN_PROGRESS` |

## Implementação e propagação

- A família agora declara DS 2.0.1 nos metadados e badges das quatro telas.
- O patch canônico foi propagado sem cherry-pick de commits de integração ou continuidade.
- `p3-b.js` corrige contagens em estados vazios e nomes acessíveis específicos da paginação; os rótulos iniciais nos wrappers HTML também foram alinhados.
- Monitoramento mostra registros abertos/fechados e distingue stale: o efetivo aparece como “Desconhecido”, preservando o último estado estável como evidência; não introduz estado `RECOVERING`.
- A lista global trata período invertido como erro de validação do filtro. O detalhe permanece somente para consulta. A consulta por câmera apresenta os papéis “Foi substituída” e “Entrou como substituta”.
- Fixtures são sintéticas e determinísticas; links, filtros e paginação são conceituais. Não há persistência, backend nem alteração produtiva.

## Estados exercitados no navegador

| Tela | Cenários pós-correção exercitados |
|---|---|
| Monitoramento | default, vazio (0 registros), stale em 390×844, fixture longa em 390×844 |
| Lista global | default, busca `CAM`, vazio, `state=error` como validação de período, intervalo invertido em 390×844, fixture longa em 390×844 |
| Detalhe | default somente leitura, fixture longa em 390×844 |
| Consulta por câmera | default, vazio (0 registros), fixture longa em 390×844; página 2 confirma “Entrou como substituta” |

Em todos os 15 cenários da matriz DOM: `hidden` inativo permaneceu visualmente oculto e a página não teve overflow global. A paginação fica oculta em estados vazios/erro e usa nomes em português específicos. A tabela usa rolagem horizontal local em mobile; o shell de navegação horizontal também pode rolar sem alargar o documento.

Defaults das quatro telas foram conferidos em 1920×1080, 1440×900, 1366×768 e 390×844. Fixtures longas foram conferidas em 390×844. A escala CSS foi medida com `devicePixelRatio=1` na viewport 390×844.

## Acessibilidade verificada

- Um H1 por tela; hierarquia de títulos, landmarks `nav`/`main`, tabelas e cabeçalhos semânticos presentes.
- Campos da lista têm labels. No período inválido, ambos os campos usam `aria-invalid=true` e apontam para `period-error-copy`.
- A navegação por teclado expõe foco visível com contorno de 3 px; campos de filtro e ações principais recebem foco.
- Os links, botões e campos visíveis dentro de `main` têm dimensões mínimas de 44×44 CSS px em 390×844.
- O detalhe não apresenta controles de edição ou exclusão.
- O shell herdado tem alvos menores (link de marca ~36 px e link de pular ~37 px), sem bloqueio conhecido neste gate. Não declarar conformidade WCAG.

## Design QA e evidências

A direção Style Lab C foi inspecionada contra capturas atuais em memória do Browser do Codex. Paleta azul-marinho/azul, tipografia, cartões, tabelas e chips estão coerentes; a fonte é referência de direção, não mock de composição desta página. Não foi observado desvio visual material nos defaults desktop/mobile inspecionados.

**DESIGN_QA_COMPLETE = NO — final result: blocked.** O gate requer capturas PNG atuais persistidas nos caminhos canônicos e revisão integral dos estados/regions. O Browser do Codex exibe as capturas, mas não as grava no repositório. A autorização para Playwright local está concedida; as capturas permanecem pendentes porque este checkpoint proíbe iniciar nova QA. As 23 imagens que já existem foram feitas antes da propagação 2.0.1 e não devem ser usadas como evidência pós-patch. Nenhuma `USER_VISUAL_APPROVAL` foi registrada.

- Fonte visual: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`.
- Diretório canônico de capturas: `docs/prototype/ui-v2/evidence/screenshots/p3-b/`.
- Histórico/finding de QA: os dois estados vazios contavam os registros-base; ambos agora exibem zero. Rótulos genéricos de paginação também foram corrigidos e revalidados.

## Escopo e estado do projeto

`DESIGN_SYSTEM_MODIFIED = NO` · `ROOT_OWNED_FILES_CHANGED = NO` · `CROSS_FAMILY_FILES_CHANGED = NO` · `PRODUCTION_CHANGED = NO` · `USER_VISUAL_APPROVAL = PENDING`.

Não promover metadados para `TECHNICAL_READY_FOR_REVIEW` nem declarar `ACTIVITY_COMPLETE` enquanto o gate visual e as evidências persistidas estiverem pendentes.
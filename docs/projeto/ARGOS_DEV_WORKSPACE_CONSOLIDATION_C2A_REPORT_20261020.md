# ARGOS — Consolidação do ambiente e reconciliação do Design System — C2-A

**PROJECT_ID:** projeto_argos
**ACTIVITY_ID:** ARGOS-DEV-WORKSPACE-CONSOLIDATION-C2A
**EXECUTION_MODE:** DIRECT
**WORKSTATION:** HOME
**ACTIVITY_TYPE:** ARCHITECTURAL_RECONCILIATION + PRESERVATION_PLANNING
**USER_DECISION:** C2_APPROVED
**CODE_IMPLEMENTATION:** NOT_AUTHORIZED_IN_C2A
**BASELINE:** ddd8f163992fc3cfda25a37d65199e25c249ee72
**WORKTREE:** C:\Users\walac\desenvolvimento\projeto_argos_e3_p0_reconciliation
**DATE:** 2026-10-20

### Estado consolidado

| Campo | Resultado |
|---|---|
| ACTIVITY_COMPLETION_PERCENT | 100% |
| DS_2_1_STATUS | Aprovado e implementado localmente; sem publicação autônoma identificada. Suas declarações estão no checkpoint cumulativo 2.2 publicado na branch P5, mas ausentes do DS global do baseline. |
| DS_2_2_STATUS | Publicado na branch P5 no commit b9cdc00dbc35915deb922c1a0596574a2b9a12bc; não está no baseline. A utility .argos-text-kpi não é consumida pela Camera Detail. |
| DS_2_3_STATUS | Publicação registrada no commit 18e93267e2a2973acc9026bb1f9df45bfced83dc; cabeçalho do contrato está desatualizado; não está no baseline. Há equivalente local na página. |
| DS_2_4_STATUS | Implementado localmente, não publicado; gate visual formal segue aberto no contrato. |
| P5_INTEGRATION_SCOPE | Composição visual essencial já está no baseline. Dos cinco arquivos P5, três divergem e dois são idênticos; não copiar arquivos inteiros. |
| P5_DEPENDENCY_MATRIX | Equivalentes DS 2.1–2.3 page-scoped estão presentes; a surface 2.4 também está escopada à página. Promoção global precisa de decisão humana. |
| LOCAL_DATA_PRESERVATION_READINESS | PARTIAL: inventário e procedimento documentados; nenhum backup ou transporte realizado. |
| C2B_IMPLEMENTATION_READINESS | READY_FOR_REVIEW / CONDITIONAL ON HUMAN SCOPE AND DS 2.4 GATE DECISION / NOT AUTHORIZED |
| CANONICAL_FOLDER_READINESS | NOT_READY, conforme C1 |
| CANONICAL_BRANCH_READINESS | NOT_READY, conforme C1 |
| WIP_PRESERVED | YES |
| CODE_CHANGES | NONE |
| DATABASE_OR_VM_CHANGES | NONE |
| BRANCHES_CREATED / WORKTREES_CREATED | NONE |
| MERGE_OR_CHERRY_PICK / COMMIT_OR_PUSH | NONE |
| FILES_CREATED_OR_MODIFIED | New C2-A report; PROJECT_STATE.md §172; AGENT_CONTINUITY.md §20.129; ACTIVE_DOCUMENT_MAP.md §132. Existing C1 and other documentary WIP preserved. |
| WIP_PRESERVED | YES |
| P1_RTSP | NOT_STARTED |
| DELETE_WORKTREES / DELETE_BRANCHES / RESET_OR_CLEAN | NO |
| PROJECT_STATE_UPDATE | PASS / PROJECT_STATE.md §172 |
| ACTIVITY_COMPLETE | YES / análise e plano C2-A |
| NEXT_GATE | C2A_REVIEW_AND_C2B_EXECUTION_AUTHORIZATION |

## 1. Escopo e fontes

Esta revisão aprofunda somente a dependência P5/Design System já identificada
pela C1. O P0 foi confirmado em HEAD ddd8f163, detached. O WIP documental
existente permaneceu intacto. Não foram inspecionados bancos, screenshots,
settings, logs, ZIPs ou credenciais. Não foram executados testes.

Foram comparados o relatório C1, os registros §§46–56 da linha P5, os contratos
DSCR 2.1–2.4, o checkpoint P5 c91bc6d4658faa408a9f565b9d1c3d6279571cb4 e os
cinco caminhos citados pela C1 contra ddd8f163. c91bc6d não é ancestral do
baseline. A publicação de DS 2.2/2.3 está registrada para a branch
codex/ui-v2-p5-production, não para a baseline operacional.

### Reconciliação da premissa C1

Diferença de blob não significa que a composição visual P5 esteja ausente. O
template do baseline já contém as regiões canônicas, Data Pair/Data Group,
Back Link, superfícies da ficha/histórico e a hierarquia que os testes P5
descrevem. O teste baseline test_detail_uses_canonical_regions_and_removes_legacy_presentational_classes
afirma essa composição. A diferença é principalmente a implementação CSS
local versus declarations compartilhadas e funcionalidades acrescidas após
c91bc6d.

O template P5 de c91bc6d antecede captura/galeria E4 e diagnóstico técnico A–D
do baseline. Ele remove esses conteúdos e estilos. Copiar o template ou CSS P5
integralmente regrediria funcionalidades do checkpoint. Portanto, a
composição visual P5 é ALREADY_PRESENT; as diferenças semânticas e a eventual
promoção global do DS ficam sob decisão humana.

## 2. Reconciliação DS 2.0.2–2.4

O baseline declara DS 2.0.2 nas folhas globais. Os estilos usados pela Camera
Detail P5 estão em regras escopadas de camera-detail.css. A ausência da API
global não equivale à ausência da apresentação funcional da tela.

| Versão | Funcionalidades e aprovação | Implementação/publicação | Presença no baseline | Dependência P5, impacto e validação |
|---|---|---|---|---|
| 2.1.0 | Data Pair, Data Group, Compact Empty State e Button Danger; STAT GROUP deferred. Aprovação do usuário em 2026-10-05. | Implementada/validada localmente em P5 (§46; 22 assertions de browser, 1280×900 e 390×844). Sem publicação autônoma identificada. As declarações aparecem no tree de b9cdc00, publicado como 2.2 cumulativo na branch P5. | As declarations globais estão ausentes. Equivalentes page-scoped existem para data pair/group, estado compacto e botão danger. | A página usa todas, exceto STAT GROUP. O scan de templates de produção encontrou esses nomes somente na Camera Detail. Se as regras forem movidas para layers globais, validar renderização e rotas consumidoras. |
| 2.2.0 | .argos-text-kpi, usando o token --argos-text-kpi existente. | Aprovada/implementada/publicada no commit b9cdc00, segundo §49 P5. O checkpoint contém as declarações acumuladas de 2.1. | Utility pública ausente; token e uso do token no KPI existente permanecem. | Camera Detail não usa .argos-text-kpi no template/CSS. Não é dependência P5; não incluir como se necessário fosse. |
| 2.3.0 | .argos-back-link declara cor, tamanho e peso; foco/hover permanecem no base. | §50 registra PUBLISHED, PUSH PASS e commit 18e9326. A branch P5 contém o commit. Cabeçalho de DSCR-UIV2-005 ainda diz NOT PUBLISHED. | A regra global está ausente; o template usa a classe e camera-detail.css fornece os mesmos tokens/valores por seletor escopado. 18e9326 não é ancestral de ddd8f163. | É usado pelo link de retorno. Se migrado para patterns global, validar link, foco e hover e revisar consumidores globais. Corrigir o cabeçalho contratual em revisão documental própria. |
| 2.4.0 | .argos-section-surface define só fundo, borda, raio e padding com tokens existentes. | Implementada localmente e não publicada (§51–52). DSCR-UIV2-006 mantém USER_REAPPROVAL_REQUIRED=PENDING. §54 registra aprovação visual humana do preview local, mas também PRODUCT_DESIGN_QA=BLOCKED, arquivo de capturas incompleto e ACTIVITY_COMPLETE=NO. | A classe está no template, mas não tem declaração global. Record/history surfaces são estilizadas localmente com as quatro propriedades e tokens da página. | P5 usa a classe em ficha/histórico; a aparência já é fornecida localmente. Não há necessidade de promoção global para manter o layout. O gate formal exige decisão humana antes de publicar. |

### Decisão recomendada para DS

Não substituir as folhas globais nem atualizar a versão do baseline para 2.4.0
nesta consolidação. Manter os estilos page-scoped evita regressão e preserva o
contrato visual já representado no alvo. Uma promoção cumulativa até 2.3 é
mudança separada do Design System, sujeita a decisão explícita de versão e
validação. 2.2 não é necessário para P5. 2.4 continua bloqueado até a
adjudicação formal da divergência entre a aprovação de preview §54 e o gate
pendente no DSCR-UIV2-006.

## 3. Arquivos P5 e comparação com o baseline

Os cinco caminhos da implementação P5 em c91bc6d foram comparados com
ddd8f163. Somente três diferem em conteúdo.

| Caminho relativo | Diferença observada e alterações aprovadas | Decisão proposta |
|---|---|---|
| cameras/templates/cameras/detalhe.html | Difere. A composição principal já existe no baseline. O source P5 remove Diagnóstico técnico A–D e substitui upload + captura + galeria atuais por upload manual apenas; também altera a apresentação de fora de escopo e do estado confirmado vazio. | ALREADY_PRESENT para a composição. Não substituir. Adjudicar diferenças de estado separadamente, preservando diagnóstico, capture flow, galeria, permissões e contratos atuais. |
| cameras/templates/cameras/partials/_monitoring_badge.html | Blob idêntico ao baseline. | ALREADY_PRESENT; nenhuma cópia/edição. |
| cameras/test_frontend.py | Difere. Testes P5 verificam regiões, ordem, formulário e badge; baseline já tem as principais asserções de composição e também casos adicionais de fora de escopo, configuração incompleta e semântica dos badges. P5 reduz a classe baseline de nove métodos para seis. | Manter os testes baseline. Acrescentar apenas assertions não equivalentes, nunca substituir o conjunto. |
| static/css/argos.css | Blob idêntico ao baseline. | ALREADY_PRESENT; nenhuma cópia/edição. |
| static/css/ui-v2/camera-detail.css | Difere. P5 remove estilos locais depois substituídos por DS global e reduz Operações complementares para upload. Baseline preserva equivalentes page-scoped e CSS do diagnóstico, captura e galeria. | ALREADY_PRESENT para a composição visual. Não substituir; eventual ajuste seletivo precisa preservar E3/E4 e A–D. |

### Matriz de dependências

| Capacidade | Uso P5 | Baseline | Dependência de código novo para manter visual |
|---|---|---|---|
| .argos-back-link | Link de retorno | Classe e regra page-scoped equivalentes presentes; API global ausente | Não |
| .argos-data-pair | Pares label/value | Classe e estilos page-scoped presentes | Não |
| .argos-data-group | Agrupa pares | Classe e grid/gap page-scoped presentes | Não |
| .argos-button--danger | Ação destrutiva | Estilo e hover page-scoped presentes | Não |
| .argos-state--compact | Estados vazios históricos | Variante page-scoped presente | Não |
| .argos-section-surface | Ficha e histórico | Classe no markup; styles record/history page-scoped presentes | Não; promoção global 2.4 segue pendente |
| .argos-text-kpi | Sem uso na Camera Detail | Utility global ausente; token KPI presente | Não |

O scan encontrou os novos nomes globais de produção somente na Camera Detail.
As declarações atuais são específicas da página. Promoção para API compartilhada
não é uma cópia mecânica dos cinco arquivos P5.

### Testes e evidência existentes

O registro P5 §54 informa 17/17 testes focados históricos, incluindo Camera
Detail, Quick Detail e regressões stale/non-stale; a suíte ampliada teve 25/26,
com falha de Inventory fora do diff. Não foram reexecutados no P0.

§54 registra aprovação humana em 2026-10-07 para o preview P5 local. O arquivo
de capturas está incompleto: o JPEG arquivado mede 1265×712, não os quatro
viewports solicitados; o pareamento com source visual permaneceu bloqueado.
Essa evidência é da composição P5 daquele preview, não da tela atual com E3/E4,
nem fecha o gate global de DS 2.4.

## 4. Preservação local

A matriz reutiliza contagens e caminhos da C1. Nenhum conteúdo local foi aberto,
copiado ou movido. UNKNOWN orienta tratamento e não afirma que um arquivo contém
segredo. Nenhum item foi provado REBUILDABLE nesta C2-A.

| SOURCE_WORKTREE | ARTIFACT_CATEGORY | RETENTION_REQUIREMENT | REBUILDABILITY | BACKUP_REQUIREMENT | SENSITIVITY | PROPOSED_ACTION | HUMAN_DECISION_REQUIRED |
|---|---|---|---|---|---|---|---|
| C:\Users\walac\desenvolvimento\projeto_argos_hom_integration | 19 SQLite ignorados; .local, settings e logs | Preservar na origem até adjudicação | UNKNOWN | Nenhum agora. Antes de futura remoção: backup consistente fora do Git, ACL restrita e manifesto mínimo, após autorização | UNKNOWN / tratar como potencialmente sensível | Não abrir/copiar/exportar/mover nem incluir no Git | Sim para backup, leitura, transporte ou remoção |
| Mesmo worktree hom_integration | Scripts/launchers QA e WIP documental E4 | PRESERVE_REQUIRED | UNKNOWN até revisão por arquivo | Manter original; backup protegido se remoção for autorizada | UNKNOWN; scripts/settings não revisados | Preservar; revisar arquivo por arquivo antes de portar ou reconstruir | Sim |
| C:\Users\walac\desenvolvimento\projeto_argos_ui_p5 | Dois SQLite ignorados | Preservar no worktree P5 de origem | UNKNOWN | Nenhum agora; backup consistente somente após autorização específica | UNKNOWN / potencialmente sensível | Não abrir ou mover | Sim |
| Mesmo worktree P5 | Cinco screenshots e settings locais de QA | Screenshots: preservar evidência original; settings: preservar fora do Git | Screenshots não são substituíveis sem nova evidência; settings devem ser reprovisionados por ambiente | Nenhum backup/export nesta rodada | SENSITIVE_LOCAL; registros de câmera, MAC/IP e config SQLite | Manter protegidos na origem; sem ZIP/GitHub | Sim |
| C:\Users\walac\desenvolvimento\projeto_argos | Um SQLite, ZIP de continuidade e branch UI-WIP | Preservar estado local | UNKNOWN | Sem backup agora; retenção local | UNKNOWN | Não abrir ZIP/DB, trocar branch ou remover worktree | Sim |
| Worktree ui-03-visual-completion | Seis alterações rastreadas e 28 arquivos não rastreados de QA/evidência | Preservar WIP; classificar evidência antes de limpeza | UNKNOWN | Backup protegido se remoção for autorizada e item não for reconstruível | UNKNOWN | Manter origem; separar por nome/finalidade sem abrir dados sensíveis | Sim |
| Worktree ui-03-density-refinement | Dezoito screenshots não rastreados | PRESERVE_REQUIRED até verificar aprovação e proveniência | UNKNOWN | Preservar originais; sem exportação em lote | UNKNOWN até revisão | Manter; capturas só passam a REBUILDABLE após fonte segura e reprodução confirmadas | Sim |
| Worktree ui-v2-p3-root | Protótipos e oito screenshots P3 integrados aprovados | PRESERVE_REQUIRED | Não reconstruir como se fosse source; preservar proveniência histórica | Reter commits e arquivos originais | Evidência local; não publicar sem revisão de identificadores | Preservar como protótipo/evidência, sem conversão a produção | Sim para promoção de protótipos |
| Worktree mon_runtime_v1 | WIP documental e script de QA local | PRESERVE_REQUIRED até revisão | UNKNOWN | Manter origem; backup se remoção autorizada | UNKNOWN; script não executado nem copiado | Adjudicar texto/script individualmente; não sobrescrever contrato vigente | Sim |
| Worktree P0 | WIP documental atual, relatórios C1 e este relatório | PRESERVE_REQUIRED | Não classificado como reproduzível | Reter no worktree e revisar antes de publicação | Documental; nenhum segredo adicionado | Preservar diffs existentes; documentação permanece não commitada | Sim para publicar |
| Caches/temporários ignorados não adjudicados | Saídas candidatas à reconstrução | UNKNOWN até identificação item a item | REBUILDABLE somente após validação | Backup não é necessário apenas se comprovadamente recriável; dados QA exigem procedimento próprio | UNKNOWN | Não remover por extensão ou por ser ignored; provar finalidade, dependências e reconstrução | Sim antes de remover/recriar |

### Procedimento antes de remover qualquer worktree no futuro

1. Registrar caminho absoluto, raiz Git, branch, HEAD, status rastreado/não
   rastreado e contagem de ignorados, sem abrir bancos, credenciais, sessões ou
   settings.
2. Classificar cada caminho por finalidade, valor de evidência, sensibilidade,
   dependências e reconstrução comprovável. Incerteza permanece UNKNOWN.
3. Obter autorização específica para backup/cópia. Guardar fora do Git, com ACL
   restrita; o manifesto registra origem, tamanho, hash e data, sem credenciais.
   SQLite requer cópia consistente e verificação isolada, sem mutar a origem.
4. Manter screenshots brutos locais; não criar ZIP para publicação GitHub.
   Segredos devem ser reprovisionados diretamente no host.
5. Confirmar hashes, recuperação de itens necessários e ausência de dependência
   aberta. Só então submeter eventual remoção a gate humano separado. C2-A não
   executou backup ou remoção.

## 5. Especificação proposta para C2-B/C2-C

Esta especificação não concede autoridade de implementação. A C2-B só começa
após revisão deste relatório e autorização explícita.

| Item | Plano fechado proposto |
|---|---|
| Baseline | Exigir ddd8f163992fc3cfda25a37d65199e25c249ee72 e registrar raiz/HEAD/status. P0 está detached nesse SHA. |
| Cinco arquivos de origem | São referência, não lista para copiar em bloco. _monitoring_badge.html e argos.css são idênticos ao alvo. |
| Arquivos candidatos de código | detalhe.html, camera-detail.css e test_frontend.py somente para deltas aprovados. Preservar capture/gallery E3/E4, diagnóstico A–D, permissões, Quick Detail, URLs, CSRF, IDs e atributos consumidos por JS. |
| DS compartilhado | Não substituir bundle. Promoção cumulativa 2.1–2.3 em components.css/patterns.css é opcional e requer decisão explícita sobre versão/escopo e regressão de rotas. Não incluir .argos-section-surface enquanto o gate 2.4 estiver aberto. tokens.css/base.css não têm mudança funcional necessária para P5. |
| Mudança P5 | Composição canônica já está presente; não transplantar o template/CSS c91bc6d. Se uma diferença aprovada for selecionada, mudar somente o trecho necessário e manter as funcionalidades atuais. |
| Quick Detail | Não alterar serviço, template, JS, hooks, timestamp ou imagem. Executar regressão funcional e confirmar visualmente isolamento de CSS. |
| Testes | Rodar CameraDetailFrontendTests; cameras.test_frontend; cameras.test_quick_detail; cameras.test_quick_detail_preview; cameras.test_monitoramento_ui; cameras.test_camera_health_projection; cameras.test_camera_diagnostics; cameras.test_imagens_capture_views; cameras.test_imagens_capture_service; cameras.test_imagens_capture_worker; cameras.test_imagens_gallery_views; cameras.test_imagens_gallery_service; manage.py check. Manter os casos baseline de fora de escopo, config incompleta e semântica dos estados. |
| Aceite visual | Revisar a tela atual com E3/E4 em 1920×1080, 1440×900, 1366×768 e 390×844, zoom 100%, DPR 1; sem overflow horizontal no documento; ordem mobile aprovada; breakpoints 901/900/899; foco visível e texto integral. Obter aprovação humana do conjunto atual. Não exportar screenshots sensíveis locais. |
| Gate 2.4 | Resolver formalmente se a aprovação de preview §54 fechou a reaprovação e concluir evidência pareada/QA antes de promover declaração global. Até lá, manter CSS da página. |
| Rollback | Executar isoladamente no P0 e guardar diff exato/manifest apenas dos caminhos autorizados. Reverter somente hunks desta atividade via patch inverso revisado. Não usar reset/clean nem sobrescrever WIP local/documental. |
| Branch operacional | Só após C2-B/C2-C aprovadas e preservação do WIP/dados. hom_integration está em df582ade e sujo conforme C1. Atualização exige gate próprio; sem merge/cherry-pick automático. Commit/push requerem autorização própria. |
| Pasta canônica | Preparar somente após alinhamento da branch e verificação do plano de dados locais. Nenhum cutover é autorizado em C2-A. |

## 6. Risco e prontidão

- **Integração de código:** risco alto se diff de hash for tratado como feature
  ausente e a fonte anterior a E4/A–D for copiada integralmente.
- **Design System:** risco moderado de efeito global ao mover estilos; alto se
  DS 2.4 for publicado sem resolver seu gate. Estilos locais isolam a tela hoje.
- **Testes:** risco moderado de reduzir cobertura se a classe baseline for
  substituída pelos seis testes P5, eliminando casos atuais.
- **Dados:** risco alto de perda/exposição; 17 worktrees têm SQLite ignorado e
  artefatos QA permanecem desconhecidos. Git não protege esses dados.
- **Evidência visual:** aprovação P5 registrada é de preview anterior. A
  captura arquivada não cobre os quatro viewports; E3/E4 requer nova revisão.
- **Pasta/branch:** permanecem NOT_READY conforme C1. projeto_argos segue na
  branch UI-WIP; hom_integration está em codex/hom-v1-integration @ df582ade,
  atrás do checkpoint e com WIP/dados locais.

**SINGLE_OPERATIONAL_FOLDER:** projeto_argos / objetivo retido / sem cutover
**SINGLE_OPERATIONAL_BRANCH:** YES / objetivo retido / ainda não alinhada
**AUTOMATIC_WORKTREE_CREATION:** NO
**DELETE_WORKTREES / DELETE_BRANCHES / RESET_OR_CLEAN:** NO
**CODE_MODIFICATION / DATABASE_MUTATION / VM_MODIFICATION:** NO
**TESTS_EXECUTED:** NO
**COMMIT_OR_PUSH:** NO
**ROADMAP_OR_SPRINTS_UPDATED:** NO / nenhuma etapa de produto mudou
**PROJECT_STATE_UPDATE:** PASS / PROJECT_STATE.md §172
**ACTIVITY_COMPLETE:** YES / análise e plano somente
**NEXT_GATE:** C2A_REVIEW_AND_C2B_EXECUTION_AUTHORIZATION

**Fim da C2-A.** A conclusão não inicia C2-B, não declara P5/DS 2.4 publicados
ou integrados, não torna a pasta/branch operacional pronta e não autoriza
excluir worktrees.


---

### Nota de proveniência e numeração na master

Este relatório preserva o registro produzido no worktree documental de origem. As referências internas às seções de PROJECT_STATE.md, AGENT_CONTINUITY.md e ACTIVE_DOCUMENT_MAP.md seguem a numeração daquele snapshot. Na pasta master, PROJECT_STATE.md §170 foi preservada como o registro C3-B já existente; a reconciliação canônica posterior está em PROJECT_STATE.md §171 e é indexada em ACTIVE_DOCUMENT_MAP.md §130. Esta nota resolve a proveniência sem renumerar nem duplicar os registros históricos. O worktree de origem não foi modificado.

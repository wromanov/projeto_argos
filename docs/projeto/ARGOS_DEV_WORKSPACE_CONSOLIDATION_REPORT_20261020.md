# ARGOS — Auditoria e plano de consolidação do ambiente

ACTIVITY_ID: ARGOS-DEV-WORKSPACE-CONSOLIDATION-01
Data: 2026-10-20
Fase: INVENTORY_AND_RECONCILIATION_PLAN
Modo: DIRECT
Repositório Git comum: C:/Users/walac/desenvolvimento/projeto_argos_e3_p0_reconciliation
Branch operacional candidata: codex/hom-v1-integration
Ref local de checkpoint: origin/codex/hom-v1-integration @ ddd8f163992fc3cfda25a37d65199e25c249ee72

## Resumo executivo

- Inventário local: 36 branches locais, 20 branches remotas em refs locais e 25 worktrees vinculadas ao mesmo repositório.
- No snapshot inicial, 6 worktrees tinham alterações rastreadas e/ou arquivos não rastreados: 19 arquivos rastreados modificados e 80 não rastreados. O relatório e as atualizações documentais desta atividade tornam o worktree P0 também sujo; o estado atual pós-relatório é 7 worktrees com WIP.
- 19 worktrees contêm arquivos ignorados pelo Git; 17 contêm banco SQLite ignorado, incluindo 19 bancos sob o checkout de homologação. Esses arquivos não foram abertos.
- O SHA ddd8f163 foi informado pelo usuário como último checkpoint publicado e coincide com HEAD do worktree P0 e com a ref local origin/codex/hom-v1-integration. Não houve fetch nem consulta ao remoto ao vivo. PROJECT_STATE.md §169 e ACTIVE_DOCUMENT_MAP.md §129 ainda refletiam o snapshot pré-publicação; este relatório supersede somente essa pendência documental.
- A pasta canônica C:/Users/walac/desenvolvimento/projeto_argos existe, porém está em codex/argos-ui-v2-wip-20261008 @ fea031d, 2 commits exclusivos e 44 atrás do checkpoint, com um ZIP não rastreado e um SQLite ignorado. Não está pronta para ser substituída ou convertida.
- O checkout da branch operacional candidata está em C:/Users/walac/desenvolvimento/projeto_argos_hom_integration, em df582ade, dois commits atrás do checkpoint e com 5 arquivos rastreados modificados, 25 não rastreados e 19 bancos SQLite ignorados.
- Nenhuma exclusão, troca de branch, merge, cherry-pick, alteração de código, migration, commit, push ou ação em VM foi executada. Nenhum conteúdo de banco, credencial, log ou imagem local foi aberto.

CANONICAL_FOLDER_READINESS = NOT_READY
CANONICAL_BRANCH_READINESS = NOT_READY / CANDIDATE_REQUIRES_WIP_RECONCILIATION_AND_FAST_FORWARD
NEXT_GATE = HUMAN_CLEANUP_APPROVAL

## Método, referência e limites

A comparação usa como alvo a ref local origin/codex/hom-v1-integration em ddd8f163. A ref coincide com o SHA publicado informado pelo usuário; as refs remotas locais não foram atualizadas nesta auditoria. As contagens ahead/behind são relativas a esse alvo. A contagem patch-unique usa git cherry e complementa ancestry; patches equivalentes por squash ou mudanças semânticas são classificados separadamente, não presumidos.

Para worktrees foram lidos raiz, branch, HEAD, estado Git e somente nomes/contagens de arquivos ignorados. Para conteúdo funcional foram comparados paths, existência e hashes de blobs selecionados, além dos snapshots documentais de continuidade. Bancos, screenshots, logs, settings locais e credenciais não foram lidos. A matriz de worktrees registra o estado antes da criação deste relatório; o WIP documental produzido nesta atividade está declarado separadamente.

## Auditoria funcional

| Área | Classificação | Evidência e encaminhamento |
|---|---|---|
| UI V2 / Design System | ALREADY_INTEGRATED parcialmente; UNMERGED_VALID_WORK em P5 | static/css/ui-v2/base.css e components.css coincidem entre checkpoint e P3 ROOT. Componentes, templates e CSS da produção P5 divergem. Revisar seletivamente sob direção C já selecionada; não substituir a implementação atual por cópia integral de branch. |
| Dashboard e inventário | UNMERGED_VALID_WORK / protótipos | P3-A está documentada como aprovada, publicada e validada no P3 ROOT, com evidência visual; o estado P3 registra que isso fecha a fase de protótipos, não a implementação de produção. Preservar família P3 e avaliar a transição P4/P5 antes de integrar source. |
| Quick Detail | ALREADY_INTEGRATED para serviço funcional | cameras/quick_detail.py tem o mesmo blob no checkpoint, UI-WIP, P3 ROOT e P5. Mudanças de composição e CSS ficam em avaliação visual separada. |
| Detalhe de câmera | UNMERGED_VALID_WORK / revisão requerida | codex/ui-v2-p5-production tem 14 commits exclusivos relativos ao alvo e implementação local com aprovação visual registrada; o estado P5 mantém ACTIVITY_COMPLETE=NO por dívida de evidência e arquivo de screenshots incompleto. Preservar código, capturas e configuração local. |
| Galeria E4 | ALREADY_INTEGRATED | gallery_service.py e gallery_preview_service.py estão presentes no checkpoint publicado; histórico de checkpoint e QA E4 estão registrados em PROJECT_STATE.md §165. |
| QA local | LOCAL_UNCOMMITTED_WORK / SENSITIVE_LOCAL_DATA | O checkout hom_integration tem WIP em launchers e scripts QA, arquivos temporários e 19 bancos SQLite ignorados. Preservar integralmente e não transportar bancos, sessões ou settings para outra estação. |
| CAM-INT-01/02/03/05/06/07 | ALREADY_INTEGRATED por ancestry | Os tips locais dessas branches são ancestrais do checkpoint. Revisões de conteúdo no target podem ser posteriores; não manter worktrees só para preservar histórico já alcançável. |
| CAM-INT-04 / capture jobs | ALREADY_INTEGRATED parcialmente; UNKNOWN_REQUIRES_REVIEW para diferenças | O checkpoint contém worker e adapter HTTP Snapshot com blobs idênticos aos do branch CAM-INT-04; o serviço de captura e adapter RTSP diferem, e o target usa migrations 0020/0021 enquanto o branch antigo tem migration 0018. PROJECT_STATE.md §168 confirma HTTP Snapshot e registra que RTSP Frame ainda não é consumido pelo serviço. Comparar comportamento e testes antes de descartar o branch antigo. |
| Monitoramento | ALREADY_INTEGRATED parcialmente; UNKNOWN_REQUIRES_REVIEW documental | mon-obs-observability e mon-runtime-v1 são ancestrais do alvo. mon-runtime-contract-closure tem um commit documental exclusivo e quatro contratos com blobs diferentes dos do target; fazer reconciliação sem reverter a versão vigente. |
| Autenticação e permissões | ALREADY_INTEGRATED por ancestry | bc-auth-implementation, CAM-INT-02 e BC-02 são ancestrais do checkpoint. cameras/authorization.py tem blob igual no alvo e nos branches verificados. |
| Contratos E3 RTSP | ALREADY_INTEGRATED no checkpoint informado | C01–C06 aparecem promovidos na linha documental atual; o usuário informou publicação em ddd8f163 e a ref local origin coincide. P1 continua não autorizada; F02/F03 e decisão C04 permanecem pendentes conforme §169. Não houve confirmação remota ao vivo. |
| Continuidade e governança | LOCAL_UNCOMMITTED_WORK / documentos divergentes | §169 e §129 conservavam “push pendente”. Esta atividade registra a confirmação do usuário e a coincidência da ref local, sem alterar política global. Os WIPs de continuidade em outros worktrees seguem separados e preservados. |
| Dependabot remoto | UNKNOWN_REQUIRES_REVIEW | Dois refs remotos só existem no cache local, cada um com um commit exclusivo; revisar estado de PR/necessidade em outra etapa antes de qualquer limpeza de refs remotas. |

## Matriz dos 25 worktrees

Delta = commits locais à frente/atrás do alvo. “WIP” descreve status Git normal antes deste relatório; “ignorados” conta arquivos ignorados, sem leitura de conteúdo. DB indica quantos arquivos de banco ignorados foram encontrados pelo nome.

| Caminho | Branch / HEAD | Delta | Estado e dados locais | Ação / risco |
|---|---|---:|---|---|
| C:/Users/walac/desenvolvimento/projeto_argos | codex/argos-ui-v2-wip-20261008 / fea031d | 2/44 | WIP: 0 rastreados, 1 não rastreado; 10178 ignorados, 1 DB | Preservar; branch divergente e ZIP local; não substituir. |
| C:/Users/walac/.codex/.chatgpt-projects/g-p-6a8267fea5e4819189e0b4fc769a41ee/argos-ui-03-visual-completion | codex/ui-03-visual-completion / c113abe | 0/141 | WIP: 6 rastreados, 28 não rastreados; 76 ignorados, 1 DB | Preservar CSS, documentos, protótipo e evidência visual; avaliar depois. |
| C:/Users/walac/.codex/worktrees/argos-img-display-01/projeto_argos | codex/img-display-01-implementation / 4bcd81d | 0/135 | Limpo; 81 ignorados, 1 DB | Candidato técnico de remoção após preservação do DB e aprovação humana. |
| C:/Users/walac/.codex/worktrees/argos-ui-03-density-refinement/projeto_argos | codex/ui-03-density-refinement / 2c802fc | 0/139 | WIP: 0 rastreados, 18 não rastreados; 76 ignorados, 1 DB | Preservar evidência visual; não excluir. |
| C:/Users/walac/.codex/worktrees/argos-ui-remediation-phase-0/projeto_argos | codex/ui-remediation-phase-0 / baa51c6 | 0/130 | Limpo; 76 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/.codex/worktrees/ui-v2-p3-a-home-evidence/projeto_argos | codex/ui-v2-p3-a-core-inventory / 36ad10d | 12/93 | Limpo; nenhum ignorado | Preservar na adjudicação da família P3; commits estão contidos no P3 ROOT. |
| C:/Users/walac/desenvolvimento/projeto_argos_bc_02_integration | codex/bc-02-integration / ccc0267 | 0/40 | Limpo; 112 ignorados, sem DB identificado | Candidato técnico após revisão de artefatos locais e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_bc_auth | codex/bc-auth-implementation / 55651d2 | 0/80 | Limpo; 82 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_health | codex/cam-health-implementation / 6ef2f70 | 0/42 | Limpo; 99 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_01 | codex/cam-int-01-capability-catalog / 75cdf70 | 0/74 | Limpo; 88 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_02 | codex/cam-int-02-camera-credentials / e4a2167 | 0/72 | Limpo; 79 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_03 | codex/cam-int-03-implementation / c031ea4 | 0/54 | Limpo; 104 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_04 | codex/cam-int-04-implementation / f9b9728 | 8/44 | Limpo; 99 ignorados, 1 DB | Preservar até revisar diferenças do capture_service e RTSP adapter; 6 patches exclusivos. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_05 | codex/cam-int-05-implementation / 68d593d | 0/43 | Limpo; 9411 ignorados, 1 DB | Candidato técnico após preservar DB/ambiente e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_06 | codex/cam-int-06-implementation / 07c8114 | 0/67 | Limpo; 91 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_cam_int_07 | codex/cam-int-07-target-hardening / 4db5536 | 0/77 | Limpo; nenhum ignorado | Candidato técnico após aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_e3_p0_reconciliation | detached / ddd8f16 | 0/0 | Limpo no snapshot inicial; nenhum ignorado | Worktree desta auditoria; agora contém as atualizações documentais não commitadas. Preservar. |
| C:/Users/walac/desenvolvimento/projeto_argos_hom_integration | codex/hom-v1-integration / df582ad | 0/2 | WIP: 5 rastreados, 25 não rastreados; 7994 ignorados, 19 DB | Preservar integralmente; não mover nem substituir; dados locais de QA. |
| C:/Users/walac/desenvolvimento/projeto_argos_mon_obs | codex/mon-obs-observability / 6fc4f70 | 0/77 | Limpo; 115 ignorados, 1 DB | Candidato técnico após preservar DB e aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_mon_runtime | codex/mon-runtime-contract-closure / 22c9e3a | 1/44 | Limpo; nenhum ignorado | Preservar contrato documental exclusivo até reconciliação. |
| C:/Users/walac/desenvolvimento/projeto_argos_mon_runtime_v1 | codex/mon-runtime-v1-implementation / 4ff2a92 | 0/37 | WIP: 8 rastreados, 2 não rastreados; 9388 ignorados, 1 DB | Preservar alterações documentais e auditoria local; não sobrescrever. |
| C:/Users/walac/desenvolvimento/projeto_argos_style_lab | codex/ui-v2-p1-style-lab / bbf89ca | 0/105 | Limpo; nenhum ignorado | Candidato técnico após aprovação humana. |
| C:/Users/walac/desenvolvimento/projeto_argos_ui_p5 | codex/ui-v2-p5-production / 4676a32 | 14/78 | WIP: 0 rastreados, 6 não rastreados; 5716 ignorados, 2 DB | Preservar; screenshots locais podem conter identificadores/MAC/IP segundo estado P5, e settings é local. |
| C:/Users/walac/desenvolvimento/projeto_argos_ui_v2_p3_b | codex/ui-v2-p3-b-monitoring-activities / 8006dad | 6/93 | Limpo; nenhum ignorado | Preservar na adjudicação da família P3; commits estão no P3 ROOT. |
| C:/Users/walac/desenvolvimento/projeto_argos_ui_v2_p3_root | codex/ui-v2-p3-root-reconciliation / e381df0 | 37/85 | Limpo; 52 ignorados, sem DB identificado | Preservar como consolidação aprovada da família P3; validar retenção de evidência. |

### WIP pré-existente por worktree

| Worktree | Rastreados modificados | Não rastreados | Conteúdo por nomes/status |
|---|---:|---:|---|
| projeto_argos (canônico atual) | 0 | 1 | Arquivo ZIP local de continuidade. |
| ui-03-visual-completion | 6 | 28 | Mudanças em CSS e continuidade; protótipo E4 e capturas de evidência. |
| ui-03-density-refinement | 0 | 18 | Capturas de antes/depois e QA visual. |
| hom_integration | 5 | 25 | Launcher/scripts QA, .local, logs/configuração isolada, artefatos E4 e documentos locais. |
| mon_runtime_v1 | 8 | 2 | Continuidade, contratos, auditoria documental e script de QA isolado. |
| ui_p5 | 0 | 6 | Cinco screenshots e settings QA local; conteúdo não aberto. |

## Matriz das 36 branches locais

Delta e patch-unique são relativos ao checkpoint. Os tips com 0 commits à frente são ancestrais do alvo. Branches limpas não são declaradas descartáveis sem considerar DBs ignorados e estado documental.

| Branch local | Tip | Ahead/behind | Patch + / equivalente | Worktree / leitura |
|---|---|---:|---:|---|
| codex/argos-ui-v2-wip-20261008 | fea031d | 2/44 | 2/0 | projeto_argos; WIP e conteúdo UI divergente; preservar/revisar |
| codex/bc-02-integration | ccc0267 | 0/40 | 0/0 | bc_02; integrado por ancestry |
| codex/bc-auth-implementation | 55651d2 | 0/80 | 0/0 | bc_auth; integrado por ancestry |
| codex/cam-health-implementation | 6ef2f70 | 0/42 | 0/0 | cam_health; integrado por ancestry |
| codex/cam-int-01-capability-catalog | 75cdf70 | 0/74 | 0/0 | cam_int_01; integrado por ancestry |
| codex/cam-int-02-camera-credentials | e4a2167 | 0/72 | 0/0 | cam_int_02; integrado por ancestry |
| codex/cam-int-02-r1-implementation | 80739e5 | 0/57 | 0/0 | sem worktree; candidato local após revisão |
| codex/cam-int-03-implementation | c031ea4 | 0/54 | 0/0 | cam_int_03; integrado por ancestry |
| codex/cam-int-04-implementation | f9b9728 | 8/44 | 6/0 | cam_int_04; preservar para comparação funcional |
| codex/cam-int-05-implementation | 68d593d | 0/43 | 0/0 | cam_int_05; integrado por ancestry |
| codex/cam-int-06-implementation | 07c8114 | 0/67 | 0/0 | cam_int_06; integrado por ancestry |
| codex/cam-int-07-target-hardening | 4db5536 | 0/77 | 0/0 | cam_int_07; integrado por ancestry |
| codex/hom-v1-integration | df582ad | 0/2 | 0/0 | hom_integration; WIP, branch local dois commits atrás da ref alvo |
| codex/img-display-01-implementation | 4bcd81d | 0/135 | 0/0 | img-display; integrado por ancestry |
| codex/mon-avail-01 | 323bfb0 | 0/121 | 0/0 | sem worktree; integrado por ancestry |
| codex/mon-obs-observability | 6fc4f70 | 0/77 | 0/0 | mon_obs; integrado por ancestry |
| codex/mon-runtime-contract-closure | 22c9e3a | 1/44 | 1/0 | mon_runtime; docs exclusivos, preservar/revisar |
| codex/mon-runtime-v1-implementation | 4ff2a92 | 0/37 | 0/0 | mon_runtime_v1; commits integrados, WIP local separado |
| codex/p5-camera-detail-production-conformance | 4a2d40d | 10/78 | 10/0 | sem worktree; ancestral de ui-v2-p5-production |
| codex/ui-03-density-refinement | 2c802fc | 0/139 | 0/0 | ui-03-density; commits integrados, evidência WIP |
| codex/ui-03-visual-completion | c113abe | 0/141 | 0/0 | visual-completion; commits integrados, CSS/evidência WIP |
| codex/ui-remediation-batch-a | deb0f3a | 0/123 | 0/0 | sem worktree; integrado por ancestry |
| codex/ui-remediation-batch-b | f494ff8 | 0/110 | 0/0 | sem worktree; integrado por ancestry |
| codex/ui-remediation-phase-0 | baa51c6 | 0/130 | 0/0 | remediation-phase-0; integrado por ancestry |
| codex/ui-v2-ds-2.0.1-hidden-semantics | 8121ed3 | 0/92 | 0/0 | sem worktree; integrado por ancestry |
| codex/ui-v2-ds-2.0.1-hidden-semantics-source | 094f626 | 1/93 | 1/0 | sem worktree; variante única, comportamento posterior em DS 2.0.2; revisão antes de limpeza |
| codex/ui-v2-ds-2.0.2-mobile-table-readability | 8a480a5 | 0/88 | 0/0 | sem worktree; integrado por ancestry |
| codex/ui-v2-p1-style-lab | bbf89ca | 0/105 | 0/0 | style_lab; integrado por ancestry |
| codex/ui-v2-p2-visual-foundation | 7277f16 | 0/103 | 0/0 | sem worktree; integrado por ancestry |
| codex/ui-v2-p3-a-core-inventory | 36ad10d | 12/93 | 11/1 | p3-a; preservado pelo P3 ROOT |
| codex/ui-v2-p3-b-monitoring-activities | 8006dad | 6/93 | 5/1 | p3-b; preservado pelo P3 ROOT |
| codex/ui-v2-p3-c-governance-audit | 52ae2c1 | 5/93 | 4/1 | sem worktree; preservado pelo P3 ROOT |
| codex/ui-v2-p3-d-forms-account-secondary | b4b4d7e | 3/93 | 2/1 | sem worktree; preservado pelo P3 ROOT |
| codex/ui-v2-p3-root-reconciliation | e381df0 | 37/85 | 33/0 | p3_root; integração P3 completa, protótipos apenas |
| codex/ui-v2-p5-production | 4676a32 | 14/78 | 14/0 | ui_p5; código exclusivo e WIP local sensível |
| master | 5bd22b0 | 0/44 | 0/0 | baseline; manter como referência do projeto |

Os tips remotos de P3-A/C/D são mais novos que os branches locais em 2/2/1 commits; todos estão incorporados no histórico do P3 ROOT. O P5 camera-detail conformance é ancestral de ui-v2-p5-production. O branch P3 ROOT contém os tips das quatro famílias A–D. Essas relações permitem manter um único branch de preservação por família depois da adjudicação, sem apagar evidências agora.

## Matriz das 20 branches remotas em cache local

Refs remotas são snapshots locais em origin; não equivalem a consulta atual do servidor. origin/HEAD é uma ref simbólica e não entra na contagem de branches.

| Ref remota | Tip | Ahead/behind do checkpoint | Patch + / equivalente | Encaminhamento |
|---|---|---:|---:|---|
| origin/codex/argos-ui-v2-wip-20261008 | fea031d | 2/44 | 2/0 | Mesmo grupo UI-WIP; preservar. |
| origin/codex/bc-02-integration | ccc0267 | 0/40 | 0/0 | Integrada por ancestry. |
| origin/codex/cam-health-implementation | 6ef2f70 | 0/42 | 0/0 | Integrada por ancestry. |
| origin/codex/cam-int-04-implementation | f9b9728 | 8/44 | 6/0 | Grupo CAM-INT-04; preservar até comparação. |
| origin/codex/cam-int-05-implementation | 68d593d | 0/43 | 0/0 | Integrada por ancestry. |
| origin/codex/hom-v1-integration | ddd8f16 | 0/0 | 0/0 | Checkpoint informado pelo usuário; ref local coincide. |
| origin/codex/mon-obs-observability | 6fc4f70 | 0/77 | 0/0 | Integrada por ancestry. |
| origin/codex/mon-runtime-contract-closure | 22c9e3a | 1/44 | 1/0 | Preservar/revisar contratos. |
| origin/codex/mon-runtime-v1-implementation | 4ff2a92 | 0/37 | 0/0 | Integrada por ancestry. |
| origin/codex/ui-v2-ds-2.0.1-hidden-semantics | 8121ed3 | 0/92 | 0/0 | Integrada por ancestry. |
| origin/codex/ui-v2-ds-2.0.2-mobile-table-readability | 8a480a5 | 0/88 | 0/0 | Integrada por ancestry. |
| origin/codex/ui-v2-p3-a-core-inventory | adc62fe | 14/93 | 13/1 | P3-A; tip contido no P3 ROOT. |
| origin/codex/ui-v2-p3-b-monitoring-activities | 8006dad | 6/93 | 5/1 | P3-B; tip contido no P3 ROOT. |
| origin/codex/ui-v2-p3-c-governance-audit | e96836c | 7/93 | 6/1 | P3-C; tip contido no P3 ROOT. |
| origin/codex/ui-v2-p3-d-forms-account-secondary | f5dd030 | 4/93 | 3/1 | P3-D; tip contido no P3 ROOT. |
| origin/codex/ui-v2-p3-root-reconciliation | e381df0 | 37/85 | 33/0 | Preservar família P3. |
| origin/codex/ui-v2-p5-production | 4676a32 | 14/78 | 14/0 | Preservar P5 e WIP local. |
| origin/dependabot/github_actions/actions-e91bde37dc | a97c191 | 1/44 | 1/0 | Remoto exclusivo; revisar status da PR antes de limpar. |
| origin/dependabot/pip/compatible-dependencies-7882619554 | a20b923 | 1/44 | 1/0 | Remoto exclusivo; revisar status da PR antes de limpar. |
| origin/master | 5bd22b0 | 0/44 | 0/0 | Baseline; manter. |

## Worktrees e branches candidatos a limpeza

WORKTREES_SAFE_TO_REMOVE = NONE nesta fase. A remoção não está autorizada e apagaria arquivos ignorados; 13 worktrees limpas têm código/histórico alcançável pelo alvo e são candidatas técnicas somente depois de preservar os DBs/ambientes locais e obter HUMAN_CLEANUP_APPROVAL: img-display-01, ui-remediation-phase-0, bc-02-integration, bc-auth, cam-health, CAM-INT-01, CAM-INT-02, CAM-INT-03, CAM-INT-05, CAM-INT-06, CAM-INT-07, mon-obs e style-lab. Dez dessas 13 têm db.sqlite3 ignorado. O worktree P0, atualmente usado para esta auditoria, permanece preservado até adjudicação desta documentação.

WORKTREES_REQUIRING_PRESERVATION = seis WIP pré-existentes; cinco worktrees limpas com conteúdo de commit exclusivo que exige revisão (CAM-INT-04, P3-A, P3-B, P3 ROOT, mon-runtime contract closure); todos os 17 worktrees que contêm DB SQLite ignorado exigem retenção dos bancos até adjudicação; e o P0 deve ser mantido enquanto esta atualização documental estiver não commitada. As categorias se sobrepõem.

BRANCHES_SAFE_TO_REMOVE = NONE nesta fase. Sete refs locais sem worktree têm tips alcançáveis pelo checkpoint e podem ser avaliadas após gate humano: codex/cam-int-02-r1-implementation, codex/mon-avail-01, codex/ui-remediation-batch-a, codex/ui-remediation-batch-b, codex/ui-v2-ds-2.0.1-hidden-semantics, codex/ui-v2-ds-2.0.2-mobile-table-readability e codex/ui-v2-p2-visual-foundation. Manter master. As refs remotas não foram classificadas como descartáveis e nenhuma exclusão remota está proposta.

## Risco e plano recomendado

RISK_ASSESSMENT = HIGH para perda de dados locais; MODERATE para regressão de integração funcional. O maior risco vem da mistura de código com WIP não commitado, screenshots locais, bancos SQLite ignorados e runtimes QA sob diferentes worktrees. P5 documenta que screenshots locais podem mostrar identificadores de câmera, MAC e IP; nenhum conteúdo de screenshot ou DB foi inspecionado.

1. Manter todos os worktrees e refs intactos até aceite humano; não trocar de branch nem substituir projeto_argos.
2. Registrar uma cópia local protegida ou decidir explicitamente retenção/reconstrução dos 17 conjuntos de bancos SQLite e dos dados .local de QA, sem transportar credenciais, sessões ou bancos entre máquinas.
3. Adjudicar os seis grupos locais de commits exclusivos: UI-WIP (2), CAM-INT-04 (8 commits de graph/6 patches únicos), contratos monitoramento (1), variante hidden-semantics (1), família P3 (37/33, A–D) e família P5 (14). Revisar também os dois commits remotos Dependabot e seu estado de PR.
4. Integrar somente mudanças aprovadas e necessárias, com comparação de código, contrato, histórico e regressão proporcional. Não promover protótipos à produção por inferência.
5. Validar codex/hom-v1-integration em ddd8f163 após decidir como preservar seu WIP; confirmar que a branch local fica sincronizada ao checkpoint informado sem sobrescrever os cinco arquivos e os artefatos locais.
6. Só então migrar a pasta operacional para C:/Users/walac/desenvolvimento/projeto_argos, preservando o branch/UI-WIP e o ZIP existente; validar branch, HEAD, status, arquivos ignorados e funcionalidades necessárias.
7. Após a validação na pasta canônica e HUMAN_CLEANUP_APPROVAL, remover worktrees candidatos e somente depois avaliar refs locais redundantes. Não apagar refs remotas nesta decisão.

NEXT_GATE = HUMAN_CLEANUP_APPROVAL
ATIVIDADE = 100% concluída para auditoria e planejamento; nenhuma limpeza executada.


---

### Nota de proveniência e numeração na master

Este relatório preserva o registro produzido no worktree documental de origem. As referências internas às seções de PROJECT_STATE.md, AGENT_CONTINUITY.md e ACTIVE_DOCUMENT_MAP.md seguem a numeração daquele snapshot. Na pasta master, PROJECT_STATE.md §170 foi preservada como o registro C3-B já existente; a reconciliação canônica posterior está em PROJECT_STATE.md §171 e é indexada em ACTIVE_DOCUMENT_MAP.md §130. Esta nota resolve a proveniência sem renumerar nem duplicar os registros históricos. O worktree de origem não foi modificado.

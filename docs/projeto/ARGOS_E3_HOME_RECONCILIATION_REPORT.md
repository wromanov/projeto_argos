# ARGOS — relatório de reconciliação P0 E3/HOME

    ACTIVITY_ID = ARGOS-E3-HOME-RECONCILIATION-01
    BASELINE = df582ade547358953cb1dee8113850ee5e186cb9
    WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos_e3_p0_reconciliation
    SCOPE = DOCUMENTATION_ONLY
    IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED

## Auditoria do WIP doméstico

| Item | Origem/finalidade provável | Estado/dependências | Equivalência/conflito com baseline | Classificação e destino |
|---|---|---|---|---|
| INICIAR_ARGOS_QA.cmd | Launcher QA local | Modificado; depende de scripts localqa e segurança Windows | Base existe, diff local requer revisão junto ao conjunto | REQUIRES_INTEGRATION — preservar no checkout doméstico |
| scripts/localqa/prepare_qa.py | Preparação QA | Modificado; lógica local | Equivalente rastreado, divergência local | REQUIRES_INTEGRATION — revisar com provisioning/settings |
| scripts/localqa/provisioning.py | Provisionamento QA | Modificado; dependências locais | Equivalente rastreado, possível divergência operacional | REQUIRES_INTEGRATION — revisar conjunto, sem copiar config |
| scripts/localqa/settings.py | Configuração runtime QA | Modificado; pode conter valores locais | Base rastreada, portabilidade não confirmada | KEEP_LOCAL_WIP — revisar sanitização antes de integração |
| scripts/localqa/start_argos_qa.ps1 | Inicialização/isolamento QA | Modificado substancialmente; Windows/DPAPI/serviços locais | Base rastreada com divergência | REQUIRES_INTEGRATION — revisão funcional e segurança |
| scripts/localqa/qa_admin.py | Administração QA | Novo, depende dos scripts/settings QA | Equivalente no HEAD não confirmado | REQUIRES_INTEGRATION — revisar API/permissões antes de integrar |
| scripts/localqa/qa_key_protection.ps1 | Proteção de chave QA | Novo; Windows/DPAPI provável | Equivalente no HEAD não confirmado | SENSITIVE_LOCAL_ARTIFACT — manter local; não transportar chaves |
| scripts/localqa/test_qa_admin.py | Testes do admin QA | Novo; depende de qa_admin/settings | Equivalente no HEAD não confirmado | READY_FOR_REVIEW — revisar com módulo; não executado nesta P0 |
| docs/projeto/ARGOS_LOCAL_QA_SETUP_CONTINUITY_RUNBOOK_V1.md | Continuidade setup doméstico | Novo documento acoplado ao host | Portabilidade/sanitização não confirmadas | KEEP_LOCAL_WIP — revisão local antes de promoção |
| .codex.zip | Pacote local de continuidade/configuração | ZIP não rastreado, não inspecionado | Conteúdo/equivalência indeterminados | SENSITIVE_LOCAL_ARTIFACT — manter fechado e local; inventariar em ambiente controlado |
| .local/ | Configuração, DBs, mídia, scripts e logs QA | Conjunto local misto; possível conteúdo sensível | Não é artefato de produto equivalente | SENSITIVE_LOCAL_ARTIFACT — manter no host; não copiar |
| .tmp-e4-gallery-qa-81e4738ac69e42adb0852a210c3cd77c/ | Execução QA visual/funcional E4 | DBs, mídia, scripts e logs temporários; validade não confirmada | Não substitui E4 publicado | KEEP_LOCAL_WIP — preservar até decisão de retenção |
| docs/prototype/ui-botao-captura/prototype/ARGOS_E4_GALLERY_REFINEMENT_V2.html | Protótipo visual E4 | Não rastreado; não representa aceite | E4 existe no HEAD; equivalência visual não confirmada | UNDETERMINED — comparar com UI aprovada antes de destino |

DUPLICATE_OR_SUPERSEDED não foi aplicado sem prova. READY_FOR_REVIEW não significa aprovação. Nenhum WIP foi removido, movido, extraído, copiado para este worktree ou publicado. Nenhum segredo ou valor local é reproduzido neste relatório.

## Estados separados

| Estado | Evidência |
|---|---|
| IMPLEMENTED_IN_REPOSITORY | Job/migrations 0020/0021, serviço/worker HTTP, diagnóstico RTSP e leitura/galeria E4 presentes em df582ade. RTSP não integrado ao capture service. |
| DEPLOYED_IN_HML | Release d44e4e6f reportada; VM não verificada nesta atividade. |
| VALIDATED_IN_HML | Smoke web reportado; captura RTSP e galeria E4 com imagem real não validadas. |
| OPERATIONALLY_ACCEPTED | Aceite de captura RTSP e imagem real E4 não estabelecido. |

## Recomendação

Manter o pacote no checkout doméstico. Revisar scripts/testes funcionais como conjunto antes de integração; manter configs, credenciais, bancos, mídia, .local, ZIP e temporários no ambiente local; revisar runbook e protótipo separadamente. Não mesclar automaticamente qualquer WIP.

## Estado final da P0 documental

```text
P0_DOCUMENTATION = READY_FOR_FINAL_ACCEPTANCE
C01_C06 = TECHNICALLY_REVIEWED
CANONICAL_AMENDMENTS = PENDING_FORMAL_USER_ACCEPTANCE
WIP_PRESERVED = YES
ROUND_1_IMPLEMENTATION = NOT_STARTED
ACTIVITY_COMPLETION_PERCENT = 100% / technical documentation complete; human acceptance and publication decision pending
```

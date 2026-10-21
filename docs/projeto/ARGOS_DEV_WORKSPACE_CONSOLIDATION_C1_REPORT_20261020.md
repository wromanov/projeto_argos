# ARGOS — Consolidação do ambiente e redução de worktrees — C1

**ACTIVITY_ID:** `ARGOS-DEV-WORKSPACE-CONSOLIDATION-C1`
**EXECUTION_MODE:** `DIRECT`
**WORKSTATION:** `HOME`
**SCOPE:** `READ_ONLY_ANALYSIS + PRESERVATION_PLAN`
**BASELINE:** `ddd8f163992fc3cfda25a37d65199e25c249ee72`
**AUTHORITATIVE_INPUT:** `docs/projeto/ARGOS_DEV_WORKSPACE_CONSOLIDATION_REPORT_20261020.md`
**DATE:** `2026-10-20`

```text
ACTIVITY_COMPLETION_PERCENT = 100%
EXCLUSIVE_CODE_REVIEW = COMPLETE / six groups adjudicated
VALID_FEATURES_TO_INTEGRATE = P5 Camera Detail production composition; shared DS promotion remains separately adjudicated
FUNCTIONAL_DUPLICATES = Quick Detail service; CAM-INT-04 HTTP Snapshot adapter and worker; global [hidden] rule
LOCAL_DATA_PRESERVATION_PLAN = COMPLETE / dados permanecem nos worktrees de origem; nenhum dado local foi aberto, copiado, exportado ou excluído
RECONCILIATION_ORDER = preserve local state → integrate approved P5 slice → adjudicate optional UI-WIP styling → retain current CAM capture implementation → reconcile monitoring documents → preserve P3 prototypes/evidence → no hidden-semantics patch → validate operational branch → cut over folder
CANONICAL_FOLDER_READINESS = NOT_READY
CANONICAL_BRANCH_READINESS = NOT_READY
RISK_ASSESSMENT = HIGH for local-data loss or exposure; MODERATE-to-HIGH for blanket integration/regression
NEXT_GATE = HUMAN_INTEGRATION_APPROVAL
```

## 1. Resultado e limites

O C1 identifica uma fatia de produção aprovada que falta no baseline: a implementação P5 de Camera Detail, com dependências compartilhadas de Design System 2.1–2.4 que ainda precisam ser reconciliadas com o Design System 2.0.2 presente no baseline. A aprovação visual P5 está registrada e o conjunto de tela foi publicado historicamente em `master`; os blobs da tela e do CSS, porém, diferem no checkpoint atual `ddd8f163`. O estado P5 distingue capacidades locais de capacidades publicadas: 2.1 foi aprovado e implementado localmente sem publicação própria identificada; 2.2 está publicado; §50 registra 2.3 publicado no commit `18e9326`, embora o cabeçalho do contrato 2.3 ainda diga `NOT PUBLISHED`; 2.4 foi autorizado e implementado localmente/não publicado, com reaprovação visual pendente no contrato. A proposta é integrar seletivamente a tela após gate humano, sem presumir que toda a linha DS possa ser promovida, preservando o Quick Detail e a UI de inventário atual.

CAM-INT-04 não oferece código de captura exclusivo que deva substituir o baseline: worker e adapter HTTP Snapshot são idênticos por hash; o serviço atual tem proteções e testes adicionais; e o branch antigo traz uma migration `0018` incompatível com a linha atual `0018`–`0021`. O frame RTSP continua fora do worker e permanece assunto dos gates E3 próprios; esta atividade não inicia P1.

UI-WIP, monitoramento, P3 e hidden semantics ficam preservados conforme seus papéis. UI-WIP altera controles e dados visíveis no inventário/Quick Detail sem evidência de aprovação para esta variante. P3 é protótipo aprovado com evidências, não código de produção. O comportamento global de `[hidden]` já está no baseline.

O plano não atualiza a pasta operacional, não troca branches, não cria worktrees/branches, não mescla nem aplica commits, não apaga arquivos e não executa testes. Bancos, screenshots, settings, logs, sessões, credenciais e ZIP local não foram abertos nem copiados. A análise funcional usou diffs, paths, hashes e documentos versionados; evidências de teste citadas abaixo são históricas e não foram reexecutadas.

## 2. Matriz de decisão — C1-A

| Grupo / funcionalidade ou artefato | Origem e presença no baseline | Diferença técnica e evidência de aprovação | Risco de regressão | Decisão e recomendação | Dependências de validação futura | Decisão humana necessária |
|---|---|---|---|---|---|---|
| **1 — P5 Camera Detail de produção** | `codex/ui-v2-p5-production`, `c91bc6d` (mesma implementação de `662e80e`). No baseline, `cameras/templates/cameras/detalhe.html` e `static/css/ui-v2/camera-detail.css` têm blobs diferentes. | O conjunto P5 aprovado cobre template da ficha, badge de monitoramento, CSS da tela e asserções de frontend. A continuidade §54 registra aprovação visual explícita em 2026-10-07; §56 registra publicação P5. A mesma §54 mantém `ACTIVITY_COMPLETE=NO` pela comparação pareada e pelo arquivo de screenshots incompleto. | **Moderado–alto:** composição da tela e CSS alteram hierarquia visual; divergência entre design system pode deixar classes sem estilo. | **`INTEGRATE`** — portar seletivamente o conjunto aprovado de cinco arquivos indicado na §61, reconciliando primeiro suas dependências de Design System; não aplicar o branch inteiro. | `CameraDetailFrontendTests`, `cameras.test_frontend`, Quick Detail, UI de monitoramento, `manage.py check` e revisão visual nas viewports exigidas pelo contrato. O registro histórico informa 17 focados e 101 integrados PASS; não foi repetido aqui. | **Sim:** aprovar o conjunto exato e a reconciliação das dependências compartilhadas. A aprovação visual da tela existe; ela não substitui a autorização desta futura integração ao baseline. |
| **1 — Padrões compartilhados P5 / DS 2.1–2.4** | No alvo, arquivos compartilhados de UI V2 identificam DS 2.0.2. Na linha P5: 2.1 está local sem publicação própria identificada; 2.2 publicado; §50 registra 2.3 publicado; 2.4 implementado localmente/não publicado. | `DSCR-UIV2-003` tem aprovação de usuário, mas implementação sem publicação própria identificada; `004` está publicado; o estado §50 registra 2.3 como publicado no commit `18e9326`, enquanto o cabeçalho de `DSCR-UIV2-005` ainda diz `NOT PUBLISHED`; `006` foi autorizado e implementado localmente, mas o contrato exige reaprovação visual e marca `NOT_PUBLISHED`. Camera Detail consome `.argos-back-link`, `.argos-data-pair`/`.argos-data-group` e `.argos-section-surface`; não é seguro copiar a tela sem resolver esses estilos. | **Alto se substituir globalmente:** afeta outras rotas e pode reverter melhorias do 2.0.2, inclusive legibilidade de tabelas; promover 2.4 sem fechar seu gate visual contraria o contrato. | **`REQUIRES_HUMAN_DECISION`** sobre quais dependências DS serão promovidas junto da tela P5. Não promover a linha inteira nem tratar 2.1/2.4 como publicada. | Revisar diffs e contratos de cada versão; validar rotas que carregam DS, telas P5 e correção de tabelas. 2.4 requer fechar a revisão visual indicada no próprio contrato antes de publicação. | **Sim:** escolher uma integração mínima compatível com P5 e resolver a divergência documental de 2.3 e o gate de 2.4. 2.2 e 2.3 têm publicação registrada, mas não estão presentes no baseline. |
| **1 — Quick Detail** | Serviço `cameras/quick_detail.py` idêntico por blob no baseline, UI-WIP, P3 ROOT e P5. O baseline mantém o timestamp visual e a estrutura atual. | Quick Detail é contrato protegido. A integração publicada P5 não exigiu bindings adicionais; §61 registra Quick Detail inalterado. | **Alto** se a estrutura, timestamp, serviço ou hooks forem substituídos incidentalmente. | **`ALREADY_PRESENT`** — manter o Quick Detail do baseline byte a byte nesta integração. | Regressão de `cameras.test_quick_detail`, `cameras.test_quick_detail_preview` e testes frontend já existentes, além de revisão visual se CSS compartilhado mudar. | **Não** para preservar o contrato atual; qualquer redesign ou mudança de composição exige decisão separada. |
| **2 — CAM-INT-04: HTTP Snapshot e worker** | Branch `codex/cam-int-04-implementation`, `f9b9728`; o hash do worker `run_capture_worker.py` e do adapter `http_snapshot/adapter.py` é igual ao baseline. O baseline contém job, serviço HTTP e worker atuais. | A branch histórica registra testes focados de HTTP/captura. O baseline acrescenta elegibilidade explícita, deduplicação/concorrência por câmera, regras de Target Policy/credenciais e cobertura para negar captura RTSP sem job. | **Baixo** para código idêntico; **alto** se substituir o serviço atual pelo histórico e perder proteções. | **`ALREADY_PRESENT`** para HTTP Snapshot/worker; manter os testes atuais. Não há funcionalidade CAM-INT-04 ausente identificada que justifique importar o pacote antigo. | Em integração futura, revisar testes atuais de capture service, worker, HTTP Snapshot, credenciais, Target Policy e estado das migrations. Não usar câmera real nesta etapa. | **Não** para manter o código atual. Decisão separada só se revisão posterior identificar requisito CAM-INT-04 ausente. |
| **2 — CAM-INT-04: serviço, RTSP adapter e migration histórica** | A branch antiga diverge de `capture_service.py`, `rtsp/gst_adapter.py`, `rtsp/ports.py`, `rtsp/service.py` e `models.py`. Ela possui `0018_cameracapturejob.py`; o baseline usa `0018_camera_health_snapshot`, `0019`, `0020_cameracapturejob` e `0021`. | O serviço no baseline possui `CaptureEligibility`, disponibilidade pública controlada e verificações adicionais ausentes na branch antiga. A cadeia antiga colide com a migration 0018 atual. A documentação corrente registra que RTSP Frame ainda não é consumido pelo serviço de captura. | **Alto:** regressão de política/credenciais, perda de guardrails, colisão de migration e falsa impressão de que RTSP está integrado ao worker. | **`PRESERVE_AS_ARCHIVE`** — reter commit e testes históricos; não substituir serviço, adapter RTSP, modelos ou migrations. Não converter a implementação antiga em solução P1. | Se houver requisito novo, abrir revisão CAM-INT-04 separada: contrato atual, migration graph, testes focados e análise de segurança; P1 RTSP fica fora deste plano. | **Sim** apenas para eventual requisito funcional novo. A recomendação C1 atual é não integrar a implementação antiga. |
| **3 — UI-WIP, dois commits** | `codex/argos-ui-v2-wip-20261008`: `8c79bfa` contém a fatia de UI e `fea031d` é documental. A pasta `projeto_argos` está nesta branch. | O commit WIP modifica shell/inventário e CSS. Comparado ao baseline, remove o link de importação condicional, o JSON de rótulos de monitoramento, timestamp do Quick Detail e regra visual de indisponibilidade; também muda larguras de tabela e restringe a aplicação do shell a rotas diferentes. O JavaScript do baseline consome `#monitoring-state-labels` e `[data-quick-detail-image-recorded-at]`; importar somente o template WIP deixa esses consumidores sem seus elementos. Não foi localizada aprovação para esta variante. | **Alto** se aplicada integralmente: regressão de importação/labels/timestamp, escopo de CSS alterado e impacto potencial em rotas fora do inventário. | **`PRESERVE_AS_ARCHIVE`** — manter os dois commits e o ZIP local; não usar como base operacional. Regras visuais isoladas só podem ser reavaliadas por requisito e comparação visual. | Frontend/inventário, importer, navegação/sidebar, Quick Detail e revisão visual responsiva se um subconjunto vier a ser proposto. | **Sim** para qualquer CSS visual que se queira resgatar; não há necessidade de decisão para rejeitar a aplicação integral nesta rodada. |
| **4 — Monitoramento: commit contratual** | `codex/mon-runtime-contract-closure`, `22c9e3a`, um commit exclusivo apenas documental. Quatro contratos têm hashes diferentes do baseline. | O commit registra fechamento local V1, mas contém estados históricos `OPEN/NOT_CLOSED` e `PROPOSED_PENDING_APPROVAL` antes da consolidação final. O contrato atual do baseline já contém `MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION`, `CLOSED / LOCAL V1 DECISIONS ONLY`, e esclarecimentos posteriores. Não há implementação do worker nesse commit. | **Alto** se documentos atuais forem substituídos por versões antigas ou se status históricos forem lidos como status corrente. | **`PRESERVE_AS_ARCHIVE`** — manter histórico. As decisões V1 já estão presentes no contrato atual; nenhuma substituição ou cherry-pick documental recomendado. | Revisão documental somente se uma decisão específica estiver ausente; em futura implementação, seguir contratos atuais e seus testes próprios. | **Sim** antes de promover qualquer diferença contratual; não para preservar o contrato corrente. |
| **4 — Monitoramento: WIP de `mon_runtime_v1`** | Worktree `codex/mon-runtime-v1-implementation` @ `4ff2a92`, com 8 arquivos rastreados modificados e 2 não rastreados, entre continuidade, contratos/auditoria e script de QA. | A branch histórica de implementação é ancestral do baseline; o WIP local é separado e não foi incorporado nem lido integralmente nesta C1. | **Moderado–alto:** sobrepor contratos ou incluir script/settings locais pode alterar escopo e expor dados. | **`PRESERVE_AS_ARCHIVE`** para documentos e scripts até adjudicação por arquivo; não sobrescrever documentos vigentes. | Revisão de diff documental; revisão isolada do script e testes de runtime somente se houver autorização de implementação. | **Sim** para incorporar texto ou script WIP. |
| **5 — Família P3 A–D** | `codex/ui-v2-p3-root-reconciliation` @ `e381df0`, 37 commits no grafo/33 patch-unique frente ao baseline; consolida A–D e oito capturas integradas ROOT. | §§40–41 registram A–D aprovadas, congeladas e validadas como protótipos; P3 fechou a integração de protótipos, não produção. O diff integral contra o baseline alcança 631 paths, pois a branch é muito anterior em outras partes do produto. | **Muito alto** para merge integral: importaria uma árvore antiga e pode reverter dezenas de áreas atuais. **Baixo** para retenção de protótipos/evidências. | **`PRESERVE_AS_ARCHIVE`** — preservar protótipos, contratos, fixtures e evidências aprovadas no P3 ROOT. Não converter telas em produção automaticamente; não mesclar a branch inteira. | Nenhum teste de produção necessário para retenção. Uma futura implementação exige contrato, seleção de tela e testes próprios, mais revisão visual no runtime atual. | **Sim** antes de qualquer transição de protótipo para produção. A aprovação P3 valida os protótipos, não autoriza conversão. |
| **6 — Hidden semantics / Design System** | Variante exclusiva `codex/ui-v2-ds-2.0.1-hidden-semantics-source` @ `094f626`; baseline tem DS 2.0.2 e o contrato `DSCR-UIV2-001`. | A regra corrente `[hidden]:not([hidden="until-found" i]) { display: none !important; }` está presente no baseline. A variante exclusiva volta os cabeçalhos CSS para 2.0.1 e desfaz parte da regra 2.0.2 de quebra de texto em tabelas; não acrescenta semântica `[hidden]` ausente. | **Moderado** se transplantada como pacote: downgrade de versão e regressão da política atual de legibilidade de tabelas. | **`ALREADY_PRESENT`** para semântica `[hidden]`; preservar o commit como histórico e não aplicar o pacote 2.0.1. | A validação histórica do contrato cobriu casos A–F e comportamento `until-found`; não foi repetida no C1. Se CSS-base for alterado futuramente, repetir a regressão de `[hidden]` e tabelas. | **Não** para a semântica corrente; qualquer reversão de DS exige decisão humana. |
| **Artefatos temporários/caches QA** | Arquivos ignorados distribuídos em 19 worktrees; o inventário por caminho/tipo não foi concluído para cada arquivo. | Parte pode ser gerada novamente, mas arquivos ignorados também incluem DB, evidência e settings. Nenhum item específico foi provado descartável. | **Alto** se dados ou evidências forem confundidos com cache descartável. | **`REBUILDABLE_AFTER_VALIDATION`** somente para cada arquivo confirmado como saída gerada sem estado/evidência; não se aplica por extensão ou por estar ignorado. Nenhum item fica autorizado para remoção nesta C1. | Confirmar origem, finalidade, reprodutibilidade e ausência de dependências locais; preservar antes de reconstruir. | **Sim** para adjudicar os caminhos concretos antes de qualquer remoção/reconstrução. |

### 2.1 Duplicatas e funcionalidades a integrar

- **A integrar após aprovação humana:** Camera Detail P5 aprovado, com seus cinco arquivos de produção/teste. As dependências compartilhadas 2.1/2.3/2.4 ainda exigem adjudicação própria; 2.2 é publicado mas não está no baseline. Reconciliar cada dependência contra 2.0.2 antes de copiar o CSS P5.
- **Já presentes:** Quick Detail funcional; worker e HTTP Snapshot de CAM-INT-04; regra global de `[hidden]`; decisões locais V1 do contrato de runtime de monitoramento.
- **Apenas retenção:** implementações antigas de capture service/RTSP, o histórico documental de monitoramento, o UI-WIP como conjunto, e os protótipos/evidências P3.
- **Não transformar em código:** nenhuma tela P3 e nenhum protótipo local deve virar produção por inferência a partir de aprovação visual.

## 3. Inventário e preservação — C1-B

Inventário baseado no relatório autoritativo e em status/caminhos já registrados. A classificação `UNKNOWN` indica que o nome/quantidade é conhecido, mas o conteúdo não foi aberto. A marcação como potencialmente sensível é uma regra de tratamento, não uma afirmação de que o arquivo contém um segredo.

| Conjunto / local conhecido | Classificação | Plano seguro de preservação |
|---|---|---|
| Bancos SQLite ignorados: 17 worktrees têm pelo menos um; o checkout `projeto_argos_hom_integration` tem 19; `projeto_argos` tem 1 e `ui_p5` tem 2. Nenhum conteúdo foi aberto. | `UNKNOWN` — tratar operacionalmente como dado local potencialmente sensível. | Manter cada banco no worktree de origem. Não abrir, exportar, copiar para a pasta canônica ou publicar. Se a retenção exigir backup, obter aprovação específica, identificar processos que possam escrever, gerar backup consistente fora do Git com ACL local e manifesto de origem/hash; não reutilizar o banco em outra estação sem revisão. Nenhum backup foi feito nesta C1. |
| Screenshots P5: cinco arquivos não rastreados; a continuidade P5 registra identificadores de câmera, MAC e IP e rejeição de publicação. | `SENSITIVE_LOCAL`. | Preservar nos caminhos atuais, sem abrir ou exportar. Não incluir em ZIP/GitHub. Qualquer compartilhamento futuro exige cópia derivada redigida e aprovação; conservar o original protegido. |
| Evidências P3: oito imagens `root-integrated-p3-2026-10-01` e evidências das famílias A–D sob o branch P3 ROOT. | `PRESERVE_REQUIRED`. | Reter o branch/protótipos e as evidências aprovadas como histórico verificável. Não substituir capturas nem promover seus HTMLs a templates de produção. |
| Artefatos QA e capturas em `ui-03-visual-completion` (6 rastreados/28 não rastreados) e `ui-03-density-refinement` (18 não rastreados); homologação tem 25 não rastreados, incluindo artefatos E4; conteúdo local não foi aberto. | `UNKNOWN`; evidências aceitas que sejam identificadas devem ser reclassificadas `PRESERVE_REQUIRED`; dados de teste/configuração devem ser tratados como `SENSITIVE_LOCAL`. | Deixar no worktree de origem. Antes de qualquer migração, listar caminhos e finalidade sem abrir conteúdo sensível, separar evidência aprovada de saída reexecutável e só então decidir retenção. Não excluir nem recriar nesta rodada. |
| Configurações locais: `s2b_qa_settings.py` em P5; `.local`, configuração isolada, logs e ambientes de QA em homologação; settings do runtime. | `SENSITIVE_LOCAL`. | Não ler, copiar, exportar ou incluir no Git. Configuração futura da pasta operacional deve ser reconstruída por ambiente, com segredos provisionados diretamente no host e fora dos documentos/commits. |
| Scripts QA não incorporados: launchers/scripts em homologação e script isolado no WIP `mon_runtime_v1`; conteúdo integral não foi revisado nesta atividade. | `PRESERVE_REQUIRED` até revisão; conteúdo permanece `UNKNOWN`. | Manter os arquivos nos worktrees atuais. Depois do gate humano, revisar um arquivo por vez, verificar origem/efeito/configuração antes de portar e validar isoladamente. Não executar durante C1. |
| Documentos de continuidade não publicados: WIP em homologação e `mon_runtime_v1`; documentos desta própria P0, incluindo este relatório e atualizações de continuidade. | `PRESERVE_REQUIRED`. | Preservar worktrees e diffs. Não sobrescrever nem publicar automaticamente; reconciliar por precedência/proveniência e obter aprovação de publicação. O trabalho documental P0 permanece não commitado. |
| ZIP de continuidade não rastreado em `C:\Users\walac\desenvolvimento\projeto_argos\docs\Agent-Continuity-Standard-v1.0.zip`. | `UNKNOWN`. | Manter local e fechado; não abrir, mover, recomprimir ou publicar. Resolver sua retenção em gate humano próprio. |
| Caches, ambientes virtuais e saídas temporárias ignoradas, quando identificados individualmente e provados reexecutáveis. | `REBUILDABLE`. | Só classificar após confirmar que não guardam estado/evidência; recriar depois de preservar configuração e obter validação. O relatório inicial não adjudicou arquivo por arquivo; nenhum foi removido. |

### Procedimento de preservação local recomendado

1. Preservar os worktrees e caminhos atuais como origem; registrar branch, HEAD, status, caminho e contagem sem inspecionar conteúdo sensível.
2. Separar evidências aprovadas de settings, logs e estado de QA. Tratar arquivos desconhecidos como `UNKNOWN` até revisão por nome/propósito.
3. Para qualquer backup aprovado, armazenar fora do repositório, com ACL restrita e manifesto mínimo (origem, tamanho, hash e data), sem conteúdo de credencial no manifesto. Bancos requerem backup consistente e finalidade definida antes de qualquer leitura/cópia.
4. Não transportar banco, sessão, settings nem screenshot bruto para outra estação. Reconstruir ambiente local quando seguro; injetar segredos no host por canal protegido.
5. Não criar ZIP para publicação no GitHub. ZIP local existente permanece fechado e inalterado.

## 4. Ordem proposta de convergência — C1-D

1. **Gate humano C1:** aprovar esta matriz, definir o conjunto P5 exato e confirmar a política de retenção local. Sem este gate, nada é incorporado.
2. **Preservação:** manter WIP/SQLite/screenshots/settings/scripts nos worktrees de origem; executar apenas backups que tenham autorização e destino local protegidos definidos.
3. **P5 Camera Detail:** após a decisão humana, reconciliar as capacidades DS necessárias e portar a composição P5 aprovada nos arquivos delimitados. Não presumir promoção de 2.1/2.3/2.4; respeitar a revisão visual de 2.4. Preservar Quick Detail e rotas de inventário atuais. Validar testes funcionais e evidência visual antes de considerar a fatia integrada.
4. **UI-WIP:** não aplicar a branch inteira. Se houver requisito visual residual, apresentar um diff limitado e uma comparação visual para decisão; manter link de importação, labels e timestamp do Quick Detail.
5. **CAM-INT-04:** manter worker, HTTP Snapshot, serviço, adapter RTSP e migrations atuais. Resolver requisito de captura por contrato e gates E3 separados; não iniciar P1 RTSP nesta consolidação.
6. **Monitoramento:** manter o contrato V1 vigente. Se houver delta não duplicado no commit `22c9e3a` ou no WIP documental, propor apêndice com proveniência e supersession explícita; não sobrescrever a versão corrente.
7. **P3 e hidden semantics:** preservar protótipos/evidências P3 como arquivo; nenhuma conversão de tela em produção. Não aplicar o patch DS 2.0.1, pois a semântica já está presente.
8. **Branch e pasta operacionais:** preservar o WIP do checkout `projeto_argos_hom_integration`; após autorização, sincronizar/adjudicar `codex/hom-v1-integration` contra o checkpoint informado sem perder WIP. Só então preparar `C:\Users\walac\desenvolvimento\projeto_argos` como única pasta operacional e conferir raiz, branch, HEAD, status e dados locais antes do cutover.
9. **Worktrees:** `AUTOMATIC_WORKTREE_CREATION = NO` é o estado desejado. Este plano não remove nenhum worktree/branch e não concede autorização de limpeza; qualquer remoção requer decisão humana posterior própria.

## 5. Prontidão, riscos e estado final

### Pasta canônica

`C:\Users\walac\desenvolvimento\projeto_argos` existe, mas está em `codex/argos-ui-v2-wip-20261008` @ `fea031d`, 2 commits à frente/44 atrás do baseline, com um ZIP não rastreado e um SQLite ignorado. **`CANONICAL_FOLDER_READINESS = NOT_READY`**. Preservar branch, ZIP e DB; não trocar a branch nem converter a pasta nesta atividade.

### Branch operacional candidata

`codex/hom-v1-integration` existe no checkout `C:\Users\walac\desenvolvimento\projeto_argos_hom_integration`, em `df582ade`, dois commits atrás do checkpoint informado, com 5 arquivos rastreados modificados, 25 não rastreados e 19 bancos SQLite ignorados. A ref local `origin/codex/hom-v1-integration` aponta para `ddd8f163`, mas não houve consulta remota ao vivo. **`CANONICAL_BRANCH_READINESS = NOT_READY`** até preservar/adjudicar WIP e alinhar o checkout sem perdas.

### Risco

- **Alto — dados locais:** 17 worktrees com SQLite ignorado e arquivos locais não revistos; o risco maior é perder estado QA, expor screenshots/settings ou transportar dados para outra máquina.
- **Moderado–alto — regressão de integração:** P5 depende de padrões compartilhados; aplicar bundle completo pode alterar outras telas. UI-WIP remove conteúdo/controles do baseline. CAM-INT-04 antigo conflita com migrations e reduz guardrails se for substituído.
- **Alto — regressão documental/histórica:** o merge amplo de P3 alcança 631 paths e pode reverter componentes recentes; substituir os contratos de monitoramento pode reintroduzir status intermediários como se fossem atuais.
- **Moderado — status de validação:** testes e aprovação citados são evidências históricas de outros checkpoints; nenhuma validação foi executada contra o baseline C1.

```text
SINGLE_OPERATIONAL_FOLDER = projeto_argos / TARGET, NOT_CHANGED
SINGLE_OPERATIONAL_BRANCH_DEFAULT = YES / TARGET, NOT_CHANGED
AUTOMATIC_WORKTREE_CREATION = NO / TARGET, NOT_CHANGED
BRANCH_OR_WORKTREE_CREATION = NO / NONE CREATED
DELETE_WORKTREES = NO / NONE DELETED
DELETE_BRANCHES = NO / NONE DELETED
RESET_OR_CLEAN = NO / NOT PERFORMED
CODE_MODIFICATION = NO / NONE
DATABASE_MUTATION = NO / NONE
VM_MODIFICATION = NO / NONE
MERGE_OR_CHERRY_PICK = NO / NONE
COMMIT_OR_PUSH = NO / NONE
P1_RTSP = NOT_STARTED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §171
ACTIVITY_COMPLETE = YES / C1 analysis and preservation plan only
NEXT_GATE = HUMAN_INTEGRATION_APPROVAL
WORKTREE_DELETION_AUTHORIZED = NO
```

**Fim da C1:** aguardar `HUMAN_INTEGRATION_APPROVAL` para eventual incorporação seletiva. A conclusão deste relatório não autoriza exclusão de worktrees ou branches.


---

### Nota de proveniência e numeração na master

Este relatório preserva o registro produzido no worktree documental de origem. As referências internas às seções de PROJECT_STATE.md, AGENT_CONTINUITY.md e ACTIVE_DOCUMENT_MAP.md seguem a numeração daquele snapshot. Na pasta master, PROJECT_STATE.md §170 foi preservada como o registro C3-B já existente; a reconciliação canônica posterior está em PROJECT_STATE.md §171 e é indexada em ACTIVE_DOCUMENT_MAP.md §130. Esta nota resolve a proveniência sem renumerar nem duplicar os registros históricos. O worktree de origem não foi modificado.

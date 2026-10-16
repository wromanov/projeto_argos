# ARGOS — recuperação do checkpoint global de continuidade

**Status:** commits B/C concluídos; commit final e sincronização ainda pendentes
em 2026-10-16. Este guia só representa transferência concluída após confirmar
que o SHA remoto da branch é igual ao HEAD local.

## Identificação e estado Git

```text
PROJECT_ID = projeto_argos
ACTIVITY = ARGOS-FULL-CONTINUITY-CHECKPOINT-01
SOURCE_BRANCH = codex/hom-v1-integration
HEAD_BEFORE = 5a1d9e63c97712b9ee5ddbdf8f26b802eded801e
HEAD_BEFORE_FINAL_DOC = 7cb8ec306c78dec6acd054d655568a1a12b390b4
FINAL_HEAD = o commit final deste checkpoint; consulte `git rev-parse HEAD` e o relatório da atividade
REMOTE_URL = https://github.com/wromanov/projeto_argos.git
REMOTE_BRANCH = codex/hom-v1-integration
REMOTE_SHA_OBSERVED = e91e4499d43211722b7eadba9adab842e3c75aeb
REMOTE_SYNC = PENDING_FINAL_DOC_COMMIT_AND_PUSH
LOCAL_COMMITS_UNPUBLISHED = 97c7d47c4c47761d205a7d41262bf067c56c403d; 5a1d9e63c97712b9ee5ddbdf8f26b802eded801e; 06bc2c17628ba2cb11a01a8647fb04d2ca00608c; 7cb8ec306c78dec6acd054d655568a1a12b390b4
COMMIT_B = 7cb8ec306c78dec6acd054d655568a1a12b390b4
COMMIT_C = 06bc2c17628ba2cb11a01a8647fb04d2ca00608c
PUSH = not executed
```

O HEAD local observado antes do commit documental final estava quatro commits
à frente do remoto; todos eram descendentes do SHA remoto verificado. O commit
`97c7d47` contém o checkpoint HOM-01 e evidências QA; `5a1d9e6` implementa
HOM-02/XLSX; `06bc2c1` é o Commit C de HOM-03; `7cb8ec3` é o Commit B de
roadmap e continuidade. A autorização direta do usuário foi recebida após a
rejeição inicial da revisão automática.

## WIP, staging e transferência

Campos solicitados para transporte:

```text
DATE = 2026-10-16
SOURCE_BRANCH = codex/hom-v1-integration
SOURCE_HEAD = 5a1d9e63c97712b9ee5ddbdf8f26b802eded801e
FINAL_HEAD = commit final deste checkpoint; SHA exato no relatório final e via `git rev-parse HEAD`
REMOTE_SHA = SHA da branch remota após push; comparar com `git rev-parse HEAD`
FILES_COMMITTED = commits locais 97c7d47 (HOM-01), 5a1d9e6 (HOM-02), 06bc2c1 (HOM-03/Commit C), 7cb8ec3 (roadmap/continuidade/Commit B) e o commit documental que contém este arquivo
FILES_EXCLUDED = modificação local do checkpoint HOM-01, `.local/`, bancos, helper e ZIPs não inspecionados
UNTRACKED_REMAINING = `.local/`; `docs/projeto.zip`; `docs/Agent-Continuity-Standard-v1.0/continuity.zip`
UNTRANSFERRED_REQUIRED_FILES = conteúdo do pacote/helper HOM-03 em `.local/` não foi revalidado; necessidade de transferência não confirmada. Configuração operacional e credenciais devem ser provisionadas separadamente
WORKTREE_RESIDUAL = checkout raiz mantém WIP local listado abaixo; outros 8 worktrees limpos
LOCAL_ONLY_ARTIFACTS = .local/ (QA DB/evidências/temporários); helper/ZIP HOM-03; docs/projeto.zip; continuity.zip
OTHER_BRANCHES = inventory abaixo; várias isoladas ou behind; não são incluídas no push HOM
OTHER_WORKTREES = CAM-INT-04, MON runtime, UI DS 2.0.1, P3-A/B/C/D, P5; todos limpos
ROADMAP_STATE = reconciliação §24 no Commit B (7cb8ec3)
SPRINTS_STATE = reconciliação §21 no Commit B (7cb8ec3)
HOM_STATES = HOM-01 CLOSED/APPROVED; HOM-02 aceite funcional/commit local; HOM-03 BLOCKED SSH; HOM-04 não aberta
UI_PENDING_ITEMS = P3-P7 exigem reconciliação/cobertura por escopo; sem conclusão global
BACKEND_PENDING_ITEMS = BC-02 por fatias; branches isoladas não integradas
IMAGE_PENDING_ITEMS = UI captura manual, galeria, retenção/rotação/proteção/purge e conformidade §26 pendentes
VALIDATION_RESULTS = ancestry/fast-forward possível; diff checks PASS; scans de segurança sem padrões; worktrees limpos; testes técnicos atuais NONE
NEXT_ACTIVITY = publicar o commit documental final e validar o clone no outro computador
NEXT_GATE = fast-forward autorizado; REMOTE_SYNC só PASS após igualdade exata do SHA local e remoto
```

Os commits anteriores contêm estes arquivos, ainda não publicados. `97c7d47`
(HOM-01): os três documentos de continuidade, `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, os relatórios em `docs/projeto/evidence/camera-detail-residual-qa/` e `docs/projeto/evidence/dashboard-v7-integrated-qa/`, e cinco capturas QA em `dashboard-v7-integrated-qa/`. `5a1d9e6` (HOM-02): migration `cameras/migrations/0019_alter_camera_options_cameraimportpreview.py`; `cameras/models.py`, `cameras/templates/cameras/importacao.html`, `cameras/templates/cameras/importacao_resultado.html`, `cameras/templates/cameras/lista.html`, `cameras/test_xlsx_import.py`, `cameras/urls.py`, `cameras/views.py`, `cameras/xlsx_import.py`, `docs/projeto/HOM_02_XLSX_IMPORT_PREPARATION.md`, `docs/projeto/SPRINTS_ARGOS_V5.md`, `requirements.txt`, `static/css/importacao-xlsx.css`, `templates/base.html`, `templates/components/navegacao_principal.html` e `templates/components/sidebar.html`.

Commit B (`7cb8ec306c78dec6acd054d655568a1a12b390b4`) contém somente estes
cinco documentos:

- `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`
- `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`
- `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`
- `docs/projeto/ROADMAP_ARGOS_V5.md`
- `docs/projeto/SPRINTS_ARGOS_V5.md`

Commit C (`06bc2c17628ba2cb11a01a8647fb04d2ca00608c`) contém somente
`config/settings_homologation.py`, `env.homologation.example`, `config/wsgi.py`,
`requirements.txt` e `docs/seguranca/CONFIGURACAO_DE_AMBIENTES.md`. A settings
injeta segredos pelo ambiente; o template contém placeholders. A varredura não
detectou segredo, credencial ou endpoint externo. O extra Psycopg `[c]` no Linux
exige toolchain e bibliotecas cliente PostgreSQL, incluindo `pg_config`; isso
foi acrescentado à documentação, sem declarar readiness da VM. HOM-03 continua
bloqueado até obter acesso SSH autorizado. Não houve acesso à VM/banco, migração
ou câmera real.

Outros artefatos locais preservados: `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`,
`.local/`, `docs/projeto.zip` e
`docs/Agent-Continuity-Standard-v1.0/continuity.zip`. `.local/` contém banco
SQLite de QA, capturas/evidências e arquivos temporários; algumas subpastas
estavam inacessíveis. O ZIP HOM-03 em `.local/hom03-transfer-20261015/` tem hash
histórico `1145c18fc26be278bb5450bc5369a4e4e6ea65fb5be7657160e12c363be64efc`
registrado no §121, mas seu conteúdo não foi revalidado agora. Os dois ZIPs
acima não foram inspecionados. Nenhum deles é parte confirmada da transferência;
não copiar/publicar sem revisão própria.

Classificação: HOM-01/HOM-02/C/B estão em commits locais ainda não publicados;
configuração/template/documentação HOM-03 estão em Commit C. Permanecem locais
e fora da transferência `.local/`, os ZIPs não inspecionados e a alteração do
checkpoint HOM-01. O endpoint privado observado em adições documentais foi
redigido; não repetir valores operacionais.

## Branches e worktrees

Refs locais comparadas com refs remotas observadas. Todos os worktrees fora do
checkout raiz estavam limpos.

| Branch | HEAD local | HEAD remoto | Worktree | Estado |
|---|---|---|---|---|
| `codex/hom-v1-integration` | `5a1d9e6` | `e91e449` | checkout raiz | ahead 2; WIP e cinco docs staged |
| `codex/cam-int-04-implementation` | `f9b9728` | igual | `projeto_argos_cam_int_04` | limpo, sincronizado; CAM-INT-04/IMG-CAP isolado |
| `codex/mon-runtime-contract-closure` | `22c9e3a` | igual | `projeto_argos_mon_runtime` | limpo, sincronizado |
| `codex/ui-v2-ds-2.0.1-hidden-semantics` | `9943e20` | `8121ed3` | `projeto_argos_ui_v2_ds_2_0_1` | limpo, behind 1 |
| `codex/ui-v2-p3-0-prototype-harness` | `d274ede` | sem branch homônima | nenhum | tip alcançável por refs remotas; sem commit exclusivo identificado |
| `codex/ui-v2-p3-a-core-inventory` | `adc62fe` | igual | `projeto_argos_ui_v2_p3_a` | limpo, sincronizado |
| `codex/ui-v2-p3-b-monitoring-activities` | `7b879b8` | `8006dad` | `projeto_argos_ui_v2_p3_b` | limpo, behind 1 |
| `codex/ui-v2-p3-c-governance-audit` | `e96836c` | igual | `projeto_argos_ui_v2_p3_c` | limpo, sincronizado |
| `codex/ui-v2-p3-d-forms-account-secondary` | `f5dd030` | igual | `projeto_argos_ui_v2_p3_d` | limpo, sincronizado |
| `codex/ui-v2-p5-production` | `4a2d40d` | `4676a32` | `projeto_argos_ui_p5` | limpo, behind 4 |
| `master` | `5bd22b0` | igual | nenhum | sincronizado |

Branches relevantes apenas no remoto (não transferidas pela branch HOM):
`codex/bc-02-integration` (`ccc0267`), `codex/cam-health-implementation`
(`6ef2f70`), `codex/cam-int-05-implementation` (`68d593d`),
`codex/mon-obs-observability` (`6fc4f70`),
`codex/mon-runtime-v1-implementation` (`4ff2a92`),
`codex/ui-v2-wip-20261008` (`fea031d`),
`codex/ui-v2-ds-2.0.2-mobile-table-readability` (`8a480a5`) e
`codex/ui-v2-p3-root-reconciliation` (`e381df0`). Tratar cada branch
separadamente; sem merge ou push automático.

## Estado do projeto e authorities

- **HOM-01:** CLOSED/APPROVED; preservar aceites e limitações documentadas.
- **HOM-02:** XLSX funcionalmente aceito pelo usuário; commit local `5a1d9e6`,
  não publicado. Evidências anteriores: 163 testes focados e prova sintética
  com 2.300 linhas; checkpoints posteriores citam 14 focados e 31 de regressão.
- **HOM-03:** preparação parcial; readiness bloqueada por chave SSH autorizada.
- **HOM-04:** não aberta formalmente.
- **Roadmap/Sprints:** §§24/21 reconciliados; Commit B não criado. PROJECT_STATE
  §124 contradiz sua própria narrativa sobre ROADMAP/Sprints estarem WIP e
  limpos na entrada; preservar o histórico e manter a divergência não adjudicada.
- **UI V2:** P3–P7 precisam de reconciliação/coberturas próprias; sem conclusão
  global. Branches isoladas não são integração canônica.
- **Credenciais:** backend CAM-INT-02/R1 implementado; UI de gestão pendente.
- **Imagens:** captura manual; botão/UI e galeria de até três imagens pendentes;
  retenção de 12 meses aprovada; rotação, proteção e purge aguardam contrato e
  gates. Quick Detail deve seguir contrato §26.
- **BC-02:** há fatias integradas e branches isoladas; não inferir homologação.

Authorities: `AGENTS.md`, `docs/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`,
`docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`,
`PROJECT_STATE.md`, `AGENT_CONTINUITY.md`, políticas transversais, Roadmap v5
e Sprints v5. Consultar o mapa ativo para versões vigentes; não duplicar seus
contratos.

## Validação e gates

```text
VALIDATIONS_EXECUTED_NOW = inventário Git; consulta remota read-only; ancestry; varreduras de segurança; git diff --check; git diff --cached --check
VALIDATIONS_RESULT = diff checks e padrões inspecionados PASS; testes runtime não executados
HISTORICAL_TESTS = HOM-01: 948 pass; HOM-02: evidências históricas acima; HOM-03: py_compile e manage.py check via SQLite, históricos
TESTS_NOT_EXECUTED = todos os testes técnicos nesta atividade
PROJECT_STATE_UPDATE = PASS
AGENT_HANDOFF_GATE = PENDING
CHECKPOINT_ACTIVITY_COMPLETION_PERCENT = 60%
COMMIT_COUNT = 3 criados nesta atividade: B, C e documento final; cinco commits locais a publicar no total
STATUS = READY_FOR_PUBLICATION
NEXT_ACTIVITY = concluir o commit documental, publicar a branch autorizada e verificar o clone
NEXT_GATE = fast-forward; igualdade exata do SHA remoto e HEAD local para REMOTE_SYNC=PASS
```

## PowerShell para o outro PC

No outro computador, clonar depois da publicação e buscar a branch HOM. O script
usa o SHA remoto recebido como referência e falha se o checkout local divergir.

```powershell
$RepoUrl = 'https://github.com/wromanov/projeto_argos.git'
$Branch = 'codex/hom-v1-integration'
$RepoPath = Join-Path (Get-Location) 'projeto_argos'

git clone --branch $Branch --single-branch $RepoUrl $RepoPath
Set-Location $RepoPath
git fetch origin
git switch $Branch
$ExpectedHead = (git rev-parse "origin/$Branch").Trim()
$ActualHead = (git rev-parse HEAD).Trim()
if ($ActualHead -ne $ExpectedHead) { throw "SHA inesperado: $ActualHead" }
git status --short --branch
git log -5 --oneline

Get-Content docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md
Get-Content docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md -Tail 100
Get-Content docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md -Tail 80
Get-Content docs/projeto/ROADMAP_ARGOS_V5.md -Tail 80
Get-Content docs/projeto/SPRINTS_ARGOS_V5.md -Tail 80

py -3.14 --version
py -3.14 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

O repositório não declara `requires-python`; a arquitetura documenta CPython
3.14.6 e o ambiente de origem registrou 3.14.7. Usar CPython 3.14.x e conferir
com `py -3.14 --version`. Para desenvolvimento local, ler `config/settings.py`
e `.env.example`; o exemplo contém placeholders e não é carregado
automaticamente. Só copiar/ajustar template se a configuração local realmente
exigir. Não usar credenciais operacionais, não ativar
`config.settings_homologation` e não presumir que configurações da VM foram
transferidas.

Antes de testes ou validações no destino, ler o mapa ativo e os gates HOM
correspondentes. Rodar somente os comandos autorizados nas authorities e
registrar resultados atuais separados das evidências históricas. Não abrir
HOM-04, alterar banco, fazer deploy ou acessar câmeras reais nesta retomada.
Branches além da HOM devem ser buscadas e verificadas individualmente, sem
merge automático.

Arquivos operacionais locais indispensáveis à VM exigem canal autorizado e
separado. Não copiar `.local/`, bancos, segredos, ZIPs não inspecionados ou
helper de homologação indiscriminadamente.

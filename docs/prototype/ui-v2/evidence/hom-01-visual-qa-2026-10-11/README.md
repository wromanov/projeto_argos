# ARGOS-HOM-01 — preparação de evidências visuais

## Iniciar o ambiente local

No Windows, execute `INICIAR_ARGOS_QA.cmd` na raiz do checkout. O launcher
prepara/reutiliza `.local/qa/argos_visual_qa.sqlite3`, migra o banco isolado,
carrega cinco câmeras fictícias, valida `qa-visual-hom01` sem alterar sua senha
ou permissões e prepara `qa-operacional-hom01`. O Django inicia em
`http://127.0.0.1:8765/` e o navegador é aberto automaticamente.

O terminal mostra a senha temporária da conta operacional. Cada execução do
launcher a rotaciona; a senha anterior deixa de valer. A senha visual é
preservada e não é exibida nem persistida pelo launcher. Pressione Ctrl+C na
janela do launcher para encerrar o servidor.

O banco só será migrado se o marcador local confirmar que pertence ao launcher.
Um banco preexistente sem esse marcador causa interrupção segura. O SQLite
antigo `hom01-visual-qa.sqlite3` e os logs `hom01-qa-server.*` não são usados.
O conjunto de câmeras tem somente dados fictícios e IPs reservados para
documentação; não há worker nem probes reais.

O perfil visual mantém suas cinco permissões e fica restrito a requisições de
leitura pela middleware local. O perfil operacional recebe exatamente sete
permissões para inspecionar a Camera Detail, registrar atividade e enviar uma
imagem manual sintética. Os endpoints Django aplicam autorização; o launcher
não envia imagens.

```text
ACTIVITY = ARGOS-HOM-01-ONE-CLICK-RUNTIME-SETUP
LAUNCHER_STATIC_VALIDATION = PASS
WINDOWS_RUNTIME_VERIFIED = NOT_VERIFIED
BROWSER_RENDER_VERIFIED = NOT_VERIFIED
DESIGN_QA = PENDING
```

O primeiro uso real do CMD no Windows ainda precisa confirmar HTTP e capturar
as páginas integradas para a revisão visual. As referências aprovadas,
pendentes ou ausentes permanecem como registradas abaixo.

```text
ACTIVITY = ARGOS-HOM-01-DESIGN-QA-EVIDENCE-01
DATE = 2026-10-11 / America-Sao_Paulo
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
STATUS = BLOCKED / no integrated page could be rendered
VIEWPORT_TARGET = 1440x900 CSS pixels
BROWSER_ZOOM_TARGET = 100%
DEVICE_SCALE_FACTOR_TARGET = 1
STATE_TARGET = default; synthetic data only
```

## Referências

| Tela | Classificação | Referência e aprovação conhecida |
|---|---|---|
| Shell / sidebar / topbar | `APPROVED_REFERENCE` | `SCR-SHELL-001`, P3-0 approved; baseline screenshot set in P5 source worktree `docs/prototype/ui-v2/evidence/screenshots/shell/` |
| Dashboard | `APPROVED_REFERENCE` | P3-A `SCR-DASH-001`, approved/frozen; screenshot set in P3 root source worktree `docs/prototype/ui-v2/evidence/screenshots/p3-a/` |
| Inventário | `CANDIDATE_REFERENCE` | P3-A screenshots exist. P3-A `coverage.md` §41 says approved/frozen, but current HOM-01 snapshots `PROJECT_STATE.md` §§87-88 say approval pending. Conflict unresolved; do not infer approval. |
| Camera Detail | `APPROVED_REFERENCE` | P3-A `SCR-CAM-DETAIL-001`, approved/frozen; screenshot set in P3 root source worktree `docs/prototype/ui-v2/evidence/screenshots/p3-a/` |
| Quick Detail aberto | `MISSING_REFERENCE` | Approved/protected baseline is recorded, but the reference screenshot named in continuity (`C:\Users\walac\AppData\Local\Temp\argos-batch-b-visual\corrective-final-quick-detail-390x844-viewport.png`) is not present. No redesign is authorized. |

P3/P5 source worktrees were read-only. Their reference files were not copied or
overwritten. A P3 prototype capture is not evidence of the integrated app.

## Capturas integradas

| Tela | `RENDERED_SCREENSHOT` | Estado |
|---|---|---|
| Shell / sidebar / topbar | Not captured | Loopback connection denied by sandbox |
| Dashboard | Not captured | Loopback connection denied by sandbox |
| Inventário | Not captured | Integrated human-review candidate not prepared |
| Camera Detail | Not captured | Loopback connection denied by sandbox |
| Quick Detail aberto | Not captured | Loopback connection denied by sandbox |

Playwright was not installed in the active environment or P5 virtual
environment; the P3 and main-project virtual environments could not start
because their configured Python interpreter path is unavailable. A temporary SQLite database with five synthetic
cameras and a least-privilege Visual QA identity was prepared without using the
existing `db.sqlite3` or `hom01-visual-qa.sqlite3`. The development server was
bound to `127.0.0.1:8000`; the sandbox denied the local socket request, and the
browser reported a connection timeout. The temporary database and settings were
removed. No screenshots were generated; no prototype HTML was substituted for a
real render.

## Comparação e gate

The required paired comparison could not run. Layout, alignment, typography,
spacing, tokens, navigation, tables, filters, states, overflow, responsiveness,
and accessibility differences remain unassessed. No severity or correction is
assigned without rendered evidence. `CORRECTION_EVIDENCE` is not applicable in
this activity because UI changes are not authorized.

```text
REFERENCE_SCREENSHOTS = LOCATED IN SOURCE WORKTREES / NOT COPIED
MISSING_REFERENCE_SCREENSHOTS = QUICK_DETAIL
RENDERED_SCREENSHOTS = NONE
VISUAL_DIFFERENCE_REPORT = BLOCKED
VISUAL_DEVIATIONS = UNASSESSED
INVENTORY_REFERENCE_APPROVAL = PENDING / DOCUMENT CONFLICT RECORDED
INVENTORY_HUMAN_APPROVAL = PENDING
DESIGN_QA = BLOCKED
FUNCTIONAL_REGRESSION = PRIOR_77_TESTS_PASS / NOT_REEXECUTED
HOMOLOGATION_GATE = BLOCKED
```

## Tentativa no host — 2026-10-11

```text
ACTIVITY = ARGOS-HOM-01-HOST-VISUAL-QA-01
EXECUTION_MODE = DIRECT / VISUAL_QA_EVIDENCE
WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos_hom_integration
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SOURCE_WIP_PRESERVED = YES
HOST_CHROME = AVAILABLE
HOST_BROWSER_ACCESS = BLOCKED / http://127.0.0.1:8765/dashboard/ returned net::ERR_CONNECTION_TIMED_OUT
SYNTHETIC_DATABASE = PASS / temporary SQLite migrated and seeded with five synthetic cameras; deleted after attempt
DJANGO_RENDERING = BLOCKED / no page response received by host Chrome
RENDERED_SCREENSHOTS = NONE
REFERENCE_WORKTREE_ACCESS = BLOCKED / host filesystem denied access to P3 and P5 source worktrees
OLD_QA_LOGS = PRESERVED / hom01-qa-server.err and hom01-qa-server.log were not opened for writing or removed
DESIGN_QA = BLOCKED
INVENTORY_REFERENCE = CANDIDATE_REFERENCE / approval conflict unresolved
INVENTORY_HUMAN_APPROVAL = PENDING
QUICK_DETAIL_REFERENCE = MISSING / approved and protected baseline remains pending renewed human visual approval
QUICK_DETAIL_BASELINE_APPROVAL = PENDING
FUNCTIONAL_REGRESSION = PRIOR_77_TESTS_PASS / NOT_REEXECUTED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md section 90
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md section 20.53 and ACTIVE_DOCUMENT_MAP.md section 57
UI_CODE_CHANGED = NO
BACKEND_CHANGED = NO
MIGRATIONS_CHANGED = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
HOM_01_STATUS = IN_PROGRESS
HOMOLOGATION_GATE = BLOCKED
```

A identidade `qa-visual-hom01` foi provisionada apenas no SQLite descartável,
com as permissões da rotina `provision_visual_qa`; cinco câmeras usaram somente
dados sintéticos e endereços reservados para documentação (`192.0.2.0/24`). O
schema foi migrado sem modificar migrations. O Chrome do host estava acessível,
mas a navegação local expirou. O servidor foi encerrado, a porta ficou sem
listener e o diretório descartável — incluindo banco e configuração temporária —
foi removido. Nenhuma nova tentativa equivalente foi feita. Os logs QA antigos,
que já estavam pendentes de liberação pelo sistema operacional, permanecem
intactos.

O inventário Git anterior à captura foi preservado: mudanças existentes em
templates, testes e continuidade, artefatos CSS não rastreados, este diretório
de evidências e os dois logs. Não houve staging nem mudança em arquivos de UI,
backend ou migrations nesta atividade.

### Procedimento reproduzível no Windows quando o loopback estiver disponível

Execute em uma sessão PowerShell local do Windows, no checkout desta branch. O
procedimento abaixo usa somente o Python de `.venv`, um diretório novo em `%TEMP%`,
uma senha temporária escolhida para esta execução e o bind explícito a
`127.0.0.1`. Não aponte `DATABASES` para `db.sqlite3`, não configure câmeras ou
credenciais reais e não exponha outra interface de rede.

1. Crie um diretório temporário exclusivo e o módulo Django de configuração:

   ```powershell
   Set-Location 'C:\Users\walac\desenvolvimento\projeto_argos_hom_integration'
   $repo = (Resolve-Path '.').Path
   $qaRoot = Join-Path $env:TEMP ('argos-hom01-qa-' + [guid]::NewGuid().ToString('N'))
   New-Item -ItemType Directory -Path $qaRoot | Out-Null
   $dbPath = Join-Path $qaRoot 'visual-qa.sqlite3'
   $dbLiteral = $dbPath.Replace('\', '\\')
   $settings = @"
   import os
   from config.settings import *
   DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": r"$dbLiteral"}}
   DEBUG = True
   VISUAL_QA_ENABLED = True
   VISUAL_QA_USERNAME = "qa-visual-hom01"
   VISUAL_QA_PASSWORD = os.environ["ARGOS_VISUAL_QA_PASSWORD"]
   ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
   SECRET_KEY = os.environ["ARGOS_SECRET_KEY"]
   "@
   Set-Content -LiteralPath (Join-Path $qaRoot 'qa_settings_hom01.py') -Value $settings -Encoding UTF8
   $env:PYTHONPATH = "$qaRoot;$repo"
   $env:DJANGO_SETTINGS_MODULE = 'qa_settings_hom01'
   $env:ARGOS_DEBUG = 'true'
   $env:ARGOS_VISUAL_QA_ENABLED = 'true'
   $env:ARGOS_VISUAL_QA_USERNAME = 'qa-visual-hom01'
   $env:ARGOS_VISUAL_QA_PASSWORD = Read-Host 'Defina uma senha descartável para esta identidade local de QA'
   $env:ARGOS_ALLOWED_HOSTS = '127.0.0.1,localhost'
   $env:ARGOS_SECRET_KEY = (& (Join-Path $repo '.venv\Scripts\python.exe') -c 'import secrets; print(secrets.token_urlsafe(48))').Trim()
   $env:ARGOS_MONITORING_CONCURRENCY = '1'
   $env:ARGOS_MONITORING_CYCLE_INTERVAL_SECONDS = '30'
   $env:ARGOS_MONITORING_PROBE_TIMEOUT_SECONDS = '1'
   $env:ARGOS_MONITORING_CONNECT_TIMEOUT_SECONDS = '1'
   $env:ARGOS_MONITORING_QUEUE_BOUND = '1'
   $env:ARGOS_MONITORING_SHUTDOWN_TIMEOUT_SECONDS = '2'
   $env:ARGOS_MONITORING_JITTER_RATIO = '0'
   $env:ARGOS_MONITORING_STALE_AFTER_SECONDS = '30'
   $env:ARGOS_MONITORING_HEARTBEAT_SECONDS = '10'
   $env:ARGOS_MONITORING_OWNERSHIP_LEASE_SECONDS = '2'
   $env:ARGOS_MONITORING_DB_OPERATION_DEADLINE_SECONDS = '0.1'
   $env:ARGOS_MONITORING_RECOVERY_MAX_ATTEMPTS = '1'
   $env:ARGOS_MONITORING_RECOVERY_MAX_ELAPSED_SECONDS = '11'
   ```

2. Migre somente o banco temporário e crie a identidade mínima do Visual QA:

   ```powershell
   .\.venv\Scripts\python.exe manage.py migrate --noinput
   if ($LASTEXITCODE -ne 0) { throw 'A migração temporária falhou.' }
   .\.venv\Scripts\python.exe manage.py provision_visual_qa
   ```

3. Crie cinco câmeras sintéticas no mesmo banco (não são contatos de rede):

   ```powershell
   $seedPath = Join-Path $qaRoot 'seed_visual_qa.py'
   @'
   from django.core.management import call_command
   from cameras.models import Camera
   call_command("provision_visual_qa", verbosity=0)
   statuses = [Camera.SituacaoOperacional.PRODUCAO,
               Camera.SituacaoOperacional.PRODUCAO,
               Camera.SituacaoOperacional.ESTOQUE,
               Camera.SituacaoOperacional.DESATIVADA,
               Camera.SituacaoOperacional.PRODUCAO]
   for i, status in enumerate(statuses, 1):
       Camera.objects.create(
           nome=f"QA Sintética {i:02d}", fabricante="Axis", modelo="QA-P3265",
           serial=f"QA-SER-{i:04d}", mac=f"02:00:00:00:00:{i:02X}",
           tipo=Camera.TipoCamera.DOME, situacao_operacional=status,
           terminal="T-QA", pavimento="QA", setor="QA-S" if i % 2 else "QA-N",
           ambiente=f"Ambiente sintético {i:02d}", ip=f"192.0.2.{i}",
           mascara_subrede="255.255.255.0", gateway="192.0.2.254", vlan=999,
           farm="FARM-QA-SYNTHETIC", retencao_esperada_dias=30, codec="H265",
       )
   '@ | Set-Content -LiteralPath $seedPath -Encoding UTF8
   .\.venv\Scripts\python.exe manage.py shell -c "exec(open(r'$seedPath', encoding='utf-8').read())"
   if ($LASTEXITCODE -ne 0) { throw 'A criação do conjunto sintético falhou.' }
   ```

4. Em um PowerShell dedicado, inicie o Django sem recarga automática e mantenha
   essa janela aberta durante as capturas:

   ```powershell
   .\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8765 --noreload
   ```

   Se o Windows ou o navegador não alcançar esse endereço, pare aqui, encerre o
   servidor com `Ctrl+C` e registre o bloqueio. Não mude o bind para `0.0.0.0`,
   não crie encaminhamento de porta e não repita tentativas equivalentes.

5. No Chrome local, entre em `http://127.0.0.1:8765/` com a identidade
   `qa-visual-hom01` e a senha descartável que acabou de definir. Abra DevTools,
   ative a barra de dispositivos, informe `1440 × 900`, `DPR = 1` e mantenha
   zoom do navegador em 100%. Use a página real do Django, sem HTML do protótipo.

6. Capture em PNG o Shell (pela rota Dashboard), Dashboard (`/dashboard/`),
   Inventário (`/cameras/`), Camera Detail (abra uma das cinco linhas) e Quick
   Detail (no Inventário, acione “Visualizar rapidamente”). Registre cada rota,
   viewport CSS, zoom, DPR, estado, dados sintéticos, caminho e data. Combine os
   viewports de cada tela com as dimensões da referência aprovada correspondente;
   não infira dimensões de uma tela a partir da referência de outra.

7. Compare cada par em viewport, zoom, dados e estado equivalentes. Não declare
   `DESIGN_QA = PASS` enquanto P3/P5 estiverem inacessíveis, enquanto faltar a
   captura de referência do Quick Detail, enquanto a referência do Inventário
   não for adjudicada pelo usuário ou enquanto faltar a avaliação visual humana.

8. Encerre o servidor. Confirme que a porta 8765 está sem listener. Depois
   confirme que `$qaRoot` resolve dentro de `%TEMP%` e que contém o marcador
   `qa_settings_hom01.py`; só então remova esse diretório temporário criado por
   esta execução. Preserve `hom01-qa-server.err` e `hom01-qa-server.log`, que
   pertencem à tentativa anterior e continuam pendentes de liberação.

To reproduce after local loopback is available: start the integrated branch on
loopback with a disposable database and synthetic records, authenticate with
the restricted local Visual QA identity, then capture each named route at
1440×900, 100% browser zoom, and device scale factor 1. Capture matching
approved references and rendered pages separately. For Inventory, obtain
human adjudication of the conflicting P3 approval record before treating its
reference as canonical. Do not use production credentials or sensitive data.

## Adendo de aceite humano e baseline — 2026-10-11

O usuário aprovou a composição integrada recuperada da Camera Detail e o
resultado integrado de Camera Create/Edit. Esses aceites não registram viewport
ou estado inspecionado e não aprovam os quatro tamanhos. O usuário também
aprovou a apresentação do botão de upload na conta QA operacional; isso não
comprova submissão interativa de arquivo. Permanecem sem aprovação visual
integrada documentada Shell, Dashboard, Inventário e Quick Detail aberto.

O manifesto e o resultado de reconciliação estão em
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`. As 18 referências P3-D
existentes foram mantidas no lugar e não foram duplicadas. Este adendo não
substitui os registros históricos de tentativas de captura nem altera seus
resultados.

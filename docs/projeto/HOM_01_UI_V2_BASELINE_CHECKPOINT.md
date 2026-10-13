# ARGOS HOM-01 — baseline integrada UI V2

```text
PROJECT_ID = projeto_argos
ACTIVITY = ARGOS-HOM-01-FINAL-BASELINE-CHECKPOINT
BASELINE_NAME = ARGOS_HOM_01_UI_V2_INTEGRATED_BASELINE
BASELINE_BRANCH = codex/hom-v1-integration
BASELINE_CODE_COMMIT = 188afda5470e252fa8cf6fed5556a404073ee4fc
PREVIOUS_DOCUMENT_CHECKPOINT = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
DOCUMENT_CHECKPOINT_COMMIT = 6e3550077bf682a11889f3a554875c62d115ee00 / primary checkpoint commit
CANONICAL_DS_VERSION = 2.0.2
WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos_hom_integration
CHECK_DATE = 2026-10-11 / America-Sao_Paulo
ACTIVITY_STATUS = COMPLETED / CHECKPOINT PARTIAL; HOM-01 remains IN_PROGRESS
```

## 1. Resumo executivo e gates

O código de referência desta baseline é o commit `188afda`. Ele acrescenta a
recuperação dos formulários, mudanças visuais de Dashboard/Inventário, a
provisão de QA operacional, CSS de Camera Detail e continuidade. O commit tem
57 arquivos alterados, não altera migrations e está nove commits à frente de
ref `origin/master` local. A branch não tem upstream nem remote-tracking ref
`origin/codex/hom-v1-integration` no clone. A consulta ao remoto real falhou
por DNS; o estado remoto atual não foi confirmado. O worktree e o staging
estavam limpos antes deste checkpoint.

O commit documental principal é `6e3550077bf682a11889f3a554875c62d115ee00`.
Este follow-up registra sua identidade. A ref local `origin/master` fica 10
commits atrás de `6e35500` e ficará 11 atrás após este commit de metadados;
ambos os valores são comparações locais, não confirmação do estado remoto ao
vivo.

| Gate | Resultado em 2026-10-11 | Evidência / pendência |
|---|---|---|
| `TECHNICAL_GATE` | `FAIL / PARTIAL` | `manage.py check` PASS; regressões dirigidas 405/406, com falha em `cameras.test_governanca_views.GovernancaViewsPermissoesTests.test_dashboard_exibe_situacoes_completude_e_ips_duplicados`; suíte global interrompida sem resumo após duas falhas sinalizadas. |
| `VISUAL_GATE` | `BLOCKED / PARTIAL APPROVALS` | Aceites humanos restritos abaixo; sem renderização integrada arquivada, comparação suficiente ou QA integrado nos quatro viewports. |
| `DOCUMENTATION_GATE` | `PASS` após commit deste checkpoint | Este documento, `PROJECT_STATE.md`, continuidade, mapa de documentos e authority de branches atualizados. |
| `GIT_RECONCILIATION_GATE` | `PARTIAL / UNVERIFIED WIP` | Ancestry e refs Git examinados; acesso de leitura aos diretórios de worktree P3/P5 negado pelo host. Não houve merge ou cherry-pick. |
| `PUBLICATION_GATE` | `NO` | Sem upstream/ref remota HOM local; `6e35500` está 10 commits à frente da ref local `origin/master`; após este follow-up serão 11. Consulta remota ao vivo falhou por DNS e WIP externo está UNVERIFIED. Nenhum push executado. |

```text
HOM01_STATUS = IN_PROGRESS
HOM01_CLOSURE_READINESS = FAIL / required technical and visual gates remain open
HOM02_START = BLOCKED / NOT AUTHORIZED
PUBLISH_READY = NO
CODE_CHANGED_IN_CHECKPOINT = NO
MIGRATIONS_CHANGED_IN_BASELINE = NO
NEW_BRANCH = NO
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
```

## 2. Reconciliação Git e correções aprovadas

| Origem | Ref/SHA examinada | Classificação | Decisão e limite |
|---|---|---|---|
| Integração HOM-01 | `codex/hom-v1-integration` — `188afda5470e252fa8cf6fed5556a404073ee4fc` | `INTEGRATED` | Baseline efetiva. Código e testes do commit identificados; nenhuma mudança local pendente antes do checkpoint. |
| Checkpoint HOM-00 | `d1fd9491692afb57da9dcfe0a27964efdb2d19e0` | `INTEGRATED` | Ancestral direto; autoridade e estado anteriores preservados como histórico. |
| P3-A Core/Inventory | `codex/ui-v2-p3-a-core-inventory` — `36ad10d26da14470aea9ab35e0cc4d9aa3dccd2e`; remoto `adc62fe` | `REFERENCE / APPROVAL CONFLICT` | Fonte de Dashboard, Inventário e Camera Detail. O conflito sobre aprovação da referência de Inventário continua sem adjudicação. Worktree de evidências inacessível; nenhum merge integral. |
| P3 root | `codex/ui-v2-p3-root-reconciliation` — `e381df04f59ce146bf53fc6929fb7ca272c26e2c` | `REFERENCE / PARTIAL INTEGRATION` | Fonte de protótipo e aprovações. Não fazer merge integral. O código de protótipo não é a implementação Django. WIP não versionado no worktree inacessível = `UNVERIFIED`. |
| P3-D Forms | `codex/ui-v2-p3-d-forms-account-secondary` — `b4b4d7ed99eea4467d4ae111dcddf77c09ed9bbf`; aprovação `f5dd0308f46705e03c79609077ed1ec7a12bc766`; reconciliação `9ce90bafdd67cb2b878edcdd2c4ecb1b4e849522` | `REFERENCE / APPROVED FIXES SELECTIVELY INTEGRATED` | A composição visual e os screenshots P3-D foram recuperados, usando Django Forms reais, em `188afda`. Aceite visual integrado atual é do usuário; não prova aprovação nos quatro viewports. Outros protótipos, perfis e autenticação P3-D continuam fora do escopo HOM-01. Worktree não versionado = `UNVERIFIED`. |
| P5 produção | `codex/ui-v2-p5-production` — `4676a32c78cecab33a157a0a9d4fd2cabbc90a87` | `PARTIALLY INTEGRATED / SUPERSEDED DETAILS` | A implementação base da Camera Detail está na ancestralidade da baseline por `662e80e`; atualizações posteriores P5/DS não foram promovidas em bloco. O contrato vigente HOM-01 fixa DS 2.0.2. Worktree P5 inacessível = `UNVERIFIED`. |
| P5 conformance | `codex/p5-camera-detail-production-conformance` — `4a2d40da502ea4dafd8bc78202e707416695bee3` | `PARTIAL / SUPERSEDED OR UNVERIFIED BY FIX` | A recuperação atual é a adaptação seletiva DS 2.0.2 registrada em `188afda`; não foi feito merge integral desta branch. A auditoria V01–V10 não foi localizada como artefato independente no checkout; a equivalência de cada item fica `UNVERIFIED` até mapear o registro fonte. |
| Nome de branch indicado no pedido | `codex/p5-camera-detail-production` | `UNVERIFIED / REF NOT FOUND` | O nome exato não existe nas refs locais. A branch correspondente encontrada é `codex/p5-camera-detail-production-conformance`, acima. |
| WIP geral de UI | `codex/argos-ui-v2-wip-20261008` — `fea031d6e3ca5d55a4cebc16ffb9d3f0f236a573` | `PARTIAL / UNVERIFIED WIP` | Ref versionada comparada; o worktree também fica fora do acesso concedido. Nenhum arquivo local foi alterado ou removido. |

As referências P3-A, P3-D e P5 foram comparadas por ancestry, commit e
seleção de arquivos. O estado do WIP não versionado fora deste checkout não
pôde ser confirmado; por isso não se declara que nenhuma mudança pendente
exista. Não há evidência de que uma correção aprovada versionada tenha sido
perdida na baseline, mas o conjunto V01–V10 e o WIP externo continuam
`UNVERIFIED`. Esse limite bloqueia o gate de reconciliação/publicação que
depende dessa confirmação, sem exigir integrar branches históricas sem mudança
necessária.

## 3. Testes e regressão pós-commit

| Validação no HEAD `188afda` | Resultado |
|---|---|
| `python manage.py check` | `PASS` — sem problemas. |
| Regressão dirigida HOM-01/MON | `147 PASS / 1 FAIL` de 148; SQLite de teste isolado em `.local/qa/test-runs`, removido pelo runner. |
| Regressão dirigida Create/Edit, catálogo, upload, auditoria e perfil | `258/258 PASS`; SQLite de teste isolado em `.local/qa/test-runs`, removido pelo runner. |
| Total dirigido | `405 PASS / 1 FAIL` de 406; o finding é o mesmo teste de texto Dashboard abaixo. |
| Falha reproduzida | `test_dashboard_exibe_situacoes_completude_e_ips_duplicados`: o teste procura o texto singular `IP duplicado`; a interface renderiza `IPs duplicados`. Não corrigida neste checkpoint documental. |
| Suíte global `manage.py test --noinput` | `INCONCLUSIVE / INTERRUPTED`; indicou duas falhas durante a execução longa, depois deixou de emitir saída e não havia processo Python ativo. Runner isolado encerrado sem relatório final; nenhum PASS global alegado. |
| `git diff --check` | `PASS` — checkout de código limpo antes das mudanças documentais. Reexecutar para o checkpoint abaixo. |

A regressão dirigida cobriu Camera Detail, formulário Create/Edit, Quick
Detail, Inventário, Dashboard/Shell, QA operacional, autorização/permissões,
catálogos, validação de rede, upload, atividades, auditoria, perfis, UI do
monitoramento e serviço de leitura MON. A única falha conhecida é o contrato
de texto singular/plural acima; o resultado funcional global não é PASS até
resolução e rerun. Não foram iniciados probes, worker, scheduler,
migrações operacionais, deploy ou contatos com câmeras reais.

`CSS_DEPENDENCY_CHECK = PASS_STATIC`: os testes verificam a carga dos assets
nas rotas autorizadas; Camera Detail recupera os módulos canônicos
tokens/base/components/patterns e ajustes próprios de rota, enquanto
Create/Edit carrega primitives 2.0.2 e `camera-form.css`. Isto não substitui
renderização visual real.

## 4. QA local e limites de segurança

O commit `188afda` contém o launcher `INICIAR_ARGOS_QA.cmd`, settings e
provisionamento QA. Revisão estática confirma: bind explícito em
`127.0.0.1:8765`; SQLite exclusivo `.local/qa/argos_visual_qa.sqlite3` com
marcador de propriedade; nenhuma integração externa, worker ou scheduler;
chave gerada com `secrets.token_urlsafe(48)` por execução e exigência mínima de
32 caracteres; senha operacional gerada por execução, exibida só no terminal e
removida do ambiente no `finally`; preparação repetível com seed sintético;
conta visual verificada sem alteração; conta operacional restringida a sete
permissões; ambas sem staff/superuser conforme implementação e testes; colisão
de usuário não reconhecido interrompe antes de alterar o seed.

O registro de QA anterior (`PROJECT_STATE.md` §94) validou as sete permissões
`view_camera`, `add_camera`, `change_camera`, `consultar_eventos`,
`consultar_substituicoescamera`, `add_cameraimagerecord` e
`add_atividadecamera`, sem privilégios administrativos, e provisionamento
idempotente. O usuário confirmou em §95 que acessou o perfil e aprovou a
apresentação do botão de upload. Esse checkpoint não comprova submissão de
arquivo pelo navegador. O banco local atual não foi reprovisionado; não se
expõem nem se registram senhas ou hashes de senha.

`.gitignore` protege `.local/qa/`, `*.sqlite3`, mídia, logs QA e arquivos de
segredo usuais; os arquivos-fonte e o diretório versionado de evidências não
são cobertos por essas regras. A revisão do commit `188afda` não encontrou
banco QA, logs, `.env` ou arquivo de credencial entre os 57 paths. O commit é
fonte do launcher e da suíte; nenhum segredo estático ou credencial foi
registrado no checkpoint. Também consultei o SQLite local estritamente em modo
read-only: marcador de propriedade válido; ambas as contas ativas, sem grupos,
staff ou superuser; marcador de seed válido; conta visual com exatamente cinco
permissões previstas e conta operacional com exatamente as sete permissões
previstas. Senhas e hashes não foram lidos nem impressos. O banco não foi
reprovisionado nem alterado.

## 5. Baseline visual e aceites

| Superfície | Referência/protótipo | Implementação integrada | Teste funcional | Inspeção e aceite humano | Responsividade / teclado |
|---|---|---|---|---|---|
| Shell/navegação | Shell P3 aprovado; quatro referências existentes | Integrado na baseline; testes de Shell passam | `FUNCTIONALLY_TESTED` | `NOT_VERIFIED` na implementação atual | `NOT_VERIFIED` |
| Dashboard | P3-A `SCR-DASH-001`, referência aprovada | Dashboard integrado em `188afda` | `FUNCTIONALLY_TESTED`; finding singular/plural aberto | `NOT_VERIFIED` | `NOT_VERIFIED` |
| Inventário | P3-A `SCR-INV-001`; conflito de aprovação entre `coverage.md` §41 e PROJECT_STATE §§87–88 não adjudicado | Integrado em `188afda`; funcionalmente testado | `FUNCTIONALLY_TESTED` | Aprovação humana da integração pendente | `NOT_VERIFIED` |
| Camera Detail | P5 recuperado; P3-A também mantém referência de produto | Implementação integrada e CSS recuperado em `188afda`; `OUT_OF_SCOPE = OPTION_A` | Testes direcionados passam | `APPROVED` pelo usuário para a composição P5 recuperada; sem declaração de viewports aprovados | `NOT_VERIFIED` |
| Camera Create/Edit | P3-D aprovada em 30/09/2026; referência `b4b4d7e`, review `f5dd030`, reconciliação `9ce90ba` | Formulários Django reais e recuperação seletiva integrados em `188afda` | Testes focais passam; regressão geral tem um finding Dashboard | `APPROVED` pelo usuário após inspeção da integração; largura/estado inspecionados não foram registrados | `NOT_VERIFIED` |
| Quick Detail | Baseline aprovada e protegida; screenshot aprovado não localizado | Baseline protegida; sem redesign | Testes direcionados passam | `NOT_VERIFIED` para renderização integrada atual | `NOT_VERIFIED` |
| Botão de upload em Camera Detail | Recurso funcional existente | Apresentação confirmada pelo usuário com perfil operacional | Autorização e renderização em testes anteriores passam | `APPROVED`, restrita à apresentação do botão | Upload interativo não verificado; responsividade/foco pendentes |

`VISUAL_APPROVED`, `FUNCTIONALLY_TESTED`, `RESPONSIVE_VALIDATED` e
`NOT_VERIFIED` são dimensões distintas. A aprovação de uma composição não
representa aprovação de todos os quatro viewports. Nenhuma captura integrada
foi encontrada ou criada neste checkpoint; as capturas de referência não são
evidência da aplicação renderizada.

**Pendências visuais concretas:** captura integrada de Shell, Dashboard,
Inventário, Camera Detail e Quick Detail aberto; referência Quick Detail ausente;
adjudicação humana da referência Inventário; comparação das telas realmente
renderizadas; review integrado em 1920×1080, 1440×900, 1366×768 e 390×844 a
zoom 100%; navegação por teclado e foco; estados de erro aplicáveis. O host já
registrou timeout de loopback e instruiu a não repetir tentativa equivalente.
Quando o usuário iniciar `INICIAR_ARGOS_QA.cmd` em Windows com loopback
funcional, usar o procedimento do README de evidências e solicitar somente as
capturas/decisões que faltarem.

## 6. Manifesto de evidências visuais

As capturas listadas são **referências de protótipo**, salvo indicação. Os
nomes codificam resolução; zoom não foi preservado em metadados verificáveis,
por isso consta como `UNVERIFIED`. `TEST_RESULT` indica o resultado da fonte
de referência, não um teste de renderização da implementação integrada. As
aprovações humanas da implementação foram comunicadas na solicitação desta
atividade; a conversa não fornece arquivo de captura nem screenshot.

| EVIDENCE_ID | SCREEN / FEATURE | REFERENCE_SOURCE / COMMIT | IMPLEMENTATION_SOURCE | VIEWPORT | DATE | TEST_RESULT / HUMAN_APPROVAL | EVIDENCE_PATH / SHA256 |
|---|---|---|---|---|---|---|---|
| SHELL-1366 | Shell/sidebar/topbar | P3 root `e381df0` | `188afda` | 1366×768 | commit 2026-10-01 | ref aprovada; render integrada `NOT_VERIFIED` | `evidence/screenshots/shell/shell__1366x768__default__default.png`; `0F67F9BDEF844D18FE71643C612EE5B3868A24A74DA5E7CFC514D6070F752979` |
| SHELL-1440 | Shell/sidebar/topbar | P3 root `e381df0` | `188afda` | 1440×900 | commit 2026-10-01 | ref aprovada; render integrada `NOT_VERIFIED` | `evidence/screenshots/shell/shell__1440x900__default__default.png`; `E0FFADE4055B14DCA3C5D508459EFD2247004CB349FEA0165D52C6635D94E9D4` |
| SHELL-1920 | Shell/sidebar/topbar | P3 root `e381df0` | `188afda` | 1920×1080 | commit 2026-10-01 | ref aprovada; render integrada `NOT_VERIFIED` | `evidence/screenshots/shell/shell__1920x1080__default__default.png`; `E52585BADB54530F03449ABBEF594C5616FDE6B5659E696C94BC6F56D4C71790` |
| SHELL-390 | Shell/sidebar/topbar | P3 root `e381df0` | `188afda` | 390×844 | commit 2026-10-01 | ref aprovada; render integrada `NOT_VERIFIED` | `evidence/screenshots/shell/shell__390x844__default__default.png`; `B716D58F7558BA88F000434F279768081E2A18BA4DFE1B304C1742DEA2B04F0F` |
| P3D-CREATE-1366 | Camera Create / referência | P3-D ROOT/reconciliation `9ce90ba`; aprovação `f5dd030` | `188afda` | 1366×768 | approval 2026-09-30 | P3-D QA PASS; integração aprovada pelo usuário sem viewport registrado | `.../reference/scr-cam-create-001__1366x768__default__default.png`; `5EE3A791CD5FA1CCE2A6B9879C6CDBE82C46CC1D1E1FE68EF0D92836AEF7FBEF` |
| P3D-CREATE-1440 | Camera Create / referência default | idem | `188afda` | 1440×900 | approval 2026-09-30 | P3-D QA PASS; aceites conforme escopo acima | `.../reference/scr-cam-create-001__1440x900__default__default.png`; `008B490058BF4E280FBB622BFCBF7D0B469133C6F473518144E3C7EF508FA025` |
| P3D-CREATE-LONG | Camera Create / conteúdo longo | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integrado não capturado | `.../reference/scr-cam-create-001__1440x900__default__long.png`; `13AACA88ED69D1BA59AE2F2DDE40B632812077D9F35A016A2B002943ADC86C47` |
| P3D-CREATE-ERROR | Camera Create / erro | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integração funcional testada | `.../reference/scr-cam-create-001__1440x900__error__long.png`; `754D1A680386DDD12164DEC7F57A9C3AD104102AAF0F9E55A8EBED419A0A8DFA` |
| P3D-CREATE-FOCUS | Camera Create / foco | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; teclado integrado `NOT_VERIFIED` | `.../reference/scr-cam-create-001__1440x900__focus__default.png`; `7908591602A6AE331300C9D6190053071ADD7ACDC9D9A010827D7EA2B521FC6B` |
| P3D-CREATE-SELECTED | Camera Create / seleção | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integrated render `NOT_VERIFIED` | `.../reference/scr-cam-create-001__1440x900__selected__default.png`; `8A59EEEF47247CE6ABA2FCF24D035DF0F4B82638B180D50B4DEDF16EA2FF91D5` |
| P3D-CREATE-SUCCESS | Camera Create / sucesso | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; validação Django coberta por teste | `.../reference/scr-cam-create-001__1440x900__success__default.png`; `29F08B4993E69FBDE627001442DED1F29977486DCE0577F4838BE84D61F037BE` |
| P3D-CREATE-1920 | Camera Create / referência | idem | `188afda` | 1920×1080 | approval 2026-09-30 | ref de protótipo; responsividade integrada `NOT_VERIFIED` | `.../reference/scr-cam-create-001__1920x1080__default__default.png`; `B86342BDDC0A403E0247E17BA7F3206590C5B0A1C81FE04D9CD45B937E1C5D60` |
| P3D-CREATE-390 | Camera Create / referência móvel | idem | `188afda` | 390×844 | approval 2026-09-30 | ref de protótipo; responsividade integrada `NOT_VERIFIED` | `.../reference/scr-cam-create-001__390x844__default__default.png`; `1E239B6EEF005B5661131AE438C01FC90F3CEC7147370041B6C24FA5614DFBCD` |
| P3D-EDIT-1366 | Camera Edit / referência | P3-D ROOT/reconciliation `9ce90ba`; aprovação `f5dd030` | `188afda` | 1366×768 | approval 2026-09-30 | P3-D QA PASS; integração aprovada pelo usuário sem viewport registrado | `.../reference/scr-cam-edit-001__1366x768__default__default.png`; `EF8EC2D765636111C15E0E09883E6CAA6B67C6F23E40A5AAB6AA61B7627F1B9B` |
| P3D-EDIT-1440 | Camera Edit / referência default | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integrated render `NOT_VERIFIED` | `.../reference/scr-cam-edit-001__1440x900__default__default.png`; `5C5CE70F52537483B3E99B0BBEA6CB7FA6F4DBC0693D904AB82DB4E3F566C56F` |
| P3D-EDIT-LONG | Camera Edit / conteúdo longo | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integrated render `NOT_VERIFIED` | `.../reference/scr-cam-edit-001__1440x900__default__long.png`; `2B25664E2792282B9726D4B408CB3FB7EEEF97961ACFBA84A6A04BC02DE2082A` |
| P3D-EDIT-ERROR | Camera Edit / erro | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integração funcional testada | `.../reference/scr-cam-edit-001__1440x900__error__long.png`; `907B4ED671CED7952E52B0FE56A919D6D2701D83B861D08EF8EA2DFE53884712` |
| P3D-EDIT-FOCUS | Camera Edit / foco | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; teclado integrado `NOT_VERIFIED` | `.../reference/scr-cam-edit-001__1440x900__focus__default.png`; `B2D1AFAB80F63A84AC1AC24EE7A924ECA2D94C665B75B09B0C10A5F90BE67CCA` |
| P3D-EDIT-SELECTED | Camera Edit / seleção | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; integrated render `NOT_VERIFIED` | `.../reference/scr-cam-edit-001__1440x900__selected__default.png`; `231C869EAF3D0A0346F02E56E202950483B314F73C60AE0A097DAF9742F2DA93` |
| P3D-EDIT-SUCCESS | Camera Edit / sucesso | idem | `188afda` | 1440×900 | approval 2026-09-30 | ref de protótipo; validação Django coberta por teste | `.../reference/scr-cam-edit-001__1440x900__success__default.png`; `ADDEA1CDC2BAA24EB6FDD5971EE600CC082A592FD2EFF02B587CD7E8B430E2BE` |
| P3D-EDIT-1920 | Camera Edit / referência | idem | `188afda` | 1920×1080 | approval 2026-09-30 | ref de protótipo; responsividade integrada `NOT_VERIFIED` | `.../reference/scr-cam-edit-001__1920x1080__default__default.png`; `46FF1310333B6B9F8C8B90FA8A3CA4177313FCE7A0FE07AED6C970BF6D305DC7` |
| P3D-EDIT-390 | Camera Edit / referência móvel | idem | `188afda` | 390×844 | approval 2026-09-30 | ref de protótipo; responsividade integrada `NOT_VERIFIED` | `.../reference/scr-cam-edit-001__390x844__default__default.png`; `DB559B9DCCF7FDE828F769E2D73AA11FB9487F63D7D0BCD26AED80D5241E87BD` |
| P3A-DASH | Dashboard reference family | P3-A in P3 root `e381df0` | `188afda` | 390×844, 1366×768, 1440×900, 1920×1080 | source commit 2026-10-01 | prototype source approved; integrated visual approval pending | P3 Git tree `docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001*`; individual SHA256 not computed |
| P3A-INVENTORY | Inventory reference family | P3-A in P3 root `e381df0` | `188afda` | 390×844, 1366×768, 1440×900, 1920×1080 | source commit 2026-10-01 | approval conflict; human adjudication pending | P3 Git tree `.../screenshots/p3-a/SCR-INV-001*`; SHA256 not computed |
| P3A-DETAIL | Camera Detail reference family | P3-A in P3 root `e381df0` | `188afda` | 390×844, 1366×768, 1440×900, 1920×1080 | source commit 2026-10-01 | approved reference; integrated composition approved by user, viewport unspecified | P3 Git tree `.../screenshots/p3-a/SCR-CAM-DETAIL-001*`; SHA256 not computed |
| QUICK-DETAIL-REF | Quick Detail open | Approved/protected baseline; expected Temp path absent | `188afda` | — | — | no physical reference found; current render `NOT_VERIFIED` | `MISSING`; no path fabricated |
| HUMAN-DETAIL-ACCEPT | Camera Detail composition | User report in current activity request | `188afda` | viewport unspecified | 2026-10-11 | `APPROVED`, limited to recovered composition | conversation only; no file/SHA |
| HUMAN-FORM-ACCEPT | Camera Create/Edit integrated result | User report in current activity request; P3-D refs above | `188afda` | viewport unspecified | 2026-10-11 | `APPROVED`, viewport coverage not implied | conversation only; no file/SHA |
| HUMAN-UPLOAD-BUTTON | Camera Detail upload button | User report; PROJECT_STATE §95 | `188afda` | viewport unspecified | 2026-10-11 | `APPROVED`, button presentation only; browser submission not verified | conversation and `PROJECT_STATE.md` §95; no screenshot/SHA |

Os nomes de arquivo de referência codificam estado e viewport; os arquivos
P3-D existentes foram reutilizados sem duplicação. A pasta com referências P3-D
contém 18 PNGs; o SHA-256 acima foi calculado nos arquivos do checkout atual.
Paths `evidence/...` são relativos a `docs/prototype/ui-v2/`. A abreviação
`.../reference/` significa
`evidence/argos-hom-01-camera-edit-recovery-2026-10-11/reference/`; `.../screenshots/p3-a/`
significa `docs/prototype/ui-v2/evidence/screenshots/p3-a/` como path na árvore
Git P3 root. Padrões como `SCR-DASH-001*` identificam uma família de blobs, não
um arquivo singular. A coluna `DATE` registra a data de aprovação ou do commit
fonte; o instante original de captura não está registrado. Não há caminho de
screenshot integrado porque nenhum existe.

## 7. Contratos funcionais protegidos

Esta baseline preserva MON Runtime V1 e a separação entre monitoramento e
operação; Camera Detail e `OUT_OF_SCOPE = OPTION_A`; diagnóstico técnico A–D;
Create/Edit com Django Forms e catálogos personalizados; auditoria e
permissões; invalidação por mudança de IP; upload manual em Camera Detail e
históricos; Quick Detail protegido por dialog nativo; Dashboard com cinco
câmeras recentes; Inventário com filtros/paginação; Shell e navegação; e Design
System canônico 2.0.2. Diferenças funcionais legítimas em relação a protótipos
continuam sob os contratos Django e ficam separadas da apresentação visual.
Nenhuma mudança funcional da HOM-02 foi iniciada.
As decisões de XLSX sem `id_argos`, correspondência por patrimônio/serial,
preview sem gravação, `CREATE/UPDATE` explícitos, validação Django,
confirmação, atomicidade e rollback permanecem na seção HOM-02 do Sprint Map;
exportação aprovada continua não bloqueante para homologação. Este checkpoint
não altera esses contratos.

## 8. Segurança, branch e próximo checkpoint

A regra `ARGOS-RECONCILE-BEFORE-BRANCH` foi registrada na authority
`ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`, seção 13. Branches de
desenvolvimento novas ficam bloqueadas por padrão até WIP, correções aprovadas,
testes, gates, baseline documental e checkpoint Git serem reconciliados e a
criação receber autorização explícita. Não se exige merge de branches antigas
que não contenham mudanças necessárias.

O remoto configurado é `origin` (`https://github.com/wromanov/projeto_argos.git`).
`git ls-remote` falhou porque o host não resolveu `github.com`; portanto o
estado ao vivo do remoto e a existência atual da branch destino não foram
verificados. `origin/master` é apenas a ref remote-tracking local. Essa
limitação, junto com o teste e os gates pendentes, mantém `PUBLISH_READY = NO`.

O checkpoint não concede autorização para criar branch, publicar, iniciar
HOM-02 ou alterar código. Próximas ações necessárias: resolver o teste
singular/plural com autorização de correção adequada; rerodar a suíte global e
os testes afetados; liberar acesso autorizado às evidências/worktrees ou
classificar o WIP não versionado; concluir capturas e review visual integrado;
atualizar este documento e PROJECT_STATE; então solicitar decisão humana sobre
publicação e HOM-02.

## 9. Follow-up — reconciliação do contrato do Dashboard (2026-10-12)

```text
ACTIVITY = ARGOS-HOM-01-DASHBOARD-CONTRACT-RECONCILIATION
BASELINE_BRANCH = codex/hom-v1-integration
HEAD_BEFORE = 11dcf7db0095416c125f8863ab89a2eef7fb278f
HEAD_AFTER = 11dcf7db0095416c125f8863ab89a2eef7fb278f
IP_DUPLICATION_METRIC = NUMBER_OF_AFFECTED_CAMERAS
IP_DUPLICATION_LABEL = Câmeras com IP duplicado
MONITORING_SECTION_LABEL = Monitoramento e completude
UNKNOWN_DISPLAY_LABEL = Desconhecido / internal UNKNOWN unchanged
TARGETED_TESTS = PASS / 28 of 28
GLOBAL_SUITE = PASS / 937 of 937 / 1104.507 seconds
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS / after documentation update
CODE_FILES_CHANGED = core/views.py; core/templates/core/dashboard.html; core/tests.py; core/test_frontend.py; cameras/test_governanca_views.py
DESIGN_QA = PENDING / human integrated review remains required
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
NEW_BRANCH = NO
```

O cálculo real soma os totais de câmeras em cada grupo cujo IP aparece mais
de uma vez. O teste dirigido diferencia duas câmeras com um único IP repetido
e confirma o valor `2`. A implementação manteve essa regra; limpou a ordenação
padrão do modelo antes do agrupamento e removeu o filtro `ip=""`, que em
`GenericIPAddressField` anulável era compilado pelo SQLite como comparação
com `NULL` e excluía endereços válidos. A mudança visível limita-se ao rótulo
aprovado; não houve alteração de layout, CSS ou componentes.

As duas falhas de texto reproduzidas foram corrigidas nas expectativas dos
testes, e a asserção do contrato frontend foi alinhada. A regressão direcionada
executou 28 testes e terminou `OK`. O `manage.py check` terminou sem problemas.
O primeiro run global em sandbox encontrou o limite do socket interno do
asyncio no Windows; o run final usou `scripts.localqa.test_settings`, banco
SQLite temporário e loopback local para esse socket, terminou `Ran 937 tests`
e `OK`. Nenhum dado operacional real foi acessado; os cenários de escala
registraram que não usaram rede, câmera ou credenciais reais. Logs de ambas as
tentativas e dos segmentos estão sob `.local/qa/test-runs/`.

Este follow-up supersede os achados técnicos do checkpoint de 2026-10-11 sobre
a falha textual e a suíte inconclusiva. As aprovações anteriores de Camera
Detail, Create/Edit e botão de upload permanecem intactas. QA visual integrado,
responsividade e teclado/foco seguem pendentes; HOM-01 permanece em andamento
e HOM-02 bloqueada.

## 10. Follow-up — padronização dos rótulos de monitoramento (2026-10-12)

```text
ACTIVITY = ARGOS-HOM-01-INVENTORY-UNKNOWN-PRESENTATION-FIX
BRANCH = codex/hom-v1-integration
HEAD = 11dcf7db0095416c125f8863ab89a2eef7fb278f
PRESENTATION_MAP = cameras/monitoramento/presentation.py
LABELS = ONLINE: Online; OFFLINE: Offline; UNKNOWN: Desconhecido; OUT_OF_SCOPE: Não monitorada
ALL_SUPPORTED_STATES_VERIFIED = YES / 82 targeted tests, including stale and out-of-scope
QUICK_DETAIL_TECHNICAL_PAYLOAD = PRESERVED
INTERNAL_MON_CONTRACT_CHANGED = NO
DESIGN_SYSTEM_CHANGED = NO
CSS_CHANGED_BY_ACTIVITY = NO
TARGETED_TESTS = PASS / 82 of 82
DJANGO_CHECK = PASS
JAVASCRIPT_SYNTAX = PASS
LIVE_RENDER = STALE / launcher starts runserver with --noreload
DESKTOP_MOBILE_VISUAL_QA = PENDING / need current render; 390px capture unavailable
HUMAN_VISUAL_APPROVAL = PENDING
HOM_01_STATUS = IN_PROGRESS
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §98
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
NEW_BRANCH = NO
```

O mapa único traduz os estados efetivos e trata `OUT_OF_SCOPE` como
classificação de escopo, distinta de `UNKNOWN`. Inventário, dashboard, Quick
Detail e Camera Detail usam os rótulos aprovados, sem alterar códigos técnicos,
payloads, transições ou variantes visuais. Os cenários cobrem os quatro estados
apresentados, dados stale e saída de escopo.

A aplicação integrada aberta foi iniciada com `--noreload`, então continuou
servindo as views anteriores após as alterações. Não se repetiu o launcher,
pois ele executa preparação/seed e rotaciona a senha operacional QA. O
checkpoint humano em viewport real continua pendente; este follow-up não fecha
HOM-01.

## 11. Follow-up — rótulos do diagnóstico técnico A–D (2026-10-12)

```text
ACTIVITY = ARGOS-HOM-01-DIAGNOSTIC-A-D-LABEL-RECONCILIATION
BRANCH = codex/hom-v1-integration
HEAD = 11dcf7db0095416c125f8863ab89a2eef7fb278f
EVIDENCE_STATE_VALUES = CURRENT, UNKNOWN
FRESHNESS_VALUES = FRESH, STALE, UNKNOWN
EVIDENCE_LABELS = Atual, Não determinada
FRESHNESS_LABELS = Atualizado, Desatualizado, Não determinado
UNKNOWN_IS_MON_STATE = NO / diagnostic projection strings are separate
LAST_CONFIRMED_ROW = only ONLINE or OFFLINE; omitted for UNKNOWN
INTERNAL_CONTRACTS_CHANGED = NO
TARGETED_TESTS = PASS / 65
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS
INTEGRATED_RENDER_AFTER_EDIT = PASS / actual Django page reloaded by user
VISUAL_VIEWPORTS = PASS / 1366x768 desktop; 390x844 mobile
BROWSER = Edge; ZOOM = 100%; DPR = 1; VISUAL_VIEWPORT_SCALE = 1
MOBILE_DOCUMENT_OVERFLOW = NO / horizontal scrolling confined to navigation
SCREENSHOT_FILES = NONE / actual captures displayed inline only
DESIGN_QA = PENDING
HUMAN_APPROVAL = APPROVED / bounded A–D labels and UNKNOWN last-confirmed-row behavior at 1366x768 and 390x844 only; user reply: “certo”
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
NEW_BRANCH = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

Na projeção `CameraHealthProjection`, `evidence_state` assume `CURRENT` para
snapshot válido e atual ou `UNKNOWN` quando o timestamp não permite afirmar
atualidade. `freshness` assume `FRESH`, `STALE` ou `UNKNOWN` para dados atuais,
antigos ou com timestamp futuro/inválido. O rótulo “Não determinada” não
afirma ausência de evidência; indica que o estado não pode ser determinado.
O código de cada projeção permanece técnico e intacto.

“Último estado confirmado” era semanticamente incorreto quando o estado MON
estável era `UNKNOWN`; a linha fica omitida nesse caso. O badge “Estado atual:
Desconhecido” permanece. Para ONLINE/OFFLINE confirmados, a linha continua
disponível. Mudanças restritas à camada de apresentação, sem alteração das
regras A–D, serviços MON, persistência, APIs, histórico, permissões, layout,
CSS ou Design System.

Os 65 testes dirigidos, `manage.py check` e `git diff --check` passaram. Após
o usuário recarregar o Django, a Camera Detail real foi conferida com o
registro sintético QA em 1366x768 e 390x844, zoom 100%, DPR 1 e escala visual
1. Os dois rótulos indeterminados aparecem sem quebrar o layout; em mobile,
cabem lado a lado e a largura do documento coincide com a área útil (375px).
A barra horizontal visível pertence à navegação responsiva, cujo conteúdo
continua rolável dentro do componente.

As capturas da tela integrada foram exibidas inline, mas a interface de captura
disponível não as salvou em arquivos. O usuário aprovou explicitamente, em
resposta “certo”, apenas os rótulos A–D e a omissão da linha de último estado
confirmado para MON UNKNOWN, nos viewports 1366x768 e 390x844. Essa aprovação
não cobre outros viewports, a composição completa da Camera Detail ou os demais
gates de HOM-01. DESIGN_QA permanece pendente; este follow-up não fecha HOM-01.

## 12. Aceite visual da composição integrada do Inventário (2026-10-12)

```text
ACTIVITY = ARGOS-HOM-01-INVENTORY-VISUAL-ACCEPTANCE
USER_DECISION = APPROVED / “O inventário para mim está legal.”
INVENTORY_HUMAN_VISUAL_APPROVAL = APPROVED / integrated composition
VIEWPORT_APPROVAL_SCOPE = COMPOSITION_LEVEL / no individual viewport approval inferred
KNOWN_HEADER_WRAP_FINDING = OPEN / 1366px wrap previously reported; later one-line observation does not prove resolution across all required viewports
CODE_CHANGED = NO / this activity
WIP_PRESERVED = YES
NEW_BRANCH = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
```

O aceite cobre a composição integrada do Inventário. Ele não certifica
individualmente 1920×1080, 1440×900, 1366×768 e 390×844. O finding de quebra
do cabeçalho MONITORAMENTO em 1366px permanece aberto, pois uma observação
posterior em uma linha não comprova sua resolução na cobertura responsiva
completa. Tabela desktop, cards mobile, filtros, ações, paginação, Design
System e funcionalidades ficam preservados. Nenhum ajuste visual foi feito
nesta atividade; não realizar novos ajustes sem finding material ou autorização.

## 13. Follow-up — recuperação do estado ativo da sidebar (2026-10-12)

Consultar também `PROJECT_STATE.md` seção 101 e o relatório
`docs/projeto/ARGOS_HOM_01_SIDEBAR_ACTIVE_STATE_RECOVERY.md`.

```text
ACTIVITY = ARGOS-HOM-01-SIDEBAR-ACTIVE-STATE-RECOVERY
BRANCH = codex/hom-v1-integration
HEAD = 11dcf7db0095416c125f8863ab89a2eef7fb278f
ROOT_CAUSE = Início, Governança and Eventos were outside the HOM-01 visual flag and inherited the legacy shell; active-link-only matching left the panel and surrounding layout divergent
FIX = scoped HOM-01 visual opt-in and full sidebar adapter for the three affected areas
SCOPED_FILES = templates/base.html; templates/components/sidebar.html; templates/components/navegacao_principal.html; static/css/sidebar-active-recovery.css; core/test_sidebar_navigation.py; core/test_frontend.py / activity hunks only
FIVE_PAGE_ACTIVE_LINK_CHECK = PASS / exactly one matching aria-current="page" on each real page
ACTIVE_STYLE = PASS / background #2563a6; white text/icon; 40px; 8px 12px; 5px radius; centered; weight 750
SHELL_STYLE = PASS / 232px panel; #182c3a; padding 20px 16px; content gap 24px; inactive links #d0dbe3
DASHBOARD_INVENTORY_REGRESSION = PASS / canonical pages preserved
DJANGO_CHECK = PASS / manage.py check --settings=scripts.localqa.test_settings
FOCUSED_TESTS = PASS / 90 across four modules
GIT_DIFF_CHECK = PASS
INTEGRATED_VISUAL_QA = PASS / five real routes in Edge at localhost:8765 after user-confirmed Django restart
CAPTURES = docs/projeto/evidence/sidebar-active-recovery/{inicio,dashboard,inventario,governanca,eventos}-current.png; contact-sheet.jpg
COMPUTED_STYLES = docs/projeto/evidence/sidebar-active-recovery/computed-styles.json
CAPTURE_VIEWPORT = 2552x866 CSS pixels; DPR 1; visualViewport.scale 1
RESPONSIVE_VISUAL_QA = NOT_CLAIMED
HUMAN_VISUAL_APPROVAL = APPROVED / user reply: “aprovo” / five current sidebar captures and contact sheet
APPROVAL_SCOPE = integrated desktop at 2552x866 CSS pixels; no responsive/mobile approval inferred
ACTIVITY_COMPLETE = YES / this bounded activity's gates are satisfied
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §101
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
NEXT_ACTION = continue remaining HOM-01 gates; do not close HOM-01 or release HOM-02 before they pass
```

O usuário rejeitou a primeira correção porque ela alinhava apenas o link ativo
e deixava o painel lateral e a composição circundante no shell legado. A causa
era a ausência da flag visual HOM-01 em Início, Governança e Eventos; a seleção
de rota do partial já estava correta. A nova correção aplica o shell HOM-01
completo nas três áreas, com escopo local e sem ampliar a carga global do UI V2.
`templates/components/sidebar.html` disponibiliza o hint de rolagem nas rotas
escopadas e `templates/components/navegacao_principal.html` o vincula à nav
com `aria-describedby`. `core/test_frontend.py` verifica a presença do opt-in e
hint acessível mantendo as asserções de ausência das folhas globais; somente
esses hunks pertencem a esta atividade, e outras alterações no arquivo são
WIP preexistente.

Após o usuário confirmar a reinicialização do Django, as cinco rotas reais
foram inspecionadas no Edge. O JSON de estilos computados registra um único
item ativo correspondente por rota e valores iguais entre as cinco páginas
para painel, fundo, padding, espaçamento, links inativos e estado ativo.
Dashboard e Inventário preservam a composição de referência. Os testes
direcionados, `manage.py check` e `git diff --check` passaram segundo a
validação mechanical.

A evidência visual atual cobre desktop em 2552×866 CSS pixels, DPR 1 e escala
visual 1. O usuário aprovou explicitamente as cinco páginas e a contact sheet
na resposta “aprovo”. O aceite não cobre validação mobile ou responsiva. Esta
atividade está completa; HOM-01 permanece em andamento para os demais gates e
este follow-up não encerra HOM-01 nem libera HOM-02.

## 14. HOM-01-SAFE-CHECKPOINT-AND-PUSH (2026-10-13)

```text
ACTIVITY = HOM-01-SAFE-CHECKPOINT-AND-PUSH
BRANCH = codex/hom-v1-integration
HEAD_BEFORE = b122ece404c3b67afdbd1acf9087e340d1c07d2c
HEAD_FINAL = THIS_CHECKPOINT_COMMIT / resolve with git rev-parse HEAD
V7_COMMIT = b122ece404c3b67afdbd1acf9087e340d1c07d2c / preserved
SIDEBAR_RECOVERY = PRESERVED / approved integrated desktop scope and evidence committed
MONITORING_A-D = PRESERVED / approved label behavior bounded to prior acceptance
INVENTORY_QUICK_DETAIL_DASHBOARD = PRESERVED / WIP committed; open visual findings remain explicit
COMMITS = 7c4fac3a81ba6311ecaf9bad2e080240759cfd0c; d0b4c2f5bef8d4533834898a67e4d2f03b0e2d1e; db0b10bc2a11ec6a20b8b8f9b36ba43573919814; this documentation checkpoint
DJANGO_CHECK = PASS / project virtual environment
TARGETED_TESTS = PASS / 105
GIT_DIFF_CHECK = PASS
REMOTE = https://github.com/wromanov/projeto_argos.git
REMOTE_BRANCH = codex/hom-v1-integration
PUSH = COMPLETED / normal push; exact SHA equality verified
WORKTREE_CLEAN = YES / staging empty / no relevant untracked files
DASHBOARD_V7_OVERALL_HUMAN_APPROVAL = PENDING / bounded composition approval from §105 remains preserved
SIDEBAR_DESKTOP_APPROVAL = PASS / five pages at 2552x866 CSS px; no mobile inference
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §106
```

O primeiro commit (`7c4fac3`) preserva a recuperação integrada da sidebar,
seus testes, relatório e capturas. O segundo (`d0b4c2f`) preserva a
localização dos estados MON e do resumo A–D, a semântica de UNKNOWN, Quick
Detail, o CSS de Inventário e a cobertura de regressão do Dashboard. O terceiro
(`db0b10b`) removeu uma senha fixa desnecessária do teste da sidebar. O quarto
commit é este registro documental. Todos foram revisados por staging explícito;
nenhum arquivo sensível/local foi publicado.

O teste do Dashboard falhou inicialmente porque ainda procurava o texto antigo
“Cadastro completo”; a asserção foi alinhada ao texto V7 “Cadastros completos”.
Depois da correção e do hardening do teste da sidebar, a bateria dirigida
completa passou com 105 testes e Django check sem issues, usando a configuração
isolada de testes. A suíte global histórica não foi executada neste checkpoint.

O remoto não possuía a branch antes da publicação. Foi publicado o mesmo nome
da branch local, sem merge, rebase ou force push, e o SHA remoto foi conferido
por `git ls-remote` e coincidiu com `git rev-parse HEAD`. Em outro computador,
inspecione a worktree antes do fetch; só faça checkout/fast-forward com estado
limpo e ancestralidade confirmada. Recrie `.venv` e o SQLite de QA sintético
localmente pelo fluxo de `INICIAR_ARGOS_QA.cmd`; não copie banco, venv, sessão ou
credenciais. Dashboard V7 é verificado em `http://127.0.0.1:8765/dashboard/`.

O aceite prévio do Dashboard V7 em §105 permanece limitado à composição
apresentada; aceite global da matriz continua pendente. Permanecem o finding
de quebra do cabeçalho MONITORAMENTO a 1366px, QA responsivo da sidebar não
reivindicado e revisão visual mais ampla da Camera Detail. HOM-01 segue aberta;
HOM-02 continua bloqueada.

## 15. Aceite visual do Dashboard V7 — matriz integrada (2026-10-13)

Consultar `PROJECT_STATE.md` §108, `AGENT_CONTINUITY.md` §20.68 e
`docs/projeto/evidence/dashboard-v7-integrated-qa/REPORT.md`.

```text
ACTIVITY = HOM-01-DASHBOARD-V7-VISUAL-ACCEPTANCE
USER_DECISION = APPROVED / “Eu validei e está ok.”
DASHBOARD_V7_HUMAN_VISUAL_APPROVAL = PASS
APPROVED_VIEWPORTS = 1920x1080, 1440x900, 1366x768, 390x844
DPR_OBSERVED = 0.9
ZOOM_100_PERCENT = NOT_VERIFIED
PIXEL_PERFECT_COMPARISON = NOT_CLAIMED
VISUAL_COMPOSITION = PRESERVE / no new visual adjustments
AUDIT = NOT_REPEATED
SOURCE_CODE_CHANGE = NO
ACTIVITY_COMPLETION_PERCENT = 100%
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §108
```

O aceite humano cobre as quatro capturas existentes da página Django integrada.
O DPR foi observado em 0,9; não houve verificação de zoom a 100% nem comparação
pixel a pixel. A atividade de aceite visual está completa, mas HOM-01 permanece
em andamento para seus demais gates e HOM-02 continua bloqueada. A composição
V7 deve ser preservada; a auditoria aceita não deve ser repetida.

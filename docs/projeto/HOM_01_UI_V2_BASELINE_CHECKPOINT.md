# ARGOS HOM-01 — baseline integrada UI V2

```text
PROJECT_ID = projeto_argos
ACTIVITY = ARGOS-HOM-01-FINAL-BASELINE-CHECKPOINT
BASELINE_NAME = ARGOS_HOM_01_UI_V2_INTEGRATED_BASELINE
BASELINE_BRANCH = codex/hom-v1-integration
BASELINE_CODE_COMMIT = 188afda5470e252fa8cf6fed5556a404073ee4fc
PREVIOUS_DOCUMENT_CHECKPOINT = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
DOCUMENT_CHECKPOINT_COMMIT = PENDING / fill after authorized documentation commit
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

| Gate | Resultado em 2026-10-11 | Evidência / pendência |
|---|---|---|
| `TECHNICAL_GATE` | `FAIL / PARTIAL` | `manage.py check` PASS; regressões dirigidas 405/406, com falha em `cameras.test_governanca_views.GovernancaViewsPermissoesTests.test_dashboard_exibe_situacoes_completude_e_ips_duplicados`; suíte global interrompida sem resumo após duas falhas sinalizadas. |
| `VISUAL_GATE` | `BLOCKED / PARTIAL APPROVALS` | Aceites humanos restritos abaixo; sem renderização integrada arquivada, comparação suficiente ou QA integrado nos quatro viewports. |
| `DOCUMENTATION_GATE` | `PASS` após commit deste checkpoint | Este documento, `PROJECT_STATE.md`, continuidade, mapa de documentos e authority de branches atualizados. |
| `GIT_RECONCILIATION_GATE` | `PARTIAL / UNVERIFIED WIP` | Ancestry e refs Git examinados; acesso de leitura aos diretórios de worktree P3/P5 negado pelo host. Não houve merge ou cherry-pick. |
| `PUBLICATION_GATE` | `NO` | Não há upstream/ref remota HOM local; branch está 9 commits à frente da ref local `origin/master`. Consulta remota ao vivo falhou por DNS e WIP externo está UNVERIFIED. Nenhum push executado. |

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

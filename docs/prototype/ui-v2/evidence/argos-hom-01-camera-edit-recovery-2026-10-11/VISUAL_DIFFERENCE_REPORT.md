# ARGOS-HOM-01-CAMERA-EDIT-RECOVERY — evidências visuais

```text
ACTIVITY = ARGOS-HOM-01-CAMERA-EDIT-RECOVERY
STATUS = PARTIAL / IMPLEMENTATION AND FUNCTIONAL REGRESSION PASS
DESIGN_QA = BLOCKED / INTEGRATED BROWSER RENDER NOT CAPTURED
HUMAN_VISUAL_APPROVAL = PENDING
DS_CANONICAL = 2.0.2
```

## Referência aprovada

As capturas P3-D de criação e edição foram copiadas sem alteração de bytes do
commit P3 ROOT reconciliado `9ce90bafdd67cb2b878edcdd2c4ecb1b4e849522`. O SHA-1
de cada cópia foi comparado ao blob Git de origem. A aprovação humana da família
está registrada no commit `f5dd0308f46705e03c79609077ed1ec7a12bc766`.

As imagens estão em [`reference/`](reference/): nove capturas por tela entre
criação e edição, incluindo 1920×1080, 1440×900, 1366×768 e 390×844, além de
conteúdo longo, erro, foco, seleção e sucesso demonstrativo.

## Renderização integrada

```text
TARGET_SCREENSHOTS = NONE
TARGET_VIEWPORTS = NOT_CAPTURED
VISUAL_DIFFERENCES = NOT_ASSESSED
```

Não houve render real do formulário Django neste ambiente. A continuidade
registrou falha de acesso ao servidor local por loopback e orienta não repetir
uma tentativa equivalente; o navegador local não pôde receber a página. Os
screenshots P3-D acima documentam somente a referência e não são apresentados
como capturas da implementação produtiva. Portanto não há comparação visual,
avaliação responsiva integrada ou aprovação humana nesta etapa.

## Adaptações funcionais conhecidas

- A criação mantém a escolha de situação operacional dentro de Identificação; a
  edição apresenta a situação existente em contexto e não oferece controle de
  ciclo de vida.
- A navegação de edição retorna à Camera Detail, como exige o fluxo Django atual;
  a criação retorna ao Inventário.
- Avisos e sucessos de demonstração do protótipo não foram copiados. A tela usa
  erros vinculados ao Django Form, token CSRF e mensagens reais do fluxo após
  persistência.
- Upload não aparece na tela de edição e continua em Camera Detail.

Essas decisões foram confirmadas pelo mapeamento estático dos fluxos e testes.
Elas não substituem a comparação da tela renderizada.

## Validação funcional

```text
DJANGO_CHECK = PASS
TARGETED_REGRESSION = PASS / 177 TESTS
TEST_DATABASE = SQLITE IN-MEMORY
TEMPORARY_MEDIA = ISOLATED UNDER WORKSPACE; REMOVED AFTER RUN
CREATE_EDIT_AUDIT_PERMISSIONS_CSRF_CATALOGS_IP_CHANGE = COVERED
CAMERA_DETAIL_QUICK_DETAIL_SHELL_DASHBOARD_INVENTORY = REGRESSION PASS
MANUAL_IMAGE_UPLOAD = 7 TESTS PASS; UPLOAD LOCATION UNCHANGED
```

## Próximo passo para encerrar os gates visuais

Use o launcher QA local [`INICIAR_ARGOS_QA.cmd`](../../../../../INICIAR_ARGOS_QA.cmd)
e o runbook em
[`hom-01-visual-qa-2026-10-11/README.md`](../hom-01-visual-qa-2026-10-11/README.md).
Capture a criação e a edição integradas nos quatro viewports prioritários,
incluindo estados reais de erro/foco e conteúdo longo. Registre as imagens em uma
pasta `target/`, compare com as referências correspondentes e solicite a
aprovação visual humana. Até essa revisão, `DESIGN_QA = BLOCKED`,
`HUMAN_VISUAL_APPROVAL = PENDING` e `HOM_01_STATUS = IN_PROGRESS`.

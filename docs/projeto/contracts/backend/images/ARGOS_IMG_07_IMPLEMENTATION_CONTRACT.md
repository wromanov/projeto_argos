# ARGOS IMG-07 — Implementation Contract

```text
STATUS = RATIFIED_FOR_ARGOS_IMG_07
DOCUMENT_TYPE = SLICE_IMPLEMENTATION_CONTRACT
CONTRACT_ID = ARGOS-IMG-07-IMPLEMENTATION-CONTRACT
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E2
ACTIVE_SLICE = ARGOS-IMG-07-CONFORMANCE
ACTIVITY = ARGOS-IMG-07-FORMAL-CONTRACT-RATIFICATION
DECISION_ID = ARGOS-IMG-07-FORMAL-CONTRACT-RATIFICATION
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
COMMIT = NOT_AUTHORIZED
PUSH = NOT_AUTHORIZED
DEPLOY = NOT_AUTHORIZED
CONTRACT_RATIFICATION_DECISION = APPROVED
ROOT_ADJUDICATION = APPROVED
CONTRACT_STATUS = RATIFIED_FOR_ARGOS_IMG_07
RATIFICATION_DATE = 2026-10-17
HUMAN_CONDITIONAL_AUTHORIZATION = SATISFIED
HUMAN_APPROVAL_EVIDENCE = instrução do usuário nesta atividade: FORMAL_RATIFICATION_APPROVED_CONDITIONAL; condição satisfeita após ROOT PASS
CONTRACT_CONFORMANCE = PASS
TECHNICAL_GAPS = NONE
SECURITY_INVARIANTS = PRESERVED
IMPLEMENTATION_STATUS = NOT_STARTED / NOT_GRANTED
NEXT_GATE = ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW
```

Este contrato registra requisitos adjudicados de conformidade para leitura de
imagem do Quick Detail e é ratificado somente para a slice ARGOS-IMG-07. Não
substitui o contrato de domínio nem autoriza implementação. A decisão root
`ARGOS-IMG-07-FORMAL-CONTRACT-RATIFICATION` foi APPROVED em 2026-10-17 após
satisfação da autorização humana condicional. Implementação permanece
NOT_GRANTED e exige `ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW`.

## 1. Escopo e autoridade

O escopo é a conformidade do CameraQuickDetailPanel com a seleção
`LATEST_ACTIVE_IMAGE` da seção 26 de
`docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`. O contrato de domínio é a
authority normativa. Em particular, §7 preserva `LATEST_CAMERA_CAPTURE`, §24
define a entrega privada da captura técnica, §25 governa `DISPLAY_IMAGE` do
Inventário e §26 altera somente a seleção de imagem apresentada pelo Quick
Detail. A separação e a precedência entre contratos permanecem intactas.

O protótipo e as authorities visuais aprovadas governam composição e
interação. `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md` e
`docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md` registram que a baseline do Quick
Detail é `APPROVED / PROTECTED`, com redesign não autorizado. Este draft não
modifica essas authorities.

## 2. Decisões adjudicadas e invariantes

1. O Quick Detail seleciona o registro ativo mais recente de qualquer
   proveniência permitida, sem filtro por disponibilidade/integridade:
   `withdrawn_at IS NULL`, ordenação `recorded_at DESC, immutable_id DESC`.
   A seleção precede a avaliação dos bytes.
2. Se o registro selecionado estiver indisponível ou inválido, a leitura
   reporta seu estado sem procurar registro anterior e sem fallback.
3. A identidade selecionada no JSON e os bytes da prévia devem pertencer ao
   mesmo `immutable_id` e à mesma câmera. A projeção/rota privada do Quick
   Detail vincula câmera, `immutable_id` e variante fechada.
4. A seleção exige usuário autenticado, `cameras.view_camera`, câmera
   pertencente ao contexto consultado e registro ainda ativo/corrente. A
   entrega valida integridade e serve somente bytes privados autorizados.
5. Se o registro deixar de ser o corrente entre a projeção JSON e a prévia, a
   resposta adjudicada é `409 STALE_SELECTION`, sanitizada e sem conteúdo. Não
   serve outro registro e não tenta novamente automaticamente. O erro nativo
   do elemento `<img>` não expõe necessariamente o status HTTP; sem status
   explícito disponível à interface, apresentar somente o texto genérico
   aprovado, sem inferir stale.
6. Dados de imagem selecionada e estado técnico de `LATEST_CAMERA_CAPTURE`
   são semanticamente separados. `capture_state` descreve somente a captura
   técnica e nunca qualifica a imagem selecionada pelo Quick Detail.
7. Leitura, seleção e prévia não capturam, não alteram monitoramento e não
   geram efeitos colaterais. Nenhuma política de Inventário é alterada.

## 3. Projeção, identidade e entrega

A resposta mantém o envelope JSON existente `camera, location, monitoring,
image, links`. O consumidor é o Quick Detail. Dentro de `image`, preservar
`state`, `source`, `capture_state` e `preview_url`, acrescentando:

| Campo | Contrato |
|---|---|
| `immutable_id` | UUID imutável como string; `null` quando não há registro selecionado. |
| `recorded_at` | Timestamp ISO 8601 com offset; `null` quando não há registro selecionado. |
| `source` | Proveniência real do registro; `NONE` quando não há imagem. |
| `state` | Estado de apresentação existente, incluindo `NO_IMAGE_AVAILABLE`, `UNAVAILABLE` e `ERROR` conforme o resultado. |
| `capture_state` | Estado exclusivamente técnico de captura, separado da imagem selecionada. |
| `preview_url` | Referência autorizada somente quando `state=AVAILABLE`; vinculada ao `camera.id` já existente e ao mesmo `immutable_id`; `null` sem imagem ou sem preview disponível. |

Sem registro: `source=NONE`, `state=NO_IMAGE_AVAILABLE`, `immutable_id=null`,
`recorded_at=null`, `preview_url=null`. Com registro, preencher UUID, timestamp
e proveniência reais, mesmo quando o estado for `UNAVAILABLE` ou `ERROR`.
Timestamp ausente/malformado nunca usa `captured_at` como fallback: omitir a
apresentação com segurança e registrar/emitir diagnóstico pelo backend,
preservando o estado da imagem. Não criar payload alternativo nem adicionar
storage key/path/segredo. Não inventar endpoint ou path concreto.

A futura requisição de preview deve estar bound à câmera e ao
`immutable_id`, com variante/query validada por allowlist. A sequência de
validação é: autenticação; permissão `cameras.view_camera`; formato, variante
e query; câmera existente e dentro do escopo; UUID existente e pertencente à
câmera. Identidade inexistente, não autorizada ou de outra câmera retorna 404
sanitizado, sem revelar existência. Se o registro autorizado da própria
câmera deixou de ser corrente por withdrawal ou supersession, retornar 409
`STALE_SELECTION` antes de acessar storage ou bytes. Revalidar, a cada
requisição de preview, que o UUID continua sendo a seleção
`LATEST_ACTIVE_IMAGE` corrente: registros `withdrawn_at IS NULL`, ordenados
`recorded_at DESC, immutable_id DESC`. Não inferir ou expor chave/caminho de
storage.

A validação inicial ocorre antes de qualquer leitura de storage/bytes. Depois
do load e do processamento de bytes (hash, decode e re-encode), mas antes de
construir qualquer resposta `200`, executar uma segunda leitura canônica fresca
de `LATEST_ACTIVE_IMAGE` conforme §26. Se câmera, UUID, corrente ou lifecycle
divergir da identidade selecionada no JSON, descartar os bytes em memória e
retornar `409 STALE_SELECTION` com corpo vazio, `no-store` e `nosniff`; não
fazer fallback nem retry. Esta segunda leitura é o ponto de linearização do
atendimento. Alterações posteriores a esse ponto não são garantidas pelo
contrato. Não manter lock ou snapshot/transaction durante I/O; ambas as
validações usam leituras canônicas frescas. Se o I/O falhar e o resultado
seria `422` ou `503`, revalidar a seleção antes da resposta: se tiver ficado
stale durante a operação, `409` tem precedência sobre `422`/`503`.

Aplicar os controles de segurança da entrega privada estabelecidos em
`ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` §24: validar hash e decodificação/regravação
conforme o pipeline aprovado, servir objeto privado e enviar `Cache-Control:
no-store` e `X-Content-Type-Options: nosniff`. Isso não declara a rota atual de
§24 apropriada à seleção IMG-07 nem presume endpoint por identidade existente;
eventual reuso de componentes internos deve preservar o vínculo definido aqui.
Resultados futuros da superfície IMG-07: `401` não autenticado; `403` sem
permissão; `400` formato/variante/query inválidos; `404` identidade ausente,
não autorizada ou de outra câmera; `409 STALE_SELECTION` para registro
autorizado próprio mas withdrawn/superseded; `503` selecionado indisponível;
`422` falha de integridade após autorização do ID selecionado; `200` com
`image/jpeg` e `Content-Disposition: inline`. Em `404`, usar sempre o estado
genérico `NOT_FOUND`; não distinguir câmera de registro quando isso revelar
existência. Reusar a semântica/mapeamento aprovado de §24 para
401/403/400/404/503/422/200 somente na futura superfície IMG-07; §24 continua
exclusivamente latest-capture e não se afirma reuso de sua rota. `409` é
resultado stale novo. `X-Preview-State` é mapeado sem ambiguidade:

| HTTP | `X-Preview-State` |
|---|---|
| 401 | `UNAUTHENTICATED` |
| 403 | `FORBIDDEN` |
| 400 | `INVALID_VARIANT` |
| 404 | `NOT_FOUND` |
| 409 | `STALE_SELECTION` |
| 503 | `UNAVAILABLE` |
| 422 | `ERROR` |
| 200 | `AVAILABLE` |

`NO_IMAGE_AVAILABLE` pertence somente à projeção JSON sem registro e não
possui URL/endpoint de preview. Todas as respostas da superfície IMG-07,
incluindo erros, usam `Cache-Control: no-store` e
`X-Content-Type-Options: nosniff`. Respostas de erro têm corpo vazio e não
incluem bytes. Resultados `503` e `422` só podem ocorrer depois de validar a
autorização do registro selecionado. Não revelar existência de identidade
não autorizada.

## 4. Estados e fallback

Preservar os estados de domínio definidos pelas authorities de imagem:

| Estado do registro já selecionado | Comportamento do Quick Detail |
|---|---|
| Ausente | Estado sem imagem, sem inventar registro ou origem. |
| Disponível e íntegro | Identidade selecionada e prévia do mesmo `immutable_id`. |
| Indisponível | Estado explícito do selecionado, sem bytes e sem fallback. |
| Erro de integridade/validação | Erro explícito e sanitizado do selecionado, sem fallback. |
| Seleção ficou obsoleta antes da prévia | `409 STALE_SELECTION`, sem conteúdo e sem retry automático. |

Falhas de autenticação, autorização, consulta, correspondência de câmera,
identidade ou variante não podem ser convertidas em ausência de imagem nem
fazer a resposta revelar dados privados. A matriz futura de resultados está
fechada na seção 3. JSON sem registro usa `source=NONE`,
`state=NO_IMAGE_AVAILABLE` e UUID/timestamp/preview nulos. Erros de entrega
têm corpo vazio e nunca servem bytes.

## 5. Limites de escopo

Este contrato não cria `PRIMARY_IMAGE`, galeria, fluxo de captura, fluxo de
upload, rotação, purge/expurgo, schema ou migration. Não altera proveniência,
histórico ou lifecycle além dos requisitos de seleção e validação descritos
acima. Captura e upload permanecem manuais segundo os contratos vigentes; este
draft não define novo comportamento para essas operações.

`LATEST_CAMERA_CAPTURE` permanece isolado: somente `CAPTURA_CAMERA`, seleção e
ordenação de §7, entrega `ultima-captura` de §24 e consumidores técnicos. A
política `DISPLAY_IMAGE`/`preview_exibicao` continua sendo a de §25 para
Inventário; Inventário não herda §26. Nenhuma rota existente de captura passa
a aceitar upload ou a servir a imagem selecionada do Quick Detail.

## 6. Impacto visual e revisão

Quick Detail permanece visual e funcionalmente protegido: preservar dialog,
composição, navegação/foco, ações, contexto do Inventário, layout e CSS
aprovados. `UI_IMPACT=MICRO_ADJUSTMENT`, `PROTOTYPE_REQUIRED=NO` e
`PROTECTED_LAYOUT=REQUIRED`. As decisões UI-IMG07-01 e UI-IMG07-02 estão
aprovadas. Manter a sequência vertical IMAGEM, IDENTIDADE, INFORMAÇÕES GERAIS,
LOCALIZAÇÃO, MONITORAMENTO, FOOTER. Exibir `recorded_at` na região de imagem
existente como texto exato `Registrada em DD/MM/AAAA às HH:MM`, locale `pt-BR`
e timezone explícito `America/Sao_Paulo` conforme `config/settings.py`.
Ancorar no título da seção de imagem. Sem registro, não mostrar data; com
registro indisponível/erro, mostrar se timestamp válido. Timestamp
inválido/ausente é omitido e nunca substituído por `captured_at`. Usar texto
simples, anunciável por tecnologia assistiva, com quebra natural e sem
clipping/overflow. Não adicionar card/campo, redimensionar drawer, reordenar
seções ou criar nova área de scroll. Se não couber na composição aprovada,
registrar divergência e `STOP_AND_ESCALATE`, sem mudança de layout.

Rótulos aprovados para estados existentes (não criam estados de domínio):

| Estado/origem | Texto literal |
|---|---|
| `CAPTURA_CAMERA` | “Imagem capturada pela câmera” |
| `UPLOAD_MANUAL` | “Imagem enviada manualmente” |
| Sem imagem | “Nenhuma imagem disponível” |
| Imagem indisponível | “Imagem temporariamente indisponível” |
| Erro de integridade | “Não foi possível exibir a imagem” |
| Erro do `<img>` sem status explícito | “Não foi possível carregar a imagem selecionada” |

Não atribuir stale ao erro genérico do `<img>`; usar mensagem de stale somente
quando o frontend receber explicitamente o status correspondente.

## 7. Requisitos de validação futura (não executados)

Implementação e validação runtime continuam pendentes. A QA futura deve cobrir
capture versus upload; ordenação/desempate; withdrawal; estados sem bytes;
stale antes do storage; mesma identidade/câmera JSON-preview; authz, isolamento
e matriz HTTP; allowlist, hash e headers; Inventário e captura técnica; seis
rótulos, timestamp, frontend status handling; acessibilidade, responsividade,
footer acessível e ausência de nova rolagem interna/overflow nos viewports
2048×741, 2048×914, 1920×1080, 1366×768, 900×768 e 390×844. Verificar timestamp
em estados ausente, indisponível, erro e malformed. Para concorrência, usar
fake storage com barrier após load/decode: inserir um registro mais novo ou
retirar o selecionado, liberar o barrier e exigir 409 sem bytes; controle sem
mudança exige 200. Verificar IDs/câmeras cruzados e requests paralelos. A
revalidação também deve preceder `422`/`503` após falha de I/O, com 409
prioritário quando stale. `CONTRACT_READY=YES` não
equivale a `VISUAL_QA_PASS`; este último está `NOT_RUN`. Se não couber sem
alterar composição protegida, parar e escalar ao usuário. Nenhum teste/runtime
foi executado nesta atividade documental.

## 8. Estado da ratificação e próximo gate

Decisão formal `ARGOS-IMG-07-FORMAL-CONTRACT-RATIFICATION` = APPROVED,
2026-10-17. Autorização humana condicional satisfeita. A revisão root
registrou `CONTRACT_CONFORMANCE=PASS`, `TECHNICAL_GAPS=NONE`,
`VISUAL_DECISIONS=APPROVED`, `SECURITY_INVARIANTS=PRESERVED`; architect não foi
invocado porque não havia conflito ou ambiguidade material. Este contrato é
ratificado somente para ARGOS-IMG-07; nenhuma authority superior foi alterada.
Não há evidência de implementação/endpoints IMG-07 existentes. Esta
ratificação documental não declara `VISUAL_QA_PASS` nem validação runtime.

Os requisitos de validação futura da seção 7 continuam necessários antes de
qualquer declaração de implementação/QA. `IMPLEMENTATION_STATUS =
NOT_STARTED / NOT_GRANTED`; próximo gate:
`ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW`.

`PRIMARY_IMAGE` permanece questão independente e aberta. Mudança da matriz de
autorização ou da semântica de histórico/backend exige decisão própria. §26 do
contrato de domínio é decisão específica/posterior somente para seleção do
Quick Detail; o texto legado do UI DS que prioriza `LATEST_CAMERA_CAPTURE`
permanece aplicável à captura técnica e não altera Inventário §25 nem a rota
`LATEST_CAMERA_CAPTURE`. §§24/25 existentes não são endpoints IMG-07 por
identidade. Inventário `DISPLAY_IMAGE`, `ultima-captura` e `preview_exibicao`
permanecem protegidos. Nenhuma `PENDING_USER_DECISION` resta nesta revisão;
gates de implementação seguem pendentes. Próximo gate:
`ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW`.

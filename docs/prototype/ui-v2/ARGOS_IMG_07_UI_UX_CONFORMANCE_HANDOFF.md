# ARGOS IMG-07 — UI/UX Conformance Handoff

```text
STATUS = FINAL_HANDOFF_FOR_RATIFIED_CONTRACT
DOCUMENT_TYPE = UI_UX_CONFORMANCE_HANDOFF
HANDOFF_ID = ARGOS-IMG-07-UI-UX-CONFORMANCE-HANDOFF
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E2
ACTIVE_SLICE = ARGOS-IMG-07-CONFORMANCE
ACTIVITY = ARGOS-IMG-07-IMPLEMENTATION-CONTRACT-AND-UI-HANDOFF
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
QUICK_DETAIL = APPROVED / PROTECTED
QUICK_DETAIL_STRUCTURE = PROTECTED
REDESIGN_AUTHORIZED = NO
UI_IMPACT = MICRO_ADJUSTMENT
PROTOTYPE_REQUIRED = NO
VISUAL_DECISIONS = APPROVED
PROTECTED_LAYOUT = REQUIRED
CONTRACT_RATIFICATION_DECISION = APPROVED
CONTRACT_STATUS = RATIFIED_FOR_ARGOS_IMG_07
VISUAL_IMPLEMENTATION = NOT_STARTED
NEXT_GATE = ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW
```

Este handoff encaminha a revisão de conformidade visual e funcional do Quick
Detail. A baseline aprovada segue protegida. As decisões visuais UI-IMG07-01
e UI-IMG07-02 estão aprovadas, conforme §7. A ratificação formal do contrato
consta na seção 8; este handoff não autoriza implementação.

## 1. Autoridade e vínculo com o contrato

O contrato de domínio
[`ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`](../../projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md)
§26 é a authority para a imagem que o Quick Detail apresenta. O contrato
backend da mesma slice,
[`ARGOS_IMG_07_IMPLEMENTATION_CONTRACT.md`](../../projeto/contracts/backend/images/ARGOS_IMG_07_IMPLEMENTATION_CONTRACT.md),
registra a identidade JSON/prévia, estados, segurança e limites já
adjudicados. Este handoff mantém apenas o necessário para orientar o review e
os cenários de conformance.

O `ARGOS_UI_V2_VISUAL_CONTRACT.md` e o `ARGOS_UI_V2_MASTER_PLAN.md` preservam a
baseline atual do Quick Detail como `APPROVED / PROTECTED`. Composição e
interações aprovadas prevalecem para a tela. §25 do contrato de domínio
continua regendo `DISPLAY_IMAGE`/`preview_exibicao` do Inventário; a política
§26 não é herdada pelo Inventário. `LATEST_CAMERA_CAPTURE` conserva sua
semântica técnica separada, apenas de `CAPTURA_CAMERA`.

## 2. Resultado funcional a representar

O Quick Detail deve apresentar a imagem selecionada por `LATEST_ACTIVE_IMAGE`:
registro ativo mais recente por `recorded_at DESC, immutable_id DESC`, entre
as proveniências permitidas, com seleção anterior à avaliação de
disponibilidade/integridade. A imagem selecionada e a prévia devem apontar ao
mesmo `immutable_id`. Imagem ausente, indisponível ou com erro deve manter seu
estado explícito sem fallback para um registro anterior.

O painel deve distinguir semanticamente a identidade/estado dessa imagem do
`capture_state` técnico. Não apresentar a imagem como “última captura” apenas
porque seu registro é o mais recente. Sugestão de conteúdo para o review:
estado e origem apresentados de modo inequívoco, preservando contexto e
densidade atuais; a sugestão não define o texto final.

Se a seleção mudar antes da prévia, o resultado é `409 STALE_SELECTION`, sem
conteúdo, sem exibir outro registro e sem retry automático. A leitura não deve
iniciar captura nem alterar monitoramento.

## 3. Baseline a preservar

Preservar a composição do Quick Detail aprovado, incluindo dialog, hierarquia,
layout, densidade, ações e contexto do Inventário. Preservar navegação,
comportamento e gerenciamento de foco. Não alterar CSS ou reestruturar o painel
como parte desta atividade documental. A tela precisa manter acessibilidade e
comportamentos já aprovados.

## 4. Decisões de apresentação aprovadas

UI-IMG07-01 = APPROVED; UI-IMG07-02 = APPROVED_OPTION_B. Os seis textos
aprovados para estados existentes (não criam estados de domínio) são os da
seção 7. `PRIMARY_IMAGE` permanece uma decisão independente e não é resolvida
por este handoff.

## 5. Cenários de conformance para execução futura

Os seguintes cenários são requisitos de uma validação posterior, ainda não
executada nesta atividade:

| Cenário | Evidência esperada |
|---|---|
| Upload manual mais recente que captura | Quick Detail segue o registro ativo mais recente; não o rotula incorretamente como captura. |
| Captura mais recente | Imagem selecionada e identidade apresentada correspondem ao registro mais recente. |
| `recorded_at` empatado | O desempate estável usa `immutable_id DESC`. |
| Registro retirado logicamente | Não é selecionado como registro ativo corrente. |
| Selecionado indisponível ou inválido | Estado explícito do selecionado; sem fallback ou bytes incorretos. |
| Seleção muda antes do preview | `409 STALE_SELECTION`, sem conteúdo, sem troca silenciosa e sem retry automático. |
| Câmera incompatível, anônimo, sem permissão | Falha privada/autorizativa sanitizada; nenhuma prévia indevida. |
| Variante fechada ou query inválida | Rejeição conforme contrato, sem exposição de bytes. |
| Entrega de bytes | `no-store`, `nosniff`, hash e decode/re-encode conferidos, sem storage path/key. |
| Isolamento de políticas | Inventário continua em §25; rota de `ultima-captura` continua somente captura técnica. |
| Efeito colateral | Seleção/leitura/prévia não mutam monitoramento nem iniciam captura. |
| Requests simultâneos ou troca rápida | Identidade não cruza câmeras/registros; seleção obsoleta não mostra preview errado. |
| Acessibilidade | Teclado, foco, leitor de tela e estados sem bytes verificados sem regressão. |
| Comparação visual | Baseline comparada nos viewports aplicáveis, com diferenças registradas para decisão humana. |

Esta tabela descreve trabalho futuro; nenhum teste, captura, inspeção de
browser ou validação visual é declarado como executado por este handoff.

## 6. Fora do escopo e gate

Não criar ou especificar `PRIMARY_IMAGE`, galeria, novo fluxo de captura ou
upload, rotação, purge/expurgo, schema ou migration. Não mudar `LATEST_CAMERA_CAPTURE`,
`ultima-captura`, Inventário §25 (`DISPLAY_IMAGE`/`preview_exibicao`),
monitoramento, autorização ou histórico. §26 prevalece somente para seleção
Quick Detail; o texto legado UI DS que prioriza `LATEST_CAMERA_CAPTURE`
permanece aplicável à captura técnica. §§24/25 não são endpoints IMG-07 por
identidade. Este handoff final acompanha contrato ratificado para IMG-07;
implementação continua não autorizada. Próximo gate:
`ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW`.

## 7. Adjudicação visual posterior — estado vigente

Esta seção supersede somente as afirmações anteriores neste draft que tratavam decisões de apresentação como pendentes. UI-IMG07-01 = APPROVED; UI-IMG07-02 = APPROVED_OPTION_B. `UI_IMPACT=MICRO_ADJUSTMENT`, `PROTOTYPE_REQUIRED=NO`, `VISUAL_DECISIONS=APPROVED`, `PROTECTED_LAYOUT=REQUIRED`.

Rótulos literais para estados existentes (não criam estados de domínio):

| Estado/origem | Texto literal aprovado |
|---|---|
| `CAPTURA_CAMERA` | “Imagem capturada pela câmera” |
| `UPLOAD_MANUAL` | “Imagem enviada manualmente” |
| Sem imagem | “Nenhuma imagem disponível” |
| Imagem indisponível | “Imagem temporariamente indisponível” |
| Erro de integridade | “Não foi possível exibir a imagem” |
| Erro do `<img>` sem status explícito | “Não foi possível carregar a imagem selecionada” |

Mostrar `recorded_at` discretamente na região de imagem existente, usando formato e timezone do aplicativo; não usar `captured_at`. Não criar card/campo nem alterar estrutura do drawer. Preservar sequência IMAGEM, IDENTIDADE, INFORMAÇÕES GERAIS, LOCALIZAÇÃO, MONITORAMENTO, FOOTER. Se não couber, registrar divergência e STOP_AND_ESCALATE sem alterar layout. Erro de `<img>` sem status HTTP explícito usa somente a mensagem genérica aprovada, sem inferir stale.

O JSON já existente e a futura preview devem referenciar a mesma câmera e `immutable_id`; projetar identity, provenance, `recorded_at`, presentation state e authorized preview ref no JSON existente, sem payload alternativo nem storage paths/keys. Stale futuro: 409 STALE_SELECTION sem bytes, retry ou fallback. `capture_state` é exclusivo técnico; §26 prevalece para seleção do Quick Detail sem mudar Inventário §25, `DISPLAY_IMAGE`, `ultima-captura`, `preview_exibicao` ou rota `LATEST_CAMERA_CAPTURE`. §§24/25 não são endpoints IMG-07 por identidade. Validação futura inclui frontend status handling, seis rótulos, timestamp, todos os cenários da seção 5, acessibilidade e responsividade. Nada foi executado nesta atividade.

## 8. Revisão técnica — estado vigente

Esta revisão registra os gaps 1–3 fechados pelo contrato ratificado.
`CONTRACT_CONFORMANCE=PASS`, `TECHNICAL_GAPS=NONE`,
`SECURITY_INVARIANTS=PRESERVED`; decisão formal
`ARGOS-IMG-07-FORMAL-CONTRACT-RATIFICATION` APPROVED em 2026-10-17, após
satisfação da autorização humana condicional. Este artefato permanece um
handoff de UI/UX, não um contrato canônico novo. `VISUAL_IMPLEMENTATION=NOT_STARTED`;
implementação não autorizada por este handoff. Próximo gate:
`ARGOS_IMG_07_IMPLEMENTATION_AUTHORIZATION_REVIEW`. E3 proibida.

O JSON mantém o envelope existente `camera, location, monitoring, image,
links`. Em `image`, manter `state`, `source`, `capture_state`, `preview_url` e
acrescentar `immutable_id` como UUID string e `recorded_at` ISO8601 com offset.
Sem registro: `source=NONE`, `state=NO_IMAGE_AVAILABLE`, ID/timestamp/preview
nulos. Com registro, projetar valores reais inclusive `UNAVAILABLE`/`ERROR`.
Preview só em `AVAILABLE`, bound ao `camera.id` já existente + mesmo
`immutable_id`. `capture_state` permanece exclusivamente técnico. Timestamp
inválido/ausente é omitido e diagnosticado no backend; nunca fallback a
`captured_at`. Sem payload alternativo, storage key/path/secret ou endpoint
concreto inventado.

Sequência de validação da futura superfície: auth → `cameras.view_camera` →
validar formato/variante/query → câmera existe/no escopo → UUID existe e
pertence à câmera. UUID ausente/não autorizado/outra câmera: 404 sanitizado.
UUID autorizado próprio, mas withdrawn/superseded: 409 `STALE_SELECTION`
antes de storage/bytes. Revalidar em cada request que continua sendo
`LATEST_ACTIVE_IMAGE` (`withdrawn_at IS NULL`, `recorded_at DESC`,
`immutable_id DESC`). Sem retry/fallback; erros com body vazio. Reusar somente
o mapeamento de §24 para 401/403/400/404/503/422/200 na superfície futura; §24
continua latest-capture-only e nenhuma rota é presumida/reusada por assertion.
409 é novo. 503 indisponível e 422 integridade somente após autorização do ID;
200 `image/jpeg` inline. `X-Preview-State`: 401=`UNAUTHENTICATED`,
403=`FORBIDDEN`, 400=`INVALID_VARIANT`, 404=`NOT_FOUND` genérico para câmera
ou UUID ausente/não autorizado/outra câmera, 409=`STALE_SELECTION`,
503=`UNAVAILABLE`, 422=`ERROR`, 200=`AVAILABLE`. `NO_IMAGE_AVAILABLE` é só
estado da projeção JSON sem URL/endpoint de preview. Todas as respostas,
inclusive erros, usam `Cache-Control: no-store` e
`X-Content-Type-Options: nosniff`; erros não têm body nem bytes. Não vazar
existência não autorizada.

Timestamp exato: `Registrada em DD/MM/AAAA às HH:MM`, locale `pt-BR`, timezone
explícito `America/Sao_Paulo` conforme `config/settings.py`, ancorado no título
da região de imagem. Sem imagem, sem data; em indisponível/erro, exibir se
válido. Texto acessível, wrap natural, sem clipping/overflow; sem card, campo,
resize do drawer, reorder ou nova área scroll. Não há blocker estrutural
evidente; risco de altura baixa fica contido ao frame de imagem existente.

Validação futura: runtime visual nos viewports 2048×741, 2048×914, 1920×1080,
1366×768, 900×768 e 390×844, todos os conteúdos/footer acessíveis, sem nova
rolagem interna ou overflow, além de cenários funcionais, de segurança,
integridade, frontend status handling, acessibilidade/responsividade da seção
5. Se não couber sem mudar composição aprovada, `STOP_AND_ESCALATE` ao usuário.
`VISUAL_QA_PASS=NOT_RUN`; esta revisão não implementou nem validou endpoint,
código, testes ou runtime. Os três gaps estão `CLOSED_BY_CONTRACT`, mas a
implementação segue `PENDING_IMPLEMENTATION_VALIDATION`.

#### Revalidação stale depois do I/O

Validação canônica inicial ocorre antes de storage/bytes. Após load/hash/
decode/re-encode e imediatamente antes de qualquer resposta 200, fazer uma
segunda leitura canônica fresca de `LATEST_ACTIVE_IMAGE` (§26). Mudança de
câmera, UUID, corrente ou lifecycle invalida a resposta: descartar bytes em
memória e retornar 409 `STALE_SELECTION`, body vazio, `no-store`/`nosniff`, sem
fallback/retry. Esta checagem é o ponto de linearização; alterações posteriores
não são garantidas. Não segurar lock ou snapshot transacional durante I/O.
Se I/O falhar, revalidar antes de 422/503 e dar precedência a 409 caso stale.

Critérios futuros de concorrência: fake storage com barrier após load/decode;
inserir registro mais recente ou retirar o selecionado enquanto pausado e, ao
retomar, exigir 409 sem bytes; controle sem mudança retorna 200. Cobrir IDs/
câmeras cruzados e requests paralelos. Revalidar ambas as leituras pela regra
§26; não há fallback/retry.

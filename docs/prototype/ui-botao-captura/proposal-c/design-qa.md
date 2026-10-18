# Design QA — Proposta C de elegibilidade E3

```text
SOURCE = ARGOS_E3_CAPTURE_ELIGIBILITY_STATES_PROPOSAL_V1.html
TARGET = user-approved Variante B + additive contextual states C
QA_TYPE = STATIC_SOURCE_REVIEW
FINAL_RESULT = BLOCKED
BLOCKER = browser policy rejected opening the local file URL; Edge was absent from current browser inventory
SCREENSHOTS = NONE
VIEWPORTS_RENDERED = NONE
KEYBOARD_INTERACTION = NOT_RUN
SCREEN_READER = NOT_RUN
HUMAN_VISUAL_APPROVAL = PENDING
```

## Evidência disponível

- Inspecionada nesta atividade a captura de referência existente `../evidence/ARGOS_E3_V1_ALTERNATIVA_B.png`: duas zonas compactas, upload à esquerda, captura à direita e divisor neutro. Essa imagem é referência aprovada, não screenshot novo nem evidência de renderização da proposta.
- Inspecionados o contrato visual aprovado, o protótipo original V1 e o contrato técnico de elegibilidade DRAFT.
- A tentativa de abrir o HTML local pelo navegador integrado foi recusada porque somente URLs HTTP/HTTPS são aceitas na sessão. Nenhum servidor, outro navegador ou caminho alternativo foi usado para contornar essa barreira.

## Revisão estática do protótipo

| Verificação | Resultado estático | Limite |
|---|---|---|
| Integridade da referência V1 | SHA-256 do HTML original coincide com `SHA256SUMS.txt`; o arquivo de baseline permanece intacto. | Não valida a renderização do novo protótipo. |
| JavaScript inline | `node --check` passou. | Não executa o DOM nem os eventos no browser. |
| IDs HTML | Nenhuma duplicação encontrada. | Não é validação de acessibilidade completa. |
| Chamadas externas/operacionais | Nenhum fetch, XHR, endpoint, URL de câmera ou endereço IP encontrado no protótipo. | Não valida autorização do produto; o artefato é local e sem backend. |
| Cenários presentes | 01, 02, 03, 04a, 04b, 05, 06, 07a, 07b e 08 constam no seletor e no mapeamento JS. | Não confirma comportamento no browser. |
| Baseline B | Referência original é exibida separadamente do estado C; `Ver imagens` é rotulada como conceito E4 e não foi adicionada à proposta E3. | A imagem de comparação não foi renderizada pelo novo HTML nesta sessão. |
| Controles inertes indisponíveis | O botão de captura é ocultado nos estados temporário, incompleto, não suportado, desconhecido, genérico, running e sem permissão; aparece em available e failed, condicionado no texto à possibilidade de nova intenção. | Validação de DOM computado/teclado pendente. |
| Operação única | Classes dedicadas retiram divisor e padding quando só captura ou só upload aparece. | Layout/overflow em tela precisa de captura renderizada. |
| Acessibilidade do markup | Seletor nativo com label, modos com `aria-pressed`, botão nomeado, foco visível e status com `role=status`/`aria-live`. | Navegação real por teclado, leitura por screen reader e contraste renderizado não testados. |
| Contraste calculado das cores declaradas | `#5e7891` sobre branco = 4.59:1; `#70480e` sobre `#fff6e7` = 7.47:1; branco sobre `#2464a6` = 6.09:1. | Cálculo sobre valores CSS, não medição de pixels da renderização. |
| Segurança | Sem integração de rede, credenciais, destinos, upload ou backend no arquivo. | Não valida autorização de produção. |
| Viewports 2048×742, 1440×900, 1366×768, 390×844 | Regras responsivas correspondentes estão definidas no CSS. | Nenhuma dimensão foi renderizada ou comparada nesta sessão. |

## Finding e próximo gate

O artefato está pronto para inspeção estática e revisão de conteúdo, mas a proposta não pode receber `PASS` visual/responsivo sem abrir e capturar o HTML nos quatro tamanhos. O bloqueio veio da política do navegador ao receber `file://`; requer uma superfície de navegador autorizada para essa origem local ou screenshots obtidas pelo usuário.

O parecer independente do papel `SENIOR_UI_UX_FRONTEND_CONSULTANT` também não foi produzido, pois esse papel não aparece no catálogo disponível nesta sessão. A revisão atual é preliminar e não substitui essa avaliação especializada.

`NEXT_GATE = USER_VISUAL_AMENDMENT_REVIEW` — revisar a proposta e providenciar o navegador autorizado/screenshot para validação renderizada. Implementação Django continua proibida até autorização futura.

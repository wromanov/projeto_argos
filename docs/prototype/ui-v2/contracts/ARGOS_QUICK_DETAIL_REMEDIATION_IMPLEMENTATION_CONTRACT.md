# ARGOS — Quick Detail Remediation Implementation Contract

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E2
ACTIVITY = ARGOS-QD-REMEDIATION-CONTRACT
STATUS = RATIFIED / QD01_BOUNDED
REMEDIATION_CONTRACT_STATUS = RATIFIED
HUMAN_RATIFICATION = YES / ROOT-ADJUDICATED USER AUTHORIZATION
IMPLEMENTATION_AUTHORIZATION = GRANTED_WITHIN_RATIFIED_SCOPE
QD01 = RATIFIED
QD02 = ACCEPTED_BASELINE
QD03 = OPTION_B_APPROVED
QD03_SPECIFICATION_GAP = OPEN
COMMIT = NOT_AUTHORIZED
PUSH = NOT_AUTHORIZED
DEPLOY = NOT_AUTHORIZED
```

Este documento registra a remediação delimitada de QD01, ratificada conforme a
decisão humana adjudicada pelo ROOT. A autorização de implementação vale apenas
para o escopo ratificado abaixo. Ele não altera nem substitui o contrato IMG-07
ou a baseline visual protegida. QD02 permanece baseline aceita; QD03-B é decisão
separada e não fecha a divergência de especificação §7.3.

## 1. Objetivo e escopo ratificados

Corrigir o scroll do documento que continua alcançável por trás do Quick Detail
modal, preservando a rolagem interna já existente no corpo do drawer, a posição
anterior da página, o comportamento de foco e toda a baseline funcional e visual
ratificada do IMG-07.

Este contrato cobre somente o scroll lock do Quick Detail e os testes diretamente
necessários para demonstrá-lo. A única mudança visual esperada é nenhuma mudança
de composição; qualquer deslocamento perceptível causado por scrollbar ou por
estilos de rolagem deve ser evitado ou registrado para avaliação.

## 2. Autoridades e precedência

- [`ARGOS_UI_V2_VISUAL_CONTRACT.md`](ARGOS_UI_V2_VISUAL_CONTRACT.md) mantém o
  Quick Detail `APPROVED / PROTECTED` e o redesign não autorizado.
- [`ARGOS_IMG_07_UI_UX_CONFORMANCE_HANDOFF.md`](../ARGOS_IMG_07_UI_UX_CONFORMANCE_HANDOFF.md)
  determina a preservação de composição, layout, ações, contexto, navegação e
  foco, e registra a validação futura de acessibilidade e responsividade.
- [`ARGOS_IMG_07_IMPLEMENTATION_CONTRACT.md`](../../../projeto/contracts/backend/images/ARGOS_IMG_07_IMPLEMENTATION_CONTRACT.md)
  continua sendo o contrato ratificado de comportamento de imagem. Este contrato
  não reabre nem altera suas decisões.
- [`ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`](../../../projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md)
  §7.3 lista Terminal, Pavimento, Setor, Ambiente e Ponto de referência na
  localização do Quick Detail.
- [`PROJECT_STATE.md`](../../../Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md)
  §§19 e 27 e [`AGENT_CONTINUITY.md`](../../../Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md)
  §17 registram a baseline
  visual aceita com três cards de largura integral e quatro campos por card,
  incluindo Ambiente. A referência visual aprovada do Quick Detail está
  registrada como ausente em
  [`README.md`](../evidence/hom-01-visual-qa-2026-10-11/README.md) §3.

Quando houver conflito entre conteúdo funcional e composição visual protegida,
este contrato não escolhe silenciosamente uma interpretação. O escopo ratificado
preserva a renderização atual e deixa a divergência de localização para decisão
visual humana separada.

## 3. Findings e evidências adjudicadas

### QD01 — Documento rola sob o dialog modal

Em 390×844, com o dialog modal aberto e foco no botão de fechar, PageDown moveu
`documentTop` de 143 para 190. O dialog permaneceu aberto. Portanto, a rolagem do
documento de fundo não está bloqueada.

### QD02 — Região interna controlada existente

Em 390×844, o corpo do drawer tem uma única região interna de rolagem observada,
com alcance de 23 px. O wheel moveu essa região de 0 para 23 px sem mudar a
posição do documento (`documentTop=143`). A baseline aceita anteriormente
continha essa rolagem interna (§27 de `PROJECT_STATE.md`). Ela deve permanecer
como a única região interna controlada do drawer; não se exige alcance zero,
clip de conteúdo nem redesign.

### QD03 — Autoridade conflitante sobre localização

A especificação funcional §7.3 lista cinco campos, incluindo Ponto de
referência. A baseline aceita e o teste visual registrado preservam quatro
campos, incluindo Ambiente; o template não tem slot para `ponto_referencia`,
embora a projeção de dados exista. A captura aprovada de referência está
ausente. O registro vigente classifica a conformidade integral de localização
como `FAIL` e requer decisão visual separada.

**Decisão humana registrada:**

- **A — Propor inclusão (não selecionada):** autorizar uma proposta visual separada de UI V2 e sua
  revisão para adicionar `Ponto de referência` à composição protegida do Quick
  Detail. Esta opção autoriza somente preparar e revisar a proposta; não
  autoriza implementar a mudança de campo ou layout.
- **B — Manter a composição aceita (aprovada):** manter a composição atual de quatro campos
  e encaminhar a divergência com §7.3 para esclarecimento formal de autoridade.
  Esta opção não declara que a especificação funcional foi alterada nem resolve
  a divergência por inferência.

QD03-B foi aprovada como decisão separada: manter a composição aceita de quatro
campos e encaminhar a divergência com §7.3 para esclarecimento formal. Isso não
altera nenhum campo, template, dado ou contrato de IMG-07. Ambiente permanece
visível. `QD03_SPECIFICATION_GAP=OPEN` até esclarecimento formal de autoridade.

### QD04 — Estado de acessibilidade

O contraste da mensagem genérica de erro foi medido em 7.5619:1 (`PASS`) e o do
timestamp em 4.5063:1 (`PASS`). O teste anterior de teclado registrou Tab,
Shift+Tab, foco visível, Escape e retorno do foco ao acionador como `PASS`; o
PageDown desta revisão revelou o finding QD01. Zoom e leitor de tela estão
`NOT_RUN`. O handoff §5 requer verificação por leitor de tela; não há critério
explícito de porcentagem de zoom registrado no contrato IMG-07 ou no handoff.
Essas ausências não podem ser declaradas `PASS`.

As quatro capturas persistidas da revisão são `DOM MOCK`; elas não provam
transporte HTTP. O teste integrado Django anterior confirmou separadamente
HTTP 409 `STALE_SELECTION` com corpo vazio. A verificação de contraste atual
leu CSS computado no Edge. Evidências e contextos não devem ser tratados como
intercambiáveis.

## 4. Solução técnica ratificada

1. Enquanto o Quick Detail estiver aberto como dialog modal, impedir que a
   rolagem do documento de fundo avance ou recue por teclado, roda do mouse ou
   gesto de toque.
2. Manter rolável o corpo interno existente do drawer quando seu conteúdo
   exceder a área disponível. Conteúdo e footer devem continuar acessíveis.
3. Ao fechar, restaurar a posição de rolagem e o comportamento/estilos
   preexistentes do documento em todos os caminhos de fechamento cobertos pelo
   componente.
4. A implementação deve respeitar um estado de scroll lock que já existia
   antes de abrir o Quick Detail e não interferir em outros dialogs. O
   mecanismo deve atuar sobre o elemento que efetivamente rola o documento.
   Não usar bloqueio global de eventos `wheel`/`touch`.
5. Preservar o contraste medido: erro 7.5619:1 com `--color-danger` e timestamp
   4.5063:1 com `--color-text-muted`. Não mudar os tokens ou a aparência aprovada
   como parte do lock, salvo necessidade demonstrada e nova adjudicação.
6. Nenhum retry automático deve ser introduzido. O comportamento de JSON,
   preview HTTP, seleção IMG-07 e mensagem de erro permanece inalterado.

A escolha local do mecanismo de implementação permanece para o implementador,
dentro destas restrições e do escopo ratificado. Se o estado real do DOM ou
um dialog coexistente impedir cumprir as condições sem alteração estrutural ou
visual, interromper essa parte e retornar para decisão; não ampliar o escopo.

## 5. Invariantes protegidos

- Preservar integralmente os contratos ratificados e os comportamentos
  funcionais de IMG-07: seleção, identidade, proveniência, `recorded_at`, estado
  da imagem, preview e stale 409.
- Preservar composição, hierarquia, densidade, sequência de seções, ações,
  foco, navegação e contexto do Inventário do Quick Detail.
- Preservar Ambiente e os quatro campos atualmente renderizados. Não incluir,
  remover, renomear nem reordenar campos de localização neste escopo.
- Preservar a região interna única do drawer e o footer visível. Não criar outra
  área de rolagem, não forçar alcance interno zero, não cortar conteúdo e não
  redesenhar o painel.
- Não alterar backend/API, envelope JSON, preview HTTP, autenticação,
  autorização, seleção de IMG-07, contratos, schema, migration, banco, fixtures,
  imagens, outras câmeras, Inventário, `LATEST_CAMERA_CAPTURE`, captura técnica,
  monitoramento ou histórico.
- Não alterar credenciais, WIP ou evidências existentes.
- Não declarar teste como `PASS` sem execução e evidência observável. Manter
  zoom e screen reader como `NOT_RUN` até que sejam realmente avaliados.

## 6. Arquivos autorizados para implementação QD01

Escopo de escrita autorizado somente para a implementação QD01:

- `static/js/camera-quick-detail.js` — ciclo abrir/fechar, gerenciamento do
  scroll lock e restauração de estado.
- `static/css/inventario.css` — somente se uma regra CSS estritamente necessária
  ao scroll lock for demonstrada; preservar o token e contraste de erro/timestamp.
- Teste(s) direcionado(s) existente(s) do Quick Detail para o comportamento do
  scroll lock e restauração. O implementador selecionará o arquivo de teste
  existente mais adequado. Não alterar template ou testes de localização.

Qualquer arquivo adicional ou necessidade de mudança fora dessa lista exige
interrupção e autorização de escopo separada. Não criar migration ou fixture.

## 7. Matriz obrigatória de validação

Executar nos viewports CSS `390×844`, `1366×768`, `1440×900` e `1920×1080`.

| Caso | Resultado exigido |
|---|---|
| Dialog aberto; documento previamente rolado | PageDown, PageUp, wheel e gesto de toque não movem o documento de fundo. |
| Drawer com conteúdo acima da área visível | O corpo interno continua rolável quando necessário; conteúdo e footer são alcançáveis. |
| Fechar pelo botão, Escape e backdrop, quando suportado | Posição original e estado de rolagem do documento são restaurados; foco volta conforme comportamento aprovado. |
| Abertura/fechamento repetido | Não acumula locks nem altera progressivamente estilos ou posição da página. |
| Navegação entre câmeras, carregamento e estado de erro | Lock e liberação permanecem corretos, sem alterar os resultados funcionais IMG-07. |
| Estado de rolagem preexistente | Um lock que já existia antes da abertura é preservado e continua pertencendo ao seu proprietário. |
| Dialogs coexistentes | O fechamento do Quick Detail não libera nem modifica o estado de outro dialog. |
| Layout e clipping | Sem overflow horizontal, corte de conteúdo, ocultação do footer ou deslocamento visual inesperado. |
| Teclado e foco | Tab/Shift+Tab, foco visível, Escape, retorno do foco e ordem de navegação continuam conformes. |
| Regressão funcional | Preservar seleção/imagem, identidade, proveniência, timestamp, mensagem genérica e stale 409 sem retry; preservar Inventário e captura técnica. |
| Contraste | Reconfirmar error ≥ 4.5:1 e timestamp ≥ 4.5:1 com cores/fundos computados. Valores de referência anteriores: 7.5619:1 e 4.5063:1. |
| Zoom e leitor de tela | Executar e registrar configuração, tecnologia/versão quando aplicável, passos e resultado. Não declarar `PASS` sem evidência. |

Os casos de regressão devem ser proporcionais aos arquivos efetivamente
alterados. Se o comportamento requerido falhar em algum viewport ou coexistir
com mudança estrutural, registrar o achado e interromper a expansão do escopo.

## 8. Critérios de aceite

O finding de scroll lock só poderá ser marcado `PASS` quando evidências
reproduzíveis demonstrarem que:

1. o documento de fundo não se move enquanto o dialog está aberto nos quatro
   viewports e pelos modos de entrada especificados;
2. a região interna única do drawer continua utilizável e footer/conteúdo
   permanecem alcançáveis;
3. cada caminho de fechamento validado restaura posição, estado de rolagem e
   foco; aberturas repetidas e coexistência não deixam estado residual;
4. não houve regressão nas invariantes funcionais, visuais e de acessibilidade;
5. testes efetivamente executados, screenshots sanitizados, viewport,
   data/hora, modo de entrada e resultado estão registrados.

Este aceite técnico não resolve QD03 nem, isoladamente, fecha IMG-07, E2 ou
qualquer gate de aceitação final. Acessibilidade permanece `PARTIAL` até os
itens obrigatórios aplicáveis serem executados; em particular, a verificação de
leitor de tela pendente não pode ser inferida a partir de teclado ou de árvore
de acessibilidade.

## 9. Ratificação e gate de implementação

Antes da implementação, a autoridade humana deve registrar os seguintes campos
com o contrato revisado:

```text
REMEDIATION_CONTRACT_STATUS = RATIFIED
HUMAN_RATIFICATION = YES / ROOT-ADJUDICATED USER AUTHORIZATION
SCOPE_ACKNOWLEDGED = YES
RATIFIED_SCOPE = QD01_SCROLL_LOCK_ONLY; preserve QD02; QD03-B separately approved; specification gap remains open
```

A decisão QD03-B é separada da ratificação QD01 e não autoriza proposta ou
alteração de composição. `Ponto de referência` permanece fora desta
implementação; a divergência §7.3 segue aberta para esclarecimento formal.

Implementação está autorizada somente nos arquivos listados na seção 6 e para
QD01, observadas as invariantes e validação deste contrato. Zoom e leitor de
tela mantêm seus status reais; nenhum PASS é inferido. O resultado será revisado
e validado antes de qualquer decisão de prontidão. Commit, push, merge e deploy
permanecem não autorizados.

## 10. Rollback, limitações e publicação

Se a correção alterar composição, foco, navegação, conteúdo, estado de dialogs
coexistentes ou qualquer invariante, reverter somente a alteração nova e
autorizada por meio do fluxo de revisão aprovado, preservando WIP preexistente.
Não usar reset, restore, clean ou stash automáticos. Em caso de dúvida sobre
propriedade de mudanças preexistentes, não reverter; interromper e escalar.

Este contrato ratifica exclusivamente QD01; não autoriza commit, push, merge,
publicação, deployment, encerramento de E2 ou início de E3. O escopo de
implementação é QD01, preservando QD02; QD03-B está aprovada separadamente e
`QD03_SPECIFICATION_GAP=OPEN`. Zoom e leitor de tela continuam `NOT_RUN` até
avaliação real.

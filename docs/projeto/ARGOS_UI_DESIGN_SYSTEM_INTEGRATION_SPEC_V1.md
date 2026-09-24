# ARGOS — Especificação Canônica de Integração Seletiva do Design System

```text
STATUS = CANONICAL
DOCUMENT_TYPE = PROJECT_UI_DESIGN_SYSTEM_INTEGRATION_SPEC
VERSION = V1
LANGUAGE = pt-BR
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
REFERENCE_PACKAGE_MANIFEST_VERSION = 1.0.1
REFERENCE_PACKAGE_STATUS = VISUAL_BASELINE_APPROVED
REFERENCE_PACKAGE_REPOSITORY_SHA256 = 510D75399A5C2F641DB77EF1AF9C982B8A2B3D9C08B06854073CE16FE028DA14
STRATEGY = SELECTIVE VISUAL RETROFIT + SELECTIVE INTERACTION PATTERN ADOPTION
FULL_UI_REDESIGN = NO
FULL_DESIGN_SYSTEM_MIGRATION = NO
APP_SHELL_REPLACEMENT = NO
FRAMEWORK_MIGRATION = NO
DO_NOT_MIGRATE_FRAMEWORKS = YES
```

Este documento é a authority detalhada para a integração visual seletiva do
Camera Inventory Design System v1.0.1 no ARGOS, para o
`CameraQuickDetailPanel`, para as regras de interação associadas, para a
relação com a Fase C e para a integração incremental entre slices.

Ele é autossuficiente quanto às decisões de produto e engenharia registradas
aqui. O pacote de referência foi localizado externamente no caminho acima e
inspecionado sem ser extraído para o repositório. A ausência de uma cópia
repositória não autoriza inventar valores visuais adicionais nem alterar os
contratos abaixo.

O `package-manifest.json` confirma a identidade `camera-inventory-design-system`
na versão `1.0.1`, com status `VISUAL_BASELINE_APPROVED`. O título interno de
`DESIGN_SYSTEM_SPEC.md` no ZIP recebido usava `v1.0`. Na cópia canônica
incorporada ao repositório, o título foi alinhado para `v1.0.1`; o ZIP original
em `Downloads` foi preservado sem alteração. A identidade adotada continua
sendo `camera-inventory-design-system-v1.0.1`.

## 1. Finalidade, escopo e autoridade

O ARGOS deve continuar reconhecível como ARGOS, preservando sua estrutura,
arquitetura da informação, densidade operacional e fluxos, mas adotando uma
linguagem visual corporativa, moderna e sistematizada quando isso for compatível
com a stack e com os contratos existentes.

Esta é uma atividade documental de especificação. A existência desta
specification não autoriza implementação, mudança de CSS, instalação de
dependências, alteração de framework, avanço de fase ou alteração de lógica de
domínio. A autorização futura deverá ser explícita e independente.

### 1.1 Authorities

```text
ARGOS_CURRENT_FUNCTIONAL_CONTRACT = FUNCTIONAL_AUTHORITY
ARGOS_CURRENT_INFORMATION_ARCHITECTURE = STRUCTURAL_AUTHORITY
CAMERA_INVENTORY_DESIGN_SYSTEM_V1_0_1 = VISUAL_LANGUAGE_AUTHORITY
DESIGN_SYSTEM_SEMANTIC_TOKENS = VISUAL_TOKEN_AUTHORITY
EXPLICITLY_APPROVED_PATTERNS = INTERACTION_PATTERN_AUTHORITY
```

Precedência:

```text
STRUCTURAL QUESTION
→ ARGOS

FUNCTIONAL QUESTION
→ ARGOS DOMAIN CONTRACTS

VISUAL QUESTION
→ DESIGN SYSTEM

NEW INTERACTION
→ SOMENTE PADRÕES EXPLICITAMENTE APROVADOS
```

Em qualquer conflito:

```text
IDENTIFY → CLASSIFY → REPORT → PROPOSE
```

Conflitos não podem ser resolvidos silenciosamente. Design system, skill,
plugin, protótipo ou preferência visual não transferem authority nem substituem
contrato do ARGOS.

### 1.2 Princípios não negociáveis

```text
ARGOS OWNS STRUCTURE.
DESIGN SYSTEM OWNS VISUAL LANGUAGE.
NEW INTERACTION PATTERNS ARE ADOPTED SELECTIVELY.
```

Esses princípios devem permanecer explícitos em revisões, handoffs e prompts de
execução. O pacote de referência é uma fonte de linguagem visual e de padrões
aprovados, não um produto a ser copiado integralmente.

## 2. Classificação oficial da estratégia

```text
STRATEGY =
SELECTIVE VISUAL RETROFIT
+ SELECTIVE INTERACTION PATTERN ADOPTION
```

Não é:

```text
FULL_UI_REDESIGN = PROHIBITED
FULL_DESIGN_SYSTEM_MIGRATION = PROHIBITED
APP_SHELL_REPLACEMENT = PROHIBITED
FRAMEWORK_MIGRATION = PROHIBITED
```

Resultado esperado: modernizar a linguagem visual e adotar apenas os padrões de
interação aprovados, sem copiar o protótipo como produto, sem substituir a
composição atual das páginas e sem alterar o domínio para servir à aparência.

## 3. Stack: referência visual não é autorização técnica

A stack apresentada pelo pacote de referência é:

```text
React
TypeScript
Tailwind CSS
shadcn/ui
Lucide
TanStack Table
```

Essa stack é somente referência. Ela não autoriza alteração da stack factual do
ARGOS. A arquitetura documentada do ARGOS permanece uma aplicação Django
modular com Django Templates, CSS próprio, views/forms, serviços de domínio e
models Django; a arquitetura atual também registra que Bootstrap e Tailwind não
são utilizados.

```text
DO_NOT_MIGRATE_FRAMEWORKS = YES
```

Contratos visuais e interacionais devem ser traduzidos para a stack real do
ARGOS. Não introduzir React, TypeScript, Tailwind, shadcn/ui, TanStack Table,
Lucide ou dependência equivalente apenas porque aparecem no pacote.

Authorities factuais relacionadas:

- `docs/projeto/03_arquitetura.md` — stack e arquitetura atual;
- `docs/projeto/08_principios.md` — princípios de operação antes de decoração,
  cor com significado e ausência de framework visual por impulso;
- `docs/projeto/ADR-019_monitoramento_disponibilidade_gestao_imagens.md` —
  direção de monitoramento e gestão de imagens;
- `docs/projeto/ROADMAP_ARGOS_V5.md` — macrofases e slices vigentes.

### 4.3 Direção visual confirmada no pacote

O pacote classifica a direção aprovada como `Corporate Tech / Infrastructure`:
calma, densa o bastante para operação diária e imediatamente legível. A
referência visual usa sidebar petrol-blue, canvas blue-gray, primary azul
corporativo, acento teal, Inter e iconografia Lucide. Isso não substitui a
composição do ARGOS nem autoriza impor dimensões do `AppShell` do pacote.

O pacote proíbe, como linguagem visual:

- preto ou branco puros como paleta dominante;
- gradientes decorativos, neon, cyberpunk ou gamer;
- sombras fortes e excesso de cantos arredondados;
- controles superdimensionados que reduzam a densidade da tabela;
- vermelho, verde, âmbar ou roxo como decoração não semântica;
- cores ou tipografia one-off por página.

O pacote também define os composites `CameraStatusBadge`, `CameraTable`,
`CameraHealthCard`, `InventoryFilters`, `CameraDetailSheet`, `NetworkInfo`,
`VmsStatus`, `LocationBreadcrumb` e `InventoryKpiCard`. No ARGOS, eles são
contratos de referência para mapeamento visual e semântico, não autorização
para copiar componentes React/TypeScript ou substituir componentes existentes.

Componentes de domínio devem permanecer presentacionais: não devem possuir
data fetching nem routing próprios. Estados `default`, `hover`,
`focus-visible`, `pressed`, `disabled`, `loading`, `empty`, `error` e
`responsive` devem ser definidos quando aplicáveis; componentes densos também
devem tratar `selected`, `sorted`, `filtered` e `stale`.

## 4. Linguagem visual a aproveitar

A intenção é adotar e adaptar, quando compatível com a composição e com os
tokens atuais do ARGOS:

- semantic tokens;
- background e superfícies;
- cards;
- borders;
- radius;
- shadows;
- botões;
- inputs;
- focus states;
- hover states;
- selected states;
- status visual;
- tipografia;
- iconografia.

Compatibilidade significa preservar a densidade operacional, a legibilidade,
os nomes semânticos e o comportamento acessível do ARGOS. Uma propriedade
visual do pacote não deve ser aplicada apenas porque existe no pacote.

### 4.1 Tokens semânticos de referência

Os seguintes valores fazem parte do contrato documental desta integração e
devem ser preservados como referência de linguagem visual:

| Token | Valor de referência | Uso semântico |
|---|---|---|
| `background` | `#F4F7FA` | fundo geral |
| `foreground` | `#172B3A` | texto principal |
| `surface` | `#FAFCFE` | superfície de conteúdo |
| `surface-elevated` | `#FFFFFF` | superfície elevada, painel ou card destacado |
| `primary` | `#2563A6` | ação e ênfase institucional |
| `primary-hover` | `#1D4F86` | estado hover da ação primária |
| `primary-foreground` | `#FFFFFF` | conteúdo sobre ação primária |
| `secondary` | `#E8F2FA` | ação/superfície secundária |
| `secondary-foreground` | `#1D4F86` | conteúdo sobre superfície secundária |
| `accent` | `#DFF3F2` | acento contextual aprovado |
| `accent-foreground` | `#0F6F71` | conteúdo sobre acento |
| `muted` | `#EAF0F4` | estado neutro, fundo sutil ou informação secundária |
| `muted-foreground` | `#607485` | texto secundário |
| `border` | `#D8E2EA` | separadores e contornos |
| `input` | `#D8E2EA` | borda de input |
| `ring` | `#2563A6` | foco visível |

Tokens operacionais confirmados no pacote:

| Família | Valores de referência |
|---|---|
| `sidebar` | `#123047` |
| `sidebar-foreground` | `#EAF3F8` |
| `sidebar-muted` | `#AFC3D1` |
| `sidebar-hover` | `#1A405B` |
| `sidebar-active` | `#2563A6` |
| `sidebar-border` | `#27485F` |
| `font-sans` | `Inter, ui-sans-serif, system-ui, sans-serif` |
| `space` | `1=4px`, `2=8px`, `3=12px`, `4=16px`, `5=20px`, `6=24px`, `8=32px`, `10=40px`, `12=48px` |
| `radius` | `sm=6px`, `md=8px`, `lg=10px`, `xl=12px`, `pill=999px` |
| `shadow-card` | `0 1px 2px rgba(18,48,71,.04)` |
| `shadow-elevated` | `0 4px 14px rgba(18,48,71,.08)` |
| `shadow-sheet` | `0 8px 30px rgba(18,48,71,.12)` |

Valores tipográficos e de layout confirmados como baseline do pacote:

- título de página: `28px/700`;
- título de seção: `20px/600`;
- valor de métrica: `28–32px/700`;
- corpo: `14px/400`;
- label: `14px/500`;
- cabeçalho de tabela: `12–13px/600`;
- caption: `12px/400`;
- tabela: linhas de `52–56px`;
- page padding: `24px` desktop e `16px` mobile;
- cards: `16–20px` de padding interno;
- botões/inputs: radius de `8px`;
- badges de status: formato pill.

O pacote também confirma a seguinte paleta operacional:

| Status de referência | Foreground | Soft background | Semântica do pacote |
|---|---|---|---|
| `online` | `#16A36A` | `#DDF5EA` | alcançável e saudável |
| `warning` | `#E59B22` | `#FFF1D6` | degradado, stale ou atenção |
| `offline` | `#D64545` | `#FCE3E3` | inalcançável ou falho |
| `maintenance` | `#7C5CC4` | `#EEE8FB` | em manutenção intencional |
| `disabled` | `#81909C` | `#E8EDF0` | desabilitada administrativamente |
| `info` | `#3B82C4` | `#E3F0FA` | estado informativo |

Esses nomes/cores são referência visual e não alteram a semântica de estados do
ARGOS. O mapeamento precisa ser feito a partir do domínio do ARGOS, não a partir
da disponibilidade de uma cor.

Os valores acima estão confirmados no ZIP. Para qualquer valor que não esteja
confirmado nos arquivos do ZIP:

```text
DO_NOT_INVENT_VISUAL_VALUES_WHEN_TOKEN_EXISTS = YES
TOKEN_MAPPING_REQUIRED = YES
PACKAGE_VALUE_NOT_VERIFIED = DO_NOT_INFER
```

### 4.2 Tokens operacionais

Tokens operacionais não são decoração livre. Devem possuir uso e semântica
definidos antes de serem aplicados:

| Família | Deve governar | Limite |
|---|---|---|
| `focus` | `focus-visible`, ring e contraste | não depender de hover ou cor isolada |
| `hover` | feedback de ponteiro/teclado quando aplicável | não alterar significado do domínio |
| `selected` | linha/câmera atualmente selecionada | não confundir com status operacional |
| `status` | mapeamento de estado já produzido pelo domínio | nunca inventar estado a partir de uma cor |
| `surface/elevation` | separação de contexto e painel | não reorganizar a página para criar elevation |
| `radius/shadow` | hierarquia visual | não aumentar espaços ou ornamentos incompatíveis com operação |
| `typography` | hierarquia e leitura técnica | preservar valores técnicos e densidade |
| `motion` | abertura, troca e fechamento de superfícies | respeitar `prefers-reduced-motion` |

As cores operacionais não podem ser utilizadas como decoração. Se um token já
existir na camada do ARGOS, ele deve ser mapeado/adaptado, não duplicado com um
segundo valor semântico concorrente.

## 5. Semântica de status

Regra obrigatória:

```text
DOMAIN STATE
→ ARGOS SEMANTICS
→ VISUAL TOKEN MAPPING
```

Nunca:

```text
AVAILABLE COLOR
→ INVENT NEW MEANING
```

Status não pode depender apenas de cor. Quando aplicável, utilizar:

```text
ICON + LABEL + COLOR
```

Os estados visuais do Design System não podem criar, eliminar ou alterar
estados de domínio do ARGOS. A distinção entre situação operacional, status
técnico, conectividade e freshness continua pertencendo aos contratos do
ARGOS. `STALE` é qualificador de atualidade quando aplicável, não autorização
para apresentar dado antigo como corrente.

O pacote fornece um mapa tipado de referência com os estados visuais
`online`, `warning`, `offline`, `maintenance`, `disabled` e `info`, cada qual
com label, token de foreground, token de background e ícone (`CheckCircle2`,
`AlertTriangle`, `XCircle`, `Wrench`, `CircleOff` e `Info`). Esse mapa não cria
novos estados no ARGOS: a implementação futura deve adaptar os estados de
domínio existentes e preservar label, ícone e cor como sinais complementares.

## 6. Composição da página e camada de adaptação

```text
ARGOS CURRENT PAGE COMPOSITION = PRESERVE
DESIGN SYSTEM VISUAL STYLE = ADAPT
```

Não:

- substituir layout existente;
- reorganizar caixas apenas para parecer com o protótipo;
- criar nova sidebar porque o pacote possui sidebar;
- substituir tabela funcional apenas para usar TanStack Table;
- mudar navegação global;
- aumentar espaços de forma incompatível com a densidade operacional;
- copiar a estrutura de uma tela de demonstração como nova arquitetura do ARGOS.

### 6.1 Adapter layer preferencial

```text
DESIGN SYSTEM TOKEN
↓
ARGOS TOKEN / VARIABLE
↓
EXISTING COMPONENT
```

O adapter layer deve:

- evitar colisões de nomes e valores;
- evitar acoplamento direto ao pacote;
- permitir adoção progressiva;
- manter rollback simples;
- evitar dois design systems visualmente conflitantes.

O adapter layer não deve esconder divergência de contrato. Se o token ou
componente do ARGOS não puder representar o valor sem perda semântica, o
conflito deve ser reportado antes da implementação.

## 7. CameraQuickDetailPanel — decisão de produto

```text
SOURCE_PATTERN = CameraDetailSheet
ARGOS_PATTERN = CameraQuickDetailPanel
DECISION = ADOPT
ROLE = Quick contextual inspection
REPLACES_FULL_DETAILS = NO
CAN_NAVIGATE_TO_FULL_DETAILS = YES
PRESERVES_INVENTORY_CONTEXT = YES
```

O `CameraQuickDetailPanel` é uma inspeção contextual rápida aberta a partir do
inventário. Ele não é uma segunda página de detalhes, não duplica a página
canônica e não pode se tornar uma mini página completa.

O pacote confirma `CameraDetailSheet` como `Quick inspection surface` que agrupa
identidade, status, rede, VMS e localização e aponta para a página roteada de
edição/detalhes profundos. No ARGOS, esse padrão é traduzido para
`CameraQuickDetailPanel`; `CameraDetailSheet` não deve ser tratado como uma
segunda feature ou como uma nova rota.

### 7.1 Fluxo canônico

```text
INVENTÁRIO
↓
usuário ativa/clica em uma câmera
↓
CameraQuickDetailPanel abre lateralmente
↓
usuário permanece no contexto do inventário
↓
consulta resumo operacional
↓
fecha e continua
OU
↓
Ver detalhes
↓
página canônica completa da câmera
```

### 7.2 Contexto do inventário

Abrir, fechar ou trocar a câmera do painel não pode destruir:

- filtros;
- busca;
- sorting;
- paginação;
- scroll;
- seleção;
- query state;
- estado útil da tabela.

```text
CONTEXT_SHOULD_REMAIN_INTACT = YES
```

Se o estado estiver representado em URL/query string, ele deve ser preservado.
O painel deve ser uma superfície contextual sobre a listagem, e não um
redirecionamento que reconstrói o inventário.

### 7.3 Conteúdo mínimo futuro

#### HEADER

- identificação/nome;
- status;
- controle de fechar.

#### CAMERA PREVIEW

- imagem da câmera conforme o contrato de imagem da seção 8.

#### PRIMARY INFORMATION

- identificação;
- fabricante/modelo;
- localização;
- IP.

#### OPERATIONAL INFORMATION

- status técnico;
- conectividade;
- última comunicação/última atualização, quando disponível;
- VMS, quando aplicável;
- demais dados essenciais que estejam factual e semanticamente disponíveis.

#### SECONDARY METADATA

- somente o necessário para inspeção rápida.

#### PRIMARY ACTION

- `Ver detalhes`.

O painel deve mostrar resumo operacional útil, sem repetir integralmente a
página completa nem criar ações administrativas por consequência automática da
integração visual.

## 8. Contrato de imagem para inspeção rápida

### 8.1 Latest camera capture

Decisão de produto:

```text
PREFERRED_QUICK_PREVIEW = LATEST_CAMERA_CAPTURE
PROVENANCE_REQUIRED = CAPTURA_CAMERA
```

O painel deve exibir a imagem mais recente adequada à inspeção da câmera, com a
intenção de mostrar o último print tirado pela câmera/última imagem registrada
do equipamento. A recomendação de engenharia é priorizar a última imagem cuja
proveniência seja comprovadamente `CAPTURA_CAMERA`.

`UPLOAD_MANUAL` nunca pode parecer uma captura comprovadamente originada do
equipamento. A origem deve continuar disponível para a UI, para auditoria e
para adjudicação futura.

### 8.2 Fallback quando não houver captura

Esta recomendação deve ser preservada para a especificação funcional da Fase C:

```text
RECOMMENDED_BEHAVIOR =
1. não fingir que UPLOAD_MANUAL é captura;
2. apresentar estado explícito “sem captura disponível”;
3. se uma imagem manual for usada como fallback visual,
   rotulá-la explicitamente como UPLOAD_MANUAL;
4. fechar a decisão concreta de fallback na especificação funcional da Fase C.
```

Nenhuma decisão de fallback pode apagar a proveniência ou transformar ausência
de captura em falsa disponibilidade.

### 8.3 Imagem principal e latest capture

```text
PRIMARY_IMAGE != LATEST_CAMERA_CAPTURE
```

`PRIMARY_IMAGE` é a imagem escolhida/definida pela regra própria do produto.
`LATEST_CAMERA_CAPTURE` é a captura mais recente originada do equipamento. Elas
podem coincidir, mas não são semanticamente equivalentes. O painel prioriza o
contrato de `LATEST_CAMERA_CAPTURE` para quick inspection, sem redefinir a
semântica de `PRIMARY_IMAGE`.

### 8.4 Abrir o painel não captura imagem

```text
OPEN_QUICK_DETAIL_PANEL != CAPTURE_NEW_IMAGE
```

Ao abrir ou trocar o painel, consultar apenas dados e imagens já registrados.
Não criar exclusivamente para alimentar o painel:

- captura automática nova;
- chamada VMS nova;
- acesso direto novo à câmera;
- polling pesado novo.

O botão/fluxo explícito de captura pertence à Fase C. Monitoramento, captura e
inspeção rápida permanecem desacoplados.

### 8.5 Performance e concorrência

Prioridade:

```text
FAST_FIRST_RENDER
```

Fluxo recomendado:

```text
panel opens
↓
identity + status + primary metadata render
↓
image loads independently
↓
secondary data loads when needed
```

A imagem não deve bloquear a abertura básica do painel. Se o painel estiver
aberto para a câmera A e o usuário selecionar a câmera B, o mesmo shell deve
ser atualizado:

```text
Camera A → panel A
Camera B → panel B
```

Não exigir `open → close → open → close`.

Proteção obrigatória contra race condition:

```text
request Camera A
request Camera B
A_RESPONSE_MUST_NOT_OVERWRITE_B = YES
```

Associar cada resposta à câmera selecionada no momento ou cancelar requests
anteriores quando a stack permitir. O estado visual nunca deve apresentar
imagem, status ou metadados de outra câmera.

### 8.6 Estados do painel e da imagem

Prever explicitamente:

```text
LOADING
AVAILABLE
NO_CAPTURE_AVAILABLE
UNAVAILABLE
ERROR
STALE
```

`STALE DATA MUST NOT LOOK CURRENT`. Um ícone de imagem quebrada não é um estado
final aceitável; a UI deve explicar indisponibilidade, erro ou ausência de
captura com texto e semântica apropriados.

## 9. Acessibilidade e interação

Alvo:

```text
WCAG 2.2 AA = TARGET_WHEN_APPLICABLE
```

No mínimo:

- equivalente de teclado para ativação;
- `focus-visible`;
- accessible names;
- controles icon-only rotulados;
- status que não dependa apenas de cor;
- ordem lógica de foco;
- `Escape` fecha;
- focus trap quando adequado ao padrão escolhido;
- focus restore para o elemento acionador;
- `prefers-reduced-motion`;
- tabela semanticamente preservada.

O padrão final deve preservar a semântica da tabela e o acesso ao acionador
mesmo quando a interação do painel for adicionada progressivamente.

Critérios adicionais confirmados no pacote:

- texto e labels devem atingir contraste `4.5:1`; texto grande, `3:1`;
- targets de toque devem ter ao menos `44×44 CSS px`;
- row activation deve ter equivalente de teclado e não depender de `<div>` não
  semântico;
- sorting e selection devem anunciar direção/estado;
- filtros devem ter label/nome acessível, ação de limpar e quantidade de filtros
  ativos;
- mensagens de refresh não críticas usam `aria-live="polite"`, sem anúncios
  assertivos para polling rotineiro;
- tooltip é complementar, nunca o único nome de controle icon-only.

## 10. Relação obrigatória com a Fase C

```text
FASE C = Captura manual e gestão de imagens
```

A Fase C deve produzir contratos canônicos que permitam ao painel consultar:

- última `CAPTURA_CAMERA`;
- origem/proveniência;
- timestamp;
- storage/reference;
- disponibilidade;
- estado da imagem;
- thumbnail/preview, quando disponível.

O painel não pode criar mecanismo paralelo exclusivo para imagens. O mesmo
modelo, histórico e caminho canônico da Fase C devem alimentar a inspeção rápida
e as superfícies futuras de imagem.

### 10.1 Dependências IMG-01 a IMG-09

| Slice | Dependência com o painel |
|---|---|
| `IMG-01 — Contrato funcional` | fechar relação imagem/câmera, proveniência, autoria, timestamp, permissões, retenção e ciclo de vida; semântica de `CAPTURA_CAMERA` versus `UPLOAD_MANUAL` é pré-requisito. |
| `IMG-02 — Modelo, storage e proveniência` | fornecer modelo/storage capazes de responder a `LATEST_CAMERA_CAPTURE`, mantendo referência, disponibilidade e origem. |
| `IMG-03 — Upload manual` | manter `UPLOAD_MANUAL` semanticamente separado; nunca apresentar upload como captura comprovada. |
| `IMG-04 — Captura sob demanda` | captura real deve alimentar o mesmo modelo e histórico canônicos consultados pelo painel. |
| `IMG-05 — Processamento independente` | captura não bloqueia monitoramento nem a UI; abertura do painel não inicia captura. |
| `IMG-06 — Histórico visual` | fornecer ordenação e consulta necessárias para localizar a captura mais recente. |
| `IMG-07 — Imagem principal` | manter `PRIMARY_IMAGE` como conceito independente de `LATEST_CAMERA_CAPTURE`. |
| `IMG-08 — Segurança e auditoria` | preservar autoria, proveniência, permissão, integridade e eventual hash; o painel não contorna esse caminho. |
| `IMG-09 — Hardening` | cobrir erros, concorrência, storage, stale, estados de indisponibilidade e UX do painel. |

## 11. Integração incremental e vertical slices

### 11.1 Lição do Projeto ORION

No Projeto ORION, módulos foram implementados isoladamente e deixados para
integração posterior. O resultado foi acúmulo de dívida de integração, uma
sprint inteira apenas para integrar, alto custo, risco elevado e comportamento
emergente difícil de diagnosticar.

O ARGOS não deve repetir esse padrão.

### 11.2 ARGOS Incremental Integration Rule

Nenhuma capability produtiva pode ser considerada `DONE` quando estiver apenas
implementada ou testada isoladamente.

```text
IMPLEMENT
↓
INTEGRATE INTO CANONICAL FLOW
↓
VALIDATE INTEGRATED
↓
CLOSE SLICE
```

```text
BIG_BANG_INTEGRATION_AT_END = PROHIBITED
INTEGRATION_SPRINT_AS_ROUTINE_CLEANUP = ANTI_PATTERN
```

Se uma grande sprint de integração for necessária ao fim de uma fase, isso é
evidência de que as slices anteriores foram fechadas incorretamente, e não um
ritual normal do roadmap.

### 11.3 Integration Gate

```text
INTEGRATION_GATE = PASS
```

Quando aplicável ao tipo de slice, só fechar com:

```text
FEATURE_REACHABLE_FROM_REAL_ENTRYPOINT = YES
FEATURE_USES_CANONICAL_DOMAIN_PATH = YES
FEATURE_PERSISTS_THROUGH_CANONICAL_PATH = YES
FEATURE_VISIBLE_TO_REAL_CONSUMER = YES
FEATURE_PERMISSION_PATH_INTEGRATED = YES_WHEN_APPLICABLE
FEATURE_AUDIT_PATH_INTEGRATED = YES_WHEN_APPLICABLE
NO_ORPHAN_IMPLEMENTATION = YES
NO_FUTURE_BIG_BANG_INTEGRATION_REQUIRED = YES
```

Os critérios devem ser adaptados ao tipo de slice; não se deve forçar
persistência ou auditoria em uma slice puramente visual quando isso não fizer
sentido. Porém, não se pode declarar integração completa sem o caminho real de
consumo quando a capability tiver consumidor real.

### 11.4 Unidade de implementação

```text
MIGRATION / IMPLEMENTATION UNIT = VERTICAL SLICE
```

Preferir:

```text
pequena capacidade completa
→ real screen
→ real domain
→ real storage
→ real UI
→ validation
→ checkpoint
```

Evitar a sequência de tokens espalhados pelo sistema, componentes separados,
painel isolado e integração deixada para o final.

## 12. Frente transversal UI-DS

```text
UI-DS = Integração seletiva do Camera Inventory Design System v1.0.1
```

Esta frente atravessa a evolução do produto e possui dependências explícitas
com a Fase C.

### UI-0 — Read-only preflight

```text
STATUS = COMPLETE / PASS_WITH_FINDINGS
READ_ONLY = YES
STOP_AFTER_REPORT = YES
FINDINGS_REPORT_PATH = docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md
FINDINGS_DETAILS_DISCOVERABLE = YES
```

Antes de qualquer implementação visual, descobrir factualmente:

- stack atual;
- inventário atual;
- layout;
- cards;
- filtros;
- tabela;
- row interaction;
- selection model;
- camera detail route;
- canonical camera identifier;
- image source atual;
- status source;
- loading/error/stale model;
- styles/tokens;
- icon system;
- typography;
- responsive behavior;
- accessibility behavior.

Saída obrigatória do preflight:

```text
PRESERVE
ADAPT
ADOPT
DO_NOT_ADOPT
TOKEN_MAPPING
COMPONENT_MAPPING
CAMERA_QUICK_DETAIL_PANEL_MAPPING
RISKS
PILOT_SCOPE
```

UI-0 termina no relatório. Não implementar, não alterar CSS e não marcar a
implementação como autorizada por ter concluído o preflight.

### UI-1 — Token & Component Adapter Foundation

Introduzir a camada de tokens/adapters para mapear a linguagem visual do
Design System para os tokens/componentes existentes do ARGOS. Não redesenhar
páginas, não substituir a composição atual e manter a implementação futura
reversível.

### UI-2 — Inventory Visual Retrofit

Piloto no `INVENTORY`, preservando layout e comportamento. Adaptar apenas:

- background;
- cards;
- table surfaces;
- borders;
- status;
- buttons;
- inputs;
- focus;
- selection.

UI-2 não pode alterar filtro, busca, sorting, paginação, query string,
seleção ou semântica de domínio para produzir aparência.

### UI-3 — CameraQuickDetailPanel

Implementar e integrar o painel aprovado ao inventário real. UI-3 não está
completa apenas porque o drawer/painel abre. Deve integrar:

```text
real inventory selection
+ real camera identifier
+ real canonical camera summary
+ real status
+ real latest-camera-capture contract when available
+ real canonical detail route
```

`INTEGRATION_GATE` é obrigatório. O painel deve consumir lógica e dados
canônicos, preservar contexto, proteger races e navegar para a rota completa
existente, sem duplicar a página de detalhes.

Se o contrato de `LATEST_CAMERA_CAPTURE` ainda não estiver fechado pela Fase C,
UI-3 pode documentar a dependência e integrar a fronteira canônica disponível,
mas não pode declarar o requisito de imagem concluído por simulação, upload
ambíguo ou mecanismo paralelo.

### UI-4 — Visual / Functional / Accessibility / Interaction QA

Executar, quando a implementação tiver autorização própria:

```text
VISUAL QA
FUNCTIONAL QA
ACCESSIBILITY QA
INTERACTION QA
```

Preservar baseline before/after e validar:

```text
LAYOUT_PRESERVED = YES
INFORMATION_ARCHITECTURE_PRESERVED = YES
FUNCTIONAL_BEHAVIOR_PRESERVED = YES
DESIGN_SYSTEM_VISUAL_LANGUAGE_APPLIED = YES
STATUS_SEMANTICS_PRESERVED = YES
DETAIL_PANEL_VIABLE = YES
ACCESSIBILITY_ACCEPTABLE = YES
FUNCTIONAL_REGRESSION_NONE = YES
UNAUTHORIZED_STACK_CHANGE_NONE = YES
```

O checklist visual do pacote também deve ser traduzido para o ambiente real:
usar tokens semânticos para canvas, surface, border, sidebar e primary; não
introduzir cor, spacing, fonte ou radius arbitrário; reutilizar componentes
existentes; validar loading, empty, error, disabled, responsive e stale; e
registrar qualquer novo token/variant antes de sua adoção.

## 13. Critérios específicos do painel

O gate do `CameraQuickDetailPanel` deve cobrir:

```text
PANEL_OPENS
PANEL_CLOSES
KEYBOARD_ACTIVATION
ESCAPE_CLOSE
FOCUS_TRAP_WHEN_APPLICABLE
FOCUS_RESTORE
INVENTORY_CONTEXT_PRESERVED
FILTER_STATE_PRESERVED
CAMERA_IMAGE
CAMERA_IMAGE_FALLBACK
SUMMARY_DATA
STATUS_SEMANTICS
CHANGE_SELECTED_CAMERA
ASYNC_RACE_PROTECTION
FULL_DETAILS_NAVIGATION
CURRENT_DETAILS_ROUTE_REUSED
NO_DOMAIN_DUPLICATION
```

### 13.1 Não duplicar domain logic

O painel não calcula independentemente:

- status;
- health;
- connectivity;
- availability;
- monitoring state;
- VMS condition.

Ele consome resultados canônicos produzidos pelo domínio. Se uma informação
necessária não estiver disponível por caminho canônico, a lacuna deve ser
registrada como dependência, não preenchida por cálculo visual local.

### 13.2 Progressive disclosure

```text
# INVENTORY ROW
minimum necessary information

# QUICK DETAIL PANEL
useful operational summary

# FULL DETAIL PAGE
complete information
```

Cada nível acrescenta informação. Os três níveis não devem repetir exatamente
o mesmo conteúdo.

### 13.3 Ações

```text
PRIMARY ACTION = Ver detalhes
```

Poucas ações rápidas adicionais só podem ser incluídas com necessidade
operacional comprovada. Nenhuma ação destrutiva deve ser adicionada como
consequência automática desta frente.

## 14. Ordem futura de execução e gates

A ordem documental recomendada, considerando os checkpoints concluídos, é:

1. `IMG-01 — Contrato funcional` — COMPLETE / DOCUMENTAL;
2. `UI-0 — Read-only preflight` — COMPLETE / PASS_WITH_FINDINGS;
3. adjudicação humana e autorização específica para IMG-02;
4. fechamento de `IMG-02` para proveniência, modelo e consulta da última captura;
5. `UI-1 — Token & Component Adapter Foundation`;
6. `UI-2 — Inventory Visual Retrofit`;
7. slices da Fase C conforme dependências (`IMG-03` a `IMG-09`), integradas ao
   caminho canônico;
8. `UI-3 — CameraQuickDetailPanel`, somente com o contrato real de resumo,
   status, rota e latest capture disponível quando aplicável;
9. `UI-4 — Visual / Functional / Accessibility / Interaction QA`;
10. checkpoint documental e técnico da slice.

Esta ordem não renumera nem substitui as macrofases existentes. UI-DS é uma
frente transversal; as dependências podem ser executadas em slices verticais,
mas nenhuma etapa pode fechar um consumidor órfão para futura integração em
big-bang.

## 15. Hard constraints

```text
DO_NOT_REDESIGN_ARGOS
DO_NOT_COPY_PROTOTYPE_AS_PRODUCT
DO_NOT_REPLACE_INFORMATION_ARCHITECTURE
DO_NOT_REPLACE_PAGE_COMPOSITION
DO_NOT_MIGRATE_FRAMEWORKS
DO_NOT_CHANGE_BUSINESS_LOGIC
DO_NOT_CHANGE_DOMAIN_STATUS_SEMANTICS
DO_NOT_INVENT_STATUS
DO_NOT_DUPLICATE_CAMERA_DETAILS_PAGE
DO_NOT_DUPLICATE_DOMAIN_LOGIC
DO_NOT_INVENT_VISUAL_VALUES_WHEN_TOKEN_EXISTS
DO_NOT_ADD_EXPENSIVE_CAMERA_REQUESTS_WITHOUT_ANALYSIS
DO_NOT_BIG_BANG_MIGRATE
DO_NOT_CLOSE_ORPHAN_FEATURES
DO_NOT_SILENTLY_RESOLVE_CONTRACT_CONFLICTS
```

Também são boundaries desta frente:

- não instalar dependências por causa da stack de referência;
- não introduzir captura, polling ou chamada VMS no evento de abertura do
  painel;
- não tratar imagem manual como captura real;
- não esconder stale, erro ou indisponibilidade;
- não fechar UI-3 apenas com shell visual sem integração canônica;
- não usar cor para inventar semântica de status;
- não executar commit, push, deploy ou alteração LIVE por inferência desta
  specification.

## 16. Package retention e futuras revisões

O pacote de origem foi localizado em `Downloads` e incorporado ao repositório
como cópia de referência. O título interno `DESIGN_SYSTEM_SPEC.md` foi alinhado
à versão confirmada pelo manifesto (`1.0.1`). A cópia externa original foi
preservada sem alteração.

```text
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
REFERENCE_PACKAGE_TITLE_VERSION = v1.0.1
REFERENCE_PACKAGE_REPOSITORY_SHA256 = 510D75399A5C2F641DB77EF1AF9C982B8A2B3D9C08B06854073CE16FE028DA14
```

Para continuidade, a cópia repositória é a referência canônica. O arquivo
externo é mantido como origem recebida. Não misturar `v1.0` com `v1.0.1` em
revisões futuras; se o pacote mudar, registrar nova versão, path e hash factuais
e preservar as decisões de authority, estrutura, proveniência, painel e
integração incremental deste documento.

## 17. Document quality gate

Antes de tratar esta specification como authority operacional, responder:

```text
CAN_A_NEW_AGENT_UNDERSTAND_AND_EXECUTE_THE_INTENT_WITHOUT_CHAT_HISTORY?
```

Para `PASS`:

```text
YES
```

Esta specification não depende de “conforme conversamos”, mensagem anterior,
conhecimento tácito do usuário ou disponibilidade imediata do pacote. Toda
decisão material sobre estratégia, authorities, stack, composição, painel,
imagem, Fase C, slices, gates e proibições está escrita aqui.

```text
DOCUMENT_QUALITY_GATE = PASS
CAN_NEW_AGENT_EXECUTE_WITHOUT_CHAT_HISTORY = YES
```

## 18. Referências de continuidade

As referências operacionais de continuidade devem apontar para este documento,
sem duplicar seu conteúdo integral:

- `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`;
- `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`;
- `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`;
- `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md`;
- `docs/projeto/ROADMAP_ARGOS_V5.md`;
- `docs/projeto/SPRINTS_ARGOS_V5.md`.

Esses documentos registram existência, path, dependências e próximo passo. Esta
specification permanece a authority detalhada.

# ARGOS UI V2 — Camera Detail Visual Architecture Contract

> Revisão vigente S2A-R3 (2026-10-06), autorizada pelo pedido explícito do usuário:
> a seção 26 prevalece sobre as decisões anteriores de ausência de surface/borda
> nas quatro macro regiões. As demais restrições funcionais e de composição
> continuam vigentes. Aprovação visual humana: PENDING.

```text
DOCUMENT_TYPE = CANONICAL_SCREEN_ARCHITECTURE_CONTRACT
PROJECT = ARGOS
SCREEN = SCR-CAM-DETAIL-001 / Camera Detail
ACTIVITY = P5-VR-S2A-R2 — Canonicalization
SOURCE_PROPOSAL = P5-VR-S2A-R1 — Camera Detail Visual Architecture Contract Proposal
SOURCE_PROPOSAL_STATUS = PASS / STATIC CONTRACT PROPOSAL
USER_ADJUDICATION = APPROVED WITH REQUIRED REFINEMENT
ADJUDICATION_SCOPE = architecture below; one mandatory Legacy Presentational Class Migration refinement
CONTRACT_STATUS = APPROVED / CANONICAL
DESIGN_SYSTEM_VERSION = 2.1.0
DS_GAP = NONE
DOMAIN_DECISION_GAP = NONE
ARCHITECTURAL_AMBIGUITIES_REMAINING = NONE
S2B_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
CAMERA_DETAIL_IMPLEMENTATION = NOT_STARTED
CAMERA_DETAIL_VISUAL_RUNTIME_VALIDATION = NOT_PERFORMED
CAMERA_DETAIL_USER_VISUAL_APPROVAL = PENDING
LANGUAGE = pt-BR
```

Este documento canonicaliza as decisões adjudicadas da proposta S2A-R1. As
seções 1–24 abaixo preservam o inventário e os contratos da proposta; a seção
25 incorpora o refinamento obrigatório aprovado. Não há autorização para
implementar S2B. `NEXT_REQUIRED_ACTIVITY` não equivale a autorização de execução.

## Rastreabilidade e authorities

- Screen Census: `docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md`
- Plano operacional: `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`
- Design System: `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md`
- Catálogo: `docs/prototype/ui-v2/contracts/COMPONENT_CATALOG.md`
- DSCR 2.1.0: `docs/prototype/ui-v2/contracts/DSCR-UIV2-003-SHARED-PATTERNS-2.1.0.md`

```text
P5-VR-S1A = CLOSED
P5-VR-S1B = IMPLEMENTED / PUBLISHED
P5-VR-S1B_CHECKPOINT = eaeb25e19b0c6fb99e8bc78efd75ce368195d9d3
P5-VR-S2A-R1 = ARCHITECTURE PROPOSAL COMPLETE / APPROVED WITH REFINEMENT
P5-VR-S2A-R2 = PASS
P5-VR-S2B = NEXT REQUIRED / NOT AUTHORIZED
```

## Inventário factual e contrato aprovado

CURRENT_PAGE_INVENTORY
======================================================================

Convenções:

C = camera
M = monitoring
D = renderização por default:"—"
T = date:"d/m/Y H:i"

Todos os campos dependem do acesso à página por:

cameras.view_camera

Todos podem ser movidos visualmente, preservando:
- fonte;
- associação;
- condição;
- conteúdo.

Nenhum dado pode ser removido.

Somente ocorrências duplicadas explicitamente identificadas neste contrato
podem desaparecer.

----------------------------------------------------------------------
CAMPOS ATUAIS
----------------------------------------------------------------------

1. C.nome
Current section:
Hero; Identificação / Nome
Rendering:
H1; valor em destaque no grupo

2. C.fabricante
Current section:
Hero; Identificação / Fabricante
Rendering:
Opcional no resumo do Hero; valor direto no grupo

3. C.modelo
Current section:
Hero; Identificação / Modelo
Rendering:
Opcional no resumo do Hero; valor direto no grupo

4. C.get_tipo_display
Current section:
Hero; Identificação / Tipo
Rendering:
Hero condicionado a C.tipo; D no grupo

5. C.patrimonio
Current section:
Hero / Patrimônio; Identificação / Patrimônio
Rendering:
D; monospace

6. C.ip
Current section:
Hero / Endereço IP; Rede / IP
Rendering:
D; monospace

7. C.terminal
Current section:
Hero / Localização; Localização / Terminal
Rendering:
Resumo condicional; D no grupo

8. C.ambiente
Current section:
Hero / Localização; Localização / Ambiente
Rendering:
Resumo condicional; D no grupo

9. M.label + M.effective_state
Current section:
Hero; Monitoramento / Estado atual
Rendering:
Badge do partial de monitoramento

10. M.contexto
Current section:
Hero; Monitoramento / Estado atual
Rendering:
title no badge e texto em small, se presente

11. C.get_situacao_operacional_display
Current section:
Hero; Situação e completude / Situação
Rendering:
Badge por situação

12. C.cadastro_completo
Current section:
Hero; Situação e completude / Completude
Rendering:
Cadastro completo ou Cadastro incompleto

13. C.serial
Current section:
Identificação / Serial
Rendering:
D; monospace

14. C.mac
Current section:
Identificação / MAC
Rendering:
D; monospace

15. C.pavimento
Current section:
Localização / Pavimento
Rendering:
D

16. C.setor
Current section:
Localização / Setor
Rendering:
D

17. C.descricao_detalhada
Current section:
Localização / Descrição detalhada
Rendering:
D; texto integral

18. C.ponto_referencia
Current section:
Localização / Ponto de referência
Rendering:
D; texto integral

19. C.mascara_subrede
Current section:
Rede / Máscara
Rendering:
D; monospace

20. C.gateway
Current section:
Rede / Gateway
Rendering:
D; monospace

21. C.vlan
Current section:
Rede / VLAN
Rendering:
D; monospace

22. C.farm
Current section:
Gravação / Farm
Rendering:
D; monospace

23. C.retencao_esperada_dias
Current section:
Gravação / Retenção esperada
Rendering:
D; monospace

24. C.codec
Current section:
Gravação / Codec
Rendering:
D; monospace

25. M.stable_label
Current section:
Monitoramento / Último estado confirmado
Rendering:
Texto direto

26. M.evidence_at
Current section:
Monitoramento / Última evidência útil
Rendering:
T + D

27. M.state_since
Current section:
Monitoramento / Estado desde
Rendering:
T + D

28. M.open_outage.opened_at + M.outage_duration
Current section:
Monitoramento / Indisponibilidade aberta
Rendering:
Desde {T} · {duração}
Somente se M.open_outage

29. C.criado_por
Governança cadastral / Criado por
D

30. C.criado_em
Governança cadastral / Criado em
T

31. C.atualizado_por
Governança cadastral / Atualizado por
D

32. C.atualizado_em
Governança cadastral / Atualizado em
T

33. C.get_origem_cadastro_display
Governança cadastral / Origem
Texto direto

34. C.observacoes
Governança cadastral / Observações
D

35. C.rotulos_campos_incompletos
Situação e completude / Campos faltantes
join:", "
Somente quando cadastro incompleto

36. C.motivo_desativacao
Situação e completude / Motivo da última desativação
D

37. C.desativada_em
Situação e completude / Desativada em
T + D

38. C.desativada_por
Situação e completude / Desativada por
D

O resumo de equipamento usa separadores · somente entre valores existentes.

Quando fabricante/modelo/tipo estão ausentes:
—

O resumo de localização também compõe somente terminal/ambiente existentes.

Quando ambos estão ausentes:
—

----------------------------------------------------------------------
HISTÓRICOS ATUAIS
----------------------------------------------------------------------

outage_preview
Fields:
opened_at
closed_at
duration
open_origin
close_reason
Limit:
até 5
Rules:
fechamento ausente = "Em aberto"
motivo somente se presente

atividades
Fields:
get_tipo_display
titulo
descricao
ocorrida_em
responsavel
Limit:
até 10
descricao:
truncatechars:180
responsavel:
D
edição:
condicionada

substituicoes
Fields:
ocorrida_em
papel da câmera
nome_operacional
nome_anterior_substituta
Limit:
até 10
Permission:
consultar_substituicoescamera
Papel depende da comparação com camera_anterior_id.

eventos_auditoria
Fields:
codigo
resumo
Limit:
até 10
Permission:
consultar_eventos

Atividades, substituições e auditoria mantêm ordenação decrescente de
ocorrência e PK conforme os modelos.

Indisponibilidades mantêm a seleção/ordenação do MonitoringReadService.

Não aparecem hoje no detalhe:
- imagem de preview;
- captura;
- credenciais;
- RTSP;
- teste de conexão;
- diagnóstico.

A existência dessas capacidades em outras rotas não autoriza adicioná-las aqui.

----------------------------------------------------------------------
AÇÕES ATUAIS
----------------------------------------------------------------------

Todas as ações de navegação são links GET.

Confirmações e POST permanecem nas páginas de destino.

Somente upload possui formulário nesta página.

1. ← Voltar ao inventário
Route:
cameras:lista
/cameras/
Condition:
nenhuma condição adicional
Current location:
Hero
Confirmation/CSRF:
none

2. Editar câmera
Route:
cameras:editar(C.pk)
Permission:
change_camera
Current location:
Hero
Form:
GET/POST no destino
CSRF no destino

3. Mover para Estoque
Route:
cameras:alterar_situacao(C.pk)
Condition:
PRODUCAO + alterar_situacao_camera
Confirmation:
destino
CSRF:
destino

4. Colocar em Produção
Same route
Condition:
ESTOQUE + alterar_situacao_camera

5. Desativar
Route:
cameras:desativar(C.pk)
Condition:
PRODUCAO ou ESTOQUE + desativar_camera

6. Substituir
Route:
cameras:substituir(C.pk)
Condition:
PRODUCAO + registrar_substituicao_camera
Form transacional no destino

7. Reativar
Route:
cameras:reativar(C.pk)
Condition:
ramo atual else + reativar_camera

8. Ver histórico completo — indisponibilidades
Route:
cameras:historico_monitoramento(C.pk)
Endpoint:
view_camera

9. Ver histórico completo — atividades
Route:
cameras:lista_atividades(C.pk)
Endpoint:
view_atividadecamera

10. Registrar atividade
Route:
cameras:criar_atividade(C.pk)
Permission:
add_atividadecamera

11. Editar atividade
Route:
cameras:editar_atividade(atividade.pk)
Permission:
change_atividadecamera

12. Ver histórico completo — substituições
Route:
cameras:lista_substituicoes_camera(C.pk)
Permission:
consultar_substituicoescamera

13. Abrir substituição
Route:
cameras:detalhe_substituicao(item.pk)

14. Ver todos os eventos
Route:
cameras:eventos_camera(C.pk)
Permission:
consultar_eventos

15. Abrir evento
Route:
eventos:detalhe(evento.pk)

16. Enviar imagem
Route:
cameras:upload_imagem(C.pk)
HTTP:
POST
Permission:
add_cameraimagerecord
endpoint também exige view_camera

UPLOAD CONTRACT:

Heading:
Enviar imagem manualmente

Explanation:
A imagem será registrada como upload manual, sem data de captura da câmera.

Label:
Imagem

Input:
id="imagem-camera"
name="imagem"
type="file"
required
accept="image/jpeg,image/png,image/webp"

Submit:
Enviar imagem

Resultado e erros:
messages + redirect para detalhe.

Partials:
_monitoring_badge.html
_atividade_tipo_badge.html

Página herda:
shell
messages
skip link
de base.html.

IDs locais:
camera-detail-title
imagem-camera

Não há no detalhe:
data-*
JavaScript próprio
paginação
accordion
tabs


1. NAVIGATION CONTEXT / BACK
======================================================================

BACK_NAVIGATION_LABEL =
← Voltar ao inventário

BACK_NAVIGATION_DESTINATION =
cameras:lista / /cameras/

BACK_NAVIGATION_SEMANTICS =
link nativo

BACK_NAVIGATION_POSITION_DESKTOP =
primeira região do conteúdo

BACK_NAVIGATION_POSITION_MOBILE =
primeira região do conteúdo

BACK_NAVIGATION_RELATION_TO_PAGE_HEADER =
ABOVE

BACK_NAVIGATION_ICON_USAGE =
EXISTING_CAPABILITY_ONLY / seta textual atual

BACK_NAVIGATION_SPACING =
argos-space-3 entre retorno e Header

BACK_NAVIGATION_PERMISSION_DEPENDENCY =
nenhuma condição adicional no template

BACK_NAVIGATION_CONTEXT_DEPENDENCY =
destino fixo;
sem browser history;
sem return URL;
sem filtros;
sem novos parâmetros

Treatment:
link textual
sem surface
sem button

A seta atual não será substituída por biblioteca de ícones.

O retorno permanece visualmente subordinado ao título e à identidade.

======================================================================
2. PAGE HEADER
======================================================================

PAGE_HEADER_ROLE =
PAGE_ORIENTATION

eyebrow/context =
Inventário CFTV

title =
Detalhe da câmera

description =
NONE

metadata =
NONE

primary action =
NONE

PAGE_HEADER_ACTION_POSITION =
NONE

PAGE_HEADER_MOBILE_BEHAVIOR =
largura disponível;
texto quebra naturalmente

PAGE_HEADER_DUPLICATION_RULE =
nenhuma informação de entidade

"Inven­tário CFTV" vem da página atual.

"Detalhe da câmera" é o nome factual da superfície no Screen Census.

Consumir:

argos-page-header
argos-page-header__copy
argos-eyebrow
argos-page-title

H1 =
Detalhe da câmera

Não incluir no Header:
- nome;
- equipamento;
- localização;
- badges;
- completude.

Document title permanece:

{{ camera.nome }} — ARGOS

======================================================================
3. CAMERA HERO
======================================================================

CAMERA_HERO_ROLE =
ENTITY_OPERATIONAL_SUMMARY

CAMERA_HERO_ALLOWED_SURFACE =
NONE

CAMERA_HERO_BORDER =
NONE

CAMERA_HERO_BACKGROUND =
transparente / canvas herdado

CAMERA_HERO_INTERNAL_GROUPING =
identidade;
estados;
ação;
resumo de orientação

CAMERA_HERO_PRIMARY_INFORMATION =
nome

CAMERA_HERO_SECONDARY_INFORMATION =
patrimônio;
terminal + ambiente

CAMERA_HERO_STATUS_INFORMATION =
monitoramento + contexto;
situação;
completude

CAMERA_HERO_ACTIONS =
Editar câmera
somente com change_camera

CAMERA_HERO_MUST_NOT_REPEAT =
título/contexto do Header;
fabricante;
modelo;
tipo;
IP;
demais dados técnicos e administrativos

Fields:

Nome
ROLE = PRIMARY
Treatment = H2
argos-text-kpi
semibold
argos-line-tight
ID = camera-detail-title
Mobile = texto integral + wrap

Monitoramento + contexto
ROLE = STATUS
Treatment = Status Badge
Mobile = badge quebra; contexto abaixo

Situação
ROLE = STATUS
Treatment = Status Badge

Completude
ROLE = STATUS
Treatment = Status Badge

Editar câmera
ROLE = ACTION
Treatment = Button Primary

Patrimônio
ROLE = SECONDARY
Treatment = Data Pair
Value = mono

Terminal + ambiente
ROLE = SECONDARY
Treatment = Data Pair
Label = Localização
Composição factual atual

DESKTOP / INTERMEDIATE >680px:

linha 1:
nome = minmax(0,1fr)
edição = auto

linha 2:
estados em sequência
wrap permitido

linha 3:
patrimônio + localização
2 Data Pairs

MOBILE <=680px:

nome
→ estados/contexto
→ edição autorizada
→ patrimônio
→ localização

Não há:
- min-height;
- card;
- colored header;
- imagem.

Nome e patrimônio ficam exclusivamente no Hero.

Localização:
summary no Hero
+
full detail em Localização.

======================================================================
4. MAIN DATA
======================================================================

Heading macro =
Dados principais

DOM order:

Identificação
→ Localização
→ Rede
→ Gravação

COMMON RULES:

DATA_GROUP_DENSITY =
STANDARD

Usar:
argos-data-group
Data Pair

Labels:
acima dos valores

Data Pairs:
2 colunas iguais >680px
1 coluna <=680px

gap =
argos-space-4

label/value association =
argos-space-1

min-width =
0

overflow-wrap =
anywhere

height =
auto

Proibido:
ellipsis
clamp
new truncation

Dividers =
NONE

Empty value =
—

Mono:
somente campos explicitamente listados.

IDENTIFICAÇÃO

Fields order:
Fabricante
Modelo
Serial
MAC
Tipo

D/I/M =
2 / 2 / 1

Full-width =
NONE

Mono =
Serial
MAC

LOCALIZAÇÃO

Fields order:
Terminal
Pavimento
Setor
Ambiente
Descrição detalhada
Ponto de referência

D/I/M =
2 / 2 / 1

Full-width =
Descrição detalhada
Ponto de referência

Mono =
NONE

REDE

Fields order:
IP
Máscara
Gateway
VLAN

D/I/M =
2 / 2 / 1

Full-width =
NONE

Mono =
todos os quatro

GRAVAÇÃO

Fields order:
Farm
Retenção esperada
Codec

D/I/M =
2 / 2 / 1

Full-width =
NONE

Mono =
os três
preservando tratamento atual

D =
desktop canônico

I =
900×900

M =
390×844

Nome e patrimônio NÃO reaparecem em Identificação.

Fabricante/modelo/tipo:
removidos do resumo do Hero
mantidos em Identificação.

IP:
removido do Hero
mantido em Rede.

DESKTOP >900px:

external grid =
minmax(0,3fr) minmax(0,2fr)

gap =
argos-space-6

left column:
Identificação
Localização

right column:
Rede
Gravação

Cada coluna:
stack
gap = argos-section-gap
align-start
sem equal-height

<=900px:

4 groups stacked
semantic order preserved

Data Pairs:
2 columns until 680px
1 column <=680px

RATIONALE:

left =
11 fields
including long Description + Reference

right =
7 mainly short technical values

SURFACE =
NONE
para todos os grupos.

======================================================================
5. OPERATION
======================================================================

Heading =
Operação

OPERATION_SECTION_ORDER =

Monitoramento técnico
→ Situação e completude

MONITORAMENTO TÉCNICO

Fields:
Estado atual + contexto
Último estado confirmado
Última evidência útil
Estado desde
Indisponibilidade aberta, se existente

Actions =
NONE

Priority =
PRIMARY operacional

Surface =
NONE

SITUAÇÃO E COMPLETUDE

Fields:
Situação
Completude
Campos faltantes, se incompleto
Motivo da última desativação
Desativada em
Desativada por

Actions =
ações operacionais atuais

Priority =
PRIMARY operacional

Surface =
NONE

DESKTOP >900px:

grid =
minmax(0,2fr) minmax(0,3fr)

gap =
argos-space-6

Monitoramento =
40%

Situação/completude =
60%

RATIONALE:
Situação possui ações, campos faltantes e motivo textual.

<=900px:

stack:
Monitoramento
→ Situação

Data Pairs:
2 columns >680
1 column <=680

FULL WIDTH:

Monitoramento:
Estado atual/contexto
Indisponibilidade aberta

Situação:
Campos faltantes
Motivo da última desativação

DENSITY =
STANDARD

wrap/spacing/dividers =
mesmos do Main Data

mono =
NONE

AÇÕES DE SITUAÇÃO:

position =
depois dos campos

alignment =
start

order =
ação construtiva principal
→ movimentação secundária
→ Desativar

Preservar condições atuais.

Não mover ações para Governança cadastral.

ESTADOS TÉCNICOS:

usar:

M.effective_state
M.label
M.contexto
M.stable_label

Nunca substituir por status legado de Camera.

Visual mapping:

ONLINE = success
OFFLINE = danger
UNKNOWN = neutral
OUT_OF_SCOPE = neutral

PRODUCAO = success
ESTOQUE = neutral
DESATIVADA = neutral

Cadastro completo = success
Cadastro incompleto = warning

Preservar:

NÃO MONITORADA
Dados desatualizados
Configuração incompleta
Fora do escopo
Offline há…

Stale não cria quarto estado estável.

Campos ausentes =
—

Sem open outage:
par desaparece.

Campos faltantes:
permanecem associados à Completude.
Sem warning panel novo.

======================================================================
6. GOVERNANCE
======================================================================

GOVERNANCE_FIELDS =
Criado por
Criado em
Atualizado por
Atualizado em
Origem
Observações

GOVERNANCE_ACTIONS =
NONE

GOVERNANCE_DESKTOP_POSITION =
após Operação
antes de Histórico

GOVERNANCE_WIDTH_BEHAVIOR =
full available width

GOVERNANCE_RELATION_TO_OPERATION =
supporting cadastral metadata
fora do operational grid

GOVERNANCE_SURFACE =
NONE

GOVERNANCE_ACTION_POSITION =
NONE

GOVERNANCE_DATA_PATTERN =
Data Group + Data Pair / STANDARD

GOVERNANCE_MOBILE_POSITION =
após Situação/completude
antes de Histórico

GOVERNANCE_VISUAL_PRIORITY =
SUPPORTING

Heading =
Governança cadastral

Pairs:
2 per row >680
1 <=680

Observações =
full-width

Dates =
d/m/Y H:i

Text =
full wrap

Mono =
NONE

Dividers =
NONE

Não reservar 50% do grid.

Não repetir:
situação
completude
ações operacionais

======================================================================
7. HISTORY
======================================================================

Heading macro =
Histórico

HISTORY_ORDER =

Indisponibilidades
→ Atividades
→ Substituições
→ Eventos/Auditoria

HISTORY_FAMILY_LAYOUT_DESKTOP =
single stack / full-width

HISTORY_FAMILY_LAYOUT_INTERMEDIATE =
same

HISTORY_FAMILY_LAYOUT_MOBILE =
same

HISTORY_FAMILY_SECTION_SPACING =
argos-space-6

HISTORY_ACTION_ALIGNMENT =

>680:
actions right of heading

<=680:
actions below heading

HISTORY_EMPTY_STATE_CONSISTENCY =
Compact Empty State
factual copy
no surface
no icon
no min-height

INDISPONIBILIDADES

Heading:
Histórico técnico de indisponibilidades

Action:
Ver histórico completo

ACTION_CONTEXT:
SECTION_LEVEL

Content:
technical summary list

Initial display:
até 5
immediately visible

Link:
historico_monitoramento(C.pk)

ATIVIDADES

Heading:
Histórico de atividades

Actions:
Registrar atividade = SECTION_LEVEL
Ver histórico completo = SUPPORTING
Editar = SUPPORTING no item

Content:
activity preview list

Initial display:
até 10

Description:
truncatechars:180

Link:
lista_atividades(C.pk)

SUBSTITUIÇÕES

Heading:
Histórico de substituições

Action:
Ver histórico completo = SECTION_LEVEL
item link = SUPPORTING

Content:
historical relations list

Initial:
até 10

Permission:
consultar_substituicoescamera

Link:
lista_substituicoes_camera(C.pk)

AUDITORIA

Heading:
Eventos de auditoria

Action:
Ver todos os eventos = SECTION_LEVEL
item link = SUPPORTING

Content:
codigo + resumo

Initial:
até 10

Permission:
consultar_eventos

Link:
eventos_camera(C.pk)

ALL HISTORY BLOCKS:

SURFACE =
NONE

DIVIDER =
NONE

EMPTY_STATE_VARIANT =
argos-state--compact

EMPTY STATE COPIES:

Nenhuma indisponibilidade técnica registrada.

Nenhuma atividade registrada para esta câmera.

Nenhuma substituição registrada para esta câmera.

Nenhum evento registrado.

FILLED ITEMS:

List gap =
argos-space-3

No:
card
border
shadow
background

Internal gap =
argos-space-2

Indisponibilidade preserves:
abertura
fechamento / Em aberto
duration
origem
close reason

Atividade preserves:
type badge
title
description
occurrence
responsible
authorized editing

Substitution preserves:
Foi substituída / Entrou como substituta
historical names
item.pk link

Audit preserves:
code
summary
evento.pk destination

Activity badge mapping:

AVARIA = danger

RETIRADA = warning
ENVIO_CONSERTO = warning
RETORNO_CONSERTO = warning

OUTRO = neutral

others, including SUBSTITUICAO = info

No new DS "special" variant.

Preview limits/order unchanged.

PROHIBITED:

collapse
show more
tabs
new pagination
lazy rendering

======================================================================
8. COMPLEMENTARY OPERATIONS
======================================================================

COMPLEMENTARY_OPERATION =
manual upload

POSITION =
after all authorized histories

SURFACE =
NONE

HEADING =
Enviar imagem manualmente

ACTION_HIERARCHY =
one Primary submit

ACTION_CONTEXT =
SECTION_LEVEL

Macro heading =
Operações complementares

Entire region only renders when upload is allowed by current permission.

Preserve exactly:

explanation
label
input
accept
required
name
ID
multipart
CSRF
action
submit

DESKTOP / INTERMEDIATE >680:

explanation
→ field + submit same last row

grid:
minmax(0,1fr) auto

gap:
argos-space-3

align:
end

MOBILE:

explanation
→ field
→ submit

field and submit contained.

Filename cannot widen document.

input:
min-width:0
max available width

No preview.

No new confirmation.

Messages remain inherited.

======================================================================
9. ACTION HIERARCHY
======================================================================

← Voltar ao inventário
Context = PAGE_LEVEL
Variant = TEXT_LINK
Position = above Header

Editar câmera
Context = ENTITY_LEVEL
Variant = PRIMARY
Position = Hero

Mover para Estoque
Context = SECTION_LEVEL
Variant = SECONDARY
Position = end of Situação/completude

Colocar em Produção
Context = SECTION_LEVEL
Variant = PRIMARY
Position = same

Substituir
Context = SECTION_LEVEL
Variant = PRIMARY
Position = same

Reativar
Context = SECTION_LEVEL
Variant = PRIMARY
Position = same

Desativar
Context = DESTRUCTIVE
Variant = DANGER
Position = last operational action

Ver histórico completo — indisponibilidades
Context = SECTION_LEVEL
Variant = SECONDARY + COMPACT
Position = block heading

Ver histórico completo — atividades
Context = SUPPORTING
Variant = SECONDARY + COMPACT
Position = after Registrar atividade

Registrar atividade
Context = SECTION_LEVEL
Variant = PRIMARY + COMPACT
Position = Activities heading

Editar atividade
Context = SUPPORTING
Variant = TEXT_LINK
Position = item

Ver histórico completo — substituições
Context = SECTION_LEVEL
Variant = SECONDARY + COMPACT
Position = block heading

Abrir substituição
Context = SUPPORTING
Variant = TEXT_LINK
Position = item

Ver todos os eventos
Context = SECTION_LEVEL
Variant = SECONDARY + COMPACT
Position = Audit heading

Abrir evento
Context = SUPPORTING
Variant = TEXT_LINK
Position = item

Enviar imagem
Context = SECTION_LEVEL
Variant = PRIMARY
Position = upload form end

Colocar em Produção / Substituir / Reativar are mutually exclusive by
current conditions.

At most one Primary in that operational region.

Desativar = Danger because it removes camera from operation and current
flow already has destructive confirmation.

COMPACT is modifier, combined with Primary/Secondary.

Mobile button height 44px comes from DS <=600px.

Do not create Success button variant.

No actions in Page Header.

No actions in Governance.

======================================================================
10. SURFACE CONTRACT
======================================================================

Navigation Context = NONE
Rationale:
auxiliary text navigation

Page Header = NONE
Rationale:
page orientation

Camera Hero = NONE
Rationale:
content hierarchy communicates entity/state

Main Data = NONE

Identificação = NONE
Localização = NONE
Rede = NONE
Gravação = NONE

Operação = NONE

Monitoramento técnico = NONE

Situação/completude = NONE

Governança cadastral = NONE

History container = NONE

Indisponibilidades = NONE

Atividades = NONE

Substituições = NONE

Auditoria = NONE

History items = NONE

Complementary Operations = NONE

Upload = NONE

SURFACES_ALLOWED =
controls
badges
inherited feedback
as defined by existing DS/mechanism

SURFACES_REMOVED =
Hero card
data cards
operation/governance cards
history cards
history item cards
empty-state boxes

Intrinsic surfaces of:
button
input
badge

are not section surfaces.

Do not alter shell message container.

======================================================================
11. DIVIDER / BORDER CONTRACT
======================================================================

SECTION_DIVIDER =
NONE

DATA_GROUP_DIVIDER =
NONE

HISTORY_DIVIDER =
NONE

BORDER_USAGE_RULE =
only intrinsic borders from existing components

No decorative border for:
region
group
pair
item

Remove:

colored top bars
label/value lines
heading borders
long separators
dashed empty-state borders

Do not alter:
shell borders
fields
buttons
badges

No section shadows.

======================================================================
12. WIDTH / CONTENT CONTAINER CONTRACT
======================================================================

PAGE_CONTENT_MODE =
CONSTRAINED_CONTENT

PAGE_CONTENT_MAX_WIDTH =
argos-content-max / 1440px

PAGE_HORIZONTAL_PADDING_DESKTOP =
argos-page-inline / 30px

PAGE_HORIZONTAL_PADDING_INTERMEDIATE =
argos-page-inline / 30px

PAGE_HORIZONTAL_PADDING_MOBILE =
argos-page-inline-mobile / 14px

Use existing productive container from base.html/production.css:

width:
min(100%, var(--argos-content-max))

centered

Do not create another max-width or external padding.

Foundation documentation has 16px <=900, but productive shell currently
keeps 30px until mobile transition.

Preserve productive shell rule.

Page wrapper:
width 100% internally
min-width:0

Columns calculate against content area, not viewport/sidebar ignored.

======================================================================
13. DESKTOP GRID CONTRACT
======================================================================

Canonical viewports:

1920×1080
1440×900
1366×768

Zoom:
100%

Navigation/Header:
full-width
one column

Hero main row:
breakpoint 680px
grid = minmax(0,1fr) auto
gap = space-4

Hero summary:
breakpoint 680px
2 columns 1fr/1fr
gap = space-4

Main Data:
breakpoint 900px
2 columns 3fr/2fr
gap = space-6

Data Group pairs:
breakpoint 680px
2 columns 1fr/1fr
gap = space-4

Operation:
breakpoint 900px
2 columns 2fr/3fr
gap = space-6

Governance:
full-width
pair breakpoint 680px
2 pairs/row
gap = space-4

History:
one column
full-width
all sizes
gap = space-6 between blocks

Upload:
breakpoint 680px
field = 1fr
submit = auto
gap = space-3

All flexible tracks:
minmax(0,...)

Texts wrap.

Actions may wrap.

Do not:
equalize column heights
use masonry
fill empty space with surfaces

900px and 680px already exist in patterns.css.

======================================================================
14. INTERMEDIATE RESPONSIVE CONTRACT
======================================================================

INTERMEDIATE_RESPONSIVE_SMOKE =
REQUIRED

INTERMEDIATE_VIEWPORT =
900×900

BREAKPOINT_SOURCE =

patterns.css max-width:900px
patterns.css max-width:680px
components.css max-width:600px for touch targets

GRID_TRANSITION =
Main Data + Operation become one column at <=900px

OVERFLOW =
no global horizontal overflow
no nested vertical scroll

ACTION_PLACEMENT =
Hero keeps name + action
section actions may wrap

DATA_GROUP_BEHAVIOR =
four groups sequentially
pairs remain 2 columns

HISTORY_BEHAVIOR =
single stack
same limits and links

GOVERNANCE_BEHAVIOR =
full-width
2 pairs/row

During S2B smoke also inspect:

899px
900px
901px

height:
900px

No new breakpoint.

Do not reuse 697px/1013px KPI breakpoints.

======================================================================
15. MOBILE CONTRACT
======================================================================

Viewport:
390×844

Zoom:
100%

MOBILE_SECTION_ORDER:

1. Back navigation
2. Page Header
3. Hero
4. Main Data:
   Identificação
   Localização
   Rede
   Gravação
5. Operation:
   Monitoramento técnico
   Situação/completude
6. Governance
7. History:
   Indisponibilidades
   Atividades
   Substituições
   Auditoria
8. Complementary Operations / upload, if authorized

Behavior:

Back textual above Header.

Header:
no action
no entity metadata

Hero:
name
→ statuses/context
→ edit
→ patrimônio
→ localização

All Data Pairs:
one column
label above value

Section actions:
after their context
stacked
no fixed bar

Button groups:
available width

Item links remain text.

Governance:
full-width

Observações:
full-width

History:
heading before actions
all preview items visible in normal flow

Upload:
stacked
contained

Height:
content-driven

No:
global horizontal overflow
nested vertical scroll

Existing shell mobile horizontal navigation remains inherited.

Its contained scroll does not authorize page overflow or shell changes.

======================================================================
16. SPACING CONTRACT
======================================================================

BACK_NAVIGATION_SPACING =
space-3 between Back and Header

Header → Hero =
Page Header margin space-6

PAGE_REGION_GAP =
section-gap = 20px

Between:
Hero
Main Data
Operation
Governance
History
Complementary Operations

SECTION_GAP =
section-gap = 20px between groups in same stack

SUBSECTION_GAP =
space-4 between heading and content

DATA_PAIR_GAP =
space-1 label/value
space-4 between pairs

ACTION_GAP =
space-2

Fields → operation actions =
space-4

HISTORY_FAMILY_SECTION_SPACING =
space-6

History items =
space-3

Internal history item content =
space-2

Upload field → submit =
space-3

Do not accumulate Section Heading margin-bottom + another gap for same spacing.

Heading outside pair grid.

Existing heading margin provides 16px to content.

Do not add Page Header margin + PAGE_REGION_GAP for same interval.

======================================================================
17. TYPOGRAPHY CONTRACT
======================================================================

BACK_NAVIGATION_STYLE =
text-secondary
weight-medium
color-action
DS focus

PAGE_TITLE_STYLE =
argos-page-title
existing clamp from 27px to page-title/34px

HERO_PRIMARY_STYLE =
text-kpi / 24px
weight-semibold
line-tight

HERO_SECONDARY_STYLE =
Data Pair
text-body values

SECTION_HEADING_STYLE =
Section Heading
text-section / 18px

SUBSECTION_HEADING_STYLE =
same Section Heading style
hierarchy via semantics + position

DATA_LABEL_STYLE =
Data Pair
text-label / 11px
weight-medium
ink-muted
line-height 1.25

DATA_VALUE_STYLE =
text-body / 14px
line-base
ink

META_STYLE =
text-secondary / 12px
ink-muted
line-base

EMPTY_VALUE_STYLE =
text-body
weight-regular
ink-muted

EMPTY_STATE_STYLE =
argos-state__copy
compact variant

Activity title =
text-body
weight-semibold
line-tight

No new typography scale.

EMPTY_VALUE_TOKEN_OR_COPY =
—

EMPTY_VALUE_VISUAL_TREATMENT =
muted text value
no badge
no icon
no box

EMPTY_VALUE_SEMANTICS =
absence according to current rendering predicates

Does NOT mean:
OFFLINE
OUT_OF_SCOPE
not applicable

Authority:
current template/projection already repeatedly uses —.

Preserve current filters/predicates.

Do not silently modify:
zero handling
catalog
domain state semantics

Empty marker does not need mono even in technical field.

Never replace actual status text with —.

======================================================================
18. DUPLICATION MATRIX
======================================================================

Columns:

Field
Role
Header
Hero
Main Data
Operation
History
Duplication

Inventário CFTV
Role = ACTION_CONTEXT
Header = Contexto
Duplication = NO_DUPLICATION

Detalhe da câmera
Role = ACTION_CONTEXT
Header = Title
Duplication = NO_DUPLICATION

Nome
Role = IDENTITY
Hero = Integral
Duplication = NO_DUPLICATION

Patrimônio
Role = IDENTITY
Hero = Integral
Duplication = NO_DUPLICATION

Fabricante
Role = IDENTITY
Main Data = Identificação
Duplication = NO_DUPLICATION

Modelo
Role = IDENTITY
Main Data = Identificação
Duplication = NO_DUPLICATION

Tipo
Role = IDENTITY
Main Data = Identificação
Duplication = NO_DUPLICATION

Serial
Role = TECHNICAL
Main Data = Identificação
Duplication = NO_DUPLICATION

MAC
Role = TECHNICAL
Main Data = Identificação
Duplication = NO_DUPLICATION

Terminal
Role = LOCATION
Hero = Summary
Main Data = Localização
Duplication = SUMMARY + FULL_DETAIL_ALLOWED

Ambiente
Role = LOCATION
Hero = Summary
Main Data = Localização
Duplication = SUMMARY + FULL_DETAIL_ALLOWED

Pavimento
Role = LOCATION
Main Data = Localização
Duplication = NO_DUPLICATION

Setor
Role = LOCATION
Main Data = Localização
Duplication = NO_DUPLICATION

Descrição detalhada
Role = LOCATION
Main Data = Localização
Duplication = NO_DUPLICATION

Ponto de referência
Role = LOCATION
Main Data = Localização
Duplication = NO_DUPLICATION

IP
Role = TECHNICAL
Main Data = Rede
Duplication = NO_DUPLICATION

Máscara
Role = TECHNICAL
Main Data = Rede
Duplication = NO_DUPLICATION

Gateway
Role = TECHNICAL
Main Data = Rede
Duplication = NO_DUPLICATION

VLAN
Role = TECHNICAL
Main Data = Rede
Duplication = NO_DUPLICATION

Farm
Role = TECHNICAL
Main Data = Gravação
Duplication = NO_DUPLICATION

Retenção esperada
Role = TECHNICAL
Main Data = Gravação
Duplication = NO_DUPLICATION

Codec
Role = TECHNICAL
Main Data = Gravação
Duplication = NO_DUPLICATION

Estado efetivo + contexto
Role = STATUS
Hero = Summary
Operation = Estado atual
Duplication = STATUS_REPETITION_JUSTIFIED

Situação
Role = STATUS
Hero = Summary
Operation = Situação
Duplication = STATUS_REPETITION_JUSTIFIED

Completude
Role = STATUS
Hero = Summary
Operation = Completude
Duplication = STATUS_REPETITION_JUSTIFIED

Último estado confirmado
Role = STATUS
Hero = may appear in stale factual context
Operation = integral
Duplication = STATUS_REPETITION_JUSTIFIED

Última evidência útil
Role = TECHNICAL
Operation = Monitoramento
Duplication = NO_DUPLICATION

Estado desde
Role = TECHNICAL
Operation = Monitoramento
Duplication = NO_DUPLICATION

Current outage opening/duration
Role = SUMMARY
Hero = duration in OFFLINE context if projected
Operation = integral
History = corresponding record
Duplication = SUMMARY + FULL_DETAIL_ALLOWED

Campos faltantes
Role = ADMINISTRATIVE
Operation = Situação/completude
Duplication = NO_DUPLICATION

Motivo da última desativação
Role = ADMINISTRATIVE
Operation = Situação/completude
Duplication = NO_DUPLICATION

Desativada em
Role = ADMINISTRATIVE
Operation = Situação/completude
Duplication = NO_DUPLICATION

Desativada por
Role = ADMINISTRATIVE
Operation = Situação/completude
Duplication = NO_DUPLICATION

Criado por
Role = ADMINISTRATIVE
Operation = Governança cadastral
Duplication = NO_DUPLICATION

Criado em
Role = ADMINISTRATIVE
Operation = Governança cadastral
Duplication = NO_DUPLICATION

Atualizado por
Role = ADMINISTRATIVE
Operation = Governança cadastral
Duplication = NO_DUPLICATION

Atualizado em
Role = ADMINISTRATIVE
Operation = Governança cadastral
Duplication = NO_DUPLICATION

Origem cadastral
Role = ADMINISTRATIVE
Operation = Governança cadastral
Duplication = NO_DUPLICATION

Observações cadastrais
Role = ADMINISTRATIVE
Operation = Governança cadastral
Duplication = NO_DUPLICATION

Demais dados de indisponibilidade
Role = HISTORICAL
History = Indisponibilidades
Duplication = NO_DUPLICATION

Dados de atividade
Role = HISTORICAL
History = Atividades
Duplication = NO_DUPLICATION

Papel/nomes/data de substituição
Role = HISTORICAL
History = Substituições
Duplication = NO_DUPLICATION

Código/resumo de auditoria
Role = HISTORICAL
History = Auditoria
Duplication = NO_DUPLICATION

Editar câmera
Role = ACTION_CONTEXT
Hero = Action
Duplication = NO_DUPLICATION

Ações de situação
Role = ACTION_CONTEXT
Operation = Actions
Duplication = NO_DUPLICATION

Ações de histórico
Role = ACTION_CONTEXT
History = Block/item
Duplication = NO_DUPLICATION

RATIONALES:

Terminal/Ambiente:
Hero orientation summary + full location detail.

Statuses:
Hero initial scan + Operation evidence/action context.

Stable label:
may explain stale UNKNOWN.

Current outage:
operational summary + chronological event.

Historical replacement names:
snapshots, not current identity duplicates.

Audit summaries:
may mention current data factually; never deduplicate history.

Any other repetition:

requires adjudication.

Default:
NO_DUPLICATION.

======================================================================
19. STATE MATRIX
======================================================================

Global:

same macro order
auto height
section surfaces NONE
fixed breakpoints

STATE = Dados completos

Layout stability =
same regions/destinations

Height =
content driven

Grid reflow =
viewport only

Action changes =
situation/permission only

Surface =
NONE

Overflow risk =
low

STATE = Opcionais vazios

Pairs preserved with marker.

Height may decrease.

No grid change.

No action change.

Surface NONE.

STATE = Conteúdo longo

Order preserved.

Association preserved.

Height changes.

Column count does NOT change based on content.

No action/surface changes.

Risk:
high if min-width/nowrap incorrect.

Required:
full wrapping.

STATE = Histórico vazio

Heading/actions preserved.

Lower height.

No grid reflow.

Permission-based action presence preserved.

Compact empty state.

No min-height.

STATE = Histórico preenchido

Same blocks/family.

Height grows naturally.

No grid change.

Item editing permission preserved.

Text/link wrap.

Limits 5/10 preserved.

STATE = PRODUCAO

Same operation layout.

Actions depending on permissions:

Substituir
Mover para Estoque
Desativar

No new availability rules.

STATE = ESTOQUE

Same operation layout.

Actions:

Colocar em Produção
Desativar

Technical state still from projection.

STATE = current reactivation branch

Same layout.

Action:
Reativar by current condition.

Do not redefine enum/domain branch.

STATE = Cadastro incompleto

Fields missing in same subsection.

Height may grow.

No grid change.

Fields-missing text full-width.

STATE = UNKNOWN / stale / out of scope

Same Hero/Monitoring.

Context may add lines.

No grid change.

Do not convert to OFFLINE.

Preserve qualifiers.

STATE = reduced permissions

Remaining blocks keep order.

Height changes from factual omission.

Hero action track auto disappears.

No placeholders for unauthorized action/block.

STATE = destructive action unavailable

Same subsection.

Potentially lower height.

Action wrap may change.

No disabled new button.

STATE = upload authorized

Complementary Operations present last.

Form follows breakpoint.

Submit present.

Filename contained.

STATE = upload unauthorized

Entire Complementary Operations region absent.

No empty heading.

Warnings/messages from shell may move page vertically.

Do not hide warnings to satisfy fold expectations.

======================================================================
20. ACCESSIBILITY CONTRACT
======================================================================

H1 =
Detalhe da câmera

H2 =
camera name
Dados principais
Operação
Governança cadastral
Histórico
Operações complementares when present

H3 =
Identificação
Localização
Rede
Gravação
Monitoramento técnico
Situação e completude
the four History headings
Enviar imagem manualmente

Activity item titles:
strong text
not H3

If semantically articles/subsections:
H4 allowed
never parallel H3 just for styling

DESCRIPTION_LIST_RULE =

Data Pairs describe entity properties.

Use:
dl
dt
dd

with valid grouping.

Do NOT apply dl to:
actions
upload
entire chronological lists.

FOCUS_ORDER =
DOM reading order

No positive tabindex.

No CSS order that reverses action/read order.

ACTION_SEMANTICS =

navigation = <a>
upload submit = <button type="submit">

STATUS_SEMANTICS =
existing textual labels
static badges
no new live region

COLOR_ONLY_INFORMATION =
PROHIBITED

Monitoring context must remain readable outside tooltip.

Preserve:
skip link
conteudo-principal

Preserve:
camera-detail-title

Preserve:
label for="imagem-camera"

DS focus visible.

Do not clip outline.

Repeated "Ver histórico completo" links:
accessible name associated with relevant block heading
without changing visible copy.

Mobile buttons:
DS target size.

Auxiliary links:
sufficient clickable space via spacing
without making them new buttons.

======================================================================
21. FUNCTIONAL PROTECTION MATRIX
======================================================================

BACK NAVIGATION

Current mechanism:
link cameras:lista

Markup may move:
YES

Must preserve:
label
fixed destination
GET
no new parameters

EDIT

Current:
authorized link to form

May move:
YES

Must preserve:
change_camera
PK
destination GET/POST flow

OPERATIONAL GOVERNANCE

Current:
links to confirmation pages

May move:
YES

Must preserve:
conditions by situation/permission
routes
destination confirmation

PERMISSIONS

Current:
template + view decorators/checks

May markup move:
YES

Must preserve:
exact visibility/access facts

CSRF

Current:
upload token
destination forms

May move:
YES

Must preserve:
token + POST
no link-based submission

ACTIVITIES

Current:
camera query [:10]

May move:
YES

Must preserve:
isolation
order
type
preview
existing truncation
editing permission
PK

REPLACEMENTS

Current:
query where camera is previous/replacement [:10]

May move:
YES

Must preserve:
permission
role
historical snapshot names
item.pk links

OUTAGES

Current:
MonitoringReadService.history_page(limit=5)

May move:
YES

Must preserve:
technical source
limit
order
dates
duration
origin
closure

AUDIT/EVENTS

Current:
permission-conditioned query [:10]

May move:
YES

Must preserve:
permission
code
summary
eventos:detalhe(evento.pk)

UPLOAD

Current:
native multipart POST form

May move:
YES

Must preserve:
action
method
enctype
CSRF
ID
name
required
accept
messages

STATUS

Current:
situation/completeness labels

May move:
YES

Must preserve:
meaning
conditions
texts

MONITORING

Current:
_monitoramento_ui projection

May move:
YES

Must preserve:
effective
stable
freshness
context

No probes in browser/request.

FORMS

Current:
upload local;
others on destination

Must preserve:
do not bring governance/edit forms into detail page.

IDs

camera-detail-title
imagem-camera
inherited main ID

May move:
YES

Values/references preserved.

data-* =
none locally

Do not introduce interaction/hook.

JS hooks =
none

Do not create JS.

URLs =
Django {% url %}

Preserve:
namespace
route name
identity

History activity link:
do not hide with a new view_atividadecamera template condition.

Shared shell =
NO changes.

Quick Detail =
NO changes.

P3-B / Activity Create =
NO changes.

Moving markup never authorizes changing:
queries
services
forms
models
endpoints

======================================================================
22. FILE OWNERSHIP PLAN
======================================================================

EXPECTED FUTURE S2B FILES:

cameras/templates/cameras/detalhe.html

Responsibility:
regions
headings
field destinations
DS consumption
actions
page CSS include

cameras/templates/cameras/partials/_monitoring_badge.html

Responsibility:
opt-in adoption of existing DS variants
for Camera Detail only

cameras/templates/cameras/partials/_atividade_tipo_badge.html

Responsibility:
opt-in use of existing Badge
for Detail only

static/css/ui-v2/camera-detail.css

New file.

Responsibility:
page composition only

grids
spacing
spans
responsive rules already closed

cameras/test_frontend.py

Responsibility:
semantic structure
associations
routes
protected-consumer preservation

EXPECTED_SHARED_DS_FILES =
NONE

EXPECTED_JS_FILES =
NONE

EXPECTED_BACKEND_FILES =
NONE

EXPECTED_EXISTING_GLOBAL_CSS_CHANGES =
NONE

Page CSS restricted to Camera Detail wrapper and composition layer.

Use namespace:
argos-

Do NOT create:
primitive
component
variant
token
copy of shared patterns

Both partials are DOMAIN partials, not DS files.

Opt-in behavior:

ui_v2_badges=True

passed only by Detail.

Without argument:
current markup/presentation remains unchanged.

Do not create duplicate partial.

Preserve:
content
conditions

In opt-in branch:
consume existing DS classes and mappings from Operation/History.

Do NOT redefine components in local CSS.

Load Camera Detail CSS in consumer template after legacy sheets.

Do NOT modify:

base.html
production.css
inventario.css
governanca.css
route gate

TESTS TO RUN IN S2B:

monitoring UI
governance views
activities
audit views
image upload
frontend
Quick Detail regression
P3-B regression when partials change

Test extensions validate:
data preservation
permissions
links
partial isolation

Do not replicate CSS declarations in tests.

If implementation requires:
shared DS override
or shared DS file change

then:

S2A_STATUS =
BLOCKED_BY_DS_CHANGE

STOP.

======================================================================
23. VISUAL ACCEPTANCE CONTRACT
======================================================================

VIEWPORTS =

1920×1080
1440×900
1366×768
900×900
390×844

ZOOM =
100%

CONTENT_DRIVEN_HEIGHT =
REQUIRED

CONTENT_DRIVEN_COMPOSITION =
REQUIRED

1920×1080

ABOVE_THE_FOLD_MINIMUM_EXPECTATION:

Back
Header
Hero fully visible with ordinary content

Identity
statuses
authorized edit
perceptible

Main Data materially visible

Desktop grids

History/upload later in flow.

1440×900

Back/Header/Hero

Start of Main Data

Operational context understood from Hero.

Same desktop grids.

No artificial elevation of History/upload.

1366×768

Identity/status/edit available in initial region.

Hero materially visible.

Start of Main Data when content height allows.

Do NOT require complete Operation/History in fold.

900×900

Back/Header/Hero.

Identity + statuses.

Start of Identificação.

Main Data + Operation stacked.

Pairs remain two columns.

390×844

Back/Header + essential Hero portion.

Name/status/edit precede patrimônio/localização and extensive data.

One column.

Mobile heading/action order.

Upload last.

ESSENTIAL_INFORMATION_VISIBLE =

identity
monitoring label
situation
completeness

in initial Hero region.

PRIMARY_ACTION_AVAILABLE =

authorized Edit without reveal interaction/menu.

Test:
ordinary content
+
State Matrix variations.

Exceptional long content or inherited messages may increase height.

Do not:
truncate data
hide warning
force fixed heights
only to satisfy fold.

Instead verify:
identity
statuses
action

remain early in flow before extensive data.

GLOBAL CRITERIA:

GLOBAL_HORIZONTAL_OVERFLOW =
NONE

Evidence:
document scroll width <= viewport
except rounding tolerance

NESTED_VERTICAL_SCROLL =
NONE

No Camera Detail region with limited height + own vertical scroll.

PRIMARY_IDENTITY_CLEAR =
YES

One current name in Hero.
Associated with camera-detail-title.

OPERATIONAL_STATUS_CLEAR =
YES

Three status concepts identifiable by text.
Technical context preserved.

CARD_FRAGMENTATION_REDUCED =
YES

Zero cards/surfaces for sections/items.

COLORED_HEADER_REPETITION =
REDUCED

Zero colored backgrounds/bands in section headings.

LABEL_VALUE_ASSOCIATION =
CLEAR

Label immediately above value with Data Pair gap.

CONTENT_DENSITY =
CONTROLLED

Use planned tokens.
No decorative min-height.
No equal-height columns.

EMPTY_STATES =
COMPACT

Current copies.
No dedicated:
padding
surface
icon
min-height

ACTIONS =
HIERARCHICALLY_CLEAR

Actions present in defined locations.
At most one Primary per region.

LONG_CONTENT =
STABLE

Full content inside track.
No:
overlap
clipping
new ellipsis

PERMISSION_VARIATION =
STABLE

Missing actions/blocks follow current permissions.
No reserved empty spaces.

NO_INFORMATION_LOST =
YES

Every inventory field has a destination.

Only explicitly approved duplicate occurrences removed.

RESPONSIVE_TRANSITION =
PASS

899/900/901 verify transition.

680px verifies mobile stack.

FUNCTIONAL_PROTECTION =
PASS

Links
IDs
upload
permissions

preserved by inspection/tests.

Validate:
empty
filled
long content
situations
completeness
technical states
reduced permissions

No claim of human visual approval based on tests only.

VISUAL_RUNTIME_VALIDATION_THIS_ACTIVITY =
NOT_PERFORMED

VISUAL_PROTOTYPE_DEPENDENCY =
NONE / material design decisions can be statically closed

Future rendered validation checks compliance.

Executor gets no redesign authority.

======================================================================
24. IMPLEMENTATION FREEDOM MATRIX
======================================================================

CLOSED =

macro order
Back
Header
Hero
all field destinations
grids
proportions
Governance position
History order
action positions
action variants
surfaces
dividers
breakpoints
mobile stack
duplication decisions
empty value behavior
density
typography
spacing
preview limits
badge visual mappings

LOCAL_IMPLEMENTATION_FREEDOM =

equivalent CSS declaration order

internal non-public naming

reuse of existing helper

technically equivalent implementation only if it preserves exactly:
semantics
reading order
visual contract
functional contract

STOP_AND_ESCALATE =

any requirement to modify:

content
permission
state
route
form
preview limit
interaction
Design System
token
shared pattern
proportion
breakpoint
surface
material visual decision not covered

Do not use local freedom to "adjust visually":

grid
padding
action position
density
order

If rendered implementation reveals material incompatibility:

report finding
request adjudication

Do NOT silently redesign.


======================================================================
25. LEGACY PRESENTATIONAL CLASS MIGRATION CONTRACT
======================================================================

OBJECTIVE =
A Camera Detail V2 NÃO deve ser implementada por meio de overrides visuais
compensatórios sobre a composição legada.

RULE 1 — REMOVE PRESENTATIONAL DEPENDENCY
O template da Camera Detail deve deixar de consumir classes legadas cuja
responsabilidade seja exclusivamente:
- card/surface da implementação antiga;
- colored section header;
- grid 50/50 antigo;
- detail panel antigo;
- decorative divider;
- legacy empty-state surface;
- layout/spacing específico da composição antiga.

RULE 2 — NO COMPENSATING OVERRIDES
Não manter classe visual legada no DOM apenas para neutralizá-la depois em
static/css/ui-v2/camera-detail.css.

RULE 3 — PAGE CSS OWNERSHIP
camera-detail.css pode conter apenas responsabilidades de Page Composition:
- layout;
- grid;
- proportions já fechadas;
- spans;
- alignment;
- positioning;
- responsive composition;
- spacing usando tokens existentes.

RULE 4 — NO LOCAL DS REIMPLEMENTATION
camera-detail.css NÃO pode redefinir localmente:
- Data Pair;
- Data Group;
- Button;
- Badge;
- Compact Empty State;
- Page Header;
- Section Heading;
- tokens;
- foundation;
- shared pattern.

RULE 5 — LEGACY CLASS CLASSIFICATION
Antes de remover uma classe consumida pela Camera Detail, classificar:

LEGACY_CLASS =
OWNERSHIP =
PRESENTATIONAL | FUNCTIONAL | SHARED_VALID
USED_BY_JS =
YES | NO
USED_BY_TEST =
YES | NO
USED_BY_OTHER_SCREEN =
YES | NO
SAFE_TO_REMOVE_FROM_CAMERA_DETAIL =
YES | NO

RULE 6 — PRESERVE FUNCTIONAL CONTRACTS
Classes/hooks/IDs necessários para JavaScript, testes, semântica, permissões,
acessibilidade ou contratos compartilhados legítimos devem ser preservados.

RULE 7 — DEAD LEGACY CSS CLEANUP IS OUT OF SCOPE
Regras antigas podem permanecer fisicamente em arquivos CSS legados se deixarem
de ser consumidas pela Camera Detail. Não fazer cleanup global de dead CSS em
S2B.

RULE 8 — SPECIFICITY ESCALATION PROHIBITED
Se a implementação exigir !important, specificity artificialmente crescente,
selector chain compensatório, override local de componente do DS ou neutralização
de legacy card/component para cumprir o contrato:

STOP_AND_ESCALATE.

Não realizar patch/workaround.

EXPECTED_END_STATE =
CAMERA_DETAIL_LEGACY_PRESENTATIONAL_CLASS_DEPENDENCY = NONE
PAGE_SPECIFIC_CSS_ROLE = COMPOSITION_ONLY
SHARED_DS_OVERRIDE = NONE
SPECIFICITY_ESCALATION = NONE

======================================================================
ESTADO E LIMITES DE IMPLEMENTAÇÃO
======================================================================

CAMERA_DETAIL_ARCHITECTURE_CONTRACT = APPROVED / CANONICAL
CAMERA_DETAIL_IMPLEMENTATION = NOT_STARTED
CAMERA_DETAIL_VISUAL_RUNTIME_VALIDATION = NOT_PERFORMED
CAMERA_DETAIL_USER_VISUAL_APPROVAL = PENDING
S2B_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
NEXT_REQUIRED_ACTIVITY = P5-VR-S2B — Camera Detail Implementation
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION

ACTIVITY_SCOPE = DOCUMENTATION / CANONICALIZATION ONLY
SOURCE_CODE_CHANGED = NO
DESIGN_SYSTEM_CHANGED = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED

## P5-VR-DSG-02 implementation binding

This additive Design System binding materializes the already approved
`BACK_NAVIGATION_STYLE` from section 17 without reopening its visual decision:

```text
BACK_NAVIGATION_PUBLIC_CAPABILITY = .argos-back-link
BACK_NAVIGATION_IMPLEMENTATION = shared pattern in static/css/ui-v2/patterns.css
BACK_NAVIGATION_STYLE = --argos-text-secondary / --argos-weight-medium / --argos-color-action / global :focus-visible
```

The Camera Detail consumer migration remains within its separately authorized
implementation activity. Position, copy, destination, semantics, spacing, and
hierarchy remain as specified above.


## 26. S2A-R3 — Macro grouping / DSG-SURFACE-01 (2026-10-06)

Finding confirmado: `INSUFFICIENT_MACRO_VISUAL_GROUPING`. Este contrato revisa
as decisões anteriores de surface NONE para as quatro macro regiões, inclusive
as seções 10 e 11 e referências repetidas nos contratos de cada região.

```text
DESIGN_SYSTEM_VERSION = 2.4.0 / IMPLEMENTED_LOCALLY / NOT_PUBLISHED
DSCR = DSCR-UIV2-006-SECTION-SURFACE-2.4.0
PUBLIC_CAPABILITY = argos-section-surface / patterns layer
DADOS_PRINCIPAIS_SURFACE = ONE
OPERACAO_SURFACE = ONE
GOVERNANCA_CADASTRAL_SURFACE = ONE
HISTORICO_SURFACE = ONE / all history subgroups in the same macro surface
HERO_SURFACE = NONE
NESTED_SURFACES = NONE
UPLOAD_SURFACE = NONE / optional supporting compact surface not adopted
PAGE_SPECIFIC_CSS_ROLE = COMPOSITION_ONLY
TOKENS_NEW = NONE
SHADOW = NONE
COLORED_HEADER = NONE
ACCENT_BAR = NONE
GRADIENT = NONE
BREAKPOINTS = existing 900 / 680 / 600 only
JS_CHANGED = NO
BACKEND_CHANGED = NO
HUMAN_VISUAL_APPROVAL = PENDING
```

A capability define somente fundo `--argos-color-surface`, borda
`--argos-border-width` solid `--argos-color-border`, raio
`--argos-radius-surface` e padding base `--argos-space-6`.
Sem variante local, override compartilhado ou aumento de especificidade.

Identificação, Localização, Rede, Gravação, Monitoramento técnico, Situação e
completude, Indisponibilidades, Atividades, Substituições e Auditoria ficam sem
surfaces próprias. Itens de histórico e estados vazios também ficam sem surface.
A borda sutil externa das quatro macro surfaces é a única nova borda autorizada;
dividers continuam NONE. Hero permanece sem surface.

O pedido atual autoriza esta remediação e sua documentação, sem staging, commit
ou push. Preservar conteúdo, ações, rotas, permissões, CSRF, forms, IDs, atributos
de dados, upload, ordenação e limites de histórico, monitoramento, Quick Detail
e P3-B. Resultado técnico máximo: TECHNICAL_READY_FOR_HUMAN_VISUAL_REVIEW.

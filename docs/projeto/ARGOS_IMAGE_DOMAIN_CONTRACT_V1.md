# ARGOS — Contrato Canônico do Domínio de Imagens v1

STATUS = CANONICAL
DOCUMENT_TYPE = IMAGE_DOMAIN_CONTRACT
VERSION = 1
LANGUAGE = pt-BR
ACTIVITY = FASE C / IMG-01
ACTIVITY_STATUS = COMPLETE / DOCUMENTAL
EFFECTIVE_DATE = 2026-09-24
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_DOCUMENT
ROADMAP_AUTHORITY = docs/projeto/ROADMAP_ARGOS_V5.md
SPRINT_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md
RELATED_UI_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
RELATED_ARCHITECTURE = docs/projeto/03_arquitetura.md
RELATED_ARCHITECTURAL_DECISIONS = docs/projeto/07_decisoes_arquiteturais.md
RELATED_ADR_019 = docs/projeto/ADR-019_monitoramento_disponibilidade_gestao_imagens.md
RELATED_ADR_020 = docs/projeto/ADR-020_contrato_estado_tecnico_monitoramento.md
RELATED_SECURITY_AUTHORITY = docs/projeto/ADR-021_seguranca_capacidade_monitoramento.md

## 1. Finalidade, autoridade e limites

Este documento transforma IMG-01 em contrato de domínio para IMG-02 a IMG-09 e
para consumidores de imagem, em especial Inventário e CameraQuickDetailPanel. Define os
significados, invariantes, consultas, estados observáveis e requisitos que as
slices de implementação devem preservar. Em conflito sobre o domínio de
imagens, esta é a authority canônica; ADR-019 continua governando a separação
entre monitoramento e imagens, ADR-020 continua governando o estado técnico da
câmera, ADR-021 continua governando a fronteira de segurança de equipamentos,
e SPRINTS_ARGOS_V5.md continua governando ordem, Integration Gate e vertical
slices. A arquitetura e as decisões arquiteturais vigentes continuam válidas
como contexto, sem prescrever aqui backend ou implementação.

O contrato é documental. Não cria modelo Django, migration, storage concreto,
fila, worker, upload, captura, endpoint, permissão executável, UI nem política
de retenção implementada. A aprovação deste documento não concede autorização
automática para implementar IMG-02 ou outra slice.

## 2. Vocabulário e regras de interpretação

- CameraImageRecord é o registro lógico persistente de uma imagem associada a
  uma câmera, independentemente do backend que guarda seus bytes.
- Proveniência descreve como o ARGOS obteve a imagem; não é inferida pelo nome
  do arquivo, por metadados EXIF ou pela imagem visual.
- Captura corrente é escolhida antes de avaliar se seus bytes podem ser
  apresentados. Indisponibilidade, corrupção ou falha de validação não
  autorizam substituir silenciosamente a captura corrente por outra antiga.
- Uma decisão marcada como OPEN_DECISION continua sem valor fixado. A futura
  slice responsável deve obter adjudicação explícita quando a escolha alterar
  produto, segurança, persistência ou UX.
- Nomes conceituais deste contrato não prescrevem nomes de classes/campos,
  enums de código, tecnologia, schema ou API.

## 3. IMAGE_ENTITY_CONTRACT

### 3.1 CameraImageRecord

CameraImageRecord representa um objeto de imagem e seus fatos de domínio. Cada
registro pertence a exatamente uma câmera; uma câmera pode ter zero ou muitos
registros. O registro deve permitir recuperar, com autorização, ao menos:

- identidade imutável e estável, usada também como último desempate da ordenação;
- câmera proprietária;
- proveniência;
- autoria de quem iniciou a operação e identidade de serviço que a executou,
  quando forem identidades distintas;
- captured_at, quando há uma captura real, e recorded_at, quando o ARGOS
  registrou o resultado;
- referência opaca ao objeto armazenado, sem expor caminho físico ou URL
  pública;
- estado de validação/integridade e disponibilidade necessário para distinguir
  objeto apresentável, indisponível e conhecido como inválido;
- lifecycle que permita retirar logicamente um registro do estado corrente sem
  confundir essa ação com remoção física ou expurgo.

O registro é metadado de domínio; não é a imagem binária. Proveniência,
identidade e tempos que explicam o fato histórico não podem ser reescritos para
fazer um upload parecer captura ou para reordenar silenciosamente o passado.
Correção, substituição ou expurgo deve preservar a rastreabilidade e obedecer
ao lifecycle aprovado. A política de retenção e expurgo permanece aberta.

CameraImageRecord não contém, por este contrato, campo ou regra de imagem
principal. PRIMARY_IMAGE é independente e está DEFERRED_TO_IMG07.

### 3.2 Lifecycle lógico

Um registro retirado logicamente do estado corrente deixa de participar de
LATEST_CAMERA_CAPTURE_RECORD. A retirada não equivale a apagar o fato da
história nem define por si só se o item continuará visível no histórico. O
histórico aplica suas permissões e a política de retenção que vier a ser
adjudicada. Exclusão física, retenção, expurgo e restauração não são definidos
nesta versão.

## 4. PROVENANCE_CONTRACT

Somente estas proveniências estão inicialmente autorizadas:

| Proveniência | Significado canônico |
|---|---|
| CAPTURA_CAMERA | Imagem obtida diretamente do equipamento por fluxo de captura explícito, autorizado e executado pelo ARGOS. |
| UPLOAD_MANUAL | Arquivo fornecido manualmente por um usuário autorizado e validado pelo backend. |

UPLOAD_MANUAL != CAPTURA_CAMERA. UPLOAD_MANUAL não comprova captura direta,
data de captura, câmera de origem ou autenticidade do conteúdo. Nome, EXIF,
timestamp do cliente, associação a uma câmera ou aparência visual não mudam a
proveniência. Nenhuma outra proveniência será criada por inferência nesta
atividade.

A proveniência é definida pelo fluxo backend que aceitou o registro e fica
disponível às leituras autorizadas e à auditoria. Falha, retry ou ausência de
imagem não deve produzir um CameraImageRecord com proveniência fictícia.

## 5. TIMESTAMP_CONTRACT

- captured_at representa o instante em que a imagem foi efetivamente obtida da
  câmera. É obrigatório e produzido pelo fluxo confiável de CAPTURA_CAMERA.
- recorded_at representa o instante em que o ARGOS aceitou e registrou o
  CameraImageRecord. É produzido pelo ARGOS, não pelo browser nem pelo nome ou
  metadado não confiável do arquivo.
- Os dois instantes são fatos diferentes e não devem ser substituídos um pelo
  outro. Persistência deve preservar instantes timezone-aware e ordenáveis; a
  apresentação segue a configuração de fuso do ARGOS
  (atualmente America/Sao_Paulo).
- Um upload manual não ganha captured_at presumido. Se metadado original do
  arquivo for conservado no futuro, permanece dado declarado/não verificado,
  não substitui captured_at e não o torna elegível para LATEST_CAMERA_CAPTURE.
- Para CAPTURA_CAMERA, ausência ou invalidade de captured_at é violação do
  contrato e não pode ser corrigida descartando silenciosamente o registro e
  promovendo uma captura anterior.

Valores concretos de representação, precisão e constraints de schema pertencem
a IMG-02.

## 6. AUTHORSHIP_CONTRACT

Autoria identifica a pessoa autorizada que iniciou a captura ou enviou o
arquivo. O executor técnico (por exemplo, worker) é identidade separada quando
não for a mesma pessoa. Fluxos automatizados explicitamente autorizados
registram identidade de serviço e motivo operacional; não atribuem a ação a
uma pessoa que não a iniciou.

Autoria deve sobreviver às leituras autorizadas e aos eventos de auditoria
relevantes. Credenciais, tokens, senhas, master keys e outros segredos nunca
são autoria nem metadado publicável. Formato de referência de usuário/serviço
e política de preservação após desativação de conta serão decididos na
implementação e auditoria, sem apagar o fato histórico.

## 7. LATEST_CAMERA_CAPTURE_CONTRACT

### 7.1 Seleção canônica do registro

LATEST_CAMERA_CAPTURE_RECORD(camera) seleciona o registro antes de avaliar
integridade, validade dos bytes ou disponibilidade do objeto:

1. considerar registros pertencentes à câmera consultada;
2. considerar somente provenance = CAPTURA_CAMERA;
3. excluir registros retirados logicamente do estado corrente;
4. ordenar, nesta ordem, por captured_at DESC, recorded_at DESC,
   immutable_id DESC;
5. selecionar o primeiro registro corrente;
6. somente então determinar o estado de apresentação/recuperação desse
   registro.

immutable_id é um desempate estável, imutável e total. Backend e banco deverão
implementar a mesma ordenação, inclusive a semântica de nulos; registros
CAPTURA_CAMERA válidos sempre possuem captured_at.

Não filtrar previamente por objeto disponível, arquivo decodificável, hash
válido ou estado AVAILABLE. Esses fatores determinam o resultado do registro
selecionado; não alteram qual registro é o mais recente.

### 7.2 Resultado do registro selecionado

| Resultado da seleção e recuperação | Resultado canônico |
|---|---|
| Não existe registro corrente elegível | NO_CAPTURE_AVAILABLE |
| O registro mais recente é válido, íntegro e seus bytes estão disponíveis | AVAILABLE |
| O registro mais recente é válido e íntegro, mas o objeto está temporariamente indisponível | UNAVAILABLE |
| O registro mais recente é conhecido como corrompido ou inválido | ERROR |

DO_NOT_FALL_BACK_SILENTLY_TO_OLDER_CAPTURE = YES.

Uma captura anterior nunca será apresentada como a captura mais recente porque
a atual está ausente do storage, inacessível, corrompida ou inválida. Para
ERROR ou UNAVAILABLE, a leitura pode informar que existem itens anteriores no
histórico, sujeito a permissão, mas deve preservar o estado da captura corrente
e não substituir seus bytes pela imagem antiga.

### 7.3 Registro versus view

É permitido nomear separadamente:

- LATEST_CAMERA_CAPTURE_RECORD: resultado determinístico da seleção de domínio;
- LATEST_CAMERA_CAPTURE_VIEW: projeção autorizada do resultado, estado e
  conteúdo recuperável.

A view não pode aplicar fallback que mude o registro selecionado. Falha de
leitura, permissão ou storage deve ser representada de forma explícita e
sanitizada; não deve parecer ausência de registros quando há um registro
corrente conhecido.

## 8. PRIMARY_IMAGE_CONTRACT

PRIMARY_IMAGE != LATEST_CAMERA_CAPTURE.

PRIMARY_IMAGE é uma decisão de produto independente; sua existência, semântica,
seleção e lifecycle estão DEFERRED_TO_IMG07. Este contrato não cria atributo,
relação, flag, campo, API ou regra de implementação para PRIMARY_IMAGE.
CameraQuickDetailPanel preserva LATEST_CAMERA_CAPTURE como leitura canônica e
consome DISPLAY_IMAGE para apresentação, conforme a seção 25. Não usa
PRIMARY_IMAGE como substituto.

## 9. IMAGE_HISTORY_CONTRACT

O histórico contém múltiplos CameraImageRecord da câmera, sujeito à autorização
do leitor, ao lifecycle e à política de retenção que será definida. Deve
preservar e apresentar a proveniência sem converter UPLOAD_MANUAL em captura.
Registros anteriores podem ser consultados mesmo quando a captura corrente
está UNAVAILABLE ou ERROR, mas a UI deve identificá-los como históricos e não
como LATEST_CAMERA_CAPTURE.

A leitura histórica expõe apenas metadados e previews para os quais o usuário
tenha permissão e que estejam disponíveis/validados. Resultado, ordem,
paginação, limites de volume e comportamento após expurgo devem ser
determinísticos e definidos na slice que implementar o histórico. A leitura do
histórico não pode ser usada como fallback oculto da leitura latest.

## 10. CAPTURE_REQUEST_CONTRACT

Captura exige ação explícita de usuário ou fluxo de serviço explicitamente
autorizado, associada à câmera escolhida e a uma identidade iniciadora. Abrir,
fechar ou trocar CameraQuickDetailPanel, renderizar a tela, consultar status,
executar probe, mudar ONLINE/OFFLINE ou retentar monitoramento não solicita
captura.

O pedido é uma intenção operacional distinta do CameraImageRecord. Deve ser
possível correlacionar pedido, executor, câmera e resultado sem guardar
segredos. Somente captura concluída e validada pode criar registro
CAPTURA_CAMERA. Falha, timeout, cancelamento ou recusa deve produzir resultado
operacional/auditável conforme IMG-08/IMG-09, sem imagem falsa, sem sobrescrever
registro anterior e sem alterar disponibilidade técnica da câmera.

O processo de captura opera fora do ciclo de renderização HTTP e não pode
bloquear o monitoramento. Protocolo, worker, fila, concorrência, timeout,
retry, deduplicação e estados transitórios do pedido não são escolhidos aqui.

## 11. UPLOAD_CONTRACT

Upload é ação explícita de usuário autorizado e sempre produz provenance =
UPLOAD_MANUAL. O backend é responsável por validar o conteúdo real recebido
antes de aceitá-lo e disponibilizá-lo como CameraImageRecord. Extensão, nome de
arquivo, Content-Type declarado pelo cliente, EXIF e validação apenas no
browser não são prova suficiente.

Upload rejeitado não cria registro de imagem disponível. Upload aceito mantém
autoria do usuário, recorded_at do ARGOS, referência privada e proveniência
UPLOAD_MANUAL. Não recebe captured_at de câmera nem pode ser apresentado como
captura de equipamento.

MIME permitido, limites de bytes/dimensões, política para imagens animadas,
re-encoding e metadados retidos permanecem OPEN_DECISIONS. O uso de
UPLOAD_MANUAL como fallback exclusivamente de apresentação, quando não existe
captura corrente, está adjudicado pela política DISPLAY_IMAGE da seção 25.
O upload mantém sua proveniência e nunca passa a ser captura ou evidência de
monitoramento.

## 12. STORAGE_REQUIREMENTS

Qualquer backend escolhido deve satisfazer:

- manter bytes privados e acessíveis somente por caminho autorizado;
- associar referência opaca e estável aos metadados do registro;
- não expor caminho local, bucket, chave interna ou URL duradoura/pública ao
  browser ou em mensagens;
- permitir detectar referência sem objeto e objeto temporariamente
  indisponível sem selecionar imagem antiga como substituição;
- preservar associação da imagem ao registro/câmera e suportar múltiplos itens;
- proteger confidencialidade, integridade, disponibilidade e recuperação
  compatíveis com o risco operacional;
- permitir lifecycle, auditoria e retenção sem apagar silenciosamente a
  proveniência e autoria.

O contrato não escolhe armazenamento local, filesystem, objeto remoto ou banco,
produto/provedor, layout de chaves, replicação, backup ou política de
recuperação. IMG-02 deve estabelecer, antes da migration, um contrato
persistente de storage e uma abstração configurável para referência opaca e
acesso autorizado. A escolha do backend definitivo de produção permanece
OPEN_DECISION e não é pré-requisito para a migration. As decisões de backend
definitivo, replicação, backup e recuperação ficam diferidas para a arquitetura
de storage/produção.

## 13. VALIDATION_REQUIREMENTS

Validação é backend-side e em camadas: autorização da ação, formato/conteúdo
real, limites adjudicados, decodificação segura, consistência do registro,
referência de storage e estado de integridade. Somente conteúdo validado pode
ser marcado AVAILABLE ou servido como preview/download.

Falha de validação resulta em rejeição explícita para upload ou ERROR quando um
registro de captura já persistido for conhecido como inválido. Falha de
validação nunca apaga o histórico nem permite fallback silencioso. Regras
quantitativas de MIME, tamanho e dimensões permanecem OPEN_DECISION para
IMG-03/IMG-08; o mecanismo concreto de verificação e integridade deve ser
definido antes de declarar imagem disponível.

## 14. SECURITY_REQUIREMENTS

- Todas as operações de escrita, captura, leitura de metadados e acesso a bytes
  exigem autorização explícita e escopo por câmera/ação.
- Storage e previews são privados. A aplicação verifica permissão antes de
  revelar metadados ou emitir conteúdo; referência opaca não substitui
  autorização.
- Arquivos são entrada não confiável: validar no backend, limitar consumo,
  impedir interpretação/execução indevida e evitar traversal, exposição de
  caminhos e conteúdo ativo.
- Senhas, tokens, URLs autenticadas, chaves e conteúdo sensível não aparecem
  em logs, erros, auditoria, traces, HTML ou argumentos de processo.
- Falhas externas e detalhes de storage são sanitizados para o consumidor;
  diagnóstico operacional pode usar identificadores/categorias não secretos.
- Captura só acessa destinos autorizados a partir de configuração de domínio e
  política de rede. Browser não fornece URL/IP/porta arbitrários. Validações da
  conexão devem ocorrer no executor e na infraestrutura, conforme ADR-021.
- Privilégio de monitoramento não concede privilégio de captura. Credencial ou
  perfil de monitoramento só pode ser reutilizado após decisão explícita e
  autorização própria para captura; essa decisão permanece aberta.
- Segregar identidade humana iniciadora da identidade de serviço executora;
  aplicar least privilege e segregação por ambiente.
- Operações privilegiadas e alterações de configuração que ampliem a fronteira
  de segurança exigem governança, identidade autorizada e auditoria.

Estes requisitos complementam ADR-019, ADR-021 e as authorities de segurança
do ARGOS; não alteram os gates ambientais vigentes.

## 15. AUDIT_REQUIREMENTS

Auditar, com autoria e sem conteúdo secreto: pedido de captura e seu resultado
(inclusive falha/cancelamento quando houver ator/ação), aceite ou rejeição de
upload, alterações de lifecycle/retirada, mudanças de configuração privilegiada
e ações administrativas de retenção/expurgo. Eventos devem identificar câmera,
proveniência quando há registro, ator iniciador, executor quando aplicável,
instante, resultado e referência não sensível suficiente para correlação.

Eventos de auditoria são fatos históricos e seguem a imutabilidade definida
para o ARGOS. Não copiar bytes, senha, token, URL autenticada, ciphertext
exportável ou caminho sensível para a auditoria. A política de auditoria para
leitura/download humano, retenção de eventos e categorias exatas será fechada
em IMG-08 sem criar evento funcional por probe normal de monitoramento.

## 16. MONITORING_SEPARATION_CONTRACT

CAMERA_AVAILABILITY != IMAGE_CAPTURE_SUCCESS.

CAPTURE_PROCESSING != MONITORING_PROBE_PROCESSING.

Falha, lentidão, timeout, indisponibilidade de storage ou fila de captura não
altera automaticamente ONLINE/OFFLINE, elegibilidade, freshness, incidente ou
histórico de monitoramento. Monitoramento e captura usam caminhos de execução,
resultados, telemetria e permissões logicamente separados. A indisponibilidade
do subsistema de imagens não pode bloquear worker, scheduler, leituras ou
transições do monitoramento. ADR-021 proíbe herdar implicitamente privilégio ou
credenciais de monitoramento para captura.

## 17. READ_CONTRACTS

1. LATEST_CAMERA_CAPTURE(camera, principal) aplica a seleção da seção 7,
   autorização de leitura, resultado explícito e metadados mínimos necessários
   ao consumidor. Só CAPTURA_CAMERA participa.
2. IMAGE_HISTORY(camera, principal, page/limit) consulta o mesmo conjunto
   canônico CameraImageRecord, aplica autorização e lifecycle, mantém
   proveniência e retorna itens históricos sem alterar o resultado latest.
3. IMAGE_RECORD(record_id, principal) retorna metadados autorizados de um
   registro específico; acesso aos bytes é uma operação protegida separada ou
   parte de resposta autorizada, nunca acesso público por URL/caminho.
4. CAPTURE_REQUEST(request_id, principal), se implementado, expõe resultado
   operacional sanitizado do pedido e não equivale à leitura da imagem.
5. DISPLAY_IMAGE(camera, principal) projeta a imagem de apresentação pela
   seleção da seção 25, preservando o resultado de LATEST_CAMERA_CAPTURE e a
   proveniência do registro escolhido.

Leituras usam o caminho canônico do domínio e o mesmo modelo/histórico para UI
e superfícies futuras. Nenhum consumidor cria tabela, consulta ou regra paralela
exclusiva para imagem.

## 18. QUICK_DETAIL_PANEL_CONSUMER_CONTRACT

CameraQuickDetailPanel consome DISPLAY_IMAGE da câmera selecionada segundo
a política única da seção 25 e mantém visível o estado de
LATEST_CAMERA_CAPTURE. Não consome LATEST_IMAGE_OF_ANY_ORIGIN e não usa
PRIMARY_IMAGE como substituto. Não inicia captura, probe, chamada VMS, acesso
direto à câmera nem polling pesado ao abrir ou trocar de câmera.

O painel respeita autorização e mostra proveniência, timestamp pertinente,
estado de disponibilidade/erro e preview validado quando houver. Para
CAPTURA_CAMERA, usa rótulo equivalente a "Última captura registrada"; para
UPLOAD_MANUAL, "Imagem enviada manualmente"; para NONE, "Nenhuma imagem
disponível". UPLOAD_MANUAL usa recorded_at, sem captured_at presumido.
NO_CAPTURE_AVAILABLE, UNAVAILABLE e ERROR da captura continuam distinguíveis;
UNAVAILABLE ou ERROR não podem ser mascarados por upload manual. Upload manual
corrente indisponível ou inválido não pode ser mascarado por outro mais antigo.
Captura anterior pode aparecer somente em histórico claramente identificado,
nunca como captura corrente. O painel não contorna validação, storage,
permissão ou auditoria.

## 19. PERFORMANCE_CONSTRAINTS

- A consulta do painel é limitada à câmera selecionada e usa
  LATEST_CAMERA_CAPTURE_RECORD determinístico, com suporte de índice adequado
  a ser definido em IMG-02.
- Metadados básicos do painel não aguardam download/decode de imagem. Preview
  pode ser carregado independentemente e em representação limitada adequada à
  inspeção.
- Não carregar histórico inteiro ao abrir o painel; paginação/limite e tamanho
  de preview são adjudicados nas slices de histórico/UI.
- Não acessar câmera, storage de bytes ou VMS de modo bloqueante no request
  apenas para produzir a leitura de metadados; não introduzir polling pesado.
- Concorrência e consumo de storage/captura devem ser bounded. Custos do
  subsistema de imagens não degradam o monitoramento nem a renderização inicial.
- Seleção/troca de câmera deve associar a resposta à câmera solicitada para
  impedir conteúdo de uma câmera aparecer em outra.
- No Inventário, selecionar DISPLAY_IMAGE em lote, sem N+1: resolver capturas
  da página em lote, identificar apenas câmeras com NO_CAPTURE_AVAILABLE,
  resolver seus uploads manuais correntes em lote e produzir resultado por item.
- Índice novo para DISPLAY_IMAGE não é requisito desta atividade.
  INDEX_MIGRATION = MEASURE_BEFORE_DECIDING; migration posterior depende de
  evidência de performance.

## 20. INTEGRATION_CONSTRAINTS

Aplicar a regra canônica de sprints:

IMPLEMENT
→ INTEGRATE INTO CANONICAL FLOW
→ VALIDATE INTEGRATED
→ CLOSE SLICE

Cada capability deve ser alcançável pelo entrypoint real aplicável, usar
caminho canônico de domínio/storage, integrar permissão e auditoria quando
aplicável, ser visível ao consumidor real e não deixar implementação órfã.
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE.
BIG_BANG_INTEGRATION_AT_END = PROHIBITED.
INTEGRATION_SPRINT_AS_ROUTINE_CLEANUP = ANTI_PATTERN.

IMG-02 deve sustentar a consulta latest sem criar domínio paralelo. IMG-03 e
IMG-04 alimentam o mesmo CameraImageRecord e histórico. IMG-05 mantém captura
fora do monitoramento. IMG-06 implementa a leitura histórica. IMG-07 resolve
PRIMARY_IMAGE sem redefinir latest. IMG-08 integra autorização/auditoria;
IMG-09 fecha hardening, indisponibilidade, concorrência e estados de erro.
UI-3 consome os mesmos caminhos canônicos, quando chegar sua integração.

## 21. OPEN_DECISIONS

OPEN_DECISION_COUNT = 6

As seis questões abaixo são pendências conceituais não bloqueantes para
canonicalizar IMG-01. Permanecem sem decisão implícita e fecham nas slices
indicadas:

| # | Pendência | Fechamento esperado |
|---:|---|---|
| 1 | Backend definitivo de produção, provedor e estratégia operacional | DEFERRED; decidir na arquitetura posterior de storage/produção. IMG-02 estabelece contrato persistente e abstração configurável antes da migration. |
| 2 | MIME permitido e limites de bytes/dimensões | IMG-03/IMG-08, antes de aceitar arquivos reais |
| 3 | Retenção, lifecycle e expurgo de registros/bytes | IMG-06/IMG-08/IMG-09, antes de operação destrutiva |
| 4 | Limiar temporal e semântica de STALE/indisponibilidade do objeto | IMG-02/IMG-06/IMG-09 antes de expor freshness como estado de domínio |
| 5 | Credencial/perfil e privilégio autorizados para captura | IMG-04/IMG-08, antes de conexão a câmera real |
| 6 | Existência e semântica final de PRIMARY_IMAGE | IMG-07 |

O uso visual de UPLOAD_MANUAL sem captura foi adjudicado pela política
DISPLAY_IMAGE da seção 25 e deixou de ser OPEN_DECISION. PRIMARY_IMAGE
permanece questão independente e diferida para IMG-07. A contagem não altera
nem escolhe o conteúdo das seis decisões remanescentes.

## 22. IMG02_PREREQUISITES

Esta seção estabelece os pré-requisitos técnicos de implementação da slice
IMG-02. O status corrente e a ordem das atividades pertencem ao roadmap,
sprint map e documentos de continuidade. Antes da implementação, o agente deve:

1. ler este contrato, roadmap, sprint map, ADR-019, ADR-021 e authorities
   vigentes; revalidar Git e escopo;
2. obter adjudicação humana e autorização explícita para a implementação de
   IMG-02. Este contrato não concede autorização;
3. estabelecer contrato persistente de storage, referência privada e abstração
   configurável antes da migration. A escolha do backend definitivo de produção
   permanece deferred e não é pré-requisito para a migration;
4. traduzir CameraImageRecord para modelo persistente sem alterar as
   proveniências, autoria, timestamps, lifecycle e estados deste contrato;
5. assegurar associação a uma câmera, identidade imutável, recorded_at
   confiável, captured_at obrigatório para CAPTURA_CAMERA e proveniência
   preservada;
6. implementar a seleção latest em exatamente esta ordem:
   captured_at DESC, recorded_at DESC, immutable_id DESC, depois avaliar
   validade/integridade/disponibilidade;
7. fornecer constraints e índices que sustentem a ordenação, e demonstrar que
   registro latest inválido/indisponível não promove registro mais antigo;
8. manter bytes privados e acesso protegido por autorização, sem expor path ou
   URL pública;
9. integrar o modelo ao caminho canônico e ao Integration Gate aplicável,
   preservar a regra de vertical slice e relatar decisões ainda abertas sem
   resolvê-las por suposição.

IMG02_IMPLEMENTATION_AUTHORIZATION_FROM_THIS_DOCUMENT = NO.
CURRENT_ACTIVITY_STATUS_AUTHORITY = roadmap, sprint map e documentos de continuidade.

## 23. Critério de leitura autônoma

CAN_A_NEW_AGENT_FIND_IMG02_CONTRACT_WITHOUT_CHAT_HISTORY = YES, quanto a
entidade, proveniência, latest capture sem fallback histórico, DISPLAY_IMAGE, timestamps,
autoria, storage, validação, segurança, auditoria, separação do monitoramento,
leituras, performance, integração, decisões abertas e pré-requisitos.
Este contrato não declara o status corrente nem a ordem do trabalho. Consulte o
roadmap, sprint map e documentos de continuidade; este documento não concede
autorização de implementação.

## 24. Contrato técnico de entrega privada de preview (slice autorizada em 2026-09-25)

`CameraImagePreviewService` entrega somente `LATEST_CAMERA_CAPTURE`, reutilizando
a seleção de `CameraImageReadService.latest_records`. O cliente fornece apenas
`Camera.pk` e uma variante fechada na rota
`GET /cameras/<pk>/imagens/ultima-captura/<variant>/` (`THUMB` ou `PANEL`).
`THUMB` gera JPEG 60×42; `PANEL` gera JPEG 640×448. O crop central via
`ImageOps.fit` preserva a proporção. O serviço lê pela abstração configurada
`default_storage`, verifica SHA-256 e decodifica JPEG/PNG/WebP estático antes de
regravar pixels em JPEG sem metadados. O objeto original e o registro não são
alterados; não há preview derivado persistido.

`cameras.view_camera` é a permissão Django reutilizada para os dois consumidores.
O usuário anônimo recebe 401, o sem permissão 403, câmera inexistente 404 e
variante inválida ou query string inesperada 400. A seleção sem captura retorna
404 (`NO_CAPTURE_AVAILABLE`); latest indisponível retorna 503 (`UNAVAILABLE`);
latest inválida, corrompida ou com hash divergente retorna 422 (`ERROR`). A
resposta válida é 200 `image/jpeg`, `Content-Disposition: inline`,
`X-Content-Type-Options: nosniff` e `Cache-Control: no-store`. Falhas não
incluem bytes, chave ou caminho de storage. Nenhum estado promove captura
anterior, upload manual ou imagem principal.

O Inventário consulta metadados da página em um único batch ORM, sem consultar
ou abrir storage no render HTML. Uma captura com metadados íntegros é apenas
candidata à URL; o request lazy revalida storage e bytes. Se o objeto mudar
entre HTML e request, o navegador oculta a imagem falha e mantém o placeholder.
`alt=""` e wrapper `aria-hidden="true"` evitam repetir o nome da câmera, que
permanece no link adjacente. A fonte de imagem não altera monitoramento.

Limites operacionais reversíveis do preview: 20 MiB e 20 milhões de pixels
para o objeto de origem; não definem política definitiva de upload/captura.
Geração permanece on-demand e sem cache público ou persistente. Cache de
derivados, thumbnails persistentes e CDN exigem métricas e decisão futura.
Backend definitivo, matriz final de permissões de imagem e políticas finais de
MIME, bytes e dimensões permanecem deferred. UI-3 e IMG-04 seguem sem autorização.

## 25. DISPLAY_IMAGE_CONTRACT — projeção de apresentação

DISPLAY_IMAGE_POLICY = OPTION_B (decisão de produto aprovada).

DISPLAY_IMAGE é a projeção autorizada para exibir uma imagem da câmera no
Inventário e no CameraQuickDetailPanel. Não é um registro, uma nova proveniência
ou mutação de CameraImageRecord. DISPLAY_IMAGE != LATEST_CAMERA_CAPTURE;
DISPLAY_IMAGE != PRIMARY_IMAGE; DISPLAY_IMAGE != MONITORING_EVIDENCE. A seleção
de LATEST_CAMERA_CAPTURE da seção 7, inclusive seu estado e a proibição de
promover captura antiga, permanece integralmente preservada. PRIMARY_IMAGE
continua reservado a IMG-07. UPLOAD_MANUAL continua sem captured_at e não
produz evidência nem altera o monitoramento.

### 25.1 Seleção e estados

Para uma câmera autorizada, a projeção obtém primeiro o resultado canônico de
LATEST_CAMERA_CAPTURE. Somente NO_CAPTURE_AVAILABLE permite selecionar upload
manual. Nesse caso, considera apenas registros UPLOAD_MANUAL da câmera que
participam do estado corrente (não retirados logicamente), ordenados por
recorded_at DESC, immutable_id DESC; immutable_id corresponde ao id estável e
total do registro. Seleciona o primeiro antes de avaliar integridade ou
disponibilidade. Não filtra por AVAILABLE e não procura upload mais antigo se
o selecionado estiver UNAVAILABLE ou ERROR. OLDER_MANUAL_FALLBACK = NO.

| CAPTURE_STATE | Upload manual corrente | SOURCE | STATE | Motivo do fallback |
|---|---|---|---|---|
| AVAILABLE | não consultado | CAPTURA_CAMERA | AVAILABLE | vedado: captura disponível |
| UNAVAILABLE | não consultado | CAPTURA_CAMERA | UNAVAILABLE | vedado: captura corrente indisponível |
| ERROR | não consultado | CAPTURA_CAMERA | ERROR | vedado: captura corrente inválida |
| NO_CAPTURE_AVAILABLE | nenhum | NONE | NO_IMAGE_AVAILABLE | permitido, mas sem upload corrente |
| NO_CAPTURE_AVAILABLE | AVAILABLE | UPLOAD_MANUAL | AVAILABLE | permitido: ausência de captura |
| NO_CAPTURE_AVAILABLE | UNAVAILABLE | UPLOAD_MANUAL | UNAVAILABLE | permitido: upload corrente indisponível; sem busca anterior |
| NO_CAPTURE_AVAILABLE | ERROR | UPLOAD_MANUAL | ERROR | permitido: upload corrente inválido; sem busca anterior |

DisplayImageResult é o nome conceitual da leitura. Deve distinguir
SOURCE = CAPTURA_CAMERA | UPLOAD_MANUAL | NONE; STATE = AVAILABLE |
NO_IMAGE_AVAILABLE | UNAVAILABLE | ERROR; CAPTURE_STATE = AVAILABLE |
NO_CAPTURE_AVAILABLE | UNAVAILABLE | ERROR; e um motivo explícito da permissão
ou vedação do fallback manual. Preserva identidade e proveniência do registro
selecionado quando houver um. Falhas de autorização, permissão ou consulta não
são convertidas em NO_IMAGE_AVAILABLE; seguem erros sanitizados do contrato de
leitura e entrega segura.

### 25.2 Consumidores e apresentação

INVENTORY_THUMBNAIL e CAMERA_QUICK_DETAIL_PANEL consomem a mesma política e o
mesmo resultado, sem regras próprias de fallback. O Inventário pode usar
thumbnail compacta sem novo badge em cada item, mas origem e estados permanecem
disponíveis semanticamente para acessibilidade e integração futura; um upload
nunca é anunciado como captura. O painel usa os rótulos da seção 18 e não
esconde captura UNAVAILABLE/ERROR com upload, nem upload corrente
UNAVAILABLE/ERROR com upload anterior. Nos estados sem bytes apresentáveis,
mostra placeholder/estado apropriado sem mudar SOURCE ou CAPTURE_STATE.

### 25.3 Entrega privada e isolamento da rota de captura

`GET /cameras/<pk>/imagens/ultima-captura/<variant>/` e o
`CameraImagePreviewService` descritos na seção 24 continuam significando
exclusivamente LATEST_CAMERA_CAPTURE. Seus status e a vedação de upload manual
nessa rota permanecem válidos. A entrega de DISPLAY_IMAGE usa superfície
distinta, `GET /cameras/<pk>/imagens/exibicao/<variant>/`, sem ampliar
silenciosamente a rota de última captura. A rota de exibição foi implementada
em IMG-DISPLAY-01.

A nova superfície deve reutilizar o pipeline seguro existente: autenticação,
permissão `cameras.view_camera`, storage privado, variantes fechadas, validação
de hash/integridade, decode e re-encoding antes de servir os bytes, resposta
`nosniff` e `no-store`, sem expor path ou storage key. Seleção e entrega não
iniciam captura, probe, VMS ou qualquer side effect de monitoramento. Estados de
falha da projeção são explícitos e sanitizados. A rota de exibição preserva
a semântica da rota de última captura.

### 25.4 Consulta em lote e limite desta decisão

Para a página do Inventário, a leitura resolve capturas em lote,
identifica somente câmeras com NO_CAPTURE_AVAILABLE, resolve em lote o upload
manual corrente dessas câmeras e produz um DisplayImageResult por item. Não
introduz N+1 nem abre bytes de storage no render HTML. Índice ou migration
adicional para esta projeção não é exigido: INDEX_MIGRATION =
MEASURE_BEFORE_DECIDING. Proposta posterior depende de medição que demonstre
necessidade. A decisão documental original não implementou serviço, rota,
schema, migration ou UI; a implementação posterior é IMG-DISPLAY-01.

### 25.5 Estado de implementação — IMG-DISPLAY-01 (2026-09-26)

O contrato da seção 25 foi implementado no commit `4bcd81d` e integrado ao
`master` pelo merge `cad0760`. `DisplayImageReadService` resolve a projeção;
Inventário e CameraQuickDetailPanel consomem DISPLAY_IMAGE e a rota separada
`GET /cameras/<pk>/imagens/exibicao/<variant>/` foi adicionada. Esta
subseção registra o estado atual sem mudar a semântica normativa de
LATEST_CAMERA_CAPTURE, PRIMARY_IMAGE, provenance ou monitoramento. Esta
atualização documental não reexecutou a validação de IMG-DISPLAY-01.

## 26. Reconciliação de apresentação do Quick Detail (2026-10-11)

Esta decisão de produto, aprovada pelo usuário, supersede somente a seleção de
imagem exibida pelo CameraQuickDetailPanel descrita nas seções 18 e 25. Não
altera `LATEST_CAMERA_CAPTURE`, sua consulta, estado, rota ou consumidores
técnicos. Inventário e demais consumidores não herdam esta regra sem decisão
própria.

```text
QUICK_DETAIL_IMAGE = LATEST_ACTIVE_IMAGE
PROVENANCE = CAPTURA_CAMERA | UPLOAD_MANUAL
ORDER = recorded_at DESC, immutable_id DESC
MAX_ACTIVE_IMAGES_CAMERA_DETAIL = 3
CAMERA_DETAIL_GALLERY_ORDER = recorded_at ASC, immutable_id ASC
CAPTURE = MANUAL_ONLY
UPLOAD = MANUAL_ONLY
```

`LATEST_ACTIVE_IMAGE` seleciona entre os registros ativos da câmera consultada,
independentemente da proveniência, ordenando por `recorded_at DESC` e pelo
desempate estável `immutable_id DESC`. A imagem manual ativa registrada mais
recentemente pode, portanto, ser apresentada no Quick Detail no lugar de uma
captura anterior. A disponibilidade/integridade é avaliada após selecionar o
registro mais recente; não se escolhe um registro anterior como fallback
silencioso. O Quick Detail identifica a proveniência e não cria evento de
captura nem altera monitoramento.

`LATEST_CAMERA_CAPTURE` continua sendo o conceito técnico distinto, restrito a
`CAPTURA_CAMERA`, com a ordenação e semântica da seção 7. Nenhum endpoint,
serviço ou consumidor técnico de captura passa a aceitar upload manual por esta
decisão. Camera Detail pode exibir até três imagens ativas em ordem crescente;
captura e upload são ações exclusivamente manuais. Implementação de galeria,
captura, rotação ou expurgo não está incluída nesta reconciliação.

```text
DECISION_APPROVED = YES / USER
DOCUMENTED = YES
IMPLEMENTED = NOT_ESTABLISHED
INTEGRATED = NO
VALIDATED = NO
HOMOLOGATED = NO
```

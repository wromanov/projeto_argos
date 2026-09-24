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
para consumidores de imagem, em especial CameraQuickDetailPanel. Define os
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
CameraQuickDetailPanel usa LATEST_CAMERA_CAPTURE e não usa PRIMARY_IMAGE como
substituto.

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
re-encoding, metadados retidos e eventual fallback visual do upload permanecem
OPEN_DECISIONS. Se uma experiência futura optar por mostrar uma imagem manual
em contexto que espera captura, essa escolha deve ser explicitamente
adjudicada, rotulada UPLOAD_MANUAL e nunca funcionar como fallback implícito.

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

O contrato não decide armazenamento local, filesystem, objeto remoto, banco,
produto/provedor, layout de chaves, replicação, backup ou política de
recuperação. Backend de storage é OPEN_DECISION a ser fechado em IMG-02 antes
da migration correspondente.

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

Leituras usam o caminho canônico do domínio e o mesmo modelo/histórico para UI
e superfícies futuras. Nenhum consumidor cria tabela, consulta ou regra paralela
exclusiva para imagem.

## 18. QUICK_DETAIL_PANEL_CONSUMER_CONTRACT

CameraQuickDetailPanel consome LATEST_CAMERA_CAPTURE da câmera selecionada.
Não consome LATEST_IMAGE_OF_ANY_ORIGIN e não usa PRIMARY_IMAGE como substituto.
Não inicia captura, probe, chamada VMS, acesso direto à câmera nem polling
pesado ao abrir ou trocar de câmera. UPLOAD_MANUAL não é fallback implícito.

O painel respeita autorização e mostra proveniência, timestamp, estado de
disponibilidade/erro e preview validado quando houver. NO_CAPTURE_AVAILABLE,
UNAVAILABLE e ERROR são estados distintos; captura anterior pode aparecer
somente em histórico claramente identificado, nunca como captura corrente.
O painel não contorna validação, storage, permissão ou auditoria.

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

OPEN_DECISION_COUNT = 7

As sete questões abaixo são pendências conceituais não bloqueantes para
canonicalizar IMG-01. Permanecem sem decisão implícita e fecham nas slices
indicadas:

| # | Pendência | Fechamento esperado |
|---:|---|---|
| 1 | Backend concreto de storage, referência, recuperação e backup | IMG-02, antes de migration/integração de storage |
| 2 | MIME permitido e limites de bytes/dimensões | IMG-03/IMG-08, antes de aceitar arquivos reais |
| 3 | Uso visual de UPLOAD_MANUAL quando não houver captura | adjudicação do consumidor/UI-3; continua proibido como fallback implícito |
| 4 | Retenção, lifecycle e expurgo de registros/bytes | IMG-06/IMG-08/IMG-09, antes de operação destrutiva |
| 5 | Limiar temporal e semântica de STALE/indisponibilidade do objeto | IMG-02/IMG-06/IMG-09 antes de expor freshness como estado de domínio |
| 6 | Credencial/perfil e privilégio autorizados para captura | IMG-04/IMG-08, antes de conexão a câmera real |
| 7 | Existência e semântica final de PRIMARY_IMAGE | IMG-07 |

As sete linhas são sete decisões, porque PRIMARY_IMAGE é questão conceitual
independente; não se reduz a uma das outras seis. A contagem não altera nem
escolhe o conteúdo dessas decisões.

## 22. IMG02_PREREQUISITES

IMG-02 — Modelo, storage e proveniência é a próxima atividade de projeto.
Antes da implementação, o agente futuro deve:

1. ler este contrato, roadmap, sprint map, ADR-019, ADR-021 e authorities
   vigentes; revalidar Git e escopo;
2. obter adjudicação humana e autorização explícita para a implementação de
   IMG-02. Este checkpoint documental não autoriza implementação;
3. fechar a decisão de backend de storage e referência privada, além de
   requisitos de backup/recuperação aplicáveis, antes da migration;
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

IMG02_READY_FOR_IMPLEMENTATION = YES, após adjudicação humana e autorização.
IMG02_IMPLEMENTATION_AUTHORIZATION_FROM_THIS_DOCUMENT = NO.

O futuro agente consegue iniciar discovery e formular a implementação sem
histórico de chat; não pode substituir as adjudicações pendentes nem presumir
permissão de implementação.

## 23. Critério de leitura autônoma

CAN_A_NEW_AGENT_IMPLEMENT_IMG02_WITHOUT_CHAT_HISTORY = YES, quanto a entender
entidade, proveniência, latest capture, ausência de fallback, timestamps,
autoria, storage, validação, segurança, auditoria, separação do monitoramento,
leituras, performance, integração, decisões abertas e pré-requisitos. A
implementação continua condicionada à adjudicação das decisões aplicáveis e à
autorização humana própria.

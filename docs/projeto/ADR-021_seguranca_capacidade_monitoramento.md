# ADR-021 — Segurança e Capacidade do Monitoramento

**Status:** Aprovado
**Data:** 12/08/2026
**Escopo:** MON-02 — segurança, credenciais e capacidade técnica dos equipamentos
**Inteligência recomendada:** 🌎 Terra Alto

## 1. Contexto e autoridade

O ARGOS deverá acompanhar a disponibilidade técnica de aproximadamente 2.300
câmeras por meio de worker independente do ciclo HTTP do Django. O navegador
consulta apenas o estado conhecido pelo ARGOS e nunca sonda diretamente os
equipamentos. O status técnico continua separado da situação operacional, e o
monitoramento continua desacoplado da captura de imagens, conforme ADR-019 e
ADR-020.

A MON-00 identificou como bloqueador a custódia de credenciais de câmera e
como riscos majoritários a ausência de allowlist/defesa contra SSRF, a falta
de protocolo/porta/capacidade estruturados, o vazamento de segredos em
logs/traces/URLs e a identidade ainda não definida do worker. Este ADR fecha
os contratos arquiteturais necessários para que esses riscos não sejam
transferidos silenciosamente para uma futura implementação.

Este documento não cria model, migration, worker, probe, configuração de
firewall, usuário de banco, biblioteca criptográfica, segredo ou integração
com câmera real. Nenhum valor de credencial, CIDR real, porta real ou endpoint
real do parque é definido.

ADR-019 e ADR-020 permanecem autoridades anteriores. Este ADR os detalha no
limite de segurança e capacidade e não reabre suas decisões aprovadas.

## 2. Auditoria do estado atual

O repositório ainda não possui credencial de câmera, worker, probe, scheduler,
lease ou catálogo de capacidade implementado.

No modelo atual:

- `Camera.ip` aceita IPv4 cadastrado e não possui protocolo, porta ou endpoint
  associado;
- `Camera.status` possui somente `ONLINE` e `OFFLINE`, é anulável e ainda
  representa `NULL`/vazio como “Não verificado” na interface;
- `status_em` e `ultima_verificacao` existem, mas o código não possui produtor
  automático de probe;
- `situacao_operacional` permanece administrativa (`PRODUCAO`, `ESTOQUE` e
  `DESATIVADA`);
- `CameraAdmin` ainda expõe os campos técnicos para edição manual; o
  ownership futuro do subsistema de monitoramento não é implementado nesta
  etapa;
- `CAMPOS_CAMERA_AUDITAVEIS` não inclui os três campos técnicos atuais;
- `cameras/auditoria.py` já possui sanitização de chaves sensíveis, mas essa
  proteção existente não substitui um contrato explícito de não-logar
  segredos nem autoriza a futura passagem de exceções cruas;
- desenvolvimento usa SQLite; PostgreSQL continua sendo a direção oficial
  para produção, ainda não configurada no repositório.

Essas lacunas são estado atual auditado, não falhas corrigidas por este ADR.

## 3. Decisões de segurança e capacidade

### 3.1 Separação entre configuração e segredo

Configuração técnica não secreta e material de autenticação possuem entidades,
permissões, lifecycle e auditoria distintos.

Configuração não secreta pode conter, conforme o perfil aprovado:

- protocolo/adaptador;
- porta;
- exigência e política de TLS;
- endpoint ou path controlado;
- método de autenticação;
- referência da credencial;
- fabricante, modelo, firmware ou compatibilidade quando necessários;
- política de probe e parâmetros estritamente necessários.

Material secreto pode conter password, token, chave e outros dados de
autenticação. Username deve ser tratado como material sensível quando a
política do ambiente assim exigir; mesmo quando não for criptografado, nunca
é exibido em logs, URLs, HTML ou mensagens de erro.

Senha nunca é embutida em URL RTSP/HTTP. A URL, quando inevitável, é montada
internamente a partir de destino validado, scheme permitido e path do perfil.

### 3.2 Custódia recomendada

A direção inicial recomendada é:

```text
CredencialEquipamento separada
        |
        +--> material protegido em nível de aplicação
        +--> versão da credencial e da chave
        +--> referência explícita de escopo

chave mestra --> fornecida ao serviço por mecanismo seguro fora do banco
```

O material persistido deve ser ciphertext com proteção autenticada e
integridade verificada por primitive/biblioteca criptográfica reconhecida.
Não se implementa criptografia própria nem se escolhe biblioteca concreta
nesta etapa. A chave mestra nunca é gravada no mesmo banco, backup ou artefato
que contém o ciphertext. O worker autorizado obtém a chave somente em tempo
de execução e mantém o segredo disponível pelo menor tempo e escopo
necessários ao adaptador.

O serviço não recebe credenciais por argumento de linha de comando. Uma
variável de ambiente pode ser apenas o mecanismo de entrega de um segredo de
runtime em ambiente controlado; ela não deve virar arquivo versionado, valor
de fixture, relatório ou configuração textual compartilhada. O mecanismo
operacional concreto de fornecimento da chave permanece aberto.

### 3.3 Alternativas de custódia

| Alternativa | Simplicidade e operação | Rotação e restore | Risco, escala e recomendação |
|---|---|---|---|
| A. Ciphertext no PostgreSQL + chave fora do banco | Integra a persistência do ARGOS e é simples de consultar por referência; exige disciplina de acesso, proteção da chave e runbook de restore | Rotação exige versionamento e operação coordenada; backup do banco sozinho não revela a senha, mas restore depende da recuperação segura da chave | Adequada a milhares de referências sem duplicar o segredo; risco concentrado na chave mestra e na configuração do serviço; **recomendada como direção inicial** |
| B. Secret manager externo | Melhor separação operacional e políticas próprias de acesso/rotação; adiciona dependência, disponibilidade, integração, observabilidade e custo de operação | Pode simplificar rotação e recuperação se o serviço for bem operado; exige plano de contingência, identidade federada e backup/restore do próprio serviço | Forte opção para produção madura e múltiplos ambientes; não se escolhe fornecedor nesta etapa nem se adiciona essa dependência sem decisão operacional |
| C. Credenciais exclusivamente em environment/configuração do worker | Inicialmente simples para poucos equipamentos, mas difícil de auditar, rotacionar e distribuir com segurança | Backup, restore e rotação ficam espalhados entre hosts/processos; risco de cópia, exposição e divergência cresce com 2.300 câmeras | Não atende bem múltiplas credenciais, escopo por câmera e lifecycle centralizado; **não recomendada como armazenamento exclusivo** |

Para 2.300 equipamentos, não se presume uma senha compartilhada. Uma mesma
credencial pode ser referenciada por várias câmeras somente quando o
relacionamento tiver escopo explícito, versão, lifecycle de rotação e blast
radius reconhecido. A referência compartilhada reduz duplicação, mas aumenta
o impacto de comprometimento ou rotação daquela credencial.

### 3.4 Lifecycle de credencial e rotação

A entidade conceitual de credencial possui, no mínimo, estado ativa/inativa,
versão, referência segura, escopo, `criada_em`, `rotacionada_em` e quem
alterou a configuração. `última utilização` pode ser métrica operacional
restrita, não um valor secreto.

O fluxo aprovado conceitualmente é:

```text
nova versão
    -> validação controlada
    -> ativação da nova versão
    -> worker resolve a versão ativa autorizada
    -> versão anterior retirada conforme política
```

A troca deve ser atômica no vínculo de configuração e não pode provocar uma
onda automática de `OFFLINE` apenas porque a rotação ocorreu. Se a validação
falhar durante uma rotação planejada, a versão anterior pode continuar
temporariamente utilizável somente se ainda for segura/válida, não estiver
revogada, não houver suspeita de comprometimento e a política operacional
permitir. O evento registra referência e resultado, nunca o valor. Não se
presume fallback automático nem dual-secret.

Rotação de emergência ou revogação exige semântica diferente: versão
comprometida, revogada ou considerada insegura não pode continuar sendo usada
como fallback. Sua utilização cessa conforme a política de emergência, e a
indisponibilidade da nova credencial não autoriza reutilizá-la. A câmera não é
marcada `OFFLINE` por essa condição; probes autenticados podem ficar
temporariamente bloqueados, o estado técnico anterior é preservado e a
freshness pode evoluir para `stale`. O subsistema sinaliza o problema
operacional/de segurança por canal sanitizado.

Backup do banco contendo ciphertext é insuficiente para restauração. O
runbook futuro deve recuperar de modo separado e autorizado a chave
correspondente, validar versão/integridade e testar o acesso do serviço sem
imprimir o segredo. Perder a chave não pode ser “resolvido” extraindo-a do
backup do banco.

### 3.5 Perfil de capacidade de monitoramento

O contrato técnico deve ser representado por um `PerfilCapacidadeMonitoramento`
ou nome equivalente, sem criar model nesta tarefa. O perfil descreve o que um
adaptador autorizado pode fazer, não uma URL arbitrária fornecida por usuário.

Campos conceituais:

- protocolo/adaptador: por exemplo TCP, HTTP, HTTPS, RTSP ou ONVIF;
- porta permitida pelo perfil;
- TLS requerido, não requerido ou política equivalente a ser homologada;
- endpoint/path controlado pelo perfil;
- método de autenticação;
- `requer_credencial`;
- probe primário e, quando justificado, secundário;
- fabricante/modelo/firmware compatível quando essa distinção for necessária;
- parâmetros estritamente necessários ao adaptador;
- versão, estado ativo/inativo e referência de auditoria.

O perfil não deve normalizar agora todo fabricante/modelo nem inventar
capabilities reais. Compatibilidade declarada é uma restrição de seleção; a
capacidade efetiva precisa de evidência de laboratório. ICMP pode ser
homologado como sinal adicional, mas resposta positiva não prova serviço ou
câmera operacional. TCP positivo prova somente reachability/listener da porta.
HTTP/HTTPS pode provar o serviço específico contratado. RTSP não é health
check universal e ONVIF não prova necessariamente stream de vídeo.

### 3.6 Perfil compartilhado e configuração por câmera

São consideradas três alternativas:

1. toda a capacidade duplicada em cada câmera;
2. um perfil rígido por fabricante/modelo;
3. perfil reutilizável com override restrito e explícito por câmera.

A alternativa 1 aumenta duplicação, divergência e custo de auditoria para
aproximadamente 2.300 registros. A alternativa 2 reduz manutenção, mas
assume indevidamente que câmeras do mesmo modelo e firmware têm o mesmo
endpoint, porta, credencial ou configuração de rede. A alternativa 3 é a
recomendação: o perfil compartilhado fornece defaults e limites validados; a
câmera possui configuração efetiva apenas para os campos que o próprio perfil
declara como sobrescrevíveis.

Um override não pode liberar scheme, destino, porta, método de autenticação
ou parâmetro que a política do ambiente/perfil não autorize. O endpoint
específico de uma câmera só pode existir se o perfil o permitir e se passar
pela mesma validação de segurança. A troca de modelo, firmware ou câmera
deve revalidar o vínculo e gerar auditoria de configuração.

### 3.6.1 Autorização humana da fronteira de segurança

Edição cadastral comum de `Camera` não concede automaticamente autorização
para alterar a fronteira de segurança do monitoramento. Exigem permissão
privilegiada específica, a ser implementada posteriormente, as operações que
criem ou alterem `PerfilCapacidadeMonitoramento`; ampliem protocolo, porta,
endpoint, TLS ou autenticação; associem ou troquem credencial; criem, ativem,
inativem, rotacionem ou revoguem credencial; bloqueiem ou desbloqueiem
monitoramento; alterem allowlist/política de destino; ou criem exceções de
segurança.

Usuário comum não pode ampliar destino, porta, scheme ou privilégio. O
contrato exige least privilege humano, segregação de funções quando material
e auditoria de toda alteração privilegiada. A auditoria registra identidade,
escopo, versão, motivo e resultado sanitizado, nunca o valor secreto.
Não são definidos agora nomes concretos de grupos ou permissões Django.

### 3.7 Protocolos e destino

Não há protocolo universal nesta etapa. Adaptadores futuros podem suportar
TCP connect, HTTP, HTTPS, RTSP, ONVIF e eventualmente ICMP se homologado.
Cada uso deve declarar o que o resultado prova e seu contrato de capacidade.

O baseline de endereçamento é IP-only: o worker usa o `Camera.ip` IPv4
cadastrado e não aceita hostname/DNS até existir necessidade homologada. O
destino é derivado do registro e do perfil; o browser e o chamador do worker
não fornecem IP, URL, hostname ou porta arbitrários para uma execução.

Quando HTTP/HTTPS for aprovado, o worker constrói internamente a URL com
scheme permitido, IP validado, porta autorizada e path controlado. Userinfo é
proibido. A porta deve estar no intervalo 1..65535, ser permitida pelo perfil
e também pela política do ambiente; um usuário comum não escolhe uma porta
arbitrária no momento do probe.

DNS fica desabilitado no baseline. Se futuramente for aceito, o worker deverá
resolver e validar todos os IPs resultantes, revalidar o destino no momento
da conexão e impedir rebinding quando aplicável. Não é suficiente validar o
hostname uma única vez.

Redirects HTTP/HTTPS ficam desabilitados no baseline por serem a alternativa
mais simples e segura. Se uma integração futura exigir redirect, cada hop
deverá ter scheme, userinfo, porta e destino revalidados contra a allowlist;
um redirect para fora da política será bloqueado.

### 3.7.1 Segregação por ambiente

Desenvolvimento, teste e produção possuem custódia separada: credenciais não
podem ser reutilizadas implicitamente entre ambientes; master keys possuem
escopo de ambiente; allowlists são definidas por ambiente; e o worker só
acessa o ambiente ao qual pertence. Copiar banco entre ambientes não torna
secrets automaticamente utilizáveis. Restore ou migração exige
reestabelecer explicitamente a custódia, a chave e a política do ambiente
correto. Nenhuma infraestrutura concreta é definida nesta etapa.

### 3.8 Allowlist de rede e defesa em profundidade

O worker somente pode alcançar destinos explicitamente pertencentes à rede
de CFTV autorizada. A allowlist é configurável por ambiente e não contém
CIDRs reais neste documento. Ela deve poder expressar:

- CIDRs de CFTV autorizados;
- portas permitidas por protocolo;
- associação protocolo -> portas;
- restrição adicional por farm, segmento ou grupo autorizado;
- exceções documentadas, temporárias e auditáveis, se alguma existir.

Antes de conectar, o worker deve:

1. obter a configuração por `camera_id`/referência autorizada, nunca por URL
   recebida do browser;
2. analisar estritamente o IPv4 cadastrado e rejeitar formato ambíguo;
3. rejeitar loopback, `localhost`, unspecified, link-local, multicast,
   broadcast, endpoints de metadata de provedores e destinos administrativos
   não autorizados;
4. verificar pertencimento à allowlist de CFTV do ambiente;
5. verificar protocolo, porta, endpoint e compatibilidade do perfil;
6. aplicar a política adicional de farm/segmento quando existir;
7. conectar somente com egress/firewall do host também restrito.

O fato de um IP ser sintaticamente válido ou privado não o torna autorizado.
Uma faixa privada só é permitida se pertencer explicitamente à allowlist de
CFTV daquele ambiente. A validação no Django é uma camada de conveniência e
governança; a validação deve ser repetida no worker e reforçada pela
infraestrutura. O worker não deve honrar proxy ambiental inesperado por
default; uso de proxy, se algum dia necessário, exige configuração explícita
e destino igualmente validado.

## 4. Elegibilidade e resultados técnicos

### 4.1 Elegibilidade de domínio

Elegibilidade é determinada por configuração persistente válida e autorizada.
Uma câmera em `PRODUCAO` só é elegível quando todos os requisitos seguintes
são satisfeitos:

- IP IPv4 válido e pertencente à allowlist autorizada do ambiente;
- configuração de monitoramento ativa, não bloqueada e semanticamente válida;
- perfil/capacidade existente, ativo e compatível;
- protocolo/adaptador definido pelo perfil;
- porta válida no intervalo 1..65535 e autorizada pelo perfil e ambiente;
- endpoint/path e demais parâmetros necessários ao adaptador presentes e
  controlados;
- referência de credencial ativa e autorizada quando o protocolo exigir
  autenticação;
- nenhum bloqueio de configuração, escopo ou política de segurança.

`ESTOQUE` e `DESATIVADA` permanecem fora do escopo conforme ADR-020. Uma
câmera em `PRODUCAO` sem requisito, com referência inválida, destino fora da
allowlist ou configuração bloqueada também não é sondada.

Ausência, invalidade ou bloqueio de configuração não gera `OFFLINE` nem
`UNKNOWN` técnico: a condição derivada é **NÃO MONITORADA — CONFIGURAÇÃO
INCOMPLETA** ou **NÃO MONITORADA — CONFIGURAÇÃO BLOQUEADA**, conforme a causa.
Essa condição não abre indisponibilidade.

### 4.1.1 Prontidão transitória do subsistema

Prontidão de execução é uma condição operacional transitória, separada da
elegibilidade da câmera. Ela exige worker disponível, banco acessível, master
key disponível, secret backend/mecanismo de chave disponível e os recursos
necessários ao adaptador.

Uma câmera elegível não sai do escopo porque essa infraestrutura está
temporariamente indisponível. Nesses casos o worker não executa o probe,
preserva o último estado técnico, não abre nem fecha incidente, não registra
`SAIU_DO_ESCOPO` e permite que evidence/freshness envelheça normalmente,
eventualmente apresentando `stale`/`UNKNOWN` conforme ADR-020. O subsistema
registra somente health/erro sanitizado. `CONFIG_ERROR` ou `TARGET_BLOCKED`
podem ser resultados/preflight normalizados quando apropriado, mas falha
transitória do subsistema não é configuração persistente inválida da câmera.

### 4.2 Credencial ausente versus falha de autenticação

As situações são distintas:

| Situação | Elegibilidade | Resultado |
|---|---|---|
| Perfil não requer credencial | Elegível, se os demais requisitos passarem | Probe conforme o contrato do perfil |
| Perfil requer credencial, mas não há referência, está inativa ou está persistentemente inválida/bloqueada | Não elegível | Configuração incompleta/bloqueada; nenhum `OFFLINE` |
| Credencial ativa existe, probe executa e o equipamento rejeita autenticação | Elegível | Resultado técnico normalizado `AUTH_FAILURE` |
| Credencial ativa existe, mas a proteção/chave não está disponível ao serviço por falha transitória do subsistema | Elegível | Não executar probe; preservar estado/freshness; health/erro sanitizado, sem `OFFLINE` ou `SAIU_DO_ESCOPO` |

`AUTH_FAILURE` é observação técnica e não decisão automática de domínio. Sua
interpretação como `ONLINE`, `OFFLINE`, incidente ou manutenção depende do
contrato do adaptador e da política anti-flapping homologada posteriormente.

### 4.3 Categorias de resultado

O adaptador deve normalizar pelo menos:

```text
TIMEOUT
CONNECTION_REFUSED
AUTH_FAILURE
TLS_ERROR
PROTOCOL_ERROR
CONFIG_ERROR
TARGET_BLOCKED
CANCELLED
INCONCLUSIVE
```

Essas categorias não substituem os estados estáveis `UNKNOWN`, `ONLINE` e
`OFFLINE`. Um probe individual não produz transição de domínio; `CANCELLED`
por shutdown não é falha da câmera; configuração incompleta não é prova de
indisponibilidade.

## 5. Modelo conceitual e ownership

O modelo mínimo recomendado é:

```text
Camera
  |
  +-- 0..1 ConfiguracaoMonitoramento ativa
          |
          +-- 1 PerfilCapacidadeMonitoramento
          +-- 0..1 referência a CredencialEquipamento
          +-- destino derivado de Camera.ip

CredencialEquipamento
  +-- pode ser referenciada por 1..N configurações se o escopo permitir
```

### Camera

Responsabilidade: identidade, cadastro, localização, rede cadastral e
situação operacional do equipamento. Não contém password, token, chave ou
URL autenticada. `ip` é locador cadastral do destino; não é autorização por
si só. Ownership de `status`, `status_em` e `ultima_verificacao` continua no
subsistema de monitoramento conforme ADR-020.

### ConfiguracaoMonitoramento

Responsabilidade: vínculo efetivo entre uma câmera, um perfil, overrides
permitidos e referência de credencial. Contém somente dados não secretos ou
referências seguras; não replica o valor do segredo. Tem lifecycle próprio:
ativa, bloqueada, revisada e substituída conforme decisões futuras. Mudanças
de perfil, porta, endpoint, TLS, autenticação, referência ou bloqueio são
auditáveis como configuração.

### PerfilCapacidadeMonitoramento

Responsabilidade: catálogo versionado dos contratos que os adaptadores podem
executar. É reutilizável por câmeras compatíveis e define limites, portas,
protocolos, autenticação e parâmetros permitidos. Não é um cadastro livre de
fabricante/modelo nem uma licença para acessar qualquer destino.

### CredencialEquipamento

Responsabilidade: custódia de material de autenticação separado da câmera.
Contém referência, estado, escopo, versões e ciphertext protegido; nunca
plaintext em auditoria, histórico, resposta, template ou log. O acesso de
leitura/decriptação pertence somente ao serviço autorizado. Eventos de
criação, mudança de escopo, ativação/inativação, rotação, revogação e troca de
referência são auditáveis por referência, versão, câmera/configuração e
resultado sanitizado; o consumo normal pelo worker durante cada probe não é
`EventoAuditoria` funcional.

### Worker e infraestrutura

Responsabilidade: ler câmeras elegíveis, ler configuração/perfil, obter a
credencial mínima, conectar somente a destinos autorizados, persistir apenas
estado técnico/transições/incidentes permitidos e emitir telemetria
sanitizada. Firewall/egress, identidade de processo, permissões de banco e
proteção de chave pertencem à camada de infraestrutura e não são substituídos
por validação de formulário.

Captura não herda automaticamente a autorização do monitoramento. Uma
credencial ou perfil de monitoramento só pode ser reutilizado pela captura se
um contrato posterior conceder explicitamente esse privilégio.

## 6. Identidade e privilégio do worker

O futuro worker deverá:

- executar como conta/processo dedicado e sem necessidade de login
  interativo;
- não executar como root por necessidade do ARGOS;
- não reutilizar conta administrativa humana do Django;
- usar identidade de serviço com `worker_id` não secreto;
- ler somente câmeras/configurações elegíveis e perfis autorizados;
- obter/decriptar somente credenciais necessárias ao probe autorizado;
- usar usuário de banco dedicado e menor privilégio quando o worker for
  implementado;
- persistir apenas campos, transições e incidentes que o contrato lhe
  atribuir;
- acessar apenas egress/rede de CFTV permitidos;
- não aceitar do browser IP, URL, hostname, porta ou credencial para sondar;
- não possuir implicitamente privilégio de captura, administração do Django,
  acesso ao banco fora de sua função ou acesso irrestrito à VPS.

PostgreSQL é a direção de produção. A implementação futura deve usar conexão
autenticada, segredo do banco fora do código, TLS conforme a topologia,
backup protegido e ciphertext sem a chave mestra no mesmo backup. Nenhuma
configuração de banco ou infraestrutura é feita nesta etapa.

## 7. Threat model e SSRF

O alvo da análise é o worker, que pode receber configuração maliciosa,
processar dados alterados ou ser comprometido. O risco residual assume que
nenhuma camada é perfeita; por isso controles de aplicação e infraestrutura
são obrigatórios simultaneamente.

| Ameaça | Vetor | Impacto | Controle aplicacional | Controle infraestrutura | Risco residual |
|---|---|---|---|---|---|
| SSRF para loopback/localhost | URL, IP ou endpoint construído a partir de entrada | Acesso a serviços locais e bypass de fronteiras | destino derivado de `Camera.ip`; rejeição explícita de loopback e localhost; sem alvo arbitrário | egress sem loopback/serviços locais | Médio, se houver erro futuro de validação |
| Destino unspecified, link-local, multicast ou broadcast | Representação IP alternativa ou configuração inválida | Varredura, abuso de rede e ruído operacional | parsing estrito e bloqueio por classe especial; allowlist positiva | ACL/egress por sub-rede e porta | Baixo a médio |
| Metadata endpoint cloud ou rede administrativa | IP especial ou CIDR não autorizado | Exfiltração de tokens/configuração ou acesso lateral | deny por política e allowlist de CFTV; `TARGET_BLOCKED` | firewall/egress e segmentação do host | Médio, depende da topologia |
| DNS rebinding | Hostname resolve para IP permitido e depois proibido | Bypass da allowlist | DNS desabilitado no baseline; futuramente validar todos os IPs e revalidar no connect | firewall/egress | Baixo no baseline; médio se DNS for liberado |
| Redirect escape | Endpoint HTTP redireciona para destino não autorizado | SSRF indireto | redirects desabilitados; se liberados, validar cada hop | egress restrito | Baixo no baseline |
| Porta maliciosa | Override de porta ou alteração de configuração | Acesso a banco, painel ou serviço interno | intervalo + permissão do perfil + política do ambiente; porta não escolhida no probe | firewall por porta/protocolo | Médio |
| URL com userinfo | `user:secret@host` em endpoint | Vazamento de segredo e alvo disfarçado | userinfo proibido; URL montada internamente | inspeção/egress complementar | Baixo |
| IPv4 textual alternativo | Decimal, hexadecimal, octal ou forma ambígua | Bypass de bloqueios de IP | parser canônico e comparação após normalização | firewall com regras de rede | Baixo |
| Conexão à própria VPS ou ao banco | `Camera.ip` adulterado ou regra ampla | Leitura, alteração ou pivot interno | allowlist CFTV positiva e `TARGET_BLOCKED` | sub-rede/firewall sem rota de retorno indevida | Médio |
| Proxy ambiental inesperado | Variáveis/configuração herdada do processo | Desvio do destino e exposição de conteúdo | proxy desabilitado por default e configuração explícita | egress/proxy controlado | Baixo |
| Credential leakage | URL, exception, traceback, argumento, HTML, trace ou request dump | Comprometimento de câmeras e reutilização | schema allowlist de logs; segredo fora de Camera; sanitização antes de serializar | permissões, secret store, redaction central | Médio |
| Log leakage | Logs/EventoAuditoria armazenam payload ou header completo | Exposição persistente e ampla | categorias normalizadas e deny-by-contract; nunca Authorization/header/payload | retenção, acesso e criptografia de logs | Baixo a médio |
| Escalada de privilégio | Worker usa conta humana/root ou DB amplo | Controle do ARGOS, banco ou host | identidade dedicada e menor privilégio | usuário de serviço, sandbox, firewall, DB grants | Médio |
| Worker comprometido | Processo usa credenciais ou egress excessivos | Varredura, exfiltração, alteração de estados | escopo mínimo, alvo derivado, sem captura implícita | isolamento, egress, supervisão e rotação | Médio |
| Database leak | Backup contém configuração e ciphertext | Exposição de metadados; tentativa de recuperar segredos | ciphertext autenticado e chave fora do banco | backup protegido e chave em custódia separada | Médio |
| Master-key leak | Chave em código, banco, backup ou processo indevido | Decriptação em massa | chave fora do banco, acesso só ao worker autorizado, versões | secret store/host ACL, rotação e auditoria | Alto se ocorrer; blast radius reconhecido |
| Credential reuse | Uma credencial compartilhada referencia muitas câmeras | Comprometimento em massa após um vazamento | escopo, referência explícita, rotação, blast radius e privilégio mínimo | segregação por ambiente/segmento | Médio |
| Configuração maliciosa | Perfil/override libera scheme, path ou porta | Sondagem de destino indevido ou resultado falso | perfil versionado, override restrito, revisão/auditoria e revalidação no worker | allowlist/egress | Médio |

O controle de aplicação não é considerado suficiente isoladamente. Uma falha
de validação não deve conceder automaticamente acesso à VPS, ao banco ou à
rede corporativa.

## 8. Política de logs, traces e erros

O mecanismo futuro deve aplicar uma política de **allowlist de campos** antes
de construir a linha de log, métrica, trace, evento ou mensagem. Sanitizar
depois que o objeto secreto já foi interpolado é insuficiente.

Podem ser registrados, quando necessários:

- `camera_id` e referência da configuração;
- perfil/capacidade e versão;
- protocolo e categoria normalizada de resultado;
- duração/latência agregada;
- `worker_id`;
- código de erro sanitizado;
- transição técnica confirmada e referência de incidente;
- contagem, ciclo e métricas sem payload.

Por padrão não registrar:

- password, token, chave ou username sensível;
- Authorization, cookies ou headers completos;
- URL com segredo ou userinfo;
- request/response dump e payload ONVIF autenticado;
- traceback cru, exceção com contexto secreto ou argumento de processo;
- HTML, query string ou parâmetros de linha de comando contendo material de
  autenticação;
- IP real quando `camera_id` for suficiente.

Eventos de erro devem usar categorias como `TIMEOUT`, `CONNECTION_REFUSED`,
`AUTH_FAILURE`, `TLS_ERROR`, `PROTOCOL_ERROR`, `CONFIG_ERROR`,
`TARGET_BLOCKED`, `CANCELLED` e `INCONCLUSIVE`. A exceção crua nunca é estado
de domínio. Diagnóstico detalhado, se autorizado no futuro, deve ser gerado
em canal protegido, com sanitização anterior e retenção/acesso próprios.

Auditoria humana de configuração é separada da telemetria de probe:

- alteração de perfil, porta, endpoint, TLS, método de autenticação,
  referência/estado/versão de credencial e bloqueio é auditável;
- rotação registra quem, quando, escopo, versão e resultado sanitizado;
- acesso humano excepcional ou revelação, se algum dia permitido, é auditável
  sem registrar o segredo;
- o worker obter/decriptar a credencial para cada probe é consumo normal e
  não deve criar `EventoAuditoria` funcional por tentativa; pode aparecer em
  telemetria, métricas agregadas, access log do secret backend ou evento de
  segurança apropriado, conforme arquitetura futura;
- probe individual, retry, latência, `SUSPECT` e cancelamento são telemetria
  do worker;
- nenhum evento contém o valor secreto, valor anterior em texto, ciphertext
  exportável, token ou URL autenticada.

## 9. Invariantes de segurança

As seguintes regras são obrigatórias para qualquer implementação posterior:

- **S1.** Segredo nunca é persistido em plaintext.
- **S2.** Chave mestra não fica no mesmo banco, backup ou artefato do
  ciphertext.
- **S3.** Browser nunca informa destino arbitrário para probe.
- **S4.** Worker só conecta a destino autorizado por allowlist de ambiente e
  egress de infraestrutura.
- **S5.** Porta precisa ser válida e autorizada pelo perfil e pela política do
  ambiente.
- **S6.** URL, scheme, userinfo e redirect não podem escapar da allowlist.
- **S7.** Segredo nunca aparece deliberadamente em log, auditoria, trace,
  HTML, query string, erro ou argumento de processo.
- **S8.** Configuração incompleta ou bloqueada não gera `OFFLINE`.
- **S9.** `AUTH_FAILURE` é resultado técnico, não decisão automática de
  domínio.
- **S10.** Credencial não é atributo cadastral comum de `Camera`.
- **S11.** Conta humana não é identidade do worker.
- **S12.** Segurança de rede também existe fora da aplicação.
- **S13.** Configuração e segredo possuem lifecycle e auditoria separados.
- **S14.** Monitoramento não concede implicitamente privilégio de captura.
- **S15.** `Camera.ip` é locador de destino no baseline, não autorização; toda
  conexão deve repetir as verificações no worker.
- **S16.** DNS fica desabilitado até homologação; se liberado, todos os IPs e
  o destino no momento da conexão são revalidados.
- **S17.** Redirects ficam desabilitados no baseline.
- **S18.** Worker parado ou sem evidência fresca não marca câmeras `OFFLINE`.
- **S19.** Segredo compartilhado só é permitido com relacionamento,
  escopo, rotação e blast radius explícitos.
- **S20.** Probe individual, `CANCELLED`, `INCONCLUSIVE` e resultado
  intermediário não são transição de domínio.
- **S21.** Indisponibilidade transitória de secrets, chave, banco ou worker
  não altera elegibilidade nem produz `SAIU_DO_ESCOPO`, abertura/fechamento de
  incidente ou `OFFLINE`.
- **S22.** Credencial revogada, comprometida ou considerada insegura nunca é
  utilizada como fallback automático.
- **S23.** Somente identidade humana privilegiada pode alterar configuração
  que expanda a fronteira de segurança do monitoramento.
- **S24.** Segredo, chave e política são segregados por ambiente; cópia de
  banco não concede custódia utilizável em outro ambiente.
- **S25.** Consumo normal de credencial pelo worker não cria `EventoAuditoria`
  funcional por probe.

## 10. Decisões fechadas nesta etapa

- Custódia inicial preferencial: entidade de credencial separada, ciphertext
  autenticado em aplicação e chave mestra fora do banco; a recomendação não é
  implementação nem escolha de biblioteca.
- Credencial pode ser referenciada por várias câmeras somente com vínculo,
  escopo, versão, rotação e blast radius auditáveis.
- Configuração técnica é separada de segredo; não há senha em URL, Camera,
  HTML, auditoria, log ou erro.
- Capacidade é contrato versionado de perfil, com protocolo, porta, TLS,
  endpoint controlado, autenticação, exigência de credencial e probes
  declarados.
- A combinação recomendada é perfil reutilizável + override restrito por
  câmera.
- O baseline usa o IPv4 cadastrado, sem DNS/hostname, com destino derivado da
  câmera e não fornecido pelo browser.
- Allowlist por ambiente, portas por protocolo e egress de infraestrutura são
  obrigatórios.
- Redirects são desabilitados no baseline; qualquer futuro redirect exige
  revalidação a cada hop.
- Elegibilidade exige situação `PRODUCAO` e configuração completa, válida,
  ativa e autorizada; falha de configuração resulta em “não monitorada”, não
  em `OFFLINE`.
- Elegibilidade de domínio é distinta da prontidão transitória do subsistema;
  indisponibilidade de worker, banco, chave ou secret backend preserva o
  estado técnico e a elegibilidade.
- Rotação planejada pode manter temporariamente a versão anterior somente se
  ela continuar segura e a política permitir; credencial revogada ou
  comprometida nunca é fallback.
- Alteração que expanda a fronteira de segurança exige identidade humana
  privilegiada, least privilege, segregação de funções quando material e
  auditoria sem segredo.
- Segredos, master keys, allowlists e workers são segregados por ambiente; um
  banco copiado não transfere custódia utilizável.
- `AUTH_FAILURE` é resultado normalizado, sem interpretação automática como
  estado de domínio.
- O worker terá identidade dedicada, sem root, sem conta humana e com menor
  privilégio.
- Logs/traces/auditoria usam campos permitidos e categorias sanitizadas; probe
  individual não é evento de auditoria funcional, incluindo o consumo normal
  de credencial pelo worker.
- Monitoramento e captura não compartilham privilégio implicitamente.

## 11. Decisões adiadas

Exigem decisão posterior, evidência ou laboratório:

- biblioteca/primitive criptográfica concreta, formato de envelope e
  mecanismo de fornecimento da chave;
- secret manager, serviço de distribuição, usuário de banco e grants reais;
- CIDRs, portas, farms, segmentos e regras reais do parque;
- protocolo universal ou adaptador obrigatório;
- fabricante/modelo/firmware e capabilities reais;
- timeout, retry, backoff, frequência, jitter, concorrência, scheduler,
  anti-flapping e thresholds;
- DNS e política de redirects limitados, se o baseline for insuficiente;
- certificados, CA, mTLS e comportamento TLS por equipamento;
- usernames, passwords, tokens, paths RTSP, profiles ONVIF e valores de
  credenciais;
- firewall, egress, segmentação, deployment, supervisão e PostgreSQL reais;
- retenção de logs/métricas, alertas, health check e atualização da UI;
- privilégio, fluxo e reuso de credencial para captura de imagem.

## 12. Checklist de laboratório futuro

Coletar por fabricante/modelo/firmware quando relevante, sem colocar senha ou
URL autenticada nos artefatos:

- porta disponível e serviço correspondente;
- protocolo efetivamente suportado e autenticação exigida;
- TLS, certificado, CA, hostname exigido e falhas de validação;
- endpoint HTTP/HTTPS e comportamento de redirect;
- RTSP, path, autenticação, negociação e diferença entre stream e health;
- ONVIF, perfil, operações permitidas e diferença entre gestão e vídeo;
- comportamento sem autenticação e com credencial inválida;
- classificação de timeout, recusa, filtro, erro de protocolo e serviço
  incorreto;
- latência/jitter em condições normais, congestionamento, boot, reboot e
  recuperação;
- número de conexões simultâneas toleradas e impacto no equipamento;
- privilégios mínimos da conta e possibilidade de conta somente leitura ou
  específica de monitoramento;
- comportamento de rotação e janela segura de troca;
- conectividade host-worker, banco e rede de CFTV, incluindo ACL/egress;
- testes sintéticos em estágios de 50, 100, 500 e aproximadamente 2.300
  alvos, sem inferir capacidade real de câmeras a partir de cálculo;
- restart, shutdown, banco indisponível, duas instâncias e recuperação sem
  duplicar transições/incidentes.

## 13. Critério de encerramento de MON-02

MON-02 está documentalmente concluída e aprovada porque o contrato permite
responder, sem implementação real e sem ambiguidade:

1. onde o segredo fica conceitualmente e onde a chave não fica;
2. quem pode obter/decriptar cada credencial;
3. como câmera, configuração, perfil e credencial se relacionam;
4. como protocolo, porta, TLS, endpoint e capacidade são representados;
5. o que torna uma câmera elegível;
6. o que acontece com configuração ausente, inválida ou bloqueada;
7. quais destinos o worker pode alcançar;
8. como loopback, metadata, DNS rebinding, redirects, portas e proxy são
   tratados;
9. qual é a identidade e o privilégio do worker;
10. o que pode ou não entrar em log, trace e auditoria;
11. quais alterações de configuração/credencial são auditáveis;
12. quais dados ainda exigem laboratório real.

O estado “Aprovado” é documental e não autoriza migration, instalação, deploy,
acesso a câmera real, abertura de rede, criação de segredo ou promoção para
produção.

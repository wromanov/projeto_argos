# CAM-INT-02-R1 — Runtime Credential Resolution Boundary

```text
ID = CAM-INT-02-R1
STATUS = IMPLEMENTATION_READY
IMPLEMENTATION_READY = YES / LOCAL SERVICE BOUNDARY
IMPLEMENTATION = IMPLEMENTED / INTEGRATED / VALIDATED_LOCAL / PUBLISHED (PROJECT_STATE §50)
ACTIVITY = CAM-INT-02-R1-ARCH / DOCUMENTARY ADJUDICATION
BASELINE_HEAD = c0e5a954d8a2e290acb5ce86a1b699a10c02b190
RUNTIME_CREDENTIAL_RESOLUTION_OWNER = CAM-INT-02
CONSUMERS = CAM-INT-03; CAM-INT-04; future explicitly authorized adapters
PREDECESSORS = CAM-INT-02
SUCCESSORS = CAM-INT-03; CAM-INT-04
IMPLEMENTER_TARGET = LUNA / HIGH
IMPLEMENTATION_AUTHORIZED_BY_THIS_DOCUMENT = NO
BOUNDARY = INTERNAL / PUBLIC_TO_APPLICATION_CODE / NON_HTTP / NON_SERIALIZABLE / EPHEMERAL / FAIL_CLOSED
MIGRATION_EXPECTED = NO
```

## 1. Evidência e decisão

CAM-INT-02 publicou custódia, versões e lifecycle em
`cameras/integracao/credentials.py`, provider em `key_provider.py` e schema em
`cameras/models.py`/migration `0016`. Há serviços públicos de gestão,
metadados, reveal e rotação de chave; `_decrypt` é privado. Não existe serviço
público de resolução operacional. `resolve_connection_config` retorna apenas
configuração não secreta e não entrega um `CameraConnectionConfig` nem segredo.
Esse é um gap de boundary, não de schema e não uma falha de CAM-INT-03.

DECISÃO: CAM-INT-02-R1 acrescentará a API interna abaixo ao módulo de
credenciais existente. CAM-INT-03/04 consomem somente essa API e seu valor
efêmero; crypto, ciphertext e provider permanecem sob ownership CAM-INT-02.
O contrato pai continua normativo para custódia e lifecycle. Este contrato
fecha somente execução interna, sem endpoint, implementação ou homologação.

## 2. API, entrada e saída

Assinatura contratada (declaração documental, não implementação):

```text
cameras.integracao.credentials.resolve_active_credential_for_execution(
    *, config: CameraConnectionConfig
) -> ResolvedCameraCredential
```

`config` é instância persistida de `CameraConnectionConfig`, selecionada pelo
caso de uso confiável para a câmera cuja operação já foi autorizada. Não é
dict de browser, resultado de `resolve_connection_config`, instância fabricada
sem persistência, ID arbitrário de versão ou objeto fornecido pelo adapter.
A seleção e a validação não secreta da conexão permanecem no caso de uso e na
boundary de configuração; o resolver recebe o mesmo config da operação.

O resolver relê a configuração pelo PK e compara `camera_id`, `config_version`,
`credential_id`, `profile_id`, `enabled`, `rtsp_uri`, `http_endpoint_override`,
`http_port_override` e `transport` com a entrada. Não confia em relações
cacheadas nem em alterações não salvas. Configuração inexistente, não
persistida ou divergente falha fechada; não escolhe outra configuração.
Não há argumentos públicos `actor`, `current_password`, `ciphertext`,
`key_version`, `version_id` ou `key_provider`. Provider de teste é substituído
na composição interna de CAM-INT-02 (por exemplo, mock da factory existente),
sem superfície de injeção oferecida aos adapters.

`ResolvedCameraCredential` pertence ao mesmo módulo e contém somente
`username` e `password`, respeitando o schema/limites existentes (255/1024).
Não é necessário retornar identificador de versão nesta slice. É value object
imutável/frozen, sem relação ORM, Model, serializer, response DTO, método de
exportação ou conversão para dict/JSON. Ambos os campos são excluídos de repr;
repr e str são fixos/sanitizados. Serialização JSON/pickle não é suportada;
pickle deve ser recusado explicitamente. Uso de serializadores genéricos,
`asdict`, introspecção para exportação, cache, fila ou persistência é proibido.
Isso é contrato de aplicação, não isolamento contra código Python hostil no
mesmo processo.

Não retorna ciphertext, chave, provider, `key_version` ou objetos de domínio
que permitam navegar até esses valores. O caller só entrega os dois campos ao
port de autenticação em memória da tentativa autorizada. O resultado não
concede acesso genérico a outras câmeras, versões ou segredos.

## 3. Autorização: execução versus reveal humano

| Operação | Fronteira de autorização | Resultado e auditoria |
|---|---|---|
| HUMAN_REVEAL | `reveal_camera_credential`; POST+CSRF; confirmação da senha atual do ator; câmera e ator verificados pelo serviço existente | retorno explícito ao humano autorizado, `no-store`; evento `camera.credential.revealed` |
| Diagnóstico manual | view e serviço do caso de uso verificam `run_camera_connection_test` para a câmera antes de resolver segredo ou chamar port/rede | diagnóstico sanitizado e auditado pelo caso de uso; segredo somente na tentativa |
| Captura manual | view e serviço do caso de uso verificam `capture_camera_image` antes de resolver segredo ou chamar port/rede | bytes seguem IMG-CAP; auditoria própria da captura, sem segredo |
| Worker automático | execução interna confiável, câmera/configuração elegíveis, compatibility/capability e destino validados segundo CAM-INT-01/06/07 e MON-WORKER | somente versão ativa da câmera selecionada; nenhum Django User fictício ou Group humano |

O resolver valida vínculo, integridade e lifecycle da credencial. Não autentica
usuário humano nem substitui permissões, elegibilidade, target policy,
compatibilidade ou ownership/fencing do caso de uso. Importar uma função ou
possuir um objeto config não prova autorização externa; somente código interno
confiável após esses gates pode chamá-la. Não criar identidade de serviço de
produção nesta slice; sua entrega operacional continua em PROD-TOPO.

EXECUTION_RESOLUTION não é HUMAN_REVEAL. Adapter e worker não recebem nem
precisam de `reveal_camera_credential`, reautenticação humana ou permissão de
metadados para essa resolução. Não reutilizar endpoint/serviço de reveal nem
`credential_metadata` para obter material de execução.

## 4. Algoritmo, integridade e concorrência

1. Validar a entrada persistida e reler o config factual conforme §2.
2. Obter somente `config.credential`; vínculo ausente é erro, nunca busca de
   outra credencial por câmera ou fallback anônimo.
3. Exigir `credential.camera_id == config.camera_id`.
4. Exigir `credential.active_version_id` definido. A versão é escolhida por
   esse ponteiro, nunca por maior número, busca da última ACTIVE ou caller.
5. Exigir `active_version.credential_id == credential.pk` e coerência da
   única versão ACTIVE com o ponteiro. Referência cruzada/inconsistência falha.
6. Exigir `CameraCredential.state == ACTIVE` e
   `CameraCredentialVersion.state == ACTIVE`. PENDING, RETIRED e REVOKED são
   recusadas, mesmo que uma referência corrompida aponte para elas.
7. Obter provider exclusivamente dentro de CAM-INT-02. Decrypt usa somente a
   `key_version` da linha selecionada por `key_for_version`, sem tentativas
   em outras chaves e sem exigir a chave ativa de encrypt para ler versão
   legítima cifrada com uma chave anterior ainda disponível.
8. Decrypt e validar schema/username/password dentro de CAM-INT-02,
   reutilizando `_decrypt` apenas dentro desse módulo.
9. Retornar o value object efêmero e encerrar a transação antes de rede/port.
   Nenhuma escrita, plaintext persistido ou log é produzido pelo resolver.

A releitura, checagem de ponteiro/estado e decrypt formam uma operação
transacional coerente com replace/revoke/rotate existentes: serialização pela
mesma linha `Camera` primeiro, depois config/credential/versão quando houver
locks adicionais, sem inversão da ordem dos serviços de lifecycle. Não manter
locks durante socket, GStreamer, HTTP ou processamento de imagem. O serviço
não congela um segredo no config: cada nova tentativa resolve o ativo atual.

Rotação/revogação concluída antes da resolução deve ser observada. Não prometer
revogar retroativamente bytes já entregues a uma tentativa em andamento nem
zeroização garantida de strings Python. Tentativas em curso seguem deadline e
cancelamento próprios dos consumers; ao terminar/falhar/cancelar, liberam o
objeto e as propriedades/client auth que retiverem material. Sem cache entre
tentativas, sem fallback para versão retirada ou revogada e sem reuso em retry.
Validação concorrente real em PostgreSQL permanece um gate de produção.

Perfil sem autenticação pode seguir o fluxo explicitamente não autenticado
contratado pelo consumer sem chamar o resolver. Quando a operação exige
autenticação ou decide usar o vínculo configurado, erro do resolver nunca
permite continuar anônimo, alterar método ou experimentar senha antiga.

## 5. Falhas públicas sanitizadas

Todas as falhas previstas abaixo retornam/levantam `CredentialOperationError`
com somente `.code` fechado e str/repr seguros, sem payload, URL, chave ou
exception chain com segredo. Não propagar exceção crua do provider/Fernet.

| Código | Condição / relação com taxonomia publicada |
|---|---|
| `CONFIGURATION_NOT_ALLOWED` | Novo em R1: config não persistido/inexistente ou divergência dos campos comparados em §2; consumer deve reiniciar sua resolução não secreta, nunca continuar com destino antigo |
| `CREDENTIAL_NOT_CONFIGURED` | Existente: vínculo configurado ausente ou credencial referenciada inexistente |
| `CROSS_CAMERA_REFERENCE` | Novo em R1: credencial de outra câmera ou ponteiro de versão pertencente a outra credencial |
| `NO_ACTIVE_VERSION` | Novo em R1: ponteiro ativo nulo; inclui revogação normal que o zera, sem procurar versão anterior |
| `VERSION_NOT_ALLOWED` | Novo em R1: owner INACTIVE, versão PENDING/RETIRED/REVOKED, estado inválido ou incoerência entre ponteiro e única ACTIVE |
| `KEY_MISSING` | Existente: provider informa ausência de material necessário; normalizar para esse mesmo erro seguro |
| `KEY_INVALID` | Existente: entrega/configuração ou material de chave inválido |
| `KEY_VERSION_UNKNOWN` | Existente: provider não possui a key_version da linha, inclusive provider vazio; é o comportamento factual de `key_for_version` |
| `DECRYPT_FAILED` | Existente: token adulterado, assinatura inválida, erro de decode/JSON/schema ou payload inválido; TAMPERED_CIPHERTEXT é coberto por este código, sem novo detalhe/oráculo público |

Não exigir `active_key()` para resolver: ausência de chave de encrypt ativa
não implica ausência da chave exata de decrypt. Testes de chave ausente cobrem
provider vazio (`KEY_VERSION_UNKNOWN`) e provider que informa `KEY_MISSING`.
Esses nomes novos pertencem somente à API R1; não renomear erros de reveal.
Qualquer falha bloqueia autenticação antes de port/rede, sem fallback. Consumer
pode mapear falhas para seu diagnóstico seguro de configuração/auth, neutro
para disponibilidade; nunca inferir OFFLINE da resolução malsucedida.

## 6. Segredo e auditoria

```text
PLAINTEXT_IN_DATABASE = NO
PLAINTEXT_IN_LOG = NO
PLAINTEXT_IN_AUDIT = NO
PLAINTEXT_IN_EXCEPTION = NO
PLAINTEXT_IN_NORMAL_RESPONSE = NO
AUTHENTICATED_URI_PERSISTED = NO
AUTHENTICATED_URI_CONSTRUCTED = NO
CIPHERTEXT_DIRECTLY_EXPOSED_TO_ADAPTER = NO
KEY_PROVIDER_DIRECTLY_EXPOSED_TO_ADAPTER = NO
NO_NEW_AUDIT_EVENT_REQUIRED = YES
```

Username e password são sensíveis. Resolver não escreve eventos nem transforma
probe/captura em reveal. Preservar `camera.credential.created`, `.replaced`,
`.revealed`, `.revoked`, `.key_rotated` e auditoria de falha de reveal existente;
preservar auditoria sanitizada do diagnóstico/captura no caso de uso externo.
BC-AUTH e CAM-INT-02 já determinam ausência de evento funcional por probe.
Não criar telemetria de uso por resolução nem novas métricas de cardinalidade.

CAM-INT-03/04 não importam helper privado, leem ciphertext, acessam provider,
duplicam crypto, usam reveal ou montam URI autenticada. RTSP usa propriedades
em memória `user-id`/`user-pw`; HTTP usa auth Basic/Digest do client autorizado,
conforme seus contratos. Nenhum desses valores integra request serializável,
resultado diagnóstico, log, trace, auditoria ou resposta normal.

## 7. Ownership da implementação futura

```text
PRIMARY_FILES = cameras/integracao/credentials.py
SHARED_FILES = cameras/integracao/key_provider.py; cameras/models.py;
               cameras/integracao/configuration.py (read-only contracts/evidence)
TEST_FILES = cameras/test_camera_credential_resolution.py (new);
             cameras/test_camera_credentials.py (existing regression)
MODEL_CHANGE = NONE
MIGRATION_EXPECTED = NO
DATA_MIGRATION = NO
DEPENDENCY_CHANGE = NO
ADAPTER_CODE_OWNERSHIP = CAM-INT-03 / CAM-INT-04, outside R1
GLOBAL_CONTINUITY_OWNER = INTEGRATION_GATE
```

Adicionar API/value object ao módulo existente; não promover `_decrypt` a API
de adapter. Factory/provider, models e configuração são evidência compartilhada,
sem alteração esperada. Não mudar permissões, reveal, URLs, views, adapters ou
requirements em R1. Necessidade material de schema, novo método de auth,
provider operacional ou contradição nova exige parada e adjudicação Sol.

## 8. Contrato de testes e aceite

Testes locais determinísticos, provider sintético em memória e consumer/port
fake; sem câmera/rede real. O contrato exige:

1. Config persistido e autorizado resolve somente o ponteiro ACTIVE da mesma
   câmera; retorno contém apenas username/password e não models/provider.
2. Ausência de vínculo/ponteiro, owner INACTIVE, PENDING, RETIRED, REVOKED,
   referência cross-camera/cross-credential e incoerência de ponteiro falham
   conforme §5, antes de decrypt quando a falha for de integridade.
3. Versão antiga segura existente nunca é tentada após qualquer erro; rotação
   entre duas resoluções seleciona somente a nova ACTIVE; revogação anterior
   à chamada bloqueia resolução; relações cacheadas não contornam releitura.
4. Config não salvo, excluído, modificado sem salvar ou obsoleto por troca de
   config_version/vínculo/câmera é recusado sem port/rede.
5. Provider vazio, versão de chave desconhecida, KEY_MISSING, chave inválida,
   token adulterado e payload/schema inválido falham sem expor detalhe secreto;
   chave de decrypt anterior disponível funciona sem chave ativa de encrypt.
6. Frozen, repr/str sanitizados, ausência de exportadores e recusa de
   serialização JSON/pickle; DB não contém username/password/chaves e preserva
   somente o ciphertext já contratado. Logs capturados, auditoria e erros/chains
   não contêm username/password/ciphertext/chaves. Não há persistência do retorno.
7. Consumer fake recebe só o value object, nunca ciphertext/provider; falhas
   impedem sua chamada. A revisão de imports confirma ausência de crypto e
   dependências privadas nos consumers quando implementados nessas slices.
8. Resolução bem-sucedida ou negada não cria `.revealed` nem outro evento novo
   e não chama `authenticate`/reveal/checagem de permission humana. Funciona
   sem actor e sem `reveal_camera_credential`; a regressão de reveal continua.
9. Caso de uso fake manual aplica sua permission externa antes de resolver:
   ator sem `run_camera_connection_test`/`capture_camera_image` não chega ao
   resolver/port. Esse teste de composição não implementa endpoints/adapters
   em R1; consumers reais repetem o gate em suas próprias slices.

| Critério | Aceite objetivo |
|---|---|
| AC-R1-01 | Consumer interno autorizado obtém em memória somente username/password da ACTIVE configurada, sem ciphertext, provider ou seleção arbitrária de versão. |
| AC-R1-02 | Credencial/config ausente, inválida, obsoleta, retirada, revogada, cross-camera ou indecriptável falha fechada antes de rede, sem fallback. |
| AC-R1-03 | Resolução não persiste/exporta/loga segredo nem gera human reveal; repr/str/erros seguros, value object efêmero e permissões externas preservadas. |
| AC-R1-04 | RTSP e HTTP autenticados usam a mesma API pública interna; responsabilidade criptográfica permanece em CAM-INT-02, sem migration ou acesso privado nos consumers. |

API, input, output, failures, autorização, invariantes, ownership e testes estão
fechados; R1 é IMPLEMENTATION_READY. CAM-INT-03 permanece
PAUSED_ARCHITECTURAL_DEPENDENCY até implementação, integração, validação e
publicação de R1. CAM-INT-04 também depende de R1 para autenticação; seu trabalho
local observado não é avaliado nem declarado concluído por esta adjudicação.
Contrato pronto não equivale a resolver publicado ou autorização de retomada.

## Estado de publicação (2026-10-08)

O serviço R1 está publicado e sua API permanece a única boundary autorizada
para resolução runtime de credenciais. O finding HTTP-R1-CALLSITE-01 é
responsabilidade do consumer IMG-CAP: CAM-INT-04 fornece o adapter; o worker
IMG-CAP verifica autorização e TargetPolicy, resolve pela API R1 e só então
chama o adapter. A integração local passou nos testes de resolução de credencial
(12/12), adapter HTTP Snapshot (15/15) e capture service (16/16), sem fallback
inseguro nem exposição de credenciais. O finding está RESOLVED para a slice
local; isso não declara homologação de câmera ou credencial real.

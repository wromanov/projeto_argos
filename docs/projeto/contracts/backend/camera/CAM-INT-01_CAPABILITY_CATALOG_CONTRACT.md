# CAM-INT-01 — Catálogo de capabilities de câmera

```text
STATUS = ACTIVE / CONTRACT BASELINE
MODEL_IMPLEMENTATION = NOT_PRESENT
BC02_STATUS = IMPLEMENTATION_READY
IMPLEMENTATION_READY = YES
IMPLEMENTER_TARGET = LUNA
```

## Contrato

Uma capability é uma afirmação versionada e evidenciada sobre o que um modelo/firmware pode fazer por determinado protocolo e perfil. Ela limita a seleção de adapter; não é, por si só, autorização para alcançar o dispositivo nem prova de que o recurso funciona na unidade instalada.

O perfil conceitual de `ADR-021` deve declarar: protocolo/adapter; porta permitida; política TLS; endpoint/path controlado; método de autenticação; requisito de credencial; probe primário/secundário e o que o resultado comprova; parâmetros estritamente necessários; compatibilidade de fabricante/modelo/firmware; versão e estado ativo. Configuração comum fornece defaults e limites; override por câmera só é permitido para campos declarados sobrescrevíveis.

## Registro e evidência

Cada capability futura deve identificar fonte (datasheet, laboratório ou validação de unidade), firmware/escopo aplicável, validade, limitações, ambiente e versão. Compatibilidade ausente ou ambígua significa `UNVERIFIED`, nunca suporte presumido. Nenhum inventário automático de fabricante/modelo ou endpoint universal é inferido dos campos cadastrais.

O catálogo não armazena segredo, URL arbitrária, senha, token ou stream path com material de autenticação. Segredos são referenciados por identificador opaco segundo CAM-INT-02. Destination policy e allowlist permanecem responsabilidade do hardening.

## Estado observado e adiamentos

`Camera` tem texto livre para fabricante/modelo e campos como `tipo`, `codec`, `farm` e IP; no checkout BC-02 ainda não há model de catálogo, perfil ou configuração efetiva. Tipos cadastrais não equivalem a capabilities. O baseline é IP IPv4 cadastrado, DNS desabilitado e perfil compartilhado com override restrito. O schema local é fechado abaixo; dados reais compatíveis aguardam evidência de laboratório.

Referências: ADR-021 §§3.5–3.6; `cameras/models.py`; `CAM-INT-03`, `CAM-INT-04`, `CAM-INT-06`.

## BC-02 — schema e seleção implementáveis

`CameraCapabilityProfile` é entidade versionada e não secreta, com
`profile_key` estável, `version` inteiro positivo, `active`, `adapter_key`
(`RTSP`/`HTTP_SNAPSHOT`), `allowed_schemes`, `allowed_ports`, política de TLS,
`auth_method` (`NONE/BASIC/DIGEST/RTSP_NEGOTIATE`), `credential_required`,
`endpoint_policy` (`PROFILE_FIXED` ou
`TECHNICIAN_OVERRIDE`), path default relativo opcional, `allowed_override_fields`,
`probe_evidence_stage` e `source_ref`/`created_at`/`created_by`. A combinação
`(profile_key, version)` é única; versões são imutáveis depois de ativadas.
Campos estruturados de lista usam JSON validado em service (scheme/porta/
override em allowlist fechada), nunca JSON arbitrário enviado ao adapter.
Perfil não contém username/password nem URI com userinfo. Desativar um perfil
impede novas execuções que o referenciem; não apaga histórico de configuração.

`CameraConnectionConfig` tem relação 1:1 com `Camera` e FK protegida para
Profile, `enabled`, `rtsp_uri` normalizada sem credencial (opcional até a
configuração existir), `http_endpoint_override` relativo e
`http_port_override` opcionais para profile HTTP, `transport`
(`AUTO`, `TCP`, `UDP`) para RTSP, referência opaca à
credencial ativa quando exigida, `config_version` positivo e timestamps/ator
da última alteração. Porta opcional da URI: resolver a porta do perfil,
`554` somente para RTSP quando o perfil não fixar outra; a porta efetiva deve
estar em perfil **e** policy de ambiente. `Camera.ip` continua a fonte do
host. Codec é descoberto pelo resultado C/D e registrado como diagnóstico,
não inferido de `Camera.codec` cadastral nem obrigatório na configuração.
Stream/profile não é campo obrigatório. O path informado por Técnico/Admin
é override da URI, permitido apenas em profile com
`TECHNICIAN_OVERRIDE`, validado sem segredo, fragmento, query secreta ou
destination override. A referência de credencial é adicionada ao schema da
Config pela migration CAM-INT-02; CAM-INT-01 não referencia model futuro.
A URI salva não é argumento de probe vindo da UI.

Existe perfil seed `RTSP_DISCOVERY_V1`, sem declaração de suporte por
fabricante: `rtsp`, porta default 554, auth `RTSP_NEGOTIATE`, credencial
opcional, `TECHNICIAN_OVERRIDE` somente para path/porta dentro da policy,
transport `AUTO`; permite **somente teste manual** sob autorização e allowlist;
resultado fica `UNVERIFIED` até evidência CAM-INT-06. Não iniciar monitoramento
automático nem captura com perfil/evidência `UNVERIFIED`. Não criar linhas
`SUPPORTED` por default. Mudança de perfil/URI/porta/credencial incrementa
`config_generation` via serviço transacional e audita sem URI completa.

```text
MODEL_CHANGE = CameraCapabilityProfile + CameraConnectionConfig
MIGRATION_REQUIRED = YES
EXPECTED_MODELS = CameraCapabilityProfile; CameraConnectionConfig
RELATIONSHIPS = Camera 1:1 Config; Profile 1:N Config; Credential reference optional
CONSTRAINTS = unique(profile_key,version); config_version > 0; one Config/Camera
INDEXES = profile(active,adapter_key); config(enabled,profile_id)
DATA_MIGRATION = YES / seed idempotente RTSP_DISCOVERY_V1 sem vendor SUPPORTED;
                 existing cameras start without technical config
ROLLBACK_CONSIDERATION = disable configs first; preserve profile/version audit
EXPECTED_PRIMARY_FILES = cameras/models.py; cameras/integracao/configuration.py
EXPECTED_NEW_FILES = cameras/integracao/capabilities.py
EXPECTED_TEST_FILES = cameras/test_camera_capabilities.py; cameras/test_camera_connection_config.py
SHARED_FILES = cameras/models.py; cameras/migrations; configuration resolver
STOP_AND_ESCALATE_TO_SOL_IF = profile needs arbitrary target/secret endpoint;
                              schema cannot represent a required approved mode
```

Acceptance criteria:

1. Dado perfil/version ativo, configuração valida somente scheme, porta,
   endpoint e override permitidos; alteração de versão ativa é rejeitada.
2. Dada câmera sem perfil ou com compatibilidade `UNVERIFIED`, execução
   automática/captura é bloqueada; teste manual privilegiado permanece
   possível com `RTSP_DISCOVERY_V1` e policy de destino aprovada.
3. Dada mudança técnica, `config_generation` cresce e completion antiga não
   grava estado; dado cadastro livre `fabricante/modelo/codec`, nenhuma
   capability é inferida.

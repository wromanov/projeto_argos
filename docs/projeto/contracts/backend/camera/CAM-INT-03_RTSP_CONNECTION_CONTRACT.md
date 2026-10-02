# CAM-INT-03 — Conexão RTSP

```text
STATUS = ACTIVE / ADAPTER CONTRACT; NOT HOMOLOGATED
RTSP_ADAPTER_IMPLEMENTED = NO
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL ADAPTER AND FAKE
IMPLEMENTER_TARGET = LUNA
EXECUTION_STATUS = PAUSED_ARCHITECTURAL_DEPENDENCY
READY_NOW = NO / CAM-INT-02-R1 NOT_PUBLISHED
REQUIRED_PREDECESSORS = CAM-INT-01; CAM-INT-02; CAM-INT-02-R1; CAM-INT-06; CAM-INT-07
```

## Semântica

RTSP não é um health check universal. Sucesso de conexão, autenticação, negociação de sessão, leitura de stream e decodificação de vídeo são evidências diferentes; um adapter só pode afirmar a capacidade efetivamente verificada. Um probe RTSP não se torna automaticamente captura de snapshot, prova de gravação VMS ou saúde completa da câmera.

## Fronteira futura do adapter

O adapter receberá request tipado criado a partir de câmera elegível e perfil validado, nunca URL arbitrária do browser. O endpoint RTSP deve ser relativo/controlado pelo perfil; userinfo é proibido; credencial é resolvida por referência autorizada e injetada sem compor/logar URL textual. IP IPv4, porta e path são validados contra profile e allowlist antes da conexão. Timeout é bounded e cancelamento não altera estado técnico. Redirect, DNS, proxy ambiental e transporte não homologado ficam desabilitados por padrão.

O adapter retorna apenas categoria fechada, timestamp UTC aware, duração monotônica não negativa e código de erro sanitizado, seguindo `ProbeRequest`/`ProbeResult`. Conteúdo de stream, headers e credenciais não são persistidos pelo contrato de monitoramento.

## Homologação requerida

Validar modelos/firmwares reais, transporte e modo de autenticação, timeout de connect/read, encerramento de sessão, limite de bytes/frames, vazamento em erros/logs, impacto no equipamento e o que o sinal comprova. Falha de auth/configuração deve ser neutra para transição de disponibilidade. Não existe escolha de RTSP como mecanismo universal nem acesso de rede homologado neste baseline.

Referências: ADR-019 itens em aberto; ADR-021 §§3.5–3.8, 4, 7–9; `cameras/monitoramento/contracts.py`.

## BC-02 — persistência, discovery e adapter

Técnico/Admin informa URI RTSP **na configuração**, com permissão
`change_camera_connection`; Operador só a lê sem credencial. Persistir URI
normalizada em `CameraConnectionConfig.rtsp_uri`, sem username/password,
fragmento ou query. Scheme V1 somente `rtsp`; host é IPv4 canônico e igual
ao `Camera.ip` cadastrado, validado também em CAM-INT-07. Porta opcional:
usar porta do profile ou 554; override só se profile e policy permitem.
Path é permitido apenas pelo profile/override restrito, com limite 256,
path absoluto iniciado por `/`, sem CR/LF, percent-encoding ambíguo, `..`,
userinfo ou material de autenticação. URI contendo token/segredo no path não
é suportada em V1: requer outro contrato de secret reference. `transport`
default `AUTO`; `TCP`/`UDP` somente quando profile/policy permitem. AUTO
negocia dentro de um único orçamento, sem multicast; não faz fallback para
destino não autorizado. Codec vem de SDP/recebimento, não é obrigatório nem
inferido de `Camera.codec` cadastral. Stream/profile ONVIF é opcional e não
pré-requisito V1.

`RtspAdapter` recebe request tipado resolvido por `camera_id`, destino/URI
validado, referência de credencial e deadline monotônico; nunca URI de request
de browser. A/B/C/D: A TCP reachability do IPv4/porta; B resposta válida à
negociação RTSP; C DESCRIBE/SDP com mídia de vídeo e codec identificável; D
entrega de frame/mídia decodificada válida. D PASS é a única evidência de
`SUCCESS` para monitoramento; C PASS sozinho não é ONLINE. Teste manual
executa A→B→C→D e devolve resultados por estágio com status
`PASS/FAIL/NOT_RUN`, categoria fechada, UTC, duração e error code seguro,
sem mudar estado/streak/incidente. Falha em A/B/C interrompe estágios seguintes.

Backend real escolhido para recepção/decodificação: `GStreamer rtspsrc` +
depay/decoder + `appsink`, com `user-id`/`user-pw` em propriedades em memória,
sem subprocesso ou credencial em URL/linha de comando. O adapter de
GStreamer é plugin opcional: import/instalação ausente resulta
`ADAPTER_UNAVAILABLE` operacional e readiness false para RTSP, sem OFFLINE;
fake determinístico implementa o mesmo port localmente. Não ativar conector
real em ambiente sem policy/egress aprovados. Nenhuma versão de GStreamer ou
plugin de codec é presumida como instalada; PRODUCTION_TOPO valida empacotamento
e codecs reais. O port expõe `describe`/`receive_one_frame` e cancelamento;
um decoder indisponível é `INCONCLUSIVE/CONFIG_ERROR`, não falha de câmera.

Timeout total usa `MonitoringConfig.probe_timeout_seconds` (1–30 s), connect
até `connect_timeout_seconds`, cada estágio consome o saldo restante; não
existe retry interno para resultado negativo. Cancelamento fecha sessão e
descarta bytes, sem transição. Resultado bruto/SDP/frame não entra em log,
histórico de probe ou auditoria. Erros normalizados em `TIMEOUT`,
`CONNECTION_REFUSED`, `AUTH_FAILURE`, `PROTOCOL_ERROR`, `CONFIG_ERROR`,
`TARGET_BLOCKED`, `CANCELLED`, `INCONCLUSIVE`; auth/config/policy/codec são
neutros para reducer. Validação real por firmware/transporte/câmera fica externa.

```text
MODEL_CHANGE = CameraConnectionConfig from CAM-INT-01; no additional table
MIGRATION_REQUIRED = NO IN THIS SLICE / CAM-INT-01 creates schema
EXPECTED_MODELS = CameraConnectionConfig
RELATIONSHIPS = profile and credential references from predecessors
CONSTRAINTS = URI/port/transport validated by service and target policy
INDEXES = NONE NEW
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = disable RTSP adapter/config, preserve URI audit
EXPECTED_PRIMARY_FILES = cameras/integracao/configuration.py
EXPECTED_NEW_FILES = cameras/integracao/rtsp/ports.py; cameras/integracao/rtsp/gst_adapter.py;
                     cameras/integracao/rtsp/fake.py
EXPECTED_TEST_FILES = cameras/test_camera_rtsp_uri.py; cameras/test_camera_rtsp_adapter.py
SHARED_FILES = configuration resolver read-only; integration views/urls later
STOP_AND_ESCALATE_TO_SOL_IF = required codec/protocol not representable;
                              GStreamer cannot satisfy no-secret-URI boundary;
                              product requires hostname/query-secret/ONVIF V1
```

Acceptance criteria:

1. URI com userinfo, hostname, host diferente do `Camera.ip`, query,
   fragmento, path/porta fora do profile/policy é rejeitada antes de socket;
   URI válida é persistida normalizada e lida sem credencial.
2. Fake emite A/B/C PASS e D FAIL: teste manual mostra D FAIL, monitoramento
   não recebe SUCCESS nem grava estado. Fake A/B/C/D PASS produz um SUCCESS
   somente no fluxo automático, sujeito ao reducer existente.
3. Timeout/cancelamento fecha recursos dentro do deadline, sem retry oculto;
   erro de auth/codec é neutro; falta de GStreamer sinaliza indisponibilidade
   do adapter sem declarar câmera OFFLINE.

Referências do backend escolhido: [rtspsrc](https://gstreamer.freedesktop.org/documentation/rtsp/rtspsrc.html)
e [appsink](https://gstreamer.freedesktop.org/documentation/app/appsink.html).

## CAM-INT-02-R1 — dependency de resolução de credencial

`IMPLEMENTATION_READY` acima qualifica o contrato local do adapter, não
`READY_NOW`. CAM-INT-03 parou corretamente no gate e permanece
`PAUSED_ARCHITECTURAL_DEPENDENCY`, blocker CAM-INT-02-R1, até implementação,
integração, validação e publicação dessa boundary. CAM-INT-06/07 continuam
dependencies independentes; readiness ambiental não é promovido por R1.

O caso de uso interno autorizado seleciona o `CameraConnectionConfig`
persistido da operação e chama exclusivamente
`cameras.integracao.credentials.resolve_active_credential_for_execution(*, config)`.
O port RTSP recebe somente `ResolvedCameraCredential` efêmero e usa
username/password em propriedades em memória, fora do request serializável.
Input, falhas e lifetime são normativos no
[contrato R1](CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md).
Resolução falha antes de port/rede, sem fallback de senha/versão ou fluxo
anônimo; o resultado de configuração/auth continua neutro para disponibilidade.

Proibidos: importar/chamar `_decrypt` ou helper privado; ler ciphertext/model
de versão para decrypt; acessar `CredentialKeyProvider`; duplicar crypto;
reutilizar reveal endpoint/serviço ou metadados; montar credencial em URI RTSP.
Caller manual aplica `run_camera_connection_test` antes do resolver; worker
aplica elegibilidade/compatibilidade/destino e ownership do seu caso de uso,
sem permission reveal ou User fictício. Resolver não audita human reveal.
Na implementação do adapter, testar a composição com a API R1, negação antes
da chamada, erro seguro sem port/rede e ausência de imports privados/crypto.

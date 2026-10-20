# Integração de captura de imagem

```text
ID = IMG-CAP
STATUS = ACTIVE / COMPLEMENT TO CANONICAL IMAGE DOMAIN
DOMAIN_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL CAPTURE PIPELINE
IMPLEMENTER_TARGET = LUNA
```

## Fronteira

Captura de câmera é ação explícita, autorizada e desacoplada do monitoramento. Não captura automaticamente na primeira detecção, em probe, em transição ou em retorno `OFFLINE -> ONLINE`. Captura direta e upload manual são proveniências distintas (`CAPTURA_CAMERA`, `UPLOAD_MANUAL`) no mesmo `CameraImageRecord`; não criar tabela, histórico ou regra de latest paralelos.

Futuro fluxo de captura: autenticar/autorizar operador ou identidade de serviço de captura; resolver camera e capability homologada; validar destino com CAM-INT-07; resolver somente credencial autorizada CAM-INT-02; obter resposta bounded; validar formato/bytes e integridade no servidor; armazenar via abstração privada; criar registro com `captured_at` observado e `recorded_at` do servidor, origem, executor e checksum; auditar ação sem segredo. Falha não cria registro AVAILABLE, não muda saúde nem mascara estado de captura corrente.

## Leitura e entrega

O domínio canônico determina ordenação de `LATEST_CAMERA_CAPTURE`, ausência de fallback para captura antiga quando a latest falha, `DISPLAY_IMAGE` com upload manual somente quando nenhuma captura existe, preview privado, hash/integridade, variants fechadas, autorização `cameras.view_camera`, `nosniff` e `no-store`. IMG-CAP não redefine esses contratos; remete às seções 7, 18, 19, 24 e 25 do documento canônico.

Upload manual atual é implementado com `cameras.add_cameraimagerecord`, valida JPEG/PNG/WEBP estático, tamanho/dimensões bounded, decode/re-encode, storage configurado e auditoria. Limites correntes são operacionais, não política definitiva de produção. Adapter de captura a câmera, worker/caminho autenticado e armazenamento de produção não estão implementados/homologados.

## Decisões abertas

O BC-02 abaixo fecha credencial/perfil, método e privilégio locais de captura. Endpoints reais por fabricante/modelo, políticas finais de MIME/tamanho/dimensões, storage de produção, retenção/expurgo e homologação permanecem pendentes conforme contrato de imagem e ADR-019/021. Este documento não autoriza captura em câmera real.

## BC-02 — caso de uso e execução separada

O produto autorizou os quatro perfis no BC-02; captura direta exige
`cameras.capture_camera_image` (Técnico/Admin na matriz BC-AUTH), diferente
de upload manual. `RequestCameraCapture(camera_id, actor, idempotency_key,
source_preference?)` valida permissão, elegibilidade, profile/capability
SUPPORTED, target policy e vínculo de credencial; grava job e auditoria
sanitizada, sem abrir câmera no request de renderização. UI recebe ID/status
opaco. `CameraCaptureJob` durável tem UUID, Camera FK, requestor FK, chave de
idempotência opaca, source `HTTP_SNAPSHOT/RTSP_FRAME`, profile/config version,
status `QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELLED`, datas, error code
allowlisted e FK opcional para `CameraImageRecord`. Não armazena URI, bytes,
SDP ou segredo. A mesma chave para ator+câmera devolve o mesmo job; chave
distinta permite nova captura, inclusive bytes idênticos. Não deduplicar por
hash e não substituir registro existente.
A chave é token aleatório de 16–128 caracteres seguros gerado pelo cliente
da ação ou pelo servidor, validado antes de criar job; não contém PII.

Seleção: preferência explícita aceita apenas entre capabilities SUPPORTED e
permitidas; sem preferência, selecionar `RTSP_FRAME` quando elegível e
configurado. `HTTP_SNAPSHOT` é método secundário independente e sua seleção
deve ser explícita quando RTSP não for escolhido. Falha, indisponibilidade ou
inelegibilidade do método selecionado retorna resultado explícito; não alternar
silenciosamente nem criar captura por outra fonte. Essa prioridade supersede
esta regra anterior de prioridade HTTP por amendment C01 aprovado em
`ARGOS-E3-RTSP-CONTRACT-PROMOTION-01`. Worker de captura separado do
monitoramento consome job com claim atômico, bounded concurrency/timeout e
credencial resolvida no momento.
HTTP usa CAM-INT-04; RTSP usa a API complementar de extração de frame/JPEG de
CAM-INT-03, separada dos diagnósticos A/B/C/D. Ambas as fontes convergem no
mesmo fluxo de validação, persistência privada, auditoria e `CameraImageRecord`;
E4 continua lendo esse registro pelos contratos e regras existentes. Sem perfil/
credencial/egress ou adapter pronto, job falha com código seguro; não cria
`CameraImageRecord` e não altera disponibilidade.

Bytes/frame passam por validação de formato JPEG/PNG/WEBP estático,
≤10 MiB e ≤20 milhões de pixels como guardrails locais reversíveis, decode,
re-encode e SHA-256 pelo servidor. Salvar via `default_storage` privado em
chave gerada pelo servidor; só então criar `CameraImageRecord` canônico com
`CAPTURA_CAMERA`, `captured_at` UTC do recebimento, `recorded_at` servidor,
executor e metadados. Atualizar job SUCCEEDED e FK na mesma transação da
linha; falha de DB remove objeto recém-salvo por compensação; falha de
storage não cria linha AVAILABLE. Reprocessar job SUCCEEDED não duplica
registro. `LATEST_CAMERA_CAPTURE`/`DISPLAY_IMAGE` preservam a seleção e
ausência de fallback do contrato de imagem. Captura não usa streak,
incidente, worker de monitoramento ou seu budget de fila. Produção define
storage/backend/retenção em gate separado.

```text
MODEL_CHANGE = CameraCaptureJob; reuse CameraImageRecord unchanged
MIGRATION_REQUIRED = YES
EXPECTED_MODELS = CameraCaptureJob; CameraImageRecord existing
RELATIONSHIPS = Camera 1:N Job; User 1:N Job; Job 0..1:1 ImageRecord
CONSTRAINTS = unique(camera,requestor,idempotency_key); job/image camera same
              checked in service transaction; status/result coherence
INDEXES = (status,created_at); (camera,created_at)
DATA_MIGRATION = NO; prior uploads/captures unchanged
ROLLBACK_CONSIDERATION = drain/cancel jobs, reconcile orphan objects; preserve images
EXPECTED_PRIMARY_FILES = cameras/imagens/read_service.py; cameras/imagens/preview_service.py
EXPECTED_NEW_FILES = cameras/imagens/capture_service.py;
                     cameras/management/commands/run_capture_worker.py; CameraCaptureJob model
EXPECTED_TEST_FILES = cameras/test_imagens_capture_service.py;
                      cameras/test_imagens_read_service.py; permission tests
SHARED_FILES = cameras/models.py/migrations; views/urls integration sequential
STOP_AND_ESCALATE_TO_SOL_IF = request requires automatic capture, new
                              provenance/latest rule, or secret-bearing endpoint
```

Acceptance criteria:

1. Mesmo ator/câmera/key cria um job/registro no máximo; key nova cria nova
   captura mesmo com hash igual. HTTP e RTSP fakes válidos criam
   `CAPTURA_CAMERA` no mesmo modelo canônico.
2. Falha de auth, policy, adapter, timeout, decode, storage ou DB termina job
   com erro seguro, sem registro AVAILABLE, sem objeto órfão conhecido e sem
   mudar estado/streak/incidente. Falha não usa outra fonte automaticamente.
3. Usuário sem permissão não cria job; captura não revela segredo/URI/bytes em
   log/auditoria; latest inválida não promove captura antiga; upload manual
   conserva sua proveniência e seu fluxo.

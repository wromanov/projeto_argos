# CAM-INT-04 — Captura HTTP de snapshot

```text
STATUS = ACTIVE / ADAPTER CONTRACT; NOT HOMOLOGATED
HTTP_CAMERA_ADAPTER_IMPLEMENTED = NO
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL ADAPTER AND FAKE
IMPLEMENTER_TARGET = LUNA
READY_NOW = NO / CAM-INT-02-R1 NOT_PUBLISHED
REQUIRED_PREDECESSORS = CAM-INT-01; CAM-INT-02; CAM-INT-02-R1; CAM-INT-06; CAM-INT-07
```

## Separação de operações

Uma requisição HTTP usada como probe de saúde não é automaticamente uma captura e uma captura sob demanda não é uma transição de disponibilidade. A captura autorizada busca uma imagem por adapter/capability homologada e encaminha os bytes ao pipeline canônico `CameraImageRecord`; não salva evidência automaticamente em evento de monitoramento.

## Requisitos de conexão

O futuro adapter constrói internamente esquema HTTP/HTTPS permitido, IPv4 de `Camera`, porta autorizada e path controlado pelo perfil. Userinfo e credenciais em URL são proibidos. Redirects ficam desabilitados; se adjudicados, cada hop exige validação completa de esquema, destino, porta e allowlist. DNS e proxy ambiental permanecem desabilitados no baseline. Timeout, tamanho máximo de resposta, content-type, status e cancelamento devem ser bounded. Não seguir link para VMS ou host não permitido.

Resposta HTTP só é captura válida se o conteúdo for validado por assinatura/formato e decode seguro e então passar pelo fluxo de persistência de imagem; MIME declarado pelo equipamento não basta. Nenhum token/header sensível é incluído em logs. Erros são normalizados e sanitizados.

## Limites

ADR-019 proíbe captura automática associada a probe, primeira detecção ou retorno `OFFLINE -> ONLINE`; captura é sob demanda de ator autorizado. O BC-02 abaixo fecha método/limites locais; endpoints reais e política definitiva de produção variam por capability e ainda exigem validação. `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` define proveniência, integridade, seleção e armazenamento; este documento não os duplica.

Referências: ADR-019; ADR-021 §§3.5–3.8, 7–9; IMG-CAP; CAM-INT-01/02/07.

## BC-02 — adapter local e integração de bytes

`HttpSnapshotAdapter` recebe request tipado de configuração/capability já
autorizadas, não URL de browser. Método V1 `GET`; endpoint relativo é
fornecido pelo perfil ou override restrito Técnico/Admin, sem endpoint
universal de fabricante. Scheme `https` por default para auth; HTTP
autenticado exige policy explícita de ambiente homologada, sem autorização
implícita neste contrato. Autenticação Basic/Digest somente quando o perfil
declara o método, com segredo resolvido por CAM-INT-02 e entregue pelo client
sem userinfo. Biblioteca escolhida para a slice: `httpx==0.28.1`, com client
`trust_env=False`, `follow_redirects=False`, timeout connect/read bounded e
streaming de resposta; pin entra em requirements na implementação. Redirect,
proxy e DNS ficam desabilitados; host é `Camera.ip` e TLS verifica certificado
sem `verify=False`. Falha de certificado é `TLS_ERROR`, não OFFLINE.

Orçamento total por tentativa até 30 s e connect ≤ orçamento, herdados da
configuração; nenhuma repetição automática. Resposta só é candidata em status
200, Content-Type image/jpeg/png/webp permitido pelo perfil, tamanho entre 1
e 10 MiB e até 20 milhões de pixels (guardrails locais reversíveis coerentes
com upload/preview existentes). Ler em chunks, interromper ao exceder limite
mesmo se Content-Length mentir; desabilitar decompression não bounded ou medir
bytes pós-decompressão. PIL verifica assinatura, decode estático e dimensões;
re-encode limpa metadados antes do pipeline de `CameraImageRecord`. MIME
declarado sozinho nunca basta. Outros status, HTML, imagem animada/truncada,
timeout e cancelamento são resultados sanitizados sem criar registro.

HTTP probe e captura são operações distintas. Este adapter retorna bytes
validados à camada IMG-CAP quando chamado para captura; não escreve imagem,
não muda monitoramento e não audita por conta própria. A captura final usa
`CAPTURA_CAMERA`, `captured_at` do instante observado pelo servidor e
`recorded_at` do servidor, sem promover upload manual. Fakes cobrem HTTP
200 válido, 30x, 401, MIME falso, oversize e timeout. Endpoint/formato real
por fabricante permanece validação externa.

```text
MODEL_CHANGE = NONE beyond CAM-INT-01 schema
MIGRATION_REQUIRED = NO
EXPECTED_MODELS = CameraConnectionConfig; CameraImageRecord reused
RELATIONSHIPS = existing configuration/profile/credential references
CONSTRAINTS = service validation; image model constraints unchanged
INDEXES = NONE NEW
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = disable adapter, preserve image records
EXPECTED_PRIMARY_FILES = cameras/integracao/configuration.py; requirements.txt
EXPECTED_NEW_FILES = cameras/integracao/http_snapshot/adapter.py;
                     cameras/integracao/http_snapshot/fake.py
EXPECTED_TEST_FILES = cameras/test_camera_http_snapshot.py
SHARED_FILES = configuration resolver read-only; IMG-CAP consumes adapter port
STOP_AND_ESCALATE_TO_SOL_IF = vendor requires redirect/DNS/query-secret,
                              unsupported auth method or unsafe TLS bypass
```

Acceptance criteria:

1. Dada resposta válida de fake, adapter devolve bytes/formato/dimensões
   validados sem criar imagem ou mudar estado de monitoramento.
2. Dado redirect, proxy ambiental, destino bloqueado, status não 200,
   Content-Type falso, bytes/pixels acima do limite ou decode inválido,
   adapter falha fechado sem persistência e sem vazar URL/segredo.
3. Dado timeout/cancelamento, conexão fecha no orçamento e o próximo probe
   não herda side effect; validação de endpoint real fica pendente.

Referências do client escolhido: [HTTPX Client](https://www.python-httpx.org/advanced/clients/),
[autenticação](https://www.python-httpx.org/advanced/authentication/) e
[versão 0.28.1](https://pypi.org/project/httpx/0.28.1/).

## CAM-INT-02-R1 — dependency factual de autenticação HTTP

Basic/Digest já contratado requer username/password; portanto
`CAM-INT-04_REQUIRES_R1 = YES`. `IMPLEMENTATION_READY` acima qualifica a
especificação local, não `READY_NOW`: o fluxo autenticado depende de
CAM-INT-02-R1 implementada, integrada, validada e publicada. Não criar outra
resolução de segredo para HTTP. CAM-INT-06/07 mantêm suas dependencies próprias.

O caso de uso confiável seleciona o `CameraConnectionConfig` persistido
autorizado e resolve exclusivamente pela API pública interna
`cameras.integracao.credentials.resolve_active_credential_for_execution(*, config)`.
O port HTTP recebe somente `ResolvedCameraCredential` efêmero para auth
Basic/Digest em memória. Não inclui segredo em request serializável, URL,
resultado ou resposta; o objeto/client auth é liberado ao encerrar a tentativa.
Input, falhas e lifetime estão no
[contrato R1](CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md).

Proibidos: helper privado de decrypt, leitura de ciphertext, acesso ao provider,
crypto duplicada, reveal endpoint/serviço ou metadados como resolução e URI
autenticada. Falha de resolução bloqueia port/rede, sem fallback antigo/anônimo.
Captura manual verifica `capture_camera_image` no caso de uso externo antes
de resolver; eventual diagnóstico verifica `run_camera_connection_test`.
Não exigir reveal nem User fictício para execução interna. Nenhum evento de
reveal é criado por captura/probe; a auditoria própria da captura é preservada.
Testes do consumer cobrem integração com R1 e negação sem rede/segredo.

Observação desta adjudicação: worktree `codex/cam-int-04-implementation` tem
alterações locais em requirements, `http_snapshot/` e teste; apenas o status
Git foi consultado. Não se declara execução pausada, aceite, falha ou conclusão
desse trabalho sem evidência própria. O gate de publicação do fluxo autenticado
exige R1; esta atividade não altera esse worktree nem avalia seu conteúdo.

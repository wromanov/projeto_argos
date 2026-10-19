# ARGOS E3 — Rodada 1: RTSP Frame Extraction Foundation

ACTIVITY_ID = ARGOS-E3-RTSP-DOC-01
FOLLOW_ON_ACTIVITY_ID = ARGOS-E3-RTSP-ROUND-1-P1
ROUND = 1 / P1
STATUS = PLAN_RECONCILED / HUMAN_APPROVAL_PENDING; NOT_STARTED

## Objetivo

Evoluir a fronteira do adapter para entregar uma única imagem de frame validável e bounded. A Rodada 1 não integra o worker E3, não cria job/migration, não persiste imagem, não usa câmera real e não executa código nesta atividade documental.

## Diagnóstico dirigido inicial

1. Registrar contrato atual `RtspAdapter`: `probe(request)`, `describe(request)`, `receive_one_frame(session) -> bool`, `cancel(...)`.
2. Seguir `GStreamerRtspAdapter.describe()` e `receive_one_frame()`: `describe` invoca `probe`; callback do `appsink` marca `seen["frame"]` após amostra válida; resultado guardado em `_sessions`; `receive_one_frame` consome somente booleano. `GstSample`/buffer não é exportado.
3. Inspecionar construção de pipeline, teardown, callback thread-safety e deadline global; não confundir A/B/C/D de diagnóstico com imagem JPEG persistível.
4. Verificar disponibilidade e versões de GStreamer, PyGObject, plugins `rtspsrc`, depay H.264/H.265, decoder e `appsink` no runtime Linux de destino. requirements.txt não declara PyGObject/GStreamer; GI é opcional e o adapter falha fechado se indisponível. Python 3.14.8 foi citado no checkpoint anterior, sem compatibilidade demonstrada. Registrar distribuição/arquitetura/Python, GStreamer/GI e plugins de H.264/H.265 no runtime Linux pretendido. Se incompatível, propor runtime reproduzível isolado; não instalar ou alterar ambiente/VM nesta rodada.

## Contrato de saída a decidir na P1

Propor valor opaco/imutável para frame com bytes de imagem, media type validado, dimensões, codec de origem sanitizado e metadados temporais necessários. Nunca incluir URI, credencial, SDP, caminho local ou objeto GStreamer serializável. Definir API explícita distinta do resultado diagnóstico; não sobrecarregar booleano nem serializar `RtspConnectionRequest`.

## Limites e tratamento

- Deadline total e cancelamento propagados até teardown; no máximo um frame por chamada.
- Limite de bytes de entrada configurável e bounded; dimensão/largura/altura/pixels limitados antes da alocação/decodificação final; proteger contra frame malformado e pressão de memória.
- Appsink deve obter a amostra de vídeo decodificada, mapear/copy bounded, soltar buffer/sample e destruir pipeline em sucesso, timeout, cancelamento e erro.
- H.264 e H.265/HEVC devem ter caminhos de depay/decode explícitos e erro sanitizado para plugin/codec indisponível.
- Codificar JPEG com qualidade/faixa definida; validar assinatura, decode, dimensões e bytes de saída. Não salvar arquivo/registro nesta P1.
- Não alterar semântica de probe, estados de disponibilidade, worker MON ou E4.

## Testes sintéticos

Separar duas classes de evidência:

- **Testes com fakes:** source/appsink e amostras determinísticas para H.264/H.265; cobrir frame válido, vazio, oversized, inválido, timeout, cancelamento, falha decode/encode, plugin ausente, limpeza e ausência de segredo. Esses testes validam lógica, limites e tratamento de falha, mas não comprovam disponibilidade/compatibilidade de GStreamer ou plugins.
- **Decodificação offline real:** para cada codec alegado como suportado, executar pipeline GStreamer real no runtime Linux escolhido, usando fixture H.264 e fixture H.265/HEVC locais, identificadas por origem e SHA-256, sem rede/câmera. Registrar distribuição/arquitetura, Python, GStreamer/GI/PyGObject, plugins e versões, elementos efetivamente selecionados, comando/pipeline e resultado de decode; preservar log sanitizado, saída de diagnóstico e evidência do frame/JPEG decodificado independentemente com dimensões e tamanho. Evidência de H.264 não comprova H.265, nem o contrário. Se fixture, runtime, elemento ou evidência faltar, marcar aquele codec como `NOT_VALIDATED` e não alegar suporte real.

## Aceite e interfaces

P1 aceita quando API de saída e limites são aprovados, testes com fakes passam e cada codec alegado tem decodificação offline real demonstrada no runtime GStreamer escolhido; todas falhas são bounded/sanitizadas e recursos GStreamer são liberados. JPEG gerado deve ser decodificado independentemente. Preservar `probe`, `describe`, diagnósticos A–D e compatibilidade dos callers; definir migration/API versioning em adapter novo ou alteração compatível. Se `receive_one_frame` tiver consumidores atuais, inventariá-los antes de qualquer mudança. Entregáveis de P1: decisão de runtime, contrato de frame, implementação isolada, testes com fakes, evidência offline por codec, relatório de validação e revisão independente conforme DAG aplicável.

```text
REAL_CAMERA = PROHIBITED_IN_P1
PERSISTENCE_AND_WORKER = OUT_OF_SCOPE
PYTHON_3_14_8_COMPATIBILITY = TO_BE_EVIDENCED
ROUND_1_START = REQUIRES_EXPLICIT_HUMAN_APPROVAL
```

## Plano executável condicionado à autorização P1

A baseline contém GStreamerRtspAdapter, diagnóstico A/B/C/D, identificação de codec e recepção de frame booleana. A P1 evolui isoladamente a fronteira de captura; não cria o adapter do zero e não integra run_capture_worker.

1. Inventariar callers de probe/describe/receive_one_frame/cancel e limites atuais. Definir port/DTO aditivo, separado do diagnóstico, com bytes bounded, media type, dimensões e codec sanitizado; nunca expor objeto GStreamer, URI, SDP ou segredo.
2. Antes da implementação, registrar runtime Linux/Python e versões de GStreamer/GstRtsp, GI/PyGObject, rtspsrc, depayloaders, parsers, decoders e appsink. requirements.txt não declara GI/GStreamer. Não assumir suporte de plugins instalados.
3. Obter exatamente uma amostra de vídeo decodificada no appsink; copiar somente dentro do limite, soltar GstSample/buffer e codificar JPEG com dimensões e qualidade controladas. Validar assinatura, decodificação independente, media type, dimensões, pixels e tamanho. Nenhuma persistência na P1.
4. H.264 e H.265/HEVC devem ser avaliados em caminhos reais de decode no runtime escolhido. Evidência para um codec não comprova o outro. Fakes isolados não comprovam compatibilidade de plugin.
5. Usar deadline monotônico global, propagação de cancelamento e teardown do pipeline para NULL em sucesso, timeout, cancelamento e erro. Liberar bus, source, pipeline, sample e buffer. Garantir callbacks thread-safe, sem exceções/bytes sem limite e sem sessão órfã.
6. Testes sintéticos autorizados para frames válidos H.264/H.265, vazio/inválido/oversized, plugin ausente, falha decode/encode, deadline, cancelamento, amostra tardia, cleanup e sanitização. Ambiente sem suporte a codec deve bloquear a alegação de suporte; nenhuma rede/câmera real.
7. Preservar A/B/C/D e callers existentes. No HEAD revisado, receive_one_frame retorna bool; não foi observado consumidor produtivo do adapter no serviço de captura, que hoje é HTTP-only. Pesquisar novamente callers no branch P1 e manter interface compatível/adicionar port até migração autorizada.
8. Entregar relatório com matriz Linux/Python/GStreamer/plugins, codecs validados, limite de memória, JPEG decodificado independentemente, timeout/cancelamento, cleanup, callers preservados e falhas conhecidas.

    P1_SCOPE = RTSP_FRAME_EXTRACTION_FOUNDATION_ONLY
    WORKER_INTEGRATION = OUT_OF_SCOPE
    MIGRATION = NONE
    CAMERA_NETWORK = PROHIBITED
    CODE_OR_ENVIRONMENT_CHANGE = REQUIRES_EXPLICIT_P1_AUTHORIZATION
    ROUND_1 = NOT_STARTED

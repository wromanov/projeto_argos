# ARGOS E3 — Rodada 1: RTSP Frame Extraction Foundation

ACTIVITY_ID = ARGOS-E3-RTSP-DOC-01
ROUND = 1 / P1
STATUS = READY_FOR_HUMAN_APPROVAL; NOT_STARTED

## Objetivo

Evoluir a fronteira do adapter para entregar uma única imagem de frame validável e bounded. A Rodada 1 não integra o worker E3, não cria job/migration, não persiste imagem, não usa câmera real e não executa código nesta atividade documental.

## Diagnóstico dirigido inicial

1. Registrar contrato atual `RtspAdapter`: `probe(request)`, `describe(request)`, `receive_one_frame(session) -> bool`, `cancel(...)`.
2. Seguir `GStreamerRtspAdapter.describe()` e `receive_one_frame()`: `describe` invoca `probe`; callback do `appsink` marca `seen["frame"]` após amostra válida; resultado guardado em `_sessions`; `receive_one_frame` consome somente booleano. `GstSample`/buffer não é exportado.
3. Inspecionar construção de pipeline, teardown, callback thread-safety e deadline global; não confundir A/B/C/D de diagnóstico com imagem JPEG persistível.
4. Verificar disponibilidade e versões de GStreamer, PyGObject, plugins `rtspsrc`, depay H.264/H.265, decoder e `appsink` no runtime Linux de destino. Ambiente Python 3.14.8 e compatibilidade de wheels/bindings precisam de evidência; se incompatível, propor worker/runtime isolado suportado sem alterar ambiente durante P1.

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

Fakes de source/app sink e amostras determinísticas para H.264/H.265; frame válido, vazio, oversized, inválido, timeout, cancelamento, erro de decode/encoder, plugin ausente, limpeza e ausência de segredo em mensagens. Verificar bytes JPEG por decoder independente disponível no ambiente; sem conexão de rede/câmera.

## Aceite e interfaces

P1 aceita quando API de saída e limites são aprovados, pipeline retorna JPEG sintético válido para os codecs suportados, todas falhas são bounded/sanitizadas e recursos GStreamer são liberados. Preservar `probe`, `describe`, diagnósticos A–D e compatibilidade dos callers; definir migration/API versioning em adapter novo ou alteração compatível. Se `receive_one_frame` tiver consumidores atuais, inventariá-los antes de qualquer mudança. Entregáveis de P1: decisão de runtime, contrato de frame, implementação isolada, testes sintéticos, relatório de validação e revisão independente conforme DAG aplicável.

```text
REAL_CAMERA = PROHIBITED_IN_P1
PERSISTENCE_AND_WORKER = OUT_OF_SCOPE
PYTHON_3_14_8_COMPATIBILITY = TO_BE_EVIDENCED
ROUND_1_START = REQUIRES_EXPLICIT_HUMAN_APPROVAL
```

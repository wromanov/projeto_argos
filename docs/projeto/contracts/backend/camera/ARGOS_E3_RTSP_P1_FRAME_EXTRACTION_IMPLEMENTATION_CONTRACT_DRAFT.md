# Minuta do contrato de implementação P1 — RTSP Frame Extraction Foundation

```text
STATUS = DRAFT / PHASE_A_IMPLEMENTED; P1_FINAL_ACCEPTANCE_PENDING
PHASE_A_IMPLEMENTATION_AUTHORIZATION = GRANTED
PHASE_A_REVIEW = ACCEPT_WITH_FINDINGS
P1_FINAL_ACCEPTANCE = NOT_GRANTED
PHASE_B_RUNTIME_VALIDATION = NOT_AUTHORIZED
NEXT_GATE = HUMAN_AUTHORIZATION_FOR_PHASE_B_RUNTIME_VALIDATION
CANONICAL_AMENDMENTS = C01-C06 PRESERVED
CODE_CHANGES = PHASE_A_IMPLEMENTED
FOCUSED_OFFLINE_TESTS = 28/28 PASS / executed by ROOT in test DB
STATIC_REVIEW = COMPLETE
RUNTIME_EVIDENCE = NOT_ESTABLISHED
```

## 1. Finalidade e autoridade

Este documento propõe o contrato de implementação da P1 — **RTSP Frame Extraction Foundation**. Ele detalha a API complementar que transforma uma amostra de vídeo RTSP decodificada em um JPEG validado. A implementação da Fase A está autorizada; o aceite final da P1 não está concedido. Esta minuta não altera C01–C06, não cria novo identificador canônico CAM e não declara validação de runtime, evidência de testes, operação de rede, mudança de VM ou acesso a câmera real.

Prevalecem `CAM-INT-03_RTSP_CONNECTION_CONTRACT.md`, `IMAGE_CAPTURE_INTEGRATION_CONTRACT.md`, `ARGOS_E3_RTSP_PRIMARY_RECOVERY_AMENDMENTS.md` e `ARGOS_E3_RTSP_ROUND_1_PLAN.md`. Em especial, C02 preserva os diagnósticos existentes e exige API distinta; C04 reserva a modelagem operacional de configuração à P2; C05 preserva credenciais protegidas e Target Policy; C06 mantém F02/F03 pendentes.

## 2. Escopo e exclusões

A P1 **DEVE** implementar somente a capacidade isolada de obter no máximo uma amostra de vídeo decodificada de um request RTSP interno autorizado, convertê-la em JPEG em memória, validá-la e retornar bytes e metadados seguros. **DEVE** tratar H.264 e H.265/HEVC como caminhos independentes de depay e decode, sujeitos à validação real por codec.

A P1 **NÃO DEVE** criar ou alterar modelos, migrations, configuração operacional C04/P2, worker E3, jobs, persistência, `CameraImageRecord`, galeria E4, estados de disponibilidade, reducer ou monitoramento. Não deve ativar captura automática, fallback para HTTP Snapshot, sessão com câmera real ou rede corporativa. A seleção primária futura de `RTSP_FRAME` aprovada em C01 não equivale à habilitação operacional nesta P1.

## 3. API e compatibilidade

A interface aditiva prevista é `extract_one_jpeg_frame(request: RtspConnectionRequest) -> RtspJpegFrame`, preferivelmente definida em um protocolo complementar `RtspFrameExtractor`, separado do port diagnóstico `RtspAdapter`. Essa assinatura é a API autorizada para a Fase A; a autorização não amplia o escopo nem concede aceite final da P1. A taxonomia de erros internos da P1 está fechada na seção 8 e não altera F03.

`RtspJpegFrame` **DEVE** ser valor imutável e opaco, com bytes JPEG, `media_type = image/jpeg`, largura, altura, codec de origem sanitizado e tempo de observação UTC aware. **NÃO DEVE** conter URI, IP, path, SDP, credencial, caminho local, objeto GStreamer ou campos serializáveis que os revelem. O retorno só ocorre após validação independente do JPEG, inclusive assinatura, decodificação, dimensões e limite de bytes.

`probe`, `describe`, `receive_one_frame(session) -> bool`, `cancel` e a semântica A/B/C/D **DEVEM** permanecer compatíveis. A extração não altera o significado de D nem transforma resultado diagnóstico em imagem. Callers devem ser inventariados antes da implementação; os testes de compatibilidade existentes permanecem obrigatórios.

## 4. Fronteira de autorização e credenciais

`RtspConnectionRequest` é um **tipo de entrada interna**, não uma prova de que seu destino foi autorizado: `AuthorizedTargetRequest` pode ser construído diretamente. Nenhum endpoint/browser pode invocar o extrator com URL arbitrária. O futuro caller operacional **DEVE**, antes de qualquer socket, comprovar configuração persistida e elegibilidade da operação, aplicar permissão própria de captura, perfil e allowlist de `TargetPolicy`, e resolver credencial efêmera pela API pública `resolve_active_credential_for_execution(*, config)` conforme CAM-INT-02-R1. O teste manual existente, autorizado por `run_camera_connection_test`, não substitui essa autorização de captura.

Na P1, essa composição operacional permanece **fora do escopo**. A implementação e os testes **DEVEM** deixar explícita a pré-condição de request interno confiável e demonstrar que a API não recebe URL livre. O relatório de P1 **NÃO PODE** afirmar que o fluxo persistido de captura já consome configuração autorizada de ponta a ponta.

Credencial **DEVE** permanecer fora de URI, linha de comando, logs, exceções, DTO e persistência. `rtspsrc` recebe `user-id`/`user-pw` somente em propriedades em memória. É proibido acessar helpers privados de decriptação, ciphertext, reveal de usuário ou criar fallback de senha. Falha de resolução encerra a chamada antes da rede, com erro sanitizado e sem transição de disponibilidade.

## 5. Pipeline e contrato da amostra

O pipeline obrigatório é:

```text
rtspsrc → depay H.264/H.265 → decodebin → videoconvert
        → appsink (amostra raw decodificada) → JPEG em memória
        → validação independente → RtspJpegFrame
```

O `appsink` **DEVE** receber vídeo **raw decodificado**, conforme o plano P1. `jpegenc → appsink` não satisfaz esta minuta. O `appsink` **DEVE** negociar `video/x-raw,format=RGB` (`RGB8` packed). O extrator **DEVE** inspecionar caps e verificar formato, largura, altura, pixels, stride, offsets e tamanho real do buffer antes da cópia. O tratamento de linhas **DEVE** respeitar stride/padding, sem pressupor `stride == largura × bytes_por_pixel`. O encoder JPEG **DEVE** operar sobre cópia limitada, com qualidade 85, sem resize silencioso e sem arquivo temporário. Limites quantitativos constam da seção 6.

Parser, depayloader e decoder efetivamente selecionados **DEVEM** ser registrados no relatório de validação do runtime. Ausência de plugin ou falha de codec é capacidade indisponível/erro de configuração sanitizado, não evidência de câmera OFFLINE.

## 6. Limites e orçamento de recursos

Os limites de formato e imagem abaixo foram adjudicados para esta minuta:

| Parâmetro | Limite contratual |
|---|---|
| Formato raw no appsink | `RGB8` packed; caps `video/x-raw,format=RGB` |
| Largura máxima | 1.920 pixels |
| Altura máxima | 1.080 pixels |
| Pixels máximos | 2.073.600 |
| Stride | positivo, de `largura × 3` até 8.192 bytes por linha |
| Cópia raw por amostra | até 12 MiB (12.582.912 bytes) |
| `appsink` | `max-buffers=1`; configurar `max-bytes=12 MiB` quando suportado pelo runtime |
| Buffers internos upstream (depay/parser/decoder, pools/surfaces) | Sem limite numérico imposto por `appsink`; `UPSTREAM_BUFFER_LIMIT = NOT_ESTABLISHED` |
| JPEG | quality 85; até 5 MiB (5.242.880 bytes) |
| Deadline global | 15 segundos monotônicos, incluindo teardown |
| Pico observado de memória | alvo inicial de até 256 MiB por extração; métrica observada, não limite imposto ao processo |

No pior stride admitido, `8.192 × 1.080 = 8.847.360` bytes, abaixo do limite de cópia raw de 12 MiB. Antes de copiar, validar caps, largura, altura, quantidade de pixels, stride, offsets e tamanho real do buffer/sample; tanto o tamanho real quanto o resultado calculado por `stride × altura` **DEVEM** ser conferidos contra 12 MiB. Rejeitar a amostra se qualquer limite não for satisfeito; não redimensionar silenciosamente. `appsink` **DEVE** usar `max-buffers=1`; `max-bytes=12 MiB` **DEVE** ser configurado quando a versão instalada suportar essa propriedade. A fila `max-buffers=1`/`max-bytes=12 MiB` não contém nem limita alocações anteriores ao `appsink`, incluindo buffers de depay/parser/decoder e pools/surfaces.

Separar limites impostos pela aplicação (caps, stride, tamanho da cópia raw, fila e JPEG) do alvo de pico observado de RSS/memória e do uso dos buffers upstream. O alvo de 256 MiB **NÃO** é hard cap, limite do processo nem garantia de contenção. `UPSTREAM_BUFFER_LIMIT = NOT_ESTABLISHED` e `MEMORY_BOUND = NOT_VALIDATED` até runtime fixado e medição; ausência de evidência impede declarar aceite P1. O relatório deve registrar o uso observado upstream e o pico observado por extração contra o alvo de 256 MiB. O adapter atual limita a amostra e a fila do sink, mas esses controles não limitam por si só a memória do decoder ([gst_adapter.py](../../../../../cameras/integracao/rtsp/gst_adapter.py)).

## 7. Deadline, cancelamento, teardown e destino

Uma chamada **DEVE** usar deadline monotônico global de 15 segundos, do início até a codificação, validação do JPEG e teardown; o timeout de conexão não pode exceder o saldo global. Não há retry interno nem segundo frame. Cancelamento em qualquer fase **DEVE** impedir retorno de bytes, sinalizar parada, conduzir o pipeline a `NULL` e liberar recursos. Amostras tardias e callbacks concorrentes **DEVEM** ser tratados sem retorno duplicado, retenção de buffer ou exceção não sanitizada. A exigência de prazo é contratual; o comportamento bounded permanece `NOT_VALIDATED` até evidência no runtime. Se `set_state(PLAYING/NULL)`, callbacks ou cleanup excederem os 15 segundos, o critério falha; checar relógio no loop Python não prova duração limitada dessas operações.

IP, porta, scheme, path, transporte, DNS/proxy e redirects seguem CAM-INT-03 e Target Policy. O extrator **NÃO DEVE** seguir destino diferente do validado. Rejeitar mensagem de redirect no bus não comprova que `rtspsrc` deixou de se conectar ao novo destino antes da mensagem. `REDIRECT_BLOCKING = NOT_VALIDATED`. A estratégia futura de evidência deve combinar egress allowlist externa ao `rtspsrc` com teste em servidor RTSP local controlado que redirecione a um destino proibido, verificando que nenhuma conexão chega a esse destino. Esse gate não está aprovado para execução nesta atividade; nenhuma rede real é autorizada por esta minuta.

## 8. Erros, observabilidade e segredo

Falhas **DEVEM** usar o enum interno fechado da P1: `INVALID_REQUEST`, `TARGET_BLOCKED`, `CREDENTIAL_UNAVAILABLE`, `AUTH_FAILURE`, `CODEC_UNAVAILABLE`, `DECODE_FAILED`, `ENCODE_FAILED`, `INVALID_SAMPLE`, `LIMIT_EXCEEDED`, `TIMEOUT`, `CANCELLED`, `UNAUTHORIZED_REDIRECT`, `TEARDOWN_FAILED` e `RUNTIME_ERROR`. Códigos são estáveis e sanitizados. Esta taxonomia interna **NÃO** redefine F03 nem o mapeamento futuro para `CameraCaptureJob`. Texto bruto de `GError`, SDP, frames, URI e segredos não entra em log, exceção pública, auditoria ou histórico de probe. Falhas de auth/configuração/codec não geram inferência de OFFLINE.

## 9. Divergência de porta

Há defeito pré-existente confirmado. `validate_rtsp_uri` valida e aceita uma porta explícita quando permitida pelo perfil e pela policy; depois, `resolve_connection_config` recompõe a URI escolhendo 554 ou a única porta do perfil sem preservar `parsed.port` ([configuration.py](../../../../../cameras/integracao/configuration.py#L39), [linhas 180–210](../../../../../cameras/integracao/configuration.py#L180)). **Porta explícita autorizada nunca pode ser descartada silenciosamente.**

**Dependência direta da P1 = NO.** A fundação P1 proposta recebe um request interno e não chama `resolve_connection_config`; portanto, `configuration.py` e seus testes não integram os arquivos desta P1. Registrar o defeito para correção antes da integração operacional posterior. Se uma revisão futura demonstrar dependência direta na P1, isso exige nova delimitação e autorização humana, além de testes para porta explícita, default e bloqueio por perfil/policy. Não corrigir o resolver nesta minuta.

## 10. Arquivos e sequência por fase

Arquivos de código alterados na Fase A autorizada: `cameras/integracao/rtsp/ports.py`, `cameras/integracao/rtsp/gst_adapter.py`, `cameras/integracao/rtsp/fake.py` e `cameras/test_camera_rtsp_adapter.py`. A revisão estática foi concluída com resultado `ACCEPT_WITH_FINDINGS`. Os testes focais offline foram reexecutados pelo ROOT no test DB: 28/28 PASS. Esses resultados não constituem evidência de runtime GStreamer, decodificação offline real por codec, rede, RSS ou teardown real. `configuration.py` e seus testes ficam fora desta P1, conforme a cláusula 9. Mudanças de CI, provisionamento de GStreamer ou ambiente runtime não estão autorizadas por esta minuta.

Runtime atual **não validado**. O workflow de CI usa `ubuntu-latest` e Python 3.14, mas não provisiona GStreamer explicitamente ([ci.yml](../../../../../.github/workflows/ci.yml#L14), [linha 26](../../../../../.github/workflows/ci.yml#L26)). Não presumir compatibilidade de GStreamer/PyGObject com Python 3.14. Recomenda-se selecionar e fixar um ambiente Linux reproduzível (base/distribuição e arquitetura, versão Python com compatibilidade evidenciada, GStreamer, GI/PyGObject, plugins e decoders), sem alterar CI/runtime nesta atividade. `H264 = NOT_VALIDATED`; `H265 = NOT_VALIDATED`.

Sequência e estado dos gates:

1. **Fase A implementada:** API aditiva de extração raw → JPEG; `probe`, `describe`, `receive_one_frame(session) -> bool` e diagnósticos A/B/C/D preservados. Testes focais offline: 28/28 PASS; revisão: `ACCEPT_WITH_FINDINGS`.
2. **Fase B — não autorizada:** obter autorização humana antes de qualquer validação de runtime. Só após autorização, selecionar e fixar runtime Linux compatível e reproduzível.
3. Se autorizada, validar H.264 e H.265 separadamente em GStreamer real offline.
4. Se autorizada, medir memória observada, deadline de 15 segundos, cancelamento e teardown no runtime escolhido; resultado fora do deadline é falha.
5. Se autorizada, validar redirect/egress em gate controlado separado; estratégia permanece `NOT_VALIDATED`.
6. Publicar relatório de evidência e limitações; somente então avaliar aceite final P1.

## 11. Matriz de evidência e aceite

| Evidência | Deve demonstrar | Não demonstra |
|---|---|---|
| Fakes/source/appsink simulados | Contrato da API, um frame, DTO, limites, amostra vazia/inválida/oversized, erro decode/encode/plugin, cancelamento, amostra tardia, cleanup e ausência de segredo | Decodificação real ou comportamento de rede |
| GStreamer real **offline H.264** | Depay/decode H.264 no runtime escolhido, RGB raw no appsink e JPEG decodificável | H.265 ou redirects; status atual `NOT_VALIDATED` |
| GStreamer real **offline H.265/HEVC** | Depay/decode H.265 no mesmo nível de evidência | H.264 ou redirects; status atual `NOT_VALIDATED` |
| Medição de deadline/memória/teardown/upstream | Prazo global de 15 s, cancelamento, teardown, uso observado dos buffers upstream e pico observado versus alvo de 256 MiB por extração no runtime escolhido | Hard RSS/process cap ou comportamento de câmera corporativa; sem medição upstream e de memória, o aceite permanece pendente |
| Gate controlado de redirect/egress | Ausência de conexão a destino não autorizado usando allowlist externa e servidor RTSP local controlado | Homologação de câmera real; status atual `NOT_VALIDATED` |

Fixtures offline **DEVEM** ter origem e SHA-256 registrados; relatório **DEVE** registrar distribuição/arquitetura Linux, Python, GStreamer, GI/PyGObject, plugins/versões, elementos escolhidos, dimensões, bytes e JPEG validado independentemente. Fakes não promovem suporte real a codec. Sem fixture, runtime, plugin ou evidência para um codec, marcar esse codec `NOT_VALIDATED`.

Aceite P1 requer API e limites aprovados, compatibilidade diagnóstica preservada, testes com fakes, prova offline real de cada codec alegado, JPEG válido, falhas sanitizadas, recursos liberados, deadline cumprido, medição de memória e de uso observado upstream registrada, e evidência da política de redirect/egress. Sem medição upstream ou do pico de memória versus o alvo de 256 MiB, o aceite permanece pendente. Nenhum desses resultados autoriza worker E3, persistência E4, P2, VM, câmera real ou operação recorrente.

## 12. Gatilhos pendentes para o aceite final

`PHASE_A_IMPLEMENTATION_AUTHORIZATION = GRANTED`; `PHASE_A_REVIEW = ACCEPT_WITH_FINDINGS`; `P1_FINAL_ACCEPTANCE = NOT_GRANTED`. `PHASE_B_RUNTIME_VALIDATION = NOT_AUTHORIZED`; autorização para a Fase B requer decisão humana explícita. `NEXT_GATE = HUMAN_AUTHORIZATION_FOR_PHASE_B_RUNTIME_VALIDATION`.

Pendências para o aceite final:

1. Selecionar runtime Linux concreto, reproduzível e fixado, com compatibilidade comprovada para Python, GStreamer, GI/PyGObject, plugins e decoders.
2. Definir e demonstrar estratégia verificável de redirect/egress no gate de validação autorizado.

O formato RGB8, dimensões, pixels, stride, limites de amostra/fila/JPEG, qualidade e deadline estão fechados conforme a seção 6. O alvo de 256 MiB continua uma métrica observada, não um hard cap; `MEMORY_BOUND = NOT_VALIDATED` até medição. `H264 = NOT_VALIDATED`, `H265 = NOT_VALIDATED`, `REDIRECT_BLOCKING = NOT_VALIDATED`, RSS/uso de buffers upstream e teardown dentro do deadline de 15 segundos permanecem sem evidência. Os 28/28 testes focais offline e a revisão estática não promovem nenhum desses estados. `PHASE_B_RUNTIME_VALIDATION = NOT_AUTHORIZED`; `NEXT_GATE = HUMAN_AUTHORIZATION_FOR_PHASE_B_RUNTIME_VALIDATION`.

## Fontes factuais

- [Contrato CAM-INT-03](CAM-INT-03_RTSP_CONNECTION_CONTRACT.md) e [contrato de captura de imagem](../images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md).
- [Plano RTSP P1](../../../ARGOS_E3_RTSP_ROUND_1_PLAN.md) e [amendments C01–C06](../../../ARGOS_E3_RTSP_PRIMARY_RECOVERY_AMENDMENTS.md).
- [Resolver e validador de configuração RTSP](../../../../../cameras/integracao/configuration.py#L39) — inspeção estática da aceitação e posterior recomposição da porta.
- [Adapter GStreamer atual](../../../../../cameras/integracao/rtsp/gst_adapter.py) — limites da amostra/fila do sink não comprovam contenção total de memória.
- [Workflow de CI](../../../../../.github/workflows/ci.yml#L14) — `ubuntu-latest`, Python 3.14 e ausência de provisionamento explícito de GStreamer.
- [Contrato de capacidade e fronteiras de recursos](../production/CAPACITY_AND_RESOURCE_BOUNDARIES_CONTRACT.md) — não estabelece envelope medido para este runtime/caminho.

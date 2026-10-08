# CAM-INT-03 — auditoria técnica independente

Data: 2026-10-07. Escopo: código local, contratos, testes, artefatos anteriores,
GStreamer local e duas verificações limitadas na câmera de laboratório autorizada.
Este documento registra evidência e recomendação; não autoriza implementação.

## Veredito

**PROVEN_DEFECT / ROOT_CAUSE_CONFIDENCE = PROVEN.** O depayloader dinâmico
`rtph264depay`, criado em `gst_adapter.py:96` e adicionado em `:99`, permanece
em `NULL`, com pad sink inativo. O adapter não chama `sync_state_with_parent()`
nem `set_state()` nesse elemento. Links aceitos e codec identificado não ativam
o elemento nem comprovam entrega de mídia.

A hipótese foi isolada experimentalmente: com o adapter local inalterado,
A/B/C PASS e D TIMEOUT em 15,028 s; alterando **somente a sincronização do
depayloader**, dentro de um harness externo ao repositório, A/B/C/D PASS em
0,663 s. O fluxo chegou ao appsink, com decoder real `d3d12h264dec`.

Precisão importante: o elemento não foi adicionado quando o estado corrente
do pipeline já era PLAYING. Foi adicionado **depois da solicitação PLAYING**,
com estado corrente PAUSED e estado pendente PLAYING. A ausência de
sincronização continua sendo o defeito; uma recomendação que copiasse apenas
o estado corrente PAUSED perderia essa distinção.

A documentação oficial estabelece a responsabilidade de ajustar o estado de
elementos adicionados a um pipeline em execução. Ver
[GstBin.add](https://gstreamer.freedesktop.org/documentation/gstreamer/gstbin.html)
e [manipulação de pipelines](https://gstreamer.freedesktop.org/documentation/application-development/advanced/pipeline-manipulation.html).

## Authority e baseline

```text
PROJECT = ARGOS
ACTIVITY = CAM-INT-03-INDEPENDENT-END-TO-END-TECHNICAL-AUDIT
CLASSIFICATION = ROOT_CAUSE_ARCHITECTURAL_AND_RUNTIME_AUDIT
EXECUTION_MODE = DIRECT
SUBAGENTS_USED = 0
MODEL_EXPECTATION = SOL / HIGH / fornecida pelo usuário; runtime não reconfigurado
SKILL_SELECTED = activity-progress-reporting
PLUGIN_SELECTED = NONE
BRANCH = master
HEAD = 0483f3bbca8108bc45b78b70d39577b1e30b96df
ORIGIN_MASTER = 0483f3bbca8108bc45b78b70d39577b1e30b96df / referência local
REMOTE_QUERIED = NO
INITIAL_WORKTREE = DIRTY / 6 tracked modified + 3 untracked
INITIAL_STAGING = EMPTY
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
PRODUCTION_FIX_AUTHORIZATION = NOT_GRANTED
```

Dirty set inicial, preservado:

```text
M cameras/integracao/rtsp/gst_adapter.py
M cameras/integracao/target_policy.py
M cameras/test_camera_target_policy.py
M docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md
M docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md
M docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md
?? cameras/integracao/rtsp/runtime.py
?? cameras/test_camera_rtsp_runtime.py
?? docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md
```

Authorities: `AGENTS.md`; documentos de continuidade; políticas canônicas de
independência, prompts, skills e multiagente indicadas no entrypoint;
`ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`; ADR-019 e ADR-021;
contratos CAM-INT-01, CAM-INT-02, CAM-INT-02-R1, CAM-INT-03,
CAM-INT-03_TARGET_POLICY_CONFIGURATION, CAM-INT-07 e BC-AUTH.

**CONTRACT_CONFLICT = YES**, distinguindo duas classes:

1. Implementação não satisfaz o comportamento D e lifecycle requerido por
   CAM-INT-03. Isso exige correção de código, não uma nova decisão arquitetural.
2. Cabeçalhos históricos de CAM-INT-03 e CAM-INT-02/R1 ainda qualificam adapter
   e resolução como não publicados/não implementados. PROJECT_STATE §§50–55,
   Git e código contradizem esses status, como já registrado anteriormente.
   A divergência documental permanece explicitamente pendente de reconciliação
   própria. Não se alteraram esses contratos para esconder o conflito.

Não foi encontrado conflito entre authorities que impeça a correção mínima.
`cameras/integracao/rtsp/configuration.py` não existe: a dependência efetiva é
`cameras/integracao/configuration.py`.

## Prova controlada e proteção do estado

Harness novo: `%TEMP%/argos_cam_int_03_independent_audit.py`. Não contém
literais de credencial; lê o input autorizado em memória e nunca o imprime.
`GST_DEBUG=0`, sem debug file novo, URI sem userinfo, sem gravação/exibição
de mídia. Policy exata foi fornecida como mapping process-local ao composition
root. Alvo validado antes do adapter e novamente no wrapper; nenhum outro alvo.

Foi utilizado o ator Django existente, com verificação das duas permissões
exigidas, sem criação de usuário, concessão de permissões ou alteração de RBAC.
Bootstrap exclusivamente por `replace_camera_credential`; resolução pela API
pública `resolve_active_credential_for_execution`. Chave Fernet efêmera em
ambiente do processo. Transaction externa revertida em `finally`.

As duas execuções usaram os mesmos observers, pipeline produtivo, credencial,
policy, transporte TCP, timeout de 15 s e connect timeout de 3 s. O proxy Python
delegou o pipeline original; sua única intervenção de tratamento foi chamar
`depay.sync_state_with_parent()` imediatamente após `add`. Contadores apenas
incrementam e retornam `PadProbeReturn.OK`. Nenhum sample foi puxado pelo
observer; o callback produtivo continuou responsável pelo `pull-sample`.

| Medida | UNCHANGED | SYNC_ONLY |
|---|---:|---:|
| A/B/C/D | PASS/PASS/PASS/FAIL | PASS/PASS/PASS/PASS |
| Resultado | TIMEOUT | SUCCESS |
| Duração externa | 15,028 s | 0,663 s |
| `rtspsrc.protocols` real | 4 = TCP | 4 = TCP |
| Pai no add | PAUSED, pending PLAYING | PAUSED, pending PLAYING |
| Depay após add | NULL | NULL |
| Sync efetuado | não | true |
| Depay após ação | NULL | PLAYING |
| Sink pad ativo após ação | false | true |
| Source output buffer probes | 0 | 328 |
| Depay sink buffer probes | 0 | 328 |
| Depay src buffer probes | 0 | 16 |
| Decodebin sink buffer probes | 0 | 16 |
| Raw pad emitido | 0 | 1 |
| Appsink sink buffer probes | 0 | 2 |
| Decoder instanciado | nenhum | d3d12h264dec |
| Pipeline/depay ao fim | NULL/NULL | NULL/NULL |

**FACT:** câmera fornece H264 decodificável por este runtime, neste alvo e
transporte autorizados. **FACT:** banco SQLite teve SHA-256 idêntico antes e
depois da transaction. **FACT:** pipeline e depay estavam em NULL após ambas
as tentativas. **INFERENCE:** rede, codec, decoder e appsink não causaram o
bloqueio comparado; a única intervenção liberou todo o caminho.

`INDEPENDENT_GSTREAMER_CONTROL_RUN = NOT_REQUIRED`: a comparação com uma
única intervenção já isolou a causa e comprovou o stream e o runtime. A regra
de parada antecipada do prompt foi aplicada; não se adicionou um terceiro
teste de câmera nem se exauriram hipóteses sem valor discriminante restante.
Isso não equivale a executar uma pipeline independente fora do adapter.

## Stages: contrato versus implementação

| Stage | Entrada e sucesso no código | Falha e timeout | Buffers necessários |
|---|---|---|---|
| A NETWORK_REACHABILITY | Socket IPv4/TCP; `connect` retorna | Timeout/refusal/socket error; fecha socket | Não |
| B RTSP_REACHABILITY | A passou; loader/pipeline/RTSP; `on-sdp` marca SDP recebido | Sem SDP até deadline, erro de bus, unavailable, cancelamento | Não |
| C MEDIA_DESCRIPTION | Pad source com media=video e encoding mapeado; depay criado; links depay→decoder e source→depay aceitos; `seen.codec` preenchido | Unsupported, vídeo não identificado, erros de montagem; ao final sem codec C FAIL | Não |
| D MEDIA_DELIVERY | Callback appsink recebe sample e buffer com tamanho 1..32 MiB | Sem frame até deadline = TIMEOUT; EOS antes = MEDIA_DELIVERY_FAILED | Sim |

Referências: `gst_adapter.py:61–157`, callbacks em `:82–116`.
`STAGE_C_CAN_PASS_WITH_ZERO_MEDIA_BUFFERS = YES`: `seen.codec` é atualizado
após links, sem qualquer condição de buffer. B usa recebimento de SDP como
evidência operacional de resposta RTSP; não mantém evidências individuais de
OPTIONS/SETUP/PLAY. C adiciona à descrição uma condição de pad e montagem,
portanto sua semântica concreta é mais forte que apenas interpretar SDP e
mais fraca que entregar mídia. A/B/C PASS não significam decoder funcionando
ou câmera ONLINE; somente D PASS produz SUCCESS.

Os stages não são quatro laços independentes com deadlines separados:
os callbacks acumulam observações e o resultado é consolidado ao final.

```text
STAGE_A_MEANING = NETWORK_REACHABILITY / TCP connect
STAGE_B_MEANING = RTSP_REACHABILITY / callback on-sdp
STAGE_C_MEANING = MEDIA_DESCRIPTION / codec de caps RTP + links upstream aceitos
STAGE_D_MEANING = MEDIA_DELIVERY / sample raw com buffer válido e tamanho limitado
```

## Topologia e estados

```text
PIPELINE_TOPOLOGY =
GstPipeline
  rtspsrc [rtsp-source]
    → RTP interno: manager/rtpbin → jitterbuffer → payload demux/ghost pads
    → recv_rtp_src_* (application/x-rtp; media=video; encoding-name=H264)
    → rtph264depay [video-depay-h264].sink
    → .src (video/x-h264 quando ativado e negociado)
    → decodebin [video-decoder].sink
    → autoplug/parser/decoder (d3d12h264dec observado no tratamento)
    → src_* (video/x-raw)
    → appsink [frame-sink].sink
```

O adapter não cria manualmente o RTP interno nem o decoder concreto.
`decodebin` os seleciona; factories internas podem variar por máquina.

| Elemento | Criado/add antes do pedido PLAYING | Dinâmico | Estado explícito/sync pelo adapter | Estado observado/esperado |
|---|---|---|---|---|
| Pipeline | sim | não | PLAYING e NULL | PAUSED pending PLAYING no callback; NULL ao fim |
| rtspsrc | sim/sim | não | herdado do pai | estado vivo com emissão de SDP/pad |
| decodebin | sim/sim | não | herdado do pai | aguarda mídia, autoplug no tratamento |
| appsink | sim/sim | não | herdado do pai | aguarda preroll/mídia; sample no tratamento |
| rtph264depay | não/não | sim | nenhum no código auditado | NULL e sink inativo; esperado estado-alvo do pai |
| Decoder interno | apenas no tratamento | sim, ownership decodebin | gerenciamento pelo decodebin | d3d12h264dec entrega raw no tratamento |

`DEPAY_CREATED_AFTER_PLAYING = YES / após solicitação; não após estado corrente PLAYING`.
`DEPAY_ADDED_AFTER_PLAYING = YES / mesma qualificação`.
`DEPAY_SYNCED_TO_PARENT = NO / código produtivo`.
`DYNAMIC_ELEMENT_STATE_HYPOTHESIS = PROVEN_CAUSAL`.
`PIPELINE_LIFECYCLE_VALID = NO`.

Prova local adicional, sem rede: pipeline vazio em PLAYING + `add(depay)`
deixou depay NULL/pad inativo; sync retornou true, levou depay a PLAYING e
ativou o pad. Essa observação confirma a semântica do runtime instalado.

## Links, callbacks e bus

| Link | Operação, timing | Retorno checado | Falha propagada |
|---|---|---|---|
| Depay src → decodebin sink | `depay.link(decoder)`, callback source | sim | levanta `_Failure` no callback; canal até loop não garantido |
| Source RTP → depay sink | `pad.link(target)`, callback source | sim, compara OK | mesma lacuna de callback |
| Decodebin raw → appsink sink | `pad.link(target)`, callback decoder | não | nenhuma indicação explícita ao loop |

`IGNORED_PAD_LINK_RETURN_IS_DEFECT = YES`, como lacuna de tratamento/diagnóstico.
`IGNORED_PAD_LINK_RUNTIME_CAUSALITY = NOT_SUPPORTED`: não houve raw pad no
controle; no tratamento raw/appsink funcionaram sem mudar esse callback.
Não recomendar trocar decoder/depay/appsink para corrigir este bloqueio.

`BUS_OBSERVABILITY_SUFFICIENT = NO`. Mask lê ERROR/EOS/ELEMENT/REDIRECT.
ERROR é classificado e não é deliberadamente descartado; EOS encerra o loop;
ELEMENT só trata estrutura `redirect`; REDIRECT falha fechado. WARNING,
STATE_CHANGED, ASYNC_DONE, STREAM_START, LATENCY e QOS não são tratados.
Mensagens ELEMENT de timeout RTSP sem nome redirect são ignoradas.

`ERROR_CAN_BE_MASKED_AS_TIMEOUT = YES / falha de callback ou estado/fluxo sem
ERROR de bus consumível`; não se afirma que toda mensagem ERROR seja ignorada.
Exceções em callbacks PyGObject não têm caminho explícito de retorno à thread
do loop; elevar `_Failure` ali não equivale a elevar no `try` do probe.
O estado NULL do depay não produziu ERROR terminal; o loop esperou o deadline.

## Evidência histórica e neutralidade

Artefatos existentes foram preservados e inspecionados independentemente.
Não continham os literais de username/password do input autorizado na busca
executada; isso é verificação limitada, não prova universal de ausência de
qualquer material sensível possível.

| Artefato/run | RTP arrival | Jitterbuffer output | Depay input/output | Decodebin output/appsink |
|---|---|---|---|---|
| diagnostic.log, pipelines 0 e 1 | YES, received packet | YES, tentativa push; não sucesso downstream | entrada não provada; saída não provada | não provado |
| callback_observability.log | YES, buffer real nas proxy pads RTP | YES, buffer na saída proxy; retorno FLUSHING | entrada não medida; saída não observada pelos probes relatados | não observado pelos probes relatados |
| novo UNCHANGED | probes source/depay sem buffers; não elimina chegada RTP | histórico corrobora bloqueio downstream | 0/0 no intervalo | 0/0 |
| novo SYNC_ONLY | YES, 328 buffers source | YES por entrega ao depay | 328/16 | raw pad + 2 buffers appsink |

Logs: diagnostic.log linhas 833/854 registram RTP recebido e 908/2733 tentam
push; callback log linhas 1067–1074 mostram buffer real na maquinaria RTP,
retorno flushing e pausa da tarefa do jitterbuffer. Tentativa de push não
comprova aceitação pelo sink do depay. Zero no probe source BUFFER também
não comprova zero RTP: sticky events podem falhar antes de esse buffer
alcançar o probe. A classificação anterior `CASE_A / RTP / DEPAY INPUT-OUTPUT`
era uma localização ampla, não causa raiz.

`MEDIA_FLOW_LAST_PROVEN_POINT = appsink raw video / novo SYNC_ONLY`.
Para a falha original: saída/proxy RTP antes do depay, com FLUSHING downstream;
não confundir esse limite com entrega efetiva ao depay.

`HARNESS_BEHAVIOR_NEUTRAL = PARTIAL` para o harness antigo: os observers
de fluxo são pass-through; não há factory interception, state/caps/link
modification nem sample pull. `_pipeline` é embrulhado para anexar observers
antes de PLAYING, e `element-added` anexa probe ao depay antes do retorno de add.
Observers de decoder são registrados antes do callback produtivo; só leem,
retêm referências e contam, com Lock. Há overhead e referência retida, não
neutralidade temporal absoluta. O wrapper altera AUTO para TCP deliberadamente,
e GST_DEBUG muda custo/tempo. Transaction/rollback estão corretos no harness.
O snapshot depois de NULL pode perder caps; portanto caps NONE após teardown
não comprova ausência anterior de negociação.

`TCP_DIAGNOSTIC_ACTUALLY_FORCED_TCP_MEDIA = YES`: wrapper copia request para
TCP; `_pipeline` seta `protocols=GstRtsp.RTSPLowerTrans.TCP`; nova leitura real
confirmou valor 4. Os mocks usam enum sintético TCP=1; não usar esse número
como valor GStreamer real. Transporte interleaved TCP é a opção habilitada;
o teste novo passou entregando buffers com essa restrição. Para cada run antigo
não há trace SETUP completo independente, então o enum relatado sozinho não
prova o transporte efetivamente negociado daquele run.

`AUTO_BEHAVIOR = UDP unicast e TCP permitidos; UDP preferido, fallback TCP por
timeout configurado; multicast excluído`. A ordem é do rtspsrc, não da ordem
de OR dos flags. `FORCED_TCP_BEHAVIOR = somente TCP permitido`.
`TRANSPORT_ROOT_CAUSE_STATUS = ELIMINATED / bloqueio comparado`.
Ver [rtspsrc](https://gstreamer.freedesktop.org/documentation/rtsp/rtspsrc.html).

## Ambiente, decoder, DLL, appsink e deadline

```text
GSTREAMER_VERSION = 1.28.7
PYTHON_GSTREAMER_BINDING_SOURCE = .venv/Lib/site-packages/gstreamer_python/Lib/site-packages/gi
RELEVANT_FACTORIES = rtspsrc; rtph264depay; decodebin; appsink / AVAILABLE
AVAILABLE_H264_DECODERS = d3d12h264dec rank 258; d3d11h264dec rank 257;
                         avdec_h264 rank 256; openh264dec rank 64
H264PARSE = AVAILABLE / rank 257
MFH264DEC = UNAVAILABLE
EXPECTED_SELECTED_DECODER = d3d12h264dec / prioridade e compatibilidade; não garantia universal só por rank
ACTUAL_SELECTED_DECODER = NONE no controle; d3d12h264dec no tratamento
AUTOPLUG_AVAILABLE = YES
AUTOPLUG_FAILURE = NO no tratamento; não alcançado no controle
PLUGIN_REGISTRY = FUNCTIONAL_FOR_TESTED_PATH / saúde global não certificada
GIOLIBPROXY_FILE_EXISTS = YES
GIOLIBPROXY_CLASSIFICATION = NON_CAUSAL / falha auditada
MODULE_REQUIRED_FOR_THIS_RTSP_PATH = NO / sucesso empírico apesar do aviso
WINDOWS_LOADER_FAILURE_REASON = ERROR_MOD_NOT_FOUND / LoadLibraryExW error 126
TRANSITIVE_DEPENDENCY_FAILURE = UNRESOLVED / causa exata de resolução pelo loader
```

Import table PE direta de giolibproxy: gio-2.0-0.dll, gobject-2.0-0.dll,
glib-2.0-0.dll, intl-8.dll, proxy-1.dll, VCRUNTIME140.dll,
api-ms-win-crt-string-l1-1-0.dll, api-ms-win-crt-runtime-l1-1-0.dll, KERNEL32.dll.
Busca recursiva em todos os pacotes encontrou os imports não sistêmicos;
12 DLLs percorridas, sem dependência nominal não resolvida nessa busca.
Isso não garante que o loader as encontre nos search paths. A primeira busca
em apenas parte dos pacotes não abrangia `gstreamer_libs/bin` e não serve
como prova de DLL ausente. Não foi instalado, removido ou reparado pacote.
O aviso ocorreu no processo que também entregou vídeo, eliminando causalidade
para este incidente; motivo específico do loader fica explicitamente aberto.

`APPSINK_CONFIGURATION_VALID = YES / caminho H264 demonstrado`.
Emit-signals true; sync false; max-buffers 1; drop true; max-bytes 32 MiB;
enable-last-sample false; caps video/x-raw. `new-sample` puxa sample, valida
buffer não vazio e tamanho máximo, retorna FlowReturn.OK. O tratamento passou
com essa configuração inalterada. `SAMPLE_VALIDATION_DEFECT = UNRESOLVED` para
uma validação semântica mais forte de frame: o código valida existência/tamanho,
não dimensões, layout ou integridade de cada pixel; não causou este timeout.

`PRODUCTION_TIMEOUT_DEFECT = UNRESOLVED / garantia absoluta de deadline`.
O budget começa em `probe` antes do TCP, inclui loader, construção, startup
e recebimento; default 5 s, diagnóstico 15 s. Poll tem quantum até 100 ms,
connect usa saldo. Loader/set_state/cleanup não possuem interrupção pelo
deadline; tcp-timeout usa connect budget original, não sempre saldo atualizado.
Isso limita a garantia contratual de término absoluto. Não há prova de que
5 s corte startup legítimo neste caso: com sync, startup ocorreu em 0,663 s.
Aumentar timeout não é a correção do elemento NULL.

`CLEANUP_VALID = YES / duas execuções observadas` com ambos NULL ao fim.
Garantia geral de cleanup bounded permanece **OBSERVABILITY_GAP**: finally
chama NULL sem verificar retorno/conclusão e ignora exceções. Callbacks e
objetos são liberados pelo término do pipeline/processo; não há teste aqui
de cancelamento sob todas as condições, vazamento continuado ou escala.

## Testes e deltas

66 testes PASS em 37,433 s: adapter 17, runtime 5, policy 24, configuração 8,
resolução de credencial 12. Banco temporário de teste criado/destruído.
`manage.py check` e `git diff --check` PASS. Nenhum teste/source foi editado.

```text
TESTS_USE_REAL_GSTREAMER = NO / suites existentes
DO_TESTS_MODEL_DYNAMIC_ELEMENT_STATE = NO
TESTS_VERIFY_DYNAMIC_STATE_SYNC = NO
TESTS_VERIFY_REAL_BUFFER_FLOW = NO
DO_TESTS_VERIFY_DECODEBIN_DYNAMIC_OUTPUT = NO / callback raw não exercitado no fake temporal
DO_TESTS_VERIFY_PAD_LINK_RETURN = NO / falha do raw link não modelada
DO_TESTS_VERIFY_APPSINK_SAMPLE = YES / sample sintético, não pipeline real
TARGET_POLICY_IMPLEMENTATION = PASS / escopo auditado
RUNTIME_COMPOSITION_ROOT = PASS / escopo auditado
SERVICE_ENV_COUPLING = NONE
```

MOCK_BLIND_SPOTS: fake pipeline `add` ignora estados; elementos fake aceitam links;
`deliver_frame` chama diretamente `new-sample` após source pad, sem passar
buffer por depay/decoder nem produzir raw pad; clocks simulados não exercitam
threads, dispositivos gráficos, registry ou shutdown real. Isso explica
17/17 PASS com depay real NULL.

Baseline `origin/master` ainda tem ligação antecipada `decoder.link(sink)`;
delta local remove somente essa linha. A remoção é necessária porque a saída
do decodebin é dinâmica; o callback permanece registrado antes de PLAYING.
Ela não corrige o estado do depay, defeito também presente na baseline.
TargetPolicy adiciona paths pelo parser existente; runtime novo compõe policy
por invocação, fail-closed antes de serviço/credencial/socket e deriva portas
da mesma policy. Testes e prova via composition root apoiam esses deltas.
Não foi encontrada razão para reabrir a adjudicação de path/default_path.

## Matriz de candidatos

| Candidato | A favor | Contra/limite | Status |
|---|---|---|---|
| C1 estado do depay | NULL/pad inativo; sync-only libera todos os buffers | nenhum contraste contrário | PROVEN |
| C2 mídia não chega ao depay | 0 buffers no controle | RTP anterior provado; tratamento recebe 328; é efeito de C1 | SUPPORTED como consequência; ELIMINATED como causa externa |
| C3 TCP não efetivo | enum anterior isolado não basta | property real 4, tratamento TCP passa | ELIMINATED |
| C4 depay defeituoso/configuração | saída zero inicialmente | mesmo elemento processa 16 buffers após sync | ELIMINATED para incidente |
| C5 decoder/autoplug | nenhum raw inicialmente | não recebeu encoded; d3d12 decodifica no tratamento | ELIMINATED para incidente |
| C6 pad decodebin não emitido | controle 0 | tratamento emite 1 sem trocar decodebin | SUPPORTED como consequência |
| C7 raw link falha | retorno ignorado | controle não alcança raw pad; tratamento appsink recebe | DEPRIORITIZED / defeito secundário |
| C8 appsink/sample | frame zero inicialmente | mesma configuração/callback passa | ELIMINATED para incidente |
| C9 DLL/runtime | warning loader real | mesma instalação entrega vídeo | ELIMINATED para incidente; loader específico UNRESOLVED |
| C10 timeout/lifecycle | depay NULL e espera budget | timeout é sintoma; bounds absolutos não provados | PROVEN lifecycle; timeout como causa ELIMINATED |
| C11 harness | TCP override/debug overhead | observers novos iguais nas duas execuções; static state proof | DEPRIORITIZED; neutralidade antiga PARTIAL |
| C12 câmera/stream | só SDP não prova stream | H264 raw no appsink após única intervenção | ELIMINATED para incidente |
| C13 outro defeito | callbacks/bus/cleanup têm gaps | não necessários para explicar contraste | SUPPORTED como dívida independente |

## Recomendação e prova futura da correção

```text
ROOT_CAUSE_CLASS = DYNAMIC_ELEMENT_LIFECYCLE_DEFECT
ROOT_CAUSE = PROVEN / depayloader não sincronizado ao estado-alvo do pai
ROOT_CAUSE_CONFIDENCE = PROVEN
CODE_FIX_REQUIRED = YES
ARCHITECTURAL_CHANGE_REQUIRED = NO
CONTRACT_CHANGE_REQUIRED = NO / comportamento; reconciliação de status é separada
EXPECTED_PRODUCTION_FILES = cameras/integracao/rtsp/gst_adapter.py
EXPECTED_TEST_FILES = cameras/test_camera_rtsp_adapter.py
NEXT_RECOMMENDED_ACTIVITY = CAM-INT-03-DYNAMIC-DEPAYLOADER-STATE-FIX-AND-REAL-RUNTIME-REVALIDATION
NEXT_ACTIVITY_AUTHORIZED = NO / DEFERRED_NO_AUTHORITY
```

Correção conceitual mínima: adicionar depay ao pipeline; configurar/ligar
depay→decodebin; sincronizar com o pai, checando o retorno; só então permitir
o fluxo source→depay. `sync_state_with_parent()` observa o estado-alvo,
inclusive PLAYING pendente. Falha deve ser sinalizada ao loop por canal
thread-safe/resultado fechado, sem depender de exceção escapar de callback.
Marcar sucesso de montagem/codec após essas verificações. O tratamento colocou
sync logo após add, antes de ambos os links; comprovou causalidade. A ordem
recomendada para produção favorece construir downstream antes de liberar upstream.

`MINIMAL_FIX = sincronizar depay dinâmico ao estado-alvo do pai, verificar
retorno e impedir fluxo upstream antes de downstream ativo`.

EVIDENCE_CHAIN:

1. Código adiciona depay no callback sem set_state/sync.
2. Sem rede, GStreamer instalado mantém novo elemento NULL e pad inativo.
3. Logs antigos comprovam RTP a montante e FLUSHING downstream.
4. Novo controle reproduz A/B/C PASS, D TIMEOUT e depay NULL.
5. Sync-only mantém restante do caminho e produz encoded/raw/appsink, SUCCESS.
6. NULL final e rollback/hash idêntico comprovam encerramento observado e proteção do banco.

REQUIRED_TEST_CHANGES — testes necessários na atividade autorizada:

1. Fake que represente NULL no add dinâmico e exija sync para ativar fluxo;
   teste falha no código atual e passa com correção, incluindo pai PAUSED
   com PLAYING pendente.
2. Sync false/falha: resultado fechado e cleanup, sem timeout genérico indevido.
3. Teste de GStreamer real opt-in com fonte RTP H264 sintética local: depay
   criado dinamicamente, buffers reais, decodebin raw e appsink sample;
   não repetir apenas implementação de mocks.
4. Link raw recusado e falha de callback: cobertura para observabilidade
   secundária se sua correção fizer parte da autorização; não ampliar patch
   silenciosamente.
5. Regressões focais existentes, timeout/cancelamento/NULL, policy e credenciais.

REAL_RUNTIME_REVALIDATION_PLAN — após patch: usar composition root canônico **sem proxy que
sincronize elementos**, policy exata process-local, mesmo ator, credencial
temporária via transaction/rollback; verificar state sync, buffers depay/raw,
sample válido, A/B/C/D PASS, decoder, shutdown NULL, prazo e ausência de logs
sensíveis. Testar default 5 s; transporte TCP e AUTO somente conforme authority.
Não ampliar alvos ou afirmar homologação universal de modelo/firmware.

SECURITY_IMPACT: correção não exige alterar policy, credenciais, RBAC ou
custódia; efetiva o fluxo de mídia já autorizado. Executa processamento que
antes não começava, exigindo preservar bytes/timeouts e cleanup.
REGRESSION_RISK: baixo a moderado, concentrado em callbacks/estados/threads;
mesma criação dinâmica vale para outros depayloaders mapeados, cujo runtime
não foi homologado neste H264. Revisar pad duplicado e falhas sem redesign.

## Estado final e rastreabilidade

```text
STATUS = AUDIT_COMPLETE / ROOT_CAUSE_PROVEN / FIX_DEFERRED_NO_AUTHORITY
ACTIVITY_COMPLETION_PERCENT = 100 / auditoria; não implementação ou homologação
CAM_INT_03_RUNTIME_STATUS = NOT_HOMOLOGATED / adapter produtivo ainda sem correção
SECRET_EXPOSED = NO / nenhum segredo em diagnóstico/report/documentação nova
DATABASE_PERSISTENTLY_CHANGED = NO / rollback e hash idêntico
CREDENTIAL_PERSISTENCE = ROLLED_BACK
REPOSITORY_CODE_CHANGED = NO / nesta auditoria
REPOSITORY_DOCUMENTATION_CHANGED = YES / relatório e continuidade
STAGING = EMPTY
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

Manifesto SHA-256 dos inputs locais auditados:

```text
gst_adapter.py = fedf3ba0b012ddaadb8c24ae8716fb1e2fccc90ddef905a43c32ff97784046ad
test_camera_rtsp_adapter.py = 11ff6b0282d0edb5eddacc9fd7c76030b12ddd477f7427cb9a81038a08af47b2
runtime.py = 16adc9cf914037a2289c7cd286b6f30f3c606bb1569f97f7d0e4dc7ff6f9e69c
diagnostic.log = 5bff839af49b4b5900fb9a137410823943c99af96fb148dabf94a11a28f7de9a
callback_observability.log = 7d8eddd74ef5064cd615f42de1ffefd0b1c4c7df8a156623dd0e2eb0469e3ee5
homologation.py = 18d078fd65183af4fd518c71fcb2c3729a78c545e18f39d4b3b82f80a5624dfb
independent_audit.py = 9c5621d5e7d88070e9c3647aea2412cc92d0bcd04af3df5d088c637cbf20baed
```

Os artefatos TEMP não são artifacts permanentes e podem desaparecer; os
resultados essenciais estão neste relatório. Estado recuperável em
PROJECT_STATE §56 e AGENT_CONTINUITY §20.23. Não há autorização implícita
para correção, commit, push ou produção.

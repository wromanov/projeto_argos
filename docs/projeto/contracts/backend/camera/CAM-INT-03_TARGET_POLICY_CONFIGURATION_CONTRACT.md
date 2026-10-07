# CAM-INT-03 — Contrato de configuração e composição de TargetPolicy

```text
PROJECT = ARGOS
ACTIVITY = CAM-INT-03-TARGET-POLICY-CONFIGURATION-IMPLEMENTATION
CLASSIFICATION = CONTRACT_IMPLEMENTATION
MODE = CONTRACT_FIRST
STATUS = IMPLEMENTED_LOCALLY / TECHNICAL_PASS
IMPLEMENTATION_AUTHORIZED = YES / instrução explícita da atividade
CONFIGURATION_CONTRACT_COMPLETE = YES / especificação e implementação técnica local
BOOTSTRAP_ROOT_CAUSE_CLASS = CASE_C
CONFIGURATION_SOURCE = TRUSTED_ENVIRONMENT
PRODUCTION_PARSER = TargetPolicy.from_environment
NEW_ENVIRONMENT_KEY = ARGOS_CAMERA_ALLOWED_PATHS
PATH_GRAMMAR = scheme:path[,path];...
RUNTIME_COMPOSITION_ROOT = cameras.integracao.rtsp.runtime.run_camera_connection_test_from_environment
POLICY_LIFETIME = PER_INVOCATION
SERVICE_ENV_COUPLING = NONE
DATABASE_POLICY_PERSISTENCE = NONE
DEFAULT_PATH_CHANGE = NO
CAMERA_CONFIG_CHANGE = NO
TARGET_POLICY_SEMANTICS_CHANGE = NO
FROM_ENVIRONMENT_CAPABILITY_EXTENSION = IMPLEMENTED
PRODUCTION_CALLER / COMPOSITION_ROOT_REQUIRED = YES
CONTRACT_CONFLICTS = NONE / divergências históricas de status separadas abaixo
NEW_ARCHITECTURAL_DECISION_REQUIRED = NO
EXECUTION_MODE = DIRECT
SUBAGENTS_USED = 0
SKILL_SELECTED = NONE
PLUGIN_SELECTED = NONE
NATIVE_EXECUTION_USED = YES
```

## 1. Authority, evidência e limites

A instrução explícita do usuário nesta atividade autoriza implementar este
contrato, fechando a fonte de configuração, o parser produtivo, a injeção de
dependências e o lifetime. Ela não autoriza operar câmera, mudar configuração
efetiva, realizar commit ou push.

Authorities relacionadas:

- `docs/projeto/contracts/backend/camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md`;
- `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md`;
- `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`;
- `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`, seções 3–6.

Inspeção estática em `master`, HEAD
`0483f3bbca8108bc45b78b70d39577b1e30b96df`:

- `TargetPolicy.from_mapping` já representa as cinco dimensões contratadas.
- `TargetPolicy.from_environment(environ)` exige um mapping explícito e ainda
  não transporta `allowed_paths_by_scheme`; ele não lê `os.environ` sozinho.
- `run_camera_connection_test` exige `target_policy` e
  `environment_allowed_ports`, ambos injetados. O serviço não carrega ambiente.
- A busca dos símbolos no código Python do repositório encontrou chamadas do
  serviço apenas em testes; falta uma composição de produção para o teste manual.
- `TargetPolicy.validate` compara paths por igualdade. Sem paths de policy,
  pode usar paths explícitos do perfil; com ambos, usa a interseção. Essa
  semântica existente permanece. O novo runtime exigirá paths RTSP próprios da
  policy antes do serviço, impedindo depender daquele fallback em produção.
- O serviço passa `allowed_paths=None` quando o perfil permite override de
  path. Nesse caso, a policy precisa conter os paths autorizados.

A resolução correta da câmera atual é fato fornecido pela instrução do usuário;
nesta atividade não se consultou banco, configuração efetiva nem ambiente real.
Não persistir aqui ou nos testes o IP, CIDR, porta configurada ou endpoint interno
da homologação. Câmera descreve onde está; policy descreve onde a aplicação pode
conectar. A configuração da câmera nunca cria sua própria autorização.

## 2. Transporte de paths pelo ambiente

Fluxo canônico: ambiente confiável → `from_environment(environ)` →
`from_mapping(mapping)` → `TargetPolicy` imutável. Preservar `from_mapping` e
centralizar nele e nos validadores existentes a validação semântica.

Exemplo exclusivamente sintético:

```text
ARGOS_CAMERA_ALLOWED_PATHS=rtsp:/stream-a,/stream-b;http:/image.jpg
```

Regras da extensão:

1. `;` separa grupos; dividir cada grupo no primeiro `:`; `,` separa paths.
2. Cada grupo deve ter scheme e pelo menos um path não vazio. Grupo sem `:`,
   grupo vazio, delimitador final vazio e membro CSV vazio são inválidos.
3. Remover espaços externos dos membros CSV conforme a convenção de transporte
   existente; preservar `/` inicial, caixa e conteúdo do path. Não decodificar
   percent-encoding, resolver URI, inferir vendor ou interpretar glob/regex.
4. Schemes seguem `_validate_scheme`, igual às portas: nomes canônicos em
   minúsculas, dentre `rtsp`, `rtsps`, `http`, `https`. Maiúsculas não são
   convertidas permissivamente; schemes sem correspondente em ports são inválidos.
5. Reutilizar `_validate_path` via `from_mapping`. Nenhuma regra de autorização
   de destino é duplicada no parser.
6. Não usar `_split_csv` sem checar membros vazios: o helper existente os
   descarta, contrariando a regra de paths vazios desta extensão.
7. Não criar deduplicação nova: valores repetidos podem permanecer na tupla.
   Para grupos com a mesma chave, seguir a convenção atual de portas: o último
   grupo substitui o anterior; não unir silenciosamente permissões.
8. Ausência da chave mantém o mapping de paths vazio no construtor genérico,
   preservando consumidores internos existentes. Chave presente vazia ou
   malformada lança `TargetPolicyError`, sem ecoar o valor recebido.
9. O runtime manual RTSP exige `allowed_paths_by_scheme['rtsp']` não vazio;
   ausência, mesmo que o perfil tenha path, é `MISCONFIGURED_POLICY`.

`/` só pode ser autorizado se explicitamente listado. `*` não ganha semântica
de wildcard: não autoriza outros paths. Nenhum path é obtido de
`CameraConnectionConfig` ou `CameraCapabilityProfile` para montar a allowlist.

## 3. Composição de produção proposta

Novo módulo dentro do pacote RTSP existente:
`cameras/integracao/rtsp/runtime.py`.

API implementada nesta atividade:

```python
run_camera_connection_test_from_environment(
    *, actor, camera_id, environ=None, adapter=None,
    timeout_seconds=5.0, connect_timeout_seconds=3.0,
    monotonic=time.monotonic, now=<relógio UTC aware>,
) -> RtspDiagnosticResult
```

`environ=None` usa `os.environ` no composition root; um mapping explícito é
uma dependência interna confiável para composição e testes. Não aceitar esse
mapping de request/browser. Não expor parâmetros `target_policy`,
`environment_allowed_ports`, URI ou allowlist de câmera nessa API produtiva.

Ordem obrigatória a cada invocação:

1. Selecionar a fonte confiável e chamar `TargetPolicy.from_environment(environ)`.
2. Verificar a presença das portas RTSP e de paths RTSP não vazios. CIDRs e
   configuração sintaticamente inválida já falham no parser/construtor.
3. Em falha, retornar diagnóstico sanitizado antes de chamar o serviço.
4. Em sucesso, chamar o serviço existente com `actor`, `camera_id`, a policy
   completa e `environment_allowed_ports=policy.ports_by_scheme['rtsp']`.
   Encaminhar adapter, timeouts e relógios conforme a assinatura existente.
5. Retornar o diagnóstico do serviço, preservando sua autorização manual,
   resolução, revalidação de destino, credenciais, adapter e cleanup.

Derivar as portas da mesma policy evita uma segunda configuração divergente.
Não carregar Django settings. `config/environment.py` contém helpers de ambiente,
mas a inspeção não encontrou convenção que obrigue transportar esta policy
por settings. A responsabilidade RTSP fica no pacote RTSP.

Construir policy por invocação, sem singleton, registry, global mutável,
thread de reload ou cache de banco. O serviço segue independente do ambiente.
O composition root é a entrada interna produtiva reutilizável por futuro
caller legítimo; não criar view, URL, UI, comando de gestão ou MON-WORKER
apenas para fabricar esse caller. Nenhuma sessão real é executada pela
atividade de implementação sem autorização de homologação própria.

## 4. Fail-closed e diagnóstico

Policy ausente/inválida ou sem portas/paths RTSP obrigatórios retorna
`RtspDiagnosticResult` com `error_code='MISCONFIGURED_POLICY'`, categoria
`ProbeResultCode.TARGET_BLOCKED`, A/B/C/D `NOT_RUN`, duração zero e timestamp
UTC aware. Preservar o formato existente de `_blocked` sem importar seu helper
privado: o runtime pode construir o resultado com os value objects públicos
de `ports.py`. Isso não exige alterar `service.py`.

Não chamar serviço, resolver de credencial, adapter ou rede em falha de
bootstrap. Nenhum fallback para policy permissiva ou configuração do perfil.
Não transformar a falha em OFFLINE nem confundi-la com `AUTH_FAILURE`,
`ADAPTER_UNAVAILABLE` ou falha TCP. Não devolver texto bruto da configuração
ou cadeia de exceção contendo valores operacionais.

Destino só passa com CIDR/host, scheme/porta e path simultaneamente permitidos,
além de farm quando configurada e das restrições do perfil. Manter CIDRs
negados, IPs especiais, hostname/DNS, userinfo, query/fragment e revalidação
pré-adapter conforme os contratos e a implementação existentes.

## 5. Arquivos da implementação

| Arquivo | Alteração prevista |
|---|---|
| `cameras/integracao/target_policy.py` | Transporta `ARGOS_CAMERA_ALLOWED_PATHS` por `from_environment`; validação semântica continua em `from_mapping` |
| `cameras/test_camera_target_policy.py` | Cobre parser, sanitização, compatibilidade genérica e autorização com fixtures sintéticas |
| `cameras/integracao/rtsp/runtime.py` | Composition root por invocação, com bootstrap fail-closed |
| `cameras/test_camera_rtsp_runtime.py` | Cobre composição, injeção e ausência de efeitos externos no bootstrap inválido |
| Este contrato | Registra evidências e limites em §8 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Snapshot factual em seção 55 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Handoff em seção 20.22 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Vigência e referências em seção 27 |

`service.py`, `configuration.py`, `gst_adapter.py`, models, migrations,
credentials, crypto, admin e settings não precisam de alteração. Os testes
existentes do adapter são regressão, não autorização para editar seu protocolo.
CAM-INT-04, MON-WORKER, P5, Quick Detail e Design System ficam fora do escopo.

## 6. Critérios técnicos e cobertura executada

Parser: um path RTSP; múltiplos paths; múltiplos schemes com portas
correspondentes; grupo sem separador; scheme vazio/não canônico/desconhecido;
grupo ou membro CSV vazio; chave presente vazia; path sem `/`; ausência das
variáveis base; paths de scheme sem portas; preservação de caixa e de `:`
dentro do path; duplicatas seguindo a convenção fixada. Ausência genérica de
paths continua possível, mas o runtime RTSP a rejeita.

Policy: CIDR + porta + path exato autorizados = ALLOW; outro path, porta ou
IP = DENY; farm errada e CIDR negado = DENY. `/` não é autorizado implicitamente;
`*` não autoriza outro path; rejeições existentes seguem válidas.

Runtime: provar que chama o parser e injeta as cinco dimensões completas e as
portas RTSP da mesma policy; preserva os parâmetros e resultado do serviço;
duas chamadas constroem policies distintas e observam mudança na fonte; fonte
default lê ambiente apenas no runtime; ausência de CIDR, portas ou paths RTSP,
e paths malformados retornam `MISCONFIGURED_POLICY` com todos os estágios
`NOT_RUN`. Em cada falha, assertar serviço, credential resolver e adapter não
chamados; não consultar banco nem abrir socket. Fonte só HTTP não satisfaz
bootstrap RTSP. O serviço conserva sua independência de `os.environ`/settings.

As suítes foram executadas nesta atividade; resultados e comandos constam em
§8. O checkout não contém `cameras.test_camera_rtsp_uri`; a suíte existente
`cameras.test_camera_connection_config` cobre a validação e resolução da URI e
foi executada como equivalente. Testes usam destinos e paths sintéticos; não
usam os valores internos da câmera homologada.

## 7. Divergências históricas e gates desta adjudicação

PROJECT_STATE seção 53 e AGENT_CONTINUITY seção 20.20 atribuíam o bloqueio à
ausência de `default_path`. A instrução atual adjudica que a resolução da URI
da câmera está correta e que o gap é o transporte/bootstrap da policy (CASE C).
Esses registros preservam a tentativa histórica, mas sua explicação causal e
próxima ação não regem esta atividade. Não preencher default_path nem modificar
URI/configuração para passar no gate. A inspeção estática é compatível com essa
adjudicação; não é uma nova homologação da câmera.

Cabeçalhos antigos do registry, DAG e contrato RTSP ainda têm a divergência
pré-R1/publicação já registrada na seção 52. Sua reconciliação geral permanece
adiada, sem promover readiness, homologação ou gates de outras lanes.

```text
CHECKPOINT = HISTORICAL / adjudicação contratual que antecedeu a implementação
CODE_CHANGED = NO / nesta atividade; reparo local anterior preservado
DB_CHANGED = NO
CONFIG_CHANGED = NO
DOCUMENTS_CHANGED = YES / exceção explícita de governança e continuidade
RTSP_SESSION_STARTED = NO
TESTS_RUN = NO / adjudicação por inspeção estática
CONTRACT_DOCUMENT_CHECK = PASS / campos obrigatórios, fences e ausência dos valores internos de homologação
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE seção 54; handoff em AGENT_CONTINUITY seção 20.21
ACTIVITY_COMPLETE = YES / somente adjudicação e proposta contratual
COMMIT = NOT_AUTHORIZED / NOT_PERFORMED
PUSH = NOT_AUTHORIZED / NOT_PERFORMED
IMPLEMENTATION = DEFERRED_NO_AUTHORITY
NEXT_REQUIRED_ACTIVITY = CAM-INT-03-TARGET-POLICY-CONFIGURATION-IMPLEMENTATION
NEXT_ACTIVITY_AUTHORIZED = YES / instrução explícita recebida na atividade seguinte
```

## 8. Evidência da implementação CAM-INT-03 (2026-10-07)

```text
IMPLEMENTATION_STATUS = IMPLEMENTED_LOCALLY / TECHNICAL_PASS
IMPLEMENTATION_AUTHORIZATION = EXPLICIT_USER_INSTRUCTION
BASELINE_BRANCH = master
BASELINE_HEAD = 0483f3bbca8108bc45b78b70d39577b1e30b96df
BASELINE_ORIGIN_MASTER_LOCAL_REF = 0483f3bbca8108bc45b78b70d39577b1e30b96df
BASELINE_DIVERGENCE = 0 / 0
BASELINE_DIRTY_FILES = M cameras/integracao/rtsp/gst_adapter.py; M docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md; M docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md; M docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md; ?? docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md
FILES_CHANGED_THIS_ACTIVITY = cameras/integracao/target_policy.py; cameras/test_camera_target_policy.py; cameras/integracao/rtsp/runtime.py; cameras/test_camera_rtsp_runtime.py; docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md; docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md; docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md; docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md
TARGET_POLICY_ENV_PATH_SUPPORT = PASS
RUNTIME_COMPOSITION_ROOT = PASS
SERVICE_ENV_COUPLING = NONE
POLICY_LIFETIME = PER_INVOCATION
FAIL_CLOSED_BOOTSTRAP = PASS
TARGET_POLICY_TESTS = 24/24 PASS
RTSP_RUNTIME_TESTS = 5/5 PASS
RTSP_ADAPTER_TESTS = 17/17 PASS
RTSP_URI_TEST_MODULE = UNAVAILABLE / cameras.test_camera_rtsp_uri não existe neste checkout
RTSP_URI_EQUIVALENT_TESTS = cameras.test_camera_connection_config / 8/8 PASS
CAM_INT_03_FOCAL_TESTS = cameras.test_camera_rtsp_adapter / 17/17 PASS
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS / validado após atualizações documentais
CONTRACT_UPDATE = PASS
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE seção 55
REAL_RTSP_SESSION_STARTED = NO
SECRET_ACCESSED = NO
DATABASE_CHANGED = NO / somente banco temporário de testes, criado e destruído
NEW_ARCHITECTURAL_DECISION = NONE
CONTRACT_DEVIATION = NONE
TEST_SUITE_NAME_DEVIATION = cameras.test_camera_rtsp_uri ausente; cameras.test_camera_connection_config executada como equivalente (8/8)
CAM_INT_03_RUNTIME_STATUS = NOT_HOMOLOGATED
STAGING = EMPTY
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
NEXT_RECOMMENDED_ACTIVITY = CAM-INT-03-REAL-RTSP-RUNTIME-HOMOLOGATION-R2
```

Comportamento comprovado: `from_environment` lê `ARGOS_CAMERA_ALLOWED_PATHS`
com grupos `scheme:path[,path]`, usa o último grupo duplicado, preserva paths
duplicados, caixa e conteúdo após trim externo do transporte, rejeita membros
vazios e schemes sem portas correspondentes, e não ecoa configuração em erros.
Ausência da chave mantém compatibilidade genérica; a nova entrada RTSP exige
CIDR, porta RTSP e path RTSP antes de chamar o serviço. O runtime deriva as
portas da mesma policy, encaminha adapter/timeouts/clocks e preserva o resultado
do serviço. Policy é reconstruída por invocação. `service.py` não foi alterado e
permanece sem leitura de ambiente/settings.

O bootstrap inválido retorna `MISCONFIGURED_POLICY`, categoria
`TARGET_BLOCKED`, A/B/C/D `NOT_RUN`, duração zero e instante UTC-aware. Os
testes provaram que serviço, resolver de credencial, adapter e criação de
socket não são alcançados. Nenhuma sessão RTSP real, segredo ou banco de
aplicação foi acessado. O conjunto permanece local e sem staging; CAM-INT-03
continua não homologada.

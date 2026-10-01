# CAM-INT-07 — Hardening da integração de rede

```text
STATUS = ACTIVE / SECURITY BASELINE
REAL_NETWORK_HOMOLOGATION = NOT_PERFORMED
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL POLICY
IMPLEMENTER_TARGET = LUNA
```

## Autorização do destino

O worker deriva destino apenas de câmera elegível e configuração/perfil autorizado. Baseline é IPv4 cadastrado; hostname/DNS e alvo fornecido por request/browser são proibidos. IP sintaticamente válido ou privado não implica autorização: validar allowlist de CFTV do ambiente, protocolo, porta e segmento/farm. Rejeitar loopback, localhost, unspecified, link-local, multicast, broadcast, metadata endpoint e destinos administrativos fora da allowlist. Infraestrutura também limita egress; validação da aplicação não substitui firewall.

Porta deve estar entre 1 e 65535, autorizada simultaneamente pelo perfil e política de ambiente. HTTP redirects, proxy ambiental e DNS são desabilitados no baseline. Qualquer futura exceção exige adjudicação e validação de cada destino/hop e medidas contra DNS rebinding.

## Defesa e isolamento

Worker dedicado, não root, identidade de serviço própria, sem sessão humana, privilégio mínimo de banco e sem poderes implícitos de admin/captura. Segredos, chaves, banco, allowlists e credenciais são separados por ambiente. Aplicar timeouts e limites de resposta/stream, cancelamento previsível e encerramento de conexões. Captura não herda permissão/credencial de monitoramento sem contrato específico.

## Logging e resposta

Registrar identificador técnico opaco, adapter/profile version, categoria, duração e resultado operacional sanitizado. Nunca registrar IP completo quando a política o considerar sensível, credencial, URL, userinfo, query, payload, headers de auth ou chave. Acesso bloqueado por policy é `TARGET_BLOCKED`/diagnóstico operacional, não `OFFLINE` confirmado.

## Gate para homologação

Definir CIDRs e portas reais fora deste documento; aprovar autoridade de acesso; testar DNS/redirect/proxy, egress real, segmentação VLAN/firewall, identidade e privilégios, falhas de auth, limites, logs, rotação/restore e resposta a incidente. Nenhum CIDR, segredo ou endpoint real é registrado neste contrato. Fonte: ADR-021 §§3.7–3.8, 5–9, 12.

## BC-02 — policy local fechada

`TargetPolicy` imutável é carregada de configuração confiável por ambiente:
CIDRs positivos de CFTV, portas por protocolo, farm/segmento opcional e CIDRs
negados. Ausência, CIDR inválido ou lista vazia falha fechado; teste unitário
usa fixture sintética. O serviço de destino recebe somente `camera_id`,
consulta `Camera.ip` e `CameraConnectionConfig` persistidos, normaliza
`IPv4Address` em forma canônica e valida igualdade do host da URI RTSP com o
IP cadastrado. Rejeita hostname/DNS, forma ambígua, userinfo, fragmento,
query com segredo, IP especial/administrativo, porta fora de 1..65535,
scheme/path/port não permitidos pelo perfil ou policy, e target fora do CIDR.
Porta ausente usa default do perfil; RTSP sem default usa 554. O caller do
teste manual passa `camera_id`, nunca URL/alvo. Worker **repete** a validação
imediatamente antes da conexão; a UI não é fonte de autoridade. Qualquer
mudança de URI/IP/profile invalida configuração efetiva anterior e incrementa
geração. `TARGET_BLOCKED` é neutro para disponibilidade.

DNS, proxy de ambiente e redirects permanecem desabilitados. HTTP usa client
com proxy desativado e `allow_redirects=False`; RTSP conecta IPv4 validado.
Egress por firewall/VLAN é defesa operacional complementar: valores e teste
real pertencem à homologação e não bloqueiam codificar a policy local.
Credencial é entregue ao adapter por canal separado, nunca no URI/URL, log,
exception, trace, payload diagnóstico ou argumento de processo.

```text
MODEL_CHANGE = NONE
MIGRATION_REQUIRED = NO
EXPECTED_MODELS = existing Camera + CameraConnectionConfig
RELATIONSHIPS = NONE NEW
CONSTRAINTS = validated in policy/service
INDEXES = NONE NEW
DATA_MIGRATION = NO
ROLLBACK_CONSIDERATION = fail closed if policy unavailable
EXPECTED_PRIMARY_FILES = cameras/integracao/configuration.py
EXPECTED_NEW_FILES = cameras/integracao/target_policy.py
EXPECTED_TEST_FILES = cameras/test_camera_target_policy.py
SHARED_FILES = configuration resolver; no shared migration
ENVIRONMENT_CONFIGURATION_REQUIRED = YES / actual CIDRs, ports and egress
STOP_AND_ESCALATE_TO_SOL_IF = legitimate approved target cannot fit IPv4/CIDR
                              policy or requires DNS/redirect/proxy exception
```

Acceptance criteria:

1. Dado target fora da allowlist, especial ou host da URI diferente de
   `Camera.ip`, resolver retorna `TARGET_BLOCKED` sem abrir socket.
2. Dada policy ausente/inválida, worker e teste manual falham fechados; nenhum
   erro registra URI/segredo. Dado target sintético autorizado, request tipado
   contém apenas IPv4/porta/path controlados.
3. Dado redirect/proxy/DNS ou porta/scheme não permitidos, adapter rejeita
   antes de conectar ou seguir destino; mudança de configuração invalida
   geração anterior. Teste com rede/câmera real permanece pendente.

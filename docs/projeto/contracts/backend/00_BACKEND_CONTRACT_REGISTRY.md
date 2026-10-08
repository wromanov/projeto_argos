# Registro de contratos do backend ARGOS

```text
STATUS = ACTIVE / BASELINE BC-00
ACTIVITY = PRE-BC-00 — repository sync; BC-00 baseline authorized after sync
REPOSITORY_BASELINE = 38db46b2335ac8c1ce47207b3ae015388d839d5f
SCOPE = backend contracts; documentation only
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
BC02_STATUS = CONTRACT READINESS CLOSED / LOCAL IMPLEMENTATION QUEUE
BC02_ORDER = docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md
```

## Propósito e precedência

Este registro localiza os contratos do backend e define suas fronteiras. Ele não substitui ADRs existentes nem declara que capacidades descritas como futuras já estejam implementadas. Para conflito, prevalece a instrução humana vigente, depois a authority especializada do domínio, ADR aplicável e este índice. Os fatos de implementação são evidenciados no código e migrations referenciados por cada contrato.

`docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` continua sendo a authority canônica completa do domínio de imagens. O contrato de integração abaixo a complementa, sem redefinir proveniência, ordenação, `DISPLAY_IMAGE`, permissões ou lifecycle.

## Índice

| ID | Documento | Domínio | Base / autoridade principal |
|---|---|---|---|
| BC-REG | este registro | Mapa e governança | ARGOS Continuity; este baseline |
| BC-AUTH | [01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md](01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md) | identidade, grupos e permissões | `usuarios/management/commands/configurar_perfis_argos.py`; `usuarios/admin_security.py` |
| CAM-INT-01 | [camera/CAM-INT-01_CAPABILITY_CATALOG_CONTRACT.md](camera/CAM-INT-01_CAPABILITY_CATALOG_CONTRACT.md) | declaração de capacidade | ADR-021 §§3.5–3.6 |
| CAM-INT-02 | [camera/CAM-INT-02_CREDENTIALS_CONTRACT.md](camera/CAM-INT-02_CREDENTIALS_CONTRACT.md) | segredo de equipamento | ADR-021 §§3.1–3.4, 5–6 |
| CAM-INT-02-R1 | [camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md](camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md) | sub-slice: resolução interna de credencial para execução | CAM-INT-02; BC-AUTH; adjudicação CAM-INT-02-R1-ARCH |
| CAM-INT-03 | [camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md](camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md) | adapter RTSP | ADR-019; ADR-021 §§3.5–3.8 |
| CAM-INT-04 | [camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md](camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md) | captura HTTP | ADR-019; contrato de imagens |
| CAM-INT-05 | [camera/CAM-INT-05_TECHNICAL_DIAGNOSTICS_CONTRACT.md](camera/CAM-INT-05_TECHNICAL_DIAGNOSTICS_CONTRACT.md) | resultados de probe | ADR-020 §§3–5; `cameras/monitoramento/contracts.py` |
| CAM-INT-06 | [camera/CAM-INT-06_VENDOR_MODEL_CAPABILITIES_CONTRACT.md](camera/CAM-INT-06_VENDOR_MODEL_CAPABILITIES_CONTRACT.md) | compatibilidade declarativa | ADR-021 §§3.5–3.6 |
| CAM-INT-07 | [camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md](camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md) | fronteira de rede e hardening | ADR-021 §§3.7–3.8, 7–9 |
| CAM-HEALTH | [camera/CAMERA_HEALTH_DIAGNOSTIC_CONTRACT.md](camera/CAMERA_HEALTH_DIAGNOSTIC_CONTRACT.md) | diagnóstico de saúde | ADR-020; ADR-021; CAM-INT-05 |
| MON-AV | [monitoring/MONITORING_AVAILABILITY_CONTRACT.md](monitoring/MONITORING_AVAILABILITY_CONTRACT.md) | estado técnico | ADR-020; `cameras/models.py` |
| MON-PROBE | [monitoring/MONITORING_PROBE_CONTRACT.md](monitoring/MONITORING_PROBE_CONTRACT.md) | tentativa e reducer | ADR-020/021; `cameras/monitoramento/` |
| MON-WORKER | [monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md](monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md) | execução dedicada | ADR-019/021; scheduler local não é serviço de produção |
| MON-REC | [monitoring/MONITORING_FAILURE_RECOVERY_CONTRACT.md](monitoring/MONITORING_FAILURE_RECOVERY_CONTRACT.md) | fencing, idempotência e recuperação | migrations 0010–0012; repository/scheduler |
| MON-OWN | [monitoring/MONITORING_OWNERSHIP_CONTRACT.md](monitoring/MONITORING_OWNERSHIP_CONTRACT.md) | ownership e autoridade de escrita | migration 0012; `DjangoMonitoringRepository` |
| MON-OBS | [monitoring/MONITORING_OBSERVABILITY_CONFIG_CONTRACT.md](monitoring/MONITORING_OBSERVABILITY_CONFIG_CONTRACT.md) | configuração e telemetria | ADR-021 §8; `MonitoringConfig` |
| MON-HIST | [monitoring/MONITORING_HISTORICAL_AVAILABILITY_CONTRACT.md](monitoring/MONITORING_HISTORICAL_AVAILABILITY_CONTRACT.md) | transições e indisponibilidade | ADR-020 §13; models/migration 0011 |
| IMG-CAP | [images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md](images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md) | integração de captura com domínio de imagem | `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`; ADR-019 |
| PROD-PERSIST | [production/PRODUCTION_PERSISTENCE_CONTRACT.md](production/PRODUCTION_PERSISTENCE_CONTRACT.md) | persistência e storage em produção | ADR-021; settings atuais |
| PROD-TOPO | [production/RUNTIME_TOPOLOGY_CONTRACT.md](production/RUNTIME_TOPOLOGY_CONTRACT.md) | processos, workers e fronteiras | ADR-019/021 |
| PROD-CAP | [production/CAPACITY_AND_RESOURCE_BOUNDARIES_CONTRACT.md](production/CAPACITY_AND_RESOURCE_BOUNDARIES_CONTRACT.md) | envelope medido e limites | evidência MON-08/09; `MonitoringConfig` |

## Leitura do status

- **Implementado localmente**: modelos e fluxos Django, reducer/scheduler em biblioteca, lease/fencing de persistência, serviços de leitura e upload/preview de imagem. Isso não equivale a deployment de worker, homologação de rede ou backend de produção.
- **Decidido como invariante**: browser não executa probe; monitoramento é separado de situação operacional e de captura; `UNKNOWN/ONLINE/OFFLINE` são os estados estáveis; segredos não vão a URL/log; destinos e capacidades exigem validação positiva.
- **Não decidido / não comprovado**: PostgreSQL operacional, topologia e scheduler de produção, adapters reais RTSP/HTTP, parque e credenciais reais, allowlists de CFTV, SLA/capacidade de produção, rotação de chave, backend definitivo de imagens e thresholds temporais de operação.

## Limite de autoridade

Este baseline documental não autoriza migrations, mudança de schema, adapters reais, acesso a câmeras, provisionamento de segredos, deploy, homologação, LIVE, commit ou push. Cada decisão técnica que exceda invariantes já aprovados requer autoridade própria e validação no ambiente correspondente.

## BC-02 — classificação final da fila local

O pedido humano BC-02 adjudicou quatro perfis (`Monitoramento`, `Operador`,
`Técnico`, `Administrador`), URI RTSP informada por Técnico/Admin sem
credenciais, discovery-first, transport AUTO, health A/B/C/D, ONLINE somente
após D PASS confirmado e teste manual sem mutação do monitoramento. As
extensões BC-02 em cada contrato substituem trechos de baseline BC-00 que
descrevem três grupos, decisões técnicas abertas ou estados anteriores.
BC-02 fecha decisões de **arquitetura local**; readiness não autoriza execução,
câmera real, rede, homologação, produção, commit ou push.

| Contrato | Classificação BC-02 | Pré-requisito / validação pendente |
|---|---|---|
| BC-AUTH | IMPLEMENTATION_READY | primeira slice; nenhum predecessor local |
| CAM-INT-01 | IMPLEMENTATION_READY | BC-AUTH para gestão de perfil |
| CAM-INT-02 | IMPLEMENTATION_READY | BC-AUTH e CAM-INT-01 schema; chave externa real só para operação |
| CAM-INT-02-R1 | IMPLEMENTATION_READY | CAM-INT-02 publicada; API, input/output, falhas, autorização, invariantes, ownership, testes e AC-R1-01..04 fechados; resolver não implementado |
| CAM-INT-03 | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING / READY_NOW=NO | CAM-INT-01/02/02-R1/06/07; PAUSED_ARCHITECTURAL_DEPENDENCY até R1 publicada; câmera, codec e transporte reais |
| CAM-INT-04 | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING / READY_NOW=NO | CAM-INT-01/02/02-R1/06/07; R1 necessária para Basic/Digest; endpoint/vendor real |
| CAM-INT-05 | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING | CAM-INT-03; A-D/fake local; mídia real depois |
| CAM-INT-06 | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING | CAM-INT-01; dados reais fabricante/firmware externos |
| CAM-INT-07 | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING | CIDR, egress e rede reais por ambiente |
| CAM-HEALTH | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING | CAM-INT-05; validação real depois |
| MON-AV | ALREADY_IMPLEMENTED | core local; integração D e limiares reais depois |
| MON-PROBE | ALREADY_IMPLEMENTED | core local; adapter real depois |
| MON-WORKER | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING | MON-OBS, CAM-INT-05, core existente; deploy depois |
| MON-REC | ALREADY_IMPLEMENTED | SQLite local; PostgreSQL/multi-worker depois |
| MON-OWN | ALREADY_IMPLEMENTED | SQLite local; PostgreSQL/multi-worker depois |
| MON-OBS | IMPLEMENTATION_READY | sink/port local; backend operacional depois |
| MON-HIST | ALREADY_IMPLEMENTED | histórico local; retenção futura |
| IMG-CAP | IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING | CAM-INT-03/04, BC-AUTH; câmera/storage real depois |
| PROD-PERSIST | PRODUCTION_ONLY | PostgreSQL, provider, backup/restore e storage |
| PROD-TOPO | PRODUCTION_ONLY | supervisor, identidade, egress, réplicas |
| PROD-CAP | PRODUCTION_ONLY | medição real e budgets aprovados |

```text
TOTAL_SPECIALIZED_CONTRACTS = 20
COUNTS_SCOPE = HISTORICAL_BC02_BASELINE / excludes the later CAM-INT-02-R1 sub-slice
IMPLEMENTATION_READY = 4
IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING = 8
ALREADY_IMPLEMENTED = 5
PRODUCTION_ONLY = 3
DEFERRED = 0 entire contracts; internal production/retention decisions remain
BLOCKED_HUMAN_DECISION = 0 for local queue
FIRST_LUNA_SLICE = BC-AUTH
DEFAULT_IMPLEMENTER = LUNA
SECURITY_REMEDIATION = DEFERRED_TO_FINAL_SECURITY_GATE
```

O DAG, waves, ownership, conflitos de migration, primeira slice e limites de
ambiente estão em [BACKEND_IMPLEMENTATION_ORDER.md](BACKEND_IMPLEMENTATION_ORDER.md).
Permissões e trust boundaries são invariantes imediatos, independentemente
do Security Gate final. P5 pode avançar em sua track própria; a integração de
RTSP, credential/reveal, teste manual e health A-D depende dos contratos
backend indicados, sem bloquear P5-0 por inferência.

## CAM-INT-02-R1-ARCH — readiness corrente (2026-10-02)

A tabela BC-02 preserva a classificação de arquitetura local dos contratos;
implementações publicadas devem ser verificadas no código e em PROJECT_STATE.
CAM-INT-02 já publicou custódia/lifecycle/reveal, mas não o resolver operacional.
R1 é uma sub-slice, não nova authority de custódia: 20 contratos especializados
originais + 1 sub-slice de execução. Os contadores acima são a fotografia BC-02,
não totais recalculados de implementação corrente.

```text
CAM_INT_02_R1_ID = CAM-INT-02-R1
CAM_INT_02_R1_TITLE = Runtime Credential Resolution Boundary
CAM_INT_02_R1_STATUS = IMPLEMENTATION_READY / NOT_IMPLEMENTED
CAM_INT_02_R1_READY_NOW = YES / predecessor CAM-INT-02 published; authorization still required
RUNTIME_RESOLUTION_OWNER = CAM-INT-02
CAM_INT_03_STATUS = PAUSED_ARCHITECTURAL_DEPENDENCY
CAM_INT_03_READY_NOW = NO / CAM-INT-02-R1 not published
CAM_INT_04_REQUIRES_R1 = YES / contracted Basic/Digest authentication
CAM_INT_04_READY_NOW = NO / CAM-INT-02-R1 not published
CAM_INT_04_EXECUTION_STATUS = LOCAL_CHANGES_OBSERVED / completion and pause not adjudicated
IMPLEMENTATION_AUTHORIZED_BY_THIS_REGISTRY = NO
```

A adjudicação supersede as conclusões anteriores de readiness imediata de
CAM-INT-03/04, preservadas como histórico nos checkpoints CAM-INT-07. R1 fecha
API/input/output/failures, autorização externa versus resolução interna,
invariantes, ownership, testes e critérios de aceite no contrato especializado.
Consumers retomam seu gate apenas após implementação, integração, validação e
publicação de R1, sob suas autorizações próprias. Homologação continua pendente.

## Estado factual corrente das dependências (2026-10-08)

Esta atualização factual supersede os status de implementação desatualizados
na fotografia BC-02 e na adjudicação R1 de 2026-10-02; preserva suas decisões
arquiteturais e ownership.

| Lane | Estado factual corrente |
|---|---|
| CAM-INT-02-R1 | Implementada, integrada, validada localmente e publicada; ver PROJECT_STATE §50. |
| CAM-INT-03 | Implementada, publicada e homologada; regressão local integrada PASS (68/68); sem nova sessão RTSP real nesta atividade. |
| CAM-INT-04 | HTTP Snapshot e composição HTTP-R1 integrados e validados localmente; default_path inalterado; path customizado depende exclusivamente de allowlist ambiental explícita e exata; publicação e homologação real permanecem pendentes. |
| IMG-CAP | Implementação local HTTP-only validada (service 16/16; worker 1/1); RTSP e storage de produção permanecem pendentes; sem homologação real. |

A extensão ambiental de paths está documentada no contrato CAM-INT-03 TargetPolicy. `ARGOS_CAMERA_ALLOWED_PATHS` só transporta uma allowlist confiável explícita; não muda `default_path`, não amplia autorização por perfil e não permite fallback. Configuração ausente, inválida, não listada ou revogada permanece fail-closed. Nenhuma dessas declarações autoriza runtime real, migration no banco operacional, push ou incorporação ao master.

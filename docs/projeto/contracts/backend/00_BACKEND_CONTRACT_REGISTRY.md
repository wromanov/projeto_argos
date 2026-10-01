# Registro de contratos do backend ARGOS

```text
STATUS = ACTIVE / BASELINE BC-00
ACTIVITY = PRE-BC-00 — repository sync; BC-00 baseline authorized after sync
REPOSITORY_BASELINE = 38db46b2335ac8c1ce47207b3ae015388d839d5f
SCOPE = backend contracts; documentation only
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
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

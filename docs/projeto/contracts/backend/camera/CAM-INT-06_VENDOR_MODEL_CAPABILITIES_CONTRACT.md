# CAM-INT-06 — Capabilities por fabricante, modelo e firmware

```text
STATUS = ACTIVE / COMPATIBILITY CONTRACT
CATALOG_DATA = NOT PRESENT
BC02_STATUS = IMPLEMENTATION_READY_ENVIRONMENT_VALIDATION_PENDING
IMPLEMENTATION_READY = YES / LOCAL FRAMEWORK
IMPLEMENTER_TARGET = LUNA
```

## Chave de compatibilidade

Compatibilidade pode depender de fabricante, modelo exato, revisão/firmware, região, licença e configuração real da unidade. `fabricante`, `modelo`, `tipo`, `codec` e `farm` de `Camera` são dados cadastrais; não são prova de adapter, endpoint, protocolo ou autenticação suportados. Ausência de correspondência significa não verificado e bloqueia integração que dependa da capability.

Registro futuro de compatibilidade referencia a versão do perfil CAM-INT-01, versão/escopo observado, fontes de evidência e data/revisor. `SUPPORTED`, `UNSUPPORTED` e `UNVERIFIED` devem ser distinguíveis. Um resultado de laboratório limitado a modelo/firmware/ambiente não pode ser generalizado silenciosamente para toda a marca.

## Variação por unidade

Mesmo modelo pode ter endpoint, porta, firmware, VLAN ou credenciais distintos. Perfil compartilhado fornece defaults e limites; configuração por câmera só sobrescreve campos explicitamente autorizados. Endpoint secreto ou credencial não fica no catálogo público. Capacidade de stream não implica snapshot; snapshot não implica health; ONVIF não implica stream operacional.

## Estado e decisão pendente

No checkout BC-02 ainda não há catálogo estruturado ou capability matrix implementado. O schema/matching local é fechado abaixo; curadoria de dados reais, cadência de revalidação e escopo de suporte exigem levantamento dos ativos e laboratório controlado. Não popular capacidades presumidas para produzir aparência de cobertura.

Referências: ADR-021 §§3.5–3.6 e §12; CAM-INT-01/03/04.

## BC-02 — framework separado dos dados reais

`Camera.firmware_version` é novo campo técnico opcional, editável somente por
Técnico/Admin e sem migração inferida. `CameraCapabilityEvidence` referencia
`CameraCapabilityProfile` versionado,
`vendor` e `model` normalizados (casefold/whitespace para matching),
`firmware_exact` opcional, `camera_id` opcional para evidência de unidade,
`status` `SUPPORTED/UNSUPPORTED/UNVERIFIED`, `source_type`
`DATASHEET/LAB/UNIT`, `source_ref` não secreto, data, ambiente, limite,
revisor e `active`. Não extrapolar firmware ausente para firmware diferente;
matching por unidade exata precede modelo+firmware exatos; não há fallback
para marca genérica `SUPPORTED`. Ausência/ambiguidade retorna `UNVERIFIED`.
Uma evidência `UNSUPPORTED` explícita impede seleção. Mudança de cadastro
fabricante/modelo/firmware ou profile version invalida matching anterior.

O framework pode ser implementado e testado com fixtures sintéticas sem dados
reais de parque. Perfil genérico de discovery permite teste manual controlado,
mas não converte `UNVERIFIED` em `SUPPORTED`; monitoramento automático e
captura exigem evidência SUPPORTED adequada ao perfil/unidade. Fonte real,
inventário de firmware e resultados de laboratório permanecem
`REAL_DATA_VALIDATION = EXTERNAL`.

```text
MODEL_CHANGE = Camera.firmware_version + CameraCapabilityEvidence
MIGRATION_REQUIRED = YES
EXPECTED_MODELS = Camera; CameraCapabilityEvidence
RELATIONSHIPS = Profile 1:N Evidence; Camera optional FK for unit evidence
CONSTRAINTS = status/source enums; source_ref/version required; no duplicate
              active evidence for same profile/vendor/model/firmware/camera/source
INDEXES = (profile,vendor,model,firmware_exact,status); (camera,profile)
DATA_MIGRATION = NO; do not infer support from free-text cadastro
ROLLBACK_CONSIDERATION = preserve evidence/audit export before schema removal
EXPECTED_PRIMARY_FILES = cameras/models.py
EXPECTED_NEW_FILES = cameras/integracao/compatibility.py
EXPECTED_TEST_FILES = cameras/test_camera_compatibility.py
SHARED_FILES = cameras/models.py; migrations; profile resolver
STOP_AND_ESCALATE_TO_SOL_IF = matching requires uncontracted wildcard/firmware
                              policy or unsupported status semantics
```

Acceptance criteria:

1. Dada câmera/modelo/firmware sem evidência exata, resolver retorna
   UNVERIFIED; dado SUPPORTED de outro firmware, continua UNVERIFIED.
2. Dada evidência de unidade contraditória com modelo, regra de unidade
   prevalece e conflito é diagnosticado; `UNSUPPORTED` bloqueia uso.
3. Dadas fixtures sintéticas, matcher é determinístico; nenhuma linha real
   de fabricante é gerada por migration/default.

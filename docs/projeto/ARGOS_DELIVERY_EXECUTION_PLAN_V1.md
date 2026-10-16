# ARGOS — Plano Operacional de Execução e Entrega v1

```text
DOCUMENT_ID = ARGOS_DELIVERY_EXECUTION_PLAN_V1
PROJECT_ID = projeto_argos
ACTIVITY = ARGOS-DELIVERY-ROADMAP-CANONICALIZATION-01
STATUS = CURRENT / USER_APPROVED_DIRECTION
EFFECTIVE_DATE = 2026-10-16
SCOPE = product delivery sequencing and controlled homologation protocol
MODE = DOCUMENTATION_ONLY
```

## 1. Autoridade, vigência e objetivo

Este plano registra a direção operacional aprovada pelo usuário em 2026-10-16
para finalizar capacidades pendentes em slices verticais, integrar backend e UI,
validar localmente, integrar ao baseline e avançar a homologação sob gates.
Aplica-se à continuidade do ARGOS entre agentes e computadores. Não substitui
contratos técnicos, authorities especializadas, políticas de segurança nem os
registros históricos de HOM.

Sequência de produto aprovada:

```text
FINALIZAR FUNCIONALIDADES PENDENTES
→ INTEGRAR BACKEND E UI
→ TESTAR LOCALMENTE
→ INTEGRAR NO BASELINE
→ PUBLICAR EM HOMOLOGAÇÃO SOB GATE
→ TESTAR NA VM
→ CORRIGIR
→ AVANÇAR PARA A PRÓXIMA SLICE
```

Usar ciclos incrementais completos e evitar auditorias globais repetidas ou
revisões arquiteturais sem conflito material. Esta canonicalização não executa
`ARGOS-QA-01`, não implementa funcionalidades e não altera código, banco, VM ou
ambiente de homologação.

## 2. Estado operacional e marcos formais

```text
VM_OPERATIONAL_USER_REPORT = YES
VM_INDEPENDENTLY_VERIFIED_BY_AGENT = NO
VM_REPORTED_CONFIGURATION = PostgreSQL; ARGOS em execução
HOM03_FORMAL_CLOSURE = NOT_ESTABLISHED
HOM04_FORMAL_OPENING = NOT_ESTABLISHED
HOM05_FORMAL_OPENING = NOT_ESTABLISHED
```

O relato do usuário de que a VM está operacional deve ser preservado. Operação
reportada não equivale à prontidão formal HOM-03: evidências e critérios do
contrato HOM-03 ainda precisam ser aceitos. Não presumir indisponibilidade por
falta de acesso SSH de um agente, nem repetir implantação, configuração ou
criação de banco que já esteja operacional. HOM-04 continua sendo gate de
abertura formal com os pré-requisitos vigentes; HOM-05 não é formalmente aberta
antes de HOM-04. Slices de produto podem ser preparadas em lanes isoladas antes
desses marcos, conforme seus contratos e autorizações próprios.

## 3. Programa de execução E0–E8

E0–E8 identificam o novo programa operacional e não substituem IDs contratuais
IMG, CAM-INT, BC ou fases HOM. Status indica o que está planejado nesta data;
planejamento não prova início, implementação, integração, validação ou aceite.

| Etapa | Slice(s) | Objetivo e dependências | Status |
|---|---|---|---|
| E0 — Estabilização para entrega | `ARGOS-QA-01` | Corrigir fixture do QA visual que não corresponde a `VISUAL_QA_USERNAME` na configuração usada; confirmar a falha focal e validar a correção em atividade própria. Evidência histórica: Python 3.14.7, Django 5.2.18, system check PASS, 14 testes XLSX PASS, suíte cameras 727 testes/1 erro; falha reproduzida isoladamente. | `PENDING_IMPLEMENTATION`; proposta preparada, não aplicada |
| E1 — Credenciais por câmera | `ARGOS-CRED-UI-01` | Integrar em Editar câmera os serviços backend já existentes e contratos de credenciais/segurança. Dependências: authorities CAM-INT-02, resolver runtime, autorização, reauth e auditoria. Nunca expor senha em HTML, logs ou histórico cadastral. | `PLANNED` |
| E2 — Imagem principal / Quick Detail | `ARGOS-IMG-07-CONFORMANCE` | Fazer Quick Detail selecionar `LATEST_ACTIVE_IMAGE` segundo contrato de imagem §26, qualquer que seja a proveniência. Preservar a semântica técnica separada de `LATEST_CAMERA_CAPTURE`. | `PLANNED` |
| E3 — Captura manual de imagens | `IMG-04` / `IMG-05` / `CAM-INT-04` | Reconciliar código da branch isolada, dependências, migrations e integração. Adicionar ação Capturar imagem junto a Importar imagem na seção Imagens. Captura somente por ação humana; nunca por MON. | `PLANNED` |
| E4 — Galeria de imagens | `IMG-06` | Implementar até três imagens ativas por câmera, em ordem cronológica crescente, conforme contrato aprovado. | `PLANNED` |
| E5 — Segurança e lifecycle | `IMG-08` / `IMG-09` | Implementar capacidades aprovadas de proteção, rotação, retenção e auditoria; retenção padrão de 12 meses; validar nova imagem antes da rotação. Expurgo físico exige contrato e autorização específicos. | `PLANNED` |
| E6 — Inventário / exportação | `ARGOS-INV-EXPORT-01` | Implementar exportação reutilizando modelo cadastral e regras existentes. Não reabrir aceite funcional HOM-02. | `PLANNED` |
| E7 — UI V2 residual | Slices do master plan UI V2 | Concluir superfícies pendentes, corrigir divergências visuais e fazer Design QA no escopo integrado. HOM-01 permanece aprovada/fechada; não inferir P7 global concluída. | `PLANNED` |
| E8 — Alertas e capacidades restantes | Slices pendentes em authorities | Priorizar alertas internos, lifecycle, deduplicação, observabilidade e outras capacidades pendentes segundo contratos existentes. | `PLANNED` |

Dependências e critérios específicos continuam nas authorities citadas no mapa
de documentos ativos e no mapa de sprints. Reutilizar serviços, componentes,
templates e Design System existentes. Se surgir conflito material ou ausência
de contrato suficiente, interromper somente a slice afetada e encaminhar a
lacuna para adjudicação apropriada.

## 4. Ciclo vertical e gates de slice

Para cada slice, confirmar escopo, authority, dependências e autorização própria;
integrar a superfície de UI quando aplicável; executar testes direcionados e
regressão proporcional; revisar segurança, permissões e auditoria aplicáveis;
fazer Design QA e obter aceite visual quando aplicáveis; revisar diff e
migrations; integrar de forma controlada ao baseline; registrar evidências,
findings e aceite real; somente então avaliar publicação homologada conforme a
trilha H. Código escrito sozinho não conclui uma slice. `READY` não equivale a
`ACCEPTED`.

## 5. H — Controlled Homologation Delivery

Esta trilha transversal se aplica a cada slice elegível:

1. Implementação técnica concluída.
2. UI integrada quando aplicável.
3. Testes direcionados PASS.
4. Regressão proporcional PASS.
5. Permissões e segurança verificadas.
6. Design QA e aceite visual quando aplicáveis.
7. Integração controlada no baseline.
8. Revisão do diff e das migrations.
9. Backup/rollback definido quando aplicável.
10. Autorização específica de publicação.
11. Atualização controlada na VM.
12. Smoke e testes no ambiente homologado.
13. Findings, limitações e aceite registrados.

Esta trilha não declara autorização de deploy, HOM-03 fechada ou HOM-04 aberta.
Não executar nesta atividade deploy, migrations na VM, habilitação automática de
worker/probes reais ou acesso a câmeras reais. Cada operação futura exige sua
autorização e gates específicos.

## 6. Publicação controlada, rollback e riscos

Antes de uma publicação futura, identificar baseline e diff exatos, revisar
migrations e compatibilidade, definir janela/owner, backup e procedimento de
rollback quando aplicável, confirmar autorização específica e preservar
configuração e dados locais da VM. Interromper a promoção diante de falha de
migration, health check, smoke, segurança ou integridade; registrar evidência,
executar rollback conforme plano autorizado e não avançar à slice seguinte até
resolver o finding ou obter adjudicação. Não realizar rollback destrutivo nem
alterar dados sem autoridade.

Riscos e bloqueios atuais: prontidão formal HOM-03 não estabelecida apesar do
relato operacional; HOM-04 e HOM-05 não abertas formalmente; E0 ainda não
implementada; integração das slices de produto depende das authorities,
dependências e autorizações próprias. Nenhum destes estados deve ser promovido
por inferência.

## 7. Continuidade entre casa e trabalho

Em cada retomada, confirmar repo root, branch, HEAD, origem remota, worktree e
WIP; preservar alterações locais e reconciliar diferenças antes de trocar de
branch ou transportar mudanças. Não copiar `.env`, secrets, sessões, bancos,
venvs ou dados operacionais entre computadores. Usar Git e os documentos de
continuidade como fontes de verdade dentro de seus escopos; registrar diferenças
com evidência e não reconciliá-las silenciosamente. O caminho da máquina CASA e
o da máquina de trabalho são distintos.

## 8. Progresso e continuidade para próximo agente

Em todo acompanhamento da execução, informar:

```text
PROJECT_ID
ROADMAP_STAGE
ACTIVE_SLICE
SLICE_STATUS
NEXT_GATE
NEXT_SLICE
```

Atualizar apenas por evidência real; não antecipar mudança de etapa por concluir
planejamento. Registrar estado, próximo gate e próxima slice preservando o
histórico e atualizando continuidade aplicável. O próximo agente deve ler
`AGENTS.md`, `ACTIVE_DOCUMENT_MAP.md`, `PROJECT_STATE.md`, `AGENT_CONTINUITY.md`,
este plano, Roadmap, Sprints e authorities especializadas da slice. Não repetir
auditoria global sem necessidade; fazer preflight focal da próxima slice.

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E0 — Estabilização para entrega
ACTIVE_SLICE = ARGOS-QA-01
SLICE_STATUS = PENDING_IMPLEMENTATION
NEXT_GATE = correção focal da fixture e testes direcionados, em atividade própria
NEXT_SLICE = ARGOS-CRED-UI-01
VM_OPERATIONAL_USER_REPORT = YES
VM_AGENT_VERIFIED = NO
HOM03_FORMAL_CLOSURE = NOT_ESTABLISHED
HOM04_FORMAL_OPENING = NOT_ESTABLISHED
HOM05_FORMAL_OPENING = NOT_ESTABLISHED
```

## 9. Authorities relacionadas

- `AGENTS.md` e pacote canônico de continuidade/políticas.
- `docs/projeto/ROADMAP_ARGOS_V5.md` e `docs/projeto/SPRINTS_ARGOS_V5.md`.
- `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`.
- `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`, especialmente §26.
- `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md`.
- `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md` e
  `CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`.
- `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md`.
- Contratos de captura e imagem em `docs/projeto/contracts/backend/camera/` e
  `docs/projeto/contracts/backend/images/`.
- Mapa dos contratos HOM e segurança conforme `SPRINTS_ARGOS_V5.md`.

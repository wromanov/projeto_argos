# ARGOS UI V2 — Screen Coverage

Matriz derivada do Screen Census. As linhas abaixo preservam o snapshot histórico de planejamento do P3-0; seus campos de implementação/aprovação não representam o estado corrente após a integração das famílias. O checkpoint ROOT vigente está registrado ao fim deste arquivo.

- Fonte: docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md, seção 10.
- Prototype e responsive relevance vêm do census.
- YES em estado indica que o censo nomeia o estado; NOT_DECLARED não conclui que o runtime não o suporte.
- LONG_CONTENT permanece PLANNED até validação visual do protótipo da tela.
- USER_APPROVED, IMPLEMENTED e RUNTIME_VISUAL_QA nas linhas continuam sendo valores do snapshot histórico P3-0; veja o checkpoint ROOT atual abaixo.

| SCREEN | FAMILY | PROTOTYPE | RESPONSIVE | EMPTY_STATE | LOADING_STATE | ERROR_STATE | LONG_CONTENT | USER_APPROVED | DESIGN_SYSTEM_VERSION | IMPLEMENTED | RUNTIME_VISUAL_QA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SCR-SHELL-001 — Shell autenticado | SHELL | INHERITED | HIGH | NOT_DECLARED | NOT_DECLARED | NOT_DECLARED | PLANNED | YES | 2.0.0 | NO | PENDING |
| SCR-PORTAL-001 — Início / portal | OTHER | YES | MEDIUM | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-DASH-001 — Dashboard | DASHBOARD | YES | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-INV-001 — Inventário de câmeras | INVENTORY | YES | HIGH | YES (census) | YES (census) | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-CAM-DETAIL-001 — Detalhe da câmera | CAMERA_DETAIL | YES | HIGH | YES (census) | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-CAM-QUICK-001 — Quick Detail | CAMERA_DETAIL | INHERITED | HIGH | NOT_DECLARED | YES (census) | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-CAM-CREATE-001 — Nova câmera | CAMERA_FORMS | YES | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-CAM-EDIT-001 — Editar câmera | CAMERA_FORMS | YES | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-MON-HISTORY-001 — Histórico de monitoramento | MONITORING | YES | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ACT-LIST-001 — Atividades da câmera | ACTIVITIES | YES | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ACT-CREATE-001 — Registrar atividade | ACTIVITIES | YES | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ACT-EDIT-001 — Editar atividade | ACTIVITIES | INHERITED | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-GOV-STATE-001 — Alterar situação | GOVERNANCE | YES | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-GOV-DISABLE-001 — Desativar câmera | GOVERNANCE | YES | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-GOV-REACTIVATE-001 — Reativar câmera | GOVERNANCE | YES | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-GOV-SUBSTITUTE-001 — Substituir câmera | GOVERNANCE | YES | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-SUB-LIST-001 — Substituições | SUBSTITUTIONS | YES | HIGH | YES (census) | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-SUB-DETAIL-001 — Detalhe da substituição | SUBSTITUTIONS | YES | MEDIUM | NOT_DECLARED | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-SUB-CAMERA-001 — Substituições da câmera | SUBSTITUTIONS | YES | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-EVENT-LIST-001 — Eventos de auditoria | EVENTS_AUDIT | YES | HIGH | YES (census) | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-EVENT-DETAIL-001 — Detalhe do evento | EVENTS_AUDIT | YES | MEDIUM | NOT_DECLARED | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-EVENT-CAMERA-001 — Eventos da câmera | EVENTS_AUDIT | YES | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ACCOUNT-PROFILE-001 — Perfil | PROFILE_ACCOUNT | YES | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ACCOUNT-EDIT-001 — Editar perfil | PROFILE_ACCOUNT | YES | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ACCOUNT-PASSWORD-001 — Alterar senha | PROFILE_ACCOUNT | YES | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-AUTH-LOGIN-001 — Login ARGOS | AUTH | YES | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ERROR-403-001 — Acesso negado | ERROR_PAGES | YES | LOW | NOT_DECLARED | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-LOGIN-001 — Login Admin | ADMIN | INHERITED | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-INDEX-001 — Índice Admin | ADMIN | INHERITED | MEDIUM | NOT_DECLARED | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-APP-001 — Lista de app Admin | ADMIN | INHERITED | MEDIUM | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-CHANGE-LIST-001 — Changelist Admin | ADMIN | INHERITED | HIGH | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-FORM-001 — Formulário Admin | ADMIN | INHERITED | HIGH | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-HISTORY-001 — Histórico Admin | ADMIN | INHERITED | MEDIUM | YES (census) | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-DELETE-001 — Confirmação Admin | ADMIN | INHERITED | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |
| SCR-ADMIN-PASSWORD-001 — Troca de senha Admin | ADMIN | INHERITED | MEDIUM | NOT_DECLARED | NOT_DECLARED | YES (census) | PLANNED | NO | 2.0.0 | NO | PENDING |

## UI-V2-P3-0 — modelo de ownership e integração

Este master continua owned por ROOT/Integrator. O índice atual do Census mantém os 35 `SCREEN_ID`s e suas famílias; a matriz canônica de owner exclusivo, `PROTOTYPE_PATH` planejado e status inicial foi derivada dessa lista e está em [`P3_PROTOTYPE_HARNESS.md`, seção 9](P3_PROTOTYPE_HARNESS.md#9-ownership-matrix-por-screen_id). Cada ID aparece uma vez; screens inherited continuam cobertas sem criar redesign.

Status após a revisão humana: `SCR-SHELL-001 = USER_APPROVED` (harness aprovado; runtime visual da tela permanece `PENDING` porque `IMPLEMENTED = NO`); `SCR-CAM-QUICK-001 = PROTECTED`; `SCR-ACT-EDIT-001` e oito screens ADMIN = `INHERITED`; as 24 screens elegíveis = `PLANNED`. Nenhuma screen de família foi implementada ou aprovada. A cobertura de estados e runtime visual por tela permanece pendente até as páginas de cada família serem produzidas e validadas.

Durante o fan-out, famílias registram coverage/evidence localmente. ROOT consolida o master somente após revisar e integrar uma família por vez. Cada relatório deve declarar owner e `SCREEN_ID`; `STATE_COVERAGE` por estado usa `SUPPORTED`, `TESTED` ou `NOT_APPLICABLE`, e responsive status registra o resultado por viewport. `USER_APPROVED` exige aprovação humana explícita. `DESIGN_SYSTEM_VERSION = 2.0.0` é herdado por toda linha.

## P3 ROOT Integration Phase 1 — estado atual (2026-09-30)

DESIGN_SYSTEM_VERSION = 2.0.2
P3_A = USER_APPROVED / CLOSED / PUBLISHED
P3_B = USER_APPROVED / FROZEN / CLOSED / PUBLISHED
P3_C = USER_APPROVED / FROZEN / CLOSED / PUBLISHED
P3_D = USER_APPROVED / FROZEN / ROOT_DS_RECONCILED / INTEGRATED_VALIDATION_PENDING
P3_FAMILY_GATES_COMPLETE = YES
P3_ROOT_INTEGRATION = MERGED / RECONCILED / VALIDATION_PENDING
P3_INTEGRATED_VALIDATION = PENDING
P3_COMPLETE = NO
NEXT_GATE = P3 ROOT INTEGRATED VALIDATION

Este checkpoint não declara conclusão global de P3 nem conclui a validação de runtime/browser integrada.

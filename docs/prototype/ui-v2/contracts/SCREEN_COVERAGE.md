# ARGOS UI V2 — Screen Coverage

Matriz de planejamento derivada do Screen Census. Esta foundation não inicia P3 nem implementa protótipos de tela. Estado: Design System 2.0.0 aprovado. Protótipos, aprovação visual por tela, implementação e QA de runtime continuam planejados para atividades futuras; P3 não foi iniciado.

- Fonte: docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md, seção 10.
- Prototype e responsive relevance vêm do census.
- YES em estado indica que o censo nomeia o estado; NOT_DECLARED não conclui que o runtime não o suporte.
- LONG_CONTENT permanece PLANNED até validação visual do protótipo da tela.
- USER_APPROVED=NO; IMPLEMENTED=NO; RUNTIME_VISUAL_QA=PENDING em todas as linhas.

| SCREEN | FAMILY | PROTOTYPE | RESPONSIVE | EMPTY_STATE | LOADING_STATE | ERROR_STATE | LONG_CONTENT | USER_APPROVED | DESIGN_SYSTEM_VERSION | IMPLEMENTED | RUNTIME_VISUAL_QA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SCR-SHELL-001 — Shell autenticado | SHELL | INHERITED | HIGH | NOT_DECLARED | NOT_DECLARED | NOT_DECLARED | PLANNED | NO | 2.0.0 | NO | PENDING |
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

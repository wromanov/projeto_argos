# DSCR-UIV2-001 — Semântica global de [hidden]

ID = DSCR-UIV2-001-HIDDEN-SEMANTICS
STATUS = APPROVED / IMPLEMENTED / TARGETED_VALIDATION_PASS
CHANGE = Promover o Design System ARGOS UI V2 de 2.0.0 para 2.0.1 e impor a semântica HTML de [hidden] na camada reset compartilhada.
ROOT_CAUSE = Regras autorais com display nos patterns/componentes compartilhados prevalecem sobre o display:none do user-agent para [hidden]. Reprodução em .argos-state: display:grid com hidden; também em .argos-alert: display:flex e .argos-two-column: display:grid.
OWNER = ROOT / UI-V2 DESIGN SYSTEM INTEGRATOR
AFFECTED_COMPONENTS = [hidden] global; .argos-state; .argos-alert; .argos-two-column; links de navegação que declaram display
AFFECTED_SCREEN_IDS = P3-A: SCR-CAM-DETAIL-001, SCR-DASH-001, SCR-INV-001, SCR-PORTAL-001; P3-B: SCR-MON-HISTORY-001, SCR-SUB-CAMERA-001, SCR-SUB-LIST-001; P3-C: SCR-ACT-CREATE-001, SCR-ACT-LIST-001, SCR-EVENT-CAMERA-001, SCR-EVENT-DETAIL-001, SCR-EVENT-LIST-001, SCR-GOV-DISABLE-001, SCR-GOV-REACTIVATE-001, SCR-GOV-STATE-001, SCR-GOV-SUBSTITUTE-001; P3-D: SCR-ACCOUNT-EDIT-001, SCR-ACCOUNT-PASSWORD-001, SCR-AUTH-LOGIN-001, SCR-CAM-CREATE-001, SCR-CAM-EDIT-001
FILES_CHANGED = static/css/ui-v2/base.css; static/css/ui-v2/tokens.css; static/css/ui-v2/components.css; static/css/ui-v2/patterns.css; docs/prototype/ui-v2/screens/index.html; docs/prototype/ui-v2/screens/harness.js; este DCR
VERSION_BEFORE = 2.0.0
VERSION_AFTER = 2.0.1
BREAKING_CHANGE = NO
VISUAL_REDESIGN = NO
USER_REAPPROVAL_REQUIRED = NO / patch semântico; regressão direcionada obrigatória
REGRESSION_REQUIRED = YES
DECISION = Aplicar a regra global no CSS base compartilhado e registrar 2.0.1 nas referências ativas do CSS/harness raiz. Não aplicar workaround local nem alterar artefatos ou branches P3-A/B/C/D nesta atividade.
VALIDATION = PASS: reprodução do bug antes do patch; casos A-E no browser (normal, flex, grid, padrão ARGOS, remoção de hidden restaura display normal); caso F sintético hidden="until-found" mantém display:grid e content-visibility:hidden; nenhum consumidor hidden="until-found" nos handoffs P3-A/B/C/D; preview HTTP P3-A: quatro composições padrão e variantes suportadas de vazio/loading/error exibidas isoladamente; fixtures longas verificadas; Product Design targeted QA = PASS_WITH_FINDINGS (revisão restrita à regressão semântica; QA responsivo/final das famílias permanece para a atividade de retomada); python manage.py check PASS com .venv do repositório; diff --check PASS.
PATCH_COMMIT = SELF / exact SHA recorded as DS_PATCH_WORK_COMMIT in PROJECT_STATE.md and the final activity report
IMPORTANT_USED = YES
IMPORTANT_JUSTIFICATION = preservar semântica HTML [hidden] contra display autoral
HISTORICAL_VERSION_REFERENCES = P2 approval/foundation, P3-0/P3-family baselines e fixtures permanecem em 2.0.0 como evidência histórica; só CSS e metadados ativos do harness ROOT foram atualizados.
ROOT_PATCH_DESIGN_QA = PASS_WITH_FINDINGS
PRODUCTION_CHANGED = NO
P3_FAMILY_FILES_CHANGED = NO
P3_D_LOCAL_HIDDEN_WORKAROUND = REQUIRES_REVIEW_AFTER_DS_2_0_1_PROPAGATION

## Escopo

A regra exclui hidden="until-found" para preservar o comportamento nativo desse estado no navegador. !important é usado somente para proteger o invariante semântico global de [hidden] contra declarações autorais display; não deve ser ampliado para estilos comuns do Design System. O commit PATCH_COMMIT contém o patch compartilhável e os metadados de versão ativa. Este DCR é documentação ROOT e não deve ser levado às branches familiares junto com o commit do patch.

A aprovação não conclui o QA das famílias. Após a publicação do patch, a atividade seguinte deve propagar exatamente PATCH_COMMIT às branches P3-A/B/C/D e, depois, reavaliar os respectivos handoffs; em P3-D revisar o workaround local existente após a propagação.
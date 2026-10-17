# ARGOS-CRED-UI-01 — handoff visual final E1

```text
STATUS = RATIFIED_AND_IMPLEMENTED_FOR_E1
VISUAL_BASELINE = V1_OPTION_A
SELECTED_INTERFACE = CARD_EDIT_CAMERA + NATIVE_DIALOG
USER_VISUAL_APPROVAL = PASS / 2026-10-17
DJANGO_VISUAL_CONFORMANCE = PASS
CONTRACT = docs/projeto/contracts/backend/camera/ARGOS-CRED-UI-01_HTTP_SSR_INTEGRATION_CONTRACT.md
EVIDENCE = evidence/django-qa-2026-10-17/visual-conformance-fix-01/README.md
E2 = NOT_STARTED
```

Este handoff registra a implementação final da slice E1, sob o contrato HTTP/SSR vigente. Os handoffs em `handoff/` e os contratos em `references/*DRAFT.md` preservam o estado histórico da prototipação e autorização inicial; não substituem este estado final.

## Composição aceita

- Card de credenciais em Editar câmera, entre Rede e Gravação.
- Gerenciamento por diálogo nativo, usando o Design System ARGOS existente.
- Formulário cadastral e operações de credenciais são formulários irmãos, com payloads e persistência independentes.
- A V1 aprovada permanece byte a byte intacta. Sidebar, topbar e controles demonstrativos do protótipo não foram incorporados.

## Gates independentes

- `CONTRACT_RATIFIED = PASS`: ratificação CARD B + adendo, restrita a esta slice.
- `SECURITY_FOUNDATION_VALIDATED = PASS`: falhas injetadas de auditoria e rollback registradas em `PROJECT_STATE.md` §132.
- `HTTP_IMPLEMENTATION_VALIDATED = PASS`: testes direcionados registrados em `PROJECT_STATE.md` §137, junto dos checks de encerramento.
- `DJANGO_VISUAL_CONFORMANCE = PASS`: página Django real, DOM e quatro viewports documentados no índice de evidências.
- `DJANGO_HUMAN_VISUAL_APPROVAL = PASS`: aceite explícito do usuário em 2026-10-17.

## Interações e limites

Com JavaScript, a edição cadastral dirty exige decisão explícita antes de ação independente de credenciais. Sem JavaScript, a interface não alega detectar dirty state; replace/revoke permanecem usáveis por SSR e exigem confirmação explícita antes de enviar. O `<dialog>` só abre por interação JavaScript. Reveal exige integração explícita da resposta protegida; o JSON não é renderizado como HTML, a resposta não é persistida e reveal sem JavaScript não é suportado pela UI.

Não há idempotência server-side. Replace repetido pode criar uma versão e evento adicionais; revoke repetido pode retornar `409`. Duplo submit e bloqueio visual não alteram essa semântica. Não foi executado teste de concorrência PostgreSQL. Não houve auditoria formal com leitor de tela. Estes são riscos/limites documentados, não gates aprovados por inferência.

## Próxima etapa

`NEXT_ROADMAP_STAGE = E2`, `NEXT_SLICE = ARGOS-IMG-07-CONFORMANCE`. O objetivo é corrigir seleção/apresentação da última imagem ativa no Quick Detail segundo o contrato IMG-07, preservando Quick Detail visualmente e sem alterar outras telas/contratos. `E2_START = NO`; a abertura dessa atividade requer decisão própria.

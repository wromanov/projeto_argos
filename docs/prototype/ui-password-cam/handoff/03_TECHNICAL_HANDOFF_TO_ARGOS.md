# ARGOS-CRED-UI-01 — Handoff da V1 visual para o agente técnico ARGOS

## 1. Decisão comunicada pelo usuário

O usuário aprovou a **V1, alternativa A (card na edição + diálogo nativo)** após avaliar a proposta HTML. O agente ARGOS é responsável por concluir os contratos técnicos, propor o menor delta de Django e executar a implementação **somente após autorização apropriada**. O consultor UI/UX continua responsável por avaliar a conformidade visual da implementação com o protótipo.

```
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E1
ACTIVE_SLICE = ARGOS-CRED-UI-01
VISUAL_REFERENCE = prototype/ARGOS_CRED_UI_01_PROTOTIPO_V1.html
SELECTED_VARIANT = A_CARD_NATIVE_DIALOG
ALTERNATIVE_B = NOT_SELECTED
HUMAN_VISUAL_APPROVAL = PASS
HTTP_SSR_CONTRACT_STATUS = DRAFT
DJANGO_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_VISUAL_APPROVAL
NEXT_GATE = TECHNICAL_CONTRACT_ADJUDICATION_AND_IMPLEMENTATION_AUTHORIZATION
```

## 2. Preflight antes de qualquer implementação

1. Confirmar repositório, branch, HEAD, alterações locais e autoridades canônicas atuais; não supor valores históricos.
2. Conferir os artefatos e hashes do pacote aprovado.
3. Ler `references/ARGOS-CRED-UI-01_HTTP_SSR_INTEGRATION_CONTRACT_DRAFT.md` e `references/ARGOS_CRED_UI_01_VISUAL_PROTOTYPING_HANDOFF_DRAFT.md` juntamente com os contratos canônicos CAM-INT-02, CAM-INT-02-R1 e BC-AUTH do projeto.
4. Conferir o template atual `cameras/templates/cameras/formulario.html`, `static/css/ui-v2/camera-form.css`, views, services, URLs, testes e classes reais de CSS computado.
5. Apresentar plano mínimo de integração; **não** copiar o documento HTML inteiro, menus nem barras do laboratório.

## 3. Lacunas técnicas que exigem fechamento (não resolvidas pelo design)

**G1 — Projeção de metadata:** o service existente devolve campos além do mínimo, descriptografa username e não verifica o estado do owner. A proposta SSR é projetar **somente um booleano/estado genérico**, após decisão e ajuste de contrato apropriado. Não colocar username, key_version, version, updated_at ou segredo no HTML inicial.

**G2 — HTTP de replace:** service `replace_camera_credential` existe, mas a rota POST `/<camera_id>/credentials/` está **PROPOSED / NOT_IMPLEMENTED**. Confirmar método, CSRF, permissão, validação, PRG, erro sanitizado e efeitos de submissão duplicada.

**G3 — HTTP de revoke:** service `revoke_camera_credential` existe; POST `/<camera_id>/credentials/revoke/` está **PROPOSED / NOT_IMPLEMENTED**. Adjudicar confirmação e retorno de conflito.

**G4 — Atomicidade de auditoria:** o rascunho identificou ausência de comprovação de rollback diante de falha de auditoria no service de replace. Validar/fechar segundo BC-AUTH antes de dar conformidade.

**G5 — Erros e UX:** mapping definitivo de status HTTP e mensagens para erros operacionais novos permanece pendente. Manter respostas seguras.

**G6 — Exibição de username/estado revogado:** por padrão **não exibir**. Não diferenciar credencial revogada de nunca configurada sem serviço e contrato aptos. Qualquer mudança exige decisão funcional, não visual.

**G7 — Dirty form e fluxo sem JavaScript:** planejar cancelamento, foco, preservação dos valores cadastrais e fallback SSR independente; não misturar submit cadastral com credential.

**G8 — Reveal:** preservar endpoint já existente `POST /<camera_id>/credentials/reveal/`, método, autorização, CSRF, senha atual por requisição, resposta no-store, sem armazenamento, auditoria sanitizada e limpeza visual; não tratar reveal como consulta de metadados.

## 4. Entrega técnica posterior ao gate

- Card “Credenciais de acesso” entre **Rede e Gravação**, em escopo de estilo exclusivo da tela de edição.
- Resumo mínimo condicionado a `view_camera_credential`; omitir painel integralmente quando sem permissão.
- Diálogo nativo para configurar/substituir, com campo username/password vazios, erro por campo, cancelamento, foco e feedback.
- Operações de revogação/reveal em fluxos separados **somente quando habilitadas e autorizadas**.
- Formulários irmãos e independentes, nenhum nested form; ações de credenciais não salvam nem alteram `CameraEdicaoForm`.
- Preservar UI V2, sidebar, topbar, Quick Detail, Dashboard V7, Camera Detail, demais telas e componentes globais.
- Preservar service/criptografia/resolver salvo aprovação técnica específica.
- Sem conexão com câmera real, segredo real, produção/VM, deploy, E2 ou refresh/probe operacional.

## 5. Conformance e QA necessários após implementação autorizada

- Django `manage.py check`; testes direcionados de permissões, views, CSRF, métodos HTTP e status; replace, revoke, reveal; no-store; vazamentos de dados; dirty form; PRG; regressão de `CameraEdicaoForm`.
- Confirmar que renderização inicial não inclui username armazenado, senha, ciphertext, versão, chaves, metadados indevidos.
- Comparar capturas do **Django real** com a V1 em 1920×1080, 1440×900, 1366×768 e 390×844, zoom 100%; inspecionar componente em diferentes estados e a presença/ausência conforme permissão.
- Teclado, tabulação, foco visível, Escape/cancelamento, retorno de foco, labels, mensagens anunciáveis, estados de erro e reduced motion.
- Não confundir prints do mock com evidência de funcionamento de endpoints Django.
- Human review da UI renderizada deve permanecer `PENDING` até novo aceite explícito.

## 6. STOP/ESCALATE

Parar ou apresentar alternativa formal se implementação exigir mudança de contrato funcional, exposição de username/segredo, alteração do shell, redesign do formulário, refatoração global do Design System, insegurança em auditoria/metadata ou falta de autorização para implementar.

## 7. Relatório mínimo do agente ARGOS na próxima etapa

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E1
SLICE = ARGOS-CRED-UI-01
VISUAL_BASELINE = V1_OPTION_A_APPROVED
PROTOTYPE_HASH_VERIFIED =
HTTP_CONTRACT_GAPS_CLOSED =
HTTP_CONTRACT_APPROVAL =
IMPLEMENTATION_AUTHORIZATION =
BRANCH =
HEAD =
WIP_PRESERVED =
FILES_CHANGED =
CARD_AND_DIALOG_IMPLEMENTED =
SECURITY_PERMISSIONS_VALIDATED =
REPLACE_REVOKE_REVEAL_STATUS =
CAMERA_FORM_PRESERVED =
SIDEBAR_TOPBAR_PRESERVED =
DESIGN_QA =
VIEWPORTS_AND_SCREENSHOTS =
DJANGO_CHECK_AND_TESTS =
OPEN_FINDINGS =
HUMAN_DJANGO_VISUAL_APPROVAL = PENDING
COMMIT = NOT_PERFORMED_UNLESS_SEPARATELY_AUTHORIZED
PUSH = NOT_PERFORMED_UNLESS_SEPARATELY_AUTHORIZED
NEXT_GATE =
```

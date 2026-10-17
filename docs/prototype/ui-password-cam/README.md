# ARGOS — Credenciais por câmera | Pacote de handoff visual V1

**Aprovação humana:** `V1 / ALTERNATIVA A — PASS`
**Composição selecionada:** card de credenciais em **Editar câmera**, após Rede, com gerenciamento por **`<dialog>` nativo**.
**Referência de design:** `prototype/ARGOS_CRED_UI_01_PROTOTIPO_V1.html` (**cópia íntegra, não modificada**).
**Alternativa B:** preservada **somente como referência histórica**, não selecionada.
**Estado atual da slice:** E1 implementada, validada e aceita visualmente pelo usuário em 2026-10-17.
**Contrato HTTP/SSR vigente:** `docs/projeto/contracts/backend/camera/ARGOS-CRED-UI-01_HTTP_SSR_INTEGRATION_CONTRACT.md` — ratificado para esta slice e implementado; subordinado aos contratos canônicos superiores.
**Handoff visual vigente:** `ARGOS_CRED_UI_01_FINAL_VISUAL_HANDOFF.md`.
**Aceite visual:** `PASS` para a implementação Django apresentada, não para deploy ou homologação em VM.
**Implementação Django:** concluída em E1; E2 não iniciada.

## Leia nesta ordem

1. `ARGOS_CRED_UI_01_FINAL_VISUAL_HANDOFF.md` — handoff vigente da implementação concluída.
2. `evidence/django-qa-2026-10-17/visual-conformance-fix-01/README.md` — evidências da aplicação Django real.
3. `handoff/01_APPROVAL_AND_VISUAL_CONTRACT.md` e `handoff/02_INTERACTION_AND_PERMISSION_MATRIX.md` — registros históricos da aprovação da composição V1 e de sua interação proposta.
4. `handoff/03_TECHNICAL_HANDOFF_TO_ARGOS.md` e `handoff/04_DESIGN_QA_AND_EVIDENCE.md` — snapshots históricos da etapa de prototipação.
5. `references/*DRAFT.md` e `handoff/05_AGENT_ARGOS_CARD.txt` — referências históricas, supersedidas para o estado atual.

## Atenção

O aceite Django posterior fechou o gate visual desta slice. Os estados independentes de contrato, segurança/HTTP, conformidade Django e aceite humano estão registrados no contrato vigente e em `PROJECT_STATE.md` §137. As autoridades canônicas continuam superiores a este pacote. O endpoint de reveal permanece protegido e não é exposto no carregamento comum.

**Não copiar** sidebar, topbar, formas demonstrativas, dados sintéticos, seletor de cenário nem CSS global do HTML para o Django. Qualquer interação de mock no protótipo não constitui integração real. As evidências Django reais ficam separadas em `evidence/django-qa-2026-10-17/`, com o checkpoint histórico e a correção final `visual-conformance-fix-01/`.

## Integridade

Hashes relativos dos arquivos disponíveis em `SHA256SUMS.txt`; o arquivo do protótipo aprovado foi incluído sem modificação de bytes. Capturas do mock ficam diretamente em `evidence/`; capturas Django reais ficam sob `evidence/django-qa-2026-10-17/`.

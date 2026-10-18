# ARGOS E3 — Handoff visual aprovado | Proposta C V2.1

**PROJECT_ID:** `projeto_argos`  
**ROADMAP_STAGE:** `E3`  
**ACTIVE_SLICE:** `ARGOS-E3-MANUAL-IMAGE-CAPTURE`  
**PACKAGE_STATUS:** `READY_FOR_ARGOS_TECHNICAL_RECONCILIATION`  
**PROTOTYPE_VISUAL_APPROVAL:** `PASS` — decisão expressa do usuário para C V2.1  
**DJANGO_STATES_C_IMPLEMENTATION:** `NOT_AUTHORIZED_BY_THIS_PACKAGE`  
**DJANGO_HUMAN_VISUAL_APPROVAL:** `PENDING`  
**E4:** `NOT_STARTED`

## Comece por aqui

1. Leia `contracts/01_APPROVED_VISUAL_CONTRACT_AND_PRECEDENCE.md` **antes dos contratos B anteriores**.
2. Abra `prototype/ARGOS_E3_CAPTURE_ELIGIBILITY_STATES_PROPOSAL_V2_1.html`. HTML autocontido; aba Referência B contém imagem base64 incorporada. **Não modificar o arquivo aprovado.**
3. Consulte `contracts/02_ELIGIBILITY_UI_STATE_MATRIX.md` para distinguir elegibilidade, permissão e estado do job.
4. Execute o CARD `ARGOS_E3_C_V2_1_AGENT_CARD.txt`, respeitando o limite da autorização.
5. Use `handoff/03_DJANGO_HANDOFF_AND_GATES.md` e `qa/04_PROTOTYPE_DESIGN_QA.md` para preparar a integração posterior.

## Precedência visual — atenção

O contrato **histórico** da Variante B V1 descrevia uma seção sem card branco. **A aprovação humana posterior da superfície branca única da implementação E3 prevalece** nesse ponto. A Proposta C V2.1 também utiliza a superfície branca; preservar a composição mais recente aprovada: um único card branco de Operações complementares, upload à esquerda e captura à direita, com divisor neutro quando ambas operações são mostradas. Não regredir à seção aberta por seguir uma nota antiga.

O protótipo B original continua referência de hierarquia, ordem, proporções e comportamento de estados disponíveis; **não é autoridade para desfazer refinamentos humanos posteriores**.

## Escopo e limites

- Somente estados visuais de elegibilidade para captura, como aditivo à E3, condicionados a informações autorizadas do backend.
- Não implementar lógica de autorização, capability, target policy ou heurísticas no JavaScript cliente.
- Não modificar Django ou contratos técnicos com base somente neste pacote; o agente deve primeiro reconciliar autoridades vigentes e obter autorização no gate aplicável.
- E4 “Ver imagens” é conceito futuro. Não criar botão sem destino, rota fictícia ou galeria E4.
- Sidebar, topbar, Quick Detail, Histórico, fluxos existentes de upload e contratos de domínio protegidos.

## Inventário

- `prototype/`: HTML V2.1 visualmente aprovado, bytes preservados.
- `contracts/`: contrato visual consolidado e matriz de estados.
- `handoff/`: sequenciamento técnico e limites de implementação.
- `qa/`: QA real do **protótipo**, não do Django.
- `baseline/`: HTML B V1 e contrato histórico; observar precedência.
- `references/`: adendo C anterior em DRAFT, arquivo histórico não promovido automaticamente.
- `evidence/`: screenshots renderizados do protótipo e imagem B incorporada; não são screenshots Django.
- `SHA256SUMS.txt`: hashes dos arquivos deste pacote.

**Este pacote não registra implementação nem aceite do Django.**

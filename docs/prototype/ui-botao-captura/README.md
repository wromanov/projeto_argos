# ARGOS — Handoff aprovado E3 / Operações de imagem

**Projeto:** `projeto_argos`  
**Slice:** `ARGOS-E3-MANUAL-IMAGE-CAPTURE`  
**Protótipo:** `ARGOS_E3_IMAGE_OPERATIONS_PROTOTYPE_V1.html`  
**Estado visual:** **APROVADO / FROZEN** (escolha explícita do usuário)  
**Alternativa:** **B — captura e ação secundária visíveis**  
**Implementação Django:** **não realizada por este pacote; aceite integrado pendente**  
**E4:** somente conceito, **não implementada/autorizada automaticamente**

## A decisão humana que este pacote registra

O usuário escolheu a alternativa B e, após discutir uma eventual inversão de posições, determinou **não fazer novas alterações** e **aprovar a composição tal como estava**. A referência congelada é o **HTML V1 original**, cujo layout desktop já coloca **upload manual na zona esquerda** e **captura direta + “Ver imagens” na direita**. O arquivo HTML foi copiado sem alterações. Ilustrações geradas na conversa não substituem essa autoridade executável.

A opção A continua no laboratório para comparação histórica; **não** faz parte da composição escolhida. Os seletores de alternativa/cenário e a ação futura E4 são recursos de laboratório e não devem ser copiados indiscriminadamente à produção E3.

## Conteúdo

- `prototype/` — HTML V1 aprovado, interativo e independente.
- `handoff/01_VISUAL_APPROVAL_AND_CONTRACT.md` — contrato visual consolidado.
- `handoff/02_E3_E4_STATES_AND_INTEGRATION.md` — estados, acessibilidade e fronteira E3/E4.
- `handoff/03_EXECUTION_HANDOFF_ARGOS.md` — roteiro de implementação pelo agente principal.
- `handoff/04_DESIGN_QA.md` — testes realizados no mock e testes ainda obrigatórios no Django.
- `evidence/` — capturas do mock em desktop e mobile e de cenários.
- `reference/` — screenshot do Django fornecido pelo usuário e contrato DRAFT original (histórico, não canônico após aprovação).
- `ARGOS_E3_AGENT_CARD.txt` — card copiável para o Codex/agente ARGOS.
- `SHA256SUMS.txt` — hashes SHA-256 relativos ao diretório do pacote.

## Próxima ação

Encaminhar **ZIP + CARD** ao agente ARGOS. Ele deve realizar preflight e confrontar os contratos técnicos canônicos antes de materializar E3. Este pacote é **autoridade visual**, não substitui contrato técnico nem autoriza E4/deploy/commit/push. A aprovação visual do protótipo não equivale à aprovação do Django integrado.

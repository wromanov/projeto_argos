# ARGOS UI V2 — Camera Detail · refinamento estrutural final

```text
ACTIVITY = P5-VR-CAM-DESIGN-01
SCREEN = SCR-CAM-DETAIL-001
ROUTE = /cameras/<id>/
VISUAL_DIRECTION = USER_APPROVED
STATUS = USER_APPROVED / FROZEN
CANONICAL = NO
PRODUCTION_IMPLEMENTATION = NO
DESIGN_SYSTEM_CHANGE = NO
```

## Composição vigente

Preserva a superfície da ficha com identidade/cabeçalho, conteúdo principal e rail operacional; Histórico em superfície independente; Operações complementares abertas. A composição não ganhou sombra, cor, decoração ou cartão novo.

Dentro da ficha, a estrutura desktop agora é:

- **Coluna principal:** Identificação e localização; Rede e gravação.
- **Rail operacional:** Situação e completude; Monitoramento técnico; Ações operacionais.
- **Faixa de Governança cadastral:** metadados em linha de largura total no rodapé da superfície, abaixo das duas colunas. Uma divisória horizontal neutra fecha o corpo de duas colunas; espaço interno separa a linha do título de Governança.

O rail e as colunas continuam com altura determinada pelo conteúdo. Governança remove o peso vertical que antes prolongava apenas a coluna esquerda e não estica o rail. No desktop largo, seus pares usam quatro colunas: Criado por, Criado em, Atualizado por, Atualizado em; na linha seguinte, Origem ocupa uma coluna e Observações as três restantes. Em até 900px passa a duas colunas; em até 680px empilha normalmente. A ordem mobile é identidade → situação → monitoramento → ações → identificação/localização → rede/gravação → governança → Histórico → upload.

O Histórico permanece na superfície própria e com quatro famílias; links, rótulos, destinos e hierarquia são preservados. O upload continua aberto fora da ficha e do Histórico. Campos e comportamento demonstrativo permanecem sem alteração.

## Contrato de dados e limites

Fixtures, campos, links e condições `missing`/`long` são representativos. O protótipo intercepta navegação e envio. Permissões, endpoints, métodos, CSRF, validação e dados do Django não mudam. A alteração está restrita a `index.html` e `proposal.css` do protótipo, além destes documentos de proposta/QA e do registro de continuidade.

## Revisão

```text
RECORD_GRID_ROWS = HEADER / TWO_COLUMNS / FULL_WIDTH_GOVERNANCE
GOVERNANCE_DIVIDER = FULL_WIDTH_NEUTRAL / 1PX_DS_BORDER
LOWER_RIGHT_DEAD_SPACE = STRUCTURALLY_ADDRESSED / CAPTURE_PENDING
OPERATIONAL_RAIL_STRETCHED = NO
GOVERNANCE_FULL_WIDTH = YES
GOVERNANCE_SUPPORTING_ROLE = YES
HISTORY_CHANGED = NO
CARD_STYLE_CHANGED = NO
SHADOW = NONE
DECORATIVE_ACCENT = NONE
FUNCTIONAL_CHANGE = NONE
USER_VISUAL_APPROVAL = YES
FINAL_EVIDENCE = NOT_CAPTURED
USER_FREEZE = YES
ACTIVITY_COMPLETE = NO / requested viewport captures not archived
```

O usuário aprovou explicitamente esta composição e o freeze foi registrado; não farei novos ajustes visuais sem novo achado factual. Capturas finais a 100% solicitadas: 1920×1080, 1440×900, 1366×768 e 390×844. Evidências de versões anteriores não validam esta posição de Governança. Elas não foram arquivadas porque a ferramenta bloqueou o acesso automatizado à URL local `file://`; não houve tentativa por outra superfície. O aceite visual é do usuário; a lacuna é somente o pacote de capturas.

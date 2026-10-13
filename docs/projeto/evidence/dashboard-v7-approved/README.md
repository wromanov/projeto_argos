# Evidências integradas do Dashboard V7 aprovado

## Proveniência

Estas capturas mostram a aplicação Django integrada, renderizada com o template
e CSS do branch `codex/hom-v1-integration`. A referência canônica do protótipo
fica em `docs/prototype/new_ui_dashboard/`; suas capturas demonstrativas são
referência visual e não são apresentadas como saída integrada.

A captura foi realizada em 12/10/2026 usando Django SSR e o settings de QA
isolado, com cinco câmeras sintéticas e uma atividade. O HEAD de entrada da
rodada era `11dcf7db0095416c125f8863ab89a2eef7fb278f`. Os dados são de QA, não
registros produtivos. O formulário de cadastro foi aberto por GET e não foi
enviado.

## Capturas

| Arquivo | Dimensões do arquivo | Conteúdo e estágio |
|---|---:|---|
| `DASHBOARD_LINKS_1440x900.jpg` | 1440×900 | Captura integrada desktop com ação “Nova Câmera” e os três links “Ver câmeras” para Produção, Estoque e Desativadas. Capturada antes de adicionar o caption “Total registrado”. |
| `DASHBOARD_LINKS_390x844.jpg` | 375×812 | Recorte da viewport mobile 390×844, capturado antes de adicionar “Total registrado”. Mostra os três links sem clipping. |
| `DASHBOARD_TOTAL_REGISTRADO.jpg` | 658×226 | Recorte final do Inventário com o caption “Total registrado” após o valor de substituições. |

As três imagens foram copiadas byte a byte da pasta de evidências local do QA;
seus hashes de origem e destino foram comparados após a cópia.

## Escopo do aceite

O usuário aprovou a composição integrada apresentada com “perfeito autorizo
stage e commit”. O aceite é da composição representada pelas capturas recentes;
não se infere aprovação independente de cada viewport da matriz original. A
atividade delimitada do Dashboard foi concluída. HOM-01 permanece
`IN_PROGRESS` para os demais gates. Não foi produzido screenshot da página
completa nem diff pixel a pixel.

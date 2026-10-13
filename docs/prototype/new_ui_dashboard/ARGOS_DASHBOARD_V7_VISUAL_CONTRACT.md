# ARGOS · Dashboard — Contrato Visual V7

**Projeto:** `projeto_argos`  
**Data do aceite:** 12/10/2026  
**Baseline visual:** `ARGOS_DASHBOARD_AJUSTADO_V7.html`  
**Aceite humano do protótipo:** `PASS`  
**Status de integração Django:** `PENDING`  
**Status da fase:** `HOM-01 IN_PROGRESS`

## 1. Natureza do aceite

O usuário aprovou explicitamente a **composição do Dashboard V7**, após ajustes iterativos V3–V7. Este aceite protege a composição visual do conteúdo do Dashboard, **não** constitui QA integrado, homologação funcional nem autorização de fechamento Git/HOM-01.

O protótipo é um HTML independente com dados demonstrativos, navegação simulada e CSS próprio apenas para fins de prototipação. Na aplicação Django, preservar componentes SSR, Design System canônico e funcionalidades vigentes.

## 2. Componentes do Dashboard (congelados para transposição)

- Cabeçalho do conteúdo: kicker “Visão operacional”, título “Dashboard”, descrição, “Abrir inventário” e “Nova câmera”.
- Monitoramento: KPI de estado não confirmado enfatizado na primeira coluna, Online/Offline/Não monitoradas como indicadores secundários; textos, números e badge centralizados como na V7; divisórias internas abertas com recuo consistente; frescor dos dados em faixa inferior independente do estado técnico.
- Inventário: total como KPI âncora à esquerda; título, valor e legenda centralizados em um único eixo; distribuição dos quatro indicadores em grade 2×2; divisórias abertas de ritmo uniforme.
- Qualidade cadastral: “Cadastros completos” à esquerda, com respiro entre label → número → CTA; “Incompletos” e o indicador de IP duplicado na coluna secundária; rótulos centrados no eixo integral das suas células, valores alinhados à direita; divisórias abertas.
- Atividade recente: dois painéis lado a lado no desktop, empilhados no mobile; títulos e conteúdo centralizados; resumo no cabeçalho sem inventar KPIs; alturas orientadas ao conteúdo.
- Estilo: identidade ARGOS Hybrid / enterprise operational, superfícies neutras, borda discreta, sem sombras ou faixas coloridas decorativas, densidade controlada.

## 3. Superfícies protegidas

- `SIDEBAR = LOCKED`: nenhum ajuste de HTML, classes, cor, largura, padding, menus, estado ativo ou responsividade.
- `TOPBAR = LOCKED`: nenhum ajuste de estrutura, estilos ou comportamento global.
- Shell, Design System compartilhado, Quick Detail, Inventário, Camera Detail e outros consumidores não fazem parte deste aceite.
- O protótipo contém sidebar e topbar apenas como contexto de composição. Não importar a implementação desses elementos do HTML para o Django; usar as versões já integradas e aprovadas.

## 4. Precedência de textos e semântica

O relatório integrado de 12/10/2026 registra aprovações posteriores ao histórico do protótipo para **“Monitoramento e completude”**, **“Desconhecido”** e **“Câmeras com IP duplicado”**. O protótipo V7 ainda mostra “Monitoramento técnico” e “IPs duplicados”.

**Regra de integração:** preservar nomenclaturas e regras funcionais mais recentes já aprovadas no Django. NÃO alterar silenciosamente o HTML V7 nem considerar títulos antigos do protótipo como autorização para regredir rótulos produtivos. Se um texto conflitar com a composição aprovada, registrar o ponto para adjudicação, em vez de renomear regras de domínio.

A métrica de IP duplicado contabiliza **câmeras afetadas por IP repetido**, não a quantidade de endereços IP únicos em duplicidade. Frescor `STALE` não é equivalente ao estado técnico `UNKNOWN`.

O texto “Câmeras exibidas N” do protótipo é calculado pela quantidade de itens visíveis da lista demonstrativa; não reinterpretar como total do inventário nem como novo KPI de domínio.

## 5. Responsividade

Comparar a implementação em 1920×1080, 1440×900, 1366×768 e 390×844, zoom 100%, com capturas reais do Django (não do protótipo). Cenários de 0 e aproximadamente 2.300 câmeras, registros longos e conteúdo vazio. Evitar overflow horizontal global. Preservar foco visível, navegação por teclado e permissões de ações.

## 6. Limites de implementação

- Django Templates SSR, CSS próprio, JavaScript vanilla e progressive enhancement.
- Design System canônico informado no handoff: 2.0.2; não promover integralmente capabilities 2.4.0.
- Manter consultas, serviços MON, eventos, permissões e semânticas existentes.
- Alterar o menor escopo possível. Não substituir código produtivo por fixtures estáticas do HTML.
- Nenhuma criação de branch, commit, merge, push ou deploy. Preservar o WIP existente.

## 7. Gate

`V7_PROTOTYPE_VISUAL_APPROVAL = PASS`  
`DJANGO_VISUAL_IMPLEMENTATION = PENDING`  
`INTEGRATED_DESIGN_QA = NOT_PERFORMED`  
`HUMAN_INTEGRATED_APPROVAL = PENDING`  
`HOM01 = IN_PROGRESS`

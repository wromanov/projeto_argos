# ARGOS · Integração do Dashboard V7 na branch HOM-01

## Tarefa

Reproduzir o **conteúdo** do protótipo V7 aprovado no Dashboard Django integrado. Não reconstruir shell/sidebar/topbar; não substituir os componentes existentes por trechos de HTML demonstrativo. Preservar dados dinâmicos, ações, permissões, links, traduções de estados e regressões já solucionadas.

### Local, branch e restrições do handoff

Repo informado: `C:\Users\walac\desenvolvimento\projeto_argos_hom_integration`  
Branch esperada: `codex/hom-v1-integration`  
HEAD de referência: `11dcf7db0095416c125f8863ab89a2eef7fb278f`, **não** assumir que contém WIP posterior.  

Antes de mudar código: conferir `AGENTS.md`, `git branch --show-current`, `git status --short`, `git diff`, autoridades e a UI real do Django. Não sobrescrever WIP.

`NEW_BRANCH/COMMIT/PUSH/MERGE/REBASE/RESET/STASH/DEPLOY = FORBIDDEN` nesta etapa.

### Sequência recomendada

1. Auditar em modo somente leitura o Dashboard integrado, os CSS carregados e a diferença visual frente ao protótipo V7. Identificar os dados e rótulos vigentes.
2. Elaborar um mapa `V7 visual area → Django template/selector → modification needed`, incluindo os elementos que **não** podem ser tocados.
3. Implementar apenas os ajustes do Dashboard, na camada proprietária da divergência, sem CSS global nem troca de componentes compartilhados.
4. Validar os quatro viewports e fixtures equivalentes no ambiente de QA segregado, com screenshots do **Django integrado**. Incluir testes técnicos direcionados, sem probes reais, scheduler ou dados de produção.
5. Reconciliar alterações e verificar que sidebar/topbar continuam idênticas no runtime. Obter aceite visual humano do Dashboard integrado.
6. Entregar relatório para o consultor anterior encerrar o ciclo final de HOM-01. Não efetuar checkpoint Git.

### Critérios essenciais

- Total de câmeras, label, número e legenda no mesmo eixo central na coluna âncora.
- “Cadastros completos” com ritmo vertical label → número → CTA; “Incompletos” centralizado no eixo da célula inteira, sem mover o número de sua posição à direita.
- Divisórias abertas, mesma linguagem e recuos entre Monitoramento/Inventário/Qualidade.
- Atividade recente compacta, conteúdo centralizado e com altura por conteúdo.
- Rótulos, contagens e proveniência seguem a baseline Django aprovada, não os mocks do HTML.
- Sidebar e topbar continuam intocadas.
- Ao alterar CSS, confirmar cascata/computed styles efetivos na rota real.

### Portas de aprovação

`PROTOTYPE_V7 = PASS`  
`INTEGRATION = PENDING`  
`INTEGRATED_QA = PENDING`  
`HUMAN_APPROVAL_DJANGO = PENDING`  
`HOM01 = IN_PROGRESS`

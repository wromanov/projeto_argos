# Roadmap ARGOS v5

**Status:** Roadmap operacional vigente
**Data de elaboração:** 11/08/2026
**Projeto:** ARGOS — Inventário, Governança e Monitoramento de Câmeras
**Objetivo:** substituir a leitura operacional do roadmap histórico por um mapa aderente ao estado real do produto e às decisões atuais de arquitetura e operação.

---

## 1. Finalidade deste roadmap

O Roadmap ARGOS v5 passa a organizar o desenvolvimento a partir do estado real do sistema, separando claramente:

- capacidades já entregues;
- frentes em consolidação;
- capacidades futuras;
- decisões substituídas;
- dependências arquiteturais;
- atividades de hardening e produção.

O [roadmap histórico](06_roadmap.md) permanece válido como registro da evolução do projeto, mas não deve mais ser utilizado como representação primária do trabalho futuro quando seus estados não refletirem o código e as decisões atuais.

Este documento não substitui ADRs, documentos de arquitetura ou especificações funcionais detalhadas. Ele indica **o que será desenvolvido, em qual macrofase e com quais dependências**.

---

## 2. Princípios de execução

O desenvolvimento do ARGOS continua seguindo os seguintes princípios:

1. preservar contratos funcionais e decisões oficiais;
2. diagnosticar antes de alterar comportamento;
3. realizar mudanças incrementais e auditáveis;
4. manter separação entre situação operacional e status técnico;
5. preservar histórico e rastreabilidade;
6. não apagar registros históricos para acomodar decisões novas;
7. validar antes de commit;
8. não realizar push automático;
9. evitar acoplamento desnecessário entre interface web e processamento operacional;
10. tratar escala, segurança e observabilidade como requisitos arquiteturais, não como ajustes finais.

---

## 3. Estado consolidado do produto

### 3.1 Capacidades já entregues ou substancialmente consolidadas

| Área | Estado |
|---|---|
| Fundação Django | ✅ Entregue |
| Inventário técnico de câmeras | ✅ Avançado / operacional |
| CRUD principal | ✅ Entregue |
| Governança operacional | ✅ Entregue |
| Desativação / reativação | ✅ Entregue |
| Substituição de câmeras | ✅ Entregue |
| Histórico de substituições | ✅ Entregue |
| Auditoria e eventos | ✅ Avançado |
| Sistema Global de Filtros | ✅ Entregue |
| Multiseleção e filtros ativos | ✅ Entregue |
| Paginação com estado de filtros | ✅ Entregue |
| Query string canônica | ✅ Entregue |
| Design system / modernização visual | 🟡 Avançado |
| Monitoramento automático de disponibilidade | ⏳ Futuro |
| Captura manual de imagens | ⏳ Futuro |
| Importação em lote | ⏳ Futuro |
| Integrações técnicas com câmeras | ⏳ Futuro |
| Segurança avançada | 🟡 Parcial |
| Observabilidade | ⏳ Futuro |
| Arquitetura de produção | ⏳ Futuro |

### 3.2 Baseline técnico de referência no momento da elaboração

```text
Branch: master
HEAD: 84f4bb9 fix(filtros): canonicalizar parametros globais
master = origin/master
Suíte global validada: 438/438 testes
```

Este baseline é uma fotografia do momento de elaboração do roadmap e deverá ser atualizado pelo processo documental quando novos commits de documentação forem publicados.

---

# 4. FASE A — Consolidação do produto existente

**Objetivo:** concluir a modernização visual, alinhar documentação e estabelecer um rebaseline funcional antes da abertura das novas capacidades operacionais.

---

## A0 — Documentação e rebaseline inicial

**Estado:** CONCLUÍDA.

### Escopo

- fechamento documental do Sistema Global de Filtros;
- registro de decisões arquiteturais recentes;
- adoção do Roadmap ARGOS v5;
- atualização do mapa oficial de sprints;
- identificação e correção de status documentais obsoletos;
- preservação dos documentos históricos.

### Resultado esperado

Um conjunto documental coerente com o estado real do projeto.

**Codex recomendado:** 🌎 Terra Médio

---

## A1 — BR-01 — Identidade Visual ARGOS

**Estado:** PRÓXIMA — iniciar após a publicação deste checkpoint documental.

### Objetivo

Consolidar a identidade visual já existente do ARGOS sem reabrir o design system inteiro ou criar uma identidade do zero.

### Discovery concluído — BR-01A

O discovery confirmou que já existem assets institucionais, favicon, marca na sidebar e no login, e tokens suficientes no design system. Também identificou duplicação de markup/estilos entre sidebar e login e ausência de componente único de marca.

### Escopo previsto

- BR-01B — contrato e componente compartilhado de marca;
- BR-01C — integração shell/sidebar;
- BR-01D — integração login;
- BR-01E — favicon e metadados, se necessário;
- BR-01F — hardening e redução de duplicações;

### Fora do escopo

- redesenho completo de telas já modernizadas;
- alteração funcional de fluxos;
- novo logo, nova paleta, novo design system, sidebar colapsável ou novos assets sem requisito posterior.

**Codex recomendado:** 🌎 Terra Médio

---

## A2 — Visual 5 — Formulários operacionais

### Objetivo

Uniformizar UX e apresentação dos formulários operacionais e de governança sem alterar regras de negócio.

### Mapa interno

```text
V5A — Discovery dos formulários
V5B — Componentes/padrões compartilhados
V5C — Atividades
V5D — Situação / desativação / reativação
V5E — Substituição
V5F — Demais formulários
V5G — Hardening
```

### Critérios

- hierarquia visual consistente;
- validação clara;
- diferenciação de ações críticas;
- acessibilidade;
- responsividade;
- redução de duplicação;
- preservação de contratos backend.

**Codex recomendado:**

- V5A: 🌎 Terra Médio
- implementações claras: 🌙 Luna Alto
- fluxos sensíveis de governança: 🌎 Terra Alto

---

## A3 — Visual 6 — Páginas complementares

### Escopo previsto

- Eventos;
- Atividades;
- histórico de Substituições;
- Perfil;
- edição de perfil;
- alteração de senha;
- autenticação;
- Login;
- página 403;
- páginas 404/500, quando aplicável.

### Regra

Páginas já modernizadas em frentes anteriores devem ser auditadas e ajustadas apenas quando necessário, sem refatoração gratuita.

**Codex recomendado:** 🌎 Terra Médio

---

## A4 — Visual 7 — Consolidação final do frontend

### Objetivo

Encerrar formalmente a modernização do frontend.

### Auditoria global

- responsividade;
- acessibilidade;
- tabelas;
- filtros;
- formulários;
- estados vazios;
- paginação;
- componentes;
- CSS duplicado;
- CSS morto;
- padrões antigos remanescentes;
- coerência visual entre módulos.

### Marco de saída

> Frontend moderno do ARGOS formalmente consolidado.

**Codex recomendado:** 🌎 Terra Alto

---

## A5 — RF-01 — Rebaseline funcional

### Objetivo

Auditar o produto existente contra os roadmaps históricos e classificar cada capacidade como:

```text
ENTREGUE
PARCIAL
NÃO IMPLEMENTADO
SUBSTITUÍDO
NÃO É MAIS REQUISITO
```

### Resultado

Produzir uma fotografia funcional confiável antes da abertura da Fase B.

**Codex recomendado:** 🌎 Terra Médio

---

# 5. FASE B — Monitoramento operacional

## Objetivo

Monitorar continuamente a disponibilidade técnica de aproximadamente **2.300 câmeras**, mantendo o estado conhecido pelo ARGOS sem acoplar o monitoramento às requisições HTTP do Django ou ao navegador.

### Informação operacional desejada

- estado técnico atual;
- ONLINE;
- OFFLINE;
- última vez ONLINE;
- última vez OFFLINE;
- momento da última mudança;
- histórico de indisponibilidades/transições quando aplicável.

### Princípio arquitetural

```text
                    ARGOS WEB
                       |
                 consulta estado
                       |
                       v
                 ESTADO ARGOS
                       ^
                       |
                grava transições
                       |
              WORKER MONITORAMENTO
                       |
                 parque de câmeras
```

A interface consulta o estado persistido/conhecido pelo ARGOS. Ela não monitora diretamente os equipamentos.

---

## MON-01 — Contrato de disponibilidade

**Estado:** concluída e aprovada.

O contrato foi formalizado no
`docs/projeto/ADR-020_contrato_estado_tecnico_monitoramento.md`, incluindo
estados técnicos, elegibilidade, freshness, ownership, histórico e relação
com captura. A implementação permanece fora do escopo.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-02 — Segurança e capacidade de equipamento

**Estado:** concluída e aprovada.

O contrato foi formalizado no
`docs/projeto/ADR-021_seguranca_capacidade_monitoramento.md`, cobrindo
custódia de credenciais, allowlist de rede, catálogo de capacidades,
protocolos/portas, política de logs, autorização do worker e elegibilidade
concreta. A MON-02 não implementa worker,
probe, model, migration ou infraestrutura.

Não fixar antecipadamente Celery, Redis, ICMP, TCP, RTSP ou outra tecnologia
sem evidência de laboratório.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-03 — Abstração de probe e laboratório sintético

Definir a abstração técnica mínima para probes e validar o contrato em
laboratório sintético, sem implementar ainda o processo completo de
worker/scheduler.

O escopo desta frente compreende:

- `ProbeAdapter`;
- `ProbeResult`;
- resultados técnicos normalizados;
- `FakeProbe`;
- relógio e timeout controláveis;
- testes sintéticos;
- nenhuma câmera real.

Não antecipar nesta frente:

- scheduler completo;
- serviço de monitoramento;
- concorrência de produção;
- leases;
- supervisão;
- deployment.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-04 — Concorrência e scheduler

Distribuir verificações do parque ao longo do ciclo com concorrência limitada e configurável.

Evitar:

- loop sequencial bloqueante para 2.300 ativos;
- 2.300 conexões simultâneas sem controle.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-05 — Anti-flapping

Implementar mecanismo de confirmação/debounce/histerese para impedir alterações excessivas de estado provocadas por falhas transitórias.

Valores exatos de falhas e sucessos consecutivos devem ser homologados posteriormente.

**Codex recomendado:** 🌎 Terra Médio

---

## MON-06 — Histórico de indisponibilidade

Persistir eventos operacionalmente relevantes, principalmente:

```text
ONLINE -> OFFLINE
OFFLINE -> ONLINE
```

Não gerar histórico persistente para cada probe normal.

**Codex recomendado:** 🌙 Luna Alto

---

## MON-07 — Integração eficiente com UI

A interface deve consumir dados agregados e/ou somente os registros em exibição.

Estratégias permitidas para avaliação:

- polling leve;
- atualização agregada;
- atualização dos itens visíveis;
- mecanismo orientado a eventos.

WebSocket/SSE não são obrigatórios na primeira implementação.

**Codex recomendado:** 🌎 Terra Médio

---

## MON-08 — Escala e carga

Homologar com carga representativa de aproximadamente 2.300 ativos.

Avaliar:

- duração do ciclo;
- conexões;
- CPU;
- memória;
- banco;
- volume de transições;
- falhas em massa;
- recuperação.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-09 — Hardening operacional

Cobrir:

- reinício de worker;
- worker duplicado;
- banco indisponível;
- timeouts;
- falhas de rede;
- recovery;
- observabilidade;
- configuração.

**Codex recomendado:** 🌎 Terra Alto

---

# 6. FASE C — Captura manual e gestão de imagens

## Objetivo

Permitir que o operador obtenha ou associe uma imagem a uma câmera somente quando necessário.

### Decisão operacional vigente

Não haverá captura automática baseada em eventos ONLINE/OFFLINE.

A operação será:

```text
                 CÂMERA
                   |
          +--------+--------+
          |                 |
 [Capturar imagem]   [Importar imagem]
          |                 |
          +--------+--------+
                   |
                   v
                 ARGOS
```

---

## IMG-01 — Contrato funcional de imagem

Definir:

- relação imagem/câmera;
- origem;
- autoria;
- data/hora;
- permissões;
- retenção;
- ciclo de vida.

**Codex recomendado:** 🌎 Terra Médio

---

## IMG-02 — Modelo, storage e proveniência

A solução deverá distinguir conceitualmente:

```text
CAPTURA_CAMERA
UPLOAD_MANUAL
```

Uma imagem enviada manualmente não poderá ser representada como captura confirmada diretamente do equipamento.

**Codex recomendado:** 🌎 Terra Médio

---

## IMG-03 — Upload manual

Implementar ação de importação com validação backend real do arquivo.

**Codex recomendado:** 🌙 Luna Alto

---

## IMG-04 — Captura sob demanda

Implementar ação explícita:

> Capturar imagem

A captura poderá utilizar, conforme capacidades do equipamento:

- snapshot HTTP/HTTPS;
- frame pontual RTSP.

**Codex recomendado:** 🌎 Terra Alto

---

## IMG-05 — Processamento independente

Captura de imagem não deverá bloquear o monitoramento.

```text
MONITORAMENTO             CAPTURA
worker(s) de probe        worker(s) de captura
```

**Codex recomendado:** 🌎 Terra Alto

---

## IMG-06 — Histórico visual

Permitir múltiplas imagens por câmera conforme contrato definido na fase.

**Codex recomendado:** 🌙 Luna Alto

---

## IMG-07 — Imagem principal

Definir e implementar a semântica de imagem principal sem herdar automaticamente a antiga política de três snapshots.

**Codex recomendado:** 🌙 Luna Alto

---

## IMG-08 — Segurança e auditoria

Cobrir:

- autoria;
- proveniência;
- permissões;
- validação;
- integridade;
- eventual hash de arquivo.

**Codex recomendado:** 🌎 Terra Médio

---

## IMG-09 — Hardening

Validar falhas de captura, uploads inválidos, storage, concorrência e experiência de erro.

**Codex recomendado:** 🌎 Terra Médio

---

# 7. FASE D — Operação em escala e importação

## Objetivo

Permitir entrada controlada de grandes quantidades de ativos.

### Fluxo desejado

```text
arquivo
   |
   v
validar
   |
   v
preview
   |
   v
confirmar
   |
   v
importar
   |
   v
relatório
   |
   v
auditoria
```

---

## Mapa

```text
IMP-01 — Contrato de importação
IMP-02 — Template oficial
IMP-03 — Parser/validação
IMP-04 — Preview
IMP-05 — Importação
IMP-06 — Relatório de erros
IMP-07 — Auditoria
IMP-08 — Performance/hardening
```

### Princípios

- nenhuma importação cega direto para o banco;
- regras claras de duplicidade;
- normalização de dados;
- validação antes da persistência;
- rastreabilidade;
- relatório de erros.

**Codex recomendado:**

- contrato: 🌎 Terra Médio
- implementação: 🌙 Luna Alto
- hardening: 🌎 Terra Médio

---

# 8. FASE E — Segurança e governança avançada

## Objetivo

Transformar a segurança existente em uma arquitetura de produção adequada a credenciais, arquivos, workers e integrações.

```text
SEC-01 — Security assessment
SEC-02 — Credenciais de equipamentos
SEC-03 — Criptografia e custódia
SEC-04 — Revelação controlada
SEC-05 — Revisão de permissões
SEC-06 — Sessões e autenticação
SEC-07 — Dados sensíveis e logs
SEC-08 — Segurança de uploads
SEC-09 — Hardening web
SEC-10 — Auditoria final
```

### Atenção especial

Futuras credenciais de câmeras não deverão ser tratadas como dados cadastrais comuns.

**Codex recomendado:** 🌎 Terra Alto

Problemas excepcionalmente ambíguos ou críticos poderão ser escalados para ☀️ Sol Alto/Extra Alto quando Terra não for suficiente.

---

# 9. FASE F — Integração técnica com equipamentos

## Objetivo

Consolidar as integrações técnicas necessárias para diagnóstico e captura, sem confundi-las com o estado simples de disponibilidade.

```text
CAM-INT-01 — Catálogo de capacidades
CAM-INT-02 — Credenciais
CAM-INT-03 — RTSP
CAM-INT-04 — HTTP Snapshot
CAM-INT-05 — Diagnóstico técnico
CAM-INT-06 — Fabricantes/modelos
CAM-INT-07 — Hardening
```

### Princípio

```text
Disponibilidade != RTSP != captura de imagem
```

Uma câmera responder ao probe não comprova funcionamento do stream.

Uma falha de captura também não determina, isoladamente, que a câmera esteja OFFLINE.

**Codex recomendado:** 🌎 Terra Alto

---

# 10. FASE G — Observabilidade e operação

## Objetivo

Permitir operar e diagnosticar o ARGOS de forma previsível.

```text
OBS-01 — Logging estruturado
OBS-02 — Métricas
OBS-03 — Health checks
OBS-04 — Supervisão de workers
OBS-05 — Alertas
OBS-06 — Banco e storage
OBS-07 — Dashboard operacional
```

### Perguntas que o sistema deverá permitir responder

- Quantos workers estão ativos?
- Quanto tempo dura um ciclo de monitoramento?
- Quantos probes estão falhando?
- Existe backlog de trabalho?
- O banco está saudável?
- O storage está próximo do limite?
- A taxa de falhas aumentou?
- Há degradação do serviço?

**Codex recomendado:** 🌎 Terra Alto

---

# 11. FASE H — Produção e Go-Live

## Objetivo

Homologar e colocar o ARGOS em operação produtiva com continuidade, segurança e capacidade conhecidas.

```text
PRD-01 — Arquitetura de produção
PRD-02 — Configuração por ambiente
PRD-03 — Banco
PRD-04 — Storage
PRD-05 — Backup
PRD-06 — RPO/RTO
PRD-07 — Restore / Disaster Recovery
PRD-08 — Segurança de produção
PRD-09 — Performance
PRD-10 — Testes de carga
PRD-11 — Homologação
PRD-12 — Checklist de Go-Live
PRD-13 — Go-Live
```

**Codex recomendado:** 🌎 Terra Alto / Extra Alto

Decisões arquiteturais excepcionalmente críticas poderão usar ☀️ Sol Alto quando houver justificativa.

---

# 12. Dependências macro

```text
                         ARGOS v5
                            |
                            v
               +-------------------------+
               | A — CONSOLIDAÇÃO ATUAL |
               | docs + visual + baseline|
               +------------+------------+
                            |
                            v
               +-------------------------+
               | B — MONITORAMENTO      |
               | ~2.300 ativos          |
               +------------+------------+
                            |
             +--------------+---------------+
             |                              |
             v                              v
 +-----------------------+       +----------------------+
 | C — IMAGENS MANUAIS   |       | F — INTEGRAÇÕES     |
 | captura / upload      |       | RTSP/HTTP/credencial|
 +-----------+-----------+       +----------+-----------+
             |                              |
             +--------------+---------------+
                            |
                            v
                +----------------------+
                | D — IMPORTAÇÃO      |
                | operação em escala  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | E — SEGURANÇA       |
                | hardening completo  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | G — OBSERVABILIDADE |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | H — PRODUÇÃO        |
                | homologação/go-live |
                +----------------------+
```

As fases representam dependências predominantes e não um modelo waterfall rígido. Subfrentes poderão se sobrepor quando a arquitetura permitir e quando a governança do projeto considerar seguro.

---

# 13. Sequência operacional de curto prazo

```text
1. A0 — Documentação e rebaseline inicial
2. A1 / BR-01 — Consolidação da identidade existente
3. A2 — Visual 5 — Formulários operacionais
4. A3 — Visual 6 — Páginas complementares
5. A4 — Visual 7 — Consolidação frontend
6. A5 — RF-01 — Rebaseline funcional
7. MON-00 — Discovery do monitoramento (concluída)
8. MON-01 — Contrato de disponibilidade (concluída)
9. MON-02 — Segurança e capacidade de equipamento (concluída)
10. MON-03 — Abstração de probe e laboratório sintético (próxima)
```

Após `MON-01`, o foco principal do projeto passa de modernização visual para backend operacional, concorrência, integrações, segurança, observabilidade e escala.

---

# 14. Requisitos substituídos ou retirados do roadmap futuro

Não devem ser apresentados como trabalho futuro:

### Já entregues

- CRUD básico de câmeras;
- governança operacional básica;
- desativação/reativação;
- substituição;
- histórico básico;
- eventos de auditoria básicos;
- sistema global de filtros;
- multiseleção;
- filtros ativos/chips;
- paginação preservando filtros;
- query string canônica.

### Substituídos por nova decisão operacional

- captura automática em `OFFLINE -> ONLINE`;
- captura automática na primeira detecção;
- snapshots automáticos vinculados ao monitoramento;
- rotação automática das três últimas imagens derivadas desses eventos.

Os requisitos substituídos devem permanecer preservados nos registros históricos e ADRs anteriores quando existirem, mas não representam a direção futura do produto.

---

# 15. Régua de inteligência para Codex

A escolha de inteligência deverá ser realizada por tarefa, de forma conservadora.

| Tipo de atividade | Escolha inicial |
|---|---|
| Alteração trivial | 🌙 Luna Leve |
| Alteração simples | 🌙 Luna Médio |
| Implementação clara, mas trabalhosa | 🌙 Luna Alto |
| Tarefa clara e longa/complexa | 🌙 Luna Extra Alto |
| Problema que exige mais inteligência/julgamento | 🌎 Terra Médio |
| Debug difícil | 🌎 Terra Alto |
| Arquitetura/refatoração difícil | 🌎 Terra Alto / Extra Alto |
| Problema ambíguo e muito difícil | ☀️ Sol Médio / Alto |
| Problema crítico que Terra não resolveu | ☀️ Sol Extra Alto |

### Regra

Não usar níveis mais altos apenas pelo tamanho da tarefa.

Aumentar inteligência quando houver:

- ambiguidade;
- risco arquitetural;
- dificuldade de diagnóstico;
- decisões de segurança;
- concorrência;
- persistência complexa;
- impacto transversal;
- falha anterior em uma abordagem mais simples.

---

# 16. Critérios para considerar uma frente concluída

Uma frente somente deve ser marcada como concluída quando, conforme aplicável:

- contrato funcional estiver definido;
- implementação estiver concluída;
- testes direcionados estiverem aprovados;
- suíte global estiver aprovada;
- `python manage.py check` estiver aprovado;
- migrations estiverem deliberadas e validadas;
- `git diff --check` estiver aprovado;
- documentação relevante estiver atualizada;
- não houver findings BLOCKER ou MAJOR;
- validação visual/funcional tiver sido realizada quando necessária;
- commit de fechamento estiver criado;
- publicação tiver sido confirmada quando autorizada.

---

# 17. Governança de alterações do roadmap

Mudanças relevantes de direção devem seguir:

```text
necessidade operacional
        |
        v
discussão / discovery
        |
        v
ADR quando necessário
        |
        v
ajuste do roadmap
        |
        v
implementação
```

O roadmap não deve ser usado para registrar todos os detalhes de implementação.

Decisões permanentes de arquitetura ou operação devem ser registradas em ADRs.

---

# 18. Visão de chegada

O objetivo final do ARGOS v5 é evoluir o sistema atual de inventário e governança para uma plataforma operacional capaz de:

- administrar aproximadamente 2.300 câmeras;
- conhecer sua disponibilidade técnica;
- manter histórico confiável de indisponibilidade;
- permitir captura visual sob demanda;
- preservar proveniência e auditoria das imagens;
- importar ativos em escala;
- integrar-se tecnicamente com os equipamentos;
- proteger credenciais e dados sensíveis;
- operar com observabilidade;
- suportar carga validada;
- possuir backup, RPO/RTO e recuperação;
- chegar ao Go-Live com arquitetura e riscos conhecidos.

---

## 19. Status atual do roadmap

```text
FASE A — Consolidação do produto existente     🔄 EM CURSO
FASE B — Monitoramento operacional             🔄 EM CURSO (MON-01 concluída; MON-02 concluída e aprovada; MON-03 próxima)
FASE C — Captura manual e imagens              ⏳ PLANEJADA
FASE D — Importação em escala                  ⏳ PLANEJADA
FASE E — Segurança avançada                    ⏳ PLANEJADA
FASE F — Integração técnica                    ⏳ PLANEJADA
FASE G — Observabilidade                       ⏳ PLANEJADA
FASE H — Produção e Go-Live                    ⏳ PLANEJADA
```

---

**Documento:** Roadmap ARGOS v5
**Estado:** adotado como roadmap operacional vigente do Projeto ARGOS.

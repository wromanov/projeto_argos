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

### 3.2 Requisito aprovado — exportação configurável do inventário

Requisito aprovado e deliberadamente `DEFERRED / FINAL SPRINT`.

```text
STATUS = APPROVED / DEFERRED
IMPLEMENTATION = NOT_STARTED
TARGET = FINAL SPRINT / FINALIZATION
SPRINT_NUMBER = TO_BE_DEFINED
```

A futura funcionalidade deverá permitir exportar o inventário em CSV e PDF,
com seleção explícita e ordenada dos campos, preservando os filtros aplicados
na listagem. Uma eventual opção de exportar todo o inventário permitido ao
usuário deverá ser avaliada posteriormente.

A exportação deverá reutilizar o mesmo boundary de autorização do inventário e
nunca ampliar a visibilidade do usuário. O registro exportável é somente o
registro que o usuário pode visualizar. A implementação deverá usar whitelist
explícita de campos exportáveis: campo existente no model não implica campo
exportável. Campos internos, sensíveis, credenciais e secrets deverão permanecer
excluídos salvo autorização explícita do contrato de exportação.

Para CSV, a discovery deverá definir encoding e cabeçalhos compreensíveis,
compatibilidade tabular e proteção contra CSV/Formula Injection. Para PDF, a
solução deverá ser orientada a relatório, contemplando quando aplicável título,
data/hora, quantidade, filtros, campos selecionados, tabela e paginação. A
geração deverá preferencialmente ocorrer sob demanda, sem persistência
permanente desnecessária; biblioteca e estratégia definitiva ficam para a
discovery.

Antes da implementação, a sprint correspondente deverá fazer discovery dos
models, campos permitidos e proibidos, permissões, filtros, volume, estratégias
CSV/PDF, comportamento para grandes volumes, testes de segurança/autorização e
UX. Nenhuma numeração de sprint é criada nesta etapa. MON-07 permanece a
próxima frente oficial.

### 3.3 Baseline técnico de referência no momento da elaboração

```text
Branch: master
HEAD técnico de referência: 9cf1964 test(monitoramento): validar laboratorio de confirmacao
master = origin/master
Suíte canônica após MON-04C: 569/569 testes PASS local
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

**Estado:** EM CURSO — MON-05 concluída em desenvolvimento local controlado. Security Gate local RELEASED_WITH_CONTROLS; homologação, deployment e produção BLOCKED.

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

**Estado:** concluída e aprovada.

A frente implementou e validou, em `cameras/monitoramento/`, o contrato puro
de probe e seu laboratório sintético: `ProbeRequest`, `ProbeResult`,
`ProbeResultCode`, `ProbeAdapter`, `Clock`, `SystemClock`, `FakeClock` e
`FakeProbe`. Também foram entregues timeout sintético determinístico, matriz
completa de resultados, sequências FIFO e testes sem ORM, rede ou câmera real.
O contrato permanece independente do Django ORM.

`ProbeResult` continua sendo somente evidência de uma tentativa. Um resultado
isolado não é estado técnico e não produz, por si só, `ONLINE`, `OFFLINE`,
`UNKNOWN`, incidente ou transição de domínio.

Como evidência discreta da implementação e validação, permanecem os commits
`0dd7b2e` (`feat(monitoramento): criar contrato puro de probes`) e `3863d7b`
(`test(monitoramento): validar laboratorio sintetico de probes`). A validação
de encerramento registrou 21 testes focados na MON-03B, 44 testes MON-03 após
a MON-03C, 526 testes na suíte completa, zero findings do Bandit no package de
monitoramento e nenhuma migration.

Permaneceram fora desta frente: câmera real; protocolos TCP, HTTP, RTSP,
ONVIF; worker; scheduler; concorrência de produção; leases; supervisão;
deployment; persistência de monitoramento; máquina de estado; anti-flapping;
incidentes; credenciais; e preflight/allowlist real.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-04 — Confirmação de estado e anti-flapping

**Estado:** CONCLUÍDA / APROVADA.

MON-04A — Discovery: CONCLUÍDA / APROVADA / LOCAL-ONLY.

MON-04B — reducer puro de confirmação: CONCLUÍDA / APROVADA / PUBLICADA.
Evidência: `26a8925` (`feat(monitoramento): implementar confirmacao e anti-flapping`).

MON-04C — laboratório de sequências: CONCLUÍDA / APROVADA / PUBLICADA.
Evidência: `9cf1964` (`test(monitoramento): validar laboratorio de confirmacao`).

MON-04D — fechamento documental: CONCLUÍDA.

A cadeia arquitetural validada é:

```text
ProbeAdapter
    ↓
ProbeResult
    ↓
 confirmation / anti-flapping reducer
    ↓
 TechnicalDecision
    ↓
persistência futura
```

MON-04 termina em `TechnicalDecision`. Persistência de estado técnico ainda
não foi implementada por esta frente; o reducer não é um serviço de
monitoramento completo.

Os estados técnicos estáveis reconhecidos são `UNKNOWN`, `ONLINE` e `OFFLINE`.
`SUSPECT` é condição interna e efêmera, derivada de streak pendente, e não é
um quarto estado persistente. Freshness/stale permanece conceito separado;
`STALE` não é quarto estado técnico e freshness concreta não foi implementada
nesta frente.

A classificação de `ProbeResult` é:

- evidência positiva: `SUCCESS`;
- evidências negativas: `TIMEOUT`, `CONNECTION_REFUSED`;
- barreiras neutras: `AUTH_FAILURE`, `TLS_ERROR`, `PROTOCOL_ERROR`,
  `CONFIG_ERROR`, `TARGET_BLOCKED`, `INCONCLUSIVE`;
- `CANCELLED`: barreira conservadora, sem transição, preserva o estado estável,
  zera streak/pendência e não fabrica `ONLINE` ou `OFFLINE`.

O reducer é puro, determinístico, imutável e O(1) por resultado, sem ORM,
rede, worker, scheduler ou persistência. Os thresholds obrigatórios e
configuráveis são `failures_to_offline >= 2` e `successes_to_online >= 1`.
Eles não são valores operacionais finais homologados: a política exata ainda
deve ser homologada antes da integração em produção. O laboratório validou
thresholds variados, inclusive políticas assimétricas.

A ordenação temporal preserva a regra `observed_at > last_observed_at` para
aceitação, `observed_at < last_observed_at` para `OUT_OF_ORDER` e igualdade
para `AMBIGUOUS_ORDER`. Resultados rejeitados não alteram estado, streak,
watermark ou memória, nem executam reset de `policy_version`. Igualdade
temporal não é `DUPLICATE`; deduplicação real depende de identidade futura de
execução e permanece fora da MON-04.

`ConfirmationPolicy` possui `version` e `ConfirmationMemory` registra
`policy_version`. Em resultado aceito após mudança de versão, o estado
estável é preservado, o watermark anterior permanece como base, streaks
pendentes são zerados, a nova versão passa a ser usada e o resultado corrente
é processado normalmente. `policy_version` não é mecanismo de persistência ou
deployment.

Evidências locais documentadas, sem afirmação de CI remoto, homologação em
produção ou teste com câmera real:

- MON-04B: 15 testes focados; MON-03 + MON-04B: 59 testes PASS; suíte global:
  541/541 PASS; `manage.py check`, `makemigrations --check --dry-run`,
  Bandit (0 findings) e diff checks: PASS;
- MON-04C: laboratório adicional com 28 testes; MON-04B + MON-04C: 43/43
  PASS; MON-03 + MON-04: 87/87 PASS; suíte global local: 569/569 PASS;
  `manage.py check`, `makemigrations --check --dry-run`, Bandit (0 findings)
  e diff checks: PASS.

Permaneceram fora do escopo: câmera ou protocolo reais; execução de
`ProbeAdapter` de produção; worker; scheduler; concorrência de produção;
leases; supervisão; deployment; persistência técnica; atualização de `Camera`
via ORM; incidentes; abertura/fechamento de indisponibilidade;
freshness/stale concreto; scope/eligibility operacional; credenciais reais;
secret backend; preflight real; allowlist/SSRF enforcement real;
deduplicação por attempt/execution identity; captura de imagens e snapshots;
MON-05.

MON-04D não altera os contratos do ADR-020 ou ADR-021. Permanecem válidos
UNKNOWN/ONLINE/OFFLINE, SUSPECT efêmero, stale separado, as salvaguardas de
falha de worker e os requisitos de segurança de monitoramento.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-05 — Concorrência e scheduler

**Estado:** COMPLETE / PASS / PUBLISHED. Fechamento MON-05 concluído na
baseline `fbc0164`, restrito a desenvolvimento local controlado, single-instance
e SQLite. O encerramento não libera homologação, deployment ou produção.

MON-05A, MON-05B e MON-05C estão COMPLETE / PASS / PUBLISHED. A entrega
consolidou scheduler due-based contínuo, ordenação oldest-due-first,
concorrência e fila bounded, identidade/deduplicação de attempts, proteção
contra attempts antigos, revalidação de eligibility, `config_generation`,
lifecycle com draining, graceful shutdown e restart bounded, integração com
MON-04, persistência local do estado técnico e da `ConfirmationMemory`,
freshness derivada, last usable evidence, `next_due`, transições estáveis,
atomicidade/rollback, CAS monotônico e CHECKs SQLite.

Os contratos preservados são `UNKNOWN`, `ONLINE` e `OFFLINE` como estados
estáveis; `SUSPECT` efêmero; `STALE` separado, sem conversão para `OFFLINE`,
transição ou incidente automático. O estado de monitoramento permanece
separado de `Camera.status` legado e `EventoAuditoria` permanece separado da
telemetria de probe.

Permanecem fora da MON-05: `ProbeAdapter` real, rede/câmeras/credenciais
reais, worker e management command operacionais, supervisão, deployment,
PostgreSQL, multi-worker, lease distribuído, heartbeat persistente, incident
engine completo e UI operacional.

Envelope local experimental: concurrency 20, queue bound 40, intervalo alvo
300 s, probe timeout 5 s, connect timeout 3 s, jitter 10%, `stale_after` 900 s
e shutdown timeout 30 s. Isso não constitui homologação de produção.

Hardenings deferred e não bloqueantes: `HARDENING_TRANSITION_REAL` e
`HARDENING_SCOPE_BATCH_NPLUS1`.

Evidência final conhecida da re-review independente MON-05C: 641 testes globais
PASS, zero BLOCKER/MAJOR/MINOR e dois hardenings deferred. Ruff permaneceu
indisponível.

Distribuir verificações do parque ao longo do ciclo com concorrência limitada e configurável.

Evitar:

- loop sequencial bloqueante para 2.300 ativos;
- 2.300 conexões simultâneas sem controle.

**Codex recomendado:** 🌎 Terra Alto

---

## MON-06 — Histórico de indisponibilidade

**Estado:** COMPLETE / PASS / PUBLISHED.

Baseline final da sprint: `395a543`.

MON-06A, MON-06B e MON-06C estão `COMPLETE / PASS / PUBLISHED`. A entrega
consolidou o histórico materializado de indisponibilidade, a integração
transacional com `EstadoMonitoramento`, lineage por
`TransicaoEstadoMonitoramento`, idempotência, restart sem duplicação,
neutralidade de `STALE`/`SUSPECT` e isolamento de `Camera` legado e
`EventoAuditoria`.

O contrato canônico é:

- `EstadoMonitoramento`: fonte da condição técnica corrente;
- `Indisponibilidade`: fonte dos intervalos históricos;
- `TransicaoEstadoMonitoramento`: linhagem das mudanças estáveis;
- `EventoAuditoria`: não é histórico de indisponibilidade;
- `Camera.status`, `status_em` e `ultima_verificacao`: não são fonte canônica.

As regras principais são:

- `UNKNOWN -> OFFLINE` abre `INITIAL_OFFLINE`;
- `ONLINE -> OFFLINE` abre `ONLINE_TO_OFFLINE`;
- `OFFLINE -> ONLINE` fecha `RECUPERADA`;
- saída real de escopo fecha `SAIU_DO_ESCOPO`, sem criar `ONLINE` artificial;
- retorno ao escopo reinicia em `UNKNOWN`, sem reabrir o intervalo anterior;
- `STALE`, `SUSPECT`, descartes, falhas operacionais e falhas de worker são neutros.

Completion válida mantém CAS/generation, estado, memória/evidência, due,
transição e indisponibilidade no mesmo boundary transacional; probe/I-O fica
fora da transação. A duração é derivada dos timestamps e não persistida.

Evidência final conhecida: MON-06B `GLOBAL TESTS = 659 PASSED`; MON-06C
`TESTS MON-06C = 19 PASSED`, `FOCUSED = 161 PASSED`, `GLOBAL TESTS = 678
PASSED`; review MON-06C com `BLOCKER = 0`, `MAJOR = 0`, `MINOR = 0`.

O envelope permanece `LOCAL / SINGLE-INSTANCE / SQLite`. Não foram entregues
worker operacional, management command, ProbeAdapter real, rede, câmeras ou
credenciais reais, secret manager operacional, dashboard, API, notificações,
incident engine completo, Celery, Redis, PostgreSQL, multi-worker, lease
distribuído, deployment, homologação ou produção.

Os hardenings `HARDENING_TRANSITION_REAL` e
`HARDENING_SCOPE_BATCH_NPLUS1` permanecem `DEFERRED / NON-BLOCKING`.

Não houve alteração nos gates: desenvolvimento local
`RELEASED_WITH_CONTROLS`; homologação, deployment e produção `BLOCKED`.

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

**Estado:** `COMPLETE / PASS / PUBLISHED`.

O fechamento formal MON-07E confirmou a integração do inventário, detalhe,
histórico e dashboard com a `MonitoringReadService` como boundary canônica,
sem probes no ciclo HTTP ou no navegador, sem dependência do estado legado da
`Camera` e sem regressão de permissões, projeção de segurança ou N+1. A
validação final registrou MON-07B e MON-07C aprovadas, 695 testes globais
passando, `DJANGO_CHECK = PASS`, `COMPILEALL = PASS` e ausência de alterações
de migration. A entrega permanece restrita ao desenvolvimento local com
controles; homologação, deployment e produção continuam bloqueados por seus
gates próprios.

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
1. MON-04A — concluída / aprovada / local-only
2. MON-04B — concluída / aprovada / publicada
3. MON-04C — concluída / aprovada / publicada
4. MON-04D — concluída
5. SEC-R01 — concluída / VERIFIED / PUBLICADA em 3103cec
6. SEC-R02 — concluída / VERIFIED no commit técnico 227f691
7. Fechamento documental SEC-R02D — aguardando publicação conjunta
8. Security Gate — BLOCKED — REAVALIAÇÃO NECESSÁRIA
9. SEC-GATE-01 — Reavaliação do Security Gate
10. MON-05 — permanece planejada / não autorizada até decisão explícita do gate

SEC-R01 está CONCLUÍDA / VERIFIED / PUBLICADA: a implementação foi registrada
no commit `9b58885` e o fechamento documental foi publicado em `3103cec`.
SEC-R02 está CONCLUÍDA / VERIFIED no commit técnico local `227f691`, aguardando
publicação conjunta com este fechamento documental. MON-05 permanece planejada
e não autorizada; não é automaticamente liberada após o VERIFY.

## 13.1 — Continuidade de segurança e governança

**Security Gate: BLOCKED — REAVALIAÇÃO NECESSÁRIA.** SEC-007 foi confirmado
historicamente, corrigido no commit `9b58885` e está REMEDIADO / VERIFIED. A
auditoria independente registrada em `docs/security_audit/auditoria_segurança_001.md`
confirma que o exploit original não é mais reproduzível. SEC-R02 também não é
mais motivo do bloqueio; SEC-001 a SEC-006 permanecem abertos, mas ainda não
foram classificados individualmente quanto ao efeito sobre o Security Gate. O
gate permanece BLOCKED enquanto a reavaliação de governança não for concluída.
Não declarar OPEN ou RELEASED automaticamente e não classificar todos esses
findings como blockers sem essa revisão.

```text
SEC-007 — Gestão administrativa de usuários permite escalada vertical de privilégio
Categoria: VULNERABILITY | Severidade: High | Confiança: Alta
Status histórico: CONFIRMADO | Status atual: REMEDIADO / VERIFIED | Prioridade: P0
```

Foi demonstrado, em ambiente local autorizado, que usuário ativo com
`is_staff=True`, `is_superuser=False`, membro de Administrador ARGOS e suas
permissões atuais conseguiu promover contas e a própria conta a
`is_superuser=True`, alterar `is_staff`, atribuir grupo privilegiado e
permissão arbitrária no endpoint real `POST /admin/auth/user/<id>/change/`.
O Django Admin atual não possui `UserAdmin` específico que restrinja esses
campos para esse perfil. Esta é uma síntese de governança, não um relatório
de pentest.

O gate permanece BLOCKED enquanto a reavaliação de governança não for
concluída. Essa reavaliação deverá distinguir impacto em desenvolvimento local,
homologação, deployment e produção; não congela automaticamente desenvolvimento
local, testes, MON-04 ou trabalho documental, nem autoriza alteração
arquitetural automática.

### SEC-R01 — Remediação de segurança prioritária

**CONCLUÍDA / VERIFIED.** O escopo SEC-007 foi encerrado no commit `9b58885`,
com SEC-R01B, SEC-R01C e Independent VERIFY PASS. O histórico da confirmação
permanece preservado na auditoria.

MON-04D permanece como fechamento documental e não é cancelada. MON-05 continua
NÃO AUTORIZADA enquanto o Security Gate estiver BLOCKED.

### SEC-R02 — Endurecimento do PerfilUsuarioAdmin

**CONCLUÍDA / VERIFIED.** SEC-R02 cobre SEC-008, SEC-009 e SEC-010 e foi
implementada no commit técnico local `227f691`, aguardando publicação conjunta
com o fechamento documental SEC-R02D. As evidências registradas são SEC-R02B
com 5 testes PASS, SEC-R02C com 11 testes PASS, `usuarios` com 106 testes PASS,
recorte de segurança com 65 testes PASS, suíte global com 604 testes PASS,
`manage.py check` PASS, migrations sem alterações, Independent VERIFY PASS e
harness independente 5/5 PASS.

Resultado arquitetural: a implementação reutilizou a fronteira fail-closed da
SEC-R01 no `PerfilUsuarioAdmin`, cobrindo queryset, permissões por objeto,
acessos protegidos, POST direto por ID, `save_model`, `calcular_alteracoes`,
auditoria, atomicidade e comportamento legítimo do Administrador ARGOS.

### Findings preservados

Sem reclassificação e sem declaração de correção:

```text
SEC-001 — ARCHITECTURAL RISK / High / POTENCIAL / P1
SEC-002 — SECURITY DEBT / Medium / CONFIRMADO / P1
SEC-003 — VULNERABILITY / Medium / CONFIRMADO / P1
SEC-004 — VULNERABILITY / Medium / CONFIRMADO / P1
SEC-005 — VULNERABILITY / Medium / POTENCIAL / P2
SEC-006 — SECURITY DEBT / Medium / CONFIRMADO / P2
SEC-007 — VULNERABILITY / High / REMEDIADO / VERIFIED / P0
SEC-008 — SECURITY DEBT / Medium / historicamente CONFIRMADO / REMEDIADO / VERIFIED
SEC-009 — HARDENING / Medium / historicamente CONFIRMADO / REMEDIADO / VERIFIED
SEC-010 — ARCHITECTURAL RISK / Medium / historicamente POTENCIAL / MITIGADO / VERIFIED
```

SEC-007, SEC-008 e SEC-009 não mantêm mais o gate bloqueado; SEC-010 está
MITIGADO / VERIFIED. SEC-001..SEC-006 permanecem abertos, sem classificação
individual quanto ao efeito sobre o Security Gate. O gate permanece BLOCKED —
REAVALIAÇÃO NECESSÁRIA enquanto a reavaliação de governança não for concluída.

Próxima frente: **SEC-GATE-01 — Reavaliação do Security Gate**, sem antecipar
implementação. O objetivo é revisar SEC-001..SEC-006, identificar blockers reais
por ambiente, separar backlog e decidir a próxima remediação, distinguindo
desenvolvimento local, homologação, deployment e produção. SEC-R03 fica
reservado para eventual remediação concreta determinada posteriormente pela
SEC-GATE-01. MON-05 continua PLANEJADA / NÃO AUTORIZADA.

### Decisões GOV-SEC

- GOV-SEC-01 — contrato de inicialização de produção e backend de banco ainda precisa ser definido;
- GOV-SEC-02 — garantia read-only da identidade Visual QA não deve depender exclusivamente de middleware/flag;
- GOV-SEC-03 — política de brute force/throttling ainda precisa ser definida;
- GOV-SEC-04 — limites de conteúdo e atomicidade da auditoria ainda precisam de decisão.

O Projeto ARGOS passa a operar com Agente ARGOS (arquitetura, continuidade e
governança técnica), Agente de Segurança (auditoria, findings e VERIFY) e
responsável humano (decisão final). Todo SEC-XXX é entrada técnica para
governança; finding não autoriza alteração automática.

`docs/security_audit/` é área versionável de documentação interna de segurança
do repositório privado. Uma futura publicação/open source exigirá sanitização
dos relatórios e tratamento do histórico Git em processo específico.
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
FASE B — Monitoramento operacional             🔄 EM CURSO (MON-00 a MON-07 concluídas; próxima frente MON-08; Security Gate local RELEASED_WITH_CONTROLS; homologação, deployment e produção BLOCKED)
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

## Atualização vigente após o fechamento MON-07

MON-07 está `COMPLETE / PASS / PUBLISHED`, com o gate formal MON-07E
concluído. MON-06 permanece `COMPLETE / PASS / PUBLISHED`, com baseline final
`395a543`.
Esta atualização prevalece para o estado atual; seções anteriores que
registram checkpoints e sequências históricas permanecem preservadas como
histórico documental.

**Próxima frente oficial:** `MON-08 — Escala e carga`.

O fechamento de MON-07 não autoriza câmeras ou credenciais reais,
homologação, deployment, produção, multi-worker, PostgreSQL ou lease
distribuído; esses limites continuam sujeitos a gates próprios.

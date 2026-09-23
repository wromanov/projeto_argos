# Política transversal de execução direta, delegação multiagente e roteamento econômico de inteligência — v1.7-R2.1

## 0. Status e finalidade

```text
STATUS = CANONICAL
LIFECYCLE = ACTIVE
PREVIOUS_BASELINE = v1.7-R2
PREVIOUS_BASELINE_ROLE = HISTORICAL_NON_AUTHORITATIVE
CANONICALIZATION = YES
PROMOTION = YES
USER_REVIEW_REQUIRED = NO
TRANSITION_SCOPE = AGENT ARCHITECTURE, ECONOMICAL INTELLIGENCE ROUTING AND REGISTERED ROLES ONLY

SCOPE = ANY GOVERNED PROJECT / AGENT
DIRECT_EXECUTION = DEFAULT
MULTIAGENT_EXECUTION = EXCEPTION
OPTIONAL_SUBAGENT = PROHIBITED
AUTO_ESCALATION = NO
REGISTERED_PROFILE_REQUIRED = YES
UNPROFILED_SUBAGENT = PROHIBITED
PROFILE_AVAILABLE != PROFILE_NECESSARY
USER_FINAL_AUTHORITY = YES
```

Esta política define **quando executar diretamente e quando delegar a subagentes**.

O objetivo continua sendo obter a melhor relação entre qualidade, robustez, tempo,
consumo de contexto/tokens e custo de coordenação.

Esta revisão `v1.7-R2.1` é uma **consolidação incremental** sobre a `v1.7-R2`. Ela **não altera o modelo operacional
central da v1.7**, nem introduz a metodologia de execução cíclica bounded nesta
etapa. O foco desta revisão é apenas:

- refinar a **arquitetura de agentes**;
- atualizar o **catálogo normativo de papéis**;
- melhorar o **roteamento entre agentes**;
- ajustar o **posicionamento de modelos e esforço**;
- reduzir ambiguidade sobre **quem faz o quê**.
- consolidar **limiares econômicos entre tiers adjacentes**;
- registrar **cenários de conformidade de roteamento** validados sem transformar exemplos em receitas fixas.

O modo multiagente **continua não sendo padrão, ritual, sinal de qualidade nem
consequência automática da complexidade da tarefa**. Ele só deve ser usado quando
houver **ganho material, identificável e verificável** em relação à execução direta.

Regra central:

> **Escolha a rota com menor custo esperado para uma tarefa concluída corretamente,
> preservando confiabilidade e autoridade. Se delegação, especialização, independência,
> paralelismo ou roteamento para tier inferior não produzirem ganho material líquido,
> execute diretamente.**

---

## 1. Precedência e autoridade

As authorities, regras de segurança, limites de escopo, gates, convenções e
instruções específicas do projeto, repositório, diretório ou tarefa têm
precedência sobre esta política.

```text
THIS_POLICY != PROJECT_AUTHORITY_REPLACEMENT
CAPABILITY != PERMISSION
DELEGATION != AUTHORITY_TRANSFER
MULTIAGENT != EXECUTION_AUTHORIZATION
```

O uso de subagentes não concede automaticamente autorização para:

- escrever arquivos;
- alterar arquitetura ou contrato;
- avançar fase/sprint/milestone;
- executar experimento;
- operar ambiente produtivo/LIVE;
- alterar dados persistidos;
- executar comandos de alto impacto;
- realizar `git add`, commit, push ou tag;
- modificar governance;
- tomar decisão reservada ao usuário.

Quando existir política canônica de Skills/Plugins, segurança, continuidade ou
outra governança transversal, ela complementa esta política sem ser substituída
por ela.

---

## 1.1. Escopo desta transição

Esta revisão altera **arquitetura, papéis e roteamento** de subagentes, mas
deliberadamente **não** introduz nesta etapa:

- metodologia formal de `Bounded Cyclic Execution`;
- Work Units como unidade normativa obrigatória;
- ledger operacional de ciclo;
- regras novas de retry cíclico;
- mudança de fluxo para loop autônomo estruturado.

Em outras palavras:

```text
THIS_REVISION = AGENT_ARCHITECTURE_PHASE
CYCLIC_EXECUTION_METHODOLOGY = OUT_OF_SCOPE_FOR_NOW
```

A adoção futura de execução cíclica poderá ocorrer em revisão posterior, separada
e explicitamente autorizada.

---
## 2. Invariantes fundamentais

```text
DIRECT_EXECUTION = DEFAULT
MULTIAGENT_EXECUTION = EXCEPTION

OPTIONAL_SUBAGENT = PROHIBITED
AUTO_SPAWN = NO
AUTO_ESCALATION = NO

COMPLEX_TASK != MULTIAGENT_REQUIRED
LARGE_TASK != MULTIAGENT_REQUIRED
HIGH_RISK_TASK != AUTOMATIC_SUBAGENT
STRONG_MODEL != MULTIAGENT_MODE
REVIEW != INDEPENDENT_AGENT_REVIEW
SELF_REVIEW != INDEPENDENT_REVIEW

MODEL_ESCALATION != MULTIAGENT_ESCALATION
SKILL_USE != SUBAGENT_REQUIRED
PLUGIN_USE != SUBAGENT_REQUIRED

DELEGATION_REQUIRES_MATERIAL_BENEFIT
COORDINATION_COST_MUST_BE_JUSTIFIED
IF_BENEFIT_IS_UNCLEAR = DIRECT
```

---

## 3. Direct-first com roteamento econômico

`DIRECT` continua sendo o padrão quando a execução direta for simultaneamente
**suficiente, simples e economicamente racional**.

A regra `DIRECT_EXECUTION = DEFAULT` não significa:

```text
ROOT_CAN_DO_THE_WORK
→ ROOT_SHOULD_DO_ALL_THE_WORK
```

Antes de decidir `DIRECT`, o agente principal deve avaliar não apenas se consegue
concluir toda a atividade, mas se manter a inteligência atual em todas as etapas
é a forma mais eficiente de alcançar o resultado correto.

Execução direta é preferida quando:

- existe uma única linha principal de raciocínio;
- o trabalho é fortemente acoplado e não possui fronteiras de handoff úteis;
- os mesmos arquivos/contextos precisariam ser relidos integralmente por todos;
- o custo de coordenação supera qualquer economia de tier;
- o trabalho delegado continuaria exigindo o mesmo julgamento do root;
- a quantidade de trabalho mecânico delegável é pequena demais para justificar handoff;
- a principal dificuldade é raciocínio contínuo e monolítico;
- um self-review do root é suficiente;
- não existe ganho material de paralelismo, especialização, independência,
  decomposição ou roteamento econômico de inteligência.

Por outro lado, uma atividade **sequencial** pode ser multiagente quando há ganho
material ao manter inteligência cara somente nos pontos cognitivos difíceis e
delegar execução bounded/verificável para tiers mais baratos.

```text
MULTIAGENT != PARALLELISM_ONLY
SEQUENTIAL_MULTIAGENT_PIPELINE = ALLOWED
```

Princípio:

```text
EXPENSIVE_INTELLIGENCE = COGNITIVE_HOTSPOTS_ONLY
BOUNDED_VERIFIABLE_EXECUTION = LOWEST_SUFFICIENT_TIER
```

Se todos os gates multiagente, inclusive o gate econômico, forem negativos:

```text
EXECUTION_MODE = DIRECT
SUBAGENTS_ALLOWED = NO
```

Se houver dúvida real e não for possível demonstrar ganho material:

```text
EXECUTION_MODE = DIRECT
```

---

## 4. Gate obrigatório para uso de multiagente

Um subagente só pode ser criado quando existir **benefício material verificável**
ligado a pelo menos uma das condições abaixo.

### G1 — Frentes paralelas realmente independentes

```text
PARALLEL_INDEPENDENT_FRONTS = YES
```

Exige pelo menos duas frentes que:

- possam avançar simultaneamente;
- tenham escopos claros e separáveis;
- não dependam de escrita concorrente sobre o mesmo estado;
- produzam entregáveis reconciliáveis;
- tragam redução real de tempo ou custo total.

### G2 — Especialização distinta necessária

```text
DISTINCT_SPECIALIZATION_REQUIRED = YES
```

Use quando uma disciplina separada for materialmente necessária, por exemplo
segurança, pesquisa externa, arquitetura, análise estatística, infraestrutura ou
performance, e sua separação reduzir risco ou melhorar substancialmente a decisão.

Especialização apenas conveniente não basta.

### G3 — Ganho material de decomposição

```text
MATERIAL_DECOMPOSITION_GAIN = YES
```

A decomposição deve reduzir materialmente pelo menos um destes fatores:

- wall-clock time;
- consumo de contexto do root;
- risco de omissão;
- volume operacional do root;
- custo total esperado;
- ruído de logs/evidências no root;
- complexidade cognitiva mantida no agente principal.

Dividir apenas para distribuir trabalho não constitui ganho.

### G4 — Conflito identificado que exige adjudicação

```text
IDENTIFIED_CONFLICT_REQUIRES_ADJUDICATION = YES
```

Deve existir divergência concreta entre evidências, contratos, interpretações ou
resultados. Não criar adjudicador preventivamente.

### G5 — Governança exige revisão independente

```text
GOVERNANCE_REQUIRES_INDEPENDENT_REVIEW = YES
```

Use agente independente quando policy, gate, standard, contrato ou decisão do
usuário exigir independência. Segunda opinião genérica não equivale a requisito
de independência.

### G6 — Ganho material de roteamento de inteligência

```text
MATERIAL_INTELLIGENCE_ROUTING_GAIN = YES
```

Existe quando a tarefa possui um ou mais **hotspots cognitivos** que justificam
um root/modelo mais forte, mas outras etapas podem ser executadas com segurança
por um tier mais barato.

O gate é satisfeito quando, em conjunto:

```text
HIGHER_TIER_REQUIRED_FOR_SOME_JUDGMENT = YES
LOWER_TIER_CAPABLE_OF_BOUNDED_EXECUTION = YES
DELEGATED_WORK_IS_OBJECTIVELY_VERIFIABLE = YES
HANDOFF_SCOPE_IS_CLEAR = YES
EXPECTED_TIER_SAVING_EXCEEDS_HANDOFF_COST = YES
```

Exemplos típicos:

- root Terra/High fecha a decisão matemática e Luna/High aplica patch mecânico;
- root Terra/High define invariantes e Luna/High executa validações;
- root Terra/Medium coordena e Luna/High faz exploração factual extensa;
- root resolve um ponto difícil e de-escalona a execução operacional.

Este gate **não exige paralelismo**.

```text
PARALLEL_INDEPENDENT_FRONTS = NO
MATERIAL_INTELLIGENCE_ROUTING_GAIN = YES
EXECUTION_MODE = MULTIAGENT  # permitido se os demais critérios forem satisfeitos
```

---

## 5. Regra de elegibilidade multiagente

Atender a um gate é necessário, mas não suficiente.

Antes de delegar, também deve ser verdadeiro:

```text
AT_LEAST_ONE_MULTIAGENT_GATE = YES
EXPECTED_MATERIAL_GAIN = YES
SCOPE_PARTITION_IS_CLEAR = YES
COORDINATION_COST_IS_ACCEPTABLE = YES
RESULTS_CAN_BE_RECONCILED = YES
AUTHORITY_BOUNDARIES_ARE_PRESERVED = YES
ROOT_CAPABILITY_REDUNDANCY_CHECK = PASS
```

Somente então:

```text
EXECUTION_MODE = MULTIAGENT
```

Caso contrário:

```text
EXECUTION_MODE = DIRECT
SUBAGENTS_ALLOWED = NO
```

### 5.1 Regra custo-benefício

A métrica relevante é o custo esperado para uma tarefa concluída corretamente,
não o custo isolado de uma chamada.

```text
OPTIMIZATION_TARGET = EXPECTED_COST_PER_SUCCESSFUL_TASK
```

Considere:

```text
NET_MULTIAGENT_GAIN =
PARALLELISM_GAIN
+ SPECIALIZATION_GAIN
+ INDEPENDENCE_VALUE
+ ROOT_CONTEXT_REDUCTION
+ EXPENSIVE_TIER_TIME_SAVED
+ OPERATIONAL_WORK_OFFLOADED
-
COORDINATION_OVERHEAD
-
DUPLICATED_CONTEXT_COST
-
HANDOFF_COST
-
INTEGRATION_COST
-
CONSISTENCY_RISK
-
EXPECTED_RETRY_COST
```

Se o ganho líquido não for claramente positivo:

```text
EXECUTION_MODE = DIRECT
```

### 5.2 Gate de redundância do root

Antes de cada spawn, avaliar:

```text
DOES_ROOT_ALREADY_COVER_THIS_ROLE_SUFFICIENTLY?
```

Se `YES`, perguntar:

```text
IS_INDEPENDENCE_REQUIRED?
IS_DISTINCT_SPECIALIZATION_REQUIRED?
IS_ECONOMIC_OFFLOAD_MATERIAL?
```

Se todas forem `NO`:

```text
DO_NOT_SPAWN
```

Um subagente não deve duplicar uma capacidade já presente no root sem valor
adicional identificável.

### 5.3 Escolher entre escalonar o root e criar subagente

Antes de criar um agente mais inteligente, distinguir:

```text
NEED_MORE_INTELLIGENCE
vs
NEED_SEPARATE_RESPONSIBILITY
vs
NEED_INDEPENDENCE
```

Aplicar:

```text
IF NEED_MORE_INTELLIGENCE
AND NEED_SEPARATE_RESPONSIBILITY = NO
AND NEED_INDEPENDENCE = NO
→ ESCALATE_ROOT_TEMPORARILY

IF NEED_SEPARATE_RESPONSIBILITY = YES
→ DELEGATE_TO_SMALLEST_SUFFICIENT_ROLE

IF NEED_INDEPENDENCE = YES
→ USE_INDEPENDENT_AGENT
```

---

### 5.4 Múltiplas rotas válidas e critério de seleção

Uma mesma atividade pode admitir mais de uma arquitetura tecnicamente defensável.
A política não exige uma topologia única quando diferentes rotas preservam contrato,
authority, qualidade e critérios de aceite.

```text
MULTIPLE_VALID_ROUTINGS_MAY_EXIST = YES
```

Quando houver mais de uma rota válida, selecionar pela combinação de:

```text
ROUTE_SELECTION_OBJECTIVE =
EXPECTED_COST_PER_SUCCESSFUL_TASK
+ RELIABILITY
+ AUTHORITY_PRESERVATION
+ CONTEXT_EFFICIENCY
+ REVERSIBILITY
```

A comparação deve considerar pelo menos:

- tier e tempo do root;
- tier e tempo dos subagentes;
- volume operacional;
- duplicated context;
- handoff e integração;
- retries prováveis;
- verificabilidade;
- impacto de uma falha;
- necessidade real de independência.

Não escolha uma rota apenas porque ela possui mais agentes, menos agentes ou modelos
mais baratos por chamada. A unidade de otimização continua sendo a tarefa concluída
corretamente.

```text
CHEAPEST_CALL != CHEAPEST_SUCCESSFUL_ROUTE
FEWEST_AGENTS != ALWAYS_CHEAPEST_ROUTE
MOST_CAPABLE_ROUTE != ALWAYS_BEST_ROUTE
```

---

## 6. Cabeçalho obrigatório de decisão

Em atividades governadas relevantes, declare antes da execução:

```text
EXECUTION_MODE = DIRECT | MULTIAGENT

ORCHESTRATOR_MODEL =
ORCHESTRATOR_EFFORT =
ORCHESTRATOR_ROLE = ROOT

PARALLEL_INDEPENDENT_FRONTS = YES | NO
DISTINCT_SPECIALIZATION_REQUIRED = YES | NO
MATERIAL_DECOMPOSITION_GAIN = YES | NO
IDENTIFIED_CONFLICT_REQUIRES_ADJUDICATION = YES | NO
GOVERNANCE_REQUIRES_INDEPENDENT_REVIEW = YES | NO
MATERIAL_INTELLIGENCE_ROUTING_GAIN = YES | NO

EXPECTED_MATERIAL_GAIN = YES | NO
COORDINATION_COST = LOW | MEDIUM | HIGH
ROOT_CAPABILITY_REDUNDANCY_CHECK = PASS | FAIL

SUBAGENTS_ALLOWED = YES | NO
SUBAGENTS_PLANNED = <n>
```

Quando `EXECUTION_MODE = MULTIAGENT`, registrar para cada papel:

```text
SUBAGENT_ROLE =
MODEL =
EFFORT =
WHY_NOT_ROOT =
WHY_THIS_TIER =
EXPECTED_GAIN =
```

Se `EXECUTION_MODE = DIRECT`:

```text
SUBAGENTS_ALLOWED = NO
SUBAGENTS_PLANNED = 0
```

Não declarar subagente como “opcional”. A decisão deve ser justificada antes do
spawn ou reavaliada quando surgir novo gatilho material durante a execução.

---

## 7. Roteamento de inteligência e arquitetura operacional

Modelo, esforço, execução direta/delegada e papel são decisões relacionadas, mas
não equivalentes.

```text
MODEL
EFFORT
EXECUTION_MODE
ROLE
AUTHORITY
```

Aplicar:

```text
USE_MINIMUM_SUFFICIENT_INTELLIGENCE = YES
COST_MUST_NOT_OVERRIDE_RISK = YES
MODEL_ESCALATION != MULTIAGENT_ESCALATION
MODEL_ESCALATION != AUTHORITY_ESCALATION
```

Uma tarefa difícil e monolítica pode justificar um root mais forte em modo direto.
Uma tarefa com hotspot cognitivo seguido de trabalho bounded pode justificar root
forte + subagentes baratos em pipeline sequencial.

```text
HARD_SINGLE_THREAD_PROBLEM
→ STRONGER_DIRECT_REASONING

HARD_POINT_PLUS_CHEAP_BOUNDED_WORK
→ STRONG_ROOT_FOR_HARD_POINT
→ DELEGATE_CHEAP_BOUNDED_WORK
→ ROOT_RECONCILES
```

## 7.1. Escolha do orquestrador vem antes dos subagentes

Antes de selecionar subagentes, determine a inteligência necessária para o root.

O root deve ser capaz de:

- manter estado e authorities;
- identificar hotspots cognitivos;
- decompor e contratar trabalho;
- arbitrar evidência;
- revisar quando sua própria capacidade for suficiente;
- decidir escalation/de-escalation;
- emitir o veredicto final.

```text
ROOT_INTELLIGENCE_IS_PART_OF_ROUTING_DECISION = YES
```

O root **não precisa executar pessoalmente** todo trabalho que seja capaz de fazer.

## 7.2. Baseline do orquestrador

No ambiente atual do Codex:

```text
DEFAULT_ORCHESTRATOR_MODEL = GPT-5.6-TERRA
DEFAULT_ORCHESTRATOR_EFFORT = MEDIUM
```

Esse é um baseline, não um teto.

Usar `Terra / High` como root quando a atividade exigir julgamento sustentado de
maior complexidade, por exemplo matemática sensível, integração difícil, forte
ambiguidade ou decisão de alto impacto que ainda não justifique Sol.

```text
TERRA_MEDIUM = NORMAL_ROOT_BASELINE
TERRA_HIGH = HIGH_JUDGMENT_ROOT
SOL_HIGH = TEMPORARY_ARCHITECTURAL_SPECIALIST_BY_DEFAULT
```

Preserve o princípio, não o nome literal do modelo:

> O orquestrador deve ser o menor modelo que coordene e adjudique a atividade com
> confiabilidade suficiente.

## 7.3. Piso operacional dos agentes Luna

```text
LUNA_LOW = DO_NOT_USE_BY_DEFAULT
LUNA_MEDIUM = DO_NOT_USE_BY_DEFAULT
LUNA_DEFAULT = HIGH
LUNA_ANALYTICAL = XHIGH_WHEN_SUPPORTED
```

`Luna / High` é o tier econômico padrão para trabalho delimitado. `Luna / XHigh`
fica reservado para investigação/triage realmente analítico.

## 7.4. Posicionamento dos tiers

```text
ROOT NORMAL ORCHESTRATION
→ TERRA / MEDIUM

ROOT HIGH-JUDGMENT ORCHESTRATION
→ TERRA / HIGH

FACTUAL EXPLORATION
→ LUNA / HIGH

EXTERNAL RESEARCH / ANALYTICAL TRIAGE
→ LUNA / XHIGH WHEN SUPPORTED

MECHANICAL BOUNDED IMPLEMENTATION
→ LUNA / HIGH

NORMAL IMPLEMENTATION REQUIRING JUDGMENT
→ TERRA / MEDIUM

COMPLEX IMPLEMENTATION
→ TERRA / HIGH

INDEPENDENT TECHNICAL REVIEW
→ TERRA / HIGH

ARCHITECTURE / HARD ROOT CAUSE / HARD REVIEW
→ SOL / HIGH
```

## 7.5. Fatores de roteamento

A escolha deve considerar:

```text
AMBIGUITY
COGNITIVE_COMPLEXITY
IMPACT
REVERSIBILITY
VERIFIABILITY
NOVELTY
FAILURE_HISTORY
SECURITY_SENSITIVITY
CONTEXT_DEPTH
MECHANICALITY
CONTRACT_CLOSURE
OBJECTIVE_TESTABILITY
ROOT_CURRENT_CAPABILITY
```

## 7.6. Hotspots cognitivos

Antes de manter um modelo caro em toda a tarefa, identifique:

```text
WHERE_DOES_HIGHER_INTELLIGENCE_CHANGE_SUCCESS_PROBABILITY?
```

Se apenas parte da tarefa exige tier alto:

```text
IDENTIFY_HARD_POINT
→ USE_STRONG_MODEL
→ CLOSE_DECISION_AND_INVARIANTS
→ FREEZE_BOUNDED_EXECUTION_CONTRACT
→ DELEGATE_TO_LOWER_TIER
→ VALIDATE_CHEAPLY
→ RETURN_TO_ROOT_FOR_ADJUDICATION
```

## 7.7. Regra de redundância de inteligência cara

```text
DO_NOT_DUPLICATE_EXPENSIVE_INTELLIGENCE_WITHOUT_DISTINCT_VALUE = YES
```

Exemplo normalmente inadequado:

```text
TERRA/HIGH ROOT
+ TERRA/HIGH IMPLEMENTER
+ TERRA/HIGH REVIEWER
```

sobre o mesmo contexto e sem independência exigida.

Antes de spawn de `terra_reviewer` ou outro tier caro, verificar se o root já cobre
a necessidade.

## 7.8. Escalonamento e de-escalation

Escalar exige razão observável:

```text
VALID_ESCALATION_REASONS =
AMBIGUITY |
HIGH_COGNITIVE_COMPLEXITY |
HIGH_IMPACT |
FAILED_LOWER_TIER |
LOW_CONFIDENCE |
CONFLICTING_EVIDENCE |
ARCHITECTURAL_DECISION |
SECURITY_CRITICALITY |
NO_MEANINGFUL_PROGRESS
```

```text
UNGROUNDED_ESCALATION = PROHIBITED
```

Depois que o ponto difícil for resolvido:

```text
DEESCALATE_WHEN_HIGHER_TIER_NO_LONGER_NEEDED = YES
```

De-escalation pode significar:

- root continua forte, mas delega trabalho barato;
- root volta a esforço menor quando a superfície permitir;
- especialista caro devolve decisão e sai do fluxo;
- validação e execução mecânica retornam a Luna.

## 7.9. Pipeline sequencial multiagente

Multiagente não exige simultaneidade.

Pipeline recomendado quando economicamente vantajoso:

```text
STRONG ROOT
→ closes reasoning / constraints / invariants
→ CHEAP MECHANICAL IMPLEMENTER
→ CHEAP VALIDATOR
→ TRIAGE ONLY ON FAILURE
→ STRONG ROOT SELF-REVIEW / FINAL ADJUDICATION
```

Esse fluxo é válido quando o ganho econômico supera handoff e integração.

---

## 8. Registro operacional de subagentes e catálogo normativo de papéis

Perfis concretos são capacidades registradas, não participantes obrigatórios.

```text
REGISTERED_PROFILE_REQUIRED = YES
UNPROFILED_SUBAGENT = PROHIBITED
ROLE_EXISTS != ROLE_MUST_BE_USED
PROFILE_AVAILABLE != PROFILE_NECESSARY
PROFILE_RELEVANT != MULTIAGENT_JUSTIFIED
```

## 8.1. Catálogo normativo de papéis

### SCOUT

```text
ROLE = SCOUT
DEFAULT_MODEL = LUNA
DEFAULT_EFFORT = HIGH
DEFAULT_SANDBOX = READ_ONLY
```

Exploração factual: arquivos, símbolos, fluxos, dependências, configuração,
contratos e divergências. Não escreve nem decide arquitetura.

### RESEARCHER

```text
ROLE = RESEARCHER
DEFAULT_MODEL = LUNA
DEFAULT_EFFORT = XHIGH_WHEN_SUPPORTED
DEFAULT_SANDBOX = READ_ONLY
```

Documentação oficial, APIs, versões, compatibilidade, breaking changes e pesquisa
externa autorizada. Não implementa.

### VALIDATOR

```text
ROLE = VALIDATOR
DEFAULT_MODEL = LUNA
DEFAULT_EFFORT = HIGH
DEFAULT_SANDBOX = WORKSPACE_WRITE_WHEN_REQUIRED_FOR_VALIDATION
SOURCE_WRITE_AUTHORIZATION = NO
```

Responsável por:

- testes focais e suites;
- lint;
- type checking;
- build;
- collect-only;
- diff checks;
- checks objetivos;
- coleta factual de evidência.

Ferramentas de validação podem criar caches, bytecode, build outputs, coverage e
outros artefatos transitórios. Isso não autoriza alteração de código-fonte,
testes, configuração ou critérios de aceite.

```text
WRITE_CAPABILITY != SOURCE_WRITE_AUTHORIZATION
VALIDATOR != IMPLEMENTER
```

Falha deve retornar ao root ou a Triage; Validator não corrige automaticamente.

### TRIAGE_ANALYST

```text
ROLE = TRIAGE_ANALYST
DEFAULT_MODEL = LUNA
DEFAULT_EFFORT = XHIGH_WHEN_SUPPORTED
DEFAULT_SANDBOX = READ_ONLY
```

Interpreta failure signatures, formula hipótese de root cause, estima escopo e
recomenda próxima ação. Não implementa.

### MECHANICAL_IMPLEMENTER

```text
PROFILE = luna_worker
ROLE = MECHANICAL_IMPLEMENTER
DEFAULT_MODEL = LUNA
DEFAULT_EFFORT = HIGH
DEFAULT_SANDBOX = WORKSPACE_WRITE
```

Usar quando:

```text
SOLUTION_IS_CLOSED = YES
SCOPE_IS_BOUNDED = YES
OWNERSHIP_IS_CLEAR = YES
IMPLEMENTATION_IS_MECHANICAL_OR_LOW_JUDGMENT = YES
OBJECTIVE_VALIDATION_EXISTS = YES
```

Responsabilidades:

- aplicar alteração prescrita;
- editar apenas ownership recebido;
- produzir o menor patch compatível com o contrato;
- preservar invariantes e decisões fechadas;
- reportar exatamente o que mudou.

Não pode:

- escolher nova arquitetura;
- resolver trade-off material;
- alterar requisito;
- reinterpretar contrato congelado;
- refatorar oportunisticamente;
- relaxar testes;
- executar Git consequencial sem autorização.

Se surgir decisão material:

```text
STOP_AFFECTED_SCOPE
RETURN_TO_ROOT
```

### IMPLEMENTER

```text
PROFILE = terra_implementer
ROLE = IMPLEMENTER
DEFAULT_MODEL = TERRA
DEFAULT_EFFORT = MEDIUM
DEFAULT_SANDBOX = WORKSPACE_WRITE
```

Usar quando a implementação está delimitada, mas ainda exige julgamento técnico
material, decisões locais não triviais ou integração que excede trabalho mecânico.

Quando a implementação for cognitivamente complexa:

```text
IMPLEMENTER_EFFORT = HIGH
```

sem ampliar authority.

### REVIEWER

```text
ROLE = REVIEWER
DEFAULT_MODEL = TERRA
DEFAULT_EFFORT = HIGH
DEFAULT_SANDBOX = READ_ONLY
```

Reviewer existe para **independência** ou **ganho material de revisão**.

Não usar apenas porque houve implementação.

Antes de spawn:

```text
ROOT_CAN_REVIEW_SUFFICIENTLY?
INDEPENDENCE_REQUIRED?
DISTINCT_REVIEW_VALUE?
```

Se root já for suficiente e independência não for exigida:

```text
REVIEW = ROOT_SELF_REVIEW
REVIEWER_SUBAGENT = NO
```

### SECURITY_REVIEWER

```text
ROLE = SECURITY_REVIEWER
DEFAULT_MODEL = TERRA
DEFAULT_EFFORT = HIGH
DEFAULT_SANDBOX = READ_ONLY
```

Usar somente quando houver superfície material de segurança.

### ARCHITECT

```text
ROLE = ARCHITECT
DEFAULT_MODEL = SOL
DEFAULT_EFFORT = HIGH
DEFAULT_SANDBOX = READ_ONLY
ARCHITECT != PERSISTENT_ORCHESTRATOR
```

Especialista temporário para arquitetura, alto blast radius, múltiplas soluções
defensáveis, hard root-cause e hard review.

### SCRIBE

```text
ROLE = SCRIBE
DEFAULT_MODEL = LUNA
DEFAULT_EFFORT = HIGH
DEFAULT_WRITE_SCOPE = DOCUMENTATION_ONLY
```

```text
SCRIBE_DOES_NOT_CREATE_REALITY
SCRIBE_RECORDS_REALITY
```

Registra apenas fatos/evidências/decisões estabelecidas.

## 8.2. Mapeamento operacional recomendado

| Perfil | Papel | Modelo/esforço | Sandbox | Uso |
|---|---|---|---|---|
| `luna_scout` | `SCOUT` | Luna / High | read-only | exploração factual |
| `luna_researcher` | `RESEARCHER` | Luna / XHigh quando suportado | read-only | pesquisa externa |
| `luna_validator` | `VALIDATOR` | Luna / High | workspace-write contratualmente validation-only | testes/checks |
| `luna_triage` | `TRIAGE_ANALYST` | Luna / XHigh quando suportado | read-only | diagnóstico inicial |
| `luna_worker` | `MECHANICAL_IMPLEMENTER` | Luna / High | workspace-write | patch bounded e mecânico |
| `luna_scribe` | `SCRIBE` | Luna / High | workspace-write limitado a docs | documentação factual |
| `terra_implementer` | `IMPLEMENTER` | Terra / Medium | workspace-write | implementação com julgamento |
| `terra_reviewer` | `REVIEWER` | Terra / High | read-only | review independente/material |
| `terra_security` | `SECURITY_REVIEWER` | Terra / High | read-only | segurança material |
| `sol_architect` | `ARCHITECT` | Sol / High | read-only | arquitetura/hard review |

## 8.3. Compatibilidade

Perfis de compatibilidade:

```text
luna_explorer
→ DEPRECATED_COMPATIBILITY_PROFILE
→ preferir luna_scout

luna_test_analyst
→ DEPRECATED_COMPATIBILITY_PROFILE
→ preferir luna_validator ou luna_triage
```

`luna_worker` deixa de ser deprecated nesta revisão e passa a papel ativo de
`MECHANICAL_IMPLEMENTER`.

## 8.4. Gate de seleção do papel

Depois de justificar multiagente:

```text
1. QUAL GANHO MATERIAL JUSTIFICOU A DELEGAÇÃO?
2. QUAL INTELIGÊNCIA JÁ ESTÁ PRESENTE NO ROOT?
3. QUAL RESPONSABILIDADE PRECISA SER SEPARADA?
4. O TRABALHO É MECÂNICO OU EXIGE JULGAMENTO?
5. QUAL É O MENOR TIER SUFICIENTE?
6. O SANDBOX É COMPATÍVEL?
7. HÁ OVERLAP OU DUPLICAÇÃO DE INTELIGÊNCIA CARA?
8. O RETORNO É OBJETIVAMENTE RECONCILIÁVEL?
```

Mapeamento:

```text
REPOSITORY_EXPLORATION → SCOUT
EXTERNAL_RESEARCH → RESEARCHER
TEST_EXECUTION_OR_OBJECTIVE_CHECKS → VALIDATOR
FAILURE_ANALYSIS → TRIAGE_ANALYST
MECHANICAL_BOUNDED_IMPLEMENTATION → MECHANICAL_IMPLEMENTER
IMPLEMENTATION_REQUIRING_JUDGMENT → IMPLEMENTER
INDEPENDENT_TECHNICAL_REVIEW → REVIEWER
MATERIAL_SECURITY_REVIEW → SECURITY_REVIEWER
MATERIAL_ARCHITECTURAL_CONSULTATION → ARCHITECT
FACTUAL_DOCUMENTATION_UPDATE → SCRIBE
```

## 8.5. Concorrência

```text
MAX_CONCURRENT_SUBAGENTS = 2
MAX_CONCURRENT_WRITERS = 1
MINIMUM_NECESSARY_SUBAGENTS = PREFERRED
```

Multiagente sequencial pode usar mais de um papel ao longo da atividade sem que
eles estejam simultaneamente ativos.

---

## 9. Contrato mínimo de delegação

Todo subagente deve receber contrato explícito e task-bounded.

No mínimo:

```text
TASK_ID
ROLE

DELEGATED_OBJECTIVE
SCOPE_IN
SCOPE_OUT
INPUTS

ROOT_MODEL
ROOT_EFFORT
WHY_NOT_ROOT
WHY_THIS_ROLE
WHY_THIS_TIER
EXPECTED_GAIN

DECISIONS_ALREADY_CLOSED
INVARIANTS_TO_PRESERVE

ALLOWED_ACTIONS
PROHIBITED_ACTIONS

READ_WRITE_MODE
SOURCE_WRITE_AUTHORIZATION
OWNERSHIP

EXPECTED_OUTPUT
REQUIRED_EVIDENCE
VALIDATION_EXPECTED

DONE_CRITERIA
STOP_CONDITIONS
ESCALATE_WHEN
AUTHORITY_LIMITS
DEPENDENCIES
```

Para `MECHANICAL_IMPLEMENTER`, o contrato deve fechar explicitamente a solução e
identificar o que **não** pode ser reinterpretado.

Para `VALIDATOR`, `SOURCE_WRITE_AUTHORIZATION = NO` mesmo quando a sandbox precise
de `workspace-write` para artefatos transitórios.

O contrato deve impedir:

- expansão de escopo;
- alteração arquitetural não autorizada;
- decisão reservada ao root/usuário;
- Git consequencial não autorizado;
- escrita fora do ownership;
- delegação recursiva;
- relaxamento de testes para obter PASS;
- conclusão sem evidência suficiente;
- repetição desnecessária do raciocínio já fechado pelo root.

```text
SUBAGENT_AUTO_DELEGATION = PROHIBITED
```

---

## 10. Responsabilidade do agente principal

O agente principal/orquestrador continua responsável por:

- interpretar a tarefa e authorities;
- escolher sua própria inteligência antes de selecionar subagentes;
- identificar hotspots cognitivos;
- decidir `DIRECT` ou `MULTIAGENT`;
- decidir entre root escalation, role delegation e independent review;
- selecionar o menor papel/tier suficiente;
- evitar duplicação de inteligência cara;
- fechar decisões antes de delegar execução mecânica;
- definir contratos;
- controlar dependências e ownership;
- reconciliar evidências;
- executar self-review quando sua capacidade for suficiente;
- validar o estado final;
- emitir o veredicto final.

```text
DELEGATION != ACCOUNTABILITY_TRANSFER
ROOT_CAN_DELEGATE_EXECUTION_WITHOUT_DELEGATING_DECISION_AUTHORITY
```

O root não deve se transformar em worker operacional apenas porque possui
capacidade para fazer todas as etapas.

---

## 11. Implementação: decisão por julgamento, não por capacidade bruta

A pergunta não é somente:

```text
CAN_ROOT_IMPLEMENT?
```

A pergunta correta é:

```text
DOES_IMPLEMENTATION_REQUIRE_ROOT_LEVEL_JUDGMENT?
```

### 11.1 Implementação direta pelo root

Preferir quando:

- patch é pequeno demais para justificar handoff;
- root já está no contexto completo e a delegação duplicaria leitura;
- implementação e raciocínio são fortemente acoplados;
- o custo de handoff supera economia de tier.

### 11.2 `luna_worker` / Mechanical Implementer

Preferir quando:

```text
SOLUTION_IS_CLOSED = YES
CHANGE_BOUNDARY_IS_EXPLICIT = YES
LOW_JUDGMENT = YES
OBJECTIVE_VALIDATION = YES
EXPECTED_COST_SAVING = MATERIAL
```

Não é necessário haver paralelismo.

### 11.3 `terra_implementer`

Preferir quando o writer precisa tomar decisões técnicas locais relevantes,
interpretar trade-offs, integrar componentes ou lidar com ambiguidade residual.

### 11.4 Regra econômica

```text
DO_NOT_USE_TERRA_FOR_MECHANICAL_WRITING
WHEN_LUNA_CAN_EXECUTE_SAFELY_AND_VERIFY_OBJECTIVELY
```

Custo nunca supera risco; caso a fronteira mecânica não seja clara, mantenha ou
suba o tier.

### 11.5 Threshold de delegação entre tiers adjacentes

A capacidade de um tier inferior não basta para justificar handoff.

Exemplo especialmente relevante:

```text
ROOT = TERRA / HIGH
CANDIDATE_IMPLEMENTER = TERRA / MEDIUM
```

Delegar só é preferível quando:

```text
LOWER_TIER_IS_SUFFICIENT = YES
IMPLEMENTATION_VOLUME_IS_MATERIAL = YES
BOUNDARY_IS_CLEAR = YES
EXPECTED_TIER_SAVING_IS_MATERIAL = YES
AND
EXPECTED_TIER_SAVING
> HANDOFF_COST + DUPLICATED_CONTEXT_COST + INTEGRATION_COST
```

Se o root e o implementer precisarem reconstruir praticamente o mesmo contexto e o
patch for pequeno, prefira o root mesmo que o tier inferior seja tecnicamente capaz.

```text
ADJACENT_TIER_CAPABILITY != ADJACENT_TIER_DELEGATION_REQUIRED
HIGH_ROOT_TO_MEDIUM_IMPLEMENTER_REQUIRES_MATERIAL_NET_GAIN = YES
```

A mesma lógica vale para `Terra/Medium → Luna/High`: patch mecânico minúsculo pode
continuar direto quando o handoff custar mais que a economia de execução.

---

## 12. Política de paralelismo

Paralelismo exige independência real.

Não paralelize:

- tarefas sequenciais;
- alterações nos mesmos arquivos;
- componentes fortemente acoplados;
- migrations e consumidores que dependam da mesma transição não estabilizada;
- investigações que exigem o mesmo contexto extenso;
- reviewers que apenas repetirão a mesma leitura sem independência necessária.

Quando houver paralelismo, estabeleça ownership explícito.

```text
CONCURRENT_WRITE_OVERLAP = PROHIBITED
```

O número máximo de subagentes simultâneos, quando configurado pela plataforma,
é **limite**, não objetivo.

```text
MAX_SUBAGENTS != TARGET_SUBAGENTS
MINIMUM_NECESSARY_SUBAGENTS = PREFERRED
MAX_CONCURRENT_WRITERS = 1
```

---

## 13. Economia de contexto

Evite replicar o mesmo conjunto grande de arquivos ou documentos para vários
agentes.

Multiagente perde valor quando:

```text
DUPLICATED_CONTEXT_COST
>=
PARALLELISM_OR_SPECIALIZATION_GAIN
```

Prefira:

- uma única leitura pelo principal quando o contexto é altamente compartilhado;
- partições por responsabilidade quando os dados são realmente separáveis;
- retornos compactos com evidência suficiente para adjudicação.

---

## 14. Contrato de retorno dos subagentes

O retorno deve ser proporcional ao objetivo.

Para investigação/review, prefira estrutura compacta:

```text
finding_id
severity
source / file:line
fact
inference
contract_or_invariant
impact
recommendation
confidence
```

Para implementação:

```text
scope_completed
files_changed
validation_executed
known_limitations
blockers
unresolved_decisions
```

Evite relatórios narrativos extensos quando não agregarem informação material.

---

## 15. Revisão adaptativa e capacidade do root

### 15.1 Self-review é o padrão quando o root é suficiente

```text
PRIMARY_ANALYSIS
CONSISTENCY_CHECK
ADVERSARIAL_SELF_REVIEW
FINAL_SELF_REVIEW
```

Self-review não é revisão independente.

### 15.2 Reviewer não deve duplicar o root

Antes de criar `terra_reviewer`:

```text
ROOT_REVIEW_CAPABILITY_SUFFICIENT = YES | NO
INDEPENDENCE_REQUIRED = YES | NO
DISTINCT_REVIEW_VALUE = YES | NO
```

Se:

```text
ROOT_REVIEW_CAPABILITY_SUFFICIENT = YES
INDEPENDENCE_REQUIRED = NO
DISTINCT_REVIEW_VALUE = NO
```

então:

```text
INDEPENDENT_REVIEWER = NO
REVIEW = ROOT_SELF_REVIEW
```

Exemplo típico:

```text
ROOT = TERRA / HIGH
REVIEW_REQUIREMENT <= TERRA / HIGH
INDEPENDENCE_REQUIRED = NO
→ DO_NOT_SPAWN_TERRA_HIGH_REVIEWER
```

### 15.3 Quando a revisão exigir inteligência maior, mas não independência

Preferir comparar:

```text
TEMPORARY_ROOT_ESCALATION
vs
SEPARATE_REVIEWER
```

Se apenas mais inteligência for necessária e não houver valor em responsabilidade
separada:

```text
PREFER_TEMPORARY_ROOT_ESCALATION_WHEN_CHEAPER_AND_SAFE
```

### 15.4 Quando reviewer independente é correto

Usar quando:

- governance exige independência;
- conflito de interesse cognitivo/ownership torna self-review insuficiente;
- uma segunda leitura independente reduz materialmente risco;
- o root não cobre a disciplina necessária e separar o review é mais eficiente que
  reconfigurar o root.

### 15.5 Escrita após review independente

Se independência fizer parte do gate, escrita posterior no escopo aprovado invalida
a aprovação desse escopo:

```text
FIX
→ VALIDATE
→ INDEPENDENT_REVIEW_AGAIN
```

---

## 16. Segurança

Revisão de segurança é ortogonal à revisão técnica geral.

Use `terra_security` somente quando existir superfície
material, como:

- autenticação/autorização;
- secrets;
- trust boundaries;
- filesystem sensível;
- execução de comandos;
- deserialização/parser de entrada não confiável;
- criptografia;
- exposição de rede;
- permissões/ACL;
- mudança de release com impacto relevante de segurança.

Uma tarefa ser “importante” não torna automaticamente necessário um agente de
segurança.

---

## 17. Conflitos e adjudicação

Subagente de adjudicação só deve ser considerado após existir conflito material
real.

```text
NO_CONFLICT = NO_ADJUDICATION_AGENT
```

Quando houver conflito não resolvível pelas authorities existentes ou pelo
agente principal dentro de sua responsabilidade:

```text
STOP_AT_SAFE_BOUNDARY = YES
AUTO_ESCALATION = NO
REPORT_EVIDENCE = YES
RETURN_TO_USER = YES
```

Não criar cadeia automática de reviewers ou arquitetos.

---

## 18. Skills, Plugins e multiagente

As decisões são independentes:

```text
MODEL
EFFORT
EXECUTION_MODE
SKILL
PLUGIN
```

Aplicar:

```text
SKILL_REQUIRED != SUBAGENT_REQUIRED
PLUGIN_REQUIRED != SUBAGENT_REQUIRED
SUBAGENT_REQUIRED != SKILL_REQUIRED
SUBAGENT_REQUIRED != PLUGIN_REQUIRED
```

Uma Skill ou Plugin pode ser usado pelo agente principal em modo direto.

Uma arquitetura multiagente não justifica uso adicional de Skills ou Plugins
sem benefício material próprio.

---

## 19. Read-only, write capability e limites de escrita

Separar três conceitos:

```text
GOVERNANCE_READ_ONLY
SOURCE_WRITE_AUTHORIZATION
TECHNICAL_WORKSPACE_WRITE_CAPABILITY
```

Eles não são equivalentes.

### 19.1 Atividade estritamente read-only

Se nenhuma escrita persistente ou transitória no workspace for autorizada:

```text
GOVERNANCE_READ_ONLY = YES
SUBAGENT_WRITE_PERMISSION = NO
```

Isso se aplica a todos os agentes.

### 19.2 Validação que exige artefatos transitórios

Alguns comandos de teste/build criam caches, bytecode, coverage ou outputs mesmo
quando a atividade não autoriza editar source.

Nesse caso pode ser permitido:

```text
TECHNICAL_WORKSPACE_WRITE_CAPABILITY = YES
SOURCE_WRITE_AUTHORIZATION = NO
```

Isso **não** transforma Validator em writer de código.

Se a validação produzir alteração persistente inesperada em source, tests,
configuração ou documentação governada:

```text
STOP
REPORT_UNEXPECTED_WORKSPACE_CHANGE
DO_NOT_SELF_REPAIR
```

### 19.3 Escrita de implementação/documentação

Quando source/doc write estiver autorizado:

```text
OWNERSHIP_REQUIRED = YES
MAX_CONCURRENT_WRITERS = 1
CONCURRENT_WRITE_OVERLAP = PROHIBITED
```

A delegação nunca amplia authority de escrita além do contrato recebido.

---

## 20. Git e operações consequenciais

Nenhum modo de execução autoriza por si só:

```text
GIT_STAGE
COMMIT
PUSH
TAG
RELEASE
DEPLOY
LIVE_EXECUTION
```

Essas operações dependem da autorização específica do projeto/usuário.

```text
MULTIAGENT_PASS != GIT_AUTHORIZATION
DIRECT_PASS != GIT_AUTHORIZATION
```

---

## 21. Early exit

Se um blocker inequívoco determinar que o gate necessariamente falhará:

1. registre evidência suficiente para caracterizar o blocker;
2. conclua apenas validações ainda necessárias para delimitar o estado;
3. evite gasto em findings de baixo valor que não alterariam a decisão;
4. pare em boundary seguro;
5. retorne ao agente principal/usuário conforme authority.

Não use early exit quando investigação adicional for necessária para delimitar
impacto ou preservar segurança.

---

## 22. Fluxo operacional recomendado

```text
1. CLASSIFY_TASK
2. LOAD_APPLICABLE_AUTHORITIES
3. CHOOSE_ROOT_MODEL_AND_EFFORT
4. IDENTIFY_COGNITIVE_HOTSPOTS
5. PARTITION_HIGH_JUDGMENT_VS_BOUNDED_WORK
6. EVALUATE_MULTIAGENT_GATES G1..G6
7. ESTIMATE_NET_MULTIAGENT_GAIN
8. IF GAIN UNCLEAR -> DIRECT
9. IF MULTIAGENT -> RUN ROOT_CAPABILITY_REDUNDANCY_CHECK
10. CHOOSE ESCALATE_ROOT vs DELEGATE_ROLE vs INDEPENDENT_REVIEW
11. DEFINE MINIMUM NECESSARY SUBAGENTS
12. DEFINE NON-OVERLAPPING CONTRACTS
13. EXECUTE HIGH-JUDGMENT WORK AT REQUIRED TIER
14. DELEGATE MECHANICAL/FACTUAL/VALIDATION WORK TO LOWER TIER WHEN SAFE
15. VALIDATE
16. TRIAGE ONLY ON FAILURE OR AMBIGUOUS RESULT
17. ROOT SELF-REVIEW BY DEFAULT
18. INDEPENDENT REVIEW ONLY IF REQUIRED OR MATERIALLY VALUABLE
19. RECONCILE RESULTS
20. DE-ESCALATE EXPENSIVE INTELLIGENCE WHEN POSSIBLE
21. FINALIZE ONLY WHEN STATE IS STABLE
```

---

## 23. Decision matrix

| Situação | Modo / papel recomendado |
|---|---|
| Tarefa pequena/local | `DIRECT` |
| Tarefa longa, porém cognitivamente monolítica | `DIRECT`, aumentar root se necessário |
| Root forte + muito trabalho mecânico verificável | `MULTIAGENT` sequencial por ganho econômico |
| Terra/High fecha solução; patch é prescritivo | `luna_worker` / Mechanical Implementer |
| Testes, lint, collect-only, build, diff checks | `luna_validator` |
| Falha de validação ambígua exige diagnóstico separado | `luna_triage` quando houver ganho material |
| Falha localizada e praticamente autoexplicativa | root corrige diretamente se handoff não pagar |
| Implementação exige julgamento técnico | `terra_implementer` se o handoff trouxer ganho líquido; caso contrário root implementa |
| Root Terra/High já cobre review e independência não é exigida | self-review do root; sem `terra_reviewer` |
| Governance exige review independente | `terra_reviewer` |
| Apenas mais inteligência é necessária | escalar root antes de criar papel redundante |
| Segurança material | `terra_security` quando separação agrega valor |
| Arquitetura / hard root cause | `sol_architect` temporário |
| Duas frentes read-only independentes | `MULTIAGENT`, mínimo necessário |
| Benefício de delegação incerto | `DIRECT` |
| Todos releriam o mesmo contexto extenso | `DIRECT` |
| Dois writers sobre o mesmo estado | proibido |

---

## 24. Anti-patterns proibidos

```text
SPAWN_SUBAGENT_BECAUSE_TASK_IS_COMPLEX = PROHIBITED
SPAWN_SUBAGENT_BECAUSE_PROFILE_EXISTS = PROHIBITED
SPAWN_MULTIPLE_AGENTS_FOR_SAME_ANALYSIS = PROHIBITED

ROOT_CAN_DO_IT_THEREFORE_ROOT_MUST_DO_ALL = PROHIBITED
IGNORE_ECONOMIC_TIERING_GAIN = PROHIBITED
KEEP_EXPENSIVE_ROOT_DOING_MECHANICAL_WORK_BY_DEFAULT = PROHIBITED

SPAWN_REVIEWER_BECAUSE_CODE_WAS_WRITTEN = PROHIBITED
SPAWN_TERRA_HIGH_REVIEWER_WHEN_TERRA_HIGH_ROOT_ALREADY_COVERS_REVIEW_AND_NO_INDEPENDENCE = PROHIBITED
DUPLICATE_EXPENSIVE_INTELLIGENCE_WITHOUT_DISTINCT_VALUE = PROHIBITED
DELEGATE_TO_ADJACENT_TIER_WITHOUT_MATERIAL_NET_GAIN = PROHIBITED
SPAWN_TRIAGE_BECAUSE_ANY_TEST_FAILED = PROHIBITED

USE_TERRA_IMPLEMENTER_FOR_PURELY_MECHANICAL_PATCH_BY_DEFAULT = PROHIBITED
USE_LUNA_WORKER_FOR_UNCLOSED_OR_AMBIGUOUS_DESIGN = PROHIBITED
VALIDATOR_AUTO_FIXES_WITHOUT_ROUTE = PROHIBITED
SCRIBE_INVENTS_PASS = PROHIBITED

AUTO_ESCALATE_TO_ARCHITECT = PROHIBITED
USE_SOL_AS_PERSISTENT_ORCHESTRATOR_BY_DEFAULT = PROHIBITED
USE_LUNA_LOW_OR_MEDIUM_BY_DEFAULT = PROHIBITED

USE_SUBAGENT_AS_AUTHORITY = PROHIBITED
OPTIONAL_SUBAGENT = PROHIBITED
CONCURRENT_WRITE_OVERLAP = PROHIBITED
MULTIAGENT_AS_STATUS_SYMBOL = PROHIBITED
USE_UNREGISTERED_SUBAGENT_PROFILE = PROHIBITED
SUBAGENT_RECURSIVE_DELEGATION = PROHIBITED
```

---

## 25. Cenários de conformidade de roteamento

Os cenários desta seção são **vetores de conformidade**, não receitas rígidas.
Eles registram decisões que a política deve conseguir reproduzir por raciocínio
econômico e de autoridade. Mudanças materiais no contexto podem alterar a rota.

```text
CONFORMANCE_SCENARIO != HARD_CODED_ROUTING_RECIPE
```

### Cenário A — patch trivial e localizado

Características:

- causa e solução fechadas;
- poucas linhas;
- contexto pequeno;
- teste focal objetivo;
- sem independência ou especialização.

Rota de referência validada:

```text
ROOT = TERRA / MEDIUM
MATERIAL_INTELLIGENCE_ROUTING_GAIN = NO
EXECUTION_MODE = DIRECT
SUBAGENTS_PLANNED = 0
```

Razão: Luna seria capaz de escrever/testar, mas o volume não amortiza contrato,
handoff, releitura e reconciliação.

### Cenário B — hotspot cognitivo + escrita mecânica + validação extensa

Características:

- decisão matemática/financeira sensível;
- solução pode ser fechada pelo root;
- patch posterior é prescritivo em vários arquivos;
- validação objetiva e volumosa.

Rota de referência validada:

```text
TERRA/HIGH ROOT
→ LUNA/HIGH MECHANICAL_IMPLEMENTER
→ LUNA/HIGH VALIDATOR
→ TERRA/HIGH ROOT SELF_REVIEW + FINAL ADJUDICATION
```

Não usar `terra_reviewer` sem independência; Triage somente em falha ambígua real.

### Cenário C — implementação bounded, mas com julgamento técnico local

Características:

- arquitetura e comportamento fechados;
- implementação exige concorrência/atomicidade/integração e decisões locais;
- volume suficiente para amortizar handoff;
- validação objetiva posterior.

Rota de referência validada:

```text
TERRA/HIGH ROOT
→ TERRA/MEDIUM IMPLEMENTER
→ LUNA/HIGH VALIDATOR
→ TERRA/HIGH ROOT SELF_REVIEW
```

Essa rota só é preferível quando a economia de tier supera duplicated context,
handoff e integração. Em patch menor, `TERRA/HIGH ROOT → DIRECT IMPLEMENTATION`
pode ser a rota economicamente correta.

### Cenário D — revisão independente obrigatória

Características:

- root forte;
- implementação concluída;
- governança exige independência;
- reviewer read-only.

Rota de referência validada:

```text
TERRA/HIGH ROOT
→ TERRA/HIGH INDEPENDENT REVIEWER
→ TERRA/HIGH ROOT FINAL ADJUDICATION
```

Aqui a duplicação de tier caro é justificada por `INDEPENDENCE_VALUE`, não por
incapacidade do root.

### Cenário E — falha de validação localizada e autoexplicativa

Características:

- contrato inequívoco;
- failure signature aponta diretamente para violação localizada;
- patch remanescente é mínimo;
- sem ambiguidade diagnóstica.

Rota de referência validada:

```text
ROOT = TERRA / MEDIUM
EXECUTION_MODE = DIRECT
TRIAGE = NO
NEW_HANDOFF_TO_MECHANICAL_IMPLEMENTER = NO
ROOT → REPAIR → FOCUSED_VALIDATION → SELF_REVIEW
```

Se a inspeção contradisser a hipótese evidente ou surgir falha nova/ambígua, o
roteamento deve ser reavaliado; `TEST_FAIL != TRIAGE_REQUIRED`.

### 25.1 Resultado da validação inicial da política

A bateria inicial A–E produziu:

```text
ROUTING_CONFORMANCE_TESTS = 5/5 PASS
DIRECT_SELECTION = PASS
MULTIAGENT_SELECTION = PASS
ECONOMIC_TIERING = PASS
COGNITIVE_HOTSPOT_ROUTING = PASS
MECHANICAL_IMPLEMENTATION_ROUTING = PASS
COMPLEX_IMPLEMENTATION_ROUTING = PASS
OBJECTIVE_VALIDATION_ROUTING = PASS
ROOT_REDUNDANCY_CONTROL = PASS
INDEPENDENT_REVIEW_SEMANTICS = PASS
CONDITIONAL_TRIAGE = PASS
AUTHORITY_PRESERVATION = PASS
INITIAL_ROUTING_VALIDATION = STRONG_PASS
```

Esse resultado valida inicialmente a lógica de roteamento; não transforma a política
em universalmente provada nem elimina necessidade de calibração por telemetria real.

---

## 26. Telemetria opcional para calibração

Quando fizer sentido e sem burocracia excessiva, registrar:

- `DIRECT` ou `MULTIAGENT`;
- root model/effort;
- motivo do root tier;
- gates ativados, inclusive `MATERIAL_INTELLIGENCE_ROUTING_GAIN`;
- papéis/tier usados;
- quantidade de subagentes;
- quantidade de handoffs;
- tempo aproximado;
- retries;
- escalations/de-escalations;
- conflitos de integração;
- se houve duplicação de contexto;
- se trabalho de tier caro foi efetivamente evitado;
- se a delegação produziu ganho real.

A telemetria existe para calibrar a política, não para justificar retroativamente
uma decisão ruim.

---

## 27. Regra de reavaliação durante a execução

Uma tarefa iniciada `DIRECT` pode revelar posteriormente:

- frente independente;
- necessidade de especialização;
- volume mecânico significativo;
- hotspot cognitivo seguido de trabalho barato;
- falha que justifica Triage;
- requisito novo de independência.

Isso não autoriza spawn especulativo. Registrar:

```text
NEW_MULTIAGENT_TRIGGER =
EXPECTED_GAIN =
SCOPE_OF_DELEGATION =
ROOT_CURRENT_MODEL =
ROOT_CURRENT_EFFORT =
WHY_NOT_ROOT =
SELECTED_ROLE =
SELECTED_TIER =
```

Também reavaliar no sentido oposto:

```text
MULTIAGENT_JUSTIFICATION_LOST
→ DO_NOT_SPAWN_ADDITIONAL_AGENTS
→ CONSOLIDATE_TO_DIRECT_WHEN_SAFE
```

Se um ponto difícil foi resolvido, de-escalation deve ser considerada imediatamente.

---

## 28. Checklist final antes de criar subagente

```text
1. Qual é o modelo/esforço atual do root?
2. Qual parte realmente exige essa inteligência?
3. O root já cobre suficientemente o papel proposto?
4. Existe independência obrigatória?
5. Existe especialização distinta material?
6. Existe ganho material de decomposição?
7. Existe ganho material de roteamento de inteligência?
8. O trabalho delegado é bounded e verificável?
9. O menor tier suficiente foi escolhido?
10. O handoff economiza mais do que custa?
11. Existe perfil registrado compatível?
12. O sandbox é compatível?
13. Há overlap de escrita ou contexto?
14. O retorno pode ser reconciliado objetivamente?
15. Um root escalation simples seria melhor que outro agente?
16. Estamos duplicando inteligência cara sem valor distinto?
17. Existe mais de uma rota tecnicamente válida?
18. Entre as rotas válidas, qual minimiza EXPECTED_COST_PER_SUCCESSFUL_TASK?
19. Delegação para tier adjacente ainda compensa após duplicated context e integração?
20. Uma failure é realmente ambígua o suficiente para justificar Triage?
```

Se não houver ganho claro:

```text
EXECUTION_MODE = DIRECT
SUBAGENTS_ALLOWED = NO
```

---

## 28.1 Registro operacional atual

Após materialização desta revisão, o registro operacional esperado é:

```text
ACTIVE_PROFILES =
luna_scout |
luna_researcher |
luna_validator |
luna_triage |
luna_worker |
luna_scribe |
terra_implementer |
terra_reviewer |
terra_security |
sol_architect

DEPRECATED_COMPATIBILITY_PROFILES =
luna_explorer |
luna_test_analyst

UNPROFILED_SUBAGENT = PROHIBITED
MAX_CONCURRENT_SUBAGENTS = 2
MAX_CONCURRENT_WRITERS = 1
DEFAULT_SUBAGENT_MODEL = CONFIGURATION_FALLBACK_ONLY
```

O root continua sendo escolhido na interface/superfície do Codex; a política recomenda
o tier conforme a atividade e não o fixa no TOML global.

---

## 28.2. Changelog resumido desta revisão

Mudanças da `v1.7-R2.1` sobre `v1.7-R2`:

- consolida cinco cenários A–E de conformidade com resultado inicial `5/5 PASS`;
- reconhece explicitamente que podem existir múltiplas rotas tecnicamente válidas;
- define seleção entre rotas por `EXPECTED_COST_PER_SUCCESSFUL_TASK`, confiabilidade, authority e eficiência de contexto;
- reforça que delegação para tier adjacente exige ganho líquido material após handoff, duplicated context e integração;
- proíbe spawn de Triage como reação ritual a qualquer falha de teste;
- explicita que failure localizada e autoexplicativa pode permanecer em reparo direto pelo root;
- preserva integralmente a separação desta revisão em relação a Bounded Cyclic Execution.

Base consolidada herdada da `v1.7-R2` sobre `v1.7-R1`:

- `direct-first` deixa de ser interpretado como “root capaz executa tudo”;
- adiciona `MATERIAL_INTELLIGENCE_ROUTING_GAIN` como gate G6;
- reconhece pipeline multiagente sequencial, não apenas paralelismo;
- exige escolher inteligência do root antes dos subagentes;
- adiciona gate de redundância da capacidade do root;
- diferencia `NEED_MORE_INTELLIGENCE`, `NEED_SEPARATE_RESPONSIBILITY` e
  `NEED_INDEPENDENCE`;
- introduz conceito explícito de hotspot cognitivo;
- `luna_worker` volta a ser perfil ativo como `MECHANICAL_IMPLEMENTER`;
- `terra_implementer` fica para implementação que exige julgamento material;
- Validator pode ter write capability técnica para artefatos de validação, sem
  source write authorization;
- reviewer deixa de ser apropriado quando apenas duplica root já suficiente;
- `Terra/High root + Terra/High reviewer` sem independência/valor distinto passa a
  anti-pattern;
- mantém máximo de dois subagentes concorrentes e um writer;
- mantém Bounded Cyclic Execution, Work Units e retry framework fora do escopo.

---

## 29. Resumo normativo

```text
DIRECT_EXECUTION = DEFAULT
MULTIAGENT_EXECUTION = EXCEPTION
MULTIAGENT != PARALLELISM_ONLY
SEQUENTIAL_MULTIAGENT_PIPELINE = ALLOWED

ECONOMICAL_INTELLIGENCE_ROUTING = REQUIRED
EXPECTED_COST_PER_SUCCESSFUL_TASK = OPTIMIZATION_TARGET
MULTIPLE_VALID_ROUTINGS_MAY_EXIST = YES
ROUTE_SELECTION_REQUIRES_MATERIAL_NET_GAIN = YES
ADJACENT_TIER_DELEGATION_REQUIRES_MATERIAL_NET_GAIN = YES
TEST_FAIL != TRIAGE_REQUIRED

EXPENSIVE_INTELLIGENCE = COGNITIVE_HOTSPOTS_ONLY
BOUNDED_VERIFIABLE_EXECUTION = LOWEST_SUFFICIENT_TIER

VALID_MULTIAGENT_TRIGGERS =
PARALLEL_INDEPENDENT_FRONTS |
DISTINCT_SPECIALIZATION_REQUIRED |
MATERIAL_DECOMPOSITION_GAIN |
IDENTIFIED_CONFLICT_REQUIRES_ADJUDICATION |
GOVERNANCE_REQUIRES_INDEPENDENT_REVIEW |
MATERIAL_INTELLIGENCE_ROUTING_GAIN

IF_BENEFIT_IS_UNCLEAR = DIRECT

ROOT_INTELLIGENCE_IS_PART_OF_ROUTING_DECISION = YES
ROOT_CAPABILITY_REDUNDANCY_CHECK = REQUIRED
DO_NOT_DUPLICATE_EXPENSIVE_INTELLIGENCE_WITHOUT_DISTINCT_VALUE = YES

NORMAL_ROOT = TERRA / MEDIUM
HIGH_JUDGMENT_ROOT = TERRA / HIGH

LUNA_DEFAULT = HIGH
LUNA_ANALYTICAL = XHIGH_WHEN_SUPPORTED

MECHANICAL_IMPLEMENTATION = LUNA / HIGH
NORMAL_IMPLEMENTATION_WITH_JUDGMENT = TERRA / MEDIUM
COMPLEX_IMPLEMENTATION = TERRA / HIGH

REVIEW = ROOT_SELF_REVIEW_BY_DEFAULT_WHEN_SUFFICIENT
INDEPENDENT_REVIEW = ONLY_WHEN_REQUIRED_OR_MATERIALLY_JUSTIFIED

ARCHITECTURE_OR_HARD_REVIEW = SOL / HIGH TEMPORARY SPECIALIST

MAX_CONCURRENT_SUBAGENTS = 2
MAX_CONCURRENT_WRITERS = 1

MODEL_ESCALATION != AUTHORITY_ESCALATION
DELEGATION != AUTHORITY_TRANSFER
WRITE_CAPABILITY != WRITE_AUTHORIZATION
CAPABILITY != PERMISSION

CYCLIC_EXECUTION_METHODOLOGY = OUT_OF_SCOPE_FOR_NOW
USER_FINAL_AUTHORITY = YES
```

---

## 30. Encerramento

O objetivo não é minimizar agentes a qualquer custo, nem maximizar delegação.

O objetivo é minimizar **custo esperado por tarefa concluída corretamente**, mantendo
qualidade, segurança, governança e previsibilidade.

Princípio final:

> **Use inteligência forte onde o julgamento forte muda materialmente a probabilidade
> de sucesso. Feche decisões e invariantes no tier adequado. Entre rotas tecnicamente
> válidas, prefira a que reduz o custo esperado da tarefa correta sem sacrificar
> confiabilidade ou authority. Delegue execução mecânica, factual e objetivamente
> verificável ao menor tier suficiente. Não crie
> reviewer para duplicar um root já capaz quando independência não é necessária.
> Multiagente deve economizar ou reduzir risco de forma demonstrável; caso contrário,
> execute diretamente.**

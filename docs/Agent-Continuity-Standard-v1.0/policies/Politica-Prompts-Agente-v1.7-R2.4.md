# Política de Geração de Prompts Multiagente — v1.7-R2.4

```text
STATUS = CANONICAL
LIFECYCLE = ACTIVE
PREVIOUS_BASE = Politica-Prompts-Agente-v1.7-R2.3.md
CONSOLIDATES = Politica-Prompts-Agente-v1.7-R2.3.md
REVISION_FOCUS = COGNITIVE_DEMAND_CLASSIFICATION + COGNITIVE_MECHANICAL_SPLIT
MULTIAGENT_ALIGNMENT = AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico
SCOPE = TRANSVERSAL
DOMAIN_SPECIFIC_CONTENT = PROHIBITED
BOUNDED_CYCLIC_EXECUTION_INCLUDED = NO
CANONICALIZATION = YES
PROMOTION = YES
USER_REVIEW_REQUIRED = NO
```

---

## 0. Finalidade

Esta política governa a criação de prompts de atividade para Work ou Codex.

Ela possui dois objetivos simultâneos:

1. escolher uma arquitetura de execução tecnicamente correta e economicamente racional;
2. entregar ao executor somente o contexto necessário para executar a atividade.

A política deve impedir dois desperdícios distintos:

```text
EXECUTION_WASTE =
UNNECESSARY_MODEL_COST
+ UNNECESSARY_REASONING_COST
+ UNNECESSARY_SUBAGENT_COST
+ UNNECESSARY_COORDINATION_COST

PROMPT_WASTE =
IRRELEVANT_EXECUTOR_CONTEXT
+ DUPLICATED_CONTEXT
+ INTERNAL_GOVERNANCE_REASONING_EXPOSED_TO_EXECUTOR
+ UNUSED_CAPABILITY_INFORMATION
```

Princípio central:

```text
THE_GENERATOR_MAY_REASON_BROADLY
THE_EXECUTOR_PROMPT_MUST_BE_NARROW
```

A análise necessária para escolher modelo, esforço, subagentes, Skills e Plugins
não precisa ser enviada integralmente ao Codex/Work.

---

## 1. Duas audiências, dois outputs

Toda geração de prompt deve separar obrigatoriamente:

```text
OUTPUT_A = EXECUTION_DECISION_CARD
AUDIENCE_A = USER

OUTPUT_B = EXECUTOR_PAYLOAD
AUDIENCE_B = CODEX | WORK
```

### 1.1 Regra de cópia

```text
USER_SHOULD_COPY_TO_EXECUTOR = OUTPUT_B_ONLY
```

O Card A existe para o usuário visualizar e auditar a decisão de roteamento.

O Card B contém o prompt executável.

Não misturar as duas audiências.

---

# PARTE I — DECISÃO INTERNA DO GERADOR

## 2. Internal Routing Worksheet — NÃO enviar ao executor

O agente gerador deve avaliar internamente, quando aplicável:

```text
TASK_CLASS
RISK
COGNITIVE_COMPLEXITY
OPERATIONAL_VOLUME
VERIFIABILITY
REVERSIBILITY

COGNITIVE_HOTSPOTS
MECHANICAL_WORK
OBJECTIVE_VALIDATION_WORK

AMBIGUITY_SCORE
NOVELTY_SCORE
COUPLING_SCORE
INVARIANT_COMPLEXITY_SCORE
CAUSAL_DEPTH_SCORE
QUANT_SCIENTIFIC_DEPTH_SCORE
CONTEXT_RECONCILIATION_SCORE
PEAK_DIFFICULTY
HIGH_DIMENSION_COUNT
CAPABILITY_DEMAND_CLASS

MATERIAL_DECISION_COUNT
DEPENDENCY_DEPTH
CONSTRAINT_INTERACTION
EVIDENCE_VOLUME
DEFENSIBLE_ALTERNATIVES
ITERATIVE_REASONING_NEED
DELIBERATION_DEMAND_CLASS

EXECUTION_RISK_CLASS

COGNITIVE_MECHANICAL_SPLIT
CLOSED_DECISION_MATERIALIZATION
ROOT_MUST_READ_SOURCE_TO_MAKE_DECISION
ROOT_MUST_REVIEW_FINAL_DELTA

ROUTINE_EXECUTION_GATE
SOL_GATE
ASTRA_SELECTION_GATE

PARALLEL_INDEPENDENT_FRONTS
DISTINCT_SPECIALIZATION_REQUIRED
MATERIAL_DECOMPOSITION_GAIN
IDENTIFIED_CONFLICT_REQUIRES_ADJUDICATION
GOVERNANCE_REQUIRES_INDEPENDENT_REVIEW
MATERIAL_INTELLIGENCE_ROUTING_GAIN

EXPECTED_MATERIAL_GAIN
HANDOFF_COST
DUPLICATED_CONTEXT_COST
INTEGRATION_COST
REDUNDANCY_CHECK
```

Esses campos são instrumentos de decisão.

Por padrão:

```text
INTERNAL_ROUTING_WORKSHEET
NOT_IN_EXECUTOR_PAYLOAD
```

Só transformar uma conclusão interna em instrução do executor quando ela alterar:

- ação;
- escopo;
- authority;
- ownership;
- delegation;
- validação;
- stop condition;
- output esperado.

---

## 3. Relevance Gate do payload

Antes de inserir qualquer informação no Card B, aplicar:

```text
EXECUTOR_RELEVANCE_TEST
```

Pergunta:

> Se eu remover esta informação, existe chance material de o Codex/Work executar
> uma ação diferente, ultrapassar o escopo, validar incorretamente, delegar
> incorretamente, parar no lugar errado ou produzir um output inadequado?

Se:

```text
NO
```

então:

```text
OMIT_FROM_EXECUTOR_PAYLOAD
```

### 3.1 Informação normalmente pertinente

Inclua quando aplicável:

- objetivo;
- resultado esperado;
- root oficial;
- branch/baseline quando forem gates reais;
- authorities que precisam ser consultadas;
- arquivos ou superfícies relevantes;
- escopo autorizado;
- não escopo material;
- invariantes;
- contrato congelado;
- critérios de aceite;
- ações concretas;
- ordem operacional quando necessária;
- subagentes efetivamente autorizados;
- ownership;
- write mode;
- validações;
- comandos necessários;
- regras de Git;
- ações externas autorizadas ou proibidas quando plausíveis;
- stop conditions;
- formato mínimo de retorno.

### 3.2 Informação normalmente NÃO pertinente

Não enviar ao executor por padrão:

- histórico de evolução da policy;
- explicação longa sobre por que outro modelo foi rejeitado;
- gates completos G1–G6;
- score interno de risco;
- lista completa de alternativas descartadas;
- cálculo narrativo de economicidade;
- justificativas de `NO` para papéis não usados;
- catálogo de Skills não selecionadas;
- catálogo de Plugins não selecionados;
- anti-patterns genéricos da policy;
- exemplos de conformidade;
- telemetria de governança sem impacto na atividade;
- rationale repetido em múltiplas seções;
- conteúdo de documento canônico que o executor pode ler diretamente;
- regras genéricas que não mudam a execução concreta.

---

## 4. Referenciar em vez de duplicar

Quando Codex/Work tiver acesso ao repositório ou arquivo:

```text
REFERENCE_CANONICAL_SOURCE
PREFER_OVER_COPYING_CANONICAL_SOURCE
```

Use:

```text
AUTHORITY_TO_READ =
<path exato>
```

e, quando possível:

```text
READ_ONLY_RELEVANT_SECTION =
<título, seção ou assunto necessário>
```

Não copie para o prompt dezenas ou centenas de linhas de um documento local
se o executor pode lê-lo no próprio workspace.

Exceção:

- valor congelado necessário para comparação;
- checksum esperado;
- invariant curto;
- requisito que precisa estar imediatamente visível;
- boundary crítico cuja omissão seria perigosa.

---

# PARTE II — MODELO E ESFORÇO

## 5. Configuração mínima suficiente

A configuração é composta por decisões independentes:

```text
MINIMUM_SUFFICIENT_CONFIGURATION =
MODEL
+ REASONING_EFFORT
+ EXECUTION_MODE
+ SKILL
+ PLUGIN
+ NATIVE_EXECUTION
```

Objetivo:

```text
EXPECTED_COST_PER_SUCCESSFUL_TASK
```

sujeito a:

```text
QUALITY
ROBUSTNESS
VERIFIABILITY
AUTHORITY_PRESERVATION
SCOPE_CONTROL
```

Não selecionar por prestígio ou disponibilidade.

```text
MODEL_AVAILABLE != MODEL_REQUIRED
STRONGER_MODEL != BETTER_DEFAULT
HIGHER_EFFORT != BETTER_DEFAULT
TASK_IMPORTANT != STRONGER_MODEL_REQUIRED
TASK_LARGE != STRONGER_MODEL_REQUIRED
MANY_FILES != STRONGER_MODEL_REQUIRED
LONG_CONTEXT != STRONGER_MODEL_REQUIRED
HIGH_RISK != STRONGER_MODEL_REQUIRED
SCIENTIFIC_TASK != SOL_REQUIRED
ARCHITECTURAL_TASK != SOL_REQUIRED
```

### 5.1 Três eixos independentes

A seleção deve separar:

```text
CAPABILITY_DEMAND
→ seleciona MODEL_FAMILY

DELIBERATION_DEMAND
→ seleciona REASONING_EFFORT dentro da família

EXECUTION_RISK
→ seleciona rigor de AUTHORITY, VALIDATION, REVIEW e STOP CONDITIONS
```

Regra central:

```text
MODEL_FAMILY
IS_SELECTED_BY
CAPABILITY_DEMAND

REASONING_EFFORT
IS_SELECTED_BY
DELIBERATION_DEMAND

VALIDATION_AND_AUTHORITY
ARE_SELECTED_BY
EXECUTION_RISK
```

Não usar risco, importância, domínio científico ou rótulo arquitetural como
atalho para selecionar um modelo mais forte.

### 5.2 Capability Demand — C0 a C4

A demanda de capacidade deve ser classificada por dimensões cognitivas de `0–4`.

```text
AMBIGUITY
NOVELTY
COUPLING
INVARIANT_COMPLEXITY
CAUSAL_DEPTH
QUANT_SCIENTIFIC_DEPTH
CONTEXT_RECONCILIATION
```

Interpretação geral:

```text
0 = ausente / fechado / trivial
1 = baixo
2 = moderado
3 = alto
4 = extremo / excepcional
```

Guia por dimensão:

| Dimensão | 0 | 2 | 4 |
|---|---|---|---|
| `AMBIGUITY` | requisitos fechados | algumas escolhas relevantes | problema fortemente subespecificado |
| `NOVELTY` | padrão conhecido | adaptação relevante | sem padrão confiável conhecido |
| `COUPLING` | componente isolado | vários componentes | muitas interdependências materiais |
| `INVARIANT_COMPLEXITY` | invariantes simples | múltiplos invariantes | invariantes difíceis, conflitantes ou altamente sensíveis |
| `CAUSAL_DEPTH` | causa direta | diagnóstico multietapa | causalidade difícil/cross-system |
| `QUANT_SCIENTIFIC_DEPTH` | trivial/ausente | análise técnica não trivial | derivação/modelagem científica difícil |
| `CONTEXT_RECONCILIATION` | uma fonte | várias fontes compatíveis | authorities/evidências difíceis de reconciliar |

Não somar mecanicamente os pontos.

Calcular:

```text
PEAK_DIFFICULTY =
MAX(all cognitive dimensions)

HIGH_DIMENSION_COUNT =
COUNT(dimensions >= 3)
```

Classificação:

```text
C0 =
NO_MATERIAL_DECISION
AND SOLUTION_CLOSED

C1 =
PEAK_DIFFICULTY <= 1

C2 =
PEAK_DIFFICULTY = 2

C3 =
PEAK_DIFFICULTY = 3
OR HIGH_DIMENSION_COUNT >= 2

C4 =
PEAK_DIFFICULTY = 4
OR HIGH_DIMENSION_COUNT >= 3
OR EXCEPTIONAL_CAPABILITY_TRIGGER = PRESENT
```

A classificação é um instrumento de roteamento, não um score científico exato.

### 5.3 Baseline de família por Capability Demand

```text
C0
→ LUNA

C1
→ LUNA | TERRA conforme julgamento remanescente

C2
→ TERRA

C3
→ TERRA por padrão
→ SOL somente se houver CAPABILITY_GAP material

C4
→ SOL por padrão
→ ASTRA somente se ASTRA_SELECTION_GATE = PASS
```

Importante:

```text
C3 != SOL_REQUIRED
```

Um problema difícil ainda pode estar dentro da capacidade de Terra, especialmente
quando a dificuldade é de deliberação sustentada e não de capacidade.

### 5.4 Deliberation Demand — D0 a D4

A demanda de deliberação mede quanto raciocínio sustentado é necessário **depois**
de escolhida a família de modelo.

Avaliar:

```text
MATERIAL_DECISION_COUNT
DEPENDENCY_DEPTH
CONSTRAINT_INTERACTION
EVIDENCE_VOLUME
NEED_FOR_COUNTERFACTUAL_ANALYSIS
DEFENSIBLE_ALTERNATIVES
ITERATIVE_REASONING_NEED
```

Classificação:

```text
D0 = decisão já fechada / execução prescrita
D1 = raciocínio curto
D2 = raciocínio moderado
D3 = raciocínio profundo
D4 = raciocínio excepcionalmente sustentado
```

Regra:

```text
DELIBERATION_GAP
→ INCREASE_EFFORT

CAPABILITY_GAP
→ INCREASE_MODEL
```

Não usar esforço extremo para compensar incapacidade real do modelo.

### 5.5 Effort mapping por família

#### Luna

```text
D0-D2
→ LUNA / HIGH

D3-D4 analytical work
→ LUNA / XHIGH WHEN SUPPORTED
```

Luna Low/Medium não voltam a ser defaults.

#### Terra

```text
D1-D2
→ TERRA / MEDIUM

D3
→ TERRA / HIGH

D4
→ TERRA / XHIGH WHEN SUPPORTED
```

Aplicar:

```text
TERRA_XHIGH
SHOULD_BE_CONSIDERED
BEFORE_SOL
WHEN_THE_GAP_IS_DELIBERATION
```

Mas:

```text
DO_NOT_USE_TERRA_XHIGH
TO_COMPENSATE_FOR_A_TRUE_CAPABILITY_GAP
```

#### Sol

Depois de `SOL_GATE = PASS`, dimensionar o esforço em vez de usar `HIGH`
automaticamente:

```text
D1
→ SOL / LOW

D2
→ SOL / MEDIUM

D3-D4
→ SOL / HIGH
```

Logo:

```text
SOL_REQUIRED
!=
SOL_HIGH_REQUIRED
```

Um problema pequeno e bem delimitado pode exigir capacidade Sol sem exigir
deliberação High.

Se o runtime expuser apenas um perfil Sol com esforço fixo, essa restrição deve
ser declarada como limitação operacional:

```text
DESIRED_SOL_EFFORT = <LOW | MEDIUM | HIGH>
RUNTIME_PROFILE_EFFORT = <actual>
EFFORT_OVERRIDE_AVAILABLE = YES | NO
```

Não inventar um perfil inexistente apenas para satisfazer o mapping.

Combinações incoerentes devem ser reavaliadas. Exemplo:

```text
C4 + D0
```

normalmente indica classificação incorreta, pois capability excepcional sem
qualquer decisão remanescente tende a significar que o hotspot já foi fechado.

### 5.6 Execution Risk — R0 a R4

Risco operacional permanece separado da escolha de modelo.

```text
R0 = read-only / impacto desprezível
R1 = alteração local e facilmente reversível
R2 = alteração material, bounded e reversível
R3 = ação consequencial / publicação / mudança de estado relevante
R4 = produção, LIVE, financeiro, segurança crítica, irreversibilidade alta
```

Risco controla:

```text
AUTHORIZATION_STRENGTH
VALIDATION_DEPTH
PRECONDITIONS
POSTCONDITIONS
REVIEW_REQUIREMENT
STOP_ON_MISMATCH
```

e não:

```text
MODEL_STRENGTH
```

Exemplos:

```text
C0 + D0 + R4
→ modelo barato pode ser suficiente
→ authority/validation devem ser rigorosas

C4 + D4 + R0
→ SOL/HIGH pode ser necessário
→ atividade continua read-only
```

### 5.7 Regra de quantificação para arquitetura e ciência

Antes de escalar por domínio:

```text
HIGH_DIFFICULTY
MUST_BE_QUANTIFIED
BEFORE_MODEL_ESCALATION
```

Portanto:

```text
ARCHITECTURE
→ CLASSIFY C + D + R

SCIENCE
→ CLASSIFY C + D + R
```

e nunca:

```text
ARCHITECTURE
→ AUTOMATIC SOL/HIGH

SCIENCE
→ AUTOMATIC SOL/HIGH
```

---

## 6. Taxonomia operacional de modelos

```text
NORMAL_OPERATING_RANGE =
LUNA | TERRA

SOL =
ESCALATION_MODEL

ASTRA =
EXCEPTIONAL_CAPABILITY_MODEL
```

### 6.1 Luna

Preferido para:

- trabalho focado;
- repetitivo;
- mecânico;
- baixo em ambiguidade;
- volumoso e sensível a custo;
- execução derivada de decisão já tomada.

Para subagentes:

```text
LUNA_DEFAULT = HIGH
LUNA_ANALYTICAL = XHIGH_WHEN_SUPPORTED
```

A política de subagentes não deve voltar a usar Luna Low/Medium como default.

### 6.2 Terra

Default para:

- trabalho técnico cotidiano;
- julgamento moderado;
- integração conhecida;
- implementação não puramente mecânica.

```text
TERRA_TECHNICAL_ROOT_BASELINE = MEDIUM
ROOT_BASELINE != ROOT_FLOOR
```

`Terra / Medium` é o baseline para atividades em que ainda existe julgamento
técnico real. Não é o menor ROOT permitido.

Terra/High é usado quando existe julgamento técnico elevado.

`Terra / XHigh`, quando suportado, é preferido para `D4` quando o problema continua dentro da capacidade esperada de Terra e o gap é de deliberação, não de capacidade.

### 6.2.1 Seleção do ROOT pela demanda cognitiva remanescente

O ROOT deve ser escolhido pela **demanda cognitiva ainda existente na atividade
atual**, não pela importância do projeto, pela categoria documental ou pelo fato
de a ação ser consequencial.

```text
SELECT_ROOT_BY_REMAINING_COGNITIVE_DEMAND = YES
```

Princípios:

```text
TASK_IS_GOVERNANCE != TERRA_REQUIRED
CONSEQUENTIAL_GIT_ACTION != STRONGER_MODEL_REQUIRED
HIGH_CONSEQUENCE != HIGH_COGNITIVE_COMPLEXITY
PERMISSION_REQUIREMENT != MODEL_REQUIREMENT
```

Uma atividade completamente fechada, mecânica e objetivamente verificável pode
usar Luna/High como ROOT.

```text
LUNA_ROOT_ELIGIBLE_FOR_CLOSED_MECHANICAL_TASKS = YES
```

Gate:

```text
IF
SCOPE_ALREADY_ADJUDICATED = YES
AND FILE_SET_EXACT = YES
AND SEMANTIC_DECISIONS_REMAINING = NONE
AND AUTHORITY_CONFLICT = NONE
AND VALIDATION_IS_OBJECTIVE = YES
AND OPERATION_SEQUENCE_IS_PRESCRIBED = YES
AND CONSEQUENTIAL_ACTIONS_EXPLICITLY_AUTHORIZED = YES

THEN
ROOT = LUNA / HIGH
```

Exemplos compatíveis:

- stage de paths exatos já aprovados;
- `git diff --cached --check`;
- commit com mensagem já definida;
- push já autorizado;
- verificação objetiva de `HEAD`, `origin`, divergence e worktree;
- publicação mecânica de artefato cuja identidade e escopo já foram adjudicados.

Por outro lado:

```text
IF
FILES_MUST_BE_CLASSIFIED = YES
OR SCOPE_RECONCILIATION_REQUIRED = YES
OR POLICY_IDENTITY_REQUIRES_JUDGMENT = YES
OR AUTHORITY_INTERPRETATION_REQUIRED = YES
OR DIFF_CONTAINS_UNRESOLVED_SEMANTICS = YES
OR MATERIAL_DECISION_REMAINS_OPEN = YES

THEN
ROOT = TERRA / MEDIUM
```

Escalar acima disso somente quando a carga cognitiva real justificar.

### 6.2.2 Consequência, autorização e inteligência são eixos distintos

Ações como commit, push, deploy, publicação ou alteração externa podem exigir
autorização explícita e gates rigorosos, mas isso não implica modelo mais forte.

```text
CONSEQUENTIAL_ACTION
→ STRONG_PERMISSION_BOUNDARY

CONSEQUENTIAL_ACTION
!=
STRONGER_MODEL_BY_DEFAULT
```

O modelo responde à dificuldade de raciocínio.

A permission responde à authority concedida.

A validação responde à necessidade de evidência.

Esses eixos não devem ser confundidos.

### 6.3 Sol

Sol é elegível apenas quando:

```text
SOL_GATE = PASS
```

Triggers materiais incluem:

```text
DIFFICULT_MULTI_COMPONENT_INTEGRATION
HARD_BUT_BOUNDED_DEBUGGING
MATERIAL_CONTRACT_OR_INVARIANT_REASONING
DEEP_CROSS_DOCUMENT_SYNTHESIS
NONTRIVIAL_ARCHITECTURAL_DECISION
MULTIPLE_INTERDEPENDENT_TECHNICAL_CONSTRAINTS
TERRA_EXPECTED_TO_REQUIRE_MATERIAL_REWORK
```

Também:

```text
EXPECTED_SOL_GAIN = MATERIAL
TERRA_EXPECTED_SUFFICIENCY = NO | MATERIALLY_INFERIOR
```

Depois que `SOL_GATE = PASS`, selecionar esforço separadamente:

```text
SOL / LOW
→ capability gap real + deliberação curta

SOL / MEDIUM
→ capability gap real + deliberação moderada

SOL / HIGH
→ capability gap real + deliberação profunda/sustentada
```

Não usar `SOL / HIGH` como configuração automática apenas porque Sol foi
selecionado.

### 6.4 Astra

Astra é excepcional.

Somente elegível quando:

```text
ASTRA_SELECTION_GATE = PASS
```

Exige cumulativamente:

```text
ASTRA_HARD_TRIGGER = PRESENT
EXPECTED_ASTRA_GAIN = MATERIAL
WHY_SOL_IS_NOT_PREFERRED = CONCRETE
ASTRA_USAGE_COST_ACCEPTABLE = YES
```

Hard triggers podem incluir:

```text
OPEN_ENDED_UNFAMILIAR_PROBLEM
MATERIAL_NOVELTY_WITH_NO_CLEAR_SOLUTION_PATTERN
EXCEPTIONALLY_DIFFICULT_CAUSAL_DEBUGGING
HARD_END_TO_END_REASONING_ACROSS_MULTIPLE_SYSTEMS
FRONTIER_TECHNICAL_OR_SCIENTIFIC_REASONING
VERY_DIFFICULT_LONG_CONTEXT_RECONCILIATION
HIGH_COMPLEXITY_COMPUTER_OR_TOOL_ORCHESTRATION
SOL_CAPABILITY_ALREADY_OBSERVED_AS_INSUFFICIENT
```

### 6.5 Modelo e esforço são independentes

```text
MODEL != REASONING_EFFORT

CAPABILITY_GAP
→ CONSIDER_STRONGER_MODEL

DELIBERATION_GAP
→ CONSIDER_HIGHER_EFFORT

MISSING_INFORMATION_OR_ACCESS
→ ACQUIRE_INFORMATION_OR_STOP
```

Nunca usar modelo ou esforço para compensar:

- arquivo ausente;
- contexto ausente;
- requisito ausente;
- permission ausente;
- tool/plugin ausente;
- authority ausente.

---

# PARTE III — ROTEAMENTO MULTIAGENTE

## 7. ROOT antes dos subagentes

Decidir primeiro:

```text
ORCHESTRATOR_MODEL
ORCHESTRATOR_EFFORT
```

Depois avaliar subagentes.

```text
ROOT_CAN_EXECUTE != ROOT_SHOULD_EXECUTE
LOWER_TIER_CAN_EXECUTE != LOWER_TIER_SHOULD_EXECUTE
```

---

## 8. DIRECT vs MULTIAGENT

### 8.1 DIRECT

Preferir DIRECT quando:

- trabalho pequeno;
- contexto pequeno;
- ROOT já possui contexto suficiente;
- decomposição não reduz custo/risco/contexto;
- handoff custa mais que a economia;
- não existe independência obrigatória;
- não existe especialização material separável.

```text
IF_BENEFIT_IS_UNCLEAR = DIRECT
```

### 8.2 MULTIAGENT

Multiagente exige ganho material demonstrável.

```text
MULTIAGENT != PARALLELISM
```

Pipeline sequencial é válido.

Exemplo:

```text
ROOT
→ IMPLEMENTER
→ VALIDATOR
→ ROOT
```

### 8.3 Offload Materiality Gate — obrigatório antes de qualquer delegação

Capacidade técnica para delegar não constitui justificativa econômica para delegar.

```text
OBJECTIVE_WORK != DELEGABLE_WORK
LOWER_TIER_CAPABLE != HANDOFF_ECONOMICALLY_JUSTIFIED
DELEGABLE != WORTH_DELEGATING
```

Depois de identificar um papel tecnicamente compatível, o gerador deve aplicar:

```text
OFFLOAD_MATERIALITY_GATE
```

O gate só passa quando o ganho líquido de separar a responsabilidade é material.

```text
OFFLOAD_MATERIALITY_GATE = PASS

IF:

DELEGATED_OPERATIONAL_VOLUME = MATERIAL
OR ROOT_TIME_SAVED = MATERIAL
OR ROOT_CONTEXT_POLLUTION_AVOIDED = MATERIAL
OR DISTINCT_SPECIALIZATION_VALUE = MATERIAL
OR INDEPENDENCE_VALUE = MATERIAL

AND:

EXPECTED_OFFLOAD_GAIN
>
HANDOFF_COST
+ DUPLICATED_CONTEXT_COST
+ RECONCILIATION_COST
+ INTEGRATION_COST
```

Caso contrário:

```text
OFFLOAD_MATERIALITY_GATE = FAIL
→ KEEP_WORK_IN_ROOT
```

A mera existência de um agente especializado não reduz o limiar econômico.

```text
ROLE_EXISTS != ROLE_SHOULD_BE_USED
PROFILE_AVAILABLE != OFFLOAD_JUSTIFIED
```

### 8.4 Evidence duplication vs final review

Antes de delegar, distinguir:

```text
ROOT_MUST_READ_SOURCE_TO_MAKE_DECISION
```

de:

```text
ROOT_MUST_REVIEW_FINAL_DELTA
```

Esses custos não são equivalentes.

```text
ROOT_MUST_REVIEW_FINAL_DELTA
!=
DUPLICATED_CONTEXT_BY_DEFAULT

REVIEW_COST
!=
MATERIALIZATION_COST
```

Existe penalidade forte quando o subagente precisa absorver praticamente o mesmo
contexto amplo do ROOT para **redescobrir ou reinterpretar a solução**.

Exemplo:

```text
ROOT reads all authorities
→ SUBAGENT rereads all authorities
→ SUBAGENT re-derives decisions
→ ROOT rereads everything

DUPLICATED_CONTEXT_COST = HIGH
```

Não aplicar a mesma penalidade quando o ROOT já fechou a decisão e entrega um
contrato estreito:

```text
ROOT reads authorities
→ closes decisions / invariants
→ freezes narrow contract
→ LOWER_TIER materializes
→ ROOT reviews only final delta

DUPLICATED_CONTEXT_COST = LOW | MODERATE
```

Portanto:

```text
IF ROOT_MUST_READ_SOURCE_TO_MAKE_DECISION = YES
AND LOWER_TIER_MUST_RECONSUME_SAME_SOURCE_CONTEXT = YES
AND DELEGATED_VOLUME = LOW | MEDIUM
THEN
PREFER_DIRECT = YES
```

Mas:

```text
IF ROOT_MUST_REVIEW_FINAL_DELTA = YES
AND LOWER_TIER_RECEIVES_CLOSED_NARROW_CONTRACT = YES
THEN
DO_NOT_TREAT_FINAL_REVIEW_AS_FULL_CONTEXT_DUPLICATION
```

A revisão final do ROOT preserva adjudicação; ela não implica que o ROOT deveria
ter produzido fisicamente todo o delta.

### 8.5 Routine Governance / Git Checkpoint

Atividades de reconciliação e versionamento rotineiro de governança/configuração
devem ser consideradas, por padrão, uma única linha operacional do ROOT quando:

```text
KNOWN_BASELINE = YES
BOUNDED_FILE_SET = YES
NO_ARCHITECTURAL_DECISION = YES
ROUTINE_GIT_OPERATIONS = YES
SMALL_CONFIG_VALIDATION = YES
ROOT_MUST_REVIEW_DIFF = YES
```

Rota padrão:

```text
ROUTINE_GOVERNANCE_CHECKPOINT
→ DIRECT_BY_DEFAULT
→ ZERO_SUBAGENTS_BY_DEFAULT
→ ROOT_SELECTED_BY_REMAINING_COGNITIVE_DEMAND
```

Não hard-code `Terra / Medium` apenas porque o checkpoint é de governança.

Se ainda houver reconciliação, classificação, interpretação de authority ou
julgamento semântico:

```text
ROOT = TERRA / MEDIUM
```

Se todas as decisões estiverem fechadas e restar apenas execução prescrita,
bounded e objetivamente verificável:

```text
ROOT = LUNA / HIGH
```

Não criar Validator apenas para deslocar checks pequenos de Git, TOML, filenames,
registry ou stage.

MULTIAGENT só se torna elegível quando houver ganho material adicional, por exemplo:

- suíte longa ou pesada;
- build demorado;
- grandes volumes de logs;
- varredura extensa de dados;
- centenas de arquivos/artefatos independentes;
- revisão independente obrigatória;
- especialização distinta material.

### 8.6 Nova atividade fechada vs de-escalation no meio da atividade

Distinguir:

```text
NEW_TASK_WITH_ALL_DECISIONS_ALREADY_CLOSED
```

de:

```text
MID_TASK_DEESCALATION
```

Uma nova atividade cujo contrato já nasce fechado pode começar diretamente no
menor ROOT suficiente:

```text
NEW_TASK_WITH_ALL_DECISIONS_ALREADY_CLOSED
+ MECHANICAL
+ OBJECTIVELY_VERIFIABLE
→ LUNA / HIGH ROOT IS ELIGIBLE
```

Por outro lado, se Terra já está executando uma atividade e faltam apenas poucos
comandos mecânicos, trocar de ROOT pode custar mais do que continuar diretamente.

```text
MID_TASK_DEESCALATION
REQUIRES_MATERIAL_NET_GAIN = YES
```

Portanto:

```text
LOWER_TIER_IS_SUFFICIENT
!=
MID_TASK_HANDOFF_IS_ECONOMICALLY_JUSTIFIED
```

Quando o trabalho remanescente for pequeno:

```text
CURRENT_ROOT_CONTINUES_DIRECTLY
```

é preferível a criar um novo handoff apenas para economizar algumas operações.

### 8.7 Cognitive–Mechanical Split Gate

Antes de fechar `DIRECT` ou `MULTIAGENT`, verificar se a mesma atividade contém:

```text
A) COGNITIVE_WORK
```

como:

- arquitetura;
- ciência;
- modelagem;
- adjudicação;
- definição de invariantes;
- definição de contracts;
- decisões semânticas;
- interpretação de authorities;
- resolução de conflitos;
- escolhas técnicas materiais;

e:

```text
B) MECHANICAL_MATERIALIZATION
```

como:

- escrita de documentação;
- materialização de Authority já definida;
- atualização factual de estado/roadmap/sprints;
- implementação prescrita;
- wiring simples;
- alterações repetitivas;
- configuração fechada;
- geração de arquivos segundo especificação;
- validações objetivas extensas.

Princípios:

```text
HIGH_TIER_REASONING
!=
HIGH_TIER_MATERIALIZATION

DECISION_OWNER
!=
PHYSICAL_WRITER

ROOT_CAN_MATERIALIZE
!=
ROOT_SHOULD_MATERIALIZE

ROOT_FINAL_REVIEW
!=
ROOT_MUST_AUTHOR_THE_DELTA

DELEGATING_MATERIALIZATION
!=
ROOT_DEESCALATION
```

O ROOT de tier alto pode permanecer responsável pela atividade enquanto um tier
inferior executa materialização fechada.

Classificar:

```text
COGNITIVE_MECHANICAL_SPLIT = PRESENT | ABSENT
```

A materialização só pode ser delegada quando:

```text
DECISIONS_CLOSED = YES
SEMANTICS_CLOSED = YES
INVARIANTS_CLOSED = YES
SCOPE_BOUNDED = YES
OWNERSHIP_CLEAR = YES
UNRESOLVED_MATERIAL_CHOICES = NONE
HANDOFF_CONTRACT_IS_NARROW = YES
LOWER_TIER_CAN_MATERIALIZE_WITHOUT_INTERPRETATION = YES
```

e:

```text
EXPECTED_MATERIALIZATION_OFFLOAD_GAIN
>
HANDOFF_COST
+ CONTEXT_TRANSFER_COST
+ RECONCILIATION_COST
+ EXPECTED_REWORK_COST
```

Se passar:

```text
PREFER_SEQUENTIAL_MULTIAGENT = YES
```

Fluxo preferencial:

```text
HIGHER_TIER_ROOT
→ THINK / DESIGN / DECIDE / FREEZE CONTRACT

LOWER_TIER_EXECUTOR
→ WRITE / IMPLEMENT CLOSED SPECIFICATION

HIGHER_TIER_ROOT
→ REVIEW / ADJUDICATE / ACCEPT
```

`PREFER_SEQUENTIAL_MULTIAGENT = YES` não torna delegação obrigatória.

Se o delta mecânico for pequeno demais para amortizar handoff:

```text
EXECUTION_MODE = DIRECT
```

continua correto.

#### 8.7.1 Materialization Stop Rule

Se o tier inferior encontrar:

```text
UNPRESCRIBED_CHOICE
SEMANTIC_AMBIGUITY
CONTRACT_CONFLICT
INVARIANT_CONFLICT
AUTHORITY_CONFLICT
ARCHITECTURAL_DECISION
SCIENTIFIC_DECISION
```

deve:

```text
STOP_AFFECTED_SCOPE
RETURN_TO_ROOT
```

O tier inferior não resolve por inferência.

Depois:

```text
ROOT_CLOSES_DECISION
→ FREEZES_UPDATED_CONTRACT
→ LOWER_TIER_MAY_CONTINUE
```

---

## 9. G6 — Material Intelligence Routing Gain

```text
HIGHER_TIER_REQUIRED_FOR_REASONING = YES
AND LOWER_TIER_CAPABLE_OF_BOUNDED_EXECUTION = YES
AND DELEGATED_WORK_IS_OBJECTIVELY_VERIFIABLE = YES
AND HANDOFF_SCOPE_IS_CLEAR = YES
AND EXPECTED_COST_SAVING > COORDINATION_OVERHEAD
→ MULTIAGENT_ALLOWED
```

Inteligência cara deve permanecer no hotspot cognitivo.

Trabalho bounded e verificável deve ser avaliado para tier inferior.

Entretanto:

```text
G6_TECHNICALLY_ELIGIBLE
!=
G6_ECONOMICALLY_JUSTIFIED
```

Antes de converter G6 em `MULTIAGENT`, também exigir:

```text
OFFLOAD_MATERIALITY_GATE = PASS
```

Quando houver hotspot cognitivo seguido de materialização fechada, avaliar
explicitamente:

```text
COGNITIVE_MECHANICAL_SPLIT_GATE = PASS | FAIL
```

Sem materialidade suficiente:

```text
EXECUTION_MODE = DIRECT
```

mesmo que um tier inferior seja perfeitamente capaz de executar a etapa.

---

## 10. Redundancy Gate

Antes de criar subagente:

```text
DOES_ROOT_ALREADY_COVER_THIS_ROLE_SUFFICIENTLY?
```

Se sim, exigir pelo menos um:

```text
INDEPENDENCE_REQUIRED = YES
DISTINCT_SPECIALIZATION_GAIN = YES
MATERIAL_ECONOMIC_GAIN = YES
MATERIAL_RISK_REDUCTION = YES
```

Senão:

```text
DO_NOT_SPAWN
```

Regra:

```text
DO_NOT_DUPLICATE_EXPENSIVE_INTELLIGENCE_WITHOUT_DISTINCT_VALUE
```

---

## 11. Papéis preferenciais

```text
SCOUT                  = LUNA / HIGH / READ_ONLY
RESEARCHER             = LUNA / XHIGH / READ_ONLY
VALIDATOR              = LUNA / HIGH / VALIDATION
TRIAGE_ANALYST         = LUNA / XHIGH / READ_ONLY
MECHANICAL_IMPLEMENTER = LUNA / HIGH / WORKSPACE_WRITE_BOUNDED
SCRIBE                 = LUNA / HIGH / DOCUMENTATION_BOUNDED
IMPLEMENTER            = TERRA / MEDIUM_OR_HIGH / WORKSPACE_WRITE
REVIEWER               = TERRA / HIGH / READ_ONLY
SECURITY_REVIEWER      = TERRA / HIGH / READ_ONLY
ARCHITECTURE_REASONING = MODEL_BY_CAPABILITY_CLASS / EFFORT_BY_DELIBERATION_CLASS
```

Arquitetura não seleciona `Sol / High` automaticamente.

Quando o `SOL_GATE` passar e o ambiente utilizar um perfil registrado fixo como
`sol_architect`, respeitar a configuração efetivamente disponível desse perfil.
Se o ambiente permitir selecionar esforço de Sol para o ROOT ou para um perfil
compatível, aplicar `D1 → Low`, `D2 → Medium`, `D3-D4 → High`.

```text
ARCHITECTURAL_ROLE
!=
AUTOMATIC_SOL_HIGH
```

Disponibilidade real deve ser confirmada no ambiente.

### 11.1 Mechanical Implementer

Somente quando:

```text
SOLUTION_CLOSED = YES
INVARIANTS_CLOSED = YES
SCOPE_BOUNDED = YES
OWNERSHIP_CLEAR = YES
OBJECTIVE_VALIDATION_AVAILABLE = YES
MATERIAL_NET_GAIN = YES
```

### 11.2 Implementer

Use Terra quando ainda houver:

- julgamento técnico;
- integração;
- interpretação local;
- escolhas de implementação;
- entendimento de fluxo.

### 11.2.1 Scribe

```text
SCRIBE_RECORDS_DECISIONS
SCRIBE_DOES_NOT_CREATE_DECISIONS
```

`luna_scribe / High` é preferido para materialização documental bounded quando
o conteúdo já foi decidido por um ROOT suficiente.

Pode executar:

- documentação factual;
- `PROJECT_STATE`;
- roadmap;
- sprints;
- changelog;
- atualização de referências;
- reconciliação textual factual;
- formatação de conteúdo normativo já fechado;
- materialização física de uma Authority já definida.

Materialização física de Authority é permitida somente quando:

```text
AUTHORITY_PHYSICAL_AUTHORING_BY_SCRIBE = ALLOWED

ONLY_IF:

NORMATIVE_CONTENT_CLOSED = YES
DECISIONS_CLOSED = YES
INVARIANTS_CLOSED = YES
STRUCTURE_DEFINED = YES
UNRESOLVED_SEMANTIC_CHOICES = NONE
OWNERSHIP_CLEAR = YES
```

O Scribe pode **escrever uma decisão já tomada**.

O Scribe não pode **inventar a decisão**.

Se encontrar qualquer escolha material não prescrita:

```text
STOP_AFFECTED_SCOPE
RETURN_TO_ROOT
```

### 11.3 Validator

```text
VALIDATOR_VALIDATES
VALIDATOR_DOES_NOT_IMPLEMENT
VALIDATOR_ELIGIBLE != VALIDATOR_REQUIRED
```

Ferramentas podem gerar artefatos transitórios:

```text
TECHNICAL_WORKSPACE_WRITE_CAPABILITY = ALLOWED_WHEN_REQUIRED
SOURCE_WRITE_AUTHORIZATION = NO
```

#### 11.3.1 Validation Offload Gate

Antes de criar `luna_validator`, exigir:

```text
VALIDATION_OFFLOAD_GATE = PASS
```

O gate só passa se existir volume operacional material ou redução material de
contexto/custo do ROOT.

Sinais favoráveis incluem pelo menos um:

```text
LONG_RUNNING_TEST_SUITE = YES
LARGE_LOG_VOLUME = YES
LARGE_DATASET_SCAN = YES
MANY_INDEPENDENT_VALIDATION_OPERATIONS = YES
ROOT_CONTEXT_POLLUTION_IS_MATERIAL = YES
ROOT_TIME_SAVED_IS_MATERIAL = YES
```

e também:

```text
EXPECTED_VALIDATION_OFFLOAD_GAIN
>
HANDOFF_COST
+ DUPLICATED_CONTEXT_COST
+ RECONCILIATION_COST
```

Se não:

```text
VALIDATION_OFFLOAD_GATE = FAIL
→ ROOT_VALIDATES_DIRECTLY
```

#### 11.3.2 Micro Validation Bundle

As seguintes operações, isoladamente ou em pequeno conjunto, não constituem
ganho material de offload:

```text
MICRO_VALIDATION_BUNDLE =
git status
+ git diff
+ git diff --check
+ git rev-parse
+ git rev-list
+ small TOML parse
+ file existence checks
+ filename / identity checks
+ small registry consistency checks
+ staged scope inspection
```

Regra padrão:

```text
MICRO_VALIDATION_BUNDLE
→ DIRECT_ROOT_EXECUTION
```

Em particular:

```text
ROUTINE_GIT_CHECKS
+
SMALL_CONFIG_PARSE
+
SMALL_FILE_IDENTITY_CHECKS

DO_NOT_CONSTITUTE_MATERIAL_VALIDATION_OFFLOAD_GAIN
BY_THEMSELVES
```

Não criar Validator apenas porque os checks são objetivos.

### 11.4 Reviewer

```text
IMPLEMENTATION_COMPLETE != REVIEWER_REQUIRED
```

Se:

```text
ROOT_CAPABILITY >= REVIEW_REQUIREMENT
AND INDEPENDENT_REVIEW_REQUIRED = NO
```

então:

```text
ROOT_SELF_REVIEW = YES
REVIEWER = NO
```

### 11.5 Triage

```text
TEST_FAIL != TRIAGE_REQUIRED
```

Triage só entra com ganho diagnóstico material.

---

# PARTE IV — SKILLS, PLUGINS E EXECUÇÃO NATIVA

## 12. Taxonomia

```text
CAPABILITY != SKILL
SKILL != PLUGIN
PLUGIN_MAY_CONTAIN_SKILLS = YES
SKILL_MAY_EXIST_WITHOUT_PLUGIN = YES
NAME_SYNTAX_DOES_NOT_DEFINE_CLASS = YES
```

Capacidade nativa = função já disponível diretamente.

Skill = workflow, procedimento ou guidance reutilizável.

Plugin = recurso empacotado que pode fornecer skill, app, template, ferramenta ou integração.

Nenhum transfere authority.

---

## 13. Native-first

```text
NATIVE_EXECUTION = PREFERRED_WHEN_SUFFICIENT

PLUGIN_INSTALLED != PLUGIN_REQUIRED
SKILL_AVAILABLE != SKILL_REQUIRED

USE_ONLY_WITH_MATERIAL_BENEFIT = YES
TOOL_SPRAWL = PROHIBITED
```

Se nativo for suficiente:

```text
NATIVE_EXECUTION_SUFFICIENT = YES
SKILL = NONE
PLUGIN = NONE
```

---

## 14. Skills

Classificar apenas com evidência da superfície/runtime/documentação/catálogo
operacional aplicável.

Sem confirmação:

```text
SKILL_AVAILABILITY = VERIFY_AT_RUNTIME
```

Não inventar Skill.

`NONE` é decisão válida.

---

## 15. Plugins

Plugin só deve ser recomendado quando acrescentar capability material que o
nativo ou a Skill escolhida não fornecem adequadamente.

```text
PLUGIN_USE =
NONE
| OPTIONAL_IF_MATERIAL
| REQUIRED
```

Regra:

```text
PLUGIN_CAPABILITY != WRITE_AUTHORIZATION
CAPABILITY != PERMISSION
```

Se o ambiente exigir ação explícita do usuário para conectar/invocar o Plugin,
o prompt gerador deve informar isso no Card A.

Não inserir no payload do executor instruções sobre Plugins que não serão usados.

---

# PARTE V — FORMATO OBRIGATÓRIO DE SAÍDA

## 16. CARD A — EXECUTION DECISION CARD

Este card é para o usuário.

Deve aparecer no início da resposta do agente que está gerando a atividade.

Deve ser curto.

Formato:

```text
┌─────────────────────────────────────────────────────────────┐
│ EXECUTION CARD — NÃO COPIAR PARA O CODEX/WORK              │
├─────────────────────────────────────────────────────────────┤
│ AMBIENTE            = CODEX | WORK                          │
│ ORCHESTRATOR        = <MODEL> / <EFFORT>                    │
│ EXECUTION_MODE      = DIRECT | MULTIAGENT                   │
│ SUBAGENTS           = <NONE | perfis efetivamente usados>   │
│ FLOW                = <opcional; ex. ROOT → SCRIBE → ROOT>  │
│ SKILL               = <NONE | nome + uso>                   │
│ PLUGIN              = <NONE | nome + uso>                   │
│ NATIVE_EXECUTION    = YES | PARTIAL | NO                    │
│ ESCALATION          = <regra curta>                         │
├─────────────────────────────────────────────────────────────┤
│ COPY_TO_EXECUTOR    = CARD B ONLY                           │
└─────────────────────────────────────────────────────────────┘
```

### 16.1 Rationale no Card A

Adicionar no máximo uma justificativa curta quando materialmente útil.

Exemplo:

```text
RATIONALE =
Terra/High fecha o hotspot; Luna/High executa validação objetiva.
```

Não despejar no card:

- G1–G6;
- rejected alternatives;
- score de risco;
- long model rationale;
- policy history.

### 16.2 Sol/Astra

Se Sol ou Astra forem selecionados, Card A deve acrescentar somente o motivo
mínimo necessário:

```text
ESCALATION_REASON =
<1–2 linhas>
```

A análise completa do gate permanece interna.

---

## 17. CARD B — EXECUTOR PAYLOAD

Este é o único bloco que deve ser enviado ao Codex/Work.

Formato base:

```text
┌─────────────────────────────────────────────────────────────┐
│ EXECUTOR PAYLOAD — COPIAR ESTE BLOCO PARA CODEX/WORK       │
└─────────────────────────────────────────────────────────────┘

AMBIENTE = CODEX | WORK
IDIOMA = pt-BR
ROLE = ROOT_ORCHESTRATOR

OBJETIVO
<resultado concreto>

AUTHORITIES
<somente authorities que o executor precisa consultar>

ESCOPO AUTORIZADO
<ações/arquivos/superfícies permitidos>

NÃO ESCOPO
<somente proibições materialmente plausíveis>

INVARIANTES / CONTRATOS
<somente os necessários>

ATIVIDADE
<passos executáveis>

DELEGAÇÃO
<somente se MULTIAGENT>

VALIDAÇÃO
<comandos e critérios realmente necessários>

GIT / AÇÕES EXTERNAS
<permissões e proibições pertinentes>

STOP CONDITIONS
<condições reais de parada>

RETORNO
<formato mínimo incluindo:
ACTIVITY_COMPLETION_PERCENT = <0-100>%
COMPLETION_BASIS = <quando aplicável>
```

Se uma seção não for relevante:

```text
OMIT_SECTION
```

Não preencher com `NONE` apenas para manter template.

---

## 18. Minimal Payload Rule

O Card B não é um relatório de governança.

É um contrato de execução.

Aplicar:

```text
MINIMUM_SUFFICIENT_EXECUTOR_CONTEXT = REQUIRED
```

O gerador deve procurar remover, não adicionar, informação.

Antes de finalizar:

```text
FOR_EACH_PARAGRAPH:
    DOES_THIS_CHANGE_EXECUTION?
    IF NO:
        DELETE_OR_MOVE_TO_CARD_A_IF_USER_RELEVANT

    CAN_THIS_BE_EXPRESSED_ONCE_AS_A_HIGHER_LEVEL_BOUNDARY?
    IF YES:
        COLLAPSE_DETAIL
```

O gerador deve preferir uma boundary semântica compacta quando ela preservar o
mesmo comportamento operacional.

Exemplo:

```text
SCIENTIFIC_EXECUTION = OUT_OF_SCOPE
```

é preferível a repetir uma longa lista de operações científicas proibidas quando
todas representam a mesma fronteira e nenhuma exige tratamento individual.

---

## 19. Proibições do Card B

Não inserir automaticamente:

```text
TASK_CLASS
RISK
COGNITIVE_COMPLEXITY
OPERATIONAL_VOLUME
VERIFIABILITY
REVERSIBILITY

ROUTINE_EXECUTION_GATE
SOL_GATE
ASTRA_SELECTION_GATE

PARALLEL_INDEPENDENT_FRONTS
DISTINCT_SPECIALIZATION_REQUIRED
MATERIAL_DECOMPOSITION_GAIN
MATERIAL_INTELLIGENCE_ROUTING_GAIN

EXPECTED_MATERIAL_GAIN
COORDINATION_COST
DUPLICATED_CONTEXT_COST

ROOT_CAPABILITY_REDUNDANCY_CHECK
REDUNDANCY_GATE_ANALYSIS

MODEL_SELECTION_REASON
WHY_TERRA_IS_NOT_PREFERRED
WHY_SOL_IS_NOT_PREFERRED

WHY_ROOT_SHOULD_NOT_DO_THIS_WORK
EXPECTED_ECONOMIC_GAIN
```

Esses itens permanecem internos ou no Card A de forma condensada.

Exceção: inserir um deles somente quando seu valor for necessário para uma
decisão que o executor terá de tomar durante a atividade.

---

## 20. Delegação compacta no Card B

Se MULTIAGENT, não repetir um enorme bloco por agente.

Definir primeiro boundaries compartilhados:

```text
SHARED_DELEGATION_BOUNDARIES
- não ampliar escopo;
- não transferir authority;
- não executar Git consequencial sem autorização;
- não delegar recursivamente, salvo regra explícita.
```

Depois cada agente recebe apenas:

```text
SUBAGENT = <profile>
OBJECTIVE = <objetivo estreito>
OWNERSHIP = <arquivos/superfície>
WRITE_MODE = <modo>
RETURN = <evidência mínima>
```

Adicionar `MUST_NOT` individual apenas se existir proibição específica daquele
papel que não esteja coberta pelos boundaries compartilhados.

---

## 21. Authorities compactas

Não copiar documentos canônicos extensos.

Preferir:

```text
AUTHORITIES_TO_READ
1. <path> — ler somente <seção/tema>
2. <path> — usar como authority para <decisão>
```

Se um valor exato for gate:

```text
EXPECTED_VALUE =
<valor>
```

pode ser incluído diretamente.

---

## 22. Background filter

Contexto histórico só entra no Card B se alterar a execução atual.

Não incluir por padrão:

- história da sprint;
- commits antigos sem efeito no baseline atual;
- decisões superadas;
- tentativas anteriores já irrelevantes;
- narrativa de como a arquitetura evoluiu;
- explicações para o usuário compreender o projeto.

Codex/Work precisa de estado operacional atual, não de biografia do projeto.

---

## 23. Negative-boundary filter

Não listar dezenas de proibições genéricas.

Uma proibição entra somente se:

```text
ACTION_IS_PLAUSIBLE_IN_THIS_TASK = YES
OR CONSEQUENCE_IS_HIGH_IF_MISTAKEN = YES
OR GOVERNANCE_REQUIRES_EXPLICIT_BOUNDARY = YES
```

Exemplo:

Se a tarefa é read-only:

```text
SOURCE_WRITE = PROHIBITED
GIT_CONSEQUENTIAL = PROHIBITED
```

pode bastar.

Não é necessário repetir todas as operações impossíveis ou irrelevantes.

Aplicar também:

```text
BOUNDARY_COLLAPSE_RULE =

IF MULTIPLE_PROHIBITIONS_SHARE_THE_SAME_OPERATIONAL_MEANING
AND INDIVIDUAL_ITEMIZATION_DOES_NOT_CHANGE_BEHAVIOR

THEN
COLLAPSE_TO_ONE_HIGH_LEVEL_BOUNDARY
```

O objetivo é preservar segurança sem transformar o Card B em inventário de tudo
que não deve acontecer.

---

## 24. Validation filter

Enviar somente validações necessárias ao executor.

Não explicar no Card B por que cada validação foi escolhida.

Formato preferido:

```text
VALIDATION
1. <comando>
   EXPECTED = <critério>
2. <comando>
   EXPECTED = <critério>
```

Se o ROOT deve interpretar uma divergência:

```text
ON_MISMATCH =
REPORT_AND_ADJUDICATE
```

---

## 24.1 Activity Completion Reporting

Todo prompt relevante para Work ou Codex deve exigir acompanhamento de conclusão
da **atividade específica daquele prompt**.

```text
ACTIVITY_COMPLETION_PERCENT = <0-100>%
```

A porcentagem representa:

```text
PROMPT_ACTIVITY_PROGRESS
```

e nunca:

```text
PROJECT_PROGRESS
SPRINT_PROGRESS
MILESTONE_PROGRESS
ROADMAP_PROGRESS
```

salvo quando o próprio prompt tiver explicitamente uma dessas unidades como sua
atividade integral.

Princípio:

```text
ACTIVITY_COMPLETION_PERCENT
!=
SUCCESS_PERCENT
```

A porcentagem mede quanto da atividade foi efetivamente percorrido/concluído,
independentemente do resultado ser positivo, negativo ou bloqueado.

### 24.1.1 Coerência com STATUS

Aplicar:

```text
STATUS = PASS
→ ACTIVITY_COMPLETION_PERCENT = 100%
```

como regra normal.

Exceção somente se o próprio contrato admitir `PASS` parcial explicitamente,
o que deve ser raro e declarado.

Para bloqueio:

```text
STATUS = BLOCKED
→ ACTIVITY_COMPLETION_PERCENT = <percentual efetivamente concluído antes do blocker>
```

Para falha:

```text
STATUS = FAIL
→ ACTIVITY_COMPLETION_PERCENT = <percentual efetivamente executado>
```

Uma atividade pode terminar:

```text
STATUS = FAIL
ACTIVITY_COMPLETION_PERCENT = 100%
```

quando todas as etapas previstas foram executadas e o resultado final foi
negativo.

Portanto:

```text
100_PERCENT_COMPLETE
!=
PASS
```

### 24.1.2 Base da porcentagem

A porcentagem deve ser derivada do contrato real da atividade.

Usar, conforme aplicável:

- etapas obrigatórias do prompt;
- gates obrigatórios;
- validações previstas;
- entregáveis requeridos;
- ações autorizadas ainda pendentes;
- critérios de aceite já satisfeitos.

Não calcular com base em:

- tamanho do projeto;
- número total de arquivos do repositório;
- número de tokens;
- tempo decorrido;
- impressão subjetiva genérica.

Quando a atividade possuir fases com pesos muito diferentes, o agente pode usar
ponderação razoável, mas deve evitar falsa precisão.

Preferir incrementos coerentes com marcos materiais.

Exemplo:

```text
PREFLIGHT = COMPLETE
INSPECTION = COMPLETE
IMPLEMENTATION = NOT_STARTED
VALIDATION = NOT_STARTED

ACTIVITY_COMPLETION_PERCENT = 40%
```

A política não exige aritmética exata quando o trabalho não possuir decomposição
natural; exige apenas estimativa operacional consistente e explicável.

### 24.1.3 Completion Basis

Sempre que:

- `STATUS != PASS`;
- percentual for inferior a `100%`;
- o cálculo não for autoexplicativo;
- houver blocker;
- houver diferença material entre execução e sucesso;

incluir:

```text
COMPLETION_BASIS =
<breve explicação objetiva do que foi concluído e do que resta>
```

`COMPLETION_BASIS` deve ser curto e factual.

Exemplo:

```text
STATUS = BLOCKED
ACTIVITY_COMPLETION_PERCENT = 65%
COMPLETION_BASIS =
Baseline, inspeção e validação concluídos; implementação não iniciada
devido a conflito de authority.
```

### 24.1.4 Atualizações intermediárias

Quando Work/Codex emitir atualizações de progresso durante uma atividade longa,
incluir o percentual apenas em **marcos materiais**, não a cada comando.

Formato preferido:

```text
PROGRESS_UPDATE
ACTIVITY_COMPLETION_PERCENT = <0-100>%
COMPLETION_BASIS = <breve marco atingido e próximo bloco restante>
```

Não criar cadência artificial por tempo ou quantidade fixa de comandos.

```text
PROGRESS_UPDATE_BY_MATERIAL_MILESTONE = YES
PROGRESS_UPDATE_PER_COMMAND = NO
```

Esta regra não introduz:

```text
BOUNDED_CYCLIC_EXECUTION
WORK_UNITS
CYCLE_LEDGER
STRUCTURED_RETRY_LOOP
```

O percentual é apenas telemetria de conclusão da atividade.

---

## 25. Output contract mínimo

Não exigir relatório gigantesco por padrão.

Formato base:

```text
FINAL_REPORT

STATUS =
ACTIVITY_COMPLETION_PERCENT = <0-100>%
COMPLETION_BASIS = <obrigatório quando aplicável>

FILES_CHANGED =
VALIDATIONS =
FINDINGS =
BLOCKERS =
UNAUTHORIZED_CHANGES = YES | NO
GIT_ACTIONS = NONE | <ações autorizadas realmente executadas>
FINAL_VERDICT =
```

`ACTIVITY_COMPLETION_PERCENT` é obrigatório.

`COMPLETION_BASIS` pode ser omitido somente quando:

```text
STATUS = PASS
AND ACTIVITY_COMPLETION_PERCENT = 100%
AND COMPLETION_STATE_IS_SELF_EXPLANATORY = YES
```

Adicionar outros campos apenas quando materialmente necessários.

---

# PARTE VI — REGRAS DE GERAÇÃO

## 26. Fluxo interno do gerador

1. entender objetivo;
2. identificar authority;
3. pontuar as dimensões de `CAPABILITY_DEMAND`;
4. derivar `CAPABILITY_DEMAND_CLASS = C0-C4`;
5. classificar `DELIBERATION_DEMAND = D0-D4`;
6. classificar `EXECUTION_RISK = R0-R4`;
7. identificar a demanda cognitiva remanescente;
8. escolher `MODEL_FAMILY` pela capability demand;
9. escolher `REASONING_EFFORT` pela deliberation demand;
10. escolher o menor ROOT suficiente;
11. identificar hotspots cognitivos;
12. identificar materialização mecânica;
13. identificar validação objetiva;
14. aplicar `COGNITIVE_MECHANICAL_SPLIT_GATE`;
15. avaliar DIRECT;
16. avaliar multiagente e G6;
17. aplicar `OFFLOAD_MATERIALITY_GATE`;
18. se houver validação delegável, aplicar `VALIDATION_OFFLOAD_GATE`;
19. distinguir `ROOT_MUST_READ_SOURCE_TO_MAKE_DECISION` de `ROOT_MUST_REVIEW_FINAL_DELTA`;
20. aplicar Redundancy Gate;
21. escolher subagentes mínimos;
22. avaliar execução nativa;
23. avaliar Skill;
24. avaliar Plugin;
25. montar Card A;
26. construir Card B aplicando `EXECUTOR_RELEVANCE_TEST`;
27. executar uma `PROMPT_COMPRESSION_PASS`;
28. entregar.

---

## 27. Prompt Compression Pass

Antes de entregar Card B:

```text
PROMPT_COMPRESSION_PASS = REQUIRED
```

Verificar:

```text
DUPLICATED_INFORMATION = REMOVE
INTERNAL_REASONING = REMOVE
REJECTED_ALTERNATIVES = REMOVE
UNUSED_CAPABILITIES = REMOVE
GENERIC_POLICY_TEXT = REMOVE
REDUNDANT_PROHIBITIONS = COLLAPSE
CANONICAL_TEXT_AVAILABLE_BY_PATH = REFERENCE
REPEATED_RATIONALE = REMOVE
NON_ACTIONABLE_HISTORY = REMOVE
MICRO_VALIDATION_DELEGATION = REMOVE_IF_NOT_MATERIAL
SAME_EVIDENCE_READER_DUPLICATION = REMOVE_IF_NO_NET_GAIN
HIGH_LEVEL_BOUNDARY_AVAILABLE = COLLAPSE_DETAIL
```

Executar também:

```text
PROMPT_COMPRESSION_QUESTIONS =

1. O ROOT já precisa ler isso de qualquer maneira?
2. Esta informação muda alguma ação concreta?
3. Esta proibição pode ser resumida por uma boundary superior?
4. Este subagente economiza custo total ou apenas desloca um comando curto?
5. Este bloco repete authority que pode ser referenciada por path?
6. O percentual de conclusão mede esta atividade, e não o projeto inteiro?
7. `STATUS`, percentual e `COMPLETION_BASIS` são coerentes entre si?
8. O ROOT está gastando tier alto para materializar algo já decidido?
9. O tier inferior receberia contrato fechado ou teria de redescobrir a solução?
```

Objetivo:

```text
EVERY_REMAINING_LINE
MUST_HAVE_EXECUTION_VALUE
```

---

## 28. Escalonamento durante execução

Escalar modelo apenas por:

```text
CAPABILITY_GAP
```

Escalar effort apenas por:

```text
DELIBERATION_GAP
```

Falha causada por input, permission, arquivo, tool ou authority ausente não é
capability gap.

Quando o hotspot termina, considerar de-escalonamento.

---

## 29. Review

```text
IMPLEMENTATION_COMPLETE != REVIEWER_REQUIRED
```

Se ROOT cobre review e não existe independência obrigatória:

```text
ROOT_SELF_REVIEW = YES
REVIEWER = NO
```

Independent Reviewer só entra quando independência ou ganho distinto real
justificar.

---

## 30. Triage

```text
TEST_FAIL != TRIAGE_REQUIRED
```

Falha autoexplicativa pode ser tratada diretamente pelo ROOT ou executor
apropriado.

---

## 31. Git e ações externas

Prompt não autoriza implicitamente:

- commit;
- push;
- tag;
- release;
- deploy;
- alteração LIVE;
- publicação;
- exclusão externa;
- mensagem externa.

Incluir no Card B apenas os boundaries pertinentes à atividade.

---

# PARTE VII — EXEMPLOS DE SAÍDA

## 32. Exemplo — DIRECT

```text
┌─────────────────────────────────────────────────────────────┐
│ EXECUTION CARD — NÃO COPIAR PARA O CODEX/WORK              │
├─────────────────────────────────────────────────────────────┤
│ AMBIENTE         = CODEX                                    │
│ ORCHESTRATOR     = TERRA / MEDIUM                           │
│ EXECUTION_MODE   = DIRECT                                   │
│ SUBAGENTS        = NONE                                     │
│ SKILL            = NONE                                     │
│ PLUGIN           = NONE                                     │
│ NATIVE_EXECUTION = YES                                      │
│ ESCALATION       = somente capability gap material          │
├─────────────────────────────────────────────────────────────┤
│ COPY_TO_EXECUTOR = CARD B ONLY                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ EXECUTOR PAYLOAD — COPIAR ESTE BLOCO PARA CODEX/WORK       │
└─────────────────────────────────────────────────────────────┘

AMBIENTE = CODEX
IDIOMA = pt-BR
ROLE = ROOT_ORCHESTRATOR

OBJETIVO
Corrigir o mapeamento localizado já especificado.

ESCOPO AUTORIZADO
- editar o formatter;
- ajustar o teste correspondente se necessário.

VALIDAÇÃO
- executar teste focal;
- executar check estático padrão se aplicável.

GIT / AÇÕES EXTERNAS
- commit/push não autorizados.

RETORNO
- arquivos alterados;
- validações;
- resultado final.
```

---

## 33. Exemplo — MULTIAGENT econômico

```text
┌─────────────────────────────────────────────────────────────┐
│ EXECUTION CARD — NÃO COPIAR PARA O CODEX/WORK              │
├─────────────────────────────────────────────────────────────┤
│ AMBIENTE         = CODEX                                    │
│ ORCHESTRATOR     = TERRA / HIGH                             │
│ EXECUTION_MODE   = MULTIAGENT                               │
│ SUBAGENTS        = luna_worker, luna_validator              │
│ SKILL            = NONE                                     │
│ PLUGIN           = NONE                                     │
│ NATIVE_EXECUTION = YES                                      │
│ ESCALATION       = somente ambiguidade/capability gap       │
├─────────────────────────────────────────────────────────────┤
│ COPY_TO_EXECUTOR = CARD B ONLY                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ EXECUTOR PAYLOAD — COPIAR ESTE BLOCO PARA CODEX/WORK       │
└─────────────────────────────────────────────────────────────┘

AMBIENTE = CODEX
IDIOMA = pt-BR
ROLE = ROOT_ORCHESTRATOR
EXECUTION_MODE = MULTIAGENT

OBJETIVO
Corrigir o cálculo conforme o contrato congelado.

ROOT RESPONSIBILITIES
- fechar a decisão técnica;
- definir invariantes;
- congelar o contrato bounded;
- revisar diff/evidências;
- adjudicar resultado final.

SHARED_DELEGATION_BOUNDARIES
- não ampliar escopo;
- não alterar contrato;
- não executar commit/push;
- não delegar recursivamente.

SUBAGENT = luna_worker
OBJECTIVE = aplicar somente o patch prescrito e testes definidos pelo ROOT.
OWNERSHIP = arquivos explicitamente atribuídos pelo ROOT.
WRITE_MODE = bounded source/test write.
RETURN = diff summary + arquivos alterados.

SUBAGENT = luna_validator
OBJECTIVE = executar validações objetivas e retornar evidências.
OWNERSHIP = validation only.
WRITE_MODE = transient artifacts only; source write prohibited.
RETURN = resultados exatos + blockers.

VALIDAÇÃO
- testes focais;
- suíte aplicável;
- análise estática;
- diff check.

ON_VALIDATION_FAILURE
- reportar ao ROOT;
- não criar Triage automaticamente.

RETORNO
- diff final;
- resultados das validações;
- blockers;
- veredicto do ROOT.
```

---

## 33.1 Exemplo — checkpoint mecânico fechado

Quando uma nova atividade já recebe:

```text
FILES = EXACT
DIFF_ALREADY_REVIEWED = YES
SCOPE_INTEGRITY = PASS
COMMIT_MESSAGE = DEFINED
SEMANTIC_DECISIONS_REMAINING = NONE
VALIDATION = OBJECTIVE
COMMIT_PUSH_AUTHORIZED = YES
```

o roteamento esperado é:

```text
ORCHESTRATOR = LUNA / HIGH
EXECUTION_MODE = DIRECT
SUBAGENTS = NONE
```

O fato de existir `commit` e `push` aumenta a importância dos boundaries de
permission e pós-validação, mas não cria por si só demanda cognitiva para Terra.

Se, na mesma atividade, ainda for necessário classificar arquivos, adjudicar diff,
resolver identidade de policy ou interpretar authority:

```text
ORCHESTRATOR = TERRA / MEDIUM
```

## 33.2 Testes de regressão — Cognitive–Mechanical Split

### Teste A — Authority complexa + reconciliação documental material

Entrada:

```text
ARCHITECTURAL_DECISIONS = OPEN
DOCUMENTATION_DELTA = MATERIAL
```

Esperado:

```text
TERRA / HIGH or XHIGH ROOT
→ closes Authority / decisions / invariants
→ LUNA / HIGH SCRIBE materializes Authority/docs
→ ROOT reviews and adjudicates
```

`MULTIAGENT` é esperado somente se `OFFLOAD_MATERIALITY_GATE = PASS`.

### Teste B — Authority complexa + delta documental mínimo

Entrada:

```text
ARCHITECTURAL_DECISIONS = OPEN
DOCUMENTATION_DELTA = 3 trivial lines
```

Esperado:

```text
ROOT = sufficient higher tier
EXECUTION_MODE = DIRECT
```

Handoff não se paga.

### Teste C — Design fechado + implementação prescrita material

Entrada:

```text
DESIGN_CLOSED = YES
INVARIANTS_CLOSED = YES
IMPLEMENTATION_FILES = 8
IMPLEMENTATION_IS_PRESCRIBED = YES
```

Esperado:

```text
HIGHER_TIER ROOT
→ LUNA / HIGH MECHANICAL_IMPLEMENTER
→ ROOT FINAL REVIEW
```

se o ganho líquido for material.

### Teste D — Implementação ainda contém escolhas técnicas

Entrada:

```text
UNRESOLVED_IMPLEMENTATION_CHOICES = YES
```

Esperado:

```text
DO_NOT_USE_LUNA_WORKER_FOR_DECISION
→ ROOT or TERRA_IMPLEMENTER
```

### Teste E — Luna encontra ambiguidade

Entrada:

```text
LOWER_TIER_ENCOUNTERS_UNPRESCRIBED_CHOICE = YES
```

Esperado:

```text
STOP_AFFECTED_SCOPE
→ RETURN_TO_ROOT
→ ROOT_CLOSES_DECISION
→ LOWER_TIER_CONTINUES_ONLY_WITH_CLOSED_CONTRACT
```

---

# PARTE VIII — PRINCÍPIOS FINAIS

## 34. Regras mestres

1. O gerador pode raciocinar amplamente; o executor recebe contexto estreito.
2. Card A é para o usuário; Card B é para Codex/Work.
3. O usuário copia somente Card B.
4. Escolha ROOT antes de subagentes.
5. Modelo, effort, multiagente, Skill e Plugin são decisões independentes.
6. Luna/Terra são a faixa normal; Sol/Astra exigem gates materiais.
7. `ROOT_CAN_EXECUTE != ROOT_SHOULD_EXECUTE`.
8. Multiagente não exige paralelismo.
9. G6 permite tiering econômico sequencial.
10. Reviewer não é ritual.
11. Triage não é ritual.
12. Validator não implementa.
13. Delegação não transfere authority.
14. Skills e Plugins não transferem authority.
15. Native-first quando suficiente.
16. Skill disponível não implica Skill necessária.
17. Plugin instalado não implica Plugin necessário.
18. Nenhuma informação entra no Card B sem passar pelo `EXECUTOR_RELEVANCE_TEST`.
19. Authority extensa deve ser referenciada por path, não reproduzida.
20. O Card B deve passar por `PROMPT_COMPRESSION_PASS`.
21. O relatório final deve ser mínimo e suficiente.
22. Commit, push, deploy e ações externas exigem autorização explícita.
23. Bounded Cyclic Execution permanece fora desta revisão.
24. Se o ganho de delegação for incerto, permanecer DIRECT.
25. `OBJECTIVE_WORK != DELEGABLE_WORK`.
26. `VALIDATOR_ELIGIBLE != VALIDATOR_REQUIRED`.
27. Microvalidações de Git/config/identity ficam no ROOT por padrão.
28. Se o ROOT precisa consumir a mesma evidência de qualquer forma, penalizar fortemente o handoff.
29. Todo offload exige `OFFLOAD_MATERIALITY_GATE = PASS`.
30. Toda validação delegada exige `VALIDATION_OFFLOAD_GATE = PASS`.
31. Boundaries semanticamente equivalentes devem ser compactadas quando isso não alterar comportamento.
32. `ROOT_BASELINE != ROOT_FLOOR`.
33. Selecionar ROOT pela demanda cognitiva remanescente.
34. `TASK_IS_GOVERNANCE != TERRA_REQUIRED`.
35. `CONSEQUENTIAL_GIT_ACTION != STRONGER_MODEL_REQUIRED`.
36. Luna/High pode ser ROOT de atividade fechada, mecânica e objetivamente verificável.
37. Terra/Medium permanece baseline quando ainda existe julgamento técnico ou normativo real.
38. Mid-task de-escalation só ocorre quando o ganho líquido do handoff for material.
39. `ACTIVITY_COMPLETION_PERCENT` mede somente a atividade específica do prompt.
40. `ACTIVITY_COMPLETION_PERCENT != SUCCESS_PERCENT`.
41. `STATUS = PASS` normalmente implica `ACTIVITY_COMPLETION_PERCENT = 100%`.
42. `STATUS = FAIL` pode coexistir com `ACTIVITY_COMPLETION_PERCENT = 100%`.
43. `STATUS = BLOCKED` deve registrar o percentual efetivamente concluído antes do blocker.
44. `COMPLETION_BASIS` explica objetivamente o que foi concluído e o que resta quando necessário.
45. Atualizações intermediárias de percentual ocorrem por marcos materiais, não por comando.
46. Activity completion reporting não introduz Bounded Cyclic Execution, Work Units ou cycle ledger.
47. `MODEL_FAMILY` é selecionada por `CAPABILITY_DEMAND`.
48. `REASONING_EFFORT` é selecionado por `DELIBERATION_DEMAND`.
49. Authority/validation/review são dimensionados por `EXECUTION_RISK`.
50. Arquitetura e ciência não implicam Sol automaticamente.
51. Dificuldade arquitetural/científica deve ser quantificada antes de escalonamento.
52. Terra/XHigh deve ser considerado antes de Sol quando o gap for de deliberação.
53. Terra/XHigh não deve compensar capability gap real.
54. Sol selecionado não implica Sol/High; effort de Sol é dimensionado separadamente.
55. `HIGH_TIER_REASONING != HIGH_TIER_MATERIALIZATION`.
56. `DECISION_OWNER != PHYSICAL_WRITER`.
57. `ROOT_FINAL_REVIEW != ROOT_MUST_AUTHOR_THE_DELTA`.
58. `ROOT_MUST_REVIEW_FINAL_DELTA` não constitui duplicated context integral por padrão.
59. Materialização por tier inferior exige decisões, semântica e invariantes fechados.
60. Luna pode escrever uma decisão fechada; Luna não deve inventar a decisão.
61. Ambiguidade material durante materialização retorna ao ROOT.
62. Delegar materialização não significa de-escalonar o ROOT.
63. Cognitive–Mechanical Split continua sujeito a `OFFLOAD_MATERIALITY_GATE`.
64. Se o ganho de Sol/Astra for incerto, usar o menor modelo suficiente.

---

## 35. Estado desta revisão

```text
VERSION = v1.7-R2.4
STATUS = CANONICAL
PREVIOUS_VERSION = v1.7-R2.3
REVISION_TYPE = COGNITIVE_DEMAND_CLASSIFICATION + COGNITIVE_MECHANICAL_SPLIT

CONSOLIDATES_ECONOMIC_MULTIAGENT_ROUTING = YES
CONSOLIDATES_SOL_ASTRA_MODEL_GATES = YES
CONSOLIDATES_SKILL_PLUGIN_NATIVE_TAXONOMY = YES

ANTI_OVERDELEGATION_HARDENING = PRESERVED
OFFLOAD_MATERIALITY_GATE = REQUIRED
VALIDATION_OFFLOAD_GATE = REQUIRED
ROOT_MUST_READ_ANYWAY_PENALTY = INCLUDED
MICRO_VALIDATION_BUNDLE = DIRECT_BY_DEFAULT
ROUTINE_GOVERNANCE_CHECKPOINT = DIRECT_BY_DEFAULT

ROOT_BASELINE_IS_NOT_ROOT_FLOOR = YES
SELECT_ROOT_BY_REMAINING_COGNITIVE_DEMAND = REQUIRED
LUNA_HIGH_ROOT_FOR_CLOSED_MECHANICAL_TASKS = ALLOWED
TERRA_MEDIUM_FOR_UNRESOLVED_JUDGMENT = DEFAULT
CONSEQUENTIAL_GIT_DOES_NOT_FORCE_STRONGER_MODEL = YES
MID_TASK_DEESCALATION_REQUIRES_MATERIAL_NET_GAIN = YES

ACTIVITY_COMPLETION_PERCENT_REQUIRED = YES
COMPLETION_BASIS_REQUIRED_WHEN_APPLICABLE = YES
COMPLETION_MEASURES_PROMPT_ACTIVITY_ONLY = YES
COMPLETION_PERCENT_IS_NOT_SUCCESS_PERCENT = YES
MATERIAL_MILESTONE_PROGRESS_UPDATES = ALLOWED
PER_COMMAND_PROGRESS_UPDATES = NO

CAPABILITY_DEMAND_CLASSIFICATION = C0-C4
DELIBERATION_DEMAND_CLASSIFICATION = D0-D4
EXECUTION_RISK_CLASSIFICATION = R0-R4
SIMPLE_SCORE_SUMMATION = PROHIBITED
PEAK_DIFFICULTY_AND_HIGH_DIMENSION_COUNT = REQUIRED
MODEL_FAMILY_SELECTED_BY_CAPABILITY = YES
REASONING_EFFORT_SELECTED_BY_DELIBERATION = YES
VALIDATION_AUTHORITY_SELECTED_BY_RISK = YES
TERRA_XHIGH_BEFORE_SOL_FOR_DELIBERATION_GAP = YES
SOL_EFFORT_SIZED_AFTER_SOL_GATE = YES

COGNITIVE_MECHANICAL_SPLIT_GATE = REQUIRED_WHEN_APPLICABLE
HIGH_TIER_REASONING_IMPLIES_HIGH_TIER_MATERIALIZATION = NO
SCRIBE_CLOSED_AUTHORITY_MATERIALIZATION = ALLOWED
LOWER_TIER_UNPRESCRIBED_CHOICE = RETURN_TO_ROOT
FINAL_ROOT_REVIEW_IS_FULL_CONTEXT_DUPLICATION = NO
DELEGATING_MATERIALIZATION_IS_ROOT_DEESCALATION = NO

DUAL_AUDIENCE_OUTPUT = YES
EXECUTION_DECISION_CARD = REQUIRED
EXECUTOR_PAYLOAD_CARD = REQUIRED
COPY_ONLY_EXECUTOR_PAYLOAD = YES

EXECUTOR_RELEVANCE_TEST = REQUIRED
PROMPT_COMPRESSION_PASS = REQUIRED
BOUNDARY_COLLAPSE_RULE = INCLUDED
INTERNAL_ROUTING_WORKSHEET_EXPOSED_TO_EXECUTOR = NO

BOUNDED_CYCLIC_EXECUTION = EXCLUDED

READY_FOR_USER_REVIEW = NO
CANONICAL_PROMOTION = PASS
```



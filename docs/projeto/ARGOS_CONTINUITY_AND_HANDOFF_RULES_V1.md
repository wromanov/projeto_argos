# ARGOS — Regras de Continuidade e Handoff de Agentes v1

```text
STATUS = CANONICAL / ACTIVE
DOCUMENT_TYPE = ARGOS_PROJECT_CONTINUITY_AND_HANDOFF_AUTHORITY
PROJECT = ARGOS
LANGUAGE = pt-BR
ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
```

## 1. Finalidade e escopo

Esta é a authority específica do Projeto ARGOS para continuidade do projeto,
handoff entre agentes, descoberta do estado, reconciliação documental e
identificação explícita da próxima atividade.

O `Agent Continuity Standard` e os documentos de continuidade do repositório
continuam vigentes. Esta authority materializa os requisitos próprios do ARGOS
e não substitui o `AGENTS.md`, políticas transversais, authorities de produto,
contratos especializados ou decisões humanas.

## 2. ARGOS Continuity Principle

O estado corrente do Projeto ARGOS deve ser recuperável a partir do próprio
repositório. A retomada correta não pode depender da memória de um agente, de
uma conversa específica, de conhecimento tácito do usuário ou de histórico
externo não preservado.

Um agente novo deve reconstruir o contexto operacional necessário lendo as
authorities vigentes, verificando os fatos de Git diretamente e identificando
decisões, permissões, gates, pendências e a próxima atividade. Não deve inferir
continuação somente pelo histórico do chat ou pela ordem aparente do roadmap.

## 3. Agent Handoff Gate

Uma atividade relevante que altere estado, arquitetura, contrato, fase ou
próxima atividade só está integralmente encerrada quando a documentação
necessária estiver reconciliada e o handoff for recuperável.

```text
CURRENT_STATE_DISCOVERABLE = YES
CURRENT_BASELINE_DISCOVERABLE = YES
LAST_COMPLETED_ACTIVITY_DISCOVERABLE = YES
NEXT_ACTIVITY_DISCOVERABLE = YES
CANONICAL_AUTHORITIES_DISCOVERABLE = YES
OPEN_DECISIONS_DISCOVERABLE = YES
BLOCKERS_DISCOVERABLE = YES
MAJOR_FINDINGS_DISCOVERABLE = YES
DEFERRED_ITEMS_DISCOVERABLE = YES
IMPLEMENTATION_AUTHORIZATION_STATE_DISCOVERABLE = YES
SECURITY_OR_ENVIRONMENT_GATES_DISCOVERABLE = YES_WHEN_APPLICABLE
NEW_AGENT_CAN_RESUME_WITHOUT_CHAT_HISTORY = YES
```

Para `AGENT_HANDOFF_GATE = PASS`, todos os critérios aplicáveis precisam estar
satisfeitos e apoiados por conteúdo local identificável. Um fato ausente,
contradição material não adjudicada ou finding relevante sem destino canônico
mantém o gate em `FAIL` ou `PENDING`; não converter ausência de informação em
`NONE`.

Passar o handoff gate significa que um agente consegue recuperar o estado e
seguir as authorities. Isso não concede autorização para implementar, avançar
fase, operar ambientes ou realizar ações Git consequenciais.

## 4. Relação com a conclusão da atividade

Aplicar proporcionalmente, sem exigir uma atualização extensa para cada
microatividade:

```text
TECHNICAL_WORK_COMPLETE
→ DOCUMENTATION_RECONCILED
→ PROJECT_STATE_UPDATED
→ NEXT_ACTIVITY_EXPLICIT
→ AUTHORITIES_LINKED
→ AGENT_HANDOFF_GATE = PASS
→ MILESTONE_CAN_BE_CONSIDERED_FULLY_CLOSED
```

Marcos normalmente sujeitos a atualização de continuidade:

- encerramento de atividade ou slice relevante;
- mudança de fase ou da próxima atividade;
- decisão arquitetural ou funcional relevante;
- criação, substituição ou mudança de vigência de authority/contrato;
- blocker, finding ou item adiado que afete uma retomada;
- mudança de gate de segurança ou ambiente;
- novo baseline de implementação ou fechamento de fase;
- mudança relevante na estratégia de integração.

Typos, comentários, alterações locais triviais e refatorações sem impacto no
estado não exigem atualização ampla de continuidade.

## 5. Responsabilidade e fonte de cada documento

| Documento | Pergunta que responde | Conteúdo próprio |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Para onde o projeto está indo? | Macrofases, capacidades, dependências relevantes, status macro e referências a authorities detalhadas. |
| `docs/projeto/SPRINTS_ARGOS_V5.md` | Como o trabalho está sendo executado? | Atividades/slices, sequência, status, dependências, próxima atividade e gates. |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Onde o projeto está agora? | Snapshot de branch/baseline, fase, atividade atual/próxima, última atividade concluída, gates, blockers e autorização. |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | O que um agente novo precisa saber para assumir? | Contexto operacional necessário, decisões recentes, riscos, limites, itens adiados, proibições e referências especializadas. |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Onde está cada authority e quem decide cada assunto? | Path, papel, escopo de authority e vigência dos documentos ativos e históricos relevantes. |
| `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | Como iniciar uma nova sessão? | Ordem mínima de leitura, verificação de Git, precedência, descoberta do estado e limites de autorização. |
| ADRs, specs e contratos especializados | Por que e como funciona uma decisão específica? | Detalhe técnico ou funcional de seu domínio, sem cópia integral em resumos gerais. |

## 6. Detail once, reference many

```text
DETAIL_ONCE_REFERENCE_MANY = REQUIRED
```

O documento especializado contém o detalhe completo. Roadmap, sprints,
PROJECT_STATE, continuidade, mapa de documentos e bootstrap registram somente o
status, os invariantes indispensáveis à retomada e o path da authority. Isso
evita `DOCUMENT_DRIFT`, `DUPLICATED_AUTHORITY` e `CONFLICTING_STATUS`.

Exemplo: `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` é a fonte completa do contrato de
imagem; roadmap e sprints registram status/ordem, e documentos de continuidade
resumem o estado e apontam para esse contrato.

## 7. Precedência, conflito e reconciliação

Um agente não resolve conflito documental silenciosamente. Deve:

```text
IDENTIFY → CLASSIFY → REPORT → RESOLVE_THROUGH_AUTHORITY_OR_HUMAN_ADJUDICATION
```

Uma authority especializada vigente prevalece sobre um resumo genérico dentro
de seu escopo. A instrução explícita atual do usuário prevalece conforme os
limites de segurança e do projeto. Git é a fonte dos fatos atuais de branch,
HEAD, divergência, worktree e staging; snapshot documental obsoleto deve ser
marcado e reconciliado, sem adulterar fatos históricos para esconder o
conflito.

Status conflitante não deve ser alterado automaticamente para produzir
aparência de consistência. Se não houver authority ou adjudicação suficiente,
registrar a divergência e manter o gate pendente.

## 8. Contrato mínimo do PROJECT_STATE

O snapshot deve tornar recuperáveis, quando aplicáveis:

```text
PROJECT_ROOT
BRANCH
HEAD
ORIGIN_BASELINE
DIVERGENCE
CURRENT_MACROPHASE
CURRENT_ACTIVITY
LAST_COMPLETED_ACTIVITY
NEXT_ACTIVITY
IMPLEMENTATION_AUTHORIZED
LIVE_AUTHORIZED
ENVIRONMENT_GATES
BLOCKERS
MAJOR_FINDINGS
OPEN_DECISIONS
DEFERRED_ITEMS
CANONICAL_AUTHORITIES
```

Campos irrelevantes ao estado corrente podem ser omitidos. Para fatos Git, o
snapshot informa quando foi verificado e o agente seguinte valida Git
diretamente antes de operações consequenciais.

## 9. Contrato da próxima atividade e autorização

`NEXT_ACTIVITY` deve nomear uma atividade concreta, sua situação e authority;
adicionar pré-requisitos quando aplicável. Evitar descrições vagas como
“continuar desenvolvimento”, “seguir roadmap” ou “próxima sprint”.

```text
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
PREREQUISITES = adjudicação humana e autorização explícita próprias
```

```text
PLANNED != AUTHORIZED
DOCUMENTED != AUTHORIZED
NEXT != STARTED
TECHNICALLY_READY != AUTHORIZED_FOR_IMPLEMENTATION
```

Roadmap, sprint, checkpoint documental ou status de prontidão não concede
autorização. O estado de implementação, LIVE e ambiente deve ser explícito.

## 10. Integração incremental

Preservar a sequência canônica:

```text
IMPLEMENT → INTEGRATE → VALIDATE → CLOSE
BIG_BANG_INTEGRATION = PROHIBITED
```

Quando aplicável, a continuidade registra qual vertical slice foi fechada,
qual `INTEGRATION_GATE` passou, integrações pendentes e se existe
implementação órfã. Um módulo isolado não equivale a feature concluída.
Detalhes seguem as authorities de integração e de produto correspondentes.

## 11. Recuperação por novo agente

O agente novo deve, nesta ordem:

1. validar repo root, branch, HEAD, origem, divergência, worktree e staging;
2. ler `AGENTS.md` e `ACTIVE_DOCUMENT_MAP.md`;
3. ler `PROJECT_STATE.md` e `AGENT_CONTINUITY.md`;
4. ler roadmap e sprint no nível necessário;
5. ler a authority especializada da atividade atual ou planejada;
6. comparar fontes, reportar divergências e identificar decisões, findings,
   blockers, itens adiados, gates e estado de autorização;
7. só então propor ou executar ações dentro da autorização explícita vigente.

```text
DO_NOT_RESUME_FROM_CHAT_MEMORY_ONLY = YES
DO_NOT_ASSUME_IMPLEMENTATION_AUTHORIZATION = YES
```

## 12. Document quality gate

Antes de declarar o handoff completo, executar a revisão documental mental:

```text
CAN_NEW_AGENT_IDENTIFY_CURRENT_STATE = YES
CAN_NEW_AGENT_IDENTIFY_LAST_COMPLETED_ACTIVITY = YES
CAN_NEW_AGENT_IDENTIFY_NEXT_ACTIVITY = YES
CAN_NEW_AGENT_FIND_RELEVANT_AUTHORITIES = YES
CAN_NEW_AGENT_IDENTIFY_OPEN_DECISIONS = YES
CAN_NEW_AGENT_IDENTIFY_AUTHORIZATION_STATE = YES
CAN_NEW_AGENT_RESUME_WITHOUT_CHAT_HISTORY = YES
DOCUMENT_QUALITY_GATE = PASS
```

As respostas `YES` exigem referências e fatos recuperáveis no checkout, não
apenas um status afirmado sem fonte. A revisão não substitui a reconciliação
entre authorities nem os gates de segurança e autorização.

## 13. Reconciliar antes de criar branch de desenvolvimento

```text
POLICY_ID = ARGOS-RECONCILE-BEFORE-BRANCH
BRANCH_CREATION_DEFAULT = BLOCKED
USER_DECISION = APPROVED
```

Antes de criar uma branch de desenvolvimento, reconciliar a frente anterior
proporcionalmente ao risco: identificar WIP e seu destino, preservar correções
aprovadas, executar testes e gates pertinentes, atualizar o baseline documental
e consolidar o checkpoint Git. A criação ainda exige autorização explícita do
usuário para a atividade correspondente.

Não exigir merge de branches históricas que não contenham mudanças necessárias;
não promover protótipo como implementação; não fazer merge ou cherry-pick
indiscriminado. Quando WIP ou divergência material estiver inacessível ou sem
classificação suficiente, registrar `UNVERIFIED` e bloquear somente o gate
afetado. Não apagar, sobrescrever ou arquivar worktrees históricos como parte
da reconciliação.

# AGENTS.md — Projeto ARGOS

## 1. Finalidade

Este arquivo é o entrypoint e guardrail operacional para agentes do Projeto

ARGOS. Ele resume regras estáveis e aponta para as fontes canônicas; políticas

e contratos detalhados prevalecem em caso de conflito. Não deve evoluir para

uma segunda política extensa.

## 2. Ordem mínima de leitura

Em cada retomada, seguir a sequência definida em
`docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md`,
começando pela validação factual do Git e depois pelo mapa, estado e continuidade.
Ler também, antes de agir:

1. `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`
2. `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`
3. `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`
4. `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md`
5. `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`
6. Policies transversais vigentes:
   - `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md`
   - `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.4.md`
   - `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`
   - `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`
7. Roadmap, sprints e authorities específicas da atividade atual.
Se existir uma política canônica de delegação multiagente, referenciá-la pelo path exato em vez de reproduzi-la.

## 3. Autoridade

- O usuário é a autoridade final sobre produto, escopo, arquitetura, roadmap,
commits, push, LIVE, encerramento de sprint e governança.

- Agentes, modelos e skills não criam authority. Ausência de authority deve ser
explicitada; usar `DEFERRED_NO_AUTHORITY` quando aplicável.

- Falsa authority e falsa capability são proibidas.
## 4. Independência analítica

Não concordar automaticamente. Buscar a melhor solução independente e, quando

material, distinguir `FATO`, `EVIDÊNCIA`, `INFERÊNCIA`, `HIPÓTESE`,

`PREFERÊNCIA`, `RECOMENDAÇÃO` e `DECISÃO`. Seguir a política canônica de

independência analítica.

## 5. Model / Effort / Multiagent / Skills

`MODEL / EFFORT` define capacidade cognitiva; `MULTIAGENT` define estratégia de

execução; `SKILLS / CAPABILITIES` define capacidade especializada. Os eixos

são independentes.

- Usar a menor capacidade suficiente.
- Usar subagentes somente quando houver benefício material; execução direta é
o padrão quando não agregarem valor.

- Skills podem ser `NONE`; nunca inventar skill indisponível.
- Skills não substituem reasoning, gates, revisão ou authority.
- Prompts Codex/Work devem declarar esses eixos conforme as políticas vigentes,
em pt-BR.

## 6. Work / Codex

Escolher o ambiente pela natureza da tarefa. Usar Codex para engenharia,

repositório, testes e Git quando apropriado; usar Work para browser,

persistência, artifacts ou workflows próprios quando houver benefício

material. Regras específicas do ambiente prevalecem.

## 7. Git e segurança

- Confirmar repo root, branch, `HEAD` e worktree antes de operações críticas.
- Fazer staging explícito; nunca usar `git add .`.
- Não executar automaticamente `reset`, `restore`, `clean`, `stash`, `amend` ou
force push.

- Commit e push exigem autorização explícita.
- Nunca expor passwords, master keys, TOTP, recovery codes, tokens ou secrets.
Segredos locais permanecem fora do Git.

## 8. Continuidade

Git é a fonte de verdade para repo root, branch, `HEAD` e worktree.

`docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` é o snapshot lógico/técnico. A documentação canônica

mais recente prevalece sobre memória conversacional; divergências devem ser

investigadas, não reconciliadas silenciosamente.

`ARGOS_CONTINUITY_PRINCIPLE = ACTIVE` e `AGENT_HANDOFF_GATE = ACTIVE`; a
authority específica é `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`.
Não retomar somente pela memória de chat nem presumir autorização de
implementação a partir de roadmap, status ou prontidão técnica.

## 9. Comunicação

Responder em português do Brasil, com comunicação humana e intuitiva primeiro e

estado técnico depois quando útil. Preservar rigor, rastreabilidade e

transparência sobre incerteza.

## 10. Prevalência

`AGENTS.md` é entrypoint/guardrail. Políticas, contratos e demais documentos

canônicos detalhados são a autoridade normativa; este arquivo apenas os resume

e referencia.

Toda atividade formal requer `PROJECT_STATE_UPDATE = PASS` antes de declarar

`ACTIVITY_COMPLETE = YES`.

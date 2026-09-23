# ARGOS — Agent Continuity

STATUS = ACTIVE
DOCUMENT_TYPE = PROJECT_SPECIFIC_CONTINUITY_INSTANCE
CONTINUITY_STANDARD = Agent Continuity Standard v1.0
CONTINUITY_PROTOCOL_PACKAGE = Protocolo Continuidade Projeto Em Andamento Com Novo Agente 2.0
CONTINUITY_ADOPTION_MODE = RETROFIT_REQUIRED
CONTINUITY_RETROFIT_GATE = NOT_PASSED
USER_PROTOCOL_ACTIVATION = APPROVED
PROJECT = ARGOS
LANGUAGE = pt-BR

## 1. Finalidade

Este documento materializa, para o Projeto ARGOS, o protocolo universal de
continuidade entre chats, agentes, máquinas e sessões.

Ele NÃO substitui:
- `AGENTS.md`;
- authorities específicas do projeto;
- políticas transversais canônicas;
- ADRs e roadmap canônicos;
- segurança e gates próprios do ARGOS.

Regra de precedência operacional:

1. instrução explícita atual do usuário;
2. authorities/contratos canônicos específicos do ARGOS;
3. segurança, operação e limites de authority;
4. políticas transversais canônicas aplicáveis;
5. este documento de continuidade;
6. convenções auxiliares.

CAPABILITY != AUTHORITY
DELEGATION != AUTHORITY_TRANSFER
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
CONTINUITY_RECOVERY_GATE = PASS != IMPLEMENTATION_PREFLIGHT = PASS

## 2. Identidade e repositório

PROJECT_ID = ARGOS
PROJECT_PURPOSE = inventário e monitoramento técnico de câmeras
PRIMARY_REPOSITORY = https://github.com/wromanov/projeto_argos.git

LAST_VERIFIED_LOCAL_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
LAST_VERIFIED_BRANCH = master
LAST_VERIFIED_HEAD = 92023b2520573d76a98f4cb647c20699fcd30bfe
LAST_VERIFIED_ORIGIN_MASTER = 079baee48eaaa0a90ef05c320e081363e1941c62
LAST_VERIFIED_DIVERGENCE = HEAD ahead 1 / behind 0
LAST_VERIFIED_WORKTREE = CLEAN
LAST_VERIFIED_STAGING = CLEAN

Observação:
os facts acima são um snapshot da sessão de 22/09/2026. Um novo agente deve
revalidá-los com Git antes de usá-los como facts atuais.

## 3. Governança transversal ativa

As políticas operacionais atuais são:

- `Politica-Prompts-Agente-v1.7-R2.4.md`
- `AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`
- `Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`
- `Independencia-Analitica-Agente-v1.md`

Regras de version hygiene:
- R2.4 substitui operacionalmente R2.3;
- AGENTS R2.1 usa a baseline anterior somente como histórico;
- Skills/Plugins v1.1 substitui v1.0;
- versões superseded não são authorities ativas.

## 4. Continuidade do estado técnico

LAST_COMPLETED_PUBLISHED_ACTIVITY = MON-07
LAST_PUBLISHED_BASELINE = 079baee

MON-08A = PASS
MON-08B_PREVIOUS_IMPLEMENTATION = LOST_WITH_FORMATTED_LOCAL_WORKTREE
MON-08B_REQUIREMENTS = PRESERVED
MON-08B_PREVIOUS_EVIDENCE = HISTORICAL_REFERENCE_ONLY
MON-08B_CURRENT_IMPLEMENTATION = NOT_PRESENT_IN_CURRENT_CLONE
MON-08B_CURRENT_GATE = RECOVERY_REQUIRED

O antigo checkout local foi perdido após formatação do computador. A implementação
MON-08B anterior nunca havia sido staged, commitada ou enviada ao remoto. Portanto,
a evidência antiga não pode ser promovida a PASS da implementação atual.

A implementação histórica reportava:
- 2.300 ativos sintéticos;
- 0 perdas;
- 0 duplicações;
- concorrência configurada = 20;
- máximo observado = 20;
- cenário normal = 2.300 requests/results;
- falha em massa = 4.600 requests/results e 2.300 OFFLINE;
- recuperação = 4.600 requests/results e 2.300 ONLINE;
- 5 testes MON-08B PASS;
- 176 testes focados PASS;
- 700 testes globais PASS.

Esses números são REFERENCE_TARGETS_FOR_RECOVERY, não evidência atual.

## 5. Gates de segurança e operação preservados

SECURITY_GATE_LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS
SECURITY_GATE_HOMOLOGATION = BLOCKED
SECURITY_GATE_DEPLOYMENT = BLOCKED
SECURITY_GATE_PRODUCTION = BLOCKED

LIVE / produção / homologação não são autorizados por este documento.

## 6. Decisões técnicas importantes preservadas

- Monitoramento técnico é separado da situação operacional da câmera.
- Browser/UI nunca executa probes.
- Probes pertencem a execução dedicada/independente do request/response.
- Concorrência deve ser bounded.
- UNKNOWN / ONLINE / OFFLINE são estados estáveis.
- SUSPECT é efêmero e não deve virar quarto estado persistido.
- Stale/freshness é qualificador separado; stale preserva last stable state, mas
  o estado efetivo de leitura é UNKNOWN(stale).
- Monitoramento e captura são desacoplados.
- Credenciais não pertencem a URLs, logs ou documentos de continuidade.
- Exportação CSV/PDF de inventário permanece DEFERRED para sprint final.
- HARDENING_TRANSITION_REAL permanece DEFERRED / NON-BLOCKING.
- HARDENING_SCOPE_BATCH_NPLUS1 permanece DEFERRED / NON-BLOCKING.

## 7. Primeiro comportamento em novo chat/agente

FIRST_RESPONSE_MODE = READ_ONLY_RECOVERY
CONTINUITY_RECOVERY_GATE = NOT_PASSED
USER_CONTINUITY_VALIDATION = PENDING
READY_TO_RESUME_PROJECT = NO

IMPLEMENTATION = PROHIBITED
EDIT = PROHIBITED
STAGE = PROHIBITED
COMMIT = PROHIBITED
PUSH = PROHIBITED
DEPLOY = PROHIBITED
PHASE_ADVANCEMENT = PROHIBITED

READ_FILES = YES
READ_GIT = YES
INSPECT_STATE = YES
VERIFY_FACTS = YES
COMPARE_AUTHORITIES = YES

O novo agente deve:
1. ler `AGENTS.md`;
2. ler este documento;
3. ler `PROJECT_STATE.md`;
4. ler `continuity/ACTIVE_DOCUMENT_MAP.md`;
5. ler as policies canônicas relevantes;
6. revalidar Git;
7. apresentar divergências e itens UNVERIFIED;
8. aguardar validação humana.

## 8. Próxima atividade requerida

NEXT_REQUIRED_ACTIVITY =
MON-08B RECOVERY — READ-ONLY CODE/GIT PREFLIGHT AND RECONSTRUCTION PLAN

A atividade acima NÃO está autorizada automaticamente.
Primeiro deve ocorrer:
- materialização destes artifacts no repositório;
- verificação factual;
- fechamento do `CONTINUITY_RETROFIT_GATE`;
- recuperação em novo chat, quando aplicável;
- autorização própria da atividade.

## 9. Retrofit gate

Este pacote foi gerado para materialização no repositório, mas o gate só pode
mudar para PASS após confirmação factual de que os arquivos estão presentes,
coerentes e legíveis no checkout oficial.

Critérios:

AGENTS_MD_PRESENT = REQUIRED
AGENT_CONTINUITY_PRESENT = REQUIRED
PROJECT_STATE_PRESENT = REQUIRED
NEW_CHAT_BOOTSTRAP_PRESENT = REQUIRED
ACTIVE_DOCUMENT_MAP_PRESENT = REQUIRED
KNOWN_BLOCKERS_RECORDED = YES
KNOWN_DIVERGENCES_RECORDED = YES
NEXT_REQUIRED_ACTIVITY_RECORDED = YES

Até a verificação:
CONTINUITY_RETROFIT_GATE = NOT_PASSED

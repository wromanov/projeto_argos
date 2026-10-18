# Handoff para o agente ARGOS — E3 C V2.1

## Resultado esperado do próximo gate

Reconciliar a direção funcional C e sua baseline visual V2.1 com o **estado REAL** dos contratos e do código E3, sem reabrir a Variante B ou implementar E4. Produzir uma decisão de readiness e, se necessário, levar apenas lacunas materiais para o usuário. **Não presumir autorização de escrita funcional pela aprovação visual.**

## Sequência recomendada

1. **Preflight enxuto:** conferir `AGENTS.md`, diretório atual, branch, HEAD, worktree/WIP e mapa de autoridades do projeto. Preservar alterações não commitadas. Não alterar Git por inferência histórica.
2. **Autoridades técnicas:** ler o contrato de elegibilidade E3 vigente e as regras ratificadas de captura, permissão, HTTP adapter, target policy, resolver de credenciais, jobs e imagem. Localizar a definição real de estados e a informação autorizada para o SSR/endpoint.
3. **Reconciliação visual:** usar `contracts/01...`, `contracts/02...`, HTML C V2.1 e a última versão aprovada do Camera Detail. Não usar o contrato histórico B para desfazer o card branco.
4. **Diagnóstico de lacunas:** identificar se o backend diferencia com segurança temporário/configuração/capability desconhecida/não suportada/job e quem pode ver cada explicação. Não mapear erro HTTP genérico em estado específico por heurística visual.
5. **Verificação estrutural:** inspecionar DOM/CSS/computed styles da seção Django atual. Manter os dois formulários/rotas existentes e suas permissões sem reestruturação desnecessária.
6. **Gate técnico:** registrar decisões pendentes, conflitos ou readiness. Caso o contrato técnico imponha mensagens menos específicas, alinhar copy sem criar novo redesign.
7. **Somente após autorização de implementação:** integrar estados E3 com SSR, acessibilidade e eventuais atualizações JS apoiadas em backend real; preservar layout, sem mudanças globais. Validar testes direcionados e Django real.
8. **Gate visual:** screenshots reais e avaliação humana, separadas dos screenshots do HTML.

## Limites de execução nesta entrega

```text
THIS_HANDOFF = DOCUMENTATION_AND_APPROVED_VISUAL_BASELINE
IMPLEMENTATION_AUTHORIZATION_FROM_HANDOFF = NO
DOMAIN_CONTRACTS_OVERRIDE_MOCK_BEHAVIORS = YES
E4_GALLERY_IMPLEMENTATION = FORBIDDEN
SIDEBAR_CHANGE = FORBIDDEN
TOPBAR_CHANGE = FORBIDDEN
QUICK_DETAIL_CHANGE = FORBIDDEN
HISTORY_CHANGE = FORBIDDEN
GLOBAL_DESIGN_SYSTEM_CHANGE = NOT_AUTHORIZED
GIT_DESTRUCTIVE_ACTIONS = FORBIDDEN
DEPLOY_OR_REAL_CAMERA_ACCESS = NOT_AUTHORIZED
```

## Critérios técnicos posteriores (se a execução for autorizada)

- Renderização SSR apenas de ações/informações autorizadas; autorização backend independente.
- Captura idempotente com estados reais; não criar/duplicar jobs por estado visual.
- Manter upload e sua regra de permissão, CSRF e validação.
- Não expor IP, URLs de snapshot, credenciais, logs sensíveis ou secrets no frontend.
- Não criar botão E4 inerte.
- Proteção do WIP e alterações restritas ao escopo E3.
- Executar testes de autorização, CSRF, elegibilidade, jobs, HTML renderizado, upload, regressões e `git diff --check`.
- Design QA a 100% em 2048×742, 1440×900, 1366×768, 390×844, inclusive mobile, estados de operação única e feedback real.

## Condições de STOP_AND_ESCALATE

- Backend não oferece metadado autorizado indispensável e não há fallback genérico seguro.
- Classificação específica requer disclosure proibido pela política/permissão.
- Introdução do estado implicaria alterar contrato ratificado ou segurança de captura.
- Mudança exigiria tocar sidebar, topbar, Quick Detail, Histórico ou design system global.
- Conflito com WIP/migrations que não possa ser resolvido sem exceder o escopo.

## Resposta mínima ao usuário

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
ACTIVITY = ARGOS-E3-C-V2-1-TECHNICAL-RECONCILIATION
CURRENT_BRANCH =
CURRENT_HEAD =
PREEXISTING_WIP_PRESERVED =
TECHNICAL_CONTRACT_STATUS =
ELIGIBILITY_BACKEND_CAPABILITIES =
SSR_PERMISSION_DISCLOSURE_MATRIX =
MISSING_STATE_SUPPORT =
C_V2_1_VISUAL_BASELINE = APPROVED
B_VARIANT = PROTECTED
DJANGO_C_IMPLEMENTATION = NOT_STARTED | PARTIAL | COMPLETE
IMPLEMENTATION_AUTHORIZATION =
FILES_CHANGED =
DJANGO_TESTS =
VISUAL_QA =
DJANGO_HUMAN_VISUAL_APPROVAL = PENDING
OPEN_FINDINGS =
OPEN_DECISIONS =
E4_STATUS = NOT_STARTED
NEXT_GATE =
```

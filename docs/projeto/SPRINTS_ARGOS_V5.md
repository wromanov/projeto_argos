# ARGOS — Plano Canônico de Sprints e Execução v5

```text
STATUS = CANONICAL
DOCUMENT_TYPE = PROJECT_SPRINT_EXECUTION_MAP
LANGUAGE = pt-BR
ROADMAP_AUTHORITY = docs/projeto/ROADMAP_ARGOS_V5.md
UI_DS_DETAIL_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
REFERENCE_PACKAGE_REPOSITORY_SHA256 = 510D75399A5C2F641DB77EF1AF9C982B8A2B3D9C08B06854073CE16FE028DA14
CURRENT_PHASE = FASE C — Captura manual e gestão de imagens
CURRENT_PHASE_STATUS = EM_ANDAMENTO / IMG-02 COMPLETE / INTEGRATED; UI-1 COMPLETE / INTEGRATED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_DOCUMENT
CURRENT_ACTIVITY = nenhum trabalho de implementação autorizado por este mapa
LAST_COMPLETED_ACTIVITY = IMG-02 + UI-1 — checkpoint de integração paralela
LAST_COMPLETED_ACTIVITY_STATUS = COMPLETE / INTEGRATED
NEXT_CANDIDATES = IMG-03 — Upload manual; UI-2 — Inventory Visual Retrofit
NEXT_CANDIDATES_STATUS = NOT_AUTHORIZED
IMG02_IMPLEMENTATION_AUTHORIZATION = GRANTED_BY_EXPLICIT_USER_INSTRUCTION_FOR_THIS_SLICE_ONLY
IMG-01 = COMPLETE após o checkpoint documental; contrato canônico:
docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md.
Esta ordem registra a próxima atividade, não concede autorização de
implementação nem encerra a Fase C.
ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
UI-0 = COMPLETE / PASS_WITH_FINDINGS (read-only; não concede autorização de implementação)
IMG-02 = COMPLETE / INTEGRATED; COMMIT = ceda8f6
UI-1 = COMPLETE / INTEGRATED; COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
IMG-03 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-2 = NEXT_CANDIDATE / NOT_AUTHORIZED
```

Este é o documento canônico de execução de slices para as atividades futuras
registradas abaixo. O roadmap define direção e macrofases; a especificação de
integração define contratos detalhados. Este documento registra somente ordem,
marcos, dependências e gates de execução. Não duplica a specification.

## 1. Estado e precedência

Este mapa registra status, ordem, dependências e gates das slices. O estado
recuperável entre agentes e o contrato de handoff pertencem a
`docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`.

MON-09 está tecnicamente encerrada. IMG-02 e UI-1 estão COMPLETE / INTEGRATED,
com INTEGRATION_GATE = PASS. IMG-03 e UI-2 são candidatas futuras e permanecem
NOT_AUTHORIZED. Este mapa registra status e sequência; não concede autorização
para avançar uma dessas slices, mudar de fase ou executar em
homologação/produção.

Em caso de divergência:

1. instrução explícita do usuário;
2. contracts e authorities específicos do ARGOS;
3. `ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` para UI-DS;
4. este mapa para ordem e marcos;
5. `ROADMAP_ARGOS_V5.md` para direção de macrofase.

Conflitos devem ser identificados, classificados, reportados e propostos; nunca
resolvidos silenciosamente.

## 2. Fase C — Captura manual e gestão de imagens

Slices vigentes:

```text
IMG-01 — Contrato funcional
IMG-02 — Modelo, storage e proveniência
IMG-03 — Upload manual
IMG-04 — Captura sob demanda
IMG-05 — Processamento independente
IMG-06 — Histórico visual
IMG-07 — Imagem principal
IMG-08 — Segurança e auditoria
IMG-09 — Hardening
```

A Fase C deve fechar o contrato de `CAPTURA_CAMERA` versus `UPLOAD_MANUAL`,
armazenamento, referência, disponibilidade, histórico e estados de erro. O
`CameraQuickDetailPanel` depende de uma consulta canônica de
`LATEST_CAMERA_CAPTURE`; não deve criar uma fonte paralela.

## 3. UI-DS — frente transversal

```text
UI-DS = Integração seletiva do Camera Inventory Design System v1.0.1
```

Estratégia:

```text
SELECTIVE VISUAL RETROFIT
+ SELECTIVE INTERACTION PATTERN ADOPTION
```

`ARGOS CURRENT PAGE COMPOSITION = PRESERVE` e
`DO_NOT_MIGRATE_FRAMEWORKS = YES`. O padrão aprovado
`CameraQuickDetailPanel` adota o papel de inspeção contextual rápida, sem
substituir a página canônica completa da câmera. Seu conteúdo funcional foi
explicitamente aprovado pelo usuário e está registrado em
`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`; VMS não é adotado
e Localização ocupa esse lugar. Não duplicar a especificação aqui.

### UI-0 — Read-only preflight

```text
STATUS = COMPLETE / PASS_WITH_FINDINGS
READ_ONLY = YES
IMPLEMENTATION = NO
STOP_AFTER_REPORT = YES
FINDINGS_DETAIL = docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md
```

O preflight read-only está concluído. Seu escopo cobria descobrir stack,
inventário, layout, filtros,
tabela, seleção, rota canônica,
identificador de câmera, fontes de imagem/status, modelos de loading/error/stale,
tokens, componentes, iconografia, tipografia, responsividade e acessibilidade.

Entregar `PRESERVE`, `ADAPT`, `ADOPT`, `DO_NOT_ADOPT`, `TOKEN_MAPPING`,
`COMPONENT_MAPPING`, `CAMERA_QUICK_DETAIL_PANEL_MAPPING`, `RISKS` e
`PILOT_SCOPE`. UI-0 não altera código, CSS ou dependências.

### UI-1 — Token & Component Adapter Foundation

Introduzir a camada reversível de adapter entre tokens do Design System, tokens
do ARGOS e componentes existentes. Não redesenhar páginas nem substituir
composição. Deve preceder o retrofit visual.

### UI-2 — Inventory Visual Retrofit

Aplicar o piloto no inventário, preservando layout, filtros, busca, sorting,
paginação, query string, seleção e comportamento. Escopo visual: background,
cards, table surfaces, borders, status, buttons, inputs, focus e selection.

### UI-3 — CameraQuickDetailPanel

Integrar ao inventário real o painel funcional aprovado na authority UI-DS,
com seleção real, identificador canônico, resumo e status canônicos,
`LATEST_CAMERA_CAPTURE` conforme disponibilidade contratual, localização e
rota canônica de detalhes completos. VMS permanece `DO_NOT_ADOPT`. UI-3 segue
pendente e não está autorizada por este registro documental.

```text
INTEGRATION_GATE = REQUIRED
DRAWER_OPEN_ALONE = NOT_SUFFICIENT
```

UI-3 depende de `IMG-01` e `IMG-02` para a semântica e o modelo da imagem, e de
`IMG-04`/`IMG-06` quando a captura real e o histórico forem necessários ao
consumidor. `IMG-03` deve continuar separada por proveniência. `IMG-05`,
`IMG-08` e `IMG-09` fornecem limites de processamento, segurança, auditoria,
concorrência, stale e erro.

### UI-4 — Visual / Functional / Accessibility / Interaction QA

Executar depois da integração de UI-3 e dos contratos da Fase C aplicáveis.
Validar visual, funcional, acessibilidade e interação, preservando baseline
before/after, composição, arquitetura da informação, semântica de status,
viabilidade do painel, ausência de regressão e ausência de mudança não
autorizada de stack.

## 4. Ordem recomendada e dependências

```text
IMG-01 = COMPLETE / checkpoint documental
UI-0 = COMPLETE / PASS_WITH_FINDINGS (read-only)
IMG-02 = COMPLETE / INTEGRATED (ceda8f6)
UI-1 = COMPLETE / INTEGRATED (c5928e8)
INTEGRATION_GATE = PASS (d5f1f54)
↓
CANDIDATAS: IMG-03 e UI-2 = NOT_AUTHORIZED
↓
demais slices seguem as dependências canônicas e exigem autorização própria
```

A ordem pode ser refinada por decisão humana quando uma dependência factual
exigir outra sequência, mas não pode transformar integração final em cleanup
rotineiro.

## 5. Gates transversais

### ARGOS Incremental Integration Rule

```text
IMPLEMENT
↓
INTEGRATE INTO CANONICAL FLOW
↓
VALIDATE INTEGRATED
↓
CLOSE SLICE
```

```text
BIG_BANG_INTEGRATION_AT_END = PROHIBITED
INTEGRATION_SPRINT_AS_ROUTINE_CLEANUP = ANTI_PATTERN
```

Nenhuma capability produtiva é `DONE` enquanto estiver isolada. Se uma grande
sprint de integração for necessária ao final de uma fase, as slices anteriores
devem ser reavaliadas como fechadas incorretamente.

### Integration Gate

Aplicar conforme a natureza da slice:

```text
INTEGRATION_GATE = PASS
FEATURE_REACHABLE_FROM_REAL_ENTRYPOINT = YES
FEATURE_USES_CANONICAL_DOMAIN_PATH = YES
FEATURE_PERSISTS_THROUGH_CANONICAL_PATH = YES_WHEN_APPLICABLE
FEATURE_VISIBLE_TO_REAL_CONSUMER = YES
FEATURE_PERMISSION_PATH_INTEGRATED = YES_WHEN_APPLICABLE
FEATURE_AUDIT_PATH_INTEGRATED = YES_WHEN_APPLICABLE
NO_ORPHAN_IMPLEMENTATION = YES
NO_FUTURE_BIG_BANG_INTEGRATION_REQUIRED = YES
```

Não aplicar mecanicamente persistência/auditoria a uma slice visual que não os
possua, mas sempre exigir o caminho real de consumo quando houver consumidor
produtivo.

### Vertical slice

```text
MIGRATION / IMPLEMENTATION UNIT = VERTICAL SLICE
```

Tokens, componentes e painéis não devem ser implementados em trilhas isoladas
para integração posterior. Cada slice deve alcançar o entrypoint, o domínio,
o storage e a UI reais que lhe correspondem, além da validação e do checkpoint.

## 6. Não escopo deste mapa

- não autoriza UI, CSS ou código de aplicação;
- não autoriza instalação de dependências;
- não autoriza mudança de framework;
- não autoriza captura automática ao abrir o painel;
- não autoriza segunda página de detalhes;
- não autoriza duplicação de domain logic;
- não autoriza commit, push, deploy, LIVE ou homologação;
- não autoriza tratar upload manual como captura de câmera;
- não autoriza big-bang integration.

## 7. Authority detalhada

Para qualquer decisão material da UI-DS, consultar:

`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`

Para direção da macrofase e status global, consultar:

`docs/projeto/ROADMAP_ARGOS_V5.md`

Para continuidade entre chats, consultar os quatro documentos em
`docs/Agent-Continuity-Standard-v1.0/continuity/` listados no
`ACTIVE_DOCUMENT_MAP.md`.


## 10. Checkpoint de integração IMG-02 + UI-1

IMG-02 = COMPLETE / INTEGRATED
UI-1 = COMPLETE / INTEGRATED
IMG-02_COMMIT = ceda8f6
UI-1_COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; cameras.test_imagens_read_service 13/13 PASS
IMG-03 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-2 = NEXT_CANDIDATE / NOT_AUTHORIZED
OPEN_DECISIONS = consultar docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md

# ARGOS UI V2 — Visual Contract

- STATUS: P2 CLOSED / PASS, version 2.0.0 pinned
- DESIGN_STRATEGY: CODE_FIRST / STACK_NATIVE / PROTOTYPE_DRIVEN
- VISUAL_DIRECTION: C — ARGOS HYBRID, aprovada; não reabrir nesta atividade
- SCOPE: VISUAL_ONLY
- HUMAN_APPROVAL: PASS

## Precedência de autoridade

| Domínio | Authority |
|---|---|
| Domínio e função | Documentação funcional ARGOS e implementação de domínio vigente |
| Tokens, primitives, componentes compartilhados, patterns, densidade e estados visuais | Design System canônico em static/css/ui-v2/ |
| Composição, hierarquia, agrupamento, layout e uso de componentes | Protótipo executável aprovado por tela |
| Comportamento, permissões, rotas e workflows | Contratos funcionais ARGOS |
| Figma | Informativo, opcional e não canônico |

A implementação produtiva deve conformar ao Design System, ao protótipo aprovado e aos contratos funcionais. Codex SHALL IMPLEMENT THE APPROVED PROTOTYPE. Codex SHALL NOT REDESIGN THE APPROVED PROTOTYPE. Após P3, IMPLEMENTATION_MODE = CONFORMANCE, não DESIGN.

Se o Visual Contract e um protótipo aprovado divergirem, o conflito bloqueia a implementação da tela até adjudicação explícita. Não reconciliar silenciosamente.

## CSS canônico e cascata

A implementação única do Design System é:

- static/css/ui-v2/tokens.css
- static/css/ui-v2/base.css
- static/css/ui-v2/components.css
- static/css/ui-v2/patterns.css

Ordem conceitual: @layer reset, tokens, base, components, patterns, pages, overrides. Cada propriedade deve ter owner previsível; especificidade arbitrária não é mecanismo de resolução.

Todos os nomes novos de componentes usam namespace argos-. Evitar primitives genéricas como .button, .card e .badge enquanto V1 e V2 coexistem. Base contém somente reset mínimo e defaults globais.

### Ownership

- tokens: conceitos transversais com consumidores reais;
- base: box-sizing, defaults de body/tipografia, links, foco e herança de controles;
- components: primitives e componentes compartilhados;
- patterns: composições reutilizáveis;
- pages: composição específica de uma tela, definida somente em protótipo P3 aprovado;
- overrides: exceções explícitas, não aumento oportunista de especificidade.

Nenhuma página redefine componente compartilhado sem variante contratual explícita. Exemplo: usar .argos-button--compact; não criar altura local sob .inventory-page.

## Gates de aprovação humana

P2 fechou com PASS para os gates TOKENS_APPROVED, COMPONENTS_APPROVED, DENSITY_APPROVED, RESPONSIVE_FOUNDATION_APPROVED, INTERACTION_STATES_APPROVED, DOMAIN_STATUS_LANGUAGE_APPROVED, DESKTOP_DENSITY_APPROVED, MOBILE_DENSITY_APPROVED, ACCESSIBILITY_INTERACTION_GATE, LONG_CONTENT_GATE e USER_FOUNDATION_APPROVAL. O usuário confirmou a aprovação visual; ACCESSIBILITY_INTERACTION_GATE cobre apenas a revisão de interação descrita em design-qa.md e não declara conformidade WCAG.

Validação técnica isolada não marca aprovação humana. Para esta foundation, USER_FOUNDATION_APPROVAL = PASS e a versão 2.0.0 está pinada. P3 permanece não iniciado e requer sua própria atividade autorizada.

## Escopo protegido

- Quick Detail permanece APPROVED / PROTECTED; REDESIGN_AUTHORIZED = NO.
- Migração futura de tokens só será permitida sem delta de composição ou interação e preservando a direção visual aprovada. Nenhuma migração ocorre em P2.
- Django Admin permanece INHERITED; redesenho customizado não é padrão.
- Nenhum template produtivo carrega o CSS V2 nesta atividade.

## DS_CHANGE_REQUEST

Para mudanças futuras pós-freeze, usar registro curto com CHANGE, REASON, AFFECTED_COMPONENTS, AFFECTED_SCREENS, VERSION_IMPACT e USER_REAPPROVAL_REQUIRED. O pedido evita drift silencioso; não cria fluxo burocrático.

## Versionamento

Versão aprovada e pinada: 2.0.0, após aprovação humana explícita. Esta decisão fecha P2 e não inicia P3 nem libera integração de UI em templates produtivos.

## Reconciliação para homologação progressiva (2026-10-11)

```text
BASELINE = DS 2.0.2
P5_IMPLEMENTED_VERSION = DS 2.4.0
DS_2_4_0 = RECOMMENDED_TARGET / CANONICAL_ADJUDICATION_PENDING
COMPATIBILITY_GATE = REQUIRED
DESIGN_QA = MANDATORY
```

DS 2.4.0 da fonte P5 é a versão-alvo recomendada para HOM-01, condicionada à
adjudicação canônica, compatibilidade com o baseline de integração escolhido e
Design QA. Esta recomendação não declara 2.4.0 canônica ou aprovada. Não
substituir tokens, estilos ou componentes silenciosamente; aplicar a mudança
somente por decisão registrada e preservar a baseline visual aprovada e
protegida do Quick Detail.

O Design QA obrigatório para homologação está detalhado na seção 20 de
`ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`. Ele exige comparação visual
com referência aprovada, renderização real, registro das diferenças,
correções materiais e aprovação visual humana. Este adendo é um gate futuro;
nenhuma execução de Design QA é afirmada aqui.

## Adendo Camera Detail — apresentação OUT_OF_SCOPE (2026-10-11)

```text
DECISION_ID = ARGOS-CAMERA-DETAIL-OUT-OF-SCOPE-A
USER_APPROVAL = APPROVED
OUT_OF_SCOPE_PRESENTATION = OPTION_A
DS_CANONICAL = 2.0.2
```

Na Camera Detail, o cabeçalho e “Estado atual” exibem o badge técnico
“NÃO MONITORADA” sem contexto auxiliar quando `scope_reason=OUT_OF_SCOPE`.
“Fora do escopo” continua visível no campo semântico “Escopo”. A regra afeta
somente essa apresentação da Camera Detail; payload, projeção MON e
`monitoring.contexto` permanecem intactos. `INCOMPLETE_CONFIGURATION` mantém
seu contexto próprio, e o aviso stale continua único no local já aprovado.

Esta decisão substitui a repetição visual da referência P5 nesse estado, sem
reabrir sua composição nem promover DS 2.4.0 a canônico. A validação visual
integrada e a aprovação humana permanecem gates separados.

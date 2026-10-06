# ARGOS UI V2 — Visual Contract

- STATUS: P2 FOUNDATION APPROVED / PINNED at 2.0.0; current implemented Design System = 2.2.0 locally
- CURRENT_IMPLEMENTED_VERSION: 2.2.0
- TARGET_VERSION: 2.2.0 / IMPLEMENTED LOCALLY via DSCR-UIV2-004; NOT PUBLISHED
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

O estado pinned/read-only permanece. Um DS_CHANGE_REQUEST aprovado registra o
change set, mas não autoriza implementação; execução requer autorização própria.
Mudança não adjudicada não pode ser implementada e um gap que bloqueie a tela não
deve receber workaround local. Capacidade técnica para editar CSS não transfere
authority.

## Versionamento

P2 aprovou e pinou a foundation 2.0.0. A versão implementada corrente foi
promovida a 2.0.1 e, depois, 2.0.2 por DSCRs anteriores. No estado atual:

```text
CURRENT_IMPLEMENTED_VERSION = 2.2.0
TARGET_VERSION = 2.2.0 / DSCR-UIV2-004 / IMPLEMENTED LOCALLY / NOT PUBLISHED
TARGET_VERSION_IMPLEMENTED = YES / local canonical CSS
```

Regra SemVer do ARGOS Design System:

- **PATCH — X.Y.Z+1:** correção backward-compatible do contrato existente, sem
  expansão material de capability pública. Exemplos: selector bug, correção de
  acessibilidade, regressão visual, valor de token ou comportamento existente.
- **MINOR — X.Y+1.0:** nova capability backward-compatible ou extensão pública
  compatível. Exemplos: primitive, shared pattern, variante ou token compatível.
- **MAJOR — X+1.0.0:** mudança incompatível, como remover/renomear primitive,
  variante ou token público, alterar semanticamente o contrato de forma
  incompatível, quebrar markup/classes públicas ou exigir migração estrutural
  incompatível.

`VERSION_IMPACT` reflete a mudança do contrato público, não a quantidade de
arquivos alterados. Muitos arquivos podem continuar PATCH; um primitive público
novo pode exigir MINOR; uma alteração física pequena pode ser MAJOR se quebrar
consumidores.

A promoção 2.1.0 aprovada em DSCR-UIV2-003 foi MINOR e backward-compatible /
aditiva. P5-VR-S1B materializou localmente os quatro changes do DSCR. A promoção
2.2.0 em DSCR-UIV2-004 adiciona a capability `argos-text-kpi`, consumindo o
token existente, sem exigir migração de consumidores. A versão 2.1.0 foi
publicada no checkpoint S1B; a 2.2.0 permanece local até seu checkpoint de
publicação.

# ARGOS-HOM-01-SIDEBAR-ACTIVE-STATE-RECOVERY

Data: 2026-10-12. Implementação inicial pelo root; após instrução do usuário,
reimplementação e validação pelo agente mechanical; registro documental pelo
scribe.

Branch: `codex/hom-v1-integration`
HEAD: `11dcf7db0095416c125f8863ab89a2eef7fb278f`
WIP preexistente preservado. Nenhum commit ou push.

## Causa raiz e auditoria

Dashboard e Inventário carregavam o contexto visual de produção HOM-01. Início,
Governança e Eventos ficavam fora da flag visual HOM-01 e herdavam o shell
legado completo. A divergência, portanto, não se limitava ao estado ativo do
link. A primeira correção, que alinhava apenas o item selecionado, foi
visualmente rejeitada pelo usuário porque o painel lateral e a composição ao
redor continuavam diferentes.

O diagnóstico comparativo anterior à correção integral registrou, entre
Dashboard e Eventos: painel com larguras 232px e 192px; fundos `#182c3a` e
`#123047`; padding `20px 16px` e `0`; gap do conteúdo `24px` e `32px`; links
com larguras 184px e 176px; cores de links inativos `#d0dbe3` e `#afc3d1`.
Essas diferenças explicam por que a correção restrita ao link ativo não
atendia ao objetivo visual.

O partial compartilhado
`templates/components/navegacao_principal.html` já escolhia a rota correta e
definia `aria-current="page"`. As condições de rota e permissões não foram
alteradas.

## Correção integral delimitada

- `templates/base.html`: opt-in visual HOM-01 e carga seletiva do adaptador
  nas rotas de Início, Governança (lista e detalhe) e Eventos; Dashboard e
  Inventário preservam seu contexto HOM-01 existente.
- `templates/components/sidebar.html`: disponibiliza o hint de rolagem nas
  mesmas rotas escopadas.
- `templates/components/navegacao_principal.html`: associa o hint à navegação
  com `aria-describedby` nessas rotas, preservando a seleção ativa já correta.
- `static/css/sidebar-active-recovery.css`: aplica o shell HOM-01 completo
  nessas três áreas — painel, superfície, espaçamentos, links e estados de
  interação — com regras responsivas e de movimento reduzido escopadas pelo
  atributo visual da página.
- `core/test_sidebar_navigation.py`: cobertura das rotas, seleção de um único
  link ativo correspondente e escopo visual.
- `core/test_frontend.py`: mantém as asserções de ausência das folhas globais
  nas rotas HOM-01 e adiciona asserções do opt-in visual, vínculo acessível e
  hint. Outros hunks já presentes no mesmo arquivo pertencem ao WIP
  preexistente.

O pacote global UI V2 não foi ampliado para essas rotas. Não houve alterações
em backend Django, models, views, migrations, permissões, DS 2.0.2, conteúdo
das páginas ou outros componentes. Os arquivos backend previamente modificados
no worktree pertencem ao WIP anterior.

## Validação técnica

- `manage.py check --settings=scripts.localqa.test_settings`: PASS.
- 90 testes PASS nos módulos `core.test_frontend`, `cameras.test_frontend`,
  `cameras.test_governanca_views` e `core.test_sidebar_navigation`.
- `git diff --check`: PASS.
- Os testes usam configuração SQLite isolada e não alteram o banco integrado
  QA.

## Design QA e decisão

```text
INTEGRATED_VISUAL_QA = PASS / cinco rotas reais após reinicialização do Django
CAPTURED_PAGES = Início, Dashboard, Inventário, Governança, Eventos
ACTIVE_LINKS = PASS / exatamente um aria-current="page" e rótulo correspondente por página
ACTIVE_STYLE = PASS / fundo #2563a6; texto e ícone #ffffff; altura 40px; padding 8px 12px; raio 5px; alinhamento central; peso 750
SHELL_STYLE = PASS / painel 232px #182c3a com padding 20px 16px; gap do conteúdo 24px; inativos #d0dbe3
REFERENCE_REGRESSION = PASS / Dashboard e Inventário preservados
DESKTOP_VIEWPORT = 2552x866 CSS pixels; DPR 1; visualViewport.scale 1
RESPONSIVE_VISUAL_QA = NOT_CLAIMED
HUMAN_VISUAL_APPROVAL = APPROVED / user reply: “aprovo” / five current sidebar captures and contact sheet
APPROVAL_SCOPE = INTEGRATED DESKTOP / 2552x866 CSS pixels; no responsive/mobile approval inferred
ACTIVITY_COMPLETE = YES / scope, validations, five-page QA, documentation and human visual approval complete
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §101
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
```

Depois da reinicialização confirmada pelo usuário, as cinco rotas foram
observadas na aplicação integrada real no Edge, em `localhost:8765`, usando a
conta QA existente. A captura e `computed-styles.json` mostram um único link
ativo por página e valores calculados iguais para o shell e o estado ativo nas
cinco páginas. Dashboard e Inventário permanecem corretos. As imagens atuais
evidenciam a composição; a análise de valores vem do JSON computado, não de
inferência apenas pela aparência.

A checagem visual integrada documentada cobre desktop em 2552×866 CSS pixels,
DPR 1 e escala visual 1. Em resposta às capturas atuais e à contact sheet, o
usuário aprovou explicitamente o padrão visual com “aprovo”. O aceite cobre as
cinco páginas na evidência integrada desktop. Embora o adaptador inclua regras
responsivas, esta aprovação não cobre visualização mobile/responsiva.

Esta atividade está completa. HOM-01 permanece `IN_PROGRESS` para os demais
gates; este aceite visual e a conclusão desta correção não encerram HOM-01 nem
liberam HOM-02. A aprovação anterior da composição do Inventário não substitui
nem amplia o escopo do aceite específico destas capturas.

Evidências em `docs/projeto/evidence/sidebar-active-recovery/`:

- `contact-sheet.jpg`
- `inicio-current.png`, `dashboard-current.png`, `inventario-current.png`,
  `governanca-current.png`, `eventos-current.png`
- `computed-styles.json` — valores computados detalhados por página.

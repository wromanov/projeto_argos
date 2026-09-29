# Product Design — design-qa P3-D

```text
ACTIVITY = UI-V2-P3-D
DATE = 2026-09-28
RESULT = PASS_WITH_NON_BLOCKING_SHARED_SHELL_NOTES
DESIGN_QA_COMPLETE = YES
USER_VISUAL_APPROVAL = PENDING
WCAG_CONFORMANCE = NOT_ASSESSED
```

## Escopo e referências

A revisão cobre somente as sete superfícies próprias P3-D. As oito telas Admin permanecem herdadas; não há redesenho nem runtime Admin nesta entrega.

A referência visual disponível é `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`, que registra ARGOS Hybrid, junto ao Design System 2.0.1 propagado pelo patch `8121ed38cc15e1ff6e72cb46bbb2ca865100bce0`. Não há mockup ou captura de referência específica para essas sete páginas; por isso, esta revisão avalia aderência à linguagem visual compartilhada e clareza da composição de cada página, sem alegar equivalência pixel a pixel com telas inexistentes.

A revisão seguiu o fluxo Product Design de inspeção de evidências e comparação visual. Não havia ferramenta de QA de design executável conectada à sessão; os resultados foram registrados neste relatório e nas capturas P3-D.

## Método e evidências

Chrome, zoom 100%, escala de pixel 1, barras de rolagem visíveis. Viewports obrigatórios: 1920×1080, 1440×900, 1366×768 e 390×844. Foram mantidas as duas capturas pré-existentes de Camera Create e adicionadas 51 capturas; o pacote contém 53 PNGs.

| Evidência | Cobertura |
|---|---|
| `docs/prototype/ui-v2/evidence/screenshots/p3-d/` | 28 capturas default (7 telas × 4 viewports) |
| `docs/prototype/ui-v2/evidence/screenshots/p3-d/` | 6 capturas long em 1440×900; 403 não tem fixture longa aplicável |
| `docs/prototype/ui-v2/evidence/screenshots/p3-d/` | 5 capturas error/long e 7 capturas de foco por teclado |
| `docs/prototype/ui-v2/evidence/screenshots/p3-d/` | 2 capturas selected, 4 success e 1 empty |

As duas capturas existentes de `SCR-CAM-CREATE-001` foram preservadas sem sobrescrita: `scr-cam-create-001__1440x900__default__default.png` e `scr-cam-create-001__1920x1080__default__default.png`. O restante usa o nome `<screen-id>__<viewport>__<state>__<fixture>.png`.

## Resultado visual por grupo

| Grupo | Resultado |
|---|---|
| Câmera — criação e edição | Agrupamentos e barras de ação distinguem seções do cadastro. Na edição, valores existentes continuam aparentes e a situação operacional fica como contexto. Seleção personalizada revela o campo correspondente sem deslocar ou sobrepor os demais grupos. |
| Conta — perfil, edição e senha | Perfil separa dados pessoais, dados de conta, grupos e permissões; o estado vazio preserva a hierarquia. A edição comunica os campos mantidos somente para consulta. A página de senha deixa explícito que os campos permanecem vazios e a demonstração não altera credenciais. |
| Login | Composição centrada em um único cartão, com aviso de demonstração e campos diretos. Não foram encontrados SSO, login social, lembrar-me ou recuperação de senha adicionados. |
| Erro 403 | O código e a mensagem significam falta de permissão; não induzem a erro 401, 404 ou 500. “Voltar ao início” é uma ação segura e a página identifica o estado demonstrativo. |
| Densidade e responsividade | Texto longo quebra dentro dos campos e alertas. Nos quatro viewports, os grupos empilham no mobile e não há overflow horizontal do documento nem de `body`. |
| Acessibilidade visual básica | Os sete alvos de foco alcançados por navegação Tab exibem contorno sólido de 3 px. Os controles de ação no conteúdo principal têm pelo menos 44 px de altura no viewport mobile. Rótulos, headings, landmarks e resumos de erro foram conferidos; os erros de campo referenciam texto visível. |

## Notas não bloqueantes

1. A navegação comum é horizontalmente rolável em 390 px; no início do trilho, o item final aparece parcialmente junto à borda até o usuário rolar. O documento continua sem overflow. É comportamento do shell compartilhado e não foi alterado nesta branch familiar.
2. O link de marca comum mede 36 px de altura em 390 px. As ações principais do conteúdo passam a verificação de 44 px. O link de marca pertence à camada compartilhada; fica como observação para o integrador/root, sem bloquear a prontidão técnica P3-D.

Não foram encontrados bloqueadores visuais específicos das sete telas. A revisão humana visual continua pendente; `TECHNICAL_READY_FOR_REVIEW` não equivale a `USER_APPROVED`.

## Verificações reproduzidas

- 28 combinações default e 6 fixtures longas: zero overflow horizontal.
- 7 telas: Design System 2.0.1, um `<main>` e um `<h1>` por página; estados `[hidden]` não têm exibição inline.
- 6 campos condicionais de câmera: abrir/fechar, semântica `required` e foco no campo ao revelar passaram.
- 5 fluxos de erro: resumo visível e erros associados; login comunica rejeição por alerta. Campos de senha ficaram vazios.
- 4 ações de sucesso: feedback local visível, sem requisição de rede ou persistência.
- Perfil empty, campos somente leitura username/cargo/setor e texto/ação do 403 passaram.
- Regra global preserva `hidden="until-found"` (`display:grid` e `content-visibility:hidden`) depois da remoção do workaround local.

```text
PRODUCTION_CHANGED = NO
ADMIN_RUNTIME_CHANGED = NO
P3_D_LOCAL_HIDDEN_WORKAROUND = REMOVED
OPEN_BLOCKERS = NONE
NEXT_GATE = P3-D HUMAN VISUAL REVIEW
```
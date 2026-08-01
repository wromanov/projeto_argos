# Auditoria de front-end — Sprint 4C.1-A

Data: 01/08/2026. Branch: `master`. Commit inicial: `71e234c`.

## Inventário

Foram inventariados 25 templates e 7 arquivos CSS próprios. Não há arquivos JavaScript próprios. O inventário exclui dependências da `.venv`.

Arquivos de apresentação concentram-se em `templates/`, `cameras/templates/`, `core/templates/`, `usuarios/templates/` e `static/css/`.

## Achados confirmados

- A navegação principal é ocultada no CSS responsivo em larguras estreitas.
- Não há skip link, uso consistente de `aria-current` ou região acessível compartilhada para mensagens.
- Há paginação independente em inventário e eventos.
- Há estados vazios e estilos de formulário repetidos entre telas.
- `eventos.css` é excessivamente compactado e há outros templates compactados em uma linha.
- Há seletores legados relacionados a ativo/inativo em `inventario.css`.
- Não há páginas personalizadas 404 e 500 do projeto.
- A categoria SISTEMA não possui badge próprio no CSS de eventos.

## Achados não confirmados nesta etapa

Não foram encontrados CSS inline, JavaScript inline, URLs `javascript:`, filtro `safe`, `autoescape off`, CDN, fontes externas ou JavaScript próprio. As URLs internas são predominantemente reversas do Django.

## Próximas etapas

As etapas B a F tratarão base/navegação, portal e dashboard, inventário/formulários/detalhe, atividades/eventos/governança e páginas de erro. Esta etapa não modificou telas operacionais.

## Entregas desta etapa

- design system compartilhado;
- template tag segura de query string;
- partials de paginação, estado vazio e resumo de erros;
- testes de renderização e documentação inicial.

A validação visual manual fica para quando os componentes forem aplicados às telas.

## Etapa 4C.1-B — Base, autenticação e portal

Arquivos revisados: `templates/base.html`, `core/templates/core/inicio.html`, `usuarios/templates/usuarios/login.html`, `static/css/argos.css`, `static/css/portal.css` e `static/css/autenticacao.css`.

O defeito móvel foi confirmado em `static/css/argos.css`: a regra de `@media (max-width: 700px)` aplicava `display: none` a `.main-navigation`. Ela foi substituída por quebra de linha e rolagem interna da própria navegação, mantendo uma única lista de links disponível.

Foram adicionados skip link, destino do conteúdo principal, identificação de página atual, região acessível de mensagens, menu de usuário responsivo e logout POST preservado. Login e portal receberam estrutura visual e semântica atualizada. A validação visual foi estrutural, por test client e CSS; não houve inspeção humana em navegador nesta sessão.

Pendências para 4C.1-C: dashboard e telas do inventário.

## Etapa 4C.1-C — Dashboard e listagem de câmeras

Arquivos revisados: `core/templates/core/dashboard.html`, `cameras/templates/cameras/lista.html`, `cameras/templates/cameras/partials/_status_badge.html`, `static/css/portal.css`, `static/css/inventario.css`, `core/test_frontend.py` e `cameras/test_frontend.py`.

O dashboard anterior agrupava indicadores de inventário, monitoramento e completude em uma única grade. A nova estrutura separa Inventário, Monitoramento técnico, Qualidade cadastral e Atividade. Os cartões de Produção, Estoque, Desativadas, cadastros completos e incompletos são links integrais para filtros já existentes (`situacao_operacional` e `completude`). IP duplicado, substituições e monitoramento permanecem informativos porque não possuem filtro compatível.

A listagem recebeu breadcrumb, cabeçalho com total, painel de filtros GET com `role="search"`, labels associados e ação segura para limpar filtros. A tabela passou a usar região focalizável, caption, cabeçalhos com `scope`, valores técnicos monoespaçados, badges textuais e ação explícita. A paginação local foi substituída por `components/paginacao.html`, preservando a query string; o vazio usa `components/estado_vazio.html` com ações condicionadas à permissão.

A responsividade reorganiza cartões e filtros, mantendo todas as colunas na tabela com rolagem exclusiva da região. A validação visual humana em navegador permaneceu indisponível nesta sessão; foram executados testes de renderização e validações estruturais de CSS.

Pendências para 4C.1-D: formulários, detalhe de câmera, atividades, eventos e governança permanecem fora desta revisão.
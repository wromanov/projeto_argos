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

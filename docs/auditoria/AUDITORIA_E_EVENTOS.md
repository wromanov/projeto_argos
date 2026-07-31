# Auditoria e eventos do Projeto ARGOS

## Objetivo

O módulo registra ações relevantes de autenticação, câmeras, atividades e perfil em uma trilha append-only. Os eventos não substituem logs técnicos; servem à governança e rastreabilidade funcional.

## Segurança e privacidade

- Eventos não podem ser editados ou excluídos pela aplicação ou pelo Admin.
- Senhas, tokens, cookies, sessões, cabeçalhos e parâmetros de consulta não são armazenados.
- O IP usa exclusivamente REMOTE_ADDR; cabeçalhos encaminhados não são confiados.
- Dados do usuário e da entidade são congelados para preservar o contexto histórico.
- Campos sensíveis são removidos recursivamente antes da persistência.
- A câmera usa PROTECT; o usuário usa SET_NULL, mantendo os dados congelados.

## Acesso

A consulta exige cameras.consultar_eventos. Os perfis padrão recebem apenas view_eventoauditoria e consultar_eventos, nunca permissões de adicionar, alterar ou excluir eventos.

## Eventos cobertos

- Login com sucesso, tentativa não autorizada e logout.
- Atualização de perfil e alteração de senha, sem valores de senha.
- Criação, atualização, ativação e inativação de câmera.
- Criação e atualização de atividade.
- Alterações de câmeras e atividades feitas pelo Django Admin.

## Operação

O painel geral está em /eventos/; o detalhe em /eventos/<id>/; e o histórico por câmera em /cameras/<id>/eventos/. As listas usam paginação de 50 registros e filtros por texto, categoria, origem e período.
## Governança operacional — Sprint 4C

A situação operacional é independente do status técnico. Os eventos atuais são:

- `camera.desativada`: desativação com motivo, data e usuário;
- `camera.reativada`: reativação controlada para Produção ou Estoque;
- `camera.movida_estoque`: movimentação de Produção para Estoque;
- `camera.colocada_producao`: movimentação de Estoque para Produção;
- `camera.substituida`: câmera anterior desativada por substituição física;
- `camera.assumiu_posicao`: substituta em Produção após receber os dados operacionais.

Os códigos `camera.ativada` e `camera.inativada` não são mais emitidos, mas podem permanecer em eventos históricos anteriores à Sprint 4C. Eventos antigos não são alterados.

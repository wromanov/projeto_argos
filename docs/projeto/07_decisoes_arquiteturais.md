# 07 — Decisões Arquiteturais do Projeto ARGOS

Este documento registra decisões que não devem ser revertidas sem justificativa técnica e validação explícita.

---

## ADR-001 — Django como núcleo da aplicação

**Status:** Aceita

O ARGOS utiliza Django como framework principal.

Motivos:

- autenticação;
- permissões;
- ORM;
- forms;
- templates;
- admin;
- migrations;
- testes;
- maturidade.

---

## ADR-002 — Monólito modular antes de microserviços

**Status:** Aceita

O sistema permanece como monólito modular enquanto essa arquitetura atender a escala.

Não criar microserviços apenas por antecipação.

Tarefas assíncronas podem ser separadas em workers sem fragmentar prematuramente o domínio.

---

## ADR-003 — Situação operacional separada de status técnico

**Status:** Obrigatória

Situação operacional:

```text
Produção
Estoque
Desativada
```

Status técnico:

```text
Online
Offline
Não verificado
```

Esses conceitos não podem ser fundidos.

---

## ADR-004 — Sem exclusão física normal de entidades operacionais

**Status:** Obrigatória

Câmeras e históricos principais devem ser preservados.

Preferir:

- desativação;
- substituição;
- auditoria;
- histórico.

---

## ADR-005 — Auditoria imutável

**Status:** Obrigatória

Eventos de auditoria representam fatos históricos.

Não devem ser editáveis ou apagados pela operação normal.

---

## ADR-006 — Governança de situação fora do formulário comum

**Status:** Aceita

A edição normal da câmera não deve alterar diretamente sua situação operacional.

Transições devem ocorrer pelos fluxos:

- mover para produção;
- mover para estoque;
- desativar;
- reativar;
- substituir.

---

## ADR-007 — Design system próprio

**Status:** Aceita

O projeto não utiliza Bootstrap ou Tailwind.

O front-end é baseado em:

- CSS próprio;
- tokens;
- componentes reutilizáveis;
- Django Templates.

---

## ADR-008 — Redesign incremental

**Status:** Aceita

Mudanças visuais devem ocorrer por microetapas.

Exemplo:

```text
4A.1
4A.2
4A.3
```

Cada microetapa exige validação antes da próxima.

---

## ADR-009 — Credenciais criptografadas

**Status:** Planejada / Obrigatória antes da implementação

Senha de câmera:

- não pode ficar em texto aberto;
- não pode aparecer em logs;
- não pode aparecer em templates;
- não pode ser exibida ao perfil Monitoramento.

A chave criptográfica deve ficar fora do banco.

---

## ADR-010 — Monitoramento assíncrono

**Status:** Planejada

Keepalive de aproximadamente 2.300 câmeras não deve executar dentro do ciclo normal de requisição HTTP.

Usar scheduler/worker apropriado.

---

## ADR-011 — Implantação progressiva do keepalive

**Status:** Aceita

Escalonamento:

```text
50
100
500
parque completo
```

A concorrência será ajustada com dados reais.

---

## ADR-012 — Snapshot em recuperação, não em falha

**Status:** Aceita

Snapshot automático ocorre:

```text
Offline -> Online
```

Não ocorre ao entrar Offline.

Também ocorre na primeira detecção Online.

---

## ADR-013 — Rotação de três snapshots automáticos

**Status:** Aceita

Manter:

```text
3 snapshots automáticos mais recentes
```

Snapshot manual protegido não pode ser removido pela rotação.

---

## ADR-014 — PostgreSQL para produção

**Status:** Planejada

A direção de produção é PostgreSQL.

A migração deverá incluir:

- backup;
- restore;
- validação;
- rollback.

---

## ADR-015 — Push nunca automático durante consultoria

**Status:** Aceita

O agente pode orientar commit, mas push requer autorização explícita.

---

## ADR-016 — Organização de testes separada do redesign

**Status:** Aceita

Mudanças estruturais como mover testes para pacotes devem ocorrer em etapa própria.

Não misturar com UI/UX.

---

## ADR-017 — Evidência antes de promoção

**Status:** Obrigatória

Uma mudança só é considerada aprovada quando houver evidência suficiente:

- testes;
- diff;
- status Git;
- validação visual quando aplicável.

---

## ADR-018 — Contrato global e canônico de filtros

**Status:** Aceita

O Sistema Global de Filtros é uma camada de consulta/UX; não altera permissões, modelos, migrations, contratos de auditoria, imutabilidade histórica, regras de substituição, situação operacional, status técnico ou regras de negócio do inventário.

Inventário disponibiliza as facetas status técnico, situação operacional, completude, terminal, tipo, fabricante, VLAN e farm. Terminal, fabricante e farm seguem sujeitos à normalização cadastral; valores stale/legados de facetas textuais podem permanecer visíveis e removíveis. VLAN válida está no intervalo de 1 a 4094.

Eventos disponibiliza pesquisa, categoria, origem, data inicial e data final; categoria e origem são multivaloradas e usam a paginação compartilhada. Substituições disponibiliza pesquisa, data inicial, data final e filtros ativos na lista global; o histórico local de uma câmera deliberadamente não recebe painel de filtros.

Links devem ser construídos a partir de `query_params`, a representação canônica dos filtros aceitos, para que lixo da query original não se propague. `querystring()` e `querystring_sem_valor()` usam essa fonte com fallback para `request.GET`. Enums inválidos são descartados; datas inválidas e períodos invertidos permanecem visíveis e removíveis como estado corrigível da consulta.

---

## ADR-019 (documento autônomo) — Monitoramento de Disponibilidade e Gestão de Imagens

**Status:** Aprovado

A decisão vigente está detalhada em [ADR-019_monitoramento_disponibilidade_gestao_imagens.md](ADR-019_monitoramento_disponibilidade_gestao_imagens.md). Ela estabelece monitoramento futuro por processamento independente da aplicação web, separação obrigatória entre status técnico e situação operacional, e gestão de imagens exclusivamente sob demanda do operador.

As decisões históricas deste índice sobre snapshots automáticos e sua rotação permanecem como registro de evolução, mas foram substituídas para trabalho futuro pelo ADR-019 autônomo. A referência não renumera os identificadores históricos já registrados neste índice.

---

**Qualquer agente que assumir o ARGOS deve respeitar estas decisões como estado arquitetural oficial.**

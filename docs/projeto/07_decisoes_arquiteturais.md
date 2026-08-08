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

**Qualquer agente que assumir o ARGOS deve respeitar estas decisões como estado arquitetural oficial.**

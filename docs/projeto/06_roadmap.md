# 06 — Roadmap histórico do Projeto ARGOS

Atualizado em: 11/08/2026

## Papel deste documento

Este documento preserva o histórico dos roadmaps visuais e funcionais anteriores. A fonte operacional vigente para o trabalho futuro é o [Roadmap ARGOS v5](ROADMAP_ARGOS_V5.md), adotado a partir do rebaseline documental A0.

Requisitos aqui registrados refletem seu contexto original. Em especial, as propostas históricas de snapshots automáticos foram substituídas para o futuro pelo [ADR-019](ADR-019_monitoramento_disponibilidade_gestao_imagens.md); não devem ser lidas como trabalho pendente.

## Fotografia histórica consolidada

Concluídos:

- Fundação do design system.
- Componentização do shell.
- Novo shell operacional.
- Redesign da listagem.
- Consolidação de paginação e resultados.
- Redesign do dashboard.
- Redesign do detalhe da câmera.
- GF — Sistema Global de Filtros.

Baseline pós-GF:

```text
master = origin/master = 84f4bb9
438 testes OK
```

Para a sequência operacional atual, consultar o [Roadmap ARGOS v5](ROADMAP_ARGOS_V5.md).

## Entrega concluída — GF: Sistema Global de Filtros

A frente GF foi concluída, validada e publicada na branch `master`.

O ARGOS possui um contrato global e consistente de filtragem aplicado ao Inventário de Câmeras, Eventos de Auditoria e Histórico Global de Substituições. Foram consolidados filtros multivalorados, chips removíveis, paginação que preserva estado, query string canônica, tratamento de valores inválidos e stale, progressive enhancement e infraestrutura compartilhada.

Roadmap final da frente:

- GF-01 — Discovery global — **CONCLUÍDA**
- GF-02 — Contrato global — **CONCLUÍDA**
- GF-03 — Infraestrutura compartilhada — **CONCLUÍDA**
- GF-04 — Inventário de câmeras — **CONCLUÍDA**
- GF-05 — Eventos — **CONCLUÍDA**
- GF-06 — Substituições — **CONCLUÍDA**
- GF-07 — Hardening global — **CONCLUÍDA**

Validação final: 438 testes executados com sucesso, `python manage.py check` sem issues, nenhuma migration pendente e `git diff --check` aprovado.

Commit de fechamento:

```text
84f4bb9 fix(filtros): canonicalizar parametros globais
```

Status: entrega concluída, publicada e sem pendências BLOCKER ou MAJOR conhecidas.

## Roadmap visual

### Concluído — Visual 1

Novo shell operacional.

Commit:

```text
5100448 feat(frontend): implementar novo shell operacional do ARGOS
```

### Concluído — Visual 2

Listagem responsiva e resultados.

Commits:

```text
51d8250 feat(frontend): redesenhar listagem responsiva de câmeras
22be61b feat(frontend): aprimorar resultados e consolidar paginação
```

### Concluído — Visual 3

Dashboard operacional.

Commit:

```text
5548bd3 feat(frontend): aprimorar hierarquia operacional do dashboard
```

### Concluído — Visual 4A

Detalhe operacional da câmera.

Commit:

```text
6751c68 feat(frontend): redesenhar detalhe operacional da câmera
```

### Histórico — Visual 4B

Cadastro e edição de câmera.

Microetapas:

#### 4B.1

Shell e cabeçalho.

#### 4B.2

Agrupamento dos campos.

#### 4B.3

Validação e responsividade.

### Planejado — Visual 5

Demais formulários operacionais:

- atividades;
- situação;
- desativação;
- reativação;
- substituição.

### Planejado — Visual 6

Demais telas:

- eventos;
- atividades;
- substituições;
- perfil;
- autenticação;
- 403;
- futuras 404/500.

### Planejado — Visual 7

Consolidação final:

- CSS legado;
- classes sem consumidor;
- badges;
- cards;
- breakpoints;
- overflow;
- tokens;
- estados vazios;
- paginação.

## Organização técnica futura

Após o redesign:

- reorganizar testes em pacotes;
- usar `git mv`;
- preservar contagem;
- atualizar CI;
- atualizar documentação.

## Roadmap funcional histórico

### 4D — Credenciais

- criptografia;
- chave fora do banco;
- controle por perfil;
- auditoria;
- sem segredos em logs.

### 4E — RTSP

- configuração;
- composição de URL;
- teste de conexão;
- tratamento por fabricante;
- timeout.

### 4F — Keepalive

Alvo:

```text
~2.300 câmeras
```

Parâmetros iniciais:

```text
08:00 e 18:00
concorrência: 20
tentativas: 2
timeout: 5 s
```

Implantação progressiva:

```text
50 -> 100 -> 500 -> parque completo
```

### 4G — Snapshots

Automático:

```text
Offline -> Online
primeira detecção Online
```

Retenção:

```text
3 automáticos recentes
```

Manual protegido:

```text
não entra na rotação automática
```

### 4H — Importação em lote

- planilha;
- pré-validação;
- preview;
- confirmação;
- erros por linha;
- auditoria.

### 4I — Produção e observabilidade

- PostgreSQL;
- servidor de aplicação;
- estáticos;
- segredos;
- backup;
- RPO/RTO;
- logs;
- monitoramento;
- teste de restauração;
- rollback.

## Ordem recomendada histórica

1. Visual 4B.
2. Visual 5.
3. Visual 6.
4. Visual 7.
5. Organização de testes/documentação.
6. Credenciais.
7. RTSP.
8. Keepalive.
9. Snapshots.
10. Importação.
11. Produção/observabilidade.

Esta sequência foi posteriormente substituída pelo Roadmap ARGOS v5.

---

**Documento histórico. Próxima sequência operacional: [Roadmap ARGOS v5](ROADMAP_ARGOS_V5.md).**

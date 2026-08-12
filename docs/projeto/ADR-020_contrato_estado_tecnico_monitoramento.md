# ADR-020 — Contrato de Estado Técnico do Monitoramento

**Status:** Aprovado
**Data:** 12/08/2026
**Escopo:** MON-01 — formalização do contrato de disponibilidade
**Inteligência recomendada:** 🌎 Terra Alto

## 1. Contexto e autoridade

Este ADR formaliza o contrato de domínio para disponibilidade técnica das
câmeras do Projeto ARGOS. Ele detalha o [ADR-019 — Monitoramento de
Disponibilidade e Gestão de Imagens](ADR-019_monitoramento_disponibilidade_gestao_imagens.md)
e incorpora a discovery local `ARGOS_MON_00_DISCOVERY.txt`.

O contrato é arquitetural e documental. Não implementa worker, probe,
scheduler, histórico de indisponibilidade, migration, infraestrutura ou
alteração de Admin. As decisões humanas aprovadas para MON-01 são vinculantes
para qualquer implementação posterior.

O ADR-019 continua sendo a autoridade sobre o worker independente do ciclo
HTTP, a separação entre status técnico e situação operacional e o
desacoplamento entre monitoramento e imagens. Este ADR não reabre essas
decisões.

## 2. Auditoria do estado atual

Em `cameras/models.py`, `Camera` possui:

| Campo | Semântica observada hoje | Limitação relevante |
|---|---|---|
| `status` | `CharField` nullable/blank com choices `ONLINE` e `OFFLINE` | `NULL` ou vazio funciona como “Não verificado” na UI; `UNKNOWN` não é choice persistido |
| `status_em` | `DateTimeField` nullable, exibido como “Status desde” | não há contrato formal de que represente a confirmação de estado; não deve receber cada probe |
| `ultima_verificacao` | `DateTimeField` nullable | não há produtor automático; o código atual não distingue probe real de heartbeat |
| `situacao_operacional` | `PRODUCAO`, `ESTOQUE` ou `DESATIVADA` | é condição administrativa, não disponibilidade técnica |

O Admin atual ainda permite edição de `status`, `status_em` e
`ultima_verificacao`. Isso é uma lacuna de ownership a ser corrigida antes da
entrada do worker, mas não é alterado nesta tarefa. Esses campos também não
fazem parte da lista atual de campos auditáveis de câmera.

Não existe atualmente model de `Indisponibilidade`, worker, probe, lease,
contador de anti-flapping ou histórico técnico por intervalo.

## 3. Vocabulário normativo

### 3.1 Situação operacional

`situacao_operacional` descreve a condição administrativa da câmera:

- `PRODUCAO`;
- `ESTOQUE`;
- `DESATIVADA`.

Ela não afirma se a câmera está alcançável ou disponível.

### 3.2 Estados técnicos estáveis

O domínio de disponibilidade possui conceitualmente somente estes estados
técnicos estáveis:

- `UNKNOWN`: a câmera é elegível, mas não existe evidência técnica válida e
  suficientemente fresca para afirmar `ONLINE` ou `OFFLINE`;
- `ONLINE`: disponibilidade confirmada pelo contrato homologado de probe e
  pela política de confirmação;
- `OFFLINE`: indisponibilidade confirmada pela política de anti-flapping.

`UNKNOWN` é o estado inicial de uma câmera que entra no escopo e também é a
semântica de ausência de evidência atual suficiente. O texto de UI pode ser
“Não verificado”, mas o valor canônico futuro deve ser explícito.

### 3.3 Estados e condições que não são estados técnicos

- `SUSPECT` é estado interno e efêmero do worker durante confirmação. Nunca é
  estado persistido nem situação operacional exibida para a câmera.
- “Não monitorada” é condição derivada de elegibilidade. Não é `OFFLINE` nem
  `UNKNOWN`.
- `STALE` é propriedade do frescor da evidência. Não é quarto estado técnico e
  nunca é convertido automaticamente em `OFFLINE`.

### 3.4 Resultado de probe

Resultado de probe é uma observação interna, não estado de domínio. Exemplos
de categorias futuras são `SUCCESS`, `TIMEOUT`, `CONNECTION_REFUSED`,
`AUTH_FAILURE`, `PROTOCOL_ERROR`, `CONFIG_ERROR`, `CANCELLED` e
`INCONCLUSIVE`. A lista definitiva e a interpretação por protocolo ficam
adiadas.

Um resultado isolado não altera o estado técnico. A máquina de confirmação
deve classificar uma sequência de resultados segundo a política homologada;
somente a confirmação produz transição de domínio.

## 4. Elegibilidade e escopo inicial

Uma câmera é candidata ao monitoramento quando, cumulativamente:

1. `situacao_operacional == PRODUCAO`; e
2. possui configuração técnica suficiente e válida para o mecanismo futuro de
   monitoramento.

A definição concreta dessa configuração — protocolo, porta, endpoint,
credencial, capacidade por modelo e demais requisitos — pertence à MON-02.

`ESTOQUE` e `DESATIVADA` ficam fora do escopo por padrão e não devem gerar
`OFFLINE` por estarem desconectadas. `PRODUCAO` sem configuração suficiente
também fica fora do escopo operacional, com a condição derivada
“configuração incompleta”; isso não é indisponibilidade de rede.

Não criar automaticamente um booleano `monitoramento_ativo`. A elegibilidade
deve ser derivada da situação operacional e da configuração técnica, evitando
um segundo estado que possa divergir. Um override operacional futuro, se
necessário, deve ser decisão explícita, auditável e separada da situação
operacional; permanece em aberto.

## 5. Estado persistente, frescor e estado efêmero

### 5.1 Estado persistente

O futuro modelo deve persistir o estado técnico estável (`UNKNOWN`, `ONLINE`
ou `OFFLINE`) e os dados necessários às transições relevantes. O valor
persistido representa o último estado estável confirmado, não cada tentativa
de probe.

Para não confundir histórico com afirmação atual, o estado persistido deve ser
lido junto com a frescura da evidência:

- evidência fresca pode sustentar a apresentação de `ONLINE` ou `OFFLINE`;
- evidência stale não deve ser apresentada sem qualificação como disponibilidade
  atual;
- para consultas que exigem a condição atual, `ONLINE`/`OFFLINE` stale deve ser
  tratado conceitualmente como `UNKNOWN (evidência desatualizada)`, sem
  sobrescrever o último estado confirmado;
- tornar a evidência stale não abre nem fecha incidente e não cria `OFFLINE`.

O limiar futuro `stale_after` deve ser configurável e homologado. MON-01 não
define seu valor numérico, intervalo, retry, cooldown ou frequência.

### 5.2 Frescor da evidência

Freshness responde “há quanto tempo existe evidência técnica utilizável para
esta afirmação?”. Ela é distinta de:

- `status_em`, que marca a vigência do estado estável;
- `ultima_verificacao`, que deve representar uma verificação técnica real,
  conforme a recomendação da seção 10;
- heartbeat e saúde do worker, que pertencem à operação do subsistema.

Se o worker parar, atrasar, reiniciar ou perder conectividade com o banco, a
ausência de evidência fresca deve produzir semântica de stale/UNKNOWN, nunca
uma onda de `OFFLINE`.

### 5.3 Estado efêmero

Os elementos abaixo não são estado persistente de domínio da câmera:

- `SUSPECT`;
- contadores de falhas e sucessos;
- janela de confirmação, cooldown e jitter;
- resultado intermediário e latência do probe;
- fila de próximo probe (`next_probe_at`), scheduler e lease, quando
  implementados.

`SUSPECT`, contadores, cooldown, jitter e resultados intermediários pertencem
à coordenação e ao processamento do worker. Scheduler, `next_probe_at`/fila e
lease são estado operacional do subsistema de monitoramento. Conforme a
arquitetura de execução futura, esses elementos podem ser mantidos em memória
ou em armazenamento compartilhado/persistente; MON-01 não decide entre
PostgreSQL, Redis ou outra solução.

Mesmo quando persistidos, nunca se tornam status técnico ou situação
operacional da câmera e não criam `EventoAuditoria` ou `Indisponibilidade`
individual.

## 6. Máquina de estados conceitual

“Fora do escopo” é uma condição lateral de elegibilidade, não um estado
técnico. A máquina técnica é:

```text
                         evidência confirmada
                 +------------------------------+
                 |                              v
fora do escopo ----> UNKNOWN ----------------> ONLINE
       ^               |                         |
       |               | falha confirmada        | falha confirmada
       |               v                         v
       +----------- OFFLINE <--------------------+

ONLINE/OFFLINE/UNKNOWN -- saída do escopo --> fora do escopo
fora do escopo -- volta a ser elegível --> UNKNOWN
```

O desenho acima não significa que uma falha isolada seja transição: entre o
resultado e a seta existe a confirmação anti-flapping. Uma câmera que volta a
ser elegível começa em `UNKNOWN`, mesmo que tenha um `ONLINE` ou `OFFLINE`
histórico anterior.

## 7. Matriz de elegibilidade e apresentação

| ELEGÍVEL | EVIDÊNCIA | ESTADO EFETIVO | UI conceitual |
|---|---|---|---|
| Produção + nunca sondada | nenhuma | `UNKNOWN` | “Não verificado” |
| Produção + sucesso confirmado | evidência válida e fresca | `ONLINE` | “Online” |
| Produção + falha em confirmação | sequência ainda abaixo do limiar | estado estável anterior; se não houver, `UNKNOWN` | não exibir `SUSPECT` como estado operacional; indicar verificação inconclusiva somente como detalhe técnico |
| Produção + falha confirmada | falhas suficientes segundo anti-flapping | `OFFLINE` | “Offline”; incidente aberto |
| Produção + evidência stale | estado anterior sem evidência fresca | último estado persistido, com efetivo atual `UNKNOWN (stale)` | “Evidência desatualizada”; não afirmar disponibilidade atual |
| Estoque | não aplicável | fora do escopo | “Não monitorada” |
| Desativada | não aplicável | fora do escopo | “Não monitorada” |
| Worker parado/atrasado | evidência deixa de ser fresca | último estado preservado; efetivo atual `UNKNOWN (stale)` | “Monitoramento sem evidência fresca”; não marcar todas como Offline |
| Produção + configuração incompleta | não elegível | fora do escopo | “Não monitorada — configuração incompleta” |

Uma câmera fora do escopo pode conservar o último estado técnico apenas como
registro histórico, mas esse valor não pode ser apresentado como condição
atual. Ao retornar ao escopo, o estado efetivo inicial é `UNKNOWN`.

## 8. Matriz de transições e persistência

| ORIGEM | EVENTO | DESTINO | ABRE INCIDENTE? | FECHA INCIDENTE? | MOTIVO | PERSISTE? | OBSERVAÇÃO |
|---|---|---|---|---|---|---|---|
| Fora do escopo | Torna-se elegível | `UNKNOWN` | Não | Não | entrada no escopo | Sim, como inicialização/entrada | não herda `ONLINE`/`OFFLINE` anterior como verdade atual |
| `UNKNOWN` | Sucesso confirmado | `ONLINE` | Não | Não | disponibilidade confirmada | Sim, estado e transição relevante | não captura imagem |
| `UNKNOWN` | Falha confirmada | `OFFLINE` | Sim | Não | indisponibilidade confirmada | Sim, estado e incidente | somente após anti-flapping |
| `ONLINE` | Falha confirmada | `OFFLINE` | Sim | Não | indisponibilidade confirmada | Sim, estado, transição e incidente | uma única indisponibilidade aberta |
| `OFFLINE` | Sucesso confirmado | `ONLINE` | Não | Sim, como `RECUPERADA` | recuperação técnica confirmada | Sim, estado, transição e encerramento | não captura imagem |
| `ONLINE` | Saída do escopo | Fora do escopo | Não | Não, salvo incidente inconsistente já aberto | `SAIU_DO_ESCOPO` | Sim, mudança de elegibilidade | não representa recuperação |
| `OFFLINE` | Saída do escopo | Fora do escopo | Não | Sim, como `SAIU_DO_ESCOPO` | retirada do escopo | Sim, encerramento sem recuperação | não converter para `ONLINE` |
| `UNKNOWN` | Saída do escopo | Fora do escopo | Não | Não | retirada do escopo | Sim, mudança de elegibilidade | não cria indisponibilidade |
| `OFFLINE` | Nova falha confirmada | `OFFLINE` | Não | Não | repetição do mesmo incidente | Não como nova transição | não abrir segundo incidente |
| Qualquer estado estável | Probe inconclusivo | estado estável anterior | Não | Não | evidência insuficiente | Não como transição; pode gerar métrica/log agregado | `INCONCLUSIVE` não é `OFFLINE` |
| Qualquer estado estável | Probe `CANCELLED` por shutdown | estado estável anterior | Não | Não | cancelamento operacional | Não como transição | cancelamento nunca é falha da câmera |
| Qualquer estado estável | Worker stale/parado | último estado persistido + stale | Não | Não | ausência de evidência fresca | somente health/freshness quando definido | nunca gerar Offline em massa |

Falhas ou sucessos intermediários de anti-flapping não aparecem nessa matriz
como transições de domínio. Eles permanecem no estado efêmero até cruzar o
limiar homologado.

## 9. Entrada e saída do escopo

### Entrada

Ao cumprir os critérios de elegibilidade, a câmera entra conceitualmente em
`UNKNOWN`. A entrada não abre indisponibilidade e não reutiliza
automaticamente um estado técnico anterior.

### Saída

Ao deixar de ser `PRODUCAO` ou perder a configuração mínima, o monitoramento
para. A saída:

- não é `ONLINE`;
- não é recuperação técnica;
- não cria nova indisponibilidade;
- encerra eventual incidente aberto com motivo semântico `SAIU_DO_ESCOPO`.

O histórico futuro deve distinguir pelo menos `RECUPERADA` de
`SAIU_DO_ESCOPO`. Outros motivos de encerramento, como substituição,
cancelamento administrativo ou correção de dados, podem ser necessários, mas
ficam em aberto até haver caso operacional e decisão própria.

## 10. Semântica dos campos atuais

### 10.1 `status_em`

A semântica recomendada é “momento em que o estado técnico estável
persistido atualmente foi confirmado e passou a vigorar”. Assim:

- muda em `UNKNOWN -> ONLINE`, `UNKNOWN -> OFFLINE`, `ONLINE -> OFFLINE`,
  `OFFLINE -> ONLINE` e em eventual inicialização explícita de `UNKNOWN`;
- não muda a cada probe;
- não muda apenas porque a evidência ficou stale;
- não representa o início de `SUSPECT` nem heartbeat do worker.

O nome atual é curto e pode ser confundido com o momento da última tentativa.
Esse risco deve ser preservado na documentação e resolvido em mudança futura
de contrato/migration, não por alteração silenciosa agora.

### 10.2 `ultima_verificacao`

O contrato aprovado reserva `ultima_verificacao` para a última verificação
técnica persistida e originada de um probe real concluído e classificado,
excluindo `CANCELLED`. Ela não é heartbeat do worker e não pode receber
timestamp inventado sem probe.

`ultima_verificacao` não precisa ser atualizada a cada probe executado.
Portanto, não deve ser prometida como timestamp exato do último probe que
existiu somente em memória. Freshness deve usar evidência persistida segundo
política futura conservadora; a frequência/amostragem concreta permanece uma
decisão de implementação.

Preserva-se a separação entre último probe executado, última
evidência/verificação persistida e heartbeat do worker. Se futuramente for
necessário conhecer cada último probe executado, isso pertence à
métrica/estado operacional do worker ou a campo específico, sem falsificar
`ultima_verificacao`.

Enquanto o campo atual existir, nenhum código humano deve usá-lo para afirmar
que o worker está vivo sem verificar sua origem e frescor.

## 11. Evolução de `NULL`/vazio para `UNKNOWN`

Recomendação objetiva: adotar `UNKNOWN` como valor canônico explícito do
domínio e exibir “Não verificado” na interface. O estado atual deve ser
tratado como compatibilidade transitória:

1. mapear semanticamente `NULL` e vazio para `UNKNOWN` em consultas, filtros e
   dashboard durante a transição;
2. executar futura data migration que converta ambos para `UNKNOWN`;
3. somente depois endurecer o schema para não nulo e remover a dependência de
   vazio/`NULL`;
4. atualizar choices, Admin, forms, filtros e UI na mesma evolução;
5. preservar dados existentes como “não verificados”, sem inferir `ONLINE` ou
   `OFFLINE` a partir de cadastro, nome ou situação operacional.

Não fazer migration nesta tarefa. A transição explícita melhora filtros,
contagens de dashboard, testes e consultas de elegibilidade, sem afirmar uma
disponibilidade que os dados atuais não comprovam.

## 12. Ownership e auditoria

O subsistema de monitoramento será o único proprietário de:

- `status`;
- `status_em`;
- `ultima_verificacao`;
- futuros campos de evidência, freshness, resultado técnico e transição.

Antes do worker assumir, o Admin deve remover ou restringir a edição manual
desses campos e o serviço de transição deve ser a fonte única de escrita.
MON-01 registra a regra, mas não altera `cameras/admin.py`.

Humanos auditam alterações cadastrais e operacionais, como mudança de
situação, configuração e desativação. O worker registra transições técnicas
confirmadas e incidentes relevantes. Probes individuais, tentativas
intermediárias, `SUSPECT` e cancelamentos não viram trilha de auditoria
funcional.

## 13. Persistência e histórico de indisponibilidade

A persistência oficial é:

- estado técnico estável;
- transições relevantes;
- no máximo uma indisponibilidade aberta por câmera;
- fechamento por `RECUPERADA` ou `SAIU_DO_ESCOPO`, conforme o evento real.

Uma indisponibilidade representa um intervalo confirmado: começa quando a
câmera entra em `OFFLINE` confirmado e termina em `ONLINE` confirmado ou na
saída do escopo. Falhas repetidas durante o mesmo `OFFLINE` não criam novo
registro. Sucessos insuficientes não encerram incidente.

Não haverá histórico de cada probe. `EventoAuditoria`, se futuramente usado
para transições do worker, deverá representar somente a transição confirmada
ou mudança operacional relevante, nunca cada tentativa.

## 14. Worker indisponível e shutdown

Falha, atraso, restart ou ausência do worker é falha do subsistema de
monitoramento. Não é evidência de falha das câmeras. O contrato exige:

- nenhum `OFFLINE` em massa por falta de heartbeat;
- estado anterior preservado enquanto a evidência envelhece;
- apresentação stale/UNKNOWN quando não houver evidência fresca;
- `CANCELLED` inconclusivo e sem transição;
- reidratação sem duplicar incidentes ou encerramentos.

Health do worker e disponibilidade das câmeras são indicadores diferentes e
devem ser apresentados/armazenados separadamente quando implementados.

## 15. Relação com captura de imagem

Nenhuma transição `UNKNOWN`, `ONLINE`, `OFFLINE`, `RECUPERADA`, stale ou saída
do escopo dispara captura automática, snapshot ou importação. Monitoramento e
captura continuam desacoplados conforme o ADR-019. A captura, quando existir,
será fluxo explícito e sob demanda do operador.

## 16. Decisões adiadas

Permanecem deliberadamente fora deste ADR:

- protocolo primário, porta, URL/path, ICMP, TCP, HTTP, RTSP e ONVIF;
- timeout, retries, threshold de falhas/sucessos, cooldown, jitter e
  intervalo;
- concorrência, número de workers, scheduler, polling, SSE e WebSocket;
- credenciais, criptografia, allowlist de rede e catálogo de capacidades;
- PostgreSQL de produção, lease, lock, deployment e supervisão;
- retenção histórica, campos definitivos, migrations e motivos adicionais de
  encerramento;
- implementação de probe, worker, Admin, UI e métricas.

A próxima frente é `MON-02`, responsável por segurança, capacidade técnica e
critérios concretos de elegibilidade/probe.

## 17. Invariantes

As regras abaixo são obrigatórias para qualquer implementação futura:

- **I1.** Situação operacional não é status técnico.
- **I2.** Fora do escopo não é `OFFLINE`.
- **I3.** Worker indisponível não é câmera `OFFLINE`.
- **I4.** `SUSPECT` não é estado persistido.
- **I5.** Probe individual não é transição de domínio.
- **I6.** `OFFLINE` somente após confirmação da política de anti-flapping.
- **I7.** Captura de imagem nunca é consequência automática de transição.
- **I8.** Uma câmera possui no máximo uma indisponibilidade aberta.
- **I9.** Repetição de falha enquanto `OFFLINE` não abre novo incidente.
- **I10.** Saída do escopo fecha eventual indisponibilidade sem classificá-la como recuperação.
- **I11.** Entrada no escopo começa sem assumir disponibilidade atual.
- **I12.** Estado técnico pertence ao subsistema de monitoramento.

## 18. Critério de encerramento de MON-01

MON-01 está documentalmente concluída e aprovada porque o contrato permite
responder, sem escolher protocolo, porta, timeout ou número de workers:

- o que é `ONLINE`, `OFFLINE`, `UNKNOWN`, `SUSPECT` e “não monitorada”;
- quando uma câmera entra e sai do escopo;
- como incidente aberto é encerrado;
- o que stale significa e o que acontece com o worker parado;
- quem possui os campos técnicos;
- quais transições geram histórico;
- por que monitoramento não captura imagens automaticamente.

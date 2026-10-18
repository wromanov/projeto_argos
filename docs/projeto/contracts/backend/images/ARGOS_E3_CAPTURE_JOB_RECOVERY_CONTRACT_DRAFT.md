# ARGOS E3 — proposta de recuperação administrativa de jobs de captura

```text
PROJECT = ARGOS
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
DOCUMENT_TYPE = DIAGNOSTIC_AND_NON_NORMATIVE_PROPOSAL
STATUS = DRAFT
DIAGNOSTIC_AUTHOR = SOL_MEDIUM
HUMAN_APPROVAL = PENDING
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
F02_IMPLEMENTATION = NOT_PERFORMED
RECOVERY_EXECUTION = NOT_PERFORMED
PERSISTENT_QA_DATA_CHANGED = NO
PERSISTENT_QA_MIGRATION = NOT_PERFORMED
```

> Este documento registra diagnóstico read-only e uma proposta para decisão.
> Não é contrato ativo, não altera authorities existentes e não autoriza
> implementação, comando administrativo, recuperação de job, aplicação de
> migration ou acesso a câmera real. Se houver conflito com authority ratificada,
> a authority vigente prevalece e a decisão retorna ao responsável humano.

## 1. Escopo e resultado do diagnóstico

O escopo foi limitado a compreender jobs de captura sem progresso aparente e
descrever opções futuras. Nenhum worker foi executado, nenhuma câmera foi
acessada e nenhuma recuperação foi tentada.

```text
ROOT_CAUSE_OF_CURRENT_QUEUED_JOB = UNKNOWN
WORKER_STOP_EVIDENCE = NOT_ESTABLISHED
CAPTURE_WORKER_EXECUTED = NO
CAMERA_ACCESSED = NO
```

O modelo `CameraCaptureJob` persiste estado e datas, mas não persiste identidade
do worker executor, heartbeat, lease ou fencing token. `_claim_next_job` faz a
transição compare-and-set `QUEUED → RUNNING` e confirma a transação antes de o
trabalho prosseguir fora dela. `run_capture_worker` chama `run_next_capture`,
que consome somente jobs `QUEUED`. Assim, uma interrupção depois do claim pode
deixar um job em `RUNNING`; ausência de consumidor pode deixar um job em
`QUEUED`. O código atual não permite concluir, só por idade, demora observada na
tela ou silêncio de logs, que uma execução foi abandonada.

A tentativa de consulta CIM de processos foi negada. Portanto, não há prova de
que um worker esteja parado. Settings QA com integrações ou monitoramento
desabilitados também não demonstram a ausência de um processo de captura. A
causa do job `QUEUED` observado permanece desconhecida.

## 2. Evidência e limites do snapshot QA

Foi feita inspeção somente leitura do banco SQLite QA usando URI `mode=ro` e
`PRAGMA query_only=ON`. Naquele snapshot específico:

```text
MIGRATION_0020 = APPLIED_IN_THIS_QA_SNAPSHOT
MIGRATION_0021 = NOT_APPLIED_IN_THIS_QA_SNAPSHOT
QUEUED_JOBS = 1
DUPLICATE_ACTIVE_CAMERA_JOBS = 0
PARTIAL_ACTIVE_JOB_INDEX_0021 = ABSENT_IN_THIS_QA_DATABASE
SQLITE_INTEGRITY = OK
FOREIGN_KEY_VIOLATIONS = 0
```

Não foram incluídos identificadores nem timestamps concretos do job. A leitura
é uma fotografia, não prova abandono e não descreve todos os ambientes do
projeto. O banco não foi alterado. Não se conclui que a migration 0021 esteja
ausente de todo o projeto: ela existe no checkout, mas não estava aplicada
naquele snapshot QA.

## 3. Fatos técnicos verificados no código/schema

- A idempotência é única por câmera, solicitante e chave. O service bloqueia
  nova intenção enquanto encontra job ativo.
- A migration 0021 define índice único parcial por câmera para estados
  `QUEUED` e `RUNNING`, depende da 0020 e pode falhar se houver duplicidades.
  O índice não interrompe I/O de um executor já ativo.
- O claim usa compare-and-set `QUEUED → RUNNING`.
- O objeto pode ser salvo no storage antes da transação que persiste
  `CameraImageRecord` e conclui o job. Um crash nessa janela pode deixar objeto
  sem associação comprovável; `image_record=NULL` não prova que storage foi
  reconciliado.
- Sucesso exige que o job ainda esteja `RUNNING`. Falha só finaliza se ainda
  estiver `RUNNING`.
- A auditoria existente é sanitizada e imutável por meio da API do modelo.

Esses fatos não demonstram que dados persistentes tenham sido alterados durante
esta investigação.

## 4. Alternativas consideradas

1. **Manter bloqueado e investigar:** única opção segura sem prova de parada,
   autoria e integridade. Mantém a indisponibilidade, mas evita interferir em
   trabalho possivelmente ativo.
2. **Command administrativa individual em janela de manutenção:** recomendação
   deste rascunho para futura avaliação. Não deve ter superfície HTTP nova.
3. **Ação web com workers ativos:** não recomendada; o schema não fornece fencing
   do executor.
4. **SQL ou shell ad hoc:** não recomendado, por não preservar um fluxo
   auditável e controlado do domínio.
5. **Reiniciar o worker:** pode consumir uma intenção `QUEUED` antiga; não resolve
   `RUNNING` e não é uma recuperação neutra.
6. **Requeue ou clonar job `RUNNING`:** não recomendado; pode repetir rede e
   efeitos colaterais.
7. **Lease, heartbeat e fencing:** hardening futuro, sujeito a contrato próprio.
   Mesmo um heartbeat, por si só, não provaria a cessação de I/O sem fencing.
8. **TTL ou retry automático:** não propostos nem autorizados.

## 5. Política proposta — ainda não ratificada

Avaliar cancelamento manual de uma intenção individual por command administrativa
futura, dentro de janela de manutenção comprovada para o domínio de captura. A
recuperação não conecta à câmera, captura, cria imagem, faz requeue, clona nem
repete a operação. Uma captura posterior exige ação humana separada e nova
intenção/chave. Não há autorização para implementar ou executar essa proposta.

### 5.1 Evidência operacional prévia necessária

Antes de qualquer candidato a recuperação, seria necessário cessar todos os
consumidores e bloquear reinícios, novas solicitações e escritas; inventariar
serviços, agendadores, processos e hosts; e confirmar a parada incluindo filhos.
O registro deve identificar host, ambiente, root, settings, banco e storage,
responsável pela janela e evidências. PID isolado não basta: correlacionar PID
com horário de início e executável/comando sanitizado.

Snapshot sem processos, encerramento do terminal, logs quietos e timeout HTTP
são evidências insuficientes. Se qualquer consumidor ou reinício puder existir,
a ação deve ser recusada. Locks de banco não substituem a prova de parada dos
executores.

### 5.2 Transições em avaliação

Fluxo ordinário existente: `QUEUED → RUNNING → SUCCEEDED | FAILED`.

As transições administrativas abaixo são propostas pendentes de ratificação:

- `QUEUED → CANCELLED` somente durante manutenção confirmada, para intenção
  explicitamente cancelada, com `started_at=NULL`, sem imagem/resultado e com
  estado ainda igual ao snapshot lido.
- `RUNNING → FAILED` somente após comprovar executor terminado, execução
  interrompida e resultado não confirmado; `started_at` coerente, sem imagem,
  efeitos possíveis no storage avaliados e estado ainda igual ao snapshot.
- Estados terminais permanecem sem mutação. Repetição só poderia ser idempotente
  quando a operação anterior estivesse comprovada.

Não permitir `RUNNING → QUEUED`, terminal → ativo, declarar sucesso por
recuperação, alterar solicitante/chave/configuração histórica/imagem, recuperação
em lote ou captura colateral.

Para preservar F03 e a lista existente de `error_code`, a proposta pendente usa
`INTERNAL_ERROR` — código genérico já existente — em `CANCELLED`, `finished_at`
UTC e `image_record=NULL`, deixando motivo operacional controlado somente na
auditoria. A adequação semântica de `INTERNAL_ERROR` para cancelamento depende de
decisão humana. Se não for ratificada, a transição fica indisponível até uma
decisão que preserve F03. Não adicionar código agora.

### 5.3 Autorização proposta

Permissão para capturar não implica permissão administrativa de recuperação.
`manage_monitoring_runtime` pertence a outro domínio e não deve ser reutilizada
implicitamente. Uma proposta futura deve definir privilégio/codename próprio e
matriz de grupos, exigir operador humano identificado, janela aprovada e job
explicitamente autorizado. Não conceder automaticamente a Técnico ou usuário
QA; acesso ao host não equivale a autorização da aplicação.

Não aceitar senha ou token em argumentos e não criar rota ou botão nesta
proposta. Segredos não devem aparecer em logs.

### 5.4 Atomicidade e auditoria propostas

Manter evidência operacional válida; revalidar ator, ambiente e janela; atribuir
operation ID único; reler job e comparar estado, datas, câmera e ausência de
resultado; usar transação no banco correto; usar lock de linha quando suportado
e update condicional sobre os campos esperados; exigir exatamente uma linha
alterada; registrar auditoria na mesma transação; confirmar commit e verificar
antes de liberar manutenção.

SQLite não fornece row lock efetivo; exigir isolamento, update condicional e
transação. Erro de lock deve abortar sem retry automático. Dois operadores podem
produzir no máximo uma transição. Estado inesperado, resultado/imagem presente ou
divergência deve abortar.

A auditoria futura deve usar a API canônica e registrar evento, operation ID,
operador congelado, job/câmera, estados, timestamps, código allowlisted, motivo
controlado, referências opacas à aprovação/manutenção, ambiente/versão do
procedimento e avaliação de storage. Aplicar allowlist e limites de tamanho;
texto livre não se torna seguro apenas pelo nome do campo. Não registrar URI
autenticada, IP desnecessário, credenciais, exceções cruas ou payload. Falha na
auditoria reverte o estado. Recusas/conflitos devem ser rastreáveis em transação
própria se o banco permitir.

## 6. Migration 0021 — dependência e gate futuro

A migration 0020 cria o modelo/constraints; 0021 cria o índice único parcial de
job ativo por câmera. A 0021 não drena fila nem resolve abandono; sua aplicação
pode falhar em presença de duplicidade. Não editar migration histórica. Engine
sem suporte efetivo ao índice não satisfaz a invariant.

Uma aplicação futura em banco persistente exige autorização específica,
identificação e backup verificável, writers parados, revisão do plano/SQL do
engine, inspeção de integridade, FKs, jobs e duplicidades, e tratamento de
duplicidade por decisão humana, sem cleanup automático. Depois, aplicar e
verificar migration/índice e integridade, testar cópia isolada e documentar que
rollback pode perder a garantia fornecida pela 0021. Recomenda-se exigir 0021
aplicada e verificada antes de reabrir captura após manutenção. O snapshot QA
registrado nesta investigação não satisfaz esse requisito. Nada disso foi
executado nesta atividade.

## 7. Falhas e resposta proposta

| Condição | Resposta proposta |
|---|---|
| Parada ou autorização incompleta | Recusar sem mutação. |
| Estado divergente | Abortar e reinspecionar. |
| Erro de banco, lock ou auditoria | Rollback, sem retry. |
| Commit incerto | Consultar pelo operation ID; não repetir cegamente. |
| Job terminal sem evidência | Não alegar sucesso. |
| Executor vivo ou com possibilidade de reinício | Manter manutenção e parar a ação. |
| Inconsistência de imagem/schema | Escalar. |
| Possível objeto órfão | Registrar e reconciliar em processo separado; não apagar automaticamente. |

## 8. Testes futuros sugeridos — não executados para F02

- Cancelamento `QUEUED` em manutenção; `RUNNING` somente após parada provada.
- Recusa com worker ativo/desconhecido e detecção de claim concorrente.
- Dois administradores: somente um vence; idempotência só com operação anterior
  comprovada.
- Nova intenção e manutenção impedindo corrida; estado terminal permanece
  inalterado.
- Recusa de usuário apenas com permissão de captura, Técnico e anônimo segundo
  matriz futura; revogação de privilégio.
- Falha de auditoria com rollback; DB lock e commit incerto.
- Coerência de datas, imagem e `error_code`; mesma chave retorna job terminal e
  não captura; chave nova após manutenção revalida o service.
- 0021 ausente, engine incompatível ou duplicidade fecham gate; migration em
  cópia preserva integridade.
- Ausência de vazamento de dados sensíveis; órfãos não são excluídos.
- Upload, monitoramento, histórico, status API e `error_code` preservados.

## 9. Decisões humanas pendentes e critérios de aceite futuros

Decisões ainda abertas:

1. Ratificar command administrativa ou escolher outra superfície.
2. Definir privilégio/grupos e aprovação operacional.
3. Ratificar estados e decidir se `INTERNAL_ERROR` é semântica aceitável em
   `CANCELLED`.
4. Definir como provar parada em todos os hosts.
5. Definir processo separado para possíveis objetos órfãos.
6. Autorizar, em atividade separada, aplicação da migration 0021 ao QA
   persistente.
7. Inventariar consumidores de `error_code`.
8. Definir contrato de lease/fencing se recuperação com worker ativo for
   necessária.

Aceite futuro exigiria aprovação humana e autorizações específicas e separadas
para implementação e execução; manutenção verificável; migration 0021 validada
antes de reabrir captura; transição individual por compare-and-set com auditoria;
recusa em qualquer incerteza; e testes no engine de destino. Não pode incluir
captura, retry, TTL, requeue ou mudança de monitoramento, imagem ou upload.

```text
F03_ERROR_CODE_LIST = PRESERVED
NEW_ERROR_CODE = NONE
INTERNAL_ERROR_FOR_CANCELLED = HUMAN_DECISION_PENDING
F02_IMPLEMENTATION = NOT_PERFORMED
RECOVERY_EXECUTION = NOT_PERFORMED
PERSISTENT_QA_DATA_CHANGED = NO
PERSISTENT_QA_MIGRATION = NOT_PERFORMED
```

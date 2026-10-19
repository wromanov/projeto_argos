# ARGOS-PRE-HML-01 — Runbook local de preparação HML E3 + E4

```text
PROJECT_ID = projeto_argos
ACTIVITY = ARGOS-PRE-HML-01
ROADMAP_STAGE = H / Controlled Homologation
STATUS = PREPARATION_ONLY
BASELINE_BRANCH = codex/hom-v1-integration
BASELINE_HEAD = 2f5109b0ba72ee5390eb4bcb02dcca4dfad74ff1
HML_ACCESS = NOT_PERFORMED
VM_STATE = UNVERIFIED
DEPLOY = NOT_AUTHORIZED
MIGRATIONS_VM = NOT_AUTHORIZED
CAMERA_REAL = NOT_AUTHORIZED
REAL_CAMERA_ACCESS = NOT_PERFORMED
NEXT_EXECUTION_LOCATION = OTHER_WORKSTATION
NEXT_GATE = VM_READ_ONLY_INSPECTION
```

Este runbook foi preparado a partir do checkout local. Todos os comandos são
modelos para uma futura janela autorizada; nenhum foi executado na VM. Os
marcadores REPLACE_* e variáveis de ambiente devem ser substituídos somente
por fatos confirmados na inspeção da VM. Não copie comandos com marcadores sem
resolvê-los e revisar o efeito.

A continuidade desta atividade ocorrerá em outra estação de trabalho. Esta
preparação não concede autorização para deploy, migrations na VM ou captura
real; o próximo gate é uma inspeção READ_ONLY autorizada.

## 1. Fatos locais verificados

| Item | Evidência local | Limite |
|---|---|---|
| Baseline publicado | branch codex/hom-v1-integration, HEAD e ref local origin/codex/hom-v1-integration em 2f5109b0ba72ee5390eb4bcb02dcca4dfad74ff1 | Não prova qual código está na VM |
| E3 | commit de código c42cd63; captura explícita, CameraCaptureJob, adapter HTTP snapshot, comando run_capture_worker e migrations 0020/0021 | Homologação/câmera real não validadas |
| E4 | commit de código 3f448d1; galeria integrada, sem model ou migration novo | QA visual E4 aprovado não deve ser repetido neste preparo |
| Evidência E4 publicada | PROJECT_STATE.md §165: 105/105 funcionais, 33 focados reexecutados, integração sintética fake, aprovação visual humana | Resultados existentes; não reexecutados nesta atividade |
| Dependência adicionada por E3 | httpx==0.28.1 | Ambiente e pacote instalado na VM desconhecidos |
| Configuração HML no repositório | config.settings_homologation; PostgreSQL; MEDIA_ROOT, LOG_ROOT e STATIC_ROOT sob /dados/argos | Não prova mount, capacidade, owner ou permissões na VM |
| Contrato de persistência | Define decisões operacionais ainda abertas sobre backend, retenção/expurgo, backup/restore e RPO/RTO | Confirmar owner e política HML antes de fixar retenção ou limpeza |
| Documentação de integração antiga | IMAGE_CAPTURE_INTEGRATION_CONTRACT.md ainda diz que worker/adapter não estão implementados; o código E3 e checkpoint posterior demonstram implementação local | Tratar a passagem como histórica/desatualizada; não confundir código publicado com prontidão HML |
| WIP local | alterações em scripts/localqa, launcher QA e arquivos .local, .tmp-e4, protótipo e outros não rastreados | Preservados; não são payload de release |

### Alterações funcionais no release

- E3 (c42cd63): novo serviço de captura, adapter HTTP snapshot real e fake,
  comando de worker, CameraCaptureJob, migrations 0020/0021, integração com
  detalhe da câmera, views/rotas, JavaScript e testes.
- E4 (3f448d1): leitura/preview da galeria, UI/rotas/JavaScript e testes.
  E4 não adiciona schema.
- O commit de checkpoint 2f5109b publica e sincroniza as evidências E4; a
  igualdade local/origin foi conferida nesta atividade.
- O branch contém mais documentação e protótipos E3/E4. Eles não devem ser
  confundidos com arquivos necessários para executar a aplicação.

## 2. Banco, migrations e dependências

### Migration lineage

```text
cameras.0019_alter_camera_options_cameraimportpreview
  → cameras.0020_cameracapturejob
      → cameras.0021_capture_job_active_per_camera
```

- 0020 cria CameraCaptureJob, referências a câmera, solicitante e imagem,
  constraints e índices. Não declara data migration.
- 0021 cria unicidade condicional por câmera para QUEUED e RUNNING.
  Duplicidade ativa pré-existente pode impedir a criação do índice. A migration
  não limpa fila, não recupera jobs abandonados e não prova que um worker parou.
- E4 não possui migration própria.
- Antes da aplicação: confirmar plano exato, versão/engine do banco, backup
  restaurável, integridade, estado de 0019–0021 e ausência de mais de um job
  ativo por câmera. Qualquer migration fora deste conjunto exige revisão e
  autorização separadas.
- Compatibilidade estática: o projeto fixa Django 5.2.18 e psycopg 3.3.6; a
  documentação oficial Django 5.2 suporta PostgreSQL 14 ou superior. A
  migration 0021 usa unicidade parcial, recurso documentado pelo PostgreSQL e
  representado por UniqueConstraint(condition=...) no Django. O servidor
  PostgreSQL, driver carregado e SQL efetivo da VM ainda não foram verificados.
- No Linux, o requisito é psycopg[c]; a instalação dessa variante depende dos
  pacotes de desenvolvimento necessários ao cliente libpq. Confirmar o runtime
  Python e esses pacotes na VM antes da instalação. Pillow e openpyxl estão
  definidos por faixas, não por versão exata; registrar as versões resolvidas
  no artefato de implantação.

Fontes oficiais: [suporte PostgreSQL do Django 5.2](https://docs.djangoproject.com/en/5.2/ref/databases/),
[UniqueConstraint do Django](https://docs.djangoproject.com/en/5.2/ref/models/constraints/),
[índices parciais do PostgreSQL](https://www.postgresql.org/docs/current/indexes-partial.html) e
[instalação Psycopg 3](https://www.psycopg.org/psycopg3/docs/basic/install.html).

## 3. Readiness de captura

### Worker e adapters

- Entry point no código: python manage.py run_capture_worker.
- --once chama run_next_capture() uma vez; sem --once/--max-jobs, o comando
  permanece em polling. O worker busca o job QUEUED mais antigo.
- --once não escolhe câmera ou job. Qualquer job pendente pode ser o
  próximo consumido.
- A cadeia do worker está demonstrada em testes com adapter fake. O teste do
  entrypoint substitui run_next_capture por mock e prova somente a chamada
  única e a ausência de migration automática. A evidência E3/E4 integrada usa
  adapter HTTP fake e não contatou câmera.
- O adapter padrão do worker é HttpSnapshotAdapter, uma implementação real de
  transporte HTTP. Isso não equivale a captura real validada. O adapter fake
  está separado e é injetado nos testes. O worker de captura atualmente rejeita
  job RTSP_FRAME; a existência de componentes RTSP não os integra a esse
  worker.
- Não há unit file/container/deploy manifest ou servidor WSGI incluído neste
  checkout. O entrypoint e o processo web existentes na VM precisam ser
  identificados; nomes de serviço não são presumidos aqui.

### Credenciais, HTTPS, Target Policy e rede

- A aplicação exige perfil/capacidade compatível, permissão de captura,
  configuração ativa e validação de Target Policy.
- Credencial BASIC/DIGEST só é resolvida pelo worker para destino HTTPS. A chave
  Fernet é carregada pelo provedor de ambiente (ARGOS_CAMERA_CREDENTIAL_KEYS
  e ARGOS_CAMERA_CREDENTIAL_ACTIVE_KEY_VERSION); os valores devem vir do
  mecanismo aprovado de secrets da VM e nunca ser copiados para este repo,
  argumentos, histórico do shell, logs ou evidência.
- Target Policy lê allowlist de CIDRs e portas por esquema; aceita também
  denylist, farms e caminhos. As variáveis de captura ARGOS_CAMERA_* não estão
  configuradas no exemplo HML do repositório. A política do app não substitui
  firewall/egress restrito: antes da câmera real, limitar a rede à câmera de
  teste, porta e caminho aprovados.
- Exigir HTTPS com certificado validável, horário sincronizado, endpoint fixo e
  perfil que corresponda ao modelo/capacidade homologados. Não desabilitar
  validação TLS para contornar erros. Se câmera só oferecer HTTP, não avançar
  captura real nesta rodada sem adjudicação de risco própria.

### Jobs e F02/F03

- F02 continua DRAFT e sem autoridade de recuperação. A causa de jobs
  QUEUED/RUNNING na VM é desconhecida; não mudar estado, cancelar, reenfileirar
  ou iniciar worker por inferência.
- O fluxo revisado não implementa lease/heartbeat ou recuperação automática de
  job interrompido após virar RUNNING. Um processo pode deixar estado RUNNING
  sem resolução automática; não reiniciar worker nem transicionar esse job sem
  diagnóstico e decisão autorizada.
- F03 preserva a lista de error_code; o uso de INTERNAL_ERROR para
  CANCELLED aguarda decisão humana. Não adicionar códigos ou transições
  administrativas durante implantação.
- Se existirem jobs antigos, múltiplos ativos por câmera ou workers ativos sem
  owner/estado comprovado: NO-GO para 0021 e para iniciar qualquer worker.
  --once não é um seletor seguro para contornar fila preexistente.

## 4. Convenções dos comandos futuros

- Alvo esperado dos exemplos: VM HML Linux com Bash, porque a configuração
  versionada aponta para /dados/argos. A inspeção A precisa confirmar o SO;
  para outro SO ou outro supervisor, parar e adaptar o roteiro.
- APP_ROOT, VENV, PG_RO_SERVICE, BACKUP_DIR, RELEASE_DIR, WEB_UNIT,
  CAPTURE_UNIT, APP_USER e PG_ISOLATED_RESTORE_SERVICE são variáveis que o
  operador só define depois de confirmar paths/identidades na VM.
  SOURCE_URL deve ser o remote canônico sem credencial embutida.
- Secrets: conectar apenas pelo mecanismo aprovado do serviço/DBA. Não usar
  env, printenv, set, diffsettings, systemctl show Environment, senha em
  URL/argumento, PGPASSWORD na linha de comando ou source cego de arquivo.
- Os comandos abaixo descrevem efeitos futuros e não são autorização para
  executá-los agora. Operações C–G exigem janela e autorização apropriadas.

## A. Inspeção READ_ONLY da VM

### A1. Sistema, volume de dados e runtime

**Ambiente/diretório:** VM HML, Bash, qualquer diretório.<br>
**Efeito:** lê SO, usuário, runtime, mount e espaço; não altera aplicação/DB.<br>
**Pré-requisitos:** sessão de leitura autorizada; /dados/argos pode não existir.<br>
**Privilégio:** usuário normal; permissões de leitura do host.<br>
**Risco/reversibilidade:** baixo; leitura, sem rollback necessário. Logs de acesso
do host podem registrar a sessão.

```bash
date -Is
cat /etc/os-release
hostnamectl
id
python3 --version
findmnt -T /dados/argos
df -h /dados/argos
stat -c '%A %U:%G %n' /dados/argos /dados/argos/media /dados/argos/static /dados/argos/logs
```

Se SO, Python, paths, mount ou permissões não corresponderem ao plano, registrar
e parar; não criar diretórios nem corrigir ownership nesta inspeção.

### A2. Checkout e processos

**Ambiente/diretório:** VM HML; APP_ROOT é path absoluto previamente confirmado.<br>
**Efeito:** lê revisão, WIP e serviços. --no-optional-locks evita lock opcional
do Git.<br>
**Pré-requisitos:** localizar a instalação sem assumir /opt, branch ou unidade.<br>
**Privilégio:** usuário normal; systemctl status pode exigir permissão de leitura.<br>
**Risco/reversibilidade:** baixo; não troca branch nem altera checkout.

```bash
git --no-optional-locks -C "$APP_ROOT" rev-parse --show-toplevel
git --no-optional-locks -C "$APP_ROOT" status --short --branch
git --no-optional-locks -C "$APP_ROOT" rev-parse HEAD
systemctl list-units --type=service --all
```

Depois de identificar os nomes reais, consultar cada unit separadamente:

```bash
systemctl status "$WEB_UNIT" --no-pager
systemctl status "$CAPTURE_UNIT" --no-pager
systemctl is-enabled "$CAPTURE_UNIT"
```

Se o checkout estiver sujo, preservar os arquivos e não fazer checkout, pull,
reset, clean ou cópia por cima. Se qualquer worker de captura estiver ativo ou
seu estado não puder ser confirmado, não o iniciar, parar ou reiniciar sem
adjudicar os jobs e obter autorização operacional.

### A3. PostgreSQL e fila (somente leitura)

**Ambiente/diretório:** VM HML; qualquer diretório; autenticação por serviço
PostgreSQL de leitura previamente aprovado.<br>
**Efeito:** executa SELECT dentro de transação READ ONLY.<br>
**Pré-requisitos:** PG_RO_SERVICE sem segredo na linha de comando; validar que
current_database() é o banco isolado de homologação.<br>
**Privilégio:** role apenas de leitura.<br>
**Risco/reversibilidade:** baixo; não altera schema/dados.

```bash
psql "service=$PG_RO_SERVICE" -X -v ON_ERROR_STOP=1 -c "BEGIN READ ONLY; SELECT current_database(), current_user, current_setting('server_version'); ROLLBACK;"
```

Somente se showmigrations confirmar 0020 aplicada e a tabela existir:

```bash
psql "service=$PG_RO_SERVICE" -X -v ON_ERROR_STOP=1 -c "BEGIN READ ONLY; SELECT status, count(*) FROM cameras_cameracapturejob GROUP BY status ORDER BY status; SELECT camera_id, count(*) FROM cameras_cameracapturejob WHERE status IN ('QUEUED','RUNNING') GROUP BY camera_id HAVING count(*) > 1; ROLLBACK;"
```

A consulta não retorna identificadores de job nem conteúdo de câmera. Se 0020
constar aplicada mas a tabela estiver ausente, houver divergência de schema ou a
consulta acusar duplicidades, parar e registrar finding; não executar limpeza.

### A4. Estado de migrations e configuração Django

**Ambiente/diretório:** VM HML; diretório APP_ROOT; usar o Python do venv e o
mesmo contexto de secrets protegido da aplicação.<br>
**Efeito:** showmigrations, migrate --plan, sqlmigrate e check apenas consultam
configuração/banco e imprimem diagnóstico; nenhum deles aplica migration.<br>
**Pré-requisitos:** Django e psycopg importáveis; configuração HML carregável.<br>
**Privilégio:** identidade de aplicação/DB de leitura; não usar root por padrão.<br>
**Risco/reversibilidade:** baixo; se o contexto seguro de configuração não
estiver disponível, não ler valores de ambiente para depurar.

```bash
cd "$APP_ROOT"
"$VENV/bin/python" manage.py showmigrations cameras --settings=config.settings_homologation
"$VENV/bin/python" manage.py migrate --plan --settings=config.settings_homologation
"$VENV/bin/python" manage.py sqlmigrate cameras 0020 --settings=config.settings_homologation
"$VENV/bin/python" manage.py sqlmigrate cameras 0021 --settings=config.settings_homologation
"$VENV/bin/python" manage.py check --deploy --settings=config.settings_homologation
```

Não usar diffsettings ou comandos que imprimam o ambiente completo. A
configuração HML versionada exige ARGOS_SECRET_KEY e variáveis
ARGOS_DB_NAME, ARGOS_DB_USER, ARGOS_DB_PASSWORD, ARGOS_DB_HOST e
ARGOS_DB_PORT; domínio/HTTPS usa ARGOS_ALLOWED_HOSTS,
ARGOS_CSRF_TRUSTED_ORIGINS, ARGOS_SECURE_SSL_REDIRECT e configurações de
proxy/HSTS. env.homologation.example é referência, não arquivo para carregar
como configuração real.

## B. Backup e critérios de rollback

### B1. Preparar destino restrito do backup

**Ambiente/diretório:** VM HML; caminho de backup aprovado e fora do checkout.<br>
**Efeito:** cria diretório restrito para artefatos.<br>
**Pré-requisitos:** destino com espaço, retenção aprovada e acesso limitado.<br>
**Privilégio:** usuário de operação/backup; root somente se o mount exigir.<br>
**Risco/reversibilidade:** escreve no filesystem; apagar backups requer política
de retenção, não é ação automática.

```bash
umask 077
mkdir -p "$BACKUP_DIR"
```

### B2. Snapshot do PostgreSQL e media

**Ambiente/diretório:** VM HML; backup autorizado; estabilizar writers somente
em janela aprovada e após inspeção/triagem da fila.<br>
**Efeito:** grava dump custom PostgreSQL e arquivo da árvore privada de mídia.<br>
**Pré-requisitos:** banco HML confirmado; serviço PostgreSQL autenticado sem
password em argumentos; web/worker de captura estabilizados com fila triada e
sem escritas durante a janela de snapshot; storage lido e espaço suficiente.
Se não for possível coordenar a pausa ou snapshot consistente de DB+media,
parar e obter procedimento do DBA/owner.<br>
**Privilégio:** role com dump do banco e leitura dos arquivos; sudo só se
requerido pelo owner/permissão confirmados.<br>
**Risco/reversibilidade:** operação de I/O e arquivos sensíveis; o dump contém
dados e credenciais cifradas. Restore sobrescrevendo destino ativo é proibido.

```bash
pg_dump --format=custom --file="$BACKUP_DIR/argos-hml-pre-e3e4.dump" --dbname="service=$PG_RO_SERVICE"
tar --create --file="$BACKUP_DIR/argos-media-pre-e3e4.tar" --numeric-owner --acls --xattrs --directory=/dados/argos media
sha256sum "$BACKUP_DIR/argos-hml-pre-e3e4.dump" "$BACKUP_DIR/argos-media-pre-e3e4.tar"
pg_restore --list "$BACKUP_DIR/argos-hml-pre-e3e4.dump"
tar --list --file="$BACKUP_DIR/argos-media-pre-e3e4.tar" > /dev/null
```

O perfil PostgreSQL para dump precisa de privilégios de leitura suficientes;
uma role estritamente read-only pode não conseguir ler grandes objetos ou
sequências. Se o comando falhar por privilégio, não ampliar grants
automaticamente: solicitar owner/DBA. A validação por lista/checksum não prova
restore. Antes de GO para migrations, demonstrar restore em banco e diretório
isolados, sem apontar para o serviço ativo:

```bash
pg_restore --exit-on-error --single-transaction --dbname="service=$PG_ISOLATED_RESTORE_SERVICE" "$BACKUP_DIR/argos-hml-pre-e3e4.dump"
tar --extract --file="$BACKUP_DIR/argos-media-pre-e3e4.tar" --directory="$MEDIA_RESTORE_ROOT" --numeric-owner --same-permissions
```

O banco e o diretório do restore precisam estar vazios, isolados e previamente
criados para esse ensaio. O restore altera somente esses destinos isolados,
exige DBA/owner e é reversível apenas descartando os destinos de teste após a
evidência aprovada.

**Ambiente/diretório:** VM HML; banco identificado por
PG_ISOLATED_RESTORE_SERVICE e diretório vazio MEDIA_RESTORE_ROOT, ambos isolados
do serviço ativo.<br>
**Efeito:** escreve tabelas/dados no banco de restore e arquivos no diretório de
restore.<br>
**Pré-requisitos:** autorização DBA/owner, backup validado, destinos novos/vazios,
espaço e compatibilidade verificados.<br>
**Privilégio:** role DBA/restore; acesso de escrita no diretório isolado; root
somente se ownership confirmado exigir.<br>
**Risco/reversibilidade:** altera destinos isolados; descarte posterior depende
de autorização e prova de que não são usados pelo serviço HML.

### B3. Rollback

1. Primeira opção: reativar o release anterior verificado pelo mecanismo real
   identificado em A; preservar o schema aditivo 0020/0021, banco, media e jobs.
   O release antigo não deve consumir fila E3.
2. Manter o worker de captura parado. Confirmar que não há job RUNNING antes de
   trocar ou reiniciar serviços.
3. Não reverter 0020/0021 automaticamente. Reverter 0020 remove a tabela e
   jobs; reverter 0021 remove a proteção de unicidade ativa. Uma volta de banco
   usa restore do dump em destino isolado e exige adjudicação explícita de
   perda de escritas posteriores ao backup.
4. Não remover objetos de mídia, jobs, auditoria ou credenciais como parte de
   rollback de código. Um teste de câmera real produz dados persistentes; sua
   retenção/descarte precisa de decisão do owner.
5. No-go e rollback imediato diante de erro em migration, integridade, login,
   autorização, preview, storage, segurança TLS ou health check. Congelar a
   promoção, preservar logs/evidências redigidos e decidir próximo passo com o
   owner; sem cleanup corretivo automático.

## C. Atualização da aplicação

### C1. Preparar release isolado no SHA aprovado

**Ambiente/diretório:** VM HML; Bash; RELEASE_DIR novo e vazio, separado do
checkout ativo.<br>
**Efeito:** busca a branch publicada e monta checkout detached do SHA exato.<br>
**Pré-requisitos:** origem canônica confirmada, rede autorizada, destino
inexistente, snapshot de estado/WIP existente preservado.<br>
**Privilégio:** usuário de release; sem root.<br>
**Risco/reversibilidade:** altera somente o novo diretório; pode removê-lo
depois sob retenção aprovada; não sobrescreve a aplicação ativa.

```bash
git clone --no-checkout "$SOURCE_URL" "$RELEASE_DIR"
git -C "$RELEASE_DIR" fetch origin codex/hom-v1-integration
git -C "$RELEASE_DIR" cat-file -e '2f5109b0ba72ee5390eb4bcb02dcca4dfad74ff1^{commit}'
git -C "$RELEASE_DIR" checkout --detach 2f5109b0ba72ee5390eb4bcb02dcca4dfad74ff1
git --no-optional-locks -C "$RELEASE_DIR" rev-parse HEAD
git --no-optional-locks -C "$RELEASE_DIR" status --short --branch
```

O SHA deve corresponder exatamente ao baseline acima. Se não estiver disponível
no remote, a branch tiver avançado sem o SHA, o destino não estiver vazio ou
existir WIP no checkout escolhido, parar. Não executar pull/checkout por cima
de instalação existente.

### C2. Ambiente de dependências candidato

**Ambiente/diretório:** VM HML; RELEASE_DIR; criar venv nova para este release.<br>
**Efeito:** instala runtime isolado e dependências de requirements.txt.<br>
**Pré-requisitos:** Python compatível com Django 5.2 (3.10+), acesso aprovado ao
índice de pacotes, requisitos de build/runtime de psycopg C no Linux e versão de
pacotes/faixas registrada.<br>
**Privilégio:** usuário de release, sem root no venv; pacotes de SO exigem
administrador e aprovação separada.<br>
**Risco/reversibilidade:** rede e escrita no venv candidato; remover apenas o
venv candidato é reversível sem tocar no venv ativo.

```bash
cd "$RELEASE_DIR"
python3 -m venv "$RELEASE_DIR/.venv"
"$RELEASE_DIR/.venv/bin/python" -m pip install --requirement "$RELEASE_DIR/requirements.txt"
"$RELEASE_DIR/.venv/bin/python" -m pip freeze --all
"$RELEASE_DIR/.venv/bin/python" manage.py check --deploy --settings=config.settings_homologation
```

pip freeze deve ser arquivado como evidência da versão resolvida, fora do
repositório e sem conteúdo de ambiente. Erro de instalação, pacote incompatível,
driver indisponível ou warning de deployment sem adjudicação: NO-GO.

## D. Migrations aprovadas

**Ambiente/diretório:** VM HML; release candidato RELEASE_DIR, venv candidato;
configuração HML com secrets fornecidos pelo mecanismo aprovado.<br>
**Efeito:** o primeiro comando só planeja; o comando migrate cameras 0021
altera schema persistente.<br>
**Pré-requisitos para aplicar:** gate humano/operacional próprio; backup e
restore isolado aprovados; PostgreSQL 14+ confirmado; plano contém somente as
migrations esperadas/dependências aprovadas; 0020 compatível com dados e
0021 sem duplicidades ativas; janela e owner definidos.<br>
**Privilégio:** role da aplicação/DBA autorizada a criar tabela, constraint e
índices.<br>
**Risco/reversibilidade:** alteração persistente; 0021 pode falhar em duplicidade
e criar índice pode disputar com writes. Não usar --fake, SQL manual ou
correção automática de fila.

```bash
cd "$RELEASE_DIR"
"$RELEASE_DIR/.venv/bin/python" manage.py migrate --plan --settings=config.settings_homologation
"$RELEASE_DIR/.venv/bin/python" manage.py sqlmigrate cameras 0020 --settings=config.settings_homologation
"$RELEASE_DIR/.venv/bin/python" manage.py sqlmigrate cameras 0021 --settings=config.settings_homologation
```

O owner aprova o plano/SQL e os counts da fila. Só então executar:

```bash
"$RELEASE_DIR/.venv/bin/python" manage.py migrate cameras 0021 --settings=config.settings_homologation
"$RELEASE_DIR/.venv/bin/python" manage.py showmigrations cameras --settings=config.settings_homologation
"$RELEASE_DIR/.venv/bin/python" manage.py migrate --check --settings=config.settings_homologation
```

Confirmar em leitura que 0020 e 0021 estão aplicadas e que o índice
cam_capture_active_camera_uniq existe no schema HML esperado. Migration fora
do plano aprovado, lock/timeout, estado inconsistente ou falha em qualquer
constraint: parar a promoção e não tentar --fake, drop, retry automático ou
reversão.

## E. Configuração dos serviços

### Configuração exigida a confirmar

- Web usa DJANGO_SETTINGS_MODULE=config.settings_homologation, DEBUG=false,
  host/origin HML exatos, TLS/CSRF/proxy confiável e segredo exigido pelo
  settings de produção; sem arquivo de secrets no repo.
- PostgreSQL isolado de homologação, role de aplicação com privilégio mínimo e
  conexão protegida. Confirmar server_version >= 14, driver psycopg importável
  e CONN_MAX_AGE/health checks conforme configuração.
- A aplicação e o worker precisam de acesso somente necessário a
  /dados/argos/media e /dados/argos/logs; o web server/servidor de estáticos
  precisa servir STATIC_ROOT=/dados/argos/static conforme arquitetura HML
  encontrada. Validar filesystem/mount persistente, espaço e backup.
- Resolver servidor WSGI, reverse proxy, TLS termination, static serving,
  usuários/grupos e units existentes por inspeção. O repositório não especifica
  nomes nem configuração desses serviços.
- Worker de captura fica sem auto-start durante atualização, smoke e até
  concluir gates de captura. Worker de monitoramento é processo distinto;
  preservar sua configuração e não reiniciar/habilitar automaticamente.
- Se a unit web for systemd, após autorização e após apontar para release
  validado:

```bash
sudo systemctl restart "$WEB_UNIT"
sudo systemctl status "$WEB_UNIT" --no-pager
```

**Ambiente/diretório:** VM HML, qualquer diretório. **Efeito:** reinicia serviço
web existente e consulta o estado. **Pré-requisitos:** unit identificada,
janela aprovada, versão nova preparada e rollback de release anterior testado.
**Privilégio:** restart requer sudo/root; status costuma permitir leitura.
**Risco/reversibilidade:** breve indisponibilidade; reversível reativando release
anterior pelo mecanismo confirmado. Se não for systemd, não usar estes comandos.

Não criar unit de worker por suposição. Se a instalação atual tiver worker
ativo, isso é finding para o owner: não parar abruptamente, não trocar versão e
não iniciar captura até prova de fila/execução e autorização.

## F. Smoke test funcional da aplicação e galeria

### Comandos pré-smoke

**Ambiente/diretório:** VM HML; release ativo/candidato conforme gate de C–E.<br>
**Efeito:** check consulta settings; collectstatic grava assets compilados em
STATIC_ROOT.<br>
**Pré-requisitos:** DB, segredo e hosts configurados; STATIC_ROOT confirmado e
gravável; backup/release anterior pronto; comandos executados uma vez no destino
aprovado.<br>
**Privilégio:** identidade de release para check; identidade com write em
STATIC_ROOT para collectstatic; sem root salvo requisito documentado.<br>
**Risco/reversibilidade:** check é diagnóstico; collectstatic altera
arquivos estáticos, reversível ao reconstruir assets do release anterior.

```bash
cd "$RELEASE_DIR"
"$RELEASE_DIR/.venv/bin/python" manage.py check --deploy --settings=config.settings_homologation
"$RELEASE_DIR/.venv/bin/python" manage.py collectstatic --noinput --settings=config.settings_homologation
```

### Verificação no browser autorizado (não é QA visual E4)

- Entrar com usuário de homologação autorizado a view_camera; confirmar
  login, navegação e detalhe de uma câmera de teste aprovada.
- Confirmar que a galeria carrega zero imagens sem erro; para imagem existente,
  verificar preview autorizado, tipo/tamanho esperado e resposta
  no-store/nosniff pelo comportamento/headers. Não alterar imagens nem
  permissão.
- Quando houver imagens sintéticas já aprovadas, verificar que a galeria exibe
  no máximo três ativas, mantém proveniência de upload/captura e abre/fecha o
  preview. Não criar fixture nem upload no banco persistente.
- Reaproveitar o aceite visual E4 já registrado; não comparar screenshots nem
  repetir avaliação visual/responsiva nesta atividade.
- Qualquer 5xx, redirect inesperado, acesso sem permissão, falha de storage,
  preview público/cacheado ou asset ausente é NO-GO. Registrar hora,
  status/headers e versão sem cookie, token, segredo, IP sensível ou conteúdo de
  imagem.

## G. Teste controlado de captura real (gate separado)

Não realizar nesta atividade. O teste futuro escreve job, auditoria, imagem
privada e metadados no banco/storage HML. Exige autorização específica,
dispositivo/câmera de teste, janela, owner, retenção e evidência aprovada.

Pré-condições cumulativas:

1. Gates A–F aprovados; PostgreSQL 14+; 0020/0021 aplicada e verificada.
2. Janela exclusiva aprovada sem outros produtores de captura; worker único e
   isolado, sem outro consumidor ativo; fila vazia antes de criar o job; zero
   job RUNNING; ausência de duplicidades. --once não seleciona câmera, portanto
   deve existir exatamente um job autorizado no momento de executá-lo, sem
   possibilidade de outro job ser enfileirado concorrentemente.
3. Câmera aprovada com perfil HTTP snapshot compatível, endpoint/path fixo,
   porta permitida, HTTPS/certificado validável, credencial correta entregue
   pelo secret manager quando necessária, e key version reconhecida.
4. Target Policy com menor CIDR aplicável, denylist revisada, farm/porta/path
   restritos; firewall e egress limitados ao dispositivo aprovado. Sem acesso a
   outras VLANs, subnets ou dispositivos.
5. Operador com permissão capture_camera_image envia uma intenção explícita
   pela UI durante a janela exclusiva. Confirmar que só esse job ficou QUEUED;
   nunca incluir segredo na UI/URL. Se outro produtor puder criar job, cancelar
   o gate e não executar --once.

Com o job único já criado e gate de execução aprovado, o comando abaixo faz uma
captura real e grava resultado persistente:

```bash
cd "$APP_ROOT"
"$VENV/bin/python" manage.py run_capture_worker --once --settings=config.settings_homologation
```

**Ambiente/diretório:** VM HML, aplicação e variável segura de settings ativas.
**Efeito:** consome o job QUEUED mais antigo; pode abrir conexão de rede com
câmera e escrever job, auditoria, imagem e registro. **Pré-requisitos:** todos
os cinco gates acima e prova de um único job; demais workers parados com
segurança e fila sem pendências. **Privilégio:** usuário isolado do worker com
acesso mínimo ao DB, media e log. **Risco/reversibilidade:** alto e parcialmente
irreversível; não remover automaticamente job/imagem/auditoria. Parar após uma
tentativa. Sem sucesso/falha sanitizada, revisar antes de qualquer retry.

Após a tentativa, consultar estado do job, auditoria e galeria sem expor segredo.
Confirmar um único resultado e acesso restrito ao preview. Arquivar as
evidências redigidas, desligar o processo de teste (o --once termina sozinho)
e confirmar que não ficou worker automático ativo. Não executar teste de carga,
loop contínuo, várias câmeras ou retries.

## H. Critérios GO / NO-GO

### GO para a próxima gate

Este pacote permite avançar apenas a VM_READ_ONLY_INSPECTION. Não é GO para
deploy, migration, ativar worker, homologar captura real ou fechar HOM-03/HOM-04.

### GO para uma futura atualização de aplicação

Somente com owner/janela autorizados; VM/OS/paths e source identificados; checkout
limpo preservado; baseline SHA exato; PostgreSQL 14+ isolado; requirements
instalados no candidato; backup de DB+media e restore isolado provados; plano de
migrations aprovado; settings/secrets protegidos; storage persistente e
permissões mínimas validados; serviços web/static identificados; smoke funcional
sem falhas; worker de captura explicitamente sob controle.

### GO para uma captura real

Além do acima: fila vazia e worker único; 0021 verificada; câmera/perfil de teste
aprovados; HTTPS/certificado, credencial e Target Policy verificados sem revelar
valores; egress limitado no firewall; operador autorizado; uma intenção e um
--once; disposição da imagem/job persistente acordada.

### NO-GO imediato

- VM, PostgreSQL, serviço ou armazenamento diferentes do que o código espera;
- PostgreSQL abaixo da versão suportada, psycopg ausente, Python incompatível ou
  check --deploy não aprovado;
- WIP no checkout ativo; origem/commit não correspondem ao baseline;
- backup incompleto ou restore isolado não demonstrado;
- plano com migration inesperada, duplicidade de job, schema divergente ou
  integrity/FK issue;
- fila antiga, worker ativo/desconhecido ou causa F02 não delimitada;
- necessidade de alterar job, error_code/F03, conceder permissionamento,
  abrir firewall amplo, contornar TLS ou limpar objetos;
- mount/storage sem persistência, sem espaço, permissões excessivas ou
  evidência de acesso público a imagens;
- ausência de owner, autorização, janela ou rollback executável.

## 5. Checklist de evidências

Guardar em local aprovado, fora do código e sem segredos:

- [ ] Operador, horário, ambiente, owner/aprovador e autorização/janela.
- [ ] SO/Python, paths/mounts, capacidade e owner/group/permissões dos diretórios.
- [ ] SHA de origem (2f5109b...), SHA candidato/ativo, branch/ref e estado do
  checkout sem WIP sobrescrito.
- [ ] PostgreSQL version, banco/schema isolado, usuário de serviço sem senha e
  estado de conectividade.
- [ ] Plano de migrations/SQL revisado; 0019–0021 antes/depois; índice
  cam_capture_active_camera_uniq; contagem de jobs por status e duplicidades.
- [ ] Versões resolvidas do Python/dependências e resultado de import do psycopg
  sem imprimir variáveis de ambiente.
- [ ] Backup com checksums, listagem do dump/media e prova de restore isolado.
- [ ] Settings não secretas aprovadas; segredo somente por confirmação do
  secret manager, sem copiar/mostrar seu conteúdo.
- [ ] Serviços web/worker/static identificados; usuário/grupo e estado antes e
  depois; nenhum worker de captura automático sem autorização.
- [ ] check --deploy, static collect e smoke funcional; status/headers de
  login/detalhe/preview sem cookie, payload, IP sensível ou imagem.
- [ ] Para teste real autorizado: camera/profile genéricos, HTTPS validado,
  policy e ACL resumidas, um job e resultado sanitizado, storage/auditoria,
  owner e disposição aprovada. Não registrar endpoint autenticado ou credencial.

## 6. Hipóteses que somente a VM pode resolver

| Hipótese/unknown | Evidência exigida na gate READ_ONLY |
|---|---|
| Linux, Python e paths do deployment | os-release, runtime e paths observados |
| Release atual e existência de WIP | branch/SHA/status read-only |
| PostgreSQL alvo e versão | current_database, current_user, server_version |
| Estado 0019/0020/0021 e fila | showmigrations, plano e consultas READ ONLY |
| Worker/service existente e execução | unit manager, status e owner identificados |
| Capacidade, mount e permissões de media/static/logs | mount, espaço, ownership e prova de backup |
| Secret manager, hosts, TLS/proxy, credenciais e Target Policy | confirmação não secreta do owner e checks seguros |
| Egress permitido/firewall/VLAN para câmera | regra aprovada e inspeção pelo owner de rede |
| Rotina de backup/restore e rollback | restore isolado e mecanismo de release existente |

Nenhum dos itens dessa tabela foi observado nesta preparação local.

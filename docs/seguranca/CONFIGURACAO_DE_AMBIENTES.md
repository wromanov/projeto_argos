# Configuração de ambientes

Desenvolvimento usa `config.settings`, SQLite e HTTP local. As variáveis `ARGOS_DEBUG`, `ARGOS_SECRET_KEY` e `ARGOS_ALLOWED_HOSTS` são opcionais localmente. `.env.example` é apenas referência e não é carregado automaticamente.

Produção usa `config.settings_production` e exige `ARGOS_SECRET_KEY` forte e `ARGOS_ALLOWED_HOSTS`. Configure também `ARGOS_CSRF_TRUSTED_ORIGINS`, cookies seguros e HSTS. HSTS preload só deve ser ativado após avaliação. `ARGOS_TRUST_PROXY_SSL_HEADER` só é seguro com proxy controlado que sobrescreva o cabeçalho.

Exemplo PowerShell: defina temporariamente `$env:DJANGO_SETTINGS_MODULE='config.settings_production'` e as variáveis ARGOS necessárias, então execute `python manage.py check --deploy`. Não use `runserver` em produção.

## Homologação PostgreSQL

Use `DJANGO_SETTINGS_MODULE=config.settings_homologation`. O perfil herda as
proteções web de `config.settings_production`, preserva o SQLite do perfil de
desenvolvimento e exige as variáveis `ARGOS_DB_NAME`, `ARGOS_DB_USER`,
`ARGOS_DB_PASSWORD` e `ARGOS_DB_HOST`; `ARGOS_DB_PORT` (5432) e
`ARGOS_DB_CONN_MAX_AGE` (60) têm defaults. O arquivo
`env.homologation.example` documenta os nomes e valores não secretos. Ele não
é carregado automaticamente. Injete `ARGOS_SECRET_KEY` e `ARGOS_DB_PASSWORD`
por um cofre ou pelo ambiente protegido do serviço.

O perfil aponta `MEDIA_ROOT`, `LOGGING` e `STATIC_ROOT` para
`/dados/argos/media`, `/dados/argos/logs` e `/dados/argos/static`. Antes de
iniciar o serviço, o operador deve provisionar esses diretórios com proprietário
igual ao usuário do serviço; mídia e logs devem permitir acesso somente a esse
usuário (por exemplo, diretórios `0700` e arquivos `0600`). O destino de estáticos
deve ser gravável pelo usuário que executa `collectstatic` e publicado pelo
servidor web conforme a topologia aprovada. O Django não cria nem altera
permissões desses diretórios durante o carregamento das settings.

Depois de provisionar os diretórios e configurar as variáveis no ambiente do
serviço, valide com `python manage.py check --deploy` e gere estáticos com
`python manage.py collectstatic --noinput`. A aplicação usa o backend PostgreSQL
do Django com Psycopg 3.3.6, declarado em `requirements.txt`: extra `[c]` no
Linux e `[binary]` no Windows. Esses comandos não
aplicam migrations. A conectividade, permissões efetivas do sistema de arquivos
e compatibilidade contra o servidor PostgreSQL devem ser confirmadas no ambiente
de homologação isolado antes de aceitar a preparação da VM.

No Linux, o extra `[c]` compila a extensão Psycopg durante a instalação e exige
toolchain de compilação e bibliotecas de desenvolvimento do cliente PostgreSQL
(incluindo `pg_config`). A imagem da VM deve prover esses pré-requisitos antes
de instalar `requirements.txt`; eles ainda não foram verificados na VM.

Permanecem pendentes servidor, banco, proxy reverso, HTTPS, DNS, firewall, backup, retenção, observabilidade e armazenamento seguro de futuras credenciais.

## Visual QA local

O Visual QA é uma identidade exclusiva para desenvolvimento local e validação visual autenticada. Nunca habilite esse modo em produção.

Configure a flag e a identidade somente no ambiente do processo PowerShell:

```powershell
$env:ARGOS_VISUAL_QA_ENABLED="1"
$env:ARGOS_VISUAL_QA_USERNAME="codex_visual"
$env:ARGOS_VISUAL_QA_PASSWORD="<definir-localmente>"
```

O projeto não carrega `.env` automaticamente. Execute `python manage.py provision_visual_qa` depois de definir as três variáveis. O comando é idempotente, não imprime a senha e mantém o usuário `is_staff=False` e `is_superuser=False`.

O conjunto explícito e mínimo de permissões é: `cameras.view_camera`, `cameras.add_camera`, `cameras.change_camera`, `cameras.desativar_camera`, `cameras.reativar_camera`, `cameras.alterar_situacao_camera`, `cameras.registrar_substituicao_camera`, `cameras.consultar_eventos` e `cameras.consultar_substituicoescamera`. `add_camera` e `change_camera` existem somente para que as telas GET de criação e edição possam ser abertas; a barreira central read-only é independente e bloqueia qualquer POST/PUT/PATCH/DELETE do QA. As quatro permissões de governança são necessárias para abrir os respectivos formulários protegidos por permissionamento.

O acesso do Visual QA é somente leitura: `GET`, `HEAD` e `OPTIONS` são aceitos somente quando o Host é `localhost`, `127.0.0.1` ou `::1` e `REMOTE_ADDR` é realmente `127.0.0.1` ou `::1`. Cabeçalhos de proxy não participam dessa decisão. A única exceção de método não seguro é o `POST` explícito de `/logout/`, necessário para encerrar a sessão. Login continua usando a autenticação normal do Django.

O comando recusa um username já ocupado quando não consegue reconhecer a conta como Visual QA previamente provisionada; nesse caso, não altera a conta existente. A conta criada recebe um marcador interno determinístico para permitir reaplicação idempotente das permissões aprovadas.

`$env:` vale apenas para a sessão/processo atual do PowerShell. Para persistência entre terminais, o usuário pode escolher conscientemente uma opção segura de gerenciamento de segredos do Windows; não use o repositório, fixtures, documentação ou commits para armazenar a senha e não execute `setx` automaticamente para esse segredo.

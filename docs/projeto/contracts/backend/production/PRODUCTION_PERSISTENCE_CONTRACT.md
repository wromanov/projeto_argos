# Persistência de produção

```text
ID = PROD-PERSIST
STATUS = ACTIVE / ARCHITECTURAL BASELINE
PRODUCTION_DATABASE = NOT CONFIGURED OR VALIDATED IN CHECKOUT
BC02_STATUS = PRODUCTION_ONLY
CONTRACT_READY = NO / provider, storage, restore and RPO-RTO environment decisions
IMPLEMENTATION_NOW = NO
VALIDATION_ENVIRONMENT = PostgreSQL / homologation / production
```

## Separação de dados

Dados cadastrais, estado/transições/indisponibilidades, metadados de imagem e bytes privados têm lifecycle, autorização, backup e retenção diferentes. Segredos de equipamento persistidos futuramente são ciphertext e não compartilham backup com chave mestra. Storage de imagem usa interface configurável, referências opacas privadas e nunca expõe URL pública/chave ao cliente. Integridade é verificada no server; falha do storage é explícita e não seleciona registro histórico mais antigo por conveniência.

## Estado do ambiente

`config/settings.py` define SQLite `db.sqlite3` e `MEDIA_ROOT` local privado; `settings_production.py` endurece configurações web mas herda a configuração de banco, sem declarar PostgreSQL/backup/storage remoto. Portanto o nome do settings production não constitui evidência de persistência de produção aprovada. ADR-021 recomenda PostgreSQL para produção, mas deixa topologia e provisionamento em aberto. Contrato de imagem mantém backend definitivo de produção deferido.

## Requisitos antes de operar

Selecionar engine/provider e topologia com decisão explícita; migrar e testar constraints/índices concorrentes; configurar credenciais/TLS e usuário de menor privilégio; backup/restore incluindo chaves de segredo por canal separado; RPO/RTO, retenção e expurgo; private storage, política de lifecycle e reconciliação de objetos órfãos; comportamento sob indisponibilidade e limites de conexão. Testar transações, janela/índices de latest, `select_for_update`/CAS, leases e constraints na engine final.

Não fixar valores ou fornecedor neste baseline. PostgreSQL real, multi-instância, restore testado, storage privado remoto e performance/capacity de produção não foram validados. Referências: ADR-021 §§3.2–3.4, 6; `config/settings.py`, `settings_production.py`; `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` §§21–24.

## BC-02 — limite para as slices locais

PostgreSQL é engine alvo para validação produtiva de constraints, CAS,
`select_for_update`, índices de latest, lease/fencing e contenção. Isto não
seleciona provedor, credenciais, TLS, topologia, backup/restore, RPO/RTO,
storage privado remoto ou retenção: são decisões operacionais do ambiente.
As migrations locais das slices BC-02 devem ser portáveis e verificadas no
PostgreSQL antes de homologação; não se cria migration de produção nesta
atividade. `CredentialKeyProvider` recebe chave fora do banco; restore testa
separadamente ciphertext e custódia da chave. `CameraImageRecord` continua
com referência privada opaca; objeto ausente não promove captura antiga.

```text
MODEL_CHANGE = NONE IN BC-02
MIGRATION_REQUIRED = NO IN BC-02
EXPECTED_MODELS = existing and planned domain models
RELATIONSHIPS = per local slice
CONSTRAINTS = validate all on PostgreSQL before homologation
INDEXES = validate latest/due/lease plans on PostgreSQL
DATA_MIGRATION = NO IN BC-02
ROLLBACK_CONSIDERATION = backup/restore and key recovery rehearsed separately
EXPECTED_PRIMARY_FILES = config/settings_production.py; deployment config (future)
EXPECTED_NEW_FILES = provider-specific settings/runbook (future)
EXPECTED_TEST_FILES = PostgreSQL integration/restore tests (future)
SHARED_FILES = production settings and migration graph, single owner
STOP_AND_ESCALATE_TO_SOL_IF = chosen provider breaks domain constraints or
                              requires new data/secret lifecycle
```

Acceptance gate futuro: constraints e concorrência equivalentes no banco
alvo; restore de DB, chave e storage validado; falhas de DB/storage não
geram OFFLINE ou fallback de imagem; backup, retenção e RPO/RTO aprovados.

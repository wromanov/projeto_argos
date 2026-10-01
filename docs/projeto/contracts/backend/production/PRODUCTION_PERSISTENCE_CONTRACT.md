# Persistência de produção

```text
ID = PROD-PERSIST
STATUS = ACTIVE / ARCHITECTURAL BASELINE
PRODUCTION_DATABASE = NOT CONFIGURED OR VALIDATED IN CHECKOUT
```

## Separação de dados

Dados cadastrais, estado/transições/indisponibilidades, metadados de imagem e bytes privados têm lifecycle, autorização, backup e retenção diferentes. Segredos de equipamento persistidos futuramente são ciphertext e não compartilham backup com chave mestra. Storage de imagem usa interface configurável, referências opacas privadas e nunca expõe URL pública/chave ao cliente. Integridade é verificada no server; falha do storage é explícita e não seleciona registro histórico mais antigo por conveniência.

## Estado do ambiente

`config/settings.py` define SQLite `db.sqlite3` e `MEDIA_ROOT` local privado; `settings_production.py` endurece configurações web mas herda a configuração de banco, sem declarar PostgreSQL/backup/storage remoto. Portanto o nome do settings production não constitui evidência de persistência de produção aprovada. ADR-021 recomenda PostgreSQL para produção, mas deixa topologia e provisionamento em aberto. Contrato de imagem mantém backend definitivo de produção deferido.

## Requisitos antes de operar

Selecionar engine/provider e topologia com decisão explícita; migrar e testar constraints/índices concorrentes; configurar credenciais/TLS e usuário de menor privilégio; backup/restore incluindo chaves de segredo por canal separado; RPO/RTO, retenção e expurgo; private storage, política de lifecycle e reconciliação de objetos órfãos; comportamento sob indisponibilidade e limites de conexão. Testar transações, janela/índices de latest, `select_for_update`/CAS, leases e constraints na engine final.

Não fixar valores ou fornecedor neste baseline. PostgreSQL real, multi-instância, restore testado, storage privado remoto e performance/capacity de produção não foram validados. Referências: ADR-021 §§3.2–3.4, 6; `config/settings.py`, `settings_production.py`; `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` §§21–24.

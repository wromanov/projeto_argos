# Configuração de ambientes

Desenvolvimento usa `config.settings`, SQLite e HTTP local. As variáveis `ARGOS_DEBUG`, `ARGOS_SECRET_KEY` e `ARGOS_ALLOWED_HOSTS` são opcionais localmente. `.env.example` é apenas referência e não é carregado automaticamente.

Produção usa `config.settings_production` e exige `ARGOS_SECRET_KEY` forte e `ARGOS_ALLOWED_HOSTS`. Configure também `ARGOS_CSRF_TRUSTED_ORIGINS`, cookies seguros e HSTS. HSTS preload só deve ser ativado após avaliação. `ARGOS_TRUST_PROXY_SSL_HEADER` só é seguro com proxy controlado que sobrescreva o cabeçalho.

Exemplo PowerShell: defina temporariamente `$env:DJANGO_SETTINGS_MODULE='config.settings_production'` e as variáveis ARGOS necessárias, então execute `python manage.py check --deploy`. Não use `runserver` em produção.

Permanecem pendentes servidor, banco, proxy reverso, HTTPS, DNS, firewall, backup, retenção, observabilidade e armazenamento seguro de futuras credenciais.

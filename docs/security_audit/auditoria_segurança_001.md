# ARGOS SECURITY REVIEW

**Baseline auditado:** `26a8925c6968cf61551d524e233679a1a2771993`
**Branch:** `master`
**Escopo:** auditoria de segurança inicialmente somente leitura, com VERIFY ativo posterior, local e explicitamente autorizado para SEC-007 e os findings derivados do VERIFY.

## Resumo executivo

Critical: 0
High: 2 — 1 confirmado historicamente e REMEDIADO / VERIFIED; 1 potencial
Medium: 8 — 6 confirmados; 2 potenciais
Low: 0
Info: 0

Principais riscos:

1. A configuração de produção depende da seleção manual do módulo e herda SQLite.
2. A identidade Visual QA mantém permissões de escrita quando a barreira de middleware é desativada.
3. O login não possui throttling e cada falha gera evento persistente.
4. Campos textuais aceitam conteúdo sem limite explícito.

## Validações executadas

- 569 testes: PASS (contagem da working tree; não é a contagem canônica do baseline auditado — ver Integridade da auditoria).
- `manage.py check`: PASS.
- `check --deploy`: PASS, com aviso de HSTS preload quando desativado.
- `makemigrations --check --dry-run`: PASS.
- Bandit: 0 findings médios/altos.
- `pip-audit`: nenhuma vulnerabilidade conhecida.
- `detect-secrets`: somente falsos positivos já presentes na baseline.

## Findings

### SEC-001 — Fronteira entre configuração de desenvolvimento e produção não é fail-closed

**Categoria:** ARCHITECTURAL RISK
**Severidade:** High
**Confiança:** Alta
**Status:** POTENCIAL
**Prioridade sugerida:** P1
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `config/settings.py`, `config/settings_production.py`, `manage.py`
**Linhas:** `config/settings.py:29-38`; `config/settings_production.py:5-9`; `manage.py:9`
**Componente:** Configuração de ambiente

**Descrição:**

O entrypoint padrão usa `config.settings`, que habilita `DEBUG=True`, aceita uma chave fixa de desenvolvimento e possui hosts locais padrão. A configuração segura só é aplicada quando o deployment seleciona explicitamente `config.settings_production`.

**Evidência:**

- `DEBUG` possui default `True`.
- Existe `DEVELOPMENT_SECRET_KEY` fixa no código.
- `manage.py` define `DJANGO_SETTINGS_MODULE=config.settings`.
- O `check --deploy` seguro depende do módulo de produção.

**Cenário de risco:**

Um deployment iniciado sem configurar explicitamente o módulo de produção pode expor páginas de debug e operar com chave conhecida.

**Impacto:**

Exposição de paths, configuração e informações internas; risco de comprometimento de tokens assinados dependendo do fluxo utilizado.

**Causa raiz:**

A escolha do perfil seguro depende exclusivamente do ambiente operacional.

**Correção mínima segura:**

Fazer o processo de produção iniciar somente com `config.settings_production` e rejeitar `DEBUG=True` fora de desenvolvimento local.

**Código sugerido:**

```python
if not DEBUG and SECRET_KEY == DEVELOPMENT_SECRET_KEY:
    raise ImproperlyConfigured("Chave de desenvolvimento não pode ser usada.")
```

**Hardening adicional:** rejeitar `ALLOWED_HOSTS="*"` e valores que desativem SSL/HSTS em produção.

**Teste recomendado:**

Verificar que o processo de produção falha quando `DJANGO_SETTINGS_MODULE` não é seguro, `DEBUG=True` ou a chave de desenvolvimento é usada.

### SEC-002 — Perfil de produção herda banco SQLite de desenvolvimento

**Categoria:** SECURITY DEBT
**Severidade:** Medium
**Confiança:** Alta
**Status:** CONFIRMADO
**Prioridade sugerida:** P1
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `config/settings.py`, `config/settings_production.py`
**Linhas:** `config/settings.py:105-108`; `config/settings_production.py:3-25`
**Componente:** Banco e deployment

**Descrição:**

`config.settings_production` importa as configurações de `config.settings`, mas não substitui `DATABASES`. O perfil de produção ainda usa `db.sqlite3`.

**Evidência:**

```python
'ENGINE': 'django.db.backends.sqlite3'
'NAME': BASE_DIR / 'db.sqlite3'
```

**Cenário de risco:**

Produção pode operar com banco local no diretório da aplicação, sem separação de credenciais, grants mínimos, concorrência adequada ou estratégia operacional de backup.

**Impacto:**

Maior risco de exposição do inventário, corrupção/conflito de escrita e recuperação inadequada.

**Causa raiz:**

O perfil de produção altera headers e cookies, mas não define backend de dados de produção.

**Correção mínima segura:**

Configurar explicitamente PostgreSQL ou outro backend aprovado no ambiente de produção e falhar se SQLite for detectado.

**Código sugerido:**

```python
if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    raise ImproperlyConfigured(
        "SQLite não é permitido no perfil de produção."
    )
```

**Teste recomendado:**

Executar `check --deploy` com configuração de produção e verificar que SQLite é rejeitado.

### SEC-003 — Visual QA falha aberto quando sua flag é desativada

**Categoria:** VULNERABILITY
**Severidade:** Medium
**Confiança:** Alta
**Status:** CONFIRMADO
**Prioridade sugerida:** P1
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `core/management/commands/provision_visual_qa.py`, `core/middleware.py`
**Linhas:** `provision_visual_qa.py:10-18,94-111`; `middleware.py:18-44`
**Componente:** Identidade especial e autorização

**Descrição:**

A conta Visual QA recebe permissões de criação, edição e governança. A proteção de somente leitura depende de `DEBUG=True` e `VISUAL_QA_ENABLED=True`. Se a flag for desligada, o middleware retorna sem bloquear e a conta conserva as permissões de escrita.

**Evidência:**

- A conta recebe `add_camera`, `change_camera` e permissões de governança.
- `_is_visual_qa()` retorna `False` quando `VISUAL_QA_ENABLED` está desativado.
- Sem o middleware, as views normais autorizam as mutações.

**Cenário de risco:**

A conta criada para QA pode ser reutilizada em ambiente com a flag desativada e alterar câmeras, situações operacionais ou substituições.

**Impacto:**

Alteração indevida de inventário e quebra da garantia de identidade somente leitura.

**Causa raiz:**

A propriedade de segurança está implementada como configuração temporária, não como privilégio efetivo da conta.

**Correção mínima segura:**

Não conceder permissões de escrita à conta Visual QA. Separar autorização para exibir formulários de autorização para executar POST, ou desativar a conta após cada sessão de QA.

**Teste recomendado:**

Com `VISUAL_QA_ENABLED=False`, autenticar a conta e confirmar que todos os POSTs de mutação continuam retornando `403`.

### SEC-004 — Login sem throttling e com crescimento ilimitado de eventos de falha

**Categoria:** VULNERABILITY
**Severidade:** Medium
**Confiança:** Alta
**Status:** CONFIRMADO
**Prioridade sugerida:** P1
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `usuarios/views.py`, `cameras/models.py`
**Linhas:** `usuarios/views.py:35-37`; `cameras/models.py:321-373`
**Componente:** Autenticação e auditoria

**Descrição:**

Cada tentativa de login inválida registra um evento e retorna normalmente. Não há controle por IP, usuário, janela temporal, cooldown ou limite de tentativas.

**Cenário de risco:**

Um atacante pode automatizar brute force e gerar grande volume de registros persistentes de auditoria.

**Impacto:**

Aumento da probabilidade de comprometimento de contas e crescimento não limitado da tabela de auditoria, com possível degradação do banco.

**Causa raiz:**

O login possui auditoria, mas não possui mecanismo de abuso associado.

**Correção mínima segura:**

Adicionar throttling por combinação de usuário/IP, com resposta uniforme e política de retenção ou amostragem para falhas repetidas.

**Teste recomendado:**

Enviar tentativas inválidas repetidas e verificar bloqueio temporário, ausência de enumeração e preservação do login legítimo após a janela.

### SEC-005 — Campos textuais e payloads não possuem limites de tamanho de aplicação

**Categoria:** VULNERABILITY
**Severidade:** Medium
**Confiança:** Alta
**Status:** POTENCIAL
**Prioridade sugerida:** P2
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `cameras/models.py`, `cameras/forms.py`, `cameras/views.py`
**Linhas:** `models.py:67-71,145-149,273`; `forms.py:407-417`; `views.py:318-341,512-538`
**Componente:** Validação de entrada e DoS

**Descrição:**

Campos como `descricao_detalhada`, `observacoes` e `descricao` são `TextField` sem limite explícito. O formulário de observações de substituição também não define `max_length`.

**Cenário de risco:**

Usuário autenticado com permissão de escrita envia valores muito grandes repetidamente para aumentar consumo de memória, tempo de processamento e armazenamento.

**Impacto:**

Crescimento abusivo do banco e degradação de requisições.

**Causa raiz:**

Confiança em limites externos do servidor, sem limite explícito nos forms/modelos.

**Correção mínima segura:**

Definir `max_length` coerente nos forms e modelos, aplicar limite de corpo HTTP no servidor e limitar frequência de criação.

**Teste recomendado:**

Confirmar que payloads acima do limite retornam erro de validação e que textos dentro do limite continuam sendo salvos.

### SEC-006 — Mutação cadastral e evento de auditoria não são atômicos

**Categoria:** SECURITY DEBT
**Severidade:** Medium
**Confiança:** Alta
**Status:** CONFIRMADO
**Prioridade sugerida:** P2
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `cameras/views.py`, `usuarios/views.py`
**Linhas:** `cameras/views.py:321-338,516-535`; `usuarios/views.py:65-70`
**Componente:** Integridade da auditoria

**Descrição:**

As views salvam a alteração principal antes de criar o evento de auditoria. Se a criação do evento falhar, a alteração pode permanecer sem registro.

**Cenário de risco:**

Falha de banco, timeout ou erro de serialização durante a auditoria produz alteração efetiva com resposta de erro e sem trilha correspondente.

**Impacto:**

Perda de rastreabilidade e dificuldade de investigação de alterações críticas.

**Causa raiz:**

Ausência de `transaction.atomic()` envolvendo mutação e auditoria.

**Correção mínima segura:**

Envolver cada operação de mutação e seu `registrar_evento()` na mesma transação, permitindo rollback quando a auditoria falhar.

**Teste recomendado:**

Forçar falha controlada em `registrar_evento()` e confirmar que a alteração principal não permanece; testar também o caminho legítimo.

### SEC-007 — Gestão administrativa de usuários permite escalada de privilégio

**Categoria:** VULNERABILITY
**Severidade:** High
**Confiança:** Alta
**Status histórico:** CONFIRMADO
**Status atual:** REMEDIADO / VERIFIED
**Prioridade sugerida:** P0
**Baseline:** `26a8925c6968cf61551d524e233679a1a2771993`

**Arquivo:** `usuarios/management/commands/configurar_perfis_argos.py`
**Linhas:** aproximadamente `10-16`
**Componente:** Administração e separação de privilégios

**Descrição:**

O grupo `Administrador ARGOS` recebe `auth.change_user`, além de permissões para administrar grupos e usuários. O Django Admin padrão expõe campos de grupos, `is_staff`, `is_superuser` e permissões de usuário para usuários com alteração de usuários.

**Cenário de risco:**

A reprodução VERIFY confirmou:

- atacante ativo;
- `is_staff=True`;
- `is_superuser=False`;
- membro de `Administrador ARGOS`;
- POST pelo Django Admin real;
- promoção de outra conta a superuser;
- promoção da própria conta a superuser;
- alteração de `is_staff`;
- atribuição de grupo;
- atribuição arbitrária de `user_permissions`.

**Impacto:**

Escalada vertical e quebra de separação de funções. O controle backend atual não impede a escalada.

**Causa raiz:**

Permissão ampla de alteração de usuários sem `UserAdmin` restritivo específico para o perfil ARGOS.

**Correção mínima segura:**

Criar formulário administrativo restrito para gestão de usuários, removendo `is_superuser`, `is_staff` e atribuição arbitrária de permissões para administradores operacionais.

**Teste recomendado:**

Criar teste de regressão que confirme que um administrador ARGOS não consegue promover usuário a superusuário, promover a própria conta, alterar `is_staff`, atribuir grupos privilegiados ou atribuir permissões fora da política aprovada.

**Fechamento SEC-R01:**

SEC-007 foi confirmado historicamente e corrigido pelo commit `9b58885`
(`fix(security): restringir administracao de usuarios`). A regressão adversarial
SEC-R01C passou com 11 testes, a implementação SEC-R01B passou com 8 testes,
a suíte `usuarios` passou com 90 testes, o recorte `usuarios +
core.test_seguranca` passou com 120 testes e a suíte global passou com 588
testes. O VERIFY independente passou; o exploit original não é mais
reproduzível. Não apagar este histórico: SEC-007 não é vulnerabilidade
atualmente aberta.

### SEC-008 — PerfilUsuarioAdmin expõe perfis protegidos por ID direto

**Origem:** VERIFY-01
**Categoria:** SECURITY DEBT
**Severidade:** Medium
**Confiança:** Alta
**Status:** CONFIRMADO

Administrador ARGOS recebe HTTP 200 ao acessar por ID direto o perfil associado
a superuser e o próprio `PerfilUsuario`. O `PerfilUsuarioAdmin` não aplica
queryset por objeto, `has_view_permission` por objeto,
`has_change_permission` por objeto ou `can_manage_user`. O impacto confirmado é
exposição de dados administrativos de contas protegidas. Não houve escalada nem
mutação persistida durante o VERIFY.

### SEC-009 — Edição de PerfilUsuarioAdmin falha com erro interno

**Origem:** VERIFY-02
**Categoria:** HARDENING
**Severidade:** Medium
**Confiança:** Alta
**Status:** CONFIRMADO

POST de edição de `PerfilUsuario` alcança `save_model` e retorna HTTP 500 por
`NameError`: o símbolo `calcular_alteracoes` não está definido em
`usuarios/admin.py`. O fluxo transacional dos probes impediu persistência.
O impacto é função administrativa quebrada e mascaramento da ausência de
autorização por objeto. SEC-009 não é reabertura do SEC-007.

### SEC-010 — Correção isolada do PerfilUsuarioAdmin pode permitir mutação privilegiada

**Origem:** VERIFY-03
**Categoria:** ARCHITECTURAL RISK
**Severidade:** Medium
**Confiança:** Alta
**Status:** POTENCIAL

Se o erro de SEC-009 for corrigido sem controle por objeto, um Administrador
ARGOS poderá potencialmente alterar o próprio `PerfilUsuario`, o perfil de um
superuser ou o perfil de outra conta protegida. A futura correção deve
reutilizar a política fail-closed existente para administração de usuários.

## Hardening recomendado

- Adicionar CSP compatível com os templates atuais.
- Avaliar MFA para administradores; sua ausência isolada não foi classificada como vulnerabilidade.
- Fixar GitHub Actions por SHA em vez de tags móveis (`checkout@v6`, `setup-python@v6`).
- Considerar hashes de artefatos em dependências.
- Rejeitar explicitamente `ALLOWED_HOSTS="*"` em produção.
- Definir retenção e proteção operacional dos eventos de auditoria.
- Ativar HSTS preload somente após validação de todos os subdomínios.
- Não implementar monitoramento, captura, SSRF ou uploads sem preservar o ADR-021 e as fronteiras de segurança existentes.

## Débitos de segurança

- Deployment, proxy reverso, firewall, backup e restore não estão definidos no repositório.
- PostgreSQL de produção ainda não está configurado.
- Não há política de rate limiting ou retenção de auditoria.
- Não há testes de carga para endpoints de consulta e escrita.
- Não há API, upload ou worker executável no baseline auditado.

## Dependências vulneráveis

Nenhuma vulnerabilidade conhecida foi encontrada por `pip-audit` nas dependências declaradas.

Isso não substitui atualização planejada nem validação de dependências transitivas em cada release.

## Configurações inseguras ou pendentes

- `config.settings` é apropriado apenas para desenvolvimento local.
- `config.settings_production` passou no `check --deploy` com HSTS preload ativado.
- Com HSTS preload desativado, o Django emite `security.W021`.
- O perfil de produção ainda herda SQLite.
- Não existe configuração de infraestrutura que imponha o perfil de produção.

## DECISÕES REQUERIDAS DA GOVERNANÇA

### GOV-SEC-01

**Finding relacionado:** SEC-001, SEC-002
**Decisão necessária:** definir contrato obrigatório de inicialização de produção e backend de banco.
**Alternativas:** validação fail-closed no settings; enforcement no deployment; ambos.
**Impacto:** pode exigir ajuste de deployment e configuração de banco.
**Recomendação:** exigir ambos antes da homologação.

### GOV-SEC-02

**Finding relacionado:** SEC-003
**Decisão necessária:** definir se Visual QA continuará precisando abrir telas protegidas de escrita.
**Alternativas:** conta estritamente read-only; permissões GET separadas das permissões POST; conta temporária destruída após QA.
**Impacto:** possível ajuste no contrato documentado de Visual QA.
**Recomendação:** não depender exclusivamente do middleware; preservar somente leitura como propriedade da conta.

### GOV-SEC-03

**Finding relacionado:** SEC-004
**Decisão necessária:** definir política de brute force e retenção de falhas de login.
**Alternativas:** throttling na aplicação; controle no proxy; combinação de ambos.
**Impacto:** exige política de bloqueio, observabilidade e suporte operacional.
**Recomendação:** aplicar controle no proxy e na aplicação, sem enumerar usuários.

### GOV-SEC-04

**Finding relacionado:** SEC-005, SEC-006
**Decisão necessária:** definir limites de conteúdo e requisito de atomicidade da auditoria.
**Alternativas:** limites apenas no formulário; limites no formulário e modelo; transação obrigatória para toda mutação auditável.
**Impacto:** limites no modelo podem exigir migration.
**Recomendação:** limites em todas as camadas e rollback quando a auditoria falhar.

## Security Gate

**SECURITY GATE: BLOCKED**

**Motivo:**
SEC-007 não mantém mais o gate bloqueado: está REMEDIADO / VERIFIED. O gate
permanece BLOCKED devido ao novo front SEC-R02, que trata SEC-008, SEC-009 e
SEC-010.

## SEC-R02 — Endurecimento do PerfilUsuarioAdmin

SEC-R02 foi aberto formalmente para tratar conjuntamente SEC-008, SEC-009 e
SEC-010. A sequência prevista é: SEC-R02A Discovery, SEC-R02B Implementação,
SEC-R02C Regressão, VERIFY independente e decisão do Security Gate. Esta tarefa
não implementa SEC-R02 e não antecipa sua solução definitiva.

Na Discovery deverão ser avaliados queryset, permissões por objeto, acesso ao
próprio perfil, perfil de superuser, perfil de outro Administrador ARGOS, POST
direto por ID, `save_model`, `calcular_alteracoes`, auditoria, atomicidade e
comportamento legítimo do administrador.

Como risco residual de implantação, `configurar_perfis_argos` deve ser
executado de forma controlada em cada banco existente para reconciliar
`Group.permissions`. O comando não deve remover automaticamente
`is_superuser`, `is_staff` ou `user_permissions` individuais. Antes de
produção/homologação deve existir inventário das contas historicamente
privilegiadas e decisão humana sobre eventual remediação; não fazer demotion
automática.

## Integridade da auditoria

Arquivos untracked pertencentes a trabalhos em andamento foram preservados e não foram usados para confirmar findings. Não houve staging, commit, push ou alteração funcional durante a criação deste relatório.

O baseline auditado `26a8925` correspondia a 541 testes. Durante a auditoria original, a working tree possuía 569 testes; os 28 adicionais pertenciam ao laboratório MON-04C e estavam untracked naquele momento. Posteriormente, MON-04C foi versionada/publicada no commit `9cf1964`. Por isso, 569 não era a contagem canônica do baseline `26a8925`.

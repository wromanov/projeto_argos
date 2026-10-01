# Contrato de acesso, papéis e autorização

```text
ID = BC-AUTH
STATUS = IMPLEMENTATION_READY / BC-02
IMPLEMENTATION = PARTIAL / DJANGO PERMISSIONS AND GROUPS; FOUR-ROLE EXTENSION READY
BC02_STATUS = IMPLEMENTATION_READY
IMPLEMENTATION_READY = YES
IMPLEMENTER_TARGET = LUNA
```

## Identidade e decisão de acesso

O ARGOS usa a identidade configurada por `AUTH_USER_MODEL` e o sistema de permissões Django. As permissões efetivas podem vir de atribuição direta ou grupo; a view deve verificar permissão no servidor em cada operação. Esconder controles na UI não é autorização. Este contrato não cria RBAC paralelo nem presume tenant/escopo por organização que o modelo atual não represente.

No baseline BC-00, o comando `python manage.py configurar_perfis_argos` reconciliava `Monitoramento ARGOS`, `Operador ARGOS` e `Administrador ARGOS`. A decisão vinculante BC-02 abaixo acrescenta `Técnico ARGOS` e redefine a matriz. `Administrador` não equivale automaticamente a `is_superuser`. Superusuários mantêm o comportamento administrativo privilegiado do Django, limitado por controles próprios do admin.

## Permissões observadas

| Capacidade | Permissão Django observada |
|---|---|
| Consultar câmera | `cameras.view_camera` |
| Criar/alterar câmera | `cameras.add_camera`, `cameras.change_camera` |
| Alterar situação operacional | `cameras.alterar_situacao_camera` |
| Desativar/reativar | `cameras.desativar_camera`, `cameras.reativar_camera` |
| Registrar substituição | `cameras.registrar_substituicao_camera` |
| Consultar eventos/substituições | `cameras.consultar_eventos`, `cameras.consultar_substituicoescamera` e permissões view correspondentes |
| Enviar imagem manual | `cameras.add_cameraimagerecord` |

Os grupos devem ser sincronizados pela command canônica, não mantidos por alterações divergentes no admin. A política detalhada de contas administrativas está em `usuarios/admin_security.py` e no app `usuarios`.

## Separação de capacidades

Consultar estado de saúde (`view_camera` e permissões de histórico) não concede permissão para alterar configuração técnica, revelar credenciais, executar probe sob demanda, iniciar captura, enviar imagem ou administrar o worker. A capacidade de captura deverá ser uma permissão distinta da capacidade de monitoramento. O usuário web nunca escolhe alvo, URL, endereço, porta, path ou credencial para conexão a equipamento.

O acesso ao preview privado atual usa autenticação e `cameras.view_camera`; upload usa `cameras.add_cameraimagerecord`. A rota e o serviço devem repetir as verificações no backend, responder sem divulgar existência de storage/segredo além dos estados previstos no contrato de imagem e registrar auditoria para mutações relevantes.

## Controles para operações futuras

Antes de habilitar gestão de credencial, editar perfil/capacidade, captura direta, rotação ou execução manual de probe, definir permission codenames explícitos, matriz por grupo, objeto/escopo aplicável, CSRF para mutações web, auditoria sanitizada e teste de negação para anônimo/usuário sem permissão. Worker é identidade de serviço, não usuário humano nem conta admin; sua autorização técnica não decorre de grupo Django.

## Limites e referências

SSO, MFA, autorização por tenant, segregação organizacional e delegação de credenciais permanecem fora do BC-02. O privilégio de captura é fechado abaixo. Fonte de implementação: `usuarios/management/commands/configurar_perfis_argos.py`, `usuarios/admin_security.py`, `cameras/views.py`, `cameras/imagens/upload_service.py` e `cameras/models.py`. Segurança do worker e dos segredos: `ADR-021_seguranca_capacidade_monitoramento.md` §§3–9.

## BC-02 — decisão vinculante que substitui a matriz de três grupos acima

Os quatro grupos são `Monitoramento ARGOS`, `Operador ARGOS`, `Técnico ARGOS`
e `Administrador ARGOS`. A command `configurar_perfis_argos` deve reconciliar
os quatro de forma idempotente, sem promover usuários existentes por inferência.
`Técnico ARGOS` entra na allowlist de grupos operacionais protegidos em
`usuarios/admin_security.py`; isso não lhe concede administração. Administrador
não equivale a superuser e preserva as proteções de contas existentes.

| Domínio / capacidade | Monitoramento | Operador | Técnico | Administrador |
|---|:---:|:---:|:---:|:---:|
| Inventário, atividades, eventos, substituições, health resumido | leitura | leitura | leitura | leitura |
| Cadastro permitido, notas/atividades, transições e substituição | — | escrita | escrita | escrita |
| Upload manual | — | escrita | escrita | escrita |
| URI RTSP sanitizada, sem username/password | — | leitura | leitura | leitura |
| Editar conexão RTSP/perfil/capability | — | — | escrita | escrita |
| Ver metadados/username de credencial | — | — | leitura | leitura |
| Alterar/rotacionar/revogar credencial; revelar senha | — | — | escrita/reveal | escrita/reveal |
| Testar conexão A→B→C→D; diagnóstico detalhado | — | — | execução/leitura | execução/leitura |
| Captura direta | — | — | execução | execução |
| Política global de destino e administração do runtime | — | — | — | gestão |
| Usuários, perfis humanos e sistema | — | — | — | administração |

Permissões customizadas novas em `Camera.Meta.permissions`: `view_camera_connection`,
`change_camera_connection`, `manage_camera_capability`,
`view_camera_credential`, `change_camera_credential`,
`reveal_camera_credential`, `run_camera_connection_test`,
`view_camera_diagnostic`, `capture_camera_image`,
`manage_camera_target_policy`, `manage_monitoring_runtime`. As permissões
existentes de inventário, atividades, eventos e upload mantêm seu significado;
`add_cameraimagerecord` não concede captura direta. Permissões administrativas
continuam em `auth`/`usuarios`, sem delete. Permissões diretas Django continuam
efetivas, mas a command configura apenas os defaults da tabela.

Técnico opera a configuração técnica de câmera, sem gerir usuários, policy
global de rede ou runtime administrativo do sistema. Essas duas permissões
globais pertencem somente ao grupo Administrador por default.

Cadastro (`CameraForm`), conexão (`CameraConnectionConfig`), credencial,
diagnóstico e administração são fronteiras distintas. Campo técnico/sensível
não entra no formulário cadastral nem em serializer genérico. Alteração de IP
cadastral que muda destino efetivo deve revalidar a policy e auditar.
Autenticação e `has_perm` são verificados em cada view **e** service com
`camera_id`; esconder controle na UI não autoriza. Worker usa identidade de
serviço, não Group Django. URI entregue ao Operador é `rtsp://IPv4[:porta]/path`
sem segredo. Username só é mostrado a Técnico/Admin em fluxo técnico autorizado.
Reveal exige POST, CSRF, `reveal_camera_credential`, reautenticação recente,
resposta `no-store` e auditoria; senha não entra em HTML inicial, URL ou log.
Na stack local, reautenticação é confirmação da senha atual do próprio ator
via backend Django `authenticate` em cada reveal, sem guardar o valor na
sessão. Conta sem senha utilizável não revela até existir mecanismo aprovado.

Criar/alterar URI/perfil/credencial, reveal, teste manual, captura e mudança de
policy auditam ator, câmera, ação, horário, versão, resultado e correlação
opaca, sem username, senha, URI completa, path sensível ou payload. Mutação e
auditoria são atômicas; falha de auditoria reverte mutação. Consumo normal de
credencial por worker não cria evento funcional por probe.

```text
MODEL_CHANGE = Camera.Meta.permissions
MIGRATION_REQUIRED = YES / AlterModelOptions; no new domain column
EXPECTED_MODELS = Camera; existing Django Group and Permission
RELATIONSHIPS = existing Group ↔ Permission
CONSTRAINTS = unique codename per content type
INDEXES = existing Django auth indexes
DATA_MIGRATION = NO; idempotent command reconciles group grants
ROLLBACK_CONSIDERATION = revoke grants before removing codenames; preserve users
EXPECTED_PRIMARY_FILES = cameras/models.py; usuarios/management/commands/configurar_perfis_argos.py;
                         usuarios/admin_security.py
EXPECTED_NEW_FILES = cameras/integracao/authorization.py or equivalent service
EXPECTED_TEST_FILES = usuarios/test_perfil.py; usuarios/test_admin_sec_r02c.py;
                      cameras/test_governanca_views.py; focused deny tests
SHARED_FILES = cameras/models.py; migrations; views/urls on integration
STOP_AND_ESCALATE_TO_SOL_IF = new product role semantics; protected-user rule
                              conflicts with this matrix; scope beyond four roles
```

Acceptance criteria:

1. Dado cada grupo, quando a command roda duas vezes, a matriz final é
   idêntica, sem delete ou promoção de usuários.
2. Dado Monitoramento/Operador, editar conexão/credencial, reveal, teste e
   captura são negados pela view e pelo service sem tocar rede/segredo.
3. Operador lê somente URI sanitizada; Técnico/Admin com permissão executa
   ações separadas, cada uma com auditoria sanitizada; reveal sem confirmação
   válida da senha do ator é negado.
4. Técnico não administra usuário/sistema; Administrador mantém proteções de
   contas; falha da auditoria reverte mutação.

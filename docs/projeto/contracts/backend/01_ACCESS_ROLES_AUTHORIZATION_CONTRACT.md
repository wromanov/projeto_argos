# Contrato de acesso, papéis e autorização

```text
ID = BC-AUTH
STATUS = ACTIVE / BASELINE BC-00
IMPLEMENTATION = PARTIAL / DJANGO PERMISSIONS AND GROUPS
```

## Identidade e decisão de acesso

O ARGOS usa a identidade configurada por `AUTH_USER_MODEL` e o sistema de permissões Django. As permissões efetivas podem vir de atribuição direta ou grupo; a view deve verificar permissão no servidor em cada operação. Esconder controles na UI não é autorização. Este contrato não cria RBAC paralelo nem presume tenant/escopo por organização que o modelo atual não represente.

O comando `python manage.py configurar_perfis_argos` reconcilia os grupos operacionais e suas permissões. Os nomes canônicos são `Monitoramento ARGOS`, `Operador ARGOS` e `Administrador ARGOS`; `Administrador` não equivale automaticamente a `is_superuser`. Superusuários mantêm o comportamento administrativo privilegiado do Django, limitado por controles próprios do admin.

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

Não há decisão neste baseline para SSO, MFA, autorização por tenant, segregação organizacional, delegação de credenciais ou privilégio de captura. Fonte de implementação: `usuarios/management/commands/configurar_perfis_argos.py`, `usuarios/admin_security.py`, `cameras/views.py`, `cameras/imagens/upload_service.py` e `cameras/models.py`. Segurança do worker e dos segredos: `ADR-021_seguranca_capacidade_monitoramento.md` §§3–9.

# ARGOS-CRED-UI-01 — integração HTTP/SSR (DRAFT)

```text
CONTRACT_STATUS = DRAFT
TECHNICAL_PROPOSAL = READY_FOR_REVIEW
HUMAN_APPROVAL = PENDING
DJANGO_IMPLEMENTATION = NOT_STARTED
AUTHORITY = PROPOSAL_ONLY / DOES_NOT_SUPERSEDE CAM-INT-02, CAM-INT-02-R1 OR BC-AUTH
SCOPE = SERVER_RENDERED CAMERA CREDENTIAL MANAGEMENT
```

Este rascunho registra a recomendação arquitetural e a adjudicação do root para revisão humana. Rotas e fluxos marcados `PROPOSED / NOT_IMPLEMENTED` não existem hoje. CAM-INT-02, CAM-INT-02-R1, BC-AUTH e authorities de roadmap continuam prevalecendo.

## 1. Propósito e escopo

Descrever integração Django SSR mínima para administrar credenciais por câmera reutilizando os serviços de domínio existentes. Não implementar código, schema, API JSON nova, integração operacional, deploy ou E2. A tela de edição atual mantém os campos cadastrais separados da configuração de credencial.

## 2. Capacidades existentes e evidência

| Capacidade | Estado verificado |
|---|---|
| Serviço de metadados | `credential_metadata` existe em `cameras/integracao/credentials.py`; exige `view_camera_credential` no service. Atualmente retorna `configured`, `username`, `key_version`, `updated_at` e `version` quando o ponteiro seleciona uma versão ACTIVE; para ausente, sem ponteiro ou versão não ativa retorna apenas `configured=False`. Não valida o estado do owner da credencial. |
| Criar/substituir | `replace_camera_credential` existe; exige `change_camera_credential`, opera atomicamente, valida encrypt/decrypt round-trip, ativa versão nova, preserva a anterior em falha anterior à ativação e audita sucesso. |
| Revogar | `revoke_camera_credential` existe; exige `change_camera_credential`, marca a ativa `REVOKED`, limpa o ponteiro e audita sucesso em transação; não faz fallback. |
| Reveal | Endpoint existente `POST /<camera_id>/credentials/reveal/`, nome `reveal_camera_credential`; comportamento atual descrito em §7 e preservado. |
| Editar câmera | `GET/POST /<pk>/editar/`, nome `editar`, view `editar_camera`, exige `cameras.change_camera`; usa `CameraEdicaoForm` e `cameras/templates/cameras/formulario.html`. |

Evidência: `cameras/integracao/credentials.py` (`credential_metadata`, `replace_camera_credential`, `reveal_camera_credential`, `revoke_camera_credential`); `cameras/credential_views.py`; `cameras/urls.py`; `cameras/views.py`; testes de credenciais e autorização existentes. Services existentes não comprovam endpoints HTTP de metadata, replace ou revoke.

## 3. Operações HTTP propostas

### 3.1 Metadados na edição existente — proposta

`GET /<pk>/editar/` permanece a rota de edição existente e continua protegida por `cameras.change_camera`. Dentro da view, consultar metadados somente quando o ator também tem `cameras.view_camera_credential`; o service repete a autorização para a câmera. Sem essa permissão, omitir o painel e todos seus dados. Usuário sem `change_camera` recebe 403 conforme a proteção existente; câmera ausente para ator autorizado recebe 404.

Projeção mínima proposta no SSR: somente `configured: boolean` e rótulo genérico que não permita inferir a existência de versão revogada. Não enviar username, `key_version`, versão nem timestamp sem decisão humana justificada. Não expor diferença entre credencial inexistente, inativa e revogada. Nenhuma senha/ciphertext deve ser obtida ou inserida no HTML inicial.

**Gap de contrato/serviço:** o service atual descriptografa username para metadados e devolve campos além do mínimo; também agrupa ausente/sem ponteiro/versão não ativa como `configured=False` e não valida o estado do owner da credencial. A distinção de estado revogado não está disponível. O uso SSR deve aguardar ajuste/fechamento da projeção no contrato de serviço; este rascunho não declara tal ajuste implementado nem decide nova semântica.

### 3.2 Criar/substituir — `PROPOSED / NOT_IMPLEMENTED`

```text
METHOD = POST
PATH = /<camera_id>/credentials/
NAME = replace_camera_credential
PERMISSION = cameras.change_camera_credential
PAYLOAD = username, password
```

Ambos os campos são obrigatórios. Limites observados no serviço/schema: username até 255 caracteres e password até 1024. Campos adicionais, IDs de versão, versão ativa, chave ou ciphertext não são aceitos do browser. View e service devem validar autorização no servidor; CSRF é obrigatório. Chamar `replace_camera_credential(actor, camera_id, username, password, request)`.

O service já realiza persistência de versões e vínculo em `transaction.atomic`, cifragem e validação round-trip, troca do ponteiro e auditoria de sucesso. Uma submissão duplicada pode criar versão adicional; idempotência não é garantida. Não prometer deduplicação. Após sucesso, padrão POST/Redirect/GET para `editar` com mensagem genérica, sem refletir valores submetidos. Erro de validação deve renderizar erro SSR sanitizado (400 proposto); falha operacional de custódia/chave deve mostrar mensagem genérica de indisponibilidade (503 ou estado seguro na página, decisão de transporte a revisar). Exceções inesperadas geram resposta genérica 500, sem detalhes internos.

**Gap:** BC-AUTH documenta atomicidade entre mutação e auditoria e rollback em falha de auditoria. A inspeção do service confirmou chamada de auditoria, mas não confirmou tratamento/rollback de falha de auditoria. Não duplicar auditoria na view e não declarar esse requisito satisfeito; resolver antes da aprovação final.

### 3.3 Revogar — `PROPOSED / NOT_IMPLEMENTED`

```text
METHOD = POST
PATH = /<camera_id>/credentials/revoke/
NAME = revoke_camera_credential
PERMISSION = cameras.change_camera_credential
PAYLOAD = none
```

Exigir CSRF e autorização de servidor em view e service. A UX deve pedir confirmação antes do POST. Chamar `revoke_camera_credential(actor, camera_id, request)`. O service atual revoga a versão ativa e limpa o ponteiro em transação, sem fallback. Sem credencial ativa, `CREDENTIAL_NOT_CONFIGURED` é o resultado do service; a proposta mapeia a conflito de estado 409 com mensagem genérica, sujeito a revisão. Após sucesso, PRG para editar e feedback genérico. Validation 400; erro operacional 503 ou estado seguro; falha inesperada 500 genérica. A confirmação e o POST devem continuar protegidos contra submissão CSRF.

**Gap:** não há endpoint HTTP de revoke, nem estado distinguindo “nunca configurada” de “revogada” na projeção atual.

## 4. Permissões e respostas

| Situação | Tratamento proposto/observado |
|---|---|
| GET editar sem `change_camera` | 403, comportamento atual da view decorada. |
| Camera inexistente em operação autorizada | 404; não revelar dados da credencial. |
| Painel de metadados sem `view_camera_credential` | Omitido no SSR; tentativa direta ao service é negada; endpoint futuro, se houver, retornaria 403. |
| POST replace/revoke sem `change_camera_credential` | 403 em view e service; UI não substitui autorização. |
| Reveal sem `reveal_camera_credential` | 403 atual. |
| Validação de input | Erro SSR sanitizado; POST proposta 400. Não refletir segredo em mensagens. |
| Reveal sem credencial configurada | 404 atual com `CREDENTIAL_NOT_CONFIGURED`. |
| Reveal com reautenticação inválida | 403 atual com `REAUTHENTICATION_FAILED`. |
| Reveal outro `CredentialOperationError` | 400 atual; corpo JSON contém somente código seguro. |
| Erro de chave/decrypt ou serviço operacional nos novos fluxos | Resposta/estado genérico seguro; proposta 503 para POST, sujeito à revisão. Não divulgar existência, chave, detalhe ou stack. |
| Exceção inesperada | 500 genérica sem conteúdo interno. |

**PENDING_USER_DECISION:** código/status uniforme para erros operacionais novos e mensagens finais; distinção futura de credencial revogada; visibilidade de username; política de falha/atomicidade de auditoria.

## 5. CSRF, cache e auditoria

Todos os POST mutáveis e reveal usam CSRF. Replace e revoke não devem ser aceitos por GET. Não colocar segredo em query, URL, logs, body logging, session, cache, analytics, telemetria ou auditoria. A página SSR que contém metadados de credencial e todas as respostas das ações devem usar `Cache-Control: no-store` e diretivas equivalentes contra armazenamento; resposta de reveal preserva exatamente as diretivas `no-store` atuais. Auditoria pertence aos services; não duplicar na view. Eventos devem permanecer sanitizados segundo CAM-INT-02 e BC-AUTH.

## 6. Integração com `CameraEdicaoForm`

O gerente de credenciais é uma unidade irmã e independente da edição cadastral. Não aninhar formulários HTML. O POST cadastral existente salva somente `CameraEdicaoForm`; POST replace/revoke não instancia nem salva esse formulário. Credencial tem persistência própria pelo service. Ao tentar credencial/reveal enquanto o formulário da câmera tem alterações não salvas, a interface deve avisar e permitir resolver a edição antes da ação; em navegação sem JavaScript, usar fluxo explícito de confirmação/submit sem misturar payloads. Não alterar campos ou semântica de `Camera` como efeito lateral. Não modificar CSS global sem aprovação; não redesenhar regiões protegidas.

## 7. Reveal existente — preservação

Manter `POST /<camera_id>/credentials/reveal/` e o nome atual. Código verificado aplica `@never_cache`, `@require_POST`, `@csrf_protect`, autenticação, service permission `reveal_camera_credential`, reautenticação pela senha atual em cada requisição, auditoria sanitizada e cabeçalhos `Cache-Control: no-store, no-cache, must-revalidate, private`, `Pragma: no-cache`, `Expires: 0`. O endpoint devolve JSON com segredo somente após ação explícita e autorização; não redesenhar nem consumir reveal como leitura de metadata. No UI, pedir reautenticação em cada reveal e mostrar segredo só transitoriamente, sob autorização, sem persistência browser-side.

## 8. Limites de dados e segurança

- Browser controla somente `username` e `password` para replace; revoke não recebe payload.
- Não aceitar `camera_id` de corpo como authority sobre a rota, nem IDs/version/key/ciphertext.
- Não serializar segredo no render inicial, hidden input, `data-*`, fixture, URL ou storage do browser.
- Username é dado sensível e não aparece em telemetria/auditoria; exibição ainda depende de decisão humana.
- `key_version`, ciphertext e senha não são necessários no SSR ordinário.
- Serviço verifica a permissão Django no contexto do `camera_id`; o contrato atual não define ownership/tenant por usuário. Esconder botões não autoriza operação.
- Mutação não altera configuração cadastral nem vínculo operacional além do lifecycle contratado.
- Erros públicos são allowlisted e sanitizados; logs não recebem payload de segredo.

## 9. Matriz de estados UI/HTTP

| Estado | Origem | Apresentação proposta |
|---|---|---|
| Sem permissão de metadata | Django permission | Painel oculto; servidor continua negando operação direta. |
| Sem credencial ativa / estado desconhecido | `configured=False` atual | Rótulo genérico; não afirmar “revogada”. |
| Ativa | `configured=True` após projeção mínima aprovada | Status de configuração, sem username/key/version por padrão. |
| Envio em andamento | Interface | Indicar progresso; evitar submissões concorrentes onde possível, sem alegar idempotência de servidor. |
| Replace sucesso | Service + redirect | PRG e confirmação genérica. |
| Validação rejeitada | Validador | Erro de campo sanitizado sem reexibir password. |
| 403 | Autorização | Mensagem de acesso negado sem revelar estado da credencial. |
| 404 | Recurso | Recurso indisponível; sem detalhes de credencial. |
| 409 revoke stale | Service `CREDENTIAL_NOT_CONFIGURED` | Estado mudou; atualizar página. |
| Indisponibilidade | Erro operacional | Mensagem segura, permitir nova tentativa conforme operação. |
| Confirmação de revoke | Ação explícita | Confirmar consequência; sem executar até POST. |
| Formulário Camera sujo | Estado client-side | Alertar antes de gestão/reveal; não descartar silenciosamente alterações. |
| Reveal | Endpoint existente | Reauth por requisição; resultado transitório, no-store. |

## 10. Transações e persistência

Replace/revoke delegam toda persistência a services transacionais existentes. A view não faz escrita ORM para credencial. A edição da Camera tem seu fluxo transacional próprio. Não combinar os dois domínios em uma transação ou submit HTML. A existência da transaction no service não atesta atomicidade de auditoria; gap em §3.2.

## 11. Testes esperados na implementação futura

Sem executar ou declarar testes nesta atividade. A futura implementação deve cobrir: permissão em view e service; 403/404 sem vazamento; GET metadata apenas para atores autorizados e projeção allowlist; formulário cadastral inalterado em POST de credencial; CSRF e métodos; replace/revoke chamando services com `request`; PRG; validação e erros sanitizados; transação/auditoria conforme contrato fechado; duplicação explicitamente tratada sem prometer idempotência; reveal regression com POST, CSRF, reauth por chamada e `no-store`; HTML/cache/log sem segredo; confirmação e estado dirty; acessibilidade e responsividade. Testes existentes são referências, não evidência de integração HTTP nova.

## 12. Aprovação, gaps e fora de escopo

Condições para aprovação: fechar gaps de projeção metadata, auditoria atômica, semântica/status de erros e decisões de visibilidade/confirm UX; revisar rotas e mensagens com autoridade humana; confirmar compatibilidade com CAM-INT-02, R1, BC-AUTH e layout aprovado.

`CONTRACT_GAPS`: service metadata descriptografa/devolve username/key_version/version/timestamp e não distingue revogada; rollback diante de falha de auditoria não foi verificado na implementação; replace duplicado não tem idempotência; mapping de falhas operacionais novas precisa aprovação.

`PENDING_USER_DECISION`: mostrar ou não username; eventual representação de revogada; política de confirmação final de revoke e alerta de formulário dirty; status e conteúdo final dos erros operacionais.

Fora do escopo: nova SPA/JSON API; mudança CAM-INT-02, CAM-INT-02-R1 ou BC-AUTH; novos serviços, modelos ou migrations; reautenticação diferente no reveal; endpoint, teste real de conexão, alteração de câmera, exposição de username por padrão, teste de câmera real, homologação, E2, deploy e implementação Django.

## 13. Referências

- `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md`
- `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`
- `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` (BC-AUTH)
- `cameras/integracao/credentials.py`; `cameras/credential_views.py`; `cameras/urls.py`; `cameras/views.py`; `cameras/authorization.py`
- `cameras/test_camera_credentials.py`; `cameras/test_authorization.py`
- `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`; `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md`; `COMPONENT_CATALOG.md`; `STATE_MATRIX.md`
- `docs/projeto/ARGOS_DELIVERY_EXECUTION_PLAN_V1.md`; Roadmap §25; Sprints §22

## 14. Registro da adjudicação

Root aprovou a arquitetura somente como `DRAFT FOR HUMAN REVIEW`. O perfil efetivo do arquiteto foi GPT-6 Sol/High; o pedido indicava GPT-6.1 Sol/High, indisponível no runtime. E1 segue apenas preparação deste contrato/handoff; aprovação humana pendente e implementação não iniciada.

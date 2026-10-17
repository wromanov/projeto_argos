# ARGOS-CRED-UI-01 — contrato de integração HTTP/SSR

```text
CONTRACT_STATUS = RATIFIED_FOR_E1
TECHNICAL_PROPOSAL = RATIFIED_BY_USER_ADDENDUM
HUMAN_APPROVAL = PASS / CARD B + TECHNICAL-VISUAL ADDENDUM
DJANGO_IMPLEMENTATION = IMPLEMENTED / TARGETED_VALIDATION_PASS
DJANGO_VISUAL_CONFORMANCE = PASS
DJANGO_HUMAN_VISUAL_APPROVAL = PASS / 2026-10-17
AUTHORITY = SLICE-SPECIFIC / SUBORDINATE TO CAM-INT-02, CAM-INT-02-R1 AND BC-AUTH
SCOPE = SERVER_RENDERED CAMERA CREDENTIAL MANAGEMENT
```

Este contrato materializa as decisões aprovadas no CARD B e no adendo técnico/visual. Rotas explicitamente novas são implementadas nesta slice. CAM-INT-02, CAM-INT-02-R1, BC-AUTH e authorities de roadmap continuam prevalecendo; nenhum contrato canônico superior é alterado.

## 1. Propósito e escopo

Descrever integração Django SSR mínima para administrar credenciais por câmera reutilizando os serviços de domínio existentes. Não implementar código, schema, API JSON nova, integração operacional, deploy ou E2. A tela de edição atual mantém os campos cadastrais separados da configuração de credencial.

## 2. Capacidades existentes e evidência

| Capacidade | Estado verificado |
|---|---|
| Serviço de metadados | `credential_metadata` existe em `cameras/integracao/credentials.py`; exige `view_camera_credential` no service, mas atualmente descriptografa username e retorna também `key_version`, `updated_at` e `version`. Não será usado diretamente para a projeção SSR. |
| Criar/substituir | `replace_camera_credential` existe; exige `change_camera_credential`, opera atomicamente, valida encrypt/decrypt round-trip, ativa versão nova, preserva a anterior em falha anterior à ativação e audita sucesso. |
| Revogar | `revoke_camera_credential` existe; exige `change_camera_credential`, marca a ativa `REVOKED`, limpa o ponteiro e audita sucesso em transação; não faz fallback. |
| Reveal | Endpoint existente `POST /<camera_id>/credentials/reveal/`, nome `reveal_camera_credential`; comportamento atual descrito em §7 e preservado. |
| Editar câmera | `GET/POST /<pk>/editar/`, nome `editar`, view `editar_camera`, exige `cameras.change_camera`; usa `CameraEdicaoForm` e `cameras/templates/cameras/formulario.html`. |

Evidência: `cameras/integracao/credentials.py` (`credential_metadata`, `replace_camera_credential`, `reveal_camera_credential`, `revoke_camera_credential`); `cameras/credential_views.py`; `cameras/urls.py`; `cameras/views.py`; testes de credenciais e autorização existentes. Services existentes não comprovam endpoints HTTP de metadata, replace ou revoke.

## 3. Operações HTTP propostas

### 3.1 Metadados na edição existente — ratificado

`GET /<pk>/editar/` permanece a rota de edição existente e continua protegida por `cameras.change_camera`. Dentro da view, consultar metadados somente quando o ator também tem `cameras.view_camera_credential`; o service repete a autorização para a câmera. Sem essa permissão, omitir o painel e todos seus dados. Usuário sem `change_camera` recebe 403 conforme a proteção existente; câmera ausente para ator autorizado recebe 404.

Projeção SSR: somente `configured: true | false`, representando uma credencial ativa utilizável segundo o lifecycle persistido; não representa conectividade testada. Validar credencial pertencente à câmera, owner correspondente, ponteiro/versão ativa coerentes e permissão `view_camera_credential`. Não descriptografar username. Não enviar username, senha, ciphertext, `key_version`, timestamps ou versões internas. Não expor diferença entre revogada e nunca configurada. Implementar projeção SSR específica e segura, preservando a resposta e compatibilidade dos consumidores atuais de `credential_metadata`.

**Compatibilidade:** `credential_metadata` permanece inalterado para seus consumidores existentes. A nova projeção não cria endpoint de metadata e usa o GET existente de edição.

### 3.2 Criar/substituir — endpoint novo desta slice

```text
METHOD = POST
PATH = /<camera_id>/credentials/
NAME = replace_camera_credential
PERMISSION = cameras.change_camera_credential
PAYLOAD = username, password
```

Ambos os campos são obrigatórios. Limites observados no serviço/schema: username até 255 caracteres e password até 1024. Campos adicionais, IDs de versão, versão ativa, chave ou ciphertext não são aceitos do browser. View e service devem validar autorização no servidor; CSRF é obrigatório. Chamar `replace_camera_credential(actor, camera_id, username, password, request)`.

O service já realiza persistência de versões e vínculo em `transaction.atomic`, cifragem e validação round-trip, troca do ponteiro e auditoria de sucesso. Uma submissão duplicada pode criar versão adicional; idempotência não é garantida. Não prometer deduplicação. Após sucesso, padrão POST/Redirect/GET para `editar` com mensagem genérica, sem refletir valores submetidos. Erro de validação deve renderizar erro SSR sanitizado (400 proposto); falha operacional de custódia/chave deve mostrar mensagem genérica de indisponibilidade (503 ou estado seguro na página, decisão de transporte a revisar). Exceções inesperadas geram resposta genérica 500, sem detalhes internos.

Falha ao persistir auditoria deve propagar e reverter toda mutação. O teste de falha injetada é gate obrigatório desta slice; observar `transaction.atomic` no código não é evidência suficiente.

### 3.3 Revogar — endpoint novo desta slice

```text
METHOD = POST
PATH = /<camera_id>/credentials/revoke/
NAME = revoke_camera_credential
PERMISSION = cameras.change_camera_credential
PAYLOAD = none
```

Exigir CSRF e autorização de servidor em view e service. A UX pede confirmação explícita antes do POST. Chamar `revoke_camera_credential(actor, camera_id, request)`. O service revoga a versão ativa e limpa o ponteiro, sem fallback. Sem credencial ativa, mapear `CREDENTIAL_NOT_CONFIGURED` a conflito 409 genérico. Após sucesso, PRG para editar e feedback genérico. A confirmação e o POST permanecem protegidos por CSRF.

Não criar endpoint GET de confirmação. O fallback sem JavaScript usa confirmação HTML obrigatória no formulário irmão de revogação.

## 4. Permissões e respostas

| Situação | Tratamento proposto/observado |
|---|---|
| GET editar sem `change_camera` | 403, comportamento atual da view decorada. |
| Camera inexistente em operação autorizada | 404; não revelar dados da credencial. |
| Painel de metadados sem `view_camera_credential` | Omitido no SSR; tentativa direta ao service é negada; endpoint futuro, se houver, retornaria 403. |
| POST replace/revoke sem `change_camera_credential` | 403 em view e service; UI não substitui autorização. |
| Reveal sem `reveal_camera_credential` | 403 atual. |
| Payload/validação inválida | 400 sanitizado. |
| Reveal sem credencial configurada | 404 atual com `CREDENTIAL_NOT_CONFIGURED`. |
| Reveal com reautenticação inválida | 403 atual com `REAUTHENTICATION_FAILED`. |
| Reveal outro `CredentialOperationError` | 400 atual; corpo JSON contém somente código seguro. |
| Serviço operacional conhecido indisponível | 503 sanitizado, sem divulgar existência, chave ou detalhes. |
| Exceção inesperada | 500 genérica sem conteúdo interno. |

Mapping aprovado: 400 payload/validação; 403 autorização ou reauth negada; 404 câmera inexistente para ator autorizado; 409 conflito de estado na revogação; 503 indisponibilidade operacional conhecida; 500 falha inesperada. Corpos/mensagens públicas são sanitizados. Não distinguir revogada de nunca configurada nem mostrar username.

## 5. CSRF, cache e auditoria

Todos os POST mutáveis e reveal usam CSRF. Replace e revoke não devem ser aceitos por GET. Não colocar segredo em query, URL, logs, body logging, session, cache, analytics, telemetria ou auditoria. A página SSR que contém metadados de credencial e todas as respostas das ações devem usar `Cache-Control: no-store` e diretivas equivalentes contra armazenamento; resposta de reveal preserva exatamente as diretivas `no-store` atuais. Auditoria pertence aos services; não duplicar na view. Eventos devem permanecer sanitizados segundo CAM-INT-02 e BC-AUTH.

## 6. Integração com `CameraEdicaoForm`

O gerente de credenciais é unidade irmã da edição cadastral. Não aninhar formulários HTML. O POST cadastral salva somente `CameraEdicaoForm`; POST replace/revoke não instancia nem salva esse formulário. Credencial persiste somente pelo service. Com JavaScript, detectar dirty state comparando valores originais e atuais; ações independentes exigem escolha explícita para manter e voltar ao cadastro ou descartar e continuar. Sem JavaScript, não alegar detecção dinâmica: formulários SSR irmãos permanecem utilizáveis e exigem checkbox obrigatório de confirmação de que alterações cadastrais foram salvas separadamente ou serão descartadas. O navegador deve bloquear o submit sem essa confirmação. O fallback de reveal não renderiza segredo nem trata JSON como HTML; reveal fica indisponível sem JavaScript, com explicação acessível. Não criar rota GET adicional. Não alterar campos/semântica de `Camera` por efeito lateral.

## 7. Reveal existente — preservação

Manter `POST /<camera_id>/credentials/reveal/` e o nome atual. O endpoint preserva POST, CSRF, permissão dedicada, reautenticação em cada operação, `no-store` e auditoria sanitizada. A resposta JSON não é interface SSR: frontend autorizado integra a resposta explicitamente, mantém resultado somente em memória transitória, limpa ao fechar/navegar/erro e não copia automaticamente. Sem JavaScript, reveal não é oferecido.

## 8. Limites de dados e segurança

- Browser controla somente `username` e `password` como payload de credencial para replace; revoke recebe apenas confirmação não secreta.
- Não aceitar `camera_id` de corpo como authority sobre a rota, nem IDs/version/key/ciphertext.
- Não serializar segredo no render inicial, hidden input, `data-*`, fixture, URL ou storage do browser.
- Username é dado sensível e não aparece na UI SSR ordinária, telemetria ou auditoria.
- `key_version`, ciphertext e senha não são necessários no SSR ordinário.
- Serviço verifica a permissão Django no contexto do `camera_id`; o contrato atual não define ownership/tenant por usuário. Esconder botões não autoriza operação.
- Mutação não altera configuração cadastral nem vínculo operacional além do lifecycle contratado.
- Erros públicos são allowlisted e sanitizados; logs não recebem payload de segredo.

## 9. Matriz de estados UI/HTTP

| Estado | Origem | Apresentação proposta |
|---|---|---|
| Sem permissão de metadata | Django permission | Painel oculto; servidor continua negando operação direta. |
| Sem credencial ativa / estado desconhecido | projeção SSR | Rótulo genérico; não afirmar “revogada”. |
| Ativa | `configured=True` após projeção mínima | Status de configuração ativa, sem username/key/version/timestamps. |
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

Replace/revoke delegam toda persistência a services transacionais existentes. A view não faz escrita ORM para credencial. A edição da Camera tem fluxo transacional próprio. Não combinar domínios em uma transação ou submit HTML. Auditoria participa da transação e qualquer falha ao gravá-la reverte a mutação; status de validação depende dos testes direcionados por falha injetada.

### 10.1 Submissões repetidas e concorrência

Não há chave de idempotência nem garantia de deduplicação no schema/contrato existente; não introduzir migration ou estado de domínio. POST replace repetido pode criar nova versão e novo evento em cada execução, com a última operação serializada tornando-se ativa. POST revoke repetido após sucesso retorna 409 e não restaura versão. Requisições concorrentes são serializadas pelo lock do service em bancos com suporte a `select_for_update`; em backend sem esse suporte, falha operacional/lock não pode produzir sucesso falso ou estado parcial e será mapeada seguramente. Falha de resposta após commit é ambígua para o cliente: consultar novamente a página e o estado mínimo antes de repetir. Desabilitação visual é apenas UX. Esta política aceita repetição como nova operação explícita, não promete idempotência.

## 11. Testes obrigatórios nesta implementação

Cobrir permissão em view/service; 403/404; GET metadata e projeção allowlist sem decrypt; formulário cadastral inalterado em POST de credencial; CSRF/métodos; replace/revoke via services; PRG; validação/errors sanitizados; falha injetada de auditoria com rollback efetivo; replace repetido e revoke repetido; reveal regression com POST/CSRF/reauth/no-store; HTML/cache/log sem segredo; dirty e fallback SSR; estrutura sem forms aninhados. Stress concorrente em PostgreSQL/múltiplos workers permanece fora da evidência local e não pode ser inferido dos testes SQLite.

## 12. Aprovação, gates e fora de escopo

Contrato ratificado para esta slice conforme CARD B e adendo aceitos. `CONTRACT_RATIFIED` não implica `SECURITY_FOUNDATION_VALIDATED`, `HTTP_IMPLEMENTATION_VALIDATED`, `DJANGO_VISUAL_CONFORMANCE` nem aceite visual humano; cada gate requer evidência independente.

`RESIDUAL_RISKS`: replace repetido gera versões/eventos adicionais; resposta perdida após commit não é distinguível pelo cliente; revogação concorrente com replace tem resultado serializado dependente da ordem. Não há idempotência server-side. Sem alteração autorizada no schema, esses efeitos são documentados e testados como operações repetidas, e a UI exige confirmação e reconsulta antes de repetir após falha ambígua.

Fora do escopo: nova SPA/JSON API; mudança CAM-INT-02, CAM-INT-02-R1 ou BC-AUTH; novos serviços, modelos ou migrations; reautenticação diferente no reveal; endpoint de metadata ou confirmação GET; teste real de conexão, alteração de câmera, exposição de username por padrão, teste de câmera real, homologação, E2 e deploy.

## 13. Referências

- `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md`
- `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`
- `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` (BC-AUTH)
- `cameras/integracao/credentials.py`; `cameras/credential_views.py`; `cameras/urls.py`; `cameras/views.py`; `cameras/authorization.py`
- `cameras/test_camera_credentials.py`; `cameras/test_authorization.py`
- `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`; `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md`; `COMPONENT_CATALOG.md`; `STATE_MATRIX.md`
- `docs/projeto/ARGOS_DELIVERY_EXECUTION_PLAN_V1.md`; Roadmap §25; Sprints §22

## 14. Registro da adjudicação e estado final E1

CARD B e o adendo técnico/visual foram aceitos pelo usuário; este contrato é ratificado apenas para `ARGOS-CRED-UI-01`, sem modificar autoridades superiores. Gate A (`CONTRACT_RATIFIED`) passou. Gate B permanece dividido: `SECURITY_FOUNDATION_VALIDATED` tem evidência independente de falhas injetadas de auditoria com rollback em `PROJECT_STATE.md` §132; `HTTP_IMPLEMENTATION_VALIDATED` tem os testes direcionados e regressões listados em §137. Gate C passou com aplicação Django real, inspeção de DOM, fluxo SSR sem JavaScript e capturas nos quatro viewports. Gate D (`DJANGO_HUMAN_VISUAL_APPROVAL`) passou após aceite explícito do usuário em 2026-10-17.

Riscos que permanecem abertos: não há idempotência server-side; replace repetido pode criar versão e evento adicionais; revoke repetido pode responder HTTP 409; PostgreSQL/concorrência não foram testados; reveal sem JavaScript não é suportado pela interface; auditoria formal com leitor de tela não foi realizada. A publicação Git não declara homologação operacional, deploy, acesso a câmera real ou validação de concorrência.

O contrato de prototipação com sufixo `DRAFT` preservado em `docs/prototype/ui-password-cam/references/` é somente o registro histórico anterior à ratificação. Este arquivo é o contrato vigente da slice. Estado de publicação e SHAs da integração constam em `PROJECT_STATE.md` §138 e no relatório final da atividade.

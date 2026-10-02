# CAM-INT-02 — Credenciais de equipamento

```text
STATUS = ACTIVE / SECURITY BASELINE
SECRET_STORE_IMPLEMENTATION = IMPLEMENTED / INTEGRATED / VALIDATED_LOCAL / PUBLISHED
BC02_STATUS = IMPLEMENTATION_READY
IMPLEMENTATION_READY = YES
IMPLEMENTER_TARGET = LUNA
RUNTIME_RESOLUTION_OWNER = CAM-INT-02
RUNTIME_RESOLUTION_CONTRACT = CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md
RUNTIME_RESOLUTION_STATUS = IMPLEMENTATION_READY / NOT_IMPLEMENTED
```

## Invariantes

Configuração técnica não secreta e material de autenticação têm armazenamento, permissões, lifecycle e auditoria separados. Senha, token e chave não aparecem em URL, linha de comando, HTML, logs, traces, erros, fixtures ou documentação. Username também é tratado como sensível e não é emitido em telemetria.

A direção aprovada em ADR-021 é entidade de credencial separada, segredo cifrado com proteção autenticada por biblioteca reconhecida, versão e referência de chave, enquanto a chave mestra é fornecida ao serviço por mecanismo seguro externo ao banco/backup. Não implementar criptografia própria nem gravar chave junto do ciphertext. A biblioteca local é escolhida no BC-02 abaixo; o provedor operacional de produção permanece em PROD-PERSIST.

## Ciclo de vida

Credencial conceitual identifica estado ativa/inativa, versão, escopo explícito, referência protegida, datas de criação/rotação e responsável pela alteração. Rotação: criar versão, validar controladamente, ativar vínculo de forma atômica, permitir ao worker autorizado resolver apenas a versão ativa e retirar a antiga conforme política. Não presumir fallback dual-secret. Versão revogada/comprometida nunca pode ser fallback.

Falha de configuração ou autenticação é diagnóstico do subsistema, não prova de `OFFLINE`; preserva estado estável anterior e não deve criar onda de transições. Uso normal durante probe não gera evento funcional por tentativa; alteração, rotação, revogação e concessão devem gerar trilha auditável sanitizada.

## Isolamento e recuperação

Credenciais, chaves, allowlists e identidade são segregadas entre dev/teste/prod. Copiar banco não transporta autoridade de uso de segredo. Backup de ciphertext sem a chave correspondente é insuficiente; restore exige recuperação autorizada e validada da chave, sem imprimir segredo. Worker recebe apenas credencial necessária pelo menor período/escopo e não a aceita do browser nem CLI.

Estado factual em `c0e5a954d8a2e290acb5ce86a1b699a10c02b190`: entidades,
Fernet, provider local e lifecycle/reveal foram implementados e publicados
pela CAM-INT-02. Secret manager operacional, restore e homologação reais
continuam pendentes. A API pública interna de execução ainda não existe e
pertence à sub-slice CAM-INT-02-R1 abaixo. Não habilitar adapter autenticado
antes de sua publicação e dos gates próprios de ambiente. Referência normativa:
ADR-021 §§3.1–3.4, 5–6, 8–9.

## BC-02 — custódia e lifecycle implementáveis

`CameraCredential` é 1:1 com `Camera` e guarda `active_version` nullable,
`created_at`, `updated_at`, `updated_by` e estado. `CameraCredentialVersion`
tem FK protegida para credential, `version` inteiro positivo, `ciphertext`
autenticado, `key_version` curto e não secreto, estado
`PENDING/ACTIVE/RETIRED/REVOKED`, `created_at/by`, `activated_at`,
`retired_at`, `revoked_at` e `rotated_from` opcional. `ciphertext` é payload
versionado que contém **username e password**; não há coluna plaintext de
username. A leitura humana devolve username apenas a Técnico/Admin autorizado;
a execução interna autorizada recebe username/password somente em memória
pela boundary CAM-INT-02-R1, sem constituir reveal humano.
Payload interno é JSON UTF-8 com versão de schema e chaves fechadas
`username`/`password`, limites de comprimento e sem campos adicionais;
serialização/deserialização ocorre antes/depois de Fernet, nunca no log.
`(credential_id, version)` é único e há unique condicional para no máximo uma
versão `ACTIVE` por credential; `active_version` só pode apontar para versão
da mesma credencial em estado ACTIVE, verificado sob lock transacional.
Versão revogada nunca é candidata a fallback.
CAM-INT-02 adiciona FK nullable de `CameraConnectionConfig` para
`CameraCredential`; service valida que ambas pertencem à mesma Camera antes
de ativar vínculo ou resolver segredo.

Biblioteca escolhida para implementação: `cryptography==46.0.7`, receita
`Fernet` para criptografia autenticada reversível. Este pin tem suporte a
CPython 3.14; a implementação adiciona-o a `requirements.txt` **na slice**,
não neste checkpoint documental. `CredentialKeyProvider` fornece mapa
`key_version -> Fernet key` e identificador ativo. Chaves vêm de secret
delivery externo ao banco/backup; para teste local, provider injetado em
memória. Não persistir chave em settings versionado, fixture, command line,
log ou migration. Provedor operacional concreto de produção pertence a
PROD-PERSIST, mas a interface local e sua falha estão fechadas. `encrypt`
sempre usa chave ativa; `decrypt` usa **somente** `key_version` da linha e
falha fechada em chave ausente, inválida ou token adulterado. A rotação da
chave re-encripta linha por linha com key_version novo sob lock; chave antiga
fica disponível até verificação de todas as linhas/backup e nunca é removida
por mera troca de config. `MultiFernet` não escolhe chave por tentativa cega.

Update de segredo cria versão PENDING, valida localmente formato e round-trip;
validação real opcional somente em ambiente autorizado. Ativação troca
`active_version` atomicamente, marca anterior RETIRED se segura e audita.
Falha antes da ativação deixa a anterior intacta; depois da ativação, rollback
planejado exige nova transação auditada e só é permitido se a anterior ainda
for segura/não revogada. Revogação de emergência zera vínculo ativo antes de
qualquer nova tentativa, sem fallback. Erro de chave/credencial bloqueia o
probe com diagnóstico sanitizado e deixa health envelhecer; não cria OFFLINE.

Reveal: somente Técnico/Admin com `reveal_camera_credential`, POST+CSRF,
reautenticação recente, `no-store`, sem body logging; service checa ator e
câmera antes de decrypt. Resultado não é persistido em sessão/cache.
Alteração, ativação, reveal, revogação e falha são auditadas com IDs/versões
e resultado, jamais username, password ou ciphertext. Worker resolve apenas
a versão ativa autorizada, pelo menor período, sem recebê-la da UI/CLI.

```text
MODEL_CHANGE = CameraCredential + CameraCredentialVersion + Config.credential FK
MIGRATION_REQUIRED = YES
EXPECTED_MODELS = CameraCredential; CameraCredentialVersion
RELATIONSHIPS = Camera 1:1 Credential; Credential 1:N Version; active_version FK;
                Config N:1 Credential with same-camera service invariant
CONSTRAINTS = unique(credential,version); partial unique ACTIVE/credential;
              version > 0; active FK same owner/service lock
INDEXES = credential(active_version); version(credential,status,version)
DATA_MIGRATION = NO; no legacy equipment secret exists
ROLLBACK_CONSIDERATION = never export plaintext; preserve ciphertext and key material separately
EXPECTED_PRIMARY_FILES = cameras/models.py; requirements.txt (future implementation)
EXPECTED_NEW_FILES = cameras/integracao/credentials.py; cameras/integracao/key_provider.py
EXPECTED_TEST_FILES = cameras/test_camera_credentials.py; permission/reveal tests
SHARED_FILES = cameras/models.py; migrations; configuration resolver
STOP_AND_ESCALATE_TO_SOL_IF = required secret type exceeds payload/schema;
                              external custody contradicts key provider contract;
                              rollback would use revoked version
```

Acceptance criteria:

1. Dada chave válida, criar e revelar versão ativa recupera username/password;
   DB, logs, auditoria e URI não contêm plaintext. Token alterado ou chave
   ausente/inválida falha fechado com erro seguro, sem network call.
2. Dado update com erro antes de ativar, versão anterior segura permanece
   ativa; dada ativação válida, há exatamente uma versão ativa referenciada.
3. Dada revogação de emergência, nenhuma chamada usa versão revogada nem
   marca câmera OFFLINE por isso; usuário sem permissão não obtém metadados
   sensíveis nem reveal.

Referência técnica da escolha: [Fernet em cryptography 46.0.7](https://cryptography.io/en/46.0.7/fernet/)
e [artefatos CPython 3.14 no PyPI](https://pypi.org/project/cryptography/46.0.7/).

## CAM-INT-02-R1 — resolução operacional pública interna

O contrato completo está em
[CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md](CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md).
CAM-INT-02 possui crypto, provider e resolução; CAM-INT-03/04 são consumers.
API contratada: `resolve_active_credential_for_execution(*, config)` no módulo
`cameras.integracao.credentials`, com `CameraConnectionConfig` persistido
autorizado pelo caso de uso e retorno `ResolvedCameraCredential` efêmero.
Somente a ACTIVE apontada pela credencial configurada da mesma câmera é
resolvida; PENDING/RETIRED/REVOKED e qualquer inconsistência falham sem fallback.

EXECUTION_RESOLUTION é interna, pública ao código de aplicação, não HTTP e
não serializável; não exige `reveal_camera_credential`, reautenticação ou
usuário Django fictício. Diagnóstico/captura manuais mantêm permissões próprias
no caso de uso externo. Não gera evento de reveal por execução. O contrato R1
fecha API, falhas, integridade, lifetime, ownership, testes e aceite sem alterar
o schema ou as permissões. Implementação futura não autoriza consumers a usar
helper privado, ciphertext, provider, endpoint reveal ou URI autenticada.

`CAM-INT-02-R1 = IMPLEMENTATION_READY / NOT_IMPLEMENTED`; predecessora
CAM-INT-02 publicada, successors CAM-INT-03 e CAM-INT-04 bloqueados até R1
implementada, integrada, validada e publicada. A prontidão anterior da
CAM-INT-02 não comprova presença dessa boundary; esta adjudicação corrige o
gap explícito, preservando o lifecycle já publicado.

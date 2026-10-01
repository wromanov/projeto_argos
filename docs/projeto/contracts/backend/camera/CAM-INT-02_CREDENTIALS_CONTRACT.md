# CAM-INT-02 — Credenciais de equipamento

```text
STATUS = ACTIVE / SECURITY BASELINE
SECRET_STORE_IMPLEMENTATION = NOT_PRESENT
```

## Invariantes

Configuração técnica não secreta e material de autenticação têm armazenamento, permissões, lifecycle e auditoria separados. Senha, token e chave não aparecem em URL, linha de comando, HTML, logs, traces, erros, fixtures ou documentação. Username também é tratado como sensível e não é emitido em telemetria.

A direção inicial aprovada em ADR-021 é entidade de credencial separada, segredo cifrado com proteção autenticada por biblioteca reconhecida, versão e referência de chave, enquanto a chave mestra é fornecida ao serviço por mecanismo seguro externo ao banco/backup. Não implementar criptografia própria nem gravar chave junto do ciphertext. O provedor operacional da chave e biblioteca concreta seguem não escolhidos.

## Ciclo de vida

Credencial conceitual identifica estado ativa/inativa, versão, escopo explícito, referência protegida, datas de criação/rotação e responsável pela alteração. Rotação: criar versão, validar controladamente, ativar vínculo de forma atômica, permitir ao worker autorizado resolver apenas a versão ativa e retirar a antiga conforme política. Não presumir fallback dual-secret. Versão revogada/comprometida nunca pode ser fallback.

Falha de configuração ou autenticação é diagnóstico do subsistema, não prova de `OFFLINE`; preserva estado estável anterior e não deve criar onda de transições. Uso normal durante probe não gera evento funcional por tentativa; alteração, rotação, revogação e concessão devem gerar trilha auditável sanitizada.

## Isolamento e recuperação

Credenciais, chaves, allowlists e identidade são segregadas entre dev/teste/prod. Copiar banco não transporta autoridade de uso de segredo. Backup de ciphertext sem a chave correspondente é insuficiente; restore exige recuperação autorizada e validada da chave, sem imprimir segredo. Worker recebe apenas credencial necessária pelo menor período/escopo e não a aceita do browser nem CLI.

Estado atual: não existe entidade de credenciais de equipamento nem secret manager implementado. Não conectar a câmera real ou habilitar adapter autenticado antes de fechar custódia, rotação, permissões, auditoria e restore. Referência normativa: ADR-021 §§3.1–3.4, 5–6, 8–9.

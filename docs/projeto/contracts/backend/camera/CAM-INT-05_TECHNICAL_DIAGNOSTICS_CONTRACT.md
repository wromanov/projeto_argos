# CAM-INT-05 — Diagnósticos técnicos de integração

```text
STATUS = ACTIVE / CONTRACT BASELINE
PROBE_ADAPTERS = FAKE/LAB BOUNDARY ONLY; NO REAL CAMERA HOMOLOGATION
```

## Observação e resultado

Tentativa de probe é evidência transitória; não é estado de disponibilidade nem incidente. O contrato local `ProbeResult` exige código fechado, instante aware convertido a UTC, duração finita e não negativa e `error_code` curto sem URL. `SUCCESS` não pode levar erro. Categorias atuais: `SUCCESS`, `TIMEOUT`, `CONNECTION_REFUSED`, `AUTH_FAILURE`, `TLS_ERROR`, `PROTOCOL_ERROR`, `CONFIG_ERROR`, `TARGET_BLOCKED`, `CANCELLED`, `INCONCLUSIVE`.

Na redução atual, somente sucesso e falha de transporte classificadas conforme política aprovada contam como evidência direcional; auth/TLS/protocolo/configuração/bloqueio/inconclusivo funcionam como barreira neutra, e cancelamento não é falha do dispositivo. Resultado atrasado não pode reverter observação mais recente; timestamp igual é ambíguo. Uma tentativa isolada não promove estado: confirmação produz `UNKNOWN/ONLINE/OFFLINE` e sequência interna não vira status público.

## Sanitização e armazenamento

Erro diagnóstico comunica categoria/código seguro e, quando necessário, correlação opaca. Nunca conter senha, username, URL completa, query string, path com token, header, resposta de autenticação, payload de imagem ou detalhe de rede sensível. Probe repetido normal não cria evento de auditoria de usuário nem indisponibilidade adicional. Métricas agregadas podem incluir latência e contagens sem identificação secreta.

## Limite de evidência

O código tem adapter protocol e fakes; não prova conector RTSP/HTTP real, câmera suportada ou significado operacional universal de `SUCCESS`. O diagnóstico deve declarar camada testada (IP/porta, HTTP, autenticação, sessão RTSP, imagem decodificada) e o que não foi testado. Fonte: ADR-020 §§3–5; ADR-021 §§4, 8; `cameras/monitoramento/contracts.py`, `confirmation.py`.

# CAM-INT-03 — Conexão RTSP

```text
STATUS = ACTIVE / ADAPTER CONTRACT; NOT HOMOLOGATED
RTSP_ADAPTER_IMPLEMENTED = NO
```

## Semântica

RTSP não é um health check universal. Sucesso de conexão, autenticação, negociação de sessão, leitura de stream e decodificação de vídeo são evidências diferentes; um adapter só pode afirmar a capacidade efetivamente verificada. Um probe RTSP não se torna automaticamente captura de snapshot, prova de gravação VMS ou saúde completa da câmera.

## Fronteira futura do adapter

O adapter receberá request tipado criado a partir de câmera elegível e perfil validado, nunca URL arbitrária do browser. O endpoint RTSP deve ser relativo/controlado pelo perfil; userinfo é proibido; credencial é resolvida por referência autorizada e injetada sem compor/logar URL textual. IP IPv4, porta e path são validados contra profile e allowlist antes da conexão. Timeout é bounded e cancelamento não altera estado técnico. Redirect, DNS, proxy ambiental e transporte não homologado ficam desabilitados por padrão.

O adapter retorna apenas categoria fechada, timestamp UTC aware, duração monotônica não negativa e código de erro sanitizado, seguindo `ProbeRequest`/`ProbeResult`. Conteúdo de stream, headers e credenciais não são persistidos pelo contrato de monitoramento.

## Homologação requerida

Validar modelos/firmwares reais, transporte e modo de autenticação, timeout de connect/read, encerramento de sessão, limite de bytes/frames, vazamento em erros/logs, impacto no equipamento e o que o sinal comprova. Falha de auth/configuração deve ser neutra para transição de disponibilidade. Não existe escolha de RTSP como mecanismo universal nem acesso de rede homologado neste baseline.

Referências: ADR-019 itens em aberto; ADR-021 §§3.5–3.8, 4, 7–9; `cameras/monitoramento/contracts.py`.

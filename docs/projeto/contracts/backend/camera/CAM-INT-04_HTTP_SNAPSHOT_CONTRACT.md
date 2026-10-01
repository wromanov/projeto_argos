# CAM-INT-04 — Captura HTTP de snapshot

```text
STATUS = ACTIVE / ADAPTER CONTRACT; NOT HOMOLOGATED
HTTP_CAMERA_ADAPTER_IMPLEMENTED = NO
```

## Separação de operações

Uma requisição HTTP usada como probe de saúde não é automaticamente uma captura e uma captura sob demanda não é uma transição de disponibilidade. A captura autorizada busca uma imagem por adapter/capability homologada e encaminha os bytes ao pipeline canônico `CameraImageRecord`; não salva evidência automaticamente em evento de monitoramento.

## Requisitos de conexão

O futuro adapter constrói internamente esquema HTTP/HTTPS permitido, IPv4 de `Camera`, porta autorizada e path controlado pelo perfil. Userinfo e credenciais em URL são proibidos. Redirects ficam desabilitados; se adjudicados, cada hop exige validação completa de esquema, destino, porta e allowlist. DNS e proxy ambiental permanecem desabilitados no baseline. Timeout, tamanho máximo de resposta, content-type, status e cancelamento devem ser bounded. Não seguir link para VMS ou host não permitido.

Resposta HTTP só é captura válida se o conteúdo for validado por assinatura/formato e decode seguro e então passar pelo fluxo de persistência de imagem; MIME declarado pelo equipamento não basta. Nenhum token/header sensível é incluído em logs. Erros são normalizados e sanitizados.

## Limites

ADR-019 proíbe captura automática associada a probe, primeira detecção ou retorno `OFFLINE -> ONLINE`; captura é sob demanda de operador autorizado. Método padrão, endpoints, formatos, limites definitivos e credenciais autorizadas variam por capability e continuam pendentes. `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` define proveniência, integridade, seleção e armazenamento; este documento não os duplica.

Referências: ADR-019; ADR-021 §§3.5–3.8, 7–9; IMG-CAP; CAM-INT-01/02/07.

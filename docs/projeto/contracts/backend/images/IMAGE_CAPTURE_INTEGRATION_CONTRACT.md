# Integração de captura de imagem

```text
ID = IMG-CAP
STATUS = ACTIVE / COMPLEMENT TO CANONICAL IMAGE DOMAIN
DOMAIN_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
```

## Fronteira

Captura de câmera é ação explícita, autorizada e desacoplada do monitoramento. Não captura automaticamente na primeira detecção, em probe, em transição ou em retorno `OFFLINE -> ONLINE`. Captura direta e upload manual são proveniências distintas (`CAPTURA_CAMERA`, `UPLOAD_MANUAL`) no mesmo `CameraImageRecord`; não criar tabela, histórico ou regra de latest paralelos.

Futuro fluxo de captura: autenticar/autorizar operador ou identidade de serviço de captura; resolver camera e capability homologada; validar destino com CAM-INT-07; resolver somente credencial autorizada CAM-INT-02; obter resposta bounded; validar formato/bytes e integridade no servidor; armazenar via abstração privada; criar registro com `captured_at` observado e `recorded_at` do servidor, origem, executor e checksum; auditar ação sem segredo. Falha não cria registro AVAILABLE, não muda saúde nem mascara estado de captura corrente.

## Leitura e entrega

O domínio canônico determina ordenação de `LATEST_CAMERA_CAPTURE`, ausência de fallback para captura antiga quando a latest falha, `DISPLAY_IMAGE` com upload manual somente quando nenhuma captura existe, preview privado, hash/integridade, variants fechadas, autorização `cameras.view_camera`, `nosniff` e `no-store`. IMG-CAP não redefine esses contratos; remete às seções 7, 18, 19, 24 e 25 do documento canônico.

Upload manual atual é implementado com `cameras.add_cameraimagerecord`, valida JPEG/PNG/WEBP estático, tamanho/dimensões bounded, decode/re-encode, storage configurado e auditoria. Limites correntes são operacionais, não política definitiva de produção. Adapter de captura a câmera, worker/caminho autenticado e armazenamento de produção não estão implementados/homologados.

## Decisões abertas

Credencial/perfil permitido para captura, método por fabricante/modelo, políticas finais de MIME/tamanho/dimensões, storage de produção, retenção/expurgo, rotação e privilégio de captura permanecem pendentes conforme contrato de imagem e ADR-019/021. Este documento não autoriza captura em câmera real.

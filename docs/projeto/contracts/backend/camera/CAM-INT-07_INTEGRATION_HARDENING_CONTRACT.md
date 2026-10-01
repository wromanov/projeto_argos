# CAM-INT-07 — Hardening da integração de rede

```text
STATUS = ACTIVE / SECURITY BASELINE
REAL_NETWORK_HOMOLOGATION = NOT_PERFORMED
```

## Autorização do destino

O worker deriva destino apenas de câmera elegível e configuração/perfil autorizado. Baseline é IPv4 cadastrado; hostname/DNS e alvo fornecido por request/browser são proibidos. IP sintaticamente válido ou privado não implica autorização: validar allowlist de CFTV do ambiente, protocolo, porta e segmento/farm. Rejeitar loopback, localhost, unspecified, link-local, multicast, broadcast, metadata endpoint e destinos administrativos fora da allowlist. Infraestrutura também limita egress; validação da aplicação não substitui firewall.

Porta deve estar entre 1 e 65535, autorizada simultaneamente pelo perfil e política de ambiente. HTTP redirects, proxy ambiental e DNS são desabilitados no baseline. Qualquer futura exceção exige adjudicação e validação de cada destino/hop e medidas contra DNS rebinding.

## Defesa e isolamento

Worker dedicado, não root, identidade de serviço própria, sem sessão humana, privilégio mínimo de banco e sem poderes implícitos de admin/captura. Segredos, chaves, banco, allowlists e credenciais são separados por ambiente. Aplicar timeouts e limites de resposta/stream, cancelamento previsível e encerramento de conexões. Captura não herda permissão/credencial de monitoramento sem contrato específico.

## Logging e resposta

Registrar identificador técnico opaco, adapter/profile version, categoria, duração e resultado operacional sanitizado. Nunca registrar IP completo quando a política o considerar sensível, credencial, URL, userinfo, query, payload, headers de auth ou chave. Acesso bloqueado por policy é `TARGET_BLOCKED`/diagnóstico operacional, não `OFFLINE` confirmado.

## Gate para homologação

Definir CIDRs e portas reais fora deste documento; aprovar autoridade de acesso; testar DNS/redirect/proxy, egress real, segmentação VLAN/firewall, identidade e privilégios, falhas de auth, limites, logs, rotação/restore e resposta a incidente. Nenhum CIDR, segredo ou endpoint real é registrado neste contrato. Fonte: ADR-021 §§3.7–3.8, 5–9, 12.

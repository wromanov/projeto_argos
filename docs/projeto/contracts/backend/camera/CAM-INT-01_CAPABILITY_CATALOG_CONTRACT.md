# CAM-INT-01 — Catálogo de capabilities de câmera

```text
STATUS = ACTIVE / CONTRACT BASELINE
MODEL_IMPLEMENTATION = NOT_PRESENT
```

## Contrato

Uma capability é uma afirmação versionada e evidenciada sobre o que um modelo/firmware pode fazer por determinado protocolo e perfil. Ela limita a seleção de adapter; não é, por si só, autorização para alcançar o dispositivo nem prova de que o recurso funciona na unidade instalada.

O perfil conceitual de `ADR-021` deve declarar: protocolo/adapter; porta permitida; política TLS; endpoint/path controlado; método de autenticação; requisito de credencial; probe primário/secundário e o que o resultado comprova; parâmetros estritamente necessários; compatibilidade de fabricante/modelo/firmware; versão e estado ativo. Configuração comum fornece defaults e limites; override por câmera só é permitido para campos declarados sobrescrevíveis.

## Registro e evidência

Cada capability futura deve identificar fonte (datasheet, laboratório ou validação de unidade), firmware/escopo aplicável, validade, limitações, ambiente e versão. Compatibilidade ausente ou ambígua significa `UNVERIFIED`, nunca suporte presumido. Nenhum inventário automático de fabricante/modelo ou endpoint universal é inferido dos campos cadastrais.

O catálogo não armazena segredo, URL arbitrária, senha, token ou stream path com material de autenticação. Segredos são referenciados por identificador opaco segundo CAM-INT-02. Destination policy e allowlist permanecem responsabilidade do hardening.

## Estado observado e adiamentos

`Camera` tem texto livre para fabricante/modelo e campos como `tipo`, `codec`, `farm` e IP; não há model de catálogo, perfil ou configuração efetiva de monitoramento. Tipos cadastrais não equivalem a capabilities. O baseline é IP IPv4 cadastrado, DNS desabilitado, perfil compartilhado com override restrito como recomendação de ADR-021. Normalização completa do catálogo e dados compatíveis aguardam evidência de laboratório e decisão própria.

Referências: ADR-021 §§3.5–3.6; `cameras/models.py`; `CAM-INT-03`, `CAM-INT-04`, `CAM-INT-06`.

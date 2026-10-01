# CAM-INT-06 — Capabilities por fabricante, modelo e firmware

```text
STATUS = ACTIVE / COMPATIBILITY CONTRACT
CATALOG_DATA = NOT PRESENT
```

## Chave de compatibilidade

Compatibilidade pode depender de fabricante, modelo exato, revisão/firmware, região, licença e configuração real da unidade. `fabricante`, `modelo`, `tipo`, `codec` e `farm` de `Camera` são dados cadastrais; não são prova de adapter, endpoint, protocolo ou autenticação suportados. Ausência de correspondência significa não verificado e bloqueia integração que dependa da capability.

Registro futuro de compatibilidade referencia a versão do perfil CAM-INT-01, versão/escopo observado, fontes de evidência e data/revisor. `SUPPORTED`, `UNSUPPORTED` e `UNVERIFIED` devem ser distinguíveis. Um resultado de laboratório limitado a modelo/firmware/ambiente não pode ser generalizado silenciosamente para toda a marca.

## Variação por unidade

Mesmo modelo pode ter endpoint, porta, firmware, VLAN ou credenciais distintos. Perfil compartilhado fornece defaults e limites; configuração por câmera só sobrescreve campos explicitamente autorizados. Endpoint secreto ou credencial não fica no catálogo público. Capacidade de stream não implica snapshot; snapshot não implica health; ONVIF não implica stream operacional.

## Estado e decisão pendente

Não há catálogo estruturado ou capability matrix implementado. Normalização de vendor/model/firmware, curadoria da fonte, cadência de validação e escopo de suporte aguardam levantamento dos ativos e laboratório controlado. Não popular capacidades presumidas para produzir aparência de cobertura.

Referências: ADR-021 §§3.5–3.6 e §12; CAM-INT-01/03/04.

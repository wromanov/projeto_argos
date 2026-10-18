# Design QA — Proposta C V2.1 (protótipo)

**Fonte:** `prototype/ARGOS_E3_CAPTURE_ELIGIBILITY_STATES_PROPOSAL_V2_1.html` (mesmos bytes fornecidos e aprovados pelo usuário).  
**Método:** Chromium headless; HTML carregado em memória; cenário selecionado por controle nativo; verificação de DOM/computed styles e screenshots de recortes.  
**Estado:** QA automatizado do protótipo concluído. **Não é aceitação no Django, nem auditoria de acessibilidade completa.**

| Métrica | Resultado |
|---|---|
| Viewports | 2048×742, 1440×900, 1366×768, 390×844 |
| Cenários | 01, 02, 03, 04a, 04b, 05, 06, 07a, 07b, 08 |
| Combinações executadas | **40/40** |
| Erros JavaScript (`pageerror`) | **0** |
| Achados do teste automatizado | **0** |
| Overflow horizontal global observado | **0** |
| Visibilidade de upload/captura/CTA | Conforme cenários esperados em 40 combinações |
| Mensagens de estado 02,03,04a,04b,07a,07b | Visíveis nos cenários exigidos |
| Operação única 05/08 | Sem coluna residual pelos critérios do teste |
| Referência B embutida | `naturalWidth > 0`, renderizada nos quatro viewports |
| Ciclo demonstrativo de retry 07b→07a | Exercitado; CTA desaparece no estado running |
| Upload/captura reais | **NÃO EXECUTADOS** |
| Permissões/back-end Django | **NÃO VALIDADOS** |
| Leitor de tela, contraste pixel a pixel, todos os fluxos teclado | **NÃO VALIDADOS INTEGRALMENTE** |

## Evidências

- `evidence/PROTOTYPE_C_V2_1_1440_01.png` — ambas disponíveis.
- `evidence/PROTOTYPE_C_V2_1_1440_02.png` — indisponibilidade contextual, sem CTA.
- `evidence/PROTOTYPE_C_V2_1_1440_06.png` — sem operação disponível.
- `evidence/PROTOTYPE_C_V2_1_1440_07b.png` — falha e nova intenção demonstrativa autorizada.
- `evidence/PROTOTYPE_C_V2_1_1440_08.png` — captura omitida por permissão.
- Equivalentes `390` — comportamento mobile.
- `evidence/REFERENCE_B_EMBEDDED_1440.png` e `_390.png` — referência B carregada, não Django.

## Limites

As evidências são capturas do **HTML independente**, com dados fictícios. Não fazem requisições reais, não validam câmera, serviço, credential resolver, CSRF, autorização ou integridade de imagens. O card branco e a distribuição devem ser comparados novamente no **Django atual** após execução autorizada.

O HTML V2.1 difere da V2 somente na referência B embutida e na identificação correta daquela imagem como protótipo; a matriz de estados permanece sem alteração. O teste foi **reexecutado diretamente na V2.1**, não inferido da V2.

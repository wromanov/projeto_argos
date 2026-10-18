# Design QA — E3 Operações complementares / V1 B

## Escopo comprovado nesta entrega

Este QA refere-se ao **HTML independente de demonstração**, sem backend, câmera, credenciais ou persistência. Testes reexecutados na preparação do handoff usando Chromium/Playwright contra conteúdo do HTML em memória.

| Viewport | JavaScript | Overflow horizontal global | Estado padrão | Interações demonstrativas |
|---|---|---|---|---|
| 2048 × 742 | Sem erro observado | Não | Variante B | A/B, menu A, galeria mock, cenários, queued → running → success |
| 1440 × 900 | Sem erro observado | Não | Variante B | Idem |
| 1366 × 768 | Sem erro observado | Não | Variante B | Idem |
| 390 × 844 | Sem erro observado | Não | Variante B | Idem |

**Veredito técnico do mock:** `PASS_WITH_LIMITATIONS`. O navegador automatizado verificou os caminhos testados, não conformidade WCAG completa, operação de backend, autorização, idempotência ou captura real.

## Checklist de evidência / integração futura

- [x] HTML de referência congelado e Alternativa B preselecionada.
- [x] Upload à esquerda, captura à direita na desktop do HTML.
- [x] Exemplo E4 identificado como conceito no mock.
- [x] Interações do mock funcionam nas quatro larguras ensaiadas.
- [x] Sem overflow horizontal global nos cenários ensaiados.
- [ ] Implementação Django E3 executada por agente técnico autorizado.
- [ ] Botões e estados refletindo resultados de job reais.
- [ ] Permissão, CSRF, integridade, auditoria e segurança validadas no servidor.
- [ ] Upload antigo sem regressão.
- [ ] HTML real navegado somente pelo teclado; revisão de foco e leitores de tela.
- [ ] Validar textos longos, 320px e estados de erro no Django real, se aplicável.
- [ ] Capturas comparativas reais desktop/mobile.
- [ ] Aceite humano de fidelidade no Django integrado.

## Proteções visuais

Sidebar/topbar, Camera Detail e histórico, Quick Detail e demais superfícies não foram alterados nesta prototipação. São representados em contexto demonstrativo no HTML. A implementação futura não deve copiar o shell sintético do protótipo.

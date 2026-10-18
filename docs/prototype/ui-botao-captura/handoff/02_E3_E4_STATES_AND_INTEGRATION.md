# Matriz E3 de estados e fronteira E4 — visual V1 B

## 1. Operações separadas

**Upload (`UPLOAD_MANUAL`)** é o formulário existente; manter fluxo e significado. **Captura (`CAPTURA_CAMERA`)** é uma operação explícita e potencialmente assíncrona, ligada a um job autorizado. A ação **não** é captura automática, não testa disponibilidade técnica e não altera estado de monitoramento.

| Estado E3 | Comunicação visual | Condição funcional para produção |
|---|---|---|
| `IDLE` | Botão `Capturar imagem` e ajuda curta | Só exibir/habilitar segundo permissão e elegibilidade reais |
| `QUEUED` | Solicitação registrada; aguardando processamento | Request/job confirmado no servidor; **não** equivale a imagem capturada |
| `RUNNING` | Captura em processamento | Estado real do job, não timer do mock |
| `SUCCEEDED` | Captura concluída | Somente quando job real confirmar sucesso e registro validado |
| `FAILED` | Não foi possível capturar a imagem | Erro público sanitizado; não alterar monitoramento |
| `CANCELLED` | Resultado de cancelamento | Se contrato técnico oferecer estado; não criar comando cancelar sem suporte |
| `UNAVAILABLE/INELIGIBLE` | Captura indisponível com razão segura | Não inferir de ONLINE/OFFLINE apenas |
| `PERMISSION_DENIED` | Ação não exibida/permitida, conforme política | Endpoint verifica autorização; UI não é fronteira de segurança |

Interação E3 deve ter `POST` explícito com CSRF e proteção de duplicações/idempotência segundo contrato técnico; não presumir nomes de endpoints novos. Sucesso só após resposta/autorização reais, nunca por temporizador. Evitar polling intensivo, retry implícito e fallback de fontes sem contrato. Proteger de vazamento de URIs, credenciais, bytes e detalhes de equipamentos. Preservar a separação lógica de captura e monitoramento.

## 2. Prévia E4 estritamente conceitual

O laboratório apresenta `Ver imagens` e um `<dialog>` com três placeholders para discussão. Isso **não implementa** uma galeria. O domínio canônico limita a visualização aprovada a **até três imagens ativas por câmera** e ordenação `recorded_at ASC, immutable_id ASC` na Camera Detail. A E4 deverá estabelecer rota/leitura privada, permissões, estados, integridade, lifecycle e interações próprias antes de habilitar a ação em produção. Não presumir que IMG-06 já está executada.

**Na entrega E3:** não deixar link de galeria habilitado e sem destino; **não inserir controle falso** em produção. Preservar a composição de modo que o futuro botão caiba na posição aprovada sem redesign, quando E4 for autorizada.

## 3. Mocks que não podem ser promovidos a comportamento real

- Seletores de variante e cenário; etiquetas E3/E4 demonstrativas; resultados temporizados; galeria com três imagens inventadas; simulação de upload sem bytes e de usuário sem permissão. O protótipo não prova capturas, endpoints, autorização ou persistência.
- “Capturar imagem” só cria um pedido quando integrado a um caso de uso autorizado. `QUEUED`/`RUNNING` nunca podem ser tratados como evidência de captura efetiva.

## 4. Acessibilidade e responsividade

- Labels associados ao `<input type=file>` e nomes acessíveis de ações; foco visível e contraste; retorno de foco se houver diálogo futuro; estados de sucesso/erro comunicados em texto e região viva apropriada, sem depender só de cor.
- Controles não devem ficar espremidos nem desaparecer com textos longos; respeitar `prefers-reduced-motion`; estados e menus não devem depender de hover.
- Para E3 o JS serve apenas de enriquecimento progressivo: quando estiver ausente, a captura deve ter um caminho nativo/SSR utilizável **se o contrato de operação permitir**. Se essa opção exigir rota ou semântica não prevista, parar e encaminhar a lacuna ao agente principal.

## 5. Dependências técnicas para o agente resolver

Consultar `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` (§26), `IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` e autoridades de permissão atuais. Na captura, o job tem status `QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELLED` no contrato complementar; a experiência só pode refletir os estados que a implementação real expuser, sem inventar estados adicionais. Confirmar disponibilidade de worker, perfil/capability, policy de destino, credenciais autorizadas, adaptadores e requisitos de armazenamento/ambiente. Não acessar câmera/VM real neste gate.

# ARGOS-CRED-UI-01 — Matriz de estados, permissões e interação (V1 A)

Esta matriz é um **contrato de comportamento visual**, fundamentado nos handoffs **DRAFT**. Não cria autoridade nova para endpoints, papéis ou códigos HTTP. As respostas HTTP finais continuam sujeitas ao fechamento técnico.

| Cenário | Representação visual proposta | Operações | Cuidados |
|---|---|---|---|
| `NO_ACTIVE_CREDENTIAL` | “Nenhuma credencial ativa” / “Sem ativa” | Configurar se autorizado | Não afirmar nunca configurada ou revogada |
| `CONFIGURED` | “Credencial ativa configurada” + badge “Configurada” | Substituir; ações sensíveis conforme permissão | Não afirmar conexão validada; não exibir username/senha |
| `READ_ONLY` | Resumo sem ações de mutação/reveal | Consulta mínima | Permissão efetiva, não rótulo Técnico/Admin |
| `NO_METADATA_PERMISSION` | Seção inteiramente omitida no SSR | Nenhuma | Não vazar estado/metadata por DOM ou JS |
| `EDITING` | Diálogo nativo com username e nova senha vazios | Confirmar / Cancelar | Formulário de credencial independente do cadastral |
| `SUBMITTING` | Feedback de processamento, ação temporariamente indisponível | Aguardar | Bloqueio de botão não garante idempotência no backend |
| `SUCCESS_REPLACE` | Mensagem genérica após POST/Redirect/GET | Voltar à edição | Sem ecoar username ou password submetidos |
| `VALIDATION_ERROR` | Erro associado aos campos | Corrigir / Cancelar | Não reexibir senha; status HTTP final a revisar |
| `PERMISSION_DENIED` | Acesso negado, sem mencionar existência de segredo | Retornar | Autorização sempre validada no servidor |
| `RESOURCE_UNAVAILABLE` | Mensagem genérica segura | Retornar | Não divulgar metadados da credencial |
| `OPERATION_ERROR` | Mensagem genérica de indisponibilidade | Voltar/tentar depois | Sem stack, estado interno, versão/chave |
| `REVOKE_CONFIRMATION` | Diálogo com consequência operacional e confirmação explícita | Confirmar / Manter | Revogação remove credencial ativa sem fallback |
| `REVOKE_STATE_CONFLICT` | “Estado mudou; atualize a página” | Atualizar | Código 409 proposto, sujeito a contrato final |
| `UNSAVED_CAMERA_CHANGES` | Advertência antes de ação independente | Voltar; decidir salvar/descartar | Não descartar cadastro silenciosamente |
| `REAUTHENTICATION_REQUIRED` | Diálogo focado, campo senha atual | Autorizar / Cancelar | Senha atual jamais em storage/browser logs |
| `REVEAL_TRANSIENT` | Sessão visual transitória e explicitamente autorizada | Encerrar | Limpeza ao fechar/expirar/erro; no-store |

## Fluxos canônicos de interface

**A. Configurar/substituir:** consultar estado mínimo autorizado → abrir diálogo independente → apresentar campos username/password vazios → validar entradas sem divulgar segredo → confirmar → feedback sanitizado e retorno ao resumo. Repetição do POST não é idempotente por contrato; tratar com cautela.

**B. Revogar:** ação secundária condicional → confirmação com impacto na autenticação do dispositivo → POST separado → retorno genérico. Não oferecer restauração de versão revogada.

**C. Revelar:** ação condicional explícita → reautenticação pela senha atual **em cada solicitação** → resposta transitória via endpoint existente → limpar interface e dados da memória de UI quando encerrar. O protótipo **não exibe segredo real ou de demonstração**.

**D. Cadastro com alterações não salvas:** identificar estado dirty → impedir perda silenciosa → permitir resolução explícita antes de efetuar operação independente. O desenho de fallback sem JS deve ser negociado no handoff SSR.

## Matriz de permissão a respeitar

- Editar câmera: `cameras.change_camera` (existente).
- Metadata: `cameras.view_camera_credential` (service existente; projeção SSR ainda não encerrada).
- Replace/revoke: `cameras.change_camera_credential` (services existentes; novos endpoints HTTP ainda **propostos**).
- Reveal: `cameras.reveal_camera_credential` (endpoint atual existente, com POST/CSRF/reauth).
- Não derivar permissões de Técnico/Admin visualmente; consultar permissões Django efetivas.
- Botões ocultos são UX, **nunca substitutos da autorização do servidor**.

## Integração de formulários

O card pode estar **visualmente** dentro da pilha da edição, mas os formulários de credenciais **não podem ser aninhados** dentro de `CameraEdicaoForm`. Usar composição de formulários irmãos, atributos `form` quando adequados ou diálogo fora do `<form>` cadastral, conforme implementação SSR. Cada ação possui submit e persistência independentes.

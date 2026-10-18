# ARGOS E3 — Aditivo visual de elegibilidade da captura (DRAFT)

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
ACTIVITY = ARGOS-E3-CAPTURE-ELIGIBILITY-UI-REVIEW
CONTRACT_STATUS = DRAFT
USER_APPROVED_FUNCTIONAL_DIRECTION = C
VISUAL_BASELINE = E3_VARIANT_B_APPROVED
VISUAL_IMPLEMENTATION = NOT_AUTHORIZED
PRODUCTION_SOURCE_CHANGE = FORBIDDEN
HUMAN_VISUAL_APPROVAL = PENDING
UI_UX_SPECIALIST_REVIEW = NOT_AVAILABLE_IN_CURRENT_RUNTIME
E3_STATUS = IN_PROGRESS
E4_STATUS = NOT_STARTED
NEXT_GATE = USER_VISUAL_AMENDMENT_REVIEW
```

> Este aditivo registra uma direção funcional aprovada para estados de indisponibilidade e apresenta uma proposta visual. Não aprova os screenshots, não altera o contrato técnico nem autoriza mudanças no Django.

## 1. Autoridade e precedência

O usuário aprovou a direção funcional C para o comportamento contextual. A composição aprovada da Variante B permanece congelada para o estado em que upload e captura estão disponíveis: upload à esquerda, captura à direita no desktop e upload antes da captura no mobile.

Referência técnica obrigatória: `docs/projeto/contracts/backend/images/ARGOS_E3_CAPTURE_ELIGIBILITY_VISUAL_CONTRACT_DRAFT.md`. A proposta mantém suas fronteiras: permissão separada de capability/configuração/disponibilidade; serviço backend como enforcement; worker E3 atual HTTP Snapshot; diagnóstico RTSP não significa captura RTSP operacional; Target Policy e credential resolver canônicos; job/feedback derivados de estado real.

O pacote visual aprovado está em `docs/prototype/ui-botao-captura/`. Seu HTML V1 não foi alterado. O aditivo visual complementa os estados não cobertos pela aprovação original e não autoriza botão E4 produtivo, galeria, rota fictícia ou mudança de layout das demais regiões.

## 2. Decisão e escopo visual

**DECISÃO DO USUÁRIO:** `ALTERNATIVE_C_DIRECTION_APPROVED`.

**PROPOSTA VISUAL PARA REVISÃO:** manter a zona de captura para usuário autorizado, com conteúdo contextual seguro quando a operação não estiver disponível. O botão `Capturar imagem` só aparece quando a captura estiver autorizada/elegível e não houver job ativo impeditivo. Não renderizar controle desabilitado que pareça acionável em estados indisponíveis.

Para usuários sem `cameras.capture_camera_image`, omitir zona e detalhes de captura. Upload continua seguindo sua própria autorização. A visibilidade de UI nunca concede permissão; o backend permanece autoridade final.

O protótipo novo é uma peça de discussão sem Django, serviço, rede, câmera, upload, credenciais ou persistência. Nenhuma cópia desta proposta deve ser promovida a contrato de produção antes do aceite visual humano e autorização técnica própria.

## 3. Comparação com a Variante B

| Estado | Variante B aprovada | Direção C proposta | Delta permitido nesta revisão |
|---|---|---|---|
| Upload e captura disponíveis | Duas operações; upload à esquerda e captura à direita; ação de captura presente. `Ver imagens` é conceito E4 no protótipo original. | Mesma composição e hierarquia. Na proposta E3, não há ação `Ver imagens`. | Nenhum delta na composição B; somente a ausência produtiva de E4 continua autorizada. |
| Captura indisponível | Estado não foi especificado na aprovação original. | Zona contextual sem botão inerte; upload continua disponível à esquerda. | Novo estado visual aditivo sujeito à aprovação humana. |
| Só uma operação permitida | A referência original mostra duas operações, não define a malha de operação única. | A operação restante ocupa a largura sem divisor, padding interno de par ou coluna vazia. | Novo estado visual aditivo sujeito à aprovação humana. |
| Sem operação disponível | Não especificado na baseline B. | Omitir seção vazia ou mostrar mensagem genérica somente ao público autorizado, conforme causa e audiência definidas pelo backend. | Copy/contexto continuam pendentes de aceite. |

## 4. Cenários e regra de apresentação

| Cenário | Permissão / situação | Apresentação proposta | CTA de captura |
|---|---|---|---|
| 01 — Upload e captura disponíveis | Upload e captura permitidos; configuração elegível. | Baseline B intacta. Feedback só aparece quando refletir um job real. | `Capturar imagem`, ação explícita. |
| 02 — Indisponibilidade transitória | Usuário tem permissão de captura; serviço informa indisponibilidade temporária. | Zona de captura permanece no lugar, com mensagem curta e segura. Upload não muda. | Omitido enquanto indisponível. |
| 03 — Configuração incompleta | Usuário tem permissão; estado de configuração conhecido e autorizado para exibição. | Explicação genérica, sem endereço, credencial ou policy interna. | Omitido. |
| 04a — Método não suportado | Evidência canônica classifica o método como não suportado. | Diferenciar somente quando essa classificação for conhecida e segura. | Omitido. |
| 04b — Suporte desconhecido | Evidência ausente/ambígua; não equivale a `NONE`. | Informar que o suporte não foi confirmado; não inferir ausência universal de capability. | Omitido. |
| 05 — Só captura disponível | Usuário autorizado para captura; upload indisponível por regra independente. | Uma única zona de captura, largura fluida, sem divisor à esquerda/coluna vazia. | Presente se a captura estiver disponível. |
| 06 — Nenhuma operação disponível | Nenhuma ação permitida ao usuário. | Se usuário autorizado a conhecer o estado: mensagem genérica sem causa interna. Se não autorizado, não expor estado privilegiado; omitir a seção quando não houver upload permitido. | Omitido. |
| 07a — Job em processamento | Job real em `QUEUED` ou `RUNNING`, visível ao usuário autorizado e dono. | Feedback compacto ligado ao job. Nenhum sucesso antecipado. | Não apresentar segunda intenção enquanto o job impedir nova solicitação. |
| 07b — Job falhou | Job real em `FAILED`; serviço ainda permite uma nova intenção e usuário continua autorizado. | Mensagem de falha sanitizada; estado visual não altera monitoramento. | Pode reaparecer para uma nova intenção explícita, conforme contrato de idempotência. |
| 08 — Usuário sem permissão de captura | `capture_camera_image = NO`, upload avaliado separadamente. | Omitir zona, copy e detalhes de captura; renderizar upload apenas se permitido pelas próprias regras. | Omitido; a view não substitui enforcement backend. |

`AVAILABLE` significa ausência de bloqueador conhecido; não prova conectividade. Status de job, capability e configuração devem vir de fonte autorizada. O browser não fornece URL, IP, destino ou segredo.

## 5. Copy proposta

Todas as frases abaixo são propostas de conteúdo, ainda sujeitas a revisão de produto/segurança e aprovação humana.

| Estado | Título / feedback | Texto auxiliar |
|---|---|---|
| Temporária | **Captura indisponível no momento** | Tente novamente mais tarde. |
| Configuração incompleta | **Configuração de captura incompleta** | O perfil de captura desta câmera precisa ser revisado. |
| Método não suportado | **Método de captura não suportado** | O método configurado não é compatível com o fluxo de captura disponível. |
| Suporte desconhecido | **Suporte à captura não confirmado** | Não foi possível confirmar se este método está disponível. |
| Nenhuma operação | **Nenhuma operação de imagem disponível no momento** | Exibir somente se a política de autorização permitir a informação genérica. |
| QUEUED | **Captura solicitada** | Aguardando processamento. |
| RUNNING | **Captura em processamento** | A solicitação está sendo processada. |
| FAILED | **Não foi possível concluir a captura** | Tente novamente mais tarde. |

Não revelar endpoint, endereço IP, nome de credencial, segredo, política de destino ou detalhe de equipamento. Não anunciar “online” nem “capturada” a partir de elegibilidade/configuração. `SUCCEEDED` só deve ser exibido quando o job real confirmar conclusão.

## 6. Malha, alinhamento e responsividade

- Com as duas operações disponíveis, preservar a Variante B aprovada, incluindo divisor neutro e proporção de zonas existente.
- Com duas zonas presentes, upload permanece à esquerda e captura à direita no desktop; no mobile, upload vem primeiro e captura depois, com separador horizontal.
- Se somente upload estiver presente, usar uma coluna integral, sem padding de lado destinado ao divisor.
- Se somente captura estiver presente, usar uma coluna integral, sem borda esquerda, padding de par ou coluna vazia.
- Se não existir nenhuma operação ou informação autorizada, não renderizar um card ou espaço vazio artificial.
- Não alterar a superfície, tipografia, cores, sidebar, topbar, Histórico, Quick Detail ou CSS global.
- Textos longos podem quebrar linhas; botões e controles não devem causar overflow horizontal.
- Ação E4 `Ver imagens` fica fora da proposta funcional E3; manter espaço composicional suficiente para evolução futura sem reservá-lo artificialmente.

## 7. Acessibilidade proposta

- O seletor de cenário do protótipo é nativo, rotulado e operável por teclado.
- Ações disponíveis têm nome acessível e foco visível; as mensagens não são interativas.
- Disponibilidade e job são comunicados por texto, não somente por cor ou ícone.
- Mudança de job pode usar região viva `role="status"`/`aria-live="polite"`; evitar anúncios repetidos de estados estáticos.
- Erro não deve remover foco do usuário nem usar um diálogo inesperado.
- Recomendação de contraste: texto comum ≥ 4.5:1 e foco/contorno distinguível; a verificação renderizada e teste com leitor de tela permanecem pendentes.
- O protótipo não demonstra conformidade WCAG completa. Teclado, contraste computado no browser e leitor de tela precisam de validação antes do aceite final.

## 8. Critérios de aceite visual propostos

1. No cenário 01, composição Variante B permanece visualmente idêntica no escopo permitido.
2. Em 02–04, a captura autorizada mantém hierarquia contextual, sem botão inerte.
3. Os estados 03/04 não revelam credenciais, destino ou detalhe de policy.
4. Método não suportado e suporte desconhecido só se diferenciam quando o estado técnico é conhecido.
5. Em 05 e 08, uma operação isolada não deixa coluna vazia, divisor solto ou padding de pareamento.
6. Em 06, não aparece informação privilegiada para quem não tem permissão e não há card vazio artificial.
7. Em 07, o texto segue o estado real do job e não antecipa sucesso; CTA de nova captura depende de nova intenção permitida.
8. Variante B mantém a ordem desktop e mobile aprovada quando ambas operações estão disponíveis.
9. `Ver imagens` não é uma ação funcional ou inerte em E3; continua exclusiva do futuro escopo E4.
10. Em 2048×742, 1440×900, 1366×768 e 390×844, a composição deve permanecer fluida sem overflow; cada viewport será comparado no estado correspondente.
11. Seletor/copy/CTA do protótipo são acessíveis por teclado e têm foco visível; estados são legíveis sem depender só de cor.
12. O Django real, backend e dados QA não são evidência deste protótipo e exigem gate separado de implementação autorizada.

## 9. Conflitos, riscos e limites

- O contrato técnico base ainda registra C como recomendação. Este aditivo registra a nova decisão humana sobre a direção funcional, preservando a decisão de política técnica e os gates restantes.
- A proposta não pode ser implementada até haver autorização própria; o usuário já declarou `VISUAL_IMPLEMENTATION = NOT_AUTHORIZED`.
- É necessário confirmar quais categorias de indisponibilidade o backend pode distinguir com segurança. A UI não deve inferir estado a partir de falha genérica de request.
- A operação capture-only e upload-only precisa de contexto SSR estruturalmente correto; CSS isolado não corrige autorização nem contexto.
- O status de job não pode ser usado para criar outra solicitação; idempotência e ownership permanecem do backend.
- A função `SENIOR_UI_UX_FRONTEND_CONSULTANT` não está disponível no catálogo de execução desta sessão. Esta revisão é preliminar, feita pelo root com a referência visual e a skill de design disponíveis; não substitui parecer independente do especialista selecionado.
- Não foi possível abrir/renderizar o HTML local no navegador integrado nesta sessão. Logo, nenhum viewport novo, screenshot ou acessibilidade por interação é declarado PASS nesta revisão.

## 10. Artefatos e status

```text
VISUAL_PROTOTYPE = docs/prototype/ui-botao-captura/proposal-c/ARGOS_E3_CAPTURE_ELIGIBILITY_STATES_PROPOSAL_V1.html
VISUAL_CONTRACT_DRAFT = docs/projeto/contracts/backend/images/ARGOS_E3_CAPTURE_ELIGIBILITY_VISUAL_AMENDMENT_DRAFT.md
DESIGN_QA = docs/prototype/ui-botao-captura/proposal-c/design-qa.md
SCENARIOS_COVERED = 01, 02, 03, 04a, 04b, 05, 06, 07a, 07b, 08
RESPONSIVE_VALIDATION = BLOCKED / browser capture unavailable
ACCESSIBILITY_REVIEW = STATIC_ONLY / keyboard and assistive-technology verification pending
VARIANT_B_PRESERVED = YES_IN_SCENARIO_01 / visual render verification pending
UPLOAD_PRESERVED = REPRESENTED_VISUALLY; backend unchanged
NO_INERT_CAPTURE_BUTTON = YES_IN_UNAVAILABLE_STATES / static source inspection
UI_UX_SPECIALIST_REVIEW = NOT_AVAILABLE_IN_CURRENT_RUNTIME
HUMAN_VISUAL_APPROVAL = PENDING
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
PRODUCTION_SOURCE_CHANGED = NO
QA_DATA_CHANGED = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
E3_STATUS = IN_PROGRESS
E4_STATUS = NOT_STARTED
NEXT_GATE = USER_VISUAL_AMENDMENT_REVIEW
```

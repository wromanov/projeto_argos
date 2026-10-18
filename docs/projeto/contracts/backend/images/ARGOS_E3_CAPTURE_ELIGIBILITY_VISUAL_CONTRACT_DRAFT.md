# ARGOS E3 — Capture Eligibility and Visual Stability Contract (Draft)

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
ACTIVITY = ARGOS-E3-CAPTURE-ELIGIBILITY-CONTRACT
CONTRACT_STATUS = DRAFT
DIAGNOSTIC_REVIEW = COMPLETED
ROOT_REVIEW = PASS
USER_APPROVAL = PENDING
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
VISUAL_BASELINE = E3_VARIANT_B_APPROVED
VISUAL_CONTRACT_AMENDMENT_REQUIRED = YES
UI_UX_SPECIALIST_REVIEW = REQUIRED
HUMAN_VISUAL_APPROVAL = PENDING
E2_STATUS = CLOSED_WITH_EXCEPTIONS
E3_STATUS = IN_PROGRESS
E4_STATUS = NOT_STARTED
HML_VM_DEPLOY = DEFERRED
NEXT_GATE = USER_CONTRACT_REVIEW
```

> Este documento materializa um diagnóstico e uma proposta técnica. Ele não aprova a alternativa C, não altera o baseline visual e não autoriza implementação.

## 1. Identificação e escopo

O contrato trata da apresentação SSR e do enforcement da ação de captura manual na seção **Operações complementares** da Camera Detail, quando elegibilidade, autorização ou disponibilidade variam. O upload manual existente deve permanecer independente da elegibilidade de captura.

O baseline aprovado para o cenário original com as duas operações elegíveis continua sendo a Variante B: upload à esquerda e captura à direita no desktop; upload primeiro e captura depois no mobile. Não há escopo de Quick Detail, Design System global, E4/galeria, sidebar, topbar, Histórico, acesso a câmeras reais, mudança de source ou dados QA.

## 2. Rótulos de evidência

- **FATO**: comportamento ou implementação confirmado no source indicado pelo diagnóstico.
- **EVIDÊNCIA**: fonte/trecho que sustenta o fato ou limite da verificação.
- **INFERÊNCIA**: consequência técnica derivada dos fatos, sem observação operacional adicional.
- **PROPOSTA**: comportamento recomendado para aprovação; não é requisito ratificado.
- **DECISÃO PENDENTE**: escolha reservada ao root/autoridade humana competente.

## 3. Problema observado e causa demonstrada

**FATO — SSR:** o booleano `can_capture_camera` controla tanto a renderização do painel de captura quanto a classe de composição da seção. A view monta esse contexto e o template condiciona as operações. Quando o booleano é falso, a operação de upload pode permanecer sozinha e a composição muda.

**EVIDÊNCIA:** `cameras/imagens/capture_service.py:100–114`; `cameras/views.py:517–535`; `cameras/templates/cameras/detalhe.html:239–272`.

**FATO — autorização:** a permissão `cameras.capture_camera_image` é exigida no caminho backend para solicitar captura.

**EVIDÊNCIA:** `cameras/authorization.py:27`; `cameras/views.py:539–558`.

**Limite:** as evidências demonstram que a visibilidade do painel depende de elegibilidade/capacidade operacional comunicada por `can_capture_camera`; não demonstram que ocultar o painel seja a política UX correta. Testes existentes que esperam ocultação refletem a implementação observada, não uma autoridade de UX ratificada.

## 4. Authorities, precedência e limites

O card de diagnóstico autoriza diagnóstico READ_ONLY e materialização DRAFT; declara `IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED` e `VISUAL_CHANGE_AUTHORIZATION = NOT_GRANTED`. A Variante B foi aprovada para o estado em que ambas operações estão disponíveis, mas não aprova automaticamente o comportamento de estados indisponíveis.

Precedência documental e técnica deve respeitar os contratos canônicos aplicáveis, incluindo o contrato do domínio de imagem, o contrato de integração de captura, CAM-INT-04 HTTP Snapshot, demais contratos CAM-INT referenciados pelo card, BC-AUTH, plano/roadmap/sprints e aprovação visual. O diagnóstico identificou uma lacuna de conformidade para RTSP em atividade futura; este DRAFT não adjudica o conflito nem altera esses documentos.

### Rastreabilidade das authorities

Os caminhos abaixo foram localizados como referências canônicas para esta atividade. O parecer consolidado confirma a consulta ao contrato de domínio ao registrar que BC-02 define HTTP/RTSP. Para os demais itens, o consolidado não registra um estado individual de leitura por arquivo; sua inclusão aqui não afirma nova revisão documental nem substitui as fontes normativas vigentes.

| Área | Caminho canônico | Estado rastreável |
|---|---|---|
| Execução | `docs/projeto/ARGOS_DELIVERY_EXECUTION_PLAN_V1.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Roadmap | `docs/projeto/ROADMAP_ARGOS_V5.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Sprints | `docs/projeto/SPRINTS_ARGOS_V5.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Domínio de imagens | `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` | Consulta confirmada pelo achado citado: BC-02 define HTTP/RTSP. |
| Integração de captura | `docs/projeto/contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-01 — Capability Catalog | `docs/projeto/contracts/backend/camera/CAM-INT-01_CAPABILITY_CATALOG_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-02 — Credentials | `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-02-R1 — Runtime Credential Resolution | `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-03 — RTSP Connection | `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-03 — Target Policy Configuration | `docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-04 — HTTP Snapshot | `docs/projeto/contracts/backend/camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-06 — Vendor Model Capabilities | `docs/projeto/contracts/backend/camera/CAM-INT-06_VENDOR_MODEL_CAPABILITIES_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| CAM-INT-07 — Integration Hardening | `docs/projeto/contracts/backend/camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Autorização BC-AUTH | `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Continuidade — agente | `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Continuidade — estado | `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Continuidade — mapa documental | `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Aprovação visual | `docs/prototype/ui-botao-captura/01_VISUAL_APPROVAL_AND_CONTRACT.md` | Caminho localizado; leitura individual não registrada no parecer consolidado. |
| Protótipo aprovado | `docs/prototype/ui-botao-captura/prototype/ARGOS_E3_IMAGE_OPERATIONS_PROTOTYPE_V1.html` | Caminho localizado; leitura individual não registrada no parecer consolidado. |

**DECISÃO PENDENTE:** revisão do root e decisão humana explícita sobre A/B/C, copy, casos visuais adicionais e eventual adendo ao contrato visual. Nenhuma implementação decorre automaticamente deste DRAFT.

## 5. Invariantes funcionais e de segurança

1. Permissão do usuário, capability técnica, configuração operacional e disponibilidade são dimensões independentes.
2. Mostrar uma zona ou uma mensagem nunca concede permissão para capturar.
3. O backend deve validar autorização e elegibilidade no momento da operação; frontend, visibilidade do botão e polling não são enforcement.
4. Usuário sem `cameras.capture_camera_image` não executa a captura nem recebe detalhes de capability/configuração que permitam inferir informações internas.
5. O upload manual continua disponível segundo suas próprias regras e não é bloqueado pela inelegibilidade de captura.
6. Browser não escolhe URL, IP ou destino da captura. Resolução de alvo e credenciais usa Target Policy e serviços canônicos.
7. Segredos, URIs autenticadas e detalhes internos não aparecem em logs, mensagens ou respostas públicas.
8. CSRF, ownership do job, respostas sanitizadas e `no-store` continuam obrigatórios nos endpoints aplicáveis.
9. Disponibilidade calculada sem bloqueadores conhecidos não equivale a teste de conectividade.
10. Diagnóstico RTSP não equivale a captura RTSP executável pelo worker E3.

## 6. Política de renderização recomendada (proposta)

**PROPOSTA DO DIAGNÓSTICO — Alternativa C:** manter apresentação contextual da operação para o público autorizado, variando o conteúdo conforme a condição operacional. Quando a captura estiver indisponível, informar estado/motivo seguro sem apresentar botão inerte. Para usuário não autorizado, não expor a zona privilegiada nem o motivo/capability; o enforcement server-side permanece obrigatório. O upload preserva sua própria apresentação.

Esta é uma recomendação, não uma decisão. Requer revisão de UX/UI e aprovação visual humana para os novos estados. O texto exato da mensagem/copy não está aprovado neste DRAFT.

## 7. Comparação A/B/C nos 11 critérios

A = ocultar a captura quando inelegível; B = manter zona para autorizado com botão desabilitado e explicação; C = apresentação contextual, sem exigir botão desabilitado. A avaliação abaixo registra trade-offs da proposta, não escolha ratificada.

| Critério | A — Ocultar | B — Zona + botão desabilitado | C — Contextual (recomendada pelo diagnóstico) |
|---|---|---|---|
| 1. Coerência com contrato visual aprovado | Aprovada apenas para estado elegível; em inelegibilidade o painel desaparece e a composição muda. | Mantém duas zonas, porém acrescenta estado de controle inativo não coberto pelo baseline. | Preserva hierarquia geral; os novos estados precisam adendo/revisão visual restritos. |
| 2. Consistência entre câmeras | A composição varia conforme cada câmera. | Mantém estrutura previsível para autorizados. | Mantém estrutura contextual previsível para autorizados, com conteúdo adaptado. |
| 3. Usabilidade operacional | A não explica a ausência; usuário pode não saber se a câmera não suporta ou se está indisponível. | Explica a condição, mas botão desabilitado pode parecer acionável ou gerar dúvida. | Explica condição conhecida sem affordance falsa de execução. |
| 4. Acessibilidade | Menos controles, porém mudanças de composição/ausência podem não comunicar motivo. | Exige semântica acessível de disabled, explicação associada e foco coerente. | Estado informativo sem controle inerte; precisa texto/semântica acessíveis e anúncio apropriado. |
| 5. Segurança e autorização | Não expõe a zona quando ocultada; ainda exige autorização server-side. | Pode revelar estado operacional se política de público não for separada da autorização. | Deve ocultar detalhes a não autorizados; para autorizados, mensagem sanitizada. Backend segue como autoridade. |
| 6. Simplicidade de implementação | Menor mudança aparente, mas mantém acoplamento entre elegibilidade, presença de operação e malha. | Requer estado disabled e explicação para cada condição. | Requer classificação clara de estado e copy contextual; separa melhor apresentação de execução. |
| 7. Compatibilidade com Django SSR | Compatível, mas a presença/classe dependem de booleano e mudam layout. | Compatível; view deve fornecer estado e motivo público seguro. | Compatível; SSR pode escolher conteúdo contextual a partir de estado explícito. |
| 8. Compatibilidade HTTP/RTSP | Só exibe método elegível já suportado; pode tratar ausência de HTTP como ausência total se predicado for estreito. | Pode representar indisponibilidade, mas capability precisa ser distinguida do método executável. | Pode representar capability e estado separadamente, desde que RTSP diagnóstico não seja apresentado como captura implementada. |
| 9. Responsividade | Upload expande quando painel some; layout varia por câmera. | Estrutura constante pode empilhar no mobile; estado desabilitado também exige espaço. | Estrutura contextual pode preservar hierarquia; cada estado novo precisa QA desktop/mobile. |
| 10. Risco de regressão | Mudanças de composição podem afetar seletores de primeira/última operação e colunas vazias. | Pode manter estrutura, mas aumenta risco de estados de botão inconsistentes. | Risco na classificação/copy e nos estados adicionais; mitigável com matriz SSR e testes focados. |
| 11. Aprovação visual complementar | Necessária para comportamento de inelegibilidade que diverge do estado baseline. | Necessária por introduzir botão disabled e estado novo. | Necessária; revisão deve cobrir somente indisponibilidade e combinações de operações, sem reabrir a Camera Detail inteira. |

## 8. Matriz de estados e cenários

`AVAILABLE` deve ser lido como **sem bloqueador conhecido segundo configuração/policy**, nunca como prova de conexão com o dispositivo. `TEMPORARILY_UNAVAILABLE` representa falha transitória observada pelo fluxo operacional/job. `UNKNOWN` não deve ser convertido em `NONE`.

| Usuário autorizado? | Capability | Configuração | Disponibilidade | UI proposta para autorizado | Ação de captura | Enforcement |
|---|---|---|---|---|---|---|
| NO | qualquer | qualquer | qualquer | Não expor painel privilegiado nem motivo/capability; upload segue sua permissão independente. | Não | Permissão no backend obrigatória; negar sem revelar detalhe. |
| YES | HTTP | READY: config enabled, câmera ativa, perfil HTTP ativo, evidência `SUPPORTED`, credencial/version binding se auth necessária, alvo aceito por policy | AVAILABLE (sem bloqueador conhecido; sem probe de rede) | Zona acionável conforme baseline quando upload também elegível. | Habilitada | Revalidar autorização, configuração, alvo, credencial e ownership/estado no serviço. |
| YES | HTTP | READY | TEMPORARILY_UNAVAILABLE / job falhou | Estado informativo seguro; nova tentativa depende da política/job. | Não habilitar para o job terminal existente; nova intenção conforme contrato de idempotência aprovado | Serviço valida estado e cria/processa job segundo contrato. |
| YES | HTTP | INCOMPLETE | qualquer | Estado contextual informa configuração incompleta sem expor segredo ou URI. | Não | Serviço recusa; nunca aceitar destino/segredo do browser. |
| YES | HTTP | UNSUPPORTED | qualquer | Estado contextual informa método não suportado/configurado. | Não | Serviço recusa. |
| YES | HTTP | BLOCKED por Target Policy | qualquer | Estado contextual seguro, sem revelar destino/policy interna. | Não | Policy canônica bloqueia no backend. |
| YES | RTSP | READY/diagnóstico suportado | AVAILABLE/diagnostic status | Não apresentar captura RTSP como executável pelo worker E3; comunicar limite segundo copy ainda pendente. | Não via worker E3 atual | Diagnóstico não substitui execução; não criar atalho/bypass. |
| YES | RTSP | INCOMPLETE / BLOCKED / UNKNOWN | qualquer | Estado informativo apenas se seguro e definido por autoridade/copy aprovada. | Não via worker E3 atual | Backend mantém negação; capability desconhecida não implica permissão. |
| YES | NONE | qualquer | qualquer | Estado contextual sem sugerir ausência universal de capacidade além do que a evidência sustenta. | Não | Recusa server-side. |
| YES | UNKNOWN | qualquer | qualquer | Estado desconhecido; não inferir falta universal de capability. | Não até classificação/estado operacional | Recusa fail-closed. |
| YES | HTTP | READY | job próprio: queued/running/terminal | Mostrar estado do job autorizado/owned, sanitizado e sem duplicar consultas. | Seguir estado e regras de nova intenção; não simular sucesso | Permissão + ownership; polling controlado. |

### Estados do job e acompanhamento

**FATO:** o endpoint de status exige permissão e ownership do job, sanitiza a resposta, usa `no-store` e o cliente faz polling a cada 2 segundos até estado terminal ou navegação. **PROPOSTA:** preservar essas propriedades e não permitir que acompanhamento crie jobs/capturas. Mensagens de estado devem derivar do job real, não de temporizadores que simulem sucesso.

## 9. Matriz de contrato técnico proposto — 18 itens

1. **Identificação/escopo:** estado SSR da captura na Camera Detail para E3; fora de E4 e áreas protegidas.
2. **Problema/causa:** `can_capture_camera` condiciona painel e classe de composição; falta de elegibilidade altera a presença da zona e amplia upload.
3. **Authorities/precedência:** card original, contratos ratificados e aprovações vigentes prevalecem; este documento permanece DRAFT e aponta lacuna de RTSP a adjudicar.
4. **Invariantes funcionais:** upload independente; UI não concede acesso; capability/config/status não são sinônimos; backend é enforcement.
5. **Política recomendada:** Alternativa C, somente proposta, com informação contextual para usuário autorizado sem botão inerte quando indisponível.
6. **Elegibilidade/estados:** classificar autorização, capability HTTP/RTSP/NONE/UNKNOWN, configuração READY/INCOMPLETE/UNSUPPORTED/BLOCKED, disponibilidade e job separadamente.
7. **Usuários:** negar operação ao não autorizado e não expor detalhe operacional; authorized recebe apenas status sanitizado.
8. **Botão/copy/feedback:** ação habilitada apenas quando autorização e elegibilidade permitirem; sem botão inerte em C; copy ainda depende de revisão/aceite humano.
9. **HTTP/RTSP:** worker E3 executa somente HTTP Snapshot. RTSP possui diagnóstico/suporte representado, mas não execução de bytes de imagem no worker E3. Não declarar RTSP como captura operacional.
10. **Backend vs frontend:** view/SSR pode apresentar estado; serviço/endpoint revalida autorização, configuração, Target Policy, resolução canônica de credenciais e estado do job. Frontend não decide segurança.
11. **Upload:** preservar contrato, ação, validação e disponibilidade do upload; captura não altera seu funcionamento.
12. **Segurança/CSRF/autorização:** validar permissão em toda operação, CSRF em POST, ownership no status, respostas públicas sanitizadas/no-store; nenhum destino arbitrário do browser.
13. **Responsividade:** desktop mantém composição baseline quando ambas elegíveis; mobile mantém upload antes da captura. Estados de uma operação devem não reservar coluna/divisor sem par.
14. **Variante B:** baseline com ambas operações elegíveis não muda. Estado capture-only exige revisão/aceite visual complementar restritos; não reabrir design completo.
15. **Testes:** cobrir matriz de autorização/capability/config/policy/disponibilidade/job, HTML SSR, serviço e integração autorizada; fake não é HML nem validação de câmera real.
16. **Aceite proposto:** autorização efetiva, nenhum bypass, estado SSR correto, upload preservado, nenhum job duplicado por reenvio da mesma intenção, estados terminais reais, layouts responsivos sem colunas/divisores vazios.
17. **Riscos/limites:** acoplamento booleano e seletores de operação, RTSP não implementado no worker E3, `READY` não prova conectividade, novas mensagens exigem copy/UX review, testes fake não atestam operação real.
18. **Aprovações pendentes:** escolher A/B/C, copy, casos e amendment visual; aprovar contrato; implementação segue `NOT_GRANTED` até autoridade humana explícita.

## 10. Estrutura CSS quando existe apenas uma operação

**FATO — adendo do Diagnostic Analyst:** com `can_capture_camera=True` e `add_cameraimagerecord=False`, o template omite upload (`detalhe.html:242–254`) e renderiza uma única `section.image-operation` para captura (`:255–266`). Como o header é outro tipo de elemento, essa única section satisfaz ambos os seletores `:first-of-type` e `:last-of-type`.

Consequências determinísticas no CSS:

- `camera-detail.css:437–443`: captura recebe a malha interna `.85fr 1.15fr`, alinhamento central e `padding-inline-end:16px`, regras destinadas à composição de upload.
- `:446–448`: também recebe padding esquerdo e borda esquerda.
- Wrapper permanece com duas colunas (`:413–414`) apesar de existir uma operação; a coluna vazia não tem par de operação.
- Mobile (`:563–566`) torna o grid interno uma coluna e remove o padding final; `:569–572` adiciona padding superior e divisor horizontal mesmo sem operação anterior.

**Limite de evidência:** aplicação dos seletores está confirmada; magnitude de defeito perceptivo nesse cenário requer screenshot/computed style específico, não executado pelo adendo.

**Critério proposto:** uma operação isolada não herda malha interna, divisor entre operações inexistentes ou coluna vazia que pertença ao pareamento com a outra operação. A separação de 16 px entre botão de upload e divisor só se aplica quando upload e captura coexistirem. Não se prescreve implementação CSS neste DRAFT.

**DECISÃO VISUAL PENDENTE:** captura-only elegível, captura-only indisponível e job próprio sem upload requerem revisão/aceite visual complementar restritos. Isso não muda o baseline aprovado da Variante B quando ambas operações são elegíveis.

## 11. Matriz de testes proposta

| Caso | Preparação/ação | Resultado esperado proposto |
|---|---|---|
| Usuário sem permissão, GET Camera Detail | capability/config variáveis | Não revelar detalhes da captura; upload segue permissão própria. |
| Usuário sem permissão, POST capture | CSRF válido/inválido | Negado server-side; nenhum job criado; resposta sanitizada. |
| Upload permitido sem captura | HTTP/sem capability | Upload permanece funcional e sem regressão. |
| HTTP elegível e autorizado | configuração enabled, perfil/evidência suportados, credencial version-bound se necessária, alvo permitido | Painel SSR conforme baseline; serviço cria job segundo idempotência. |
| HTTP sem configuração/incompleto | autorizado | Estado contextual proposto; ação negada; nenhum destino alternativo. |
| Capability unsupported / policy BLOCKED | autorizado | Estado seguro; backend recusa; sem exposição de policy/destino interno. |
| Credencial ausente/versão inválida | autorizado | Falha fechada sem revelar segredo; sem fallback inseguro. |
| `AVAILABLE` sem conectividade validada | configuração aparentemente READY | Não afirmar que câmera está conectada; estado não é probe. |
| Falha transitória | job real falha | Feedback deriva do estado terminal real; nenhuma simulação de sucesso. |
| Status de job | usuário autorizado e dono / não dono / sem permissão | Apenas authorized + owner acessa; resposta sanitizada/no-store. |
| Polling | job queued/running/terminal, navegação | Intervalo controlado de 2s segundo implementação observada; termina em estado terminal ou navegação; sem chamadas duplicadas. |
| Idempotência | reenvio mesma intenção / nova intenção deliberada | Reenvio não duplica job indevidamente; intenção nova pode gerar nova solicitação conforme contrato. |
| CSRF | POST capture válido/inválido | Rejeição/aceite conforme proteção Django; sem bypass. |
| RTSP suportado/diagnóstico | config RTSP | Diagnóstico não produz job executável por worker E3; nenhum caminho falseia captura RTSP. |
| RTSP desconhecido/bloqueado | várias configs/policy | Fail closed; não converter ausência de HTTP em ausência universal de capacidade. |
| Ambas operações elegíveis | desktop/mobile | Variante B: upload esquerda/captura direita; mobile upload primeiro; baseline preservado. |
| Upload + captura indisponível | autorização permitida | Estado C proposto sem botão inerte; necessidade de aceite visual restrito. |
| Captura elegível sem upload | usuário autorizado, `add_cameraimagerecord=False` | Uma operação sem grid/divisor/coluna vazia herdada do par; acceptance visual complementar restrito. |
| Captura indisponível sem upload | usuário autorizado | Estado contextual sem botão inerte e sem estilos que pressupõem operação irmã; acceptance visual complementar restrito. |
| Job próprio sem upload | queued/running/terminal | Estado real do job sem criar coluna ou divisor da operação ausente. |
| Não autorizado em capture-only | operação captura presente na configuração | Não mostrar detalhe privilegiado nem executar; backend nega. |
| SSR e responsividade | 2048x742, 1440x900, 1366x768, 390x844 conforme QA aplicável | Sem overflow; hierarquia baseline quando ambas existem; novos cenários visualmente aprovados. |
| Testes com fake | adapter fake e dados sintéticos | Evidência local de implementação somente; não declarar HML ou validação operacional. |

## 12. Segurança, riscos e limitações

- **FATO:** resolução de segredo ocorre no worker depois de policy/autorização; o browser não deve fornecer URL/IP/destino arbitrário.
- **FATO:** status do job exige permissão e ownership, resposta sanitizada e `no-store`; polling atual é 2s até estado terminal ou navegação.
- **FATO:** serviço E3 atual executa apenas HTTP Snapshot.
- **FATO:** RTSP aparece em enums/modelos/diagnóstico, mas serviço/adapters RTSP referidos pelo diagnóstico retornam estado/resultado diagnóstico, não bytes de imagem IMG-CAP consumidos pelo worker E3 (`cameras/imagens/rtsp/service.py:17`; `ports.py:135–139`; `gst_adapter.py:42–54`). O domínio BC-02 define HTTP/RTSP. O diagnóstico classifica isso como lacuna de conformidade para atividade futura.
- **INFERÊNCIA:** tratar `HTTP` ausente como `NONE` pode ocultar a distinção entre falta de configuração HTTP e suporte/capacidade RTSP, embora RTSP não seja executável pelo worker atual.
- **RISCOS:** estados SSR e CSS podem divergir; seletores `first-of-type`/`last-of-type` assumem coexistência; disponibilidade sem tentativa de conexão pode ser interpretada erroneamente como online; copy pode revelar informação; botão disabled cria affordance confusa; novos estados podem alterar layouts responsivos.
- **LIMITAÇÃO:** nenhum teste fake comprova integração contra HML ou câmera real. Acesso/captura real é vedado nesta atividade.

## 13. Decisões e revisões humanas pendentes

1. Selecionar A, B ou C; a recomendação C permanece proposta.
2. Aprovar copy e os limites de detalhe apresentados a usuários autorizados.
3. Aprovar amendment visual restrito para captura indisponível e para operação capture-only/job sem upload.
4. Realizar revisão UI/UX especializada nesses cenários, sem reabrir design completo da Camera Detail.
5. Root review e aprovação do contrato.
6. Conceder ou não autorização explícita de implementação em atividade posterior.
7. Adjudicar a lacuna de conformidade RTSP versus o domínio BC-02 em atividade apropriada; este DRAFT não define cronograma nem solução.

## 14. Status e validação

```text
ALTERNATIVES_EVALUATED = A | B | C; 11 CRITERIA
RECOMMENDED_SOLUTION = C (PROPOSAL ONLY)
TECHNICAL_JUSTIFICATION = SSR eligibility coupling; authorization/backend enforcement; HTTP-only E3 worker; RTSP diagnostic-only; one-operation selector/layout coupling
SECURITY_IMPACT = NO AUTHORIZATION BY UI; SERVER-SIDE PERMISSION/POLICY/OWNERSHIP REQUIRED
REGRESSION_RISK = SSR/CSS COMPOSITION, RTSP CAPABILITY CLASSIFICATION, RESPONSIVE STATES, COPY DISCLOSURE
CONTRACT_FILE = docs/projeto/contracts/backend/images/ARGOS_E3_CAPTURE_ELIGIBILITY_VISUAL_CONTRACT_DRAFT.md
CONTRACT_STATUS = DRAFT
DIAGNOSTIC_REVIEW = COMPLETED
ROOT_REVIEW = PASS
USER_APPROVAL = PENDING
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
VISUAL_CONTRACT_AMENDMENT_REQUIRED = YES
UI_UX_SPECIALIST_REVIEW = REQUIRED
HUMAN_VISUAL_APPROVAL = PENDING
SOURCE_CODE_CHANGED = NO
QA_DATA_CHANGED = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
E2_STATUS = CLOSED_WITH_EXCEPTIONS
E3_STATUS = IN_PROGRESS
E4_STATUS = NOT_STARTED
HML_VM_DEPLOY = DEFERRED
OPERATIONAL_CAMERA_VALIDATION = NOT_PERFORMED
NEXT_GATE = USER_CONTRACT_REVIEW
```

### Limites de validação

Este DRAFT não declara testes adicionais, conformidade visual aprovada, homologação HML ou captura operacional. As referências acima são as evidências rastreadas pelo parecer; não foram acessados browser, QA ou câmeras durante a materialização.



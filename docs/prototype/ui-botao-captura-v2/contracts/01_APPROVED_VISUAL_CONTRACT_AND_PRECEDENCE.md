# Contrato visual consolidado — E3 elegibilidade C V2.1

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
ACTIVITY = ARGOS-E3-CAPTURE-ELIGIBILITY-C-V2-1-VISUAL-HANDOFF
CONTRACT_SCOPE = VISUAL_PRESENTATION_ONLY
HUMAN_APPROVED_VARIANT_B = PASS
HUMAN_APPROVED_CONTEXTUAL_STATES_C_V2_1 = PASS
VISUAL_BASELINE = B_WITH_ADDITIVE_C_STATES
COMPOSITION_STATUS = FROZEN
CONTRACTUAL_BACKEND_BEHAVIOR = SUBJECT_TO_CANONICAL_RECONCILIATION
DJANGO_C_IMPLEMENTATION = PENDING_AUTHORIZATION
DJANGO_HUMAN_VISUAL_APPROVAL = PENDING
E4 = OUT_OF_SCOPE
```

## 1. Evidência da decisão

O usuário aprovou expressamente a alternativa B de E3 e, depois, aprovou a Proposta C V2.1. Este documento registra essas decisões **visuais**, não ratifica automaticamente decisões técnicas, de segurança ou contratos HTTP/SSR.

## 2. Ordem de autoridade

Para **composição visual**:

1. Decisões humanas explícitas mais recentes para E3, especialmente a **superfície branca única** e agrupamento final de upload e captura.
2. `prototype/ARGOS_E3_CAPTURE_ELIGIBILITY_STATES_PROPOSAL_V2_1.html` para a apresentação dos cenários C.
3. Variante B V1 aprovada para grid, hierarquia e aparência-base nos cenários de duas operações disponíveis.
4. Contrato B V1 **histórico** e adendo C anterior em DRAFT apenas como contexto; não prevalecem contra refinamentos visuais posteriores.

Para **funcionalidade, permissões, fluxo de job e segurança**, prevalecem exclusivamente os contratos técnicos ativos verificados pelo agente ARGOS no repositório. Este pacote não os substitui.

## 3. Composição invariável

- Área: `Camera Detail → Operações complementares`.
- **Uma superfície branca única**, com borda neutra discreta e raio igual aos cards vigentes; sem sombras ou novos cards de alerta.
- Desktop com duas operações: **Upload à esquerda, Captura à direita**, separadas por divisor vertical neutro de 1px.
- O upload reúne título + texto auxiliar no mesmo wrapper; label `Imagem`, input file nativo e botão `Enviar imagem` agrupados, sem texto flutuante, truncamento indevido ou botão colado ao divisor.
- A captura reúne título, descrição, botão `Capturar imagem` com ícone e feedback compacto, com espaçamento vertical já ajustado na implementação E3; não alterar esse acabamento fora do necessário.
- Mobile: upload antes de captura; divisor horizontal quando houver ambas as operações; controles fluidos.
- Em estados com uma operação, **coluna inteira**, sem divisor nem margem residual do par.
- Quando o contexto autorizado não oferece operações nem mensagem permitida, **não renderizar espaço artificial**.
- Estados de indisponibilidade de captura: **mensagem inline discreta**, sem CTA inerte nem um card amarelo/vermelho adicional; textos são sujeitos a autorização/semântica do backend.
- Em `FAILED`, uma nova intenção pode ter CTA somente quando o backend continuar autorizando e confirmando elegibilidade; nunca inferir elegibilidade de `FAILED` por si.
- Preservar sempre as seções já homologadas e o shell (sidebar/topbar), Quick Detail e Histórico.

## 4. Contrato de apresentação

- Um botão apenas quando o estado real permite uma intenção de captura.
- UI não substitui autorização server-side nem Target Policy.
- `SUPPORTED` / `UNSUPPORTED` / `UNKNOWN` não são intercambiáveis.
- `AVAILABLE` significa apenas ausência de bloqueador conhecido; não atesta câmera online.
- Mensagens não revelam IP, host, credencial, URL, política de destino ou detalhes internos.
- `QUEUED` e `RUNNING`: representar job real sem criar segunda intenção indevida.
- `SUCCEEDED`: somente após resultado terminal real, não por timeout visual.
- Upload deve continuar independente de elegibilidade e permissão de captura.
- E4 `Ver imagens` permanece apenas conceito visual; ausência da ação no E3 não é falha de fidelidade.

## 5. Condição de implementação

**Não iniciar implementação produtiva da C por simples recebimento deste pacote**. O agente ARGOS deverá primeiro verificar o contrato técnico de elegibilidade vigente, mapear capacidades/estados que podem ser apresentados sem vazamento e solicitar autorização de implementação no gate devido. Se faltar dado seguro para distinguir um estado, apresentar um estado genérico aprovado ou STOP_AND_ESCALATE, conforme contrato.

## 6. Aceite no Django

Somente após implementação autorizada: renderizar o Django real com cenários autorizados, comparar 2048×742, 1440×900, 1366×768 e 390×844, e submeter ao usuário. `PROTOTYPE_APPROVED != DJANGO_APPROVED`.

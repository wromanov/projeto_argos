# ARGOS — UI-0 Read-only Preflight — Findings v1

```text
STATUS = COMPLETE / PASS_WITH_FINDINGS
DOCUMENT_TYPE = UI_DS_READ_ONLY_PREFLIGHT_FINDINGS_RECORD
ACTIVITY = UI-0 — Read-only preflight
READ_ONLY = YES
INVENTORY_PILOT_SUITABILITY = YES_WITH_FINDINGS
FINDINGS_BLOCKING_UI0_CLOSURE = NO
IMPLEMENTATION_AUTHORIZED = NO
SOURCE = findings recovery instruction supplied by the project owner for this checkpoint
DETAIL_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
```

## 1. Escopo e interpretação

Este registro preserva o resultado e os findings do preflight UI-0 concluído em
modo somente leitura. Registra as constatações recuperadas para continuidade;
não as amplia, reinterpreta como blockers ou concede autorização de
implementação.

## 2. Findings recuperados

1. O inventário atual não possui seleção nem trigger para abrir o painel.
2. A infraestrutura de imagens não existe atualmente.
3. `LATEST_CAMERA_CAPTURE = MISSING` no momento do UI-0.
4. Há conflito entre o clique atual para abrir os detalhes da câmera e o futuro
   `CameraQuickDetailPanel`.
5. É necessária uma decisão sobre o trigger acessível do painel.
6. Existe risco futuro de race condition.
7. O carregamento da imagem precisa ocorrer independentemente do restante do
   conteúdo do quick detail.
8. Não existe endpoint nem estado cliente para quick detail.
9. A navegação atual para detalhes perde o contexto e os filtros do inventário.
10. Foram identificados findings relevantes de acessibilidade.
11. UI-3 depende de IMG-01, IMG-02 e das demais dependências aplicáveis
    registradas na seção 10.1 da authority UI canônica.

Os itens acima permanecem findings não bloqueantes para o encerramento do
UI-0. A indicação de acessibilidade é preservada no nível recebido; este
registro não inventa critérios, exemplos ou severidades adicionais.

## 3. Resultado

```text
UI_0_STATUS = COMPLETE / PASS_WITH_FINDINGS
UI_0_FINDINGS_DISCOVERABLE = YES
INVENTORY_PILOT_SUITABILITY = YES_WITH_FINDINGS
FINDINGS_BLOCKING_UI0_CLOSURE = NO
UI_0_IMPLEMENTATION = NO
UI_1...UI_4 = PENDING
```

O relatório descreve o estado observado no preflight. `LATEST_CAMERA_CAPTURE =
MISSING` é uma constatação daquele momento e não altera o contrato de domínio
de imagem posteriormente canonicalizado em
`docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`.

## 4. Relação com authorities e continuidade

- `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` continua sendo a
  authority de decisões, contratos de UI-DS e dependências de UI-3.
- `docs/projeto/SPRINTS_ARGOS_V5.md` registra status, ordem e gates das slices.
- Este arquivo preserva os findings factuais do preflight UI-0.
- A próxima atividade de projeto continua IMG-02, sujeita a adjudicação humana
  e autorização explícita próprias.

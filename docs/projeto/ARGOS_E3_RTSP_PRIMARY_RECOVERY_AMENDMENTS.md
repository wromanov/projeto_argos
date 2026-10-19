# ARGOS E3 RTSP — propostas de amendment/supersession

STATUS = PROPOSED / HUMAN_ACCEPTANCE_PENDING
ACTIVITY_ID = ARGOS-E3-RTSP-DOC-01

A decisão fornecida pelo usuário nesta atividade estabelece `RTSP_FRAME` como principal e `HTTP_SNAPSHOT` como secundário. As autoridades abaixo contêm redação que precisa adjudicação explícita; preservar o histórico até essa aprovação.

| Documento vigente | Conflito localizado | Proposta condicionada à aprovação |
|---|---|---|
| `docs/projeto/contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` | BC-02 prioriza HTTP Snapshot quando não há preferência; descreve RTSP como frame validado de CAM-INT-03 | Amendment para prioridade RTSP, HTTP secundário, seleção explícita e sem fallback; exigir pipeline comum de validação/persistência/auditoria/galeria |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Contrato separa diagnóstico/conexão e não afirma captura persistente | Preservar semântica diagnóstica A–D; complementar com contrato de frame/bytes e JPEG, sem redefinir prova de conectividade como captura |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` (IMG-04/IMG-05 e limites de implementação) | Declara captura sob demanda não autorizada/não estabelecida no checkpoint vigente | Supersession apenas do método primário e do plano de captura; manter proveniência, storage privado, leitura, Quick Detail e E4 inalterados |
| Roadmap/Sprints atuais | IMG-04 não integrado e não autorizado; status de homologação anterior | Registrar nova trilha documental E3; não declarar integração, prontidão ou homologação; reservar implementação até aprovação da Rodada 1 |

O pedido da atividade registra a decisão e autoriza esta reconciliação documental. A aceitação humana deste pacote deve confirmar os amendments antes que documentos canônicos sejam promovidos. Até então, contratos atuais continuam vigentes em seus próprios termos; implementação permanece não autorizada. F02 e F03 preservam seus IDs e escopos.

```text
RTSP_PRIMARY_DECISION = RECORDED
CANONICAL_CONTRACT_SUPERSESSION = PENDING_HUMAN_ACCEPTANCE
ROUND_1_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
```

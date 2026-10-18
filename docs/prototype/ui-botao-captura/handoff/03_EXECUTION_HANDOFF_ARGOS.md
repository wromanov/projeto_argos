# Instrução de transferência para agente técnico principal ARGOS

**USER_DECISION:** aprovação visual expressa da alternativa B sem novos refinamentos.  
**RESPONSÁVEL PELA IMPLEMENTAÇÃO:** agente principal ARGOS, condicionado aos gates técnicos.  
**RESPONSÁVEL PELA CONFORMIDADE VISUAL:** consultoria UI/UX + aceite final do usuário.

## Preflight

1. Ler `AGENTS.md` e governança canônica vigente da estação; validar branch, HEAD, worktree e WIP **reais**, sem presumir versões históricas.
2. Ler `README.md`, `SHA256SUMS.txt`, protótipo congelado e o contrato visual consolidado deste pacote.
3. Verificar contratos técnicos de imagem/captura/permissão e estado da E3; não considerar contratos DRAFT automaticamente ratificados.
4. Localizar o template e CSS atual da Camera Detail e o formulário real de upload; inspecionar sem modificar áreas fora do escopo.
5. Verificar que a execução da E3 está autorizada pelo processo do projeto. Este pacote, por si, **não é autorização de implementação**.

## Escopo de materialização, quando autorizado

- Adicionar a zona de **Captura direta da câmera à direita** da zona atual de **Enviar imagem manualmente**, preservando as duas zonas no desktop e empilhando upload/captura no mobile.
- Implementar estado, feedback e CTA E3 com serviços/jobs/URLs **reais e autorizados**, sem transportar simulações temporizadas do HTML.
- Preservar integralmente upload manual atual (CSRF, permissões, validação e mensagens), demais cartões, histórico, footer, sidebar, topbar, Quick Detail e Design System canônico.
- Não implementar E4 antecipadamente: `Ver imagens` permanece **conceito visual** até a etapa própria; não gerar botão inerte ou link falso na produção E3.
- Não introduzir captura automática, fotos fictícias, acesso direto a câmera no request de renderização ou mistura com monitoramento técnico.

## QA e aceite

- Django system check; testes de permissão/CSRF/integração/status/error e regressão do upload e da Camera Detail.
- Comparar renderizações do Django real contra evidências e HTML V1: 2048×742, 1440×900, 1366×768, 390×844; conferir estados de job reais e diferenças justificadas.
- Confirmar ausência de alterações em shell, Quick Detail, consultas não relacionadas e outras páginas.
- Reportar `DJANGO_HUMAN_VISUAL_APPROVAL = PENDING` até o usuário avaliar as capturas.
- Não presumir autorização para commit, push, merge, deploy/VM/HML ou iniciar E4.

## Condições STOP

Parar e escalar se precisar alterar layout protegido, contrato de domínio, migrar schema/rodar worker fora de ambiente autorizado, usar credencial/câmera real, implantar galeria E4 antecipadamente, ou se a stack não permitir execução/testes com evidências.

## Retorno obrigatório

```text
PROJECT_ID = projeto_argos
ROADMAP_STAGE = E3
ACTIVE_SLICE = ARGOS-E3-MANUAL-IMAGE-CAPTURE
ACTIVITY = ARGOS-E3-IMAGE-OPERATIONS-VISUAL-INTEGRATION
USER_VISUAL_DECISION = APPROVED
APPROVED_VARIANT = B
VISUAL_BASELINE = V1_FROZEN
CONTRACTS_VERIFIED =
CURRENT_BRANCH =
HEAD_BEFORE =
HEAD_AFTER =
PREEXISTING_WIP_PRESERVED =
E3_TECHNICAL_AUTHORIZATION =
IMPLEMENTATION_STATUS =
UPLOAD_PRESERVED =
CAPTURE_OPERATION =
E4_GALLERY = NOT_IMPLEMENTED_IN_E3
DJANGO_SYSTEM_CHECK =
TARGETED_TESTS =
REGRESSION_TESTS =
RESPONSIVE_QA =
DESIGN_QA =
SIDEBAR_PRESERVED =
TOPBAR_PRESERVED =
QUICK_DETAIL_PRESERVED =
FILES_CHANGED =
SCREENSHOTS =
KNOWN_DIFFERENCES =
OPEN_FINDINGS =
DJANGO_HUMAN_VISUAL_APPROVAL = PENDING
COMMIT = NOT_PERFORMED_UNLESS_SEPARATELY_AUTHORIZED
PUSH = NOT_PERFORMED_UNLESS_SEPARATELY_AUTHORIZED
DEPLOY = NOT_PERFORMED_UNLESS_SEPARATELY_AUTHORIZED
NEXT_GATE = USER_DJANGO_VISUAL_REVIEW
```

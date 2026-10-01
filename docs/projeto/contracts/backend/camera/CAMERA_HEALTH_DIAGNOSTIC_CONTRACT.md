# Diagnóstico de saúde técnica da câmera

```text
STATUS = ACTIVE / DOMAIN CONTRACT
REAL_PROBE_VALIDATION = NOT_PERFORMED
```

## Semântica

Saúde técnica responde apenas à evidência produzida pelo mecanismo de probe contratado. Não equivale a situação operacional (`PRODUCAO/ESTOQUE/DESATIVADA`), qualidade de vídeo, gravação no VMS, imagem atual, gravação contínua ou integridade física completa do equipamento.

Estados estáveis: `UNKNOWN`, `ONLINE`, `OFFLINE`. `SUSPECT` é estado efêmero do reducer; freshness é qualificador separado (`FRESH/STALE`); fora de escopo e configuração incompleta são condições de elegibilidade, não estado técnico. `STALE` projeta estado efetivo desconhecido sem apagar último estado estável nem criar OFFLINE.

## Elegibilidade, confirmação e apresentação

Escopo conceitual requer câmera em produção e configuração técnica válida, autorizada e suportada. Estoque, desativada e configuração incompleta não são falha de rede. A implantação local de leitura atualmente deriva elegibilidade de `situacao_operacional == PRODUCAO` e `cadastro_completo`; perfil, capability, allowlist e credencial ainda não existem, portanto isso não habilita probes reais.

O usuário recebe estado efetivo, frescor, instante da última evidência útil, instante desde a transição estável, condição de escopo e indisponibilidade aberta. Resultado isolado de probe nunca deve promover estado. Auth/configuração/bloqueio, cancellation, inconclusivo ou evidência stale não se traduzem automaticamente em OFFLINE.

## Limites

Histórico e leitura são do domínio de monitoramento, não `EventoAuditoria` de usuário por probe. Saúde não inicia captura e imagem não confirma saúde. Fonte: ADR-020 §§3–9, 13–15; ADR-021 §§4 e 8; `MonitoringReadService`.

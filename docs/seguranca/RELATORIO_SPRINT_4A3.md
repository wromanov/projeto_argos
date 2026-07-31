# Relatório técnico — Sprint 4A.3

Data: 2026-07-31. Commit inicial: `0580945`.

## Escopo e ferramentas

Auditoria de configuração, autenticação, autorização, CSRF, métodos HTTP, escaping, redirects, Admin, dependências e CI. Ferramentas: Bandit 1.9.4, pip-audit 2.10.1, detect-secrets 1.5.0 e coverage 7.15.2.

## Achados e correções

A chave padrão gerada pelo Django estava no código de desenvolvimento; foi substituída por fallback explicitamente local e produção passou a exigir variável forte. Nenhum banco, `.env`, chave privada ou certificado estava versionado. Um `safe` desnecessário foi removido. Exclusões de Camera e AtividadeCamera foram bloqueadas no Admin. Páginas sensíveis receberam proteção contra cache e parâmetros de senha foram marcados como sensíveis.

A pesquisa cobriu padrões de segredo, execução perigosa, CSRF, escaping, SQL e exclusão. O histórico contém chave antiga de desenvolvimento, que não deve ser usada em produção. Falsos positivos da baseline foram revisados e correspondem a exemplos/fallbacks não secretos.

## Validações

Os comandos executados incluem testes, check, check --deploy, makemigrations --check, pip check, Bandit, pip-audit, detect-secrets e cobertura. Resultados finais são registrados na entrega da sprint. O pipeline não substitui revisão humana.

## Riscos residuais

Ambiente e banco de produção não definidos; HTTPS não implantado; proxy reverso não definido; firewall não validado; backup, restauração e retenção não definidos; custódia da futura chave de credenciais não definida; RTSP não implementado; teste de carga não realizado; pipeline não substitui revisão humana.

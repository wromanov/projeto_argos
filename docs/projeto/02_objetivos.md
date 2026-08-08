# 02 — Objetivos do Projeto ARGOS

## 1. Objetivo principal

Construir uma plataforma confiável para inventário, governança e monitoramento técnico de câmeras de CFTV, preservando histórico, integridade cadastral e rastreabilidade operacional.

## 2. Objetivos funcionais

### Inventário

Manter para cada câmera, conforme aplicável:

- nome;
- patrimônio;
- fabricante;
- modelo;
- tipo;
- número de série;
- MAC;
- IP;
- máscara;
- gateway;
- VLAN;
- farm;
- codec;
- retenção esperada;
- terminal;
- pavimento;
- setor;
- ambiente;
- descrição detalhada;
- ponto de referência;
- observações.

### Governança

Controlar separadamente:

- situação operacional;
- status técnico;
- completude cadastral;
- desativação;
- reativação;
- substituição;
- histórico de alterações;
- auditoria.

### Monitoramento

Evoluir o sistema para:

- testar disponibilidade;
- atualizar Online/Offline;
- registrar início e fim das indisponibilidades;
- testar conexão RTSP;
- capturar snapshots;
- controlar falhas consecutivas.

### Auditoria

Registrar alterações importantes de forma rastreável.

A auditoria deve responder:

- o que mudou;
- quando mudou;
- quem alterou;
- qual entidade foi afetada;
- qual era o valor anterior;
- qual passou a ser o novo valor.

## 3. Objetivos de UX/UI

O ARGOS deve priorizar operação e legibilidade.

A interface deve:

- facilitar leitura rápida;
- apresentar hierarquia visual clara;
- destacar situações de risco;
- reduzir ruído visual;
- funcionar em notebooks;
- manter responsividade em tablet e celular;
- usar cores com significado;
- evitar telas excessivamente densas ou decorativas.

## 4. Objetivos de segurança

- Restringir funções por permissões.
- Não expor credenciais ao perfil Monitoramento.
- Não armazenar senhas sensíveis em texto aberto.
- Não registrar segredos em logs.
- Manter chaves criptográficas fora do banco.
- Impedir exclusão física normal de entidades operacionais principais.
- Preservar histórico e auditoria.

## 5. Objetivos de confiabilidade

- Testes automatizados antes de cada entrega.
- Mudanças incrementais.
- Gate técnico antes de commit.
- Revisão do diff.
- Ausência de alterações não relacionadas no mesmo commit.
- Não promover funcionalidade sem evidência.

## 6. Objetivos de escala

O sistema deve ser preparado para aproximadamente:

**2.300 câmeras.**

O monitoramento deverá ser implantado progressivamente:

- 50 câmeras;
- 100 câmeras;
- 500 câmeras;
- parque completo.

## 7. Objetivos de produção

Antes da entrada definitiva em produção:

- PostgreSQL;
- configuração por variáveis de ambiente;
- servidor de aplicação apropriado;
- estáticos corretamente publicados;
- backup;
- restauração testada;
- observabilidade;
- logs estruturados;
- plano de rollback;
- testes de carga;
- revisão de segurança.

---

**Os objetivos acima devem orientar decisões técnicas e impedir mudanças que desviem o ARGOS de sua finalidade operacional.**

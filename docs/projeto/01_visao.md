# 01 — Visão do Projeto ARGOS

## 1. Visão geral

O **ARGOS** é um sistema corporativo de inventário, governança e monitoramento de câmeras de CFTV, projetado para administrar um parque de aproximadamente **2.300 câmeras** em ambiente operacional crítico.

O sistema não deve ser tratado apenas como um cadastro de equipamentos. Sua função é manter uma visão confiável do ciclo de vida de cada câmera, de sua situação operacional, de seu estado técnico e de seu histórico.

O ARGOS deve permitir responder rapidamente perguntas como:

- Qual câmera está instalada em determinado local?
- Qual é o IP, VLAN, fabricante e modelo?
- A câmera está em Produção, Estoque ou Desativada?
- O equipamento está Online, Offline ou ainda não foi verificado?
- Qual foi a última atividade registrada?
- Houve substituição?
- Quando ficou indisponível?
- Quem alterou determinado dado?
- O cadastro está completo?
- Quais informações ainda faltam?
- Quais credenciais e parâmetros técnicos devem ser usados para monitoramento?
- Qual é a imagem recente do ponto monitorado?

## 2. Problema que o ARGOS resolve

Em parques grandes de CFTV, a simples existência de uma câmera no VMS não garante rastreabilidade operacional.

Quando uma câmera falha, é substituída ou fica indisponível por período superior à retenção do vídeo, pode ser difícil recuperar:

- referência visual do ponto;
- equipamento anteriormente instalado;
- local exato;
- patrimônio;
- endereço IP;
- configuração de rede;
- situação operacional;
- histórico de falhas;
- responsáveis por alterações.

O ARGOS centraliza essas informações e cria uma camada de governança independente do VMS.

## 3. Público do sistema

### Monitoramento

Perfil de consulta operacional.

Pode visualizar informações necessárias para acompanhamento do parque, mas não deve acessar dados sensíveis ou administrativos.

### Operador

Responsável por manutenção lógica e atualização operacional dos registros.

Pode cadastrar, editar, classificar, desativar, reativar, registrar atividades e substituições conforme permissões.

### Administrador

Responsável pela administração global do sistema.

Além das atribuições operacionais, pode administrar usuários, grupos, permissões e configurações globais.

## 4. Princípios centrais da visão

O ARGOS deve ser:

- auditável;
- rastreável;
- seguro;
- orientado à operação;
- responsivo;
- simples de consultar;
- rigoroso com integridade de dados;
- evolutivo;
- independente de um único fabricante de câmera;
- capaz de crescer até o parque completo.

## 5. Estado atual

O sistema já possui:

- cadastro e edição de câmeras;
- status técnico;
- situação operacional;
- atividades;
- auditoria;
- eventos;
- substituições;
- desativação e reativação;
- histórico de indisponibilidade;
- perfis e permissões;
- dashboard;
- testes automatizados;
- CI;
- redesign visual de shell, listagem, dashboard e detalhe da câmera.

A etapa visual atual é:

**Visual 4B — Cadastro e edição de câmera.**

## 6. Direção futura

As próximas capacidades funcionais principais são:

1. credenciais seguras de monitoramento;
2. integração RTSP;
3. keepalive de aproximadamente 2.300 câmeras;
4. snapshots automáticos e manuais;
5. importação em lote;
6. preparação para produção, backup e observabilidade.

---

**Documento de referência arquitetural do Projeto ARGOS.**

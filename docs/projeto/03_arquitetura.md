# 03 — Arquitetura do Projeto ARGOS

## 1. Visão arquitetural

O ARGOS é atualmente uma aplicação web monolítica modular construída com Django.

Arquitetura conceitual:

```text
Usuário
  |
  v
Interface Web
Django Templates + CSS
  |
  v
Views / Forms
  |
  v
Serviços de domínio / Governança / Auditoria
  |
  v
Models Django
  |
  v
Banco de dados
```

As futuras funções de monitoramento acrescentarão uma camada assíncrona:

```text
Scheduler
  |
  v
Workers / tarefas
  |
  +--> RTSP / câmera
  |
  +--> atualização de status
  |
  +--> indisponibilidades
  |
  +--> snapshots
  |
  +--> logs / observabilidade
```

## 2. Stack atual

- Python 3.14.6
- Django 5.2.16
- Django Templates
- CSS próprio
- PowerShell no ambiente local
- PyCharm
- Git
- testes Django
- CI

Configuração:

```text
LANGUAGE_CODE = pt-br
TIME_ZONE = America/Sao_Paulo
USE_TZ = True
```

## 3. Aplicações Django

### cameras

Responsável pelo domínio principal:

- câmeras;
- atividades;
- auditoria;
- eventos;
- situação operacional;
- indisponibilidades;
- substituições;
- governança.

### usuarios

Responsável por:

- autenticação;
- perfil;
- grupos;
- permissões;
- administração relacionada a usuários.

### core

Responsável por:

- dashboard;
- shell;
- componentes globais;
- infraestrutura de interface compartilhada.

## 4. Camadas

### Templates

Responsáveis pela apresentação.

Não devem conter regra de negócio complexa.

### Forms

Responsáveis por:

- entrada de dados;
- validação;
- normalização;
- integração com modelos.

### Views

Responsáveis por:

- autenticação e autorização;
- coordenação da requisição;
- seleção de forms;
- mensagens;
- redirecionamentos;
- carregamento do contexto.

### Governança

Regras de mudança de estado devem ficar centralizadas em serviços/funções de domínio e não espalhadas em templates.

### Auditoria

Alterações relevantes devem gerar eventos auditáveis.

## 5. Arquitetura front-end

Não utiliza Bootstrap ou Tailwind.

Arquivos principais:

```text
static/css/argos.css
static/css/design-system.css
static/css/inventario.css
static/css/governanca.css
```

Estrutura compartilhada:

```text
templates/base.html
templates/components/
```

O design system é baseado em:

- tokens;
- spacing consistente;
- cores semânticas;
- componentes reaproveitáveis;
- responsividade.

## 6. Banco de dados

No ambiente futuro de produção, a direção oficial é:

**PostgreSQL.**

Regras importantes:

- dados de auditoria devem ser preservados;
- segredos não devem ser armazenados sem proteção;
- alterações de situação não podem apagar histórico;
- operações críticas devem preferir transações.

## 7. Arquitetura futura de monitoramento

Separar conceitualmente:

1. configuração;
2. credenciais;
3. composição da URL;
4. teste de conexão;
5. consumo do stream;
6. keepalive;
7. transição de status;
8. indisponibilidade;
9. snapshot;
10. observabilidade.

Não acoplar tudo em uma única função.

## 8. Escalabilidade

O parque alvo possui aproximadamente 2.300 câmeras.

As tarefas de monitoramento devem:

- limitar concorrência;
- possuir timeout;
- possuir tentativas controladas;
- evitar execução duplicada;
- registrar duração da rodada;
- não travar a aplicação web;
- permitir evolução para worker dedicado.

## 9. Segurança

Credenciais de câmera devem:

- ser criptografadas;
- ser restritas por permissão;
- nunca aparecer em logs;
- nunca aparecer em mensagens de erro;
- nunca ser incorporadas diretamente em HTML;
- ter chave criptográfica fora do banco.

---

**A arquitetura deve permanecer modular o suficiente para separar operação web, governança e monitoramento assíncrono.**

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

Como evolução prevista, as funções operacionais acrescentarão processamento independente da aplicação web:

```text
ARGOS WEB
  |
  +--> consulta o estado persistido pelo ARGOS
                         ^
                         |
              worker futuro de monitoramento
                         |
                    parque de câmeras

Processamento futuro de captura
  |
  +--> captura sob demanda ou importação manual
  +--> gestão de evidências visuais
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

### Contrato global de filtros

O Sistema Global de Filtros é uma camada de consulta e UX server-rendered. Filtros categóricos aceitam parâmetros GET repetidos, por exemplo `?tipo=DOME&tipo=BULLET`, lidos no backend com `request.GET.getlist(...)`. A semântica é OR entre valores da mesma faceta e AND entre facetas diferentes; URLs antigas de valor único permanecem compatíveis.

A multiseleção não usa `<select multiple>` nativo: utiliza uma interface compacta com `<details>`, `<summary>` e checkboxes. O botão **Filtrar** envia a consulta. O servidor é a fonte da verdade; JavaScript somente melhora a interação, sem dependência funcional de `fetch`, SPA ou requisições automáticas por checkbox.

Filtros aplicados são exibidos como chips server-rendered e removíveis individualmente. Sua remoção elimina também `page`; há uma única ação global **Limpar todos**. A paginação compartilhada em `templates/components/paginacao.html` preserva filtros válidos e é usada também por Eventos; o partial local antigo de Eventos foi removido.

As views expõem em `query_params` a representação canônica dos filtros aceitos. As tags `querystring()` e `querystring_sem_valor()` a priorizam, com fallback para `request.GET` quando ela não existe. A canonicalização descarta enums inválidos, parâmetros desconhecidos e valores vazios; deduplica e normaliza valores efetivos; preserva parâmetros repetidos válidos; e controla `page` separadamente, com exatamente um `page` nos links de paginação.

Datas inválidas ou um período com **De > Até** são um estado visível e corrigível: não filtram o queryset, definem `periodo_invalido=True`, permanecem visíveis, são exibidas nos chips e podem ser removidas. Diferentemente, enums inválidos são ruído e não pertencem à query canônica.

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

## 7. Arquitetura planejada de monitoramento e imagens

O monitoramento de disponibilidade será responsabilidade de worker(s) ou processo(s) futuros, independentes do ciclo HTTP do Django e do navegador. A aplicação web consultará o estado conhecido pelo ARGOS; ela não realizará probes diretamente no parque de câmeras.

O monitoramento deverá persistir principalmente estado e transições relevantes, como `ONLINE -> OFFLINE` e `OFFLINE -> ONLINE`; probes normais repetidos não devem gerar novo histórico por si só. Mecanismo anti-flapping, parâmetros configuráveis e testes de carga são requisitos futuros de discovery, não escolhas já implementadas.

O processamento de captura de imagem é uma responsabilidade independente: captura lenta ou falha não poderá bloquear nem degradar o monitoramento. A captura ocorrerá sob demanda e poderá ser complementada por importação manual; proveniência deverá distinguir captura da câmera e upload manual.

Esta arquitetura planejada não define tecnologia de fila/worker, scheduler, protocolo de probe, limites de concorrência, timeouts, política de retry nem mecanismo de atualização da interface. Essas decisões serão feitas em `MON-01` e nas fases de imagens do Roadmap v5.

## 8. Escalabilidade

O parque alvo possui aproximadamente 2.300 câmeras.

O futuro monitoramento deverá:

- limitar concorrência;
- ter parâmetros de timeout e tentativas configuráveis;
- evitar execução duplicada;
- registrar métricas operacionais relevantes;
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

**A arquitetura deve permanecer modular o suficiente para separar operação web, governança, monitoramento de disponibilidade e processamento de imagens.**

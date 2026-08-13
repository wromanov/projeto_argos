# HANDOFF DE CONTINUIDADE — PROJETO ARGOS

> **Atualização de continuidade — 13/08/2026.** Esta seção prevalece sobre
> snapshots históricos abaixo quando houver divergência de branch, HEAD,
> MON-04, segurança ou próxima atividade.

## Baseline técnico atual de referência

- Data de referência: **13/08/2026**
- Branch: `master`
- Último commit técnico publicado de referência: `9cf1964` — `test(monitoramento): validar laboratorio de confirmacao`
- Origin: `master` sincronizada com `origin/master`
- Suíte canônica: `569` testes PASS local; não afirmar CI remoto
- Última entrega: MON-04C concluída e publicada
- Próxima atividade documental: MON-04D — fechamento documental
- Commits de evidência: `26a8925` e `9cf1964`

## Estado de segurança e produção

Existe auditoria independente em `docs/security_audit/auditoria_segurança_001.md`.
SEC-007 foi confirmado como vulnerabilidade **High**, confiança alta,
prioridade **P0**, envolvendo escalada vertical via Django Admin.

**SECURITY GATE: BLOCKED para produção.** Homologação, promoção e exposição
em produção estão proibidas até SEC-007 ser corrigido e revalidado. O
desenvolvimento local, testes e fechamento documental de MON-04 podem continuar.

Frente corretiva obrigatória: **SEC-R01 / SEC-007**. Ela deverá eliminar a
escalada confirmada e incluir teste de regressão; depois, o Agente de Segurança
deverá executar VERIFY. A solução não está definida neste handoff.

MON-04D permanece válida e não é cancelada. MON-05 — scheduler + concorrência
permanece planejada, mas não autorizada enquanto o gate estiver BLOCKED.

SEC-001 a SEC-006 permanecem findings existentes, tratados por prioridade; não
foram declarados corrigidos e não são todos blockers imediatos. SEC-007 é o
único finding atualmente responsável pelo Security Gate BLOCKED.

## Governança de segurança

GOV-SEC-01: contrato de inicialização de produção + backend de banco ainda
precisa ser definido. GOV-SEC-02: read-only da identidade Visual QA não deve
depender exclusivamente de middleware/flag. GOV-SEC-03: política de brute
force/throttling ainda precisa ser definida. GOV-SEC-04: limites de conteúdo e
atomicidade da auditoria ainda precisam de decisão.

O Agente ARGOS cuida de arquitetura, continuidade e governança técnica; o
Agente de Segurança conduz auditoria, findings e VERIFY; o responsável humano
tem a decisão final. Findings não autorizam alterações automáticas.

**Projeto:** ARGOS — Sistema de Inventário e Monitoramento de Câmeras  
**Atualizado em:** 13/08/2026
**Finalidade:** permitir que outro agente continue o projeto em uma nova conversa sem perder decisões técnicas, estado do código, governança, UX/UI ou histórico recente.

---

## 1. PAPEL DO AGENTE QUE ASSUMIR

Assuma o papel de **Agente ARGOS**, responsável por continuidade técnica, arquitetura, governança, consistência visual e preservação das decisões oficiais.

Princípios de trabalho:

- preservar contratos existentes;
- exigir evidência antes de mudar comportamento;
- trabalhar incrementalmente;
- evitar refatorações amplas sem justificativa;
- manter permissões e regras de negócio;
- preservar auditoria;
- validar antes de commit;
- não fazer push automaticamente.

O usuário executa os comandos localmente em Windows/PowerShell. O agente deve fornecer patches pequenos, verificáveis e com gate técnico claro.

---

## 2. REPOSITÓRIO E AMBIENTE

Repositório local:

```text
C:\Users\walac\PycharmProjects\projeto_argos
```

Ambiente:

- Windows 11;
- PowerShell;
- PyCharm;
- Python 3.14.6;
- Django 5.2.16;
- `.venv`;
- idioma `pt-br`;
- timezone `America/Sao_Paulo`;
- `USE_TZ=True`.

Branch:

```text
master
```

Estado no momento deste handoff:

```text
master...origin/master [ahead 1]
working tree limpa
```

Último commit:

```text
6751c68 feat(frontend): redesenhar detalhe operacional da câmera
```

Esse commit ainda não foi enviado para `origin`.

---

## 3. STACK FRONT-END

O ARGOS usa:

- Django Templates;
- CSS próprio;
- design system próprio;
- sem Bootstrap;
- sem Tailwind;
- JavaScript próprio mínimo ou inexistente nas telas atuais.

CSS relevante:

```text
static/css/argos.css
static/css/design-system.css
static/css/inventario.css
static/css/governanca.css
```

`inventario.css` ainda contém legado. A limpeza global fica para a consolidação final; não misturar essa limpeza com uma etapa visual específica.

---

## 4. APLICAÇÕES DJANGO

Apps principais:

```text
cameras
core
usuarios
```

Projeto Django:

```text
config
```

Migrations conhecidas:

```text
cameras: 0001 até 0008
usuarios: 0001 até 0002
```

---

## 5. GOVERNANÇA E REGRAS OFICIAIS

### 5.1 Sem exclusão física operacional normal

Entidades principais não devem ser apagadas fisicamente no fluxo normal. Preferir:

- desativação;
- histórico;
- auditoria;
- transições de situação.

### 5.2 Situação operacional != status técnico

Situação operacional:

```text
Produção
Estoque
Desativada
```

Status técnico:

```text
Online
Offline
Não verificado
```

Esses conceitos não devem ser fundidos no back-end nem na interface.

### 5.3 Auditoria

A auditoria é tratada como histórico imutável. Alterações relevantes precisam ser registradas.

### 5.4 Perfis

**Monitoramento:** consulta inventário/dashboard/status/históricos permitidos; não acessa credenciais, RTSP sensível, alterações ou administração.

**Operador:** cria/edita câmeras, classifica, desativa/reativa conforme permissões, registra atividades e substituições; futuramente poderá operar credenciais/RTSP conforme desenho de segurança.

**Administrador:** Operador + usuários, grupos, administração, configurações globais e segurança.

---

## 6. FUNCIONALIDADES IMPLEMENTADAS

Principais:

- cadastro e edição de câmeras;
- fabricante, modelo, tipo, patrimônio e dados técnicos;
- status técnico;
- situação operacional;
- Produção, Estoque e Desativada;
- desativação e reativação;
- substituição;
- atividades;
- histórico de indisponibilidade;
- auditoria;
- eventos;
- autenticação;
- perfil;
- permissões;
- dashboard;
- regras de integridade cadastral;
- rotas protegidas;
- testes e CI.

---

## 7. ROADMAP FUNCIONAL FUTURO

Blocos oficiais:

```text
4D — Credenciais e configuração de monitoramento
4E — Integração RTSP
4F — Keepalive e monitoramento de disponibilidade
4G — Snapshots
4H — Importação em lote
4I — Produção, backup e observabilidade
```

### Credenciais

Regras obrigatórias:

- senha nunca em texto aberto;
- criptografia;
- chave fora do banco;
- senha nunca em log/template/mensagem;
- acesso restrito;
- auditoria;
- testes de segurança.

### Keepalive

Parâmetros iniciais:

```text
Execuções: 08:00 e 18:00
Concorrência: 20
Tentativas: 2
Timeout: 5 segundos
```

Escalonamento:

```text
50
100
500
parque completo (~2.300 câmeras)
```

### Snapshots

Automático somente em:

```text
Offline -> Online
primeira detecção Online
primeiro cadastro detectado Online
```

Não capturar ao entrar Offline.

Retenção:

```text
3 imagens automáticas mais recentes por câmera
```

Imagem manual protegida não entra na rotação automática.

---

## 8. IDENTIDADE VISUAL ATUAL

Paleta consolidada:

```text
Primary:            #185A85
Primary hover:      #124766
Accent:             #2F80ED
Sidebar:            #0B1F33
Sidebar surface:    #132B43
Sidebar text:       #E8F0F7
Sidebar muted:      #9FB2C4
Topbar:             #FFFFFF
App background:     #F3F6FA
Surface:            #FFFFFF
Subtle surface:     #F7F9FC
Border:             #D7E0E8
Text:               #172534
Secondary text:     #5E6D7A
Online:             #167D5A / #E8F6F0
Offline:            #C23B32 / #FDECEA
Produção:           #245FAF / #EAF2FF
Estoque:            #946200 / #FFF4D6
Desativada:         #5F6B76 / #EEF1F4
```

Spacing:

```text
4 / 8 / 12 / 16 / 20 / 24 / 32 / 40
```

Controles:

```text
~40–42px
```

Shell:

```text
sidebar expandida: ~248px
sidebar recolhida: ~72px
topbar: ~56px
```

Cor deve comunicar significado: verde positivo, vermelho falha/destrutivo, ocre atenção, azul domínio técnico/institucional, cinza-azulado contexto neutro.

---

## 9. COMMITS VISUAIS IMPORTANTES

Fundação:

```text
3d67c2e refactor(frontend): consolidar tokens do design system
2c8a57c refactor(frontend): extrair componentes globais do template base
15ea34c feat(frontend): modernizar estrutura global do ARGOS
```

Shell:

```text
5100448 feat(frontend): implementar novo shell operacional do ARGOS
```

Listagem:

```text
51d8250 feat(frontend): redesenhar listagem responsiva de câmeras
22be61b feat(frontend): aprimorar resultados e consolidar paginação
```

Dashboard:

```text
5548bd3 feat(frontend): aprimorar hierarquia operacional do dashboard
```

Detalhe:

```text
6751c68 feat(frontend): redesenhar detalhe operacional da câmera
```

---

## 10. VISUAL 4A — CONCLUÍDA

Arquivos principais:

```text
cameras/templates/cameras/detalhe.html
static/css/inventario.css
```

### 4A.1

- cabeçalho operacional;
- retorno ao inventário;
- identidade da câmera;
- badges;
- resumo de patrimônio, IP e localização.

### 4A.2

- cards técnicos compactos;
- fonte monoespaçada em dados técnicos;
- valores vazios atenuados;
- identidade visual por domínio;
- monitoramento com cor dinâmica.

### 4A.3

- governança;
- campos faltantes;
- ordem das ações;
- históricos;
- estados vazios;
- responsividade.

Resultado visual aprovado pelo usuário.

Gate direcionado:

```text
72 testes aprovados
```

Suíte completa reportada antes do commit:

```text
324 testes aprovados
```

---

## 11. ETAPA ATUAL — VISUAL 4B

**Visual 4B — Cadastro e edição de câmera**

Nenhuma alteração de código dessa etapa havia sido feita no momento deste handoff.

Template:

```text
cameras/templates/cameras/formulario.html
```

Views em `cameras/views.py`:

```python
criar_camera
editar_camera
```

Forms em `cameras/forms.py`:

```python
CameraBaseForm
CameraCriacaoForm
CameraEdicaoForm
```

Comportamento confirmado:

- criação e edição reutilizam o mesmo template;
- criação inclui `situacao_operacional`;
- edição comum não altera situação operacional;
- mudança de situação continua nos fluxos de governança.

Problema visual atual:

- fieldset de Situação inicial;
- fieldset único "Dados da câmera";
- loop genérico `{% for field in form %}`;
- grid genérico de duas colunas;
- somente `descricao_detalhada` e `observacoes` em largura completa;
- identificação, localização, rede, gravação, origem e observações misturadas.

CSS legado relevante em `static/css/inventario.css`:

```text
.field
.field__label
.form-section
.form-grid
.form-field--wide
.form-actions
.field-errors
.form-errors
```

O design system também possui:

```text
.form-container
.form-section
.form-section__header
.form-grid
.form-field
.form-label
.form-help
.form-error
.form-errors-summary
.form-actions
.required-marker
```

Existe sobreposição conceitual. Não consolidar globalmente agora.

---

## 12. PLANO OFICIAL DA VISUAL 4B

### 4B.1 — Shell e cabeçalho

- link de retorno;
- título e descrição;
- contexto da câmera em edição;
- situação operacional mostrada como contexto;
- painel com largura consistente;
- ações Salvar/Cancelar mais claras.

### 4B.2 — Seções técnicas

Substituir o loop genérico por agrupamento explícito:

```text
Identificação
Localização
Rede
Gravação
Cadastro/origem
Observações
```

Preservar os mesmos `form.<campo>`.

### 4B.3 — Validação e responsividade

- obrigatório;
- help text;
- erro junto ao campo;
- resumo de erros;
- focus;
- invalid;
- disabled;
- uma coluna no mobile;
- ações responsivas.

---

## 13. PRÓXIMO PASSO EXATO

Antes de qualquer patch da Visual 4B:

1. usar/solicitar captura em tela larga de **Nova câmera**;
2. usar/solicitar captura em tela larga de **Editar câmera**;
3. comparar o estado visual atual;
4. definir o patch mínimo da 4B.1.

Escopo esperado inicialmente:

```text
cameras/templates/cameras/formulario.html
static/css/inventario.css
```

Não alterar:

```text
cameras/views.py
cameras/forms.py
```

sem necessidade funcional comprovada.

---

## 14. POLÍTICA DE IMPLEMENTAÇÃO

Fluxo:

1. diagnosticar;
2. explicar objetivo/causa;
3. alterar poucos arquivos;
4. validar template;
5. rodar `manage.py check`;
6. testes direcionados;
7. validação visual do usuário;
8. avançar microetapa;
9. suíte completa antes do commit;
10. `git diff --check`;
11. conferir staged;
12. commit;
13. sem push automático.

Comandos usuais:

```powershell
python manage.py check
python manage.py test -v 1
git diff --check
git status --short --branch
git diff --stat
git diff --name-status
```

Antes do commit:

```powershell
git diff --cached --check
git diff --cached --name-status
git diff --cached --stat
```

Avisos `LF will be replaced by CRLF` são informativos no ambiente Windows.

---

## 15. REGRAS PARA SCRIPTS POWERSHELL/PYTHON

O usuário executa patches no PowerShell. Preferir:

- scripts Python embutidos somente com caracteres ASCII quando possível;
- escapes Unicode para acentos;
- `python -X utf8` quando apropriado;
- validar número de ocorrências antes de substituir;
- gravar somente depois de todas as validações internas;
- evitar alteração parcial em caso de erro.

Padrão seguro:

```python
if content.count(old) != 1:
    raise RuntimeError(...)
```

Somente depois:

```python
path.write_bytes(...)
```

---

## 16. O QUE NÃO FAZER NA RETOMADA

Não:

- recomeçar o redesign;
- trocar o framework CSS;
- introduzir Bootstrap/Tailwind;
- alterar permissões sem evidência;
- fundir status técnico com situação operacional;
- remover auditoria;
- implementar exclusão física normal;
- reorganizar testes durante uma etapa visual;
- limpar todo o CSS legado junto com o formulário;
- fazer push sem autorização;
- criar commit antes da aprovação visual.

---

## 17. DOCUMENTO DE ROADMAP ASSOCIADO

Usar junto com este handoff:

```text
roadmap_projeto_argos_v3.txt
```

---

## 18. PROMPT PARA UMA NOVA CONVERSA

> Você será o Agente ARGOS e continuará o desenvolvimento do Projeto ARGOS a partir dos documentos anexados. Trate o handoff e o roadmap como estado oficial do projeto. Preserve arquitetura, governança, permissões, decisões de UX e histórico de commits. Trabalhe incrementalmente e exija validação antes de promover mudanças. A etapa atual é a Visual 4B — Cadastro e edição de câmera. Antes de alterar código, confirme o estado Git e retome exatamente do próximo passo descrito no handoff.

---

## 19. CHECKLIST DE RETOMADA

- [ ] Ler este handoff.
- [ ] Ler o roadmap V3.
- [ ] Confirmar branch e `git status`.
- [ ] Confirmar último commit.
- [ ] Não assumir que houve push.
- [ ] Confirmar mudanças locais posteriores ao handoff.
- [ ] Verificar se as capturas da Visual 4B já foram fornecidas.
- [ ] Retomar pela 4B.1.
- [ ] Preservar escopo incremental.
- [ ] Rodar gates antes de commit.

---

**Fim do handoff.**

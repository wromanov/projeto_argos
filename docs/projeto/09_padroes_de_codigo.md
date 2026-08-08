# 09 — Padrões de Código do Projeto ARGOS

## 1. Python

Seguir estilo legível e explícito.

Preferir:

```python
def funcao():
    ...
```

Evitar excesso de lógica em uma única linha.

Código legado com múltiplas instruções separadas por `;` pode ser refatorado em etapa apropriada, sem misturar com alterações funcionais ou visuais.

## 2. Nomes

Usar nomes em português quando já fizerem parte do domínio.

Exemplos:

```python
situacao_operacional
ultima_verificacao
retencao_esperada_dias
descricao_detalhada
```

Não misturar sinônimos sem necessidade.

## 3. Views

Uma view deve:

- validar permissão;
- carregar entidades;
- instanciar form;
- coordenar operação;
- registrar mensagem;
- redirecionar.

Regra de negócio complexa deve migrar para serviço de domínio.

## 4. Forms

Forms devem:

- validar entrada;
- normalizar;
- fornecer widgets;
- impedir dados inválidos.

Não usar template para validar regra de negócio.

## 5. Models

Models devem representar o domínio.

Evitar campos duplicados apenas para facilitar UI.

## 6. Serviços de governança

Transições importantes devem permanecer centralizadas.

Exemplos:

```text
desativar_camera
reativar_camera
alterar_situacao_camera
substituir_camera
```

## 7. Auditoria

Toda mudança auditável deve registrar:

- entidade;
- usuário;
- origem;
- resumo;
- alterações.

## 8. Templates

Templates devem priorizar:

- semântica;
- acessibilidade;
- clareza;
- componentes.

Evitar templates inteiros comprimidos em uma única linha.

Para novos trabalhos, preferir formatação legível.

## 9. CSS

Prioridades:

1. reutilizar design system;
2. reutilizar componente existente;
3. criar modificador específico;
4. somente depois criar novo padrão.

Evitar:

- duplicação de seletor;
- valores literais repetidos;
- `!important` sem necessidade;
- seletor excessivamente específico;
- efeitos visuais sem função.

## 10. Tokens

Usar tokens para:

- cores;
- spacing;
- radius;
- shadow;
- tipografia;
- dimensões de controle.

## 11. Componentes CSS

Preferir nomes claros:

```text
camera-detail-hero
detail-history-card
inventory-filter-form
form-section
```

Modificadores:

```text
--warning
--offline
--compact
```

## 12. Responsividade

Breakpoints devem possuir justificativa visual.

Evitar criar breakpoint por componente sem necessidade.

Testar pelo menos:

- desktop largo;
- notebook;
- tablet;
- celular.

## 13. Acessibilidade

Sempre que aplicável:

- `aria-label`;
- labels associados;
- foco visível;
- botões com texto claro;
- não depender apenas de cor;
- ordem de tabulação natural.

## 14. Segurança

Nunca escrever no código:

```text
senha real
token real
chave privada
segredo de produção
```

Usar variáveis de ambiente.

## 15. Integrações

Toda chamada externa deve possuir:

- timeout;
- tratamento de erro;
- log seguro;
- retry controlado quando necessário.

## 16. Testes

Durante o desenvolvimento:

```powershell
python manage.py test <escopo> -v 1
```

Antes do commit:

```powershell
python manage.py test -v 1
```

## 17. Git

Antes de stage:

```powershell
git diff --check
git status --short
git diff --stat
```

Stage explícito:

```powershell
git add -- "arquivo1" "arquivo2"
```

Antes do commit:

```powershell
git diff --cached --check
git diff --cached --name-status
git diff --cached --stat
```

## 18. Commits

Padrão preferido:

```text
feat(frontend): ...
feat(cameras): ...
fix(frontend): ...
fix(cameras): ...
refactor(frontend): ...
test(...): ...
docs(...): ...
```

A mensagem deve descrever a entrega real.

## 19. PowerShell + scripts Python

Para patches automatizados:

- preferir script ASCII;
- usar `-X utf8`;
- validar ocorrência;
- não gravar antes de validar;
- falhar explicitamente.

## 20. Migrações

Criar migration somente quando houver mudança real de schema.

Nunca editar migration histórica já aplicada sem motivo excepcional.

## 21. Alterações de escopo

Se uma tarefa visual exigir mudança de back-end, interromper e justificar antes.

Não ampliar escopo silenciosamente.

## 22. Definition of Done

Uma mudança está pronta quando:

- comportamento preservado ou validado;
- template compila;
- `manage.py check` passa;
- testes direcionados passam;
- validação visual passa quando aplicável;
- suíte completa passa antes do commit;
- `git diff --check` passa;
- staged files são exatamente os esperados;
- commit representa uma única intenção.

---

**Este documento define padrões operacionais de código para manutenção consistente do ARGOS.**

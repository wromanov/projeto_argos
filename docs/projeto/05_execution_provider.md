# 05 — Execution Provider do Projeto ARGOS

## 1. Definição

No contexto do ARGOS, o **Execution Provider** define como as mudanças propostas pelo agente são executadas, verificadas e promovidas no repositório.

O agente não executa diretamente no computador do usuário.

O fluxo oficial é:

```text
Agente propõe
    |
    v
Usuário executa localmente
    |
    v
Usuário retorna evidências
    |
    v
Agente analisa
    |
    v
Próxima microetapa
```

## 2. Ambiente de execução

```text
Sistema: Windows 11
Shell: PowerShell
IDE: PyCharm
Python: 3.14.6
Venv: .venv
Framework: Django 5.2.16
```

Repositório:

```text
C:\Users\walac\desenvolvimento\projeto_argos
```

Branch principal de trabalho:

```text
master
```

## 3. Regra de execução incremental

Cada mudança deve seguir:

1. diagnóstico;
2. patch mínimo;
3. execução local;
4. validação;
5. inspeção visual quando aplicável;
6. testes direcionados;
7. suíte completa;
8. revisão do diff;
9. stage explícito;
10. commit;
11. push somente quando solicitado.

## 4. Gates obrigatórios

### Template

Quando houver alteração de template:

```powershell
python manage.py shell -c "from django.template.loader import get_template; get_template('cameras/detalhe.html'); print('Template compilado.')"
```

Adaptar o caminho conforme a tela.

### Django

```powershell
python manage.py check
```

### Testes

Direcionados durante a implementação:

```powershell
python manage.py test <modulos> -v 1
```

Antes do commit:

```powershell
python manage.py test -v 1
```

### Git

```powershell
git diff --check
git status --short --branch
git diff --name-status
git diff --stat
```

Antes do commit:

```powershell
git diff --cached --check
git diff --cached --name-status
git diff --cached --stat
```

## 5. Política de stage

Nunca executar:

```text
git add .
```

por conveniência em uma mudança controlada.

Preferir adicionar apenas os arquivos esperados:

```powershell
git add -- "arquivo1" "arquivo2"
```

## 6. Política de commit

Um commit deve representar uma entrega coerente.

Evitar misturar:

- redesign;
- reorganização de testes;
- mudança de regra de negócio;
- limpeza de CSS;
- migração;
- alteração de infraestrutura.

## 7. Política de push

O agente não deve assumir autorização para push.

Após o commit:

```powershell
git status --short --branch
git log -1 --oneline --decorate
```

O push só ocorre quando o usuário solicitar.

## 8. Scripts Python dentro do PowerShell

Quando o agente fornecer scripts embutidos:

- preferir ASCII;
- usar escapes Unicode para textos acentuados;
- usar `python -X utf8`;
- validar quantidade de ocorrências;
- gravar somente ao final;
- não deixar arquivos parcialmente alterados em caso de erro.

Padrão:

```python
if content.count(old) != 1:
    raise RuntimeError(...)
```

Somente depois:

```python
path.write_bytes(...)
```

## 9. Evidência antes de promoção

Nenhuma estratégia deve ser considerada concluída apenas porque o código parece correto.

Para promover uma mudança:

- evidência do comando;
- testes;
- screenshot quando visual;
- diff limpo;
- escopo confirmado.

## 10. Estado Git de referência

Na geração deste documento:

```text
master...origin/master [ahead 1]
```

Último commit:

```text
6751c68 feat(frontend): redesenhar detalhe operacional da câmera
```

Push ainda não confirmado.

---

**Este documento define o contrato operacional entre agente e usuário durante o desenvolvimento do ARGOS.**

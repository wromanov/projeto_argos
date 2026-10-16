# HOM-02 — Proposta de preparação para importação XLSX

**Data:** 2026-10-14
**Projeto:** projeto_argos
**Branch / HEAD de referência:** `codex/hom-v1-integration` / `97c7d47c4c47761d205a7d41262bf067c56c403d`
**Preparação:** AUTORIZADA
**Implementação:** AUTORIZADA E IMPLEMENTADA TECNICAMENTE — ver adendo ao final
**Objetivo:** importar aproximadamente 2.300 cadastros de câmeras a partir de planilha XLSX.

## 1. Decisões e invariantes já aprovados

A seção HOM-02 de `docs/projeto/SPRINTS_ARGOS_V5.md` e o checkpoint
`HOM_01_UI_V2_BASELINE_CHECKPOINT.md` §7 registram as decisões-base a preservar:

- Não incluir nem aceitar `id_argos` fornecido pela planilha. O identificador
  interno de novo registro é gerado pelo banco.
- Classificar cada linha como `CREATE` ou `UPDATE` com correspondência única e
  inequívoca por patrimônio ou número de série. Nome ou IP isolados não
  identificam registro para atualização.
- Apresentar prévia inteligível sem gravar dados e exigir confirmação explícita.
- Validar os dados com formulários, modelos, validadores e serviços canônicos
  do Django, incluindo normalização, campos obrigatórios, unicidade e choices.
- Adotar atomicidade de lote: erro em qualquer linha impede a confirmação; erro
  durante a gravação reverte o lote inteiro.
- Não alterar diretamente o estado do MON Runtime.
- Preservar integridade cadastral e trilha de auditoria.
- Reutilizar a arquitetura e os componentes existentes; não redesenhar
  componentes aprovados.

A exportação XLSX já aprovada continua não bloqueante e não altera estes
invariantes.

## 2. Evidência técnica existente

- `cameras/models.py`: `Camera.serial` e `Camera.patrimonio` são únicos e
  nullable; novos registros podem usar `origem_cadastro=IMPORTACAO`. O modelo
  também normaliza valores e mantém constraints de unicidade adicionais.
- `cameras/forms.py`: existem `CameraCriacaoForm` e `CameraEdicaoForm`, com
  normalização e validação dos campos cadastrais e catálogos.
- O fluxo de edição atual usa transação, ator e evento de auditoria; mudança de
  IP chama `invalidate_target_config_generation_if_ip_changed(...)`.
- `cameras/auditoria.py`: `registrar_evento` cria `EventoAuditoria`; os valores
  de origem atualmente definidos são `WEB`, `ADMIN`, `COMANDO` e `SISTEMA`.
- Não foi localizado importador XLSX nem dependência de parser XLSX nas
  dependências inspecionadas. Portanto, a seleção/adjudicação de parser é uma
  decisão de implementação ainda pendente.

Estas observações são evidência da arquitetura existente, não autorização para
alterar o modelo, os formulários, permissões, eventos, dependências ou MON
Runtime.

## 3. Fluxo proposto

1. Usuário autorizado carrega o XLSX. O sistema valida o invólucro do arquivo,
   versão/schema e conteúdo suportado antes de processar linhas.
2. Leitura e normalização ocorrem sem escrita em `Camera`. Cada linha recebe
   referência de linha, resultado de validação e ação prevista (`CREATE`,
   `UPDATE` ou erro/conflito).
3. A resolução de destino compara patrimônio e serial normalizados contra o
   cadastro. A correspondência é inequívoca apenas quando os identificadores
   presentes apontam para um mesmo registro; regras de divergência aguardam
   decisão na seção 4.
4. A prévia mostra valores de entrada e destino, ação por linha, diferenças que
   seriam aplicadas e erros. Qualquer erro ou conflito bloqueia o botão de
   confirmação para o lote inteiro.
5. Na confirmação, o sistema revalida permissões, identificadores, conflitos e
   valores contra o estado atual do banco. A prévia não pode autorizar gravação
   sobre estado que mudou desde sua criação.
6. Uma transação aplica as operações e os eventos de auditoria. Falha em
   qualquer operação causa rollback integral. Em atualizações, reutilizar os
   caminhos de domínio existentes, inclusive a invalidação relacionada a
   mudança de IP quando aplicável.
7. Ao final, apresentar resumo por lote (criadas, atualizadas, rejeitadas ou
   falha), referência de lote e erros associados às linhas, sem revelar dados
   sensíveis desnecessários.

Este fluxo é proposta para autorização e não registra implementação existente.

## 4. Decisões funcionais ainda necessárias

Os itens abaixo estão em aberto. As sugestões na última coluna são defaults
recomendados para adjudicação, não decisões aprovadas.

| Decisão aberta | Recomendação para aprovação | Evidência / impacto |
|---|---|---|
| Schema, nome da aba, cabeçalhos, colunas, tipos, formato de datas e representação de choices/catálogos | Homologar um template versionado e um mapeamento explícito para campos permitidos após revisão do schema canônico; não inferir colunas neste documento | O schema/template definitivo ainda não está homologado; modelos e formulários existentes definem os campos e validações |
| Patrimônio e serial identificam registros diferentes; um identificador aponta para existente e outro não corresponde; identificador repetido no arquivo ou várias linhas apontam à mesma câmera | Rejeitar os conflitos/duplicatas e bloquear o lote inteiro, com indicação das linhas relacionadas | Impede atualização ambígua e duplicação silenciosa; matching aprovado exige unicidade e inequívoco |
| Semântica de célula vazia em `UPDATE` | Vazio significa preservar o valor atual; eventual limpeza de campo opcional requer marcação explícita homologada | Evita apagar dados cadastrais por células vazias comuns em planilhas |
| Requisitos mínimos de identificação para `CREATE` | Exigir ao menos um entre patrimônio e serial; rejeitar duplicidade e conflito antes da prévia confirmável | Ambos os campos podem ser nulos no modelo; repetibilidade e prevenção de duplicatas precisam de regra funcional explícita |
| Autorização para criação e atualização em lote | Aprovar matriz que exija permissões de criação e edição correspondentes, ou criar permissão dedicada à importação em lote; restringir confirmação ao menor conjunto adequado | Importação pode afetar muitos registros; autoridade e escopo da permissão ainda precisam de decisão |
| Contrato de auditoria e retenção do arquivo | Registrar evento por câmera/linha e resumo do lote com ator, identificador do lote e ação; não reter o XLSX original por padrão, salvo política aprovada | `registrar_evento` existe, mas origem `IMPORTACAO` não está no enum atual de `EventoAuditoria`; mudanças de enum/modelo e retenção exigem adjudicação |
| Planilha: abas, fórmulas, macros, linhas/colunas ocultas, links externos, tamanho e quantidade máxima de linhas | Aprovar um único formato de tabela/aba, valores simples sem fórmulas, macros ou links externos; decidir e documentar limites de bytes e linhas antes da implementação | A quantidade aproximada é 2.300, mas não há limite técnico aprovado; limites não devem ser inventados |
| Validade da prévia diante de concorrência ou mudanças no banco | Vincular a confirmação à prévia gerada e revalidar sob transação; rejeitar prévia obsoleta e exigir nova prévia | Protege contra alteração do destino entre preview e confirmação |
| Escopo de campos editáveis | Permitir apenas campos cadastrais aprovados pelo template; excluir IDs e metadados de sistema, ator/timestamps, status de monitoramento e situação operacional sujeita a governança própria | Evita escrita de estado técnico/controle interno por planilha; mudanças de IP devem seguir serviço existente |
| Parser XLSX e proteção operacional | Selecionar dependência XLSX mantida após revisão de compatibilidade/licença e aprovar limites de arquivo/linhas; nenhuma instalação é autorizada nesta preparação | Nenhum parser/dependência existente foi localizado nas dependências inspecionadas |

## 5. Defaults recomendados para adjudicação

Para tornar a decisão de implementação objetiva, recomenda-se aprovar em conjunto:

1. Conflito de identificadores, duplicata no arquivo ou múltiplas linhas para o
   mesmo destino bloqueiam o lote, com diagnóstico por linha.
2. Célula vazia em atualização preserva o dado atual; limpeza explícita usa
   convenção de template deliberadamente aprovada.
3. `CREATE` exige ao menos patrimônio ou serial; não permitir atualização
   apenas por nome/IP.
4. A confirmação requer autorização compatível com todas as operações. Escolher
   formalmente entre exigir permissões existentes `add` + `change` conforme o
   tipo de linha, ou permissão específica de importação em lote.
5. Prévia é vinculada ao arquivo, ator e snapshot/resolução; confirmação
   revalida sob transação. Qualquer divergência material invalida a prévia.
6. Excluir da planilha estado MON, situação operacional, status interno, ID,
   timestamps, campos de ator e outros metadados de sistema. Criação define
   `origem_cadastro=IMPORTACAO`; atualização preserva a origem atual.
7. Auditar cada alteração e resumo do lote sem armazenar o arquivo original
   por padrão. Aprovar se isso requer nova origem enum/modelo ou se o contrato
   atual suporta os metadados necessários.
8. Limitar XLSX a tabela e conteúdo simples; aprovar explicitamente limites de
   bytes e linhas, parser e política de retenção. Não assumir limite numérico
   antes da aprovação.
9. Reutilizar shell, navegação, padrões de Inventário e componentes de UI
   existentes; sem redesenho. Executar o Design QA aplicável quando houver
   implementação visual, conforme os gates vigentes.

## 6. Critérios propostos para autorização/aceite da implementação

A implementação estará pronta para revisão quando, no mínimo:

- template versionado e schema revisado estiverem homologados;
- CREATE, UPDATE, conflito, duplicata, campo vazio, campos editáveis,
  autorização, auditoria, retenção e limites do arquivo estiverem adjudicados;
- prévia não produzir escrita e explicar ação/diferenças/erros por linha;
- qualquer erro ou conflito bloquear confirmação do lote completo;
- confirmação revalidar permissões e estado, rejeitando prévia obsoleta;
- sucesso persistir todas as linhas elegíveis e eventos na mesma fronteira
  transacional; falha deixar zero efeitos parciais;
- validações usarem formulários/serviços canônicos e respeitarem unicidade,
  normalização e choices;
- não houver ID ARGOS manual nem mudança direta de MON Runtime;
- testes cobrirem criação, atualização, validação, conflitos, duplicatas,
  concorrência, permissões, auditoria, atomicidade e rollback no banco alvo;
- volume próximo de 2.300 seja exercitado de forma progressiva e controlada,
  sem disparo em massa de probes, conforme a decisão já registrada no Sprint
  Map;
- interface use componentes existentes e passe pelos gates visuais aprovados,
  sem alterar baseline protegida.

## 7. Autorização e próximo passo

```text
HOM01_STATUS = CLOSED / user approved
HOM02_PREPARATION = AUTHORIZED / proposal complete
HOM02_IMPLEMENTATION = NOT_YET_AUTHORIZED
HOM02_OPEN_DECISIONS = schema/template; matching conflicts/duplicates; blank semantics; CREATE identifiers; permissions; audit/retention; XLSX rules/limits/parser; stale preview; editable fields
```

Para iniciar HOM-02, o usuário deve aprovar as decisões abertas (aceitando ou
ajustando as recomendações) e autorizar explicitamente a implementação. A
aprovação de encerramento HOM-01 e a autorização desta preparação não concedem
autoridade para código, testes de implementação, migrations, dependências,
branch nova, publicação ou mudança no MON Runtime.

## 8. Referências

- `docs/projeto/SPRINTS_ARGOS_V5.md` — seção HOM-02, decisões-base e critérios
  existentes.
- `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` — §7 e §16.
- `cameras/models.py` — campos e constraints de `Camera`.
- `cameras/forms.py` — formulários canônicos de criação/edição.
- `cameras/auditoria.py` — `registrar_evento` e evento auditável.
- `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` — §§112–114.

---

**Status deste documento:** proposta preparatória histórica; o adendo §9 registra
a autorização posterior e a implementação técnica. A homologação humana ainda
está pendente.

## 9. Adendo — implementação autorizada e entregue (2026-10-14)

O pedido explícito `HOM-02-XLSX-IMPORT-IMPLEMENTATION` resolveu as decisões
funcionais abertas neste documento e concedeu autorização de implementação.
As seções 4–7 permanecem como histórico da preparação; seus itens em aberto e
defaults recomendados foram substituídos pelo contrato funcional aprovado no
pedido de implementação. Este documento não limita nem condiciona a entrega.

Estado: fluxo SSR completo integrado ao Inventário; template XLSX v1 gerado
pela aplicação com aba de instruções; upload, validação e prévia sem escrita;
confirmação `ALL_OR_NOTHING`, revalidação concorrente e auditoria por registro
e lote. Matching usa exclusivamente patrimônio e serial. A permissão
`importar_cameras` é adicional às permissões de criação/edição. O limite é
5.000 linhas e 10 MB; `openpyxl` rejeita fórmulas, macros, links externos e
conteúdo ativo. A prévia expira em 30 minutos e fica vinculada ao usuário,
hash do arquivo e conteúdo validado.

Validação técnica passou: regressão direcionada de integração (163 testes),
suíte do importador (13 testes em 40.173s, com 2.300 criações e confirmações),
incluindo geração/leitura do template e fluxo SSR, Django system check e
consistência das migrações. `HOM01_STATUS=CLOSED`;
`HOM02_IMPLEMENTATION=IMPLEMENTED`;
`HOM02_HUMAN_ACCEPTANCE=PENDING`. Nenhum MON Runtime, push, merge ou deploy foi
alterado/executado. O registro corrente está em
`docs/projeto/SPRINTS_ARGOS_V5.md`, seção HOM-02; o adendo §10 registra o
bugfix da prévia e o finding de provisionamento de autorização.

## 10. Correção da prévia UPDATE e finding de autorização (2026-10-15)

A validação de `CameraEdicaoForm` podia normalizar a instância-alvo antes do
cálculo do diff da prévia. `cameras/xlsx_import.py` agora conserva um snapshot
independente da câmera original antes de construir o formulário e usa esse
snapshot para `calcular_alteracoes` e `target_label`. A regressão cobre UPDATE
com alteração de nome (um campo alterado, valores anterior/novo e destino com
nome original), UPDATE sem alterações (zero campos), persistência do nome e
auditoria. Também foram reexecutados os testes do importador e a regressão de
auditoria/compatibilidade/normalização: 14 e 31 testes, respectivamente;
`manage.py check` e `git diff --check` passaram. O banco de teste foi SQLite em
memória e não houve acesso ao PostgreSQL da VM nem confirmação da prévia
preexistente.

**Finding de autorização pendente:** as views exigem a permissão
`cameras.importar_cameras`, mas o comando padrão não a atribui aos grupos
Operador/Técnico. O Administrador recebe a permissão pelo conjunto de
permissões de câmera; para os demais grupos, o grant depende de adjudicação e
provisionamento futuros. Nenhum grant ou contrato foi alterado neste pacote.
Este finding não invalida o snapshot técnico, mas impede declarar prontidão
operacional integral ou aceite humano da HOM-02.

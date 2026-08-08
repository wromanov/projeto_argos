# 04 — Modelo de Domínio do Projeto ARGOS

## 1. Entidade central — Câmera

A câmera é a principal entidade do ARGOS.

Ela representa o equipamento físico/lógico acompanhado pelo sistema.

### Grupos de dados

#### Identificação

- patrimônio;
- nome;
- fabricante;
- modelo;
- serial;
- MAC;
- tipo.

#### Localização

- terminal;
- pavimento;
- setor;
- ambiente;
- descrição detalhada;
- ponto de referência.

#### Rede

- IP;
- máscara;
- gateway;
- VLAN.

#### Gravação

- farm;
- retenção esperada;
- codec.

#### Monitoramento técnico

- status;
- status desde;
- última verificação.

#### Governança

- situação operacional;
- completude cadastral;
- motivo de desativação;
- data de desativação;
- usuário responsável;
- origem do cadastro;
- observações;
- criação;
- atualização.

## 2. Situação operacional

É um estado administrativo/operacional.

Valores oficiais:

```text
PRODUCAO
ESTOQUE
DESATIVADA
```

Não confundir com status técnico.

## 3. Status técnico

Representa disponibilidade observada.

Valores:

```text
ONLINE
OFFLINE
NAO_VERIFICADO
```

## 4. Completude cadastral

Indica se o registro possui o conjunto de informações considerado necessário.

A interface pode apresentar:

- cadastro completo;
- cadastro incompleto;
- campos faltantes.

Completude não é a mesma coisa que situação operacional.

## 5. Atividade da câmera

Representa um fato operacional registrado manualmente.

Exemplos:

- manutenção;
- intervenção;
- inspeção;
- ocorrência;
- ajuste.

Campos conceituais:

- câmera;
- tipo;
- título;
- descrição;
- data/hora;
- responsável;
- criado por;
- atualizado por.

## 6. Evento de auditoria

Representa alteração auditável.

Deve preservar:

- código;
- categoria;
- resumo;
- usuário;
- entidade;
- câmera relacionada;
- alterações;
- origem;
- data/hora.

A auditoria é historicamente imutável.

## 7. Substituição de câmera

Representa troca de um equipamento por outro.

Relaciona:

- câmera anterior;
- câmera substituta;
- nome operacional;
- motivo;
- observações;
- data/hora;
- usuário responsável.

A substituição não deve apagar a câmera anterior.

## 8. Indisponibilidade

Representa um intervalo no qual a câmera permaneceu Offline.

Modelo conceitual:

```text
Camera
  |
  +-- 1:N Indisponibilidade
```

Cada registro deve possuir:

- início;
- fim;
- duração calculável;
- origem da detecção quando aplicável.

## 9. Snapshot

Entidade planejada.

Relacionamento:

```text
Camera
  |
  +-- 1:N Snapshot
```

Tipos conceituais:

- automático;
- manual;
- principal/protegido.

Regras:

- automático em Offline -> Online;
- automático na primeira detecção Online;
- máximo de três snapshots automáticos recentes;
- snapshot manual protegido não é removido pela rotação.

## 10. Credencial de monitoramento

Entidade planejada.

Deve representar:

- usuário;
- senha protegida;
- parâmetros de autenticação;
- metadados necessários.

Nunca expor senha diretamente.

## 11. Configuração RTSP

Entidade ou configuração planejada.

Pode conter:

- porta;
- path;
- codec esperado;
- fabricante;
- estratégia de composição;
- timeout;
- parâmetros adicionais.

## 12. Relações principais

```text
Camera
 ├── Atividades
 ├── Eventos de auditoria
 ├── Indisponibilidades
 ├── Snapshots
 ├── Credenciais/configuração
 └── Substituições
      ├── câmera anterior
      └── câmera substituta
```

## 13. Regra de integridade fundamental

A história do equipamento deve ser preservada.

Por isso:

- não usar exclusão física normal;
- não sobrescrever transições sem auditoria;
- não transformar substituição em simples edição do equipamento;
- não misturar situação operacional com status técnico.

---

**Este modelo conceitual deve orientar models, forms, serviços e interface.**

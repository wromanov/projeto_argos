# Governança operacional das câmeras

## Situações

- **Produção**: equipamento instalado e em operação. Exige identificação física, localização, rede e gravação completas.
- **Estoque**: equipamento disponível fora de operação. Exige apenas identificação física completa.
- **Desativada**: registro histórico fora de operação. Pode manter cadastro legado mínimo e nunca é excluído pela governança.

O status técnico (Online, Offline ou Não verificado) permanece independente da situação operacional.

## Transições

As operações de desativação, reativação, movimentação entre Produção e Estoque e substituição física são executadas em transações atômicas, com bloqueio dos registros envolvidos. Falhas de validação ou auditoria revertem toda a operação.

Desativação exige motivo. Reativação exige justificativa e destino. Entrada em Produção exige cadastro completo. A edição comum não expõe a situação operacional.

## Substituição física

A câmera anterior deve estar em Produção e a substituta em Estoque. O processo transfere nome, localização, rede e gravação operacionais; preserva patrimônio, fabricante, modelo, serial, MAC e tipo da substituta; desativa a anterior; coloca a substituta em Produção; e cria um registro imutável com duas trilhas de auditoria.

## Integridade

O MAC é normalizado para `AA:BB:CC:DD:EE:FF` e é único quando informado. O nome é único sem diferenciar maiúsculas/minúsculas entre câmeras não desativadas. IPs duplicados são permitidos e aparecem no dashboard como indicador de revisão.

## Permissões

Monitoramento consulta inventário, atividades, eventos e substituições. Operação também cadastra/edita câmeras e atividades e executa transições/substituições. Administração recebe essas capacidades e a gestão de usuários, sem permissões de exclusão dos registros governados.

## Limitações atuais

Esta sprint não armazena credenciais, configuração web ou RTSP; não testa streams, não cria alertas externos e não exclui fisicamente câmeras ou substituições. Localizações, fabricantes e modelos permanecem nos campos atuais do inventário.

## Auditoria

Cada transição registra usuário, entidade, diferença de situação e justificativa ou motivo. A substituição cria eventos distintos para a câmera anterior e a substituta. Falha na auditoria reverte a transação operacional.

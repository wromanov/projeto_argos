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

Monitoramento consulta inventário, atividades, eventos, substituições e health resumido. Operador também cadastra/edita campos cadastrais permitidos, notas e atividades e executa transições/substituições; pode consultar URI RTSP sanitizada, sem alterá-la e sem ver username/password. Técnico recebe a operação técnica de câmera, incluindo RTSP, credenciais, reveal, diagnóstico, teste de conexão e monitoramento, sem administrar usuários, política global de rede ou sistema. Administrador recebe essas capacidades mais gestão de usuários/perfis/sistema, sem permissão de exclusão dos registros governados. A matriz Django detalhada e o status de implementação pertencem ao contrato `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md`.

## Limitações atuais

No checkout BC-02, ainda não há credenciais, configuração RTSP ou teste de streams implementados; BC-02 fechou apenas contratos para implementação posterior. Alertas externos e exclusão física de câmeras/substituições continuam fora deste checkpoint. Localizações, fabricantes e modelos permanecem nos campos atuais do inventário; firmware técnico será adicionado na slice CAM-INT-06.

## Auditoria

Cada transição registra usuário, entidade, diferença de situação e justificativa ou motivo. A substituição cria eventos distintos para a câmera anterior e a substituta. Falha na auditoria reverte a transação operacional.

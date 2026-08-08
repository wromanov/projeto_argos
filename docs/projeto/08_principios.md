# 08 — Princípios do Projeto ARGOS

## 1. Preservar histórico

O ARGOS deve preferir rastreabilidade a conveniência.

Alterações importantes precisam preservar o passado.

## 2. Status não é situação

Disponibilidade técnica e condição operacional são dimensões diferentes.

Nunca misturar.

## 3. Segurança por padrão

Dados sensíveis devem possuir proteção desde o desenho.

Não adicionar segurança apenas depois.

## 4. Menor privilégio

Cada perfil recebe somente o acesso necessário.

## 5. Evidência antes de conclusão

Não assumir que uma mudança funciona.

Testar.

## 6. Mudanças pequenas

Preferir microetapas verificáveis a grandes refatorações simultâneas.

## 7. Um commit, uma intenção

Cada commit deve representar uma entrega coerente.

## 8. Operação antes de decoração

A interface existe para facilitar trabalho operacional.

Hierarquia, clareza e densidade correta têm prioridade sobre efeitos visuais.

## 9. Cor com significado

- verde: positivo;
- vermelho: falha/destrutivo;
- ocre: atenção;
- azul: domínio técnico/institucional;
- cinza: neutro/contextual.

## 10. Sem framework visual por impulso

Não introduzir Bootstrap, Tailwind ou biblioteca equivalente sem decisão arquitetural.

## 11. Não duplicar conceitos

Antes de criar componente ou classe:

- verificar se já existe;
- verificar design system;
- reutilizar quando apropriado.

## 12. Não esconder regras no template

Template apresenta.

Domínio decide.

## 13. Governança explícita

Transições importantes devem possuir fluxos claros.

## 14. Falhar de forma segura

Erros de RTSP, snapshot ou keepalive não devem comprometer integridade dos dados.

## 15. Timeouts são obrigatórios em integrações

Nenhuma integração de rede deve poder bloquear indefinidamente.

## 16. Concorrência controlada

Mais paralelismo não significa automaticamente mais desempenho.

Medir.

## 17. Implantação progressiva

Funcionalidades de escala devem começar pequenas.

## 18. Segredos não aparecem

Nunca em:

- logs;
- HTML;
- mensagens;
- traceback apresentado ao usuário;
- commits.

## 19. Testes fazem parte da entrega

Uma feature sem gate de teste não está pronta.

## 20. Suíte completa antes do commit importante

Testes direcionados aceleram desenvolvimento.

Suíte completa fecha a etapa.

## 21. O Git é parte do processo de qualidade

Sempre verificar:

```text
diff
status
arquivos staged
commit
```

## 22. Não fazer push implicitamente

Push é uma ação separada.

## 23. Documentação deve acompanhar decisões duráveis

Roadmap, ADRs e handoff devem ser mantidos atualizados.

## 24. O detalhe da câmera é referência de UI

O redesign aprovado da página de detalhe serve como referência visual para novas telas.

## 25. O ARGOS é um sistema operacional, não um CRUD genérico

Toda decisão deve considerar:

- velocidade de consulta;
- rastreabilidade;
- criticidade do ambiente;
- escala do parque;
- manutenção de longo prazo.

---

**Estes princípios devem orientar código, arquitetura, UX, segurança e governança.**

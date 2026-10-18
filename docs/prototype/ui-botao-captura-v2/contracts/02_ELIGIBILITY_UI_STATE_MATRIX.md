# Matriz de estados visuais — E3 C V2.1

A matriz abaixo descreve **a proposta visual aprovada**, não afirma que esses estados já são expostos pelo backend da implementação atual. Os mapeamentos devem ser verificados contra o contrato técnico canônico e a matriz de autorização antes da codificação.

| Cenário | Pré-condição factual requerida do backend | Upload | Zona de captura / CTA | Evidência esperada |
|---|---|---|---|---|
| **01** Ambas disponíveis | Usuário autorizado para cada operação; captura elegível confirmada | Visível se permitido | Mostrar título, descrição e **Capturar imagem** | Baseline B, superfície branca e divisor |
| **02** Indisponibilidade transitória | Estado temporário explicitamente autorizado ao usuário | Independente | Mensagem discreta, **sem CTA** | Sem botão inerte |
| **03** Configuração incompleta | Classificação segura e conhecida pelo serviço | Independente | Mensagem genérica, **sem CTA** | Não divulgar credencial, endereço ou policy |
| **04a** Método não suportado | Capability `UNSUPPORTED` confirmada | Independente | Mensagem segura, **sem CTA** | Não deduzir de timeout/erro genérico |
| **04b** Suporte desconhecido | Capability `UNKNOWN` ou sem evidência suficiente | Independente | Mensagem neutra, **sem CTA** | Não converter `UNKNOWN` em `UNSUPPORTED` |
| **05** Apenas captura | Captura permitida, upload não autorizado/disponível pela própria regra | Oculto | Captura usa largura única, sem divisor | Nenhuma coluna em branco |
| **06** Nenhuma operação | Backend determina ausência de ambas e informa se é permitido revelar estado genérico | Oculto | Oculto; se autorizado, mensagem genérica; senão omitir seção | Sem vazamento de restrição privilegiada |
| **07a** Job em execução | Job real `QUEUED` ou `RUNNING`, visível por ownership/permissão | Independente | Feedback compacto; sem nova captura impedida pelo job | Não inventar conclusão |
| **07b** Job falhou | `FAILED` real + elegibilidade renovada e nova intenção permitida | Independente | Falha sanitizada; **nova captura** apenas se autorizada | Reintenção e chave de idempotência corretas |
| **08** Sem permissão de captura | Falta `cameras.capture_camera_image` | Independente | Não renderizar zona de captura ou informações privilegiadas | Upload ocupa toda largura se visível |

## Copy de referência da V2.1

- 02: **Captura indisponível no momento** · “Tente novamente mais tarde.”
- 03: **Configuração de captura incompleta** · “O perfil de captura desta câmera precisa ser revisado.”
- 04a: **Método de captura não suportado** · “O método configurado não é compatível com o fluxo de captura disponível.”
- 04b: **Suporte à captura não confirmado** · “Não foi possível confirmar se este método está disponível.”
- 06: **Nenhuma operação de imagem disponível no momento**, apenas quando apropriado para a audiência.
- 07a: **Captura em processamento** · sem sucesso antecipado.
- 07b: **Não foi possível concluir a captura** · próximo passo seguro.

Os textos podem demandar generalização se o contrato de segurança proibir revelar uma classificação específica. **A aprovação visual da V2.1 não aprova vazamento de informações de configuração.**

## Regras de DOM, UX e segurança

- Em modo bloqueado, não basta estilizar o botão: a UI produtiva deve omiti-lo/ocultá-lo efetivamente, inclusive de tabulação e tecnologia assistiva. SSR autorizativo é preferível a depender do cliente para esconder controles sensíveis.
- Quando apenas uma operação aparecer, ela preenche a largura e o divisor desaparece. Quando ambas aparecem, grid lado a lado e divisor.
- Em `QUEUED`/`RUNNING`, feedback atrelado ao job autorizado; `<status>` acessível se evento assíncrono, sem anúncios duplicados.
- Upload não herda a autorização de captura; autorização de captura não confere upload.
- A interface nunca aceita destino/URL/IP arbitrários vindos do browser, nem segredos do servidor enviados ao HTML.
- Falha terminal pode permitir **nova intenção** somente após verificação server-side; não reaproveitar chave de idempotência de uma solicitação concluída para uma nova intenção.
- `Ver imagens` / galeria E4 não faz parte da entrega E3.

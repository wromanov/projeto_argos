const params = new URLSearchParams(window.location.search);
const state = params.get('state') || 'default';
const set = (field, value) => { document.querySelectorAll(`[data-field="${field}"]`).forEach((node) => { node.textContent = value; }); };
const badge = (field, value, tone) => {
  document.querySelectorAll(`[data-field="${field}"]`).forEach((node) => {
    node.textContent = value;
    node.className = `argos-status-badge argos-status-badge--${tone}`;
  });
};

if (state === 'missing' || state === 'long') {
  badge('completion-badge', 'Cadastro incompleto', 'warning');
  badge('completion-detail', 'Cadastro incompleto', 'warning');
  set('missing', 'MAC, Gateway, Ponto de referência');
  set('mac', '—');
  set('gateway', '—');
  set('referencia', '—');
}
if (state === 'long') {
  document.querySelectorAll('[data-long-only]').forEach((node) => { node.hidden = false; });
  set('nome', 'P5 DEV — Câmera do corredor leste de acesso ao embarque e integração operacional');
  set('fabricante', 'Fabricante de Equipamentos de Monitoramento');
  set('fabricante-detail', 'Fabricante de Equipamentos de Monitoramento');
  set('modelo', 'P3265-LVE com configuração estendida');
  set('modelo-detail', 'P3265-LVE com configuração estendida');
  set('location-summary', 'Terminal Leste · 1º pavimento · Corredor de acesso ao embarque com orientação para a ala internacional');
  set('ambiente', 'Corredor de acesso ao embarque com orientação para a ala internacional');
  set('descricao', 'Instalada no trecho de circulação entre o saguão principal, a passagem de serviço e a entrada da área de embarque. A descrição longa exercita a quebra natural de conteúdo sem recorte.');
  set('missing', 'MAC, Gateway, Ponto de referência, Retenção esperada, Observações cadastrais');
  set('history-outages', '05/10/2026 21:10 → 22:04 · Duração: 54 min · Monitoramento técnico · Restabelecimento confirmado');
  set('history-activities', 'Inspeção de imagem · 05/10/2026 17:45 · Equipe CFTV — Verificação do enquadramento após manutenção preventiva no corredor.');
  set('history-replacements', '04/10/2026 10:32 · Foi substituída · P5 DEV → Câmera de reserva');
  set('history-audit', 'CAMERA_UPDATED · Dados cadastrais atualizados após inspeção técnica.');
}
if (state === 'default') document.querySelector('[data-field-container="missing"]').hidden = true;
document.querySelector('[data-field-container="outage"]').hidden = true;

document.querySelectorAll('[data-demo-action]').forEach((link) => link.addEventListener('click', (event) => {
  event.preventDefault();
  document.getElementById('prototype-feedback').textContent = `${link.dataset.demoAction}: ação demonstrativa. Rota funcional preservada no contrato visual; este protótipo não altera dados.`;
}));
document.querySelector('[data-demo-form]').addEventListener('submit', (event) => {
  event.preventDefault();
  document.getElementById('prototype-feedback').textContent = 'Enviar imagem: composição demonstrativa. Upload, CSRF, validação e permissões continuam sob o fluxo Django existente.';
});

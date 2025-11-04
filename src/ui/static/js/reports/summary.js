/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

/* global RS */
(() => {
  // UI elements
  const surveySelect = document.getElementById('surveySelect');
  const refreshBtn = document.getElementById('refreshSummaryBtn');
  const exportCsvBtn = document.getElementById('exportCsvBtn');
  const exportTokensCsvBtn = document.getElementById('exportTokensCsvBtn');
  const summaryContainer = document.getElementById('summaryContainer');
  const tokensTBody = document.getElementById('tokensTableBody');
  const dateFromEl = document.getElementById('dateFrom');
  const dateToEl = document.getElementById('dateTo');

  const fmtDate = iso => {
    if (!iso) {
      return '-';
    }
    try {
      const d = new Date(iso);
      return d.toLocaleString();
    } catch (_) {
      return String(iso);
    }
  };

  if (tokensTBody) {
    tokensTBody.addEventListener('click', e => {
      const btn = e.target.closest('button[data-link]');
      if (!btn) {
        return;
      }

      const link = btn.getAttribute('data-link');
      const copyPromise =
        window.RS && RS.utils && RS.utils.copyToClipboard
          ? RS.utils.copyToClipboard(link)
          : navigator.clipboard.writeText(link);

      Promise.resolve(copyPromise)
        .then(() => {
          btn.textContent = 'Copiado!';
          setTimeout(() => (btn.textContent = 'Copiar enlace'), 1200);
        })
        .catch(() => alert('No se pudo copiar.'));
    });
  }

  const loadSurveys = async () => {
    try {
      const rows = await RS.http.apiFetch('/surveys', { method: 'GET' });
      surveySelect.innerHTML = '';

      if (!Array.isArray(rows) || rows.length === 0) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'No hay encuestas';

        surveySelect.appendChild(opt);
        return;
      }

      for (const s of rows) {
        const opt = document.createElement('option');
        opt.value = String(s.id);
        opt.textContent = `${s.title} (ID: ${s.id})`;
        surveySelect.appendChild(opt);
      }
    } catch (err) {
      surveySelect.innerHTML = '';

      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Error al cargar encuestas';

      surveySelect.appendChild(opt);
      console.error('loadSurveys error:', err);
    }
  };

  const clearSummary = () => {
    summaryContainer.innerHTML = '';
  };

  const renderQuestionCard = q => {
    const card = document.createElement('div');
    card.className = 'border border-gray-200 rounded-lg p-4';

    const header = document.createElement('div');
    header.className = 'flex items-center justify-between mb-3';
    header.innerHTML = `
      <h4 class="text-md font-semibold text-gray-800">${q.text}</h4>
      <span class="text-sm text-gray-600">Total respuestas: ${q.total}</span>
    `;
    card.appendChild(header);

    const table = document.createElement('table');
    table.className = 'min-w-full border border-gray-200 rounded';

    const thead = document.createElement('thead');
    thead.className = 'bg-gray-50';
    thead.innerHTML = `
      <tr>
        <th class="px-3 py-2 text-left text-sm font-medium text-gray-700">Valor</th>
        <th class="px-3 py-2 text-left text-sm font-medium text-gray-700">Conteo</th>
      </tr>
    `;

    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    for (const a of q.answers || []) {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="px-3 py-2 text-sm text-gray-800">${String(a.value)}</td>
        <td class="px-3 py-2 text-sm text-gray-800">${Number(a.count) || 0}</td>
      `;
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    card.appendChild(table);

    if (window.Chart && Array.isArray(q.answers) && q.answers.length > 0) {
      const labels = q.answers.map(a => String(a.value));
      const data = q.answers.map(a => Number(a.count) || 0);

      const canvasWrap = document.createElement('div');
      canvasWrap.className = 'mt-4';

      const canvas = document.createElement('canvas');
      canvas.height = 120;
      canvasWrap.appendChild(canvas);

      card.appendChild(canvasWrap);
      const ctx = canvas.getContext('2d');
      canvas._chart = new window.Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Distribución',
              data,
              backgroundColor: 'rgba(30, 58, 95, 0.2)',
              borderColor: 'rgba(30, 58, 95, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    }

    summaryContainer.appendChild(card);
  };

  const loadSummary = async () => {
    const surveyId = Number(surveySelect.value);
    if (!surveyId) {
      clearSummary();
      return;
    }

    clearSummary();
    const date_from = dateFromEl.value
      ? new Date(dateFromEl.value).toISOString()
      : undefined;

    const date_to = dateToEl.value
      ? new Date(dateToEl.value).toISOString()
      : undefined;

    const qs = new URLSearchParams();

    if (date_from) {
      qs.set('date_from', date_from);
    }
    if (date_to) {
      qs.set('date_to', date_to);
    }

    const path = `/reports/surveys/${surveyId}/summary${qs.toString() ? `?${qs.toString()}` : ''}`;
    const summary = await RS.http.apiFetch(path, { method: 'GET' });

    const questions = Array.isArray(summary.questions) ? summary.questions : [];
    if (questions.length === 0) {
      const empty = document.createElement('p');
      empty.className = 'text-sm text-gray-600';
      empty.textContent =
        'No hay respuestas registradas en el rango seleccionado.';
      summaryContainer.appendChild(empty);
      return;
    }
    for (const q of questions) {
      renderQuestionCard(q);
    }
  };

  const loadTokens = async () => {
    const surveyId = Number(surveySelect.value);
    tokensTBody.innerHTML = '';
    if (!surveyId) {
      return;
    }

    const rows = await RS.http.apiFetch(
      `/tokens/${surveyId}/list?is_used=false&include_expired=false`,
      {
        method: 'GET',
      }
    );

    const baseResolveUrl = `${window.location.origin}/solve`;
    for (const t of rows || []) {
      const tr = document.createElement('tr');
      const link = `${baseResolveUrl}?token=${encodeURIComponent(t.token)}`;

      tr.innerHTML = `
        <td class="px-4 py-2 text-sm text-gray-800">${t.token}</td>
        <td class="px-4 py-2 text-sm text-gray-800">${fmtDate(t.expires_at)}</td>
        <td class="px-4 py-2 text-sm text-blue-700 underline break-all">
          <a href="${link}" target="_blank" rel="noopener">${link}</a>
        </td>
        <td class="px-4 py-2">
          <button class="px-3 py-1 bg-primary text-white rounded hover:bg-secondary" data-link="${link}">Copiar enlace</button>
        </td>
      `;
      tokensTBody.appendChild(tr);
    }
  };

  const exportSummaryCsv = async () => {
    const surveyId = Number(surveySelect.value);
    if (!surveyId) {
      return;
    }

    const date_from = dateFromEl.value
      ? new Date(dateFromEl.value).toISOString()
      : undefined;

    const date_to = dateToEl.value
      ? new Date(dateToEl.value).toISOString()
      : undefined;

    const qs = new URLSearchParams();
    qs.set('survey_id', String(surveyId));

    if (date_from) {
      qs.set('date_from', date_from);
    }
    if (date_to) {
      qs.set('date_to', date_to);
    }

    const blob = await RS.http.apiFetch(`/reports/export?${qs.toString()}`, {
      method: 'GET',
      responseType: 'blob',
    });

    if (window.RS && RS.utils && typeof RS.utils.downloadBlob === 'function') {
      RS.utils.downloadBlob(`survey_${surveyId}_summary.csv`, blob);
    } else {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');

      a.href = url;
      a.download = `survey_${surveyId}_summary.csv`;
      document.body.appendChild(a);

      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const exportTokensCsv = async () => {
    const surveyId = Number(surveySelect.value);
    if (!surveyId) {
      return;
    }

    const blob = await RS.http.apiFetch(
      `/tokens/${surveyId}/export?is_used=false&include_expired=false`,
      { method: 'GET', responseType: 'blob' }
    );

    if (window.RS && RS.utils && typeof RS.utils.downloadBlob === 'function') {
      RS.utils.downloadBlob(`survey_${surveyId}_tokens.csv`, blob);
    } else {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `survey_${surveyId}_tokens.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const init = async () => {
    await loadSurveys();
    const firstVal = surveySelect.options[0] && surveySelect.options[0].value;
    if (firstVal) {
      surveySelect.value = String(firstVal);
    }

    await loadSummary();
    await loadTokens();

    surveySelect.addEventListener('change', async () => {
      await loadSummary();
      await loadTokens();
    });

    refreshBtn.addEventListener('click', async () => {
      await loadSummary();
    });

    exportCsvBtn.addEventListener('click', exportSummaryCsv);
    exportTokensCsvBtn.addEventListener('click', exportTokensCsv);
  };

  document.addEventListener('DOMContentLoaded', init);
})();

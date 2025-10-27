(() => {
  const RS_CONFIG = window.RS_CONFIG || { apiBaseUrl: '' };
  const API_BASE_URL = RS_CONFIG.apiBaseUrl || '';

  function qs(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name) || '';
  }

  function $(sel) {
    return document.querySelector(sel);
  }

  const createEl = (tag, attrs = {}, children = []) => {
    const el = document.createElement(tag);

    Object.entries(attrs).forEach(([k, v]) => {
      if (k === 'class') {
        el.className = v;
      } else if (k.startsWith('data-')) {
        el.setAttribute(k, v);
      } else if (k === 'html') {
        el.innerHTML = v;
      } else {
        el.setAttribute(k, v);
      }
    });
    children.forEach(c => el.appendChild(c));

    return el;
  };

  const normalizeChoices = rawValues => {
    if (!rawValues) {
      return [];
    }
    if (Array.isArray(rawValues)) {
      return rawValues.filter(
        v => v !== null && v !== undefined && String(v).trim().length > 0
      );
    }

    if (typeof rawValues === 'string') {
      return rawValues
        .split(';')
        .map(s => s.trim())
        .filter(s => s.length > 0);
    }

    if (typeof rawValues === 'object') {
      try {
        return Object.values(rawValues)
          .map(v => String(v).trim())
          .filter(v => v.length > 0);
      } catch (_) {
        return [];
      }
    }
    return [];
  };

  const fetchSurveyByToken = async token => {
    const url = `${API_BASE_URL}/anonymous/resolve?token=${encodeURIComponent(
      token
    )}`;
    const resp = await fetch(url, { headers: { Accept: 'application/json' } });
    if (!resp.ok) {
      const msg = await resp.json().catch(() => ({ message: 'error' }));
      const m = (msg && msg.message) || 'error';
      throw new Error(m);
    }
    return resp.json();
  };

  const updateProgress = (current, total) => {
    const pct = Math.max(
      0,
      Math.min(100, Math.round(((current + 1) / total) * 100))
    );
    const bar = $('#progressBar');
    if (bar) {
      bar.style.width = `${pct}%`;
    }
  };

  const renderQuestion = (q, idx, total) => {
    const sec = createEl('section', {
      class: `${idx === 0 ? '' : 'hidden'} step`,
      'data-step': String(idx),
    });

    const title = createEl('h2', {
      class: 'text-lg font-medium mb-4',
      html: `${idx + 1}. ${q.text}`,
    });

    sec.appendChild(title);

    const fieldBox = createEl('div', { class: 'space-y-2' });

    if (q.type === 'text') {
      const ta = createEl('textarea', {
        name: `q_${q.id}`,
        class:
          'w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-900',

        rows: '4',
        'data-question-id': String(q.id),
        'data-type': 'text',
        ...(q.is_required ? { required: 'true' } : {}),
      });

      fieldBox.appendChild(ta);
    } else if (q.type === 'single_choice') {
      const values = normalizeChoices(q.options && q.options.values);
      values.forEach(v => {
        const label = createEl('label', {
          class:
            'flex items-center p-2 border rounded-lg hover:bg-gray-50 cursor-pointer',
        });

        const input = createEl('input', {
          type: 'radio',
          name: `q_${q.id}`,
          value: String(v),
          class: 'form-radio text-blue-900',
          'data-question-id': String(q.id),
          'data-type': 'single_choice',
          ...(q.is_required ? { required: 'true' } : {}),
        });

        const span = createEl('span', { class: 'ml-3', html: String(v) });
        label.appendChild(input);
        label.appendChild(span);
        fieldBox.appendChild(label);
      });
    } else if (q.type === 'multiple_choice') {
      const values = normalizeChoices(q.options && q.options.values);
      values.forEach(v => {
        const label = createEl('label', {
          class:
            'flex items-center p-2 border rounded-lg hover:bg-gray-50 cursor-pointer',
        });

        const input = createEl('input', {
          type: 'checkbox',
          name: `q_${q.id}`,
          value: String(v),
          class: 'form-checkbox text-blue-900',
          'data-question-id': String(q.id),
          'data-type': 'multiple_choice',
        });

        const span = createEl('span', { class: 'ml-3', html: String(v) });
        label.appendChild(input);
        label.appendChild(span);
        fieldBox.appendChild(label);
      });
      if (q.is_required) {
        const req = createEl('input', {
          type: 'hidden',
          'data-required-multiple': 'true',
          'data-question-id': String(q.id),
        });
        fieldBox.appendChild(req);
      }
    } else if (q.type === 'scale') {
      const min = (q.options && q.options.min) || 1;
      const max = (q.options && q.options.max) || 5;
      const wrap = createEl('div', { class: 'flex items-center gap-3' });
      const input = createEl('input', {
        type: 'range',
        min: String(min),
        max: String(max),
        value: String(min),
        class: 'w-full',
        'data-question-id': String(q.id),
        'data-type': 'scale',
        ...(q.is_required ? { required: 'true' } : {}),
      });

      const val = createEl('span', {
        class: 'ml-3 text-sm text-gray-700',
        html: String(min),
      });

      input.addEventListener('input', e => {
        val.textContent = String(e.target.value);
      });
      wrap.appendChild(input);
      wrap.appendChild(val);
      fieldBox.appendChild(wrap);
    } else if (q.type === 'rating') {
      const min = (q.options && (q.options.min ?? 1)) || 1;
      const max = (q.options && (q.options.max ?? 5)) || 5;
      const labels = (q.options && q.options.labels) || [];
      const wrap = createEl('div', { class: 'space-y-2' });
      const row = createEl('div', {
        class: 'flex items-center flex-wrap gap-3',
      });

      for (let val = min; val <= max; val++) {
        const label = createEl('label', {
          class: 'flex items-center gap-2 cursor-pointer',
        });

        const input = createEl('input', {
          type: 'radio',
          name: `q_${q.id}`,
          value: String(val),
          class: 'form-radio text-blue-900',
          'data-question-id': String(q.id),
          'data-type': 'rating',
          ...(q.is_required ? { required: 'true' } : {}),
        });

        const span = createEl('span', { class: 'text-sm', html: String(val) });
        label.appendChild(input);
        label.appendChild(span);
        row.appendChild(label);
      }

      const extremes = createEl('div', {
        class: 'flex justify-between text-xs text-gray-600',
      });

      const left = createEl('span', {
        html: labels[0] ? String(labels[0]) : '',
      });

      const right = createEl('span', {
        html: labels[1] ? String(labels[1]) : '',
      });

      extremes.appendChild(left);
      extremes.appendChild(right);
      wrap.appendChild(row);
      wrap.appendChild(extremes);
      fieldBox.appendChild(wrap);
    }

    sec.appendChild(fieldBox);

    const nav = createEl('div', { class: 'flex justify-between mt-6' });
    if (idx > 0) {
      const prev = createEl('button', {
        type: 'button',
        class:
          'prev-btn bg-gray-200 text-gray-800 px-5 py-2 rounded-lg shadow hover:bg-gray-300 transition',
      });

      prev.textContent = 'Anterior';
      prev.addEventListener('click', () => {
        const cur = document.querySelector(`section[data-step="${idx}"]`);
        const prevSec = document.querySelector(
          `section[data-step="${idx - 1}"]`
        );

        if (cur && prevSec) {
          cur.classList.add('hidden');
          prevSec.classList.remove('hidden');
          updateProgress(idx - 1, total);
        }
      });
      nav.appendChild(prev);
    } else {
      const spacer = createEl('div');
      nav.appendChild(spacer);
    }

    const isLast = idx === total - 1;
    const next = createEl('button', {
      type: isLast ? 'submit' : 'button',
      class: isLast
        ? 'bg-green-600 text-white px-6 py-2 rounded-lg shadow hover:bg-green-700 transition'
        : 'next-btn bg-blue-900 text-white px-5 py-2 rounded-lg shadow hover:bg-blue-950 transition',
    });
    next.textContent = isLast ? 'Enviar' : 'Siguiente';
    if (!isLast) {
      next.addEventListener('click', () => {
        const requiredMultiple = fieldBox.querySelector(
          '[data-required-multiple="true"]'
        );
        if (requiredMultiple) {
          const qid = requiredMultiple.getAttribute('data-question-id');
          const checked = document.querySelectorAll(
            `input[type="checkbox"][data-question-id="${qid}"]:checked`
          );
          if (checked.length === 0) {
            alert('Selecciona al menos una opción');
            return;
          }
        }
        const cur = document.querySelector(`section[data-step="${idx}"]`);
        const nextSec = document.querySelector(
          `section[data-step="${idx + 1}"]`
        );
        if (cur && nextSec) {
          cur.classList.add('hidden');
          nextSec.classList.remove('hidden');
          updateProgress(idx + 1, total);
        }
      });
    }
    nav.appendChild(next);

    sec.appendChild(nav);
    return sec;
  };

  const collectResponses = questions => {
    const items = [];
    for (const q of questions) {
      let answer = '';
      if (q.type === 'text') {
        const el = document.querySelector(
          `textarea[data-question-id="${q.id}"]`
        );

        answer = (el && el.value) || '';
      } else if (q.type === 'single_choice') {
        const el = document.querySelector(
          `input[type="radio"][data-question-id="${q.id}"]:checked`
        );

        answer = (el && el.value) || '';
      } else if (q.type === 'multiple_choice') {
        const els = document.querySelectorAll(
          `input[type="checkbox"][data-question-id="${q.id}"]:checked`
        );

        answer = Array.from(els)
          .map(e => e.value)
          .join('; ');
      } else if (q.type === 'scale') {
        const el = document.querySelector(
          `input[type="range"][data-question-id="${q.id}"]`
        );

        answer = el ? String(el.value) : '';
      } else if (q.type === 'rating') {
        const el = document.querySelector(
          `input[type="radio"][data-question-id="${q.id}"][data-type="rating"]:checked`
        );

        answer = (el && el.value) || '';
      }

      const trimmed = String(answer).trim();
      if (trimmed.length > 0) {
        items.push({ question_id: q.id, answer: trimmed });
      }
    }
    return items;
  };

  const submitResponses = async (token, surveyId, questions) => {
    const responses = collectResponses(questions);
    if (!Array.isArray(responses) || responses.length === 0) {
      throw new Error('Agrega al menos una respuesta válida');
    }

    const body = { token, survey_id: surveyId, responses };
    const resp = await fetch(`${API_BASE_URL}/anonymous/responses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await resp.json().catch(() => ({}));

    if (!resp.ok) {
      const msg = data && data.message ? data.message : 'error_en_envio';
      throw new Error(msg);
    }
    return data;
  };

  const init = async () => {
    const statusEl = $('#resolver-status');
    const formEl = $('#surveyForm');

    const token = qs('token');
    if (!token) {
      if (statusEl) {
        statusEl.textContent = 'Token requerido para resolver la encuesta.';
      }
      return;
    }

    try {
      const payload = await fetchSurveyByToken(token);
      const { survey, questions } = payload;

      // Render title/header
      const container = $('#resolver-container');
      if (container) {
        const header = createEl('div', { class: 'mb-6' });
        header.appendChild(
          createEl('h2', {
            class: 'text-xl font-semibold text-gray-800',
            html: survey.title || 'Encuesta',
          })
        );

        if (survey.description) {
          header.appendChild(
            createEl('p', { class: 'text-gray-600', html: survey.description })
          );
        }
        container.insertBefore(header, formEl);
      }

      // Render questions as steps
      formEl.innerHTML = '';
      questions.forEach((q, idx) => {
        formEl.appendChild(renderQuestion(q, idx, questions.length));
      });
      updateProgress(0, questions.length);

      // Manager submit
      formEl.addEventListener('submit', async e => {
        e.preventDefault();
        try {
          const res = await submitResponses(token, survey.id, questions);
          const box = $('#resolver-container');
          if (box) {
            box.innerHTML = `
              <div class="text-center py-12">
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">¡Gracias por tu respuesta!</h2>
                <p class="text-gray-600">Se registraron ${res.saved_count || 0} respuestas.</p>
              </div>
            `;
          }
        } catch (err) {
          alert((err && err.message) || 'Error al enviar.');
        }
      });
    } catch (e) {
      const msg = (e && e.message) || 'token_invalido';
      if (statusEl) {
        statusEl.textContent = `No se puede cargar la encuesta: ${msg}`;
      }
    }
  };

  document.addEventListener('DOMContentLoaded', init);
})();

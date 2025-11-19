/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

/* global RS */
const EditModal = (() => {
  const modal = document.getElementById('editModal');
  const overlay = document.getElementById('editModalOverlay');
  const panel = document.getElementById('editModalPanel');
  const closeBtn = document.getElementById('editCloseBtn');
  const closeBtn2 = document.getElementById('editCloseBtn2');
  const form = document.getElementById('editSurveyForm');
  const addQuestionBtn = document.getElementById('editAddQuestionBtn');
  const questionsList = document.getElementById('editQuestionsList');

  const idEl = document.getElementById('editSurveyId');
  const titleEl = document.getElementById('editSurveyTitle');
  const descEl = document.getElementById('editSurveyDescription');
  const categorySel = document.getElementById('editSurveyCategoryId');
  const expiresEl = document.getElementById('editSurveyExpiresAt');

  // Ensure RS client is available to avoid runtime ReferenceError
  if (!window.RS || !RS.http) {
    console.error(
      'RS.http no está disponible. Verifica la carga de js/lib/http.js'
    );
    return { init: () => {} };
  }

  const toDatetimeLocal = iso => {
    try {
      if (!iso) {
        return '';
      }

      const d = new Date(iso);
      const pad = n => String(n).padStart(2, '0');
      const yyyy = d.getFullYear();
      const mm = pad(d.getMonth() + 1);
      const dd = pad(d.getDate());
      const hh = pad(d.getHours());
      const mi = pad(d.getMinutes());

      return `${yyyy}-${mm}-${dd}T${hh}:${mi}`;
    } catch (_) {
      return '';
    }
  };

  const open = () => {
    if (!modal || !overlay || !panel) {
      return;
    }

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';

    requestAnimationFrame(() => {
      panel.classList.remove('translate-x-full');
      panel.classList.add('translate-x-0');
    });
  };

  const close = () => {
    if (!modal || !overlay || !panel) {
      return;
    }
    panel.classList.add('translate-x-full');
    panel.classList.remove('translate-x-0');
    setTimeout(() => {
      modal.classList.add('hidden');
      document.body.style.overflow = '';
    }, 250);
  };

  const fillForm = s => {
    idEl.value = s.id;
    titleEl.value = s.title || '';
    descEl.value = s.description || '';
    expiresEl.value = toDatetimeLocal(s.expires_at);
  };

  const createQuestionItem = (q = null) => {
    const el = document.createElement('div');
    el.className = 'border rounded-lg p-4 bg-gray-50';
    el.dataset.questionId = q && q.id ? String(q.id) : '';
    el.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium text-gray-700">Pregunta</span>
        <div class="flex items-center gap-3">
          <label class="text-xs text-gray-600 flex items-center gap-1">
            <input type="checkbox" data-role="required" ${q && q.is_required ? 'checked' : ''} /> Requerida
          </label>
          <button type="button" data-action="remove-question" class="text-red-600 hover:text-red-700 text-sm">
            <i class="fas fa-trash mr-1"></i> Eliminar
          </button>
        </div>
      </div>
      <div class="mt-2">
        <label class="block text-xs text-gray-600">Título de la pregunta<span class="text-red-500">*</span></label>
        <input data-role="title" type="text" class="w-full border rounded px-3 py-2 text-sm" placeholder="Escribe la pregunta" required />
      </div>
      <div class="mt-2">
        <label class="block text-xs text-gray-600">Tipo de pregunta</label>
        <select data-role="type" class="w-full border rounded px-3 py-2 text-sm">
          <option value="text">Texto</option>
          <option value="multiple_choice">Selección múltiple</option>
          <option value="single_choice">Única opción</option>
          <option value="scale">Escala</option>
        </select>
      </div>
      <div data-role="options" class="mt-2 hidden">
        <div data-type="choices" class="hidden">
          <div data-role="choices-list" class="space-y-2"></div>
          <button type="button" data-action="add-choice" class="mt-2 px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded text-xs">Agregar opción</button>
        </div>
        <div data-type="scale" class="hidden flex items-center gap-3">
          <div>
            <label class="block text-xs text-gray-600">Mínimo</label>
            <input data-role="scale-min" type="number" class="w-24 border rounded px-2 py-1 text-sm" value="1" />
          </div>
          <div>
            <label class="block text-xs text-gray-600">Máximo</label>
            <input data-role="scale-max" type="number" class="w-24 border rounded px-2 py-1 text-sm" value="5" />
          </div>
        </div>
      </div>
    `;

    const titleInp = el.querySelector('[data-role="title"]');
    const typeSel = el.querySelector('select[data-role="type"]');
    // const requiredChk = el.querySelector('[data-role="required"]');
    const optionsBox = el.querySelector('[data-role="options"]');
    const choicesBox = el.querySelector('[data-type="choices"]');
    const choicesList = el.querySelector('[data-role="choices-list"]');
    const scaleBox = el.querySelector('[data-type="scale"]');
    const addChoiceBtn = el.querySelector('[data-action="add-choice"]');

    const addChoice = (value = '') => {
      const row = document.createElement('div');
      row.className = 'flex items-center gap-2';
      row.innerHTML = `
        <input type="text" class="w-full border rounded px-3 py-1 text-sm" placeholder="Opción" value="${value}" />
        <button type="button" class="text-red-600 hover:text-red-700 text-xs" data-action="remove-choice"><i class="fas fa-trash"></i></button>
      `;
      choicesList.appendChild(row);
      row
        .querySelector('[data-action="remove-choice"]')
        .addEventListener('click', () => row.remove());
    };

    const renderForType = type => {
      if (type === 'text') {
        optionsBox.classList.add('hidden');
        choicesBox.classList.add('hidden');
        scaleBox.classList.add('hidden');
      } else if (type === 'multiple_choice' || type === 'single_choice') {
        optionsBox.classList.remove('hidden');
        choicesBox.classList.remove('hidden');
        scaleBox.classList.add('hidden');

        if (choicesList.childElementCount === 0) {
          addChoice('Opción 1');
          addChoice('Opción 2');
        }
      } else if (type === 'scale') {
        optionsBox.classList.remove('hidden');
        choicesBox.classList.add('hidden');
        scaleBox.classList.remove('hidden');
      }
    };

    addChoiceBtn.addEventListener('click', () => addChoice(''));
    typeSel.addEventListener('change', e => renderForType(e.target.value));

    // Prefill if existing question
    if (q) {
      titleInp.value = q.text || '';
      typeSel.value = q.type || 'text';
      renderForType(typeSel.value);

      if (q.type === 'multiple_choice' || q.type === 'single_choice') {
        const vals = (q.options && q.options.values) || [];

        if (Array.isArray(vals) && vals.length) {
          choicesList.innerHTML = '';
          vals.forEach(v => addChoice(v));
        }
      } else if (q.type === 'scale') {
        const { min, max } = q.options || {};
        const minEl = el.querySelector('[data-role="scale-min"]');
        const maxEl = el.querySelector('[data-role="scale-max"]');

        if (typeof min === 'number') {
          minEl.value = String(min);
        }
        if (typeof max === 'number') {
          maxEl.value = String(max);
        }
      }
    } else {
      renderForType('text');
    }

    el.querySelector('[data-action="remove-question"]').addEventListener(
      'click',
      async () => {
        const qid = Number(el.dataset.questionId || 0);
        if (qid) {
          try {
            await RS.http.apiFetch(`/questions/${qid}/state`, {
              method: 'PATCH',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ state: false }),
            });
          } catch (err) {
            console.error(err);
            alert('No se pudo eliminar la pregunta');

            return;
          }
        }
        el.remove();
      }
    );

    return el;
  };

  const collectQuestions = () => {
    const items = Array.from(
      questionsList.querySelectorAll('.border.rounded-lg.p-4.bg-gray-50')
    );
    const out = [];

    for (let i = 0; i < items.length; i++) {
      const qEl = items[i];
      const id = Number(qEl.dataset.questionId || 0) || null;
      const title = (
        qEl.querySelector('[data-role="title"]').value || ''
      ).trim();
      const type = qEl.querySelector('[data-role="type"]').value;
      const is_required = !!qEl.querySelector('[data-role="required"]').checked;
      const q = { id, text: title, type, is_required, order_position: i + 1 };

      if (type === 'multiple_choice' || type === 'single_choice') {
        const values = Array.from(
          qEl.querySelectorAll('[data-role="choices-list"] input')
        )
          .map(inp => (inp.value || '').trim())
          .filter(v => v.length > 0);
        q.options = { values, multiple: type === 'multiple_choice' };
      } else if (type === 'scale') {
        const min = Number(qEl.querySelector('[data-role="scale-min"]').value);
        const max = Number(qEl.querySelector('[data-role="scale-max"]').value);
        q.options = { min, max };
      }
      out.push(q);
    }
    return out;
  };

  const loadQuestions = async surveyId => {
    if (!questionsList) {
      return;
    }

    questionsList.innerHTML = '';
    try {
      const qs = await RS.http.apiFetch(`/questions/?survey_id=${surveyId}`, {
        method: 'GET',
      });
      (qs || [])
        .filter(
          q =>
            q &&
            (q.state === true ||
              q.state === null ||
              typeof q.state === 'undefined')
        )
        .forEach(q => questionsList.appendChild(createQuestionItem(q)));
    } catch (err) {
      console.error(err);
      // leave empty
    }
  };

  const fetchSurvey = async id => {
    return RS.http.apiFetch(`/surveys/${id}`, { method: 'GET' });
  };

  const loadCategories = async () => {
    if (!categorySel) {
      return;
    }
    try {
      categorySel.innerHTML = '';
      const rows = await RS.http.apiFetch('/categories/', { method: 'GET' });
      if (!Array.isArray(rows) || rows.length === 0) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'No hay categorías disponibles';
        categorySel.appendChild(opt);
        return;
      }
      for (const c of rows) {
        const opt = document.createElement('option');
        opt.value = String(c.id);
        opt.textContent = c.name;
        categorySel.appendChild(opt);
      }
    } catch (err) {
      console.error('Error al cargar categorías:', err);
      categorySel.innerHTML = '';
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Error al cargar categorías';
      categorySel.appendChild(opt);
    }
  };

  const save = async () => {
    const id = Number(idEl.value);
    if (!id) {
      return;
    }

    const expiresVal = expiresEl.value || null;
    if (expiresVal) {
      const exp = new Date(expiresVal);
      const now = new Date();
      if (exp < now) {
        alert('La fecha de expiración debe ser futura.');
        return;
      }
    }

    const payload = {
      title: titleEl.value.trim(),
      description: descEl.value.trim() || null,
      expires_at: expiresVal,
      // Keep surveys active by default
    };

    if (!payload.title) {
      alert('El título es obligatorio');
      return;
    }

    await RS.http.apiFetch(`/surveys/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    // Persist questions
    const questions = collectQuestions();
    for (const q of questions) {
      if (q.id) {
        await RS.http.apiFetch(`/questions/${q.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            survey_id: id,
            text: q.text,
            type: q.type,
            options: q.options || null,
            is_required: !!q.is_required,
            order_position: q.order_position || 0,
            state: true,
          }),
        });
      } else {
        // new question
        await RS.http.apiFetch('/questions/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            survey_id: id,
            text: q.text,
            type: q.type,
            options: q.options || null,
            is_required: !!q.is_required,
            order_position: q.order_position || 0,
          }),
        });
      }
    }

    alert('Encuesta y preguntas actualizadas');
    close();
    window.location.reload();
  };

  const toggleMenu = btn => {
    const container = btn.closest('.relative');
    const menu = container ? container.querySelector('.survey-menu') : null;
    if (!menu) {
      return;
    }
    // Close other menus
    document.querySelectorAll('.survey-menu').forEach(m => {
      if (m !== menu) {
        m.classList.add('hidden');
      }
    });
    menu.classList.toggle('hidden');
  };

  const closeAllMenus = () => {
    document
      .querySelectorAll('.survey-menu')
      .forEach(m => m.classList.add('hidden'));
  };

  const softDeleteSurvey = async id => {
    return RS.http.apiFetch(`/surveys/${id}/state`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: false }),
    });
  };

  const onDocumentClick = async e => {
    const menuBtn = e.target.closest('.survey-menu-btn');
    if (menuBtn) {
      toggleMenu(menuBtn);

      return;
    }

    const editBtn = e.target.closest('.survey-edit-btn');
    if (editBtn) {
      const id = Number(editBtn.dataset.surveyId);
      closeAllMenus();
      fetchSurvey(id)
        .then(s => {
          fillForm(s);
          return loadQuestions(s.id);
        })
        .then(() => {
          open();
        })
        .catch(err => {
          console.error(err);
          alert('No se pudo cargar la encuesta para editar');
        });
      return;
    }

    const deleteBtn = e.target.closest('.survey-delete-btn');
    if (deleteBtn) {
      const id = Number(deleteBtn.dataset.surveyId);
      closeAllMenus();
      const ok = confirm(
        '¿Deseas eliminar esta encuesta? Se desactivará y no se mostrará.'
      );
      if (!ok) {
        return;
      }
      try {
        await softDeleteSurvey(id);
        alert('Encuesta eliminada');
        window.location.reload();
      } catch (err) {
        console.error(err);
        alert('No se pudo eliminar la encuesta');
      }
      return;
    }

    // Close menu if clicked outside
    if (!e.target.closest('.survey-menu')) {
      closeAllMenus();
    }
  };

  const init = () => {
    if (!modal || !overlay || !panel || !form) {
      return;
    }

    // Avoid selecting past dates in the expiration field
    if (expiresEl) {
      try {
        expiresEl.min = toDatetimeLocal(new Date().toISOString());
      } catch (_) {
        // ignore formatting issues
      }
    }

    document.addEventListener('click', onDocumentClick);

    overlay.addEventListener('click', close);
    if (closeBtn) {
      closeBtn.addEventListener('click', close);
    }
    if (closeBtn2) {
      closeBtn2.addEventListener('click', close);
    }

    form.addEventListener('submit', async e => {
      e.preventDefault();
      try {
        await save();
      } catch (err) {
        console.error(err);
        // eslint-disable-next-line no-alert
        alert(
          err && err.message ? err.message : 'Error al guardar la encuesta'
        );
      }
    });

    if (addQuestionBtn) {
      addQuestionBtn.addEventListener('click', () => {
        if (questionsList) {
          questionsList.appendChild(createQuestionItem());
        }
      });
    }

    // load categories when starting editing modal
    loadCategories();
  };

  return { init };
})();

document.addEventListener('DOMContentLoaded', () => {
  EditModal.init();
});

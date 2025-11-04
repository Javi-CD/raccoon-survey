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
  const RS_ENV = window.RS_ENV || {};
  const RS_CONFIG = window.RS_CONFIG || {};
  const API_BASE_URL = RS_ENV.API_BASE_URL || RS_CONFIG.apiBaseUrl || '';

  const getTeamProfile = async () => {
    const profile = await RS.http.apiFetch('/auth/me', { method: 'GET' });
    return {
      id: profile.id,
      team_id: profile.team_id || (profile.team && profile.team.id) || null,
    };
  };

  const createQuestionItem = (initialType = 'text') => {
    const el = document.createElement('div');
    el.className = 'border rounded-lg p-4 bg-gray-50';
    el.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium text-gray-700">Pregunta</span>
        <button type="button" data-action="remove-question" class="text-red-600 hover:text-red-700 text-sm">
          <i class="fas fa-trash mr-1"></i> Eliminar
        </button>
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

    const typeSel = el.querySelector('select[data-role="type"]');
    const optionsBox = el.querySelector('[data-role="options"]');
    const choicesBox = el.querySelector('[data-type="choices"]');
    const choicesList = el.querySelector('[data-role="choices-list"]');
    const scaleBox = el.querySelector('[data-type="scale"]');
    const addChoiceBtn = el.querySelector('[data-action="add-choice"]');

    function addChoice(value = '') {
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
    }

    function renderForType(type) {
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
    }

    addChoiceBtn.addEventListener('click', () => addChoice(''));
    typeSel.addEventListener('change', e => renderForType(e.target.value));
    renderForType(initialType);

    el.querySelector('[data-action="remove-question"]').addEventListener(
      'click',
      () => {
        el.remove();
      }
    );

    return el;
  };

  const collectQuestions = container => {
    const items = Array.from(
      container.querySelectorAll('.border.rounded-lg.p-4.bg-gray-50')
    );
    const questions = [];

    for (let i = 0; i < items.length; i++) {
      const qEl = items[i];
      const title = (
        qEl.querySelector('[data-role="title"]').value || ''
      ).trim();
      const type = qEl.querySelector('[data-role="type"]').value;
      const q = {
        text: title,
        type,
        is_required: false,
        order_position: i + 1,
      };

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
      questions.push(q);
    }
    return questions;
  };

  const validateSurvey = (title, questions) => {
    const errors = [];
    if (!title || title.trim().length === 0) {
      errors.push('El título de la encuesta es obligatorio.');
    }
    if (!questions || questions.length === 0) {
      errors.push('Agrega al menos una pregunta.');
    }
    for (let i = 0; i < questions.length; i++) {
      const q = questions[i];
      if (!q.text || q.text.trim().length === 0) {
        errors.push(`La pregunta #${i + 1} debe tener título.`);
      }
      if (q.type === 'multiple_choice' || q.type === 'single_choice') {
        const values = (q.options && q.options.values) || [];
        if (!Array.isArray(values) || values.length < 2) {
          errors.push(`La pregunta #${i + 1} necesita al menos 2 opciones.`);
        }
      }
      if (q.type === 'scale') {
        const { min, max } = q.options || {};
        if (
          typeof min !== 'number' ||
          typeof max !== 'number' ||
          isNaN(min) ||
          isNaN(max)
        ) {
          errors.push(
            `La pregunta #${i + 1} debe definir valores numéricos de rango.`
          );
        } else if (min >= max) {
          errors.push(
            `En la pregunta #${i + 1}, el mínimo debe ser menor que el máximo.`
          );
        }
      }
    }
    return errors;
  };

  const createSurveyAndQuestions = async (surveyPayload, state, questions) => {
    const survey = await RS.http.apiFetch('/surveys/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(surveyPayload),
    });

    if (typeof state === 'boolean') {
      await RS.http.apiFetch(`/surveys/${survey.id}/state`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state }),
      });
    }

    for (const q of questions) {
      await RS.http.apiFetch('/questions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          survey_id: survey.id,
          text: q.text,
          type: q.type,
          options: q.options || null,
          is_required: !!q.is_required,
          order_position: q.order_position || 0,
        }),
      });
    }

    return survey.id;
  };

  const bindModal = () => {
    const modal = document.getElementById('modal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const closeBtn2 = document.getElementById('closeModalBtn2');
    const form = document.getElementById('createSurveyForm');
    const addQuestionBtn = document.getElementById('addQuestionBtn');
    const questionsList = document.getElementById('questionsList');
    const saveBtn = document.getElementById('saveSurveyBtn');

    if (!modal || !form || !questionsList) {
      return;
    }

    function open() {
      modal.classList.remove('hidden');
    }
    function close() {
      modal.classList.add('hidden');
    }

    if (openBtn) {
      openBtn.addEventListener('click', open);
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', close);
    }
    if (closeBtn2) {
      closeBtn2.addEventListener('click', close);
    }

    // First question by default
    questionsList.appendChild(createQuestionItem('text'));

    if (addQuestionBtn) {
      addQuestionBtn.addEventListener('click', () => {
        questionsList.appendChild(createQuestionItem('text'));
      });
    }

    form.addEventListener('submit', async e => {
      e.preventDefault();
      try {
        if (saveBtn) {
          saveBtn.disabled = true;
        }
        const title = (
          document.getElementById('surveyTitle').value || ''
        ).trim();
        const description = (
          document.getElementById('surveyDescription').value || ''
        ).trim();
        const status = document.getElementById('surveyStatus').value;
        const state = status === 'active';

        const questions = collectQuestions(questionsList);
        const errors = validateSurvey(title, questions);
        if (errors.length > 0) {
          alert(errors.join('\n'));
          if (saveBtn) {
            saveBtn.disabled = false;
          }
          return;
        }

        const profile = await getTeamProfile();
        if (!profile.team_id) {
          throw new Error('No se encontró el equipo del usuario (team_id).');
        }

        const surveyPayload = {
          title,
          description: description || null,
          team_id: profile.team_id,
          is_anonymous: true,
          created_by_user_id: profile.id || null,
          expires_at: null,
        };

        await createSurveyAndQuestions(surveyPayload, state, questions);
        alert('Encuesta creada correctamente');
        close();
        window.location.reload();
      } catch (err) {
        console.error(err);
        alert(
          err && err.message
            ? err.message
            : 'Ocurrió un error al crear la encuesta'
        );
      } finally {
        if (saveBtn) {
          saveBtn.disabled = false;
        }
      }
    });
  };

  if (!API_BASE_URL) {
    console.warn('API_BASE_URL not available.');
  }

  document.addEventListener('DOMContentLoaded', bindModal);
})();

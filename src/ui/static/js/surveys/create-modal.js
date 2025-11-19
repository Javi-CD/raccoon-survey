/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

/* eslint-disable no-console */
/* eslint-disable no-alert */
/* eslint-disable wrap-iife */

/* global RS */
(function () {
  const RS_ENV = window.RS_ENV || {};
  const RS_CONFIG = window.RS_CONFIG || {};
  const API_BASE_URL = RS_ENV.API_BASE_URL || RS_CONFIG.apiBaseUrl || '';

  const toDatetimeLocalFromDate = d => {
    try {
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
    const overlay = document.getElementById('modalOverlay');
    const panel = document.getElementById('modalPanel');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const closeBtn2 = document.getElementById('closeModalBtn2');
    const teamSelect = document.getElementById('surveyTeamId');
    const categorySelect = document.getElementById('surveyCategoryId');
    const form = document.getElementById('createSurveyForm');
    const addQuestionBtn = document.getElementById('addQuestionBtn');
    const questionsList = document.getElementById('questionsList');
    const questionsToggleBtn = document.getElementById('questionsToggleBtn');
    const questionsToggleIcon = document.getElementById('questionsToggleIcon');
    const saveBtn = document.getElementById('saveSurveyBtn');
    const expiresEl = document.getElementById('surveyExpiresAt');
    const teamArrow = document.getElementById('surveyTeamArrow');
    const categoryArrow = document.getElementById('surveyCategoryArrow');
    const expiresIcon = document.getElementById('surveyExpiresAtIcon');

    if (!modal || !panel || !form || !questionsList) {
      return;
    }

    function open() {
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        panel.classList.remove('translate-x-full');
        panel.classList.add('translate-x-0');
      });
      try {
        document.body.style.overflow = 'hidden';
      } catch (_) {
        void 0;
      }
    }
    function close() {
      panel.classList.add('translate-x-full');
      panel.classList.remove('translate-x-0');
      setTimeout(() => {
        modal.classList.add('hidden');
      }, 300);
      try {
        document.body.style.overflow = '';
      } catch (_) {
        void 0;
      }
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
    if (overlay) {
      overlay.addEventListener('click', close);
    }
    // Initialize Flatpickr for expiration
    try {
      if (window.flatpickr && expiresEl) {
        const cfgTokens = {
          enableTime: true,
          time_24hr: false,
          altInput: true,
          altFormat: 'd/m/Y h:i K',
          dateFormat: 'Y-m-d H:i',
          minuteIncrement: 1,
          locale: 'es',
          disableMobile: true,
        };
        window.flatpickr(expiresEl, cfgTokens);

        if (expiresIcon) {
          expiresIcon.addEventListener('click', () => {
            try {
              expiresEl.focus();
              if (expiresEl._flatpickr) {
                expiresEl._flatpickr.open();
              }
            } catch (_) {
              return;
            }
          });
        }
      }
    } catch (_) {
      // ignore
    }

    // Arrow rotation animation for selects (same pattern as Reportes)
    try {
      const wireArrow = (selectEl, arrowEl) => {
        if (!selectEl || !arrowEl) {
          return;
        }
        const rotateUp = () =>
          arrowEl.classList.add('rotate-180', 'text-primary');
        const rotateDown = () =>
          arrowEl.classList.remove('rotate-180', 'text-primary');
        selectEl.addEventListener('focus', rotateUp);
        selectEl.addEventListener('click', rotateUp);
        selectEl.addEventListener('blur', rotateDown);
        selectEl.addEventListener('change', () => setTimeout(rotateDown, 150));
      };
      wireArrow(teamSelect, teamArrow);
      wireArrow(categorySelect, categoryArrow);

      // Collapse/Expand logic for Questions section (Create)
      (function wireQuestionsCollapse() {
        if (!questionsList || !questionsToggleBtn || !questionsToggleIcon) {
          return;
        }
        let collapsed = false;
        let animating = false;
        questionsList.style.overflow = 'hidden';
        questionsList.style.transition =
          'height 300ms ease, opacity 300ms ease';
        questionsList.style.willChange = 'height, opacity';

        const setIcon = () => {
          questionsToggleIcon.classList.toggle('fa-chevron-up', !collapsed);
          questionsToggleIcon.classList.toggle('fa-chevron-down', collapsed);
          questionsToggleBtn.setAttribute('aria-expanded', String(!collapsed));
        };
        setIcon();

        const expand = () => {
          if (animating) {
            return;
          }
          animating = true;
          questionsList.style.opacity = '0';
          const target = questionsList.scrollHeight;
          questionsList.style.height = '0px';
          requestAnimationFrame(() => {
            questionsList.style.opacity = '1';
            questionsList.style.height = `${target}px`;
          });
        };

        const collapse = () => {
          if (animating) {
            return;
          }
          animating = true;
          const current = questionsList.scrollHeight;
          questionsList.style.height = `${current}px`;
          requestAnimationFrame(() => {
            questionsList.style.opacity = '0';
            questionsList.style.height = '0px';
          });
        };

        questionsList.addEventListener('transitionend', () => {
          animating = false;
          if (!collapsed) {
            questionsList.style.height = 'auto';
            questionsList.style.opacity = '1';
          }
        });

        questionsToggleBtn.addEventListener('click', () => {
          collapsed = !collapsed;
          setIcon();
          if (collapsed) {
            collapse();
          } else {
            expand();
          }
        });
      })();
    } catch (_) {
      // ignore
    }

    // Load teams for the selector
    const loadTeams = async () => {
      if (!teamSelect) {
        return;
      }

      try {
        teamSelect.innerHTML = '';
        const rows = await RS.http.apiFetch('/teams/', { method: 'GET' });

        if (!Array.isArray(rows) || rows.length === 0) {
          const opt = document.createElement('option');
          opt.value = '';
          opt.textContent = 'No hay equipos disponible';
          teamSelect.appendChild(opt);
          return;
        }

        const profile = await getTeamProfile().catch(() => ({ team_id: null }));

        for (const t of rows) {
          const opt = document.createElement('option');
          opt.value = String(t.id);
          opt.textContent = t.name || '';
          teamSelect.appendChild(opt);
        }

        // Preselect the user's computer if it exists in the list
        if (profile && profile.team_id) {
          teamSelect.value = String(profile.team_id);
        }
      } catch (err) {
        console.error('Error al cargar equipos:', err);
        teamSelect.innerHTML = '';
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'Error al cargar equipos';
        teamSelect.appendChild(opt);
      }
    };

    // Load categories for the selector
    const loadCategories = async () => {
      if (!categorySelect) {
        return;
      }

      try {
        categorySelect.innerHTML = '';
        const rows = await RS.http.apiFetch('/categories/', { method: 'GET' });

        if (!Array.isArray(rows) || rows.length === 0) {
          const opt = document.createElement('option');
          opt.value = '';
          opt.textContent = 'No hay categorías disponibles';
          categorySelect.appendChild(opt);
          return;
        }

        for (const c of rows) {
          const opt = document.createElement('option');
          opt.value = String(c.id);
          opt.textContent = c.name;
          categorySelect.appendChild(opt);
        }
      } catch (err) {
        console.error('Error al cargar categorías:', err);
        categorySelect.innerHTML = '';
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = 'Error al cargar categorías';
        categorySelect.appendChild(opt);
      }
    };

    // Default first question
    questionsList.appendChild(createQuestionItem('text'));

    // Load select data when initializing the modal
    loadTeams();
    loadCategories();

    // Prevent selecting past dates
    if (expiresEl) {
      try {
        expiresEl.min = toDatetimeLocalFromDate(new Date());
      } catch (_) {
        // ignore
      }
    }

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
        const expiresAt = (
          document.getElementById('surveyExpiresAt')?.value || ''
        ).trim();
        const teamIdStr = (teamSelect && teamSelect.value) || '';
        const teamId = Number(teamIdStr) || 0;
        const state = true; // save active by default
        const categoryIdStr = (categorySelect && categorySelect.value) || '';

        // Validate expiration is in the future
        if (expiresAt) {
          const exp = new Date(expiresAt);
          const now = new Date();
          if (exp < now) {
            alert('La fecha de expiración debe ser futura.');
            if (saveBtn) {
              saveBtn.disabled = false;
            }
            return;
          }
        }

        const questions = collectQuestions(questionsList);
        const errors = validateSurvey(title, questions);
        if (errors.length > 0) {
          alert(errors.join('\n'));
          if (saveBtn) {
            saveBtn.disabled = false;
          }
          return;
        }
        if (!teamId) {
          alert('Selecciona un equipo para la encuesta.');
          if (saveBtn) {
            saveBtn.disabled = false;
          }
          return;
        }

        if (!categoryIdStr) {
          alert('Selecciona una categoría para la encuesta.');
          if (saveBtn) {
            saveBtn.disabled = false;
          }
          return;
        }

        const profile = await getTeamProfile();

        const surveyPayload = {
          title,
          description: description || null,
          team_id: teamId,
          is_anonymous: true,
          created_by_user_id: profile.id || null,
          expires_at: expiresAt || null,
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

/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

import { qs, el } from '../utils/dom.js';
import {
  buildBackdrop,
  buildDrawerRoot,
  buildDrawerPanel,
  appendToModals,
  closeDrawer,
} from '../utils/drawer.js';
import { fmtState } from '../utils/format.js';
import { http } from '../utils/http.js';

export async function loadTeams() {
  const api = http();
  if (!api) {
    return;
  }
  try {
    const rows = await api.apiFetch('/teams/', { method: 'GET' });
    const tbody = qs('#teamsTableBody');
    if (!tbody) {
      return;
    }
    tbody.innerHTML = '';
    (rows || []).forEach(t => {
      const actionsCell = el(
        'td',
        {
          class: 'px-4 py-2 text-sm text-right space-x-2',
        },
        [
          el(
            'button',
            {
              class:
                'px-2 py-1 rounded border border-gray-300 text-gray-700 hover:bg-gray-100',
              onClick: () => openEditTeamDrawer(t),
            },
            'Editar'
          ),
          el(
            'button',
            {
              class: `${
                t.state
                  ? 'bg-red-600 hover:bg-red-700'
                  : 'bg-green-600 hover:bg-green-700'
              } px-2 py-1 rounded text-white`,
              onClick: () => (t.state ? deleteTeam(t.id) : restoreTeam(t.id)),
            },
            t.state ? 'Eliminar' : 'Restaurar'
          ),
        ]
      );

      const tr = el('tr', {}, [
        el('td', { class: 'px-4 py-2 text-sm text-gray-800' }, t.name || ''),
        el(
          'td',
          { class: 'px-4 py-2 text-sm text-gray-600' },
          t.description || ''
        ),
        el('td', { class: 'px-4 py-2 text-sm' }, fmtState(!!t.state)),
        actionsCell,
      ]);
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error('loadTeams error:', e);
  }
}

export async function openCreateTeamDrawer() {
  const api = http();
  if (!api) {
    console.warn('RS.http no disponible');
    return;
  }

  const root = buildDrawerRoot();
  const panel = buildDrawerPanel();
  const close = () => closeDrawer(root, panel, 300);
  const backdrop = buildBackdrop(close);

  const title = el('h3', {
    class: 'text-lg font-semibold text-gray-800 mb-4',
    text: 'Crear equipo',
  });

  const nameInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'teamName',
    placeholder: 'Nombre del equipo',
  });
  const descInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'teamDesc',
    placeholder: 'Descripción',
  });

  const form = el('div', { class: 'space-y-4' }, [
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Nombre',
      }),
      nameInput,
    ]),
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Descripción',
      }),
      descInput,
    ]),
  ]);

  const actions = el('div', { class: 'mt-6 flex justify-end gap-3' }, [
    el(
      'button',
      {
        class: 'px-4 py-2 rounded border border-gray-300 text-gray-700',
        onClick: () => close(),
      },
      'Cancelar'
    ),
    el(
      'button',
      {
        class: 'px-4 py-2 rounded bg-primary text-white hover:bg-secondary',
        id: 'teamSaveBtn',
      },
      'Guardar'
    ),
  ]);

  panel.appendChild(title);
  panel.appendChild(form);
  panel.appendChild(actions);

  root.appendChild(backdrop);
  root.appendChild(panel);
  appendToModals(root);

  requestAnimationFrame(() => {
    panel.classList.remove('translate-x-full');
    panel.classList.add('translate-x-0');
  });

  qs('#teamSaveBtn', panel).addEventListener('click', async () => {
    const name = (nameInput.value || '').trim();
    const description = (descInput.value || '').trim();
    if (!name) {
      alert('El nombre es obligatorio');
      return;
    }
    try {
      await api.apiFetch('/teams/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description }),
      });
      close();
      await loadTeams();
    } catch (e) {
      alert(e && e.message ? e.message : 'Error creando equipo');
    }
  });
}

async function openEditTeamDrawer(team) {
  const api = http();
  if (!api) {
    console.warn('RS.http no disponible');
    return;
  }

  const root = buildDrawerRoot();
  const panel = buildDrawerPanel();
  const close = () => closeDrawer(root, panel, 300);
  const backdrop = buildBackdrop(close);

  const title = el('h3', {
    class: 'text-lg font-semibold text-gray-800 mb-4',
    text: 'Editar equipo',
  });

  const nameInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editTeamName',
    placeholder: 'Nombre del equipo',
    value: team.name || '',
  });
  const descInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editTeamDesc',
    placeholder: 'Descripción',
    value: team.description || '',
  });

  const form = el('div', { class: 'space-y-4' }, [
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Nombre',
      }),
      nameInput,
    ]),
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Descripción',
      }),
      descInput,
    ]),
  ]);

  const actions = el('div', { class: 'mt-6 flex justify-end gap-3' }, [
    el(
      'button',
      {
        class: 'px-4 py-2 rounded border border-gray-300 text-gray-700',
        onClick: () => close(),
      },
      'Cancelar'
    ),
    el(
      'button',
      {
        class: 'px-4 py-2 rounded bg-primary text-white hover:bg-secondary',
        id: 'editTeamSaveBtn',
      },
      'Guardar cambios'
    ),
  ]);

  panel.appendChild(title);
  panel.appendChild(form);
  panel.appendChild(actions);

  root.appendChild(backdrop);
  root.appendChild(panel);
  appendToModals(root);

  requestAnimationFrame(() => {
    panel.classList.remove('translate-x-full');
    panel.classList.add('translate-x-0');
  });

  qs('#editTeamSaveBtn', panel).addEventListener('click', async () => {
    const name = (nameInput.value || '').trim();
    const description = (descInput.value || '').trim();
    if (!name) {
      alert('El nombre es obligatorio');
      return;
    }
    try {
      await api.apiFetch(`/teams/${team.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description }),
      });
      close();
      await loadTeams();
    } catch (e) {
      alert(e && e.message ? e.message : 'Error actualizando equipo');
    }
  });
}

async function deleteTeam(teamId) {
  const api = http();
  if (!api) {
    return;
  }
  const ok = window.confirm('¿Eliminar equipo? Se marcará como inactivo.');
  if (!ok) {
    return;
  }
  try {
    await api.apiFetch(`/teams/${teamId}/state`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: false }),
    });
    await loadTeams();
  } catch (e) {
    alert(e && e.message ? e.message : 'Error eliminando equipo');
  }
}

async function restoreTeam(teamId) {
  const api = http();
  if (!api) {
    return;
  }
  try {
    await api.apiFetch(`/teams/${teamId}/state`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: true }),
    });
    await loadTeams();
  } catch (e) {
    alert(e && e.message ? e.message : 'Error restaurando equipo');
  }
}

export function wireTeamCreateButton() {
  const btn = qs('#createTeamBtn');
  if (!btn) {
    console.warn('createTeamBtn no encontrado');
    return;
  }
  btn.addEventListener('click', () => openCreateTeamDrawer());
}

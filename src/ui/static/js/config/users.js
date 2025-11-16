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

export async function loadUsers() {
  const api = http();
  if (!api) {
    return;
  }
  try {
    const rows = await api.apiFetch('/users/', { method: 'GET' });
    const tbody = qs('#usersTableBody');
    if (!tbody) {
      return;
    }
    tbody.innerHTML = '';
    (rows || []).forEach(u => {
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
              onClick: () => openEditUserDrawer(u),
            },
            'Editar'
          ),
          el(
            'button',
            {
              class: 'px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700',
              onClick: () => deleteUser(u.id),
            },
            'Eliminar'
          ),
        ]
      );

      const tr = el('tr', {}, [
        el('td', { class: 'px-4 py-2 text-sm text-gray-800' }, u.name || ''),
        el('td', { class: 'px-4 py-2 text-sm text-gray-600' }, u.email || ''),
        el(
          'td',
          { class: 'px-4 py-2 text-sm text-gray-600' },
          (u.role && u.role.name) || ''
        ),
        el(
          'td',
          { class: 'px-4 py-2 text-sm text-gray-600' },
          (u.team && u.team.name) || ''
        ),
        el('td', { class: 'px-4 py-2 text-sm' }, fmtState(!!u.state)),
        actionsCell,
      ]);
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error('loadUsers error:', e);
  }
}

async function fetchRoles() {
  const api = http();
  if (!api) {
    return [];
  }
  try {
    return await api.apiFetch('/roles/', { method: 'GET' });
  } catch (_) {
    return [];
  }
}

async function fetchTeams() {
  const api = http();
  if (!api) {
    return [];
  }
  try {
    return await api.apiFetch('/teams/', { method: 'GET' });
  } catch (_) {
    return [];
  }
}

export async function openCreateUserDrawer() {
  const api = http();
  if (!api) {
    console.warn('RS.http no disponible');
    return;
  }

  const roles = await fetchRoles();
  const teams = await fetchTeams();

  const root = buildDrawerRoot();
  const panel = buildDrawerPanel();
  const close = () => closeDrawer(root, panel, 300);
  const backdrop = buildBackdrop(close);

  const title = el('h3', {
    class: 'text-lg font-semibold text-gray-800 mb-4',
    text: 'Crear usuario',
  });

  const nameInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'userName',
    placeholder: 'Nombre',
  });
  const emailInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'userEmail',
    placeholder: 'Email',
    type: 'email',
  });
  const passInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'userPass',
    placeholder: 'Contraseña',
    type: 'password',
  });

  const roleSelect = el('select', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'userRole',
  });
  roleSelect.appendChild(el('option', { value: '', text: 'Selecciona rol' }));
  roles.forEach(r =>
    roleSelect.appendChild(el('option', { value: String(r.id), text: r.name }))
  );

  const teamSelect = el('select', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'userTeam',
  });
  teamSelect.appendChild(
    el('option', { value: '', text: 'Selecciona equipo' })
  );
  teams.forEach(t =>
    teamSelect.appendChild(el('option', { value: String(t.id), text: t.name }))
  );

  const form = el('div', { class: 'space-y-4' }, [
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Nombre',
      }),
      nameInput,
    ]),
    el('div', {}, [
      el('label', { class: 'block text-sm text-gray-700 mb-1', text: 'Email' }),
      emailInput,
    ]),
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Contraseña',
      }),
      passInput,
    ]),
    el('div', {}, [
      el('label', { class: 'block text-sm text-gray-700 mb-1', text: 'Rol' }),
      roleSelect,
    ]),
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Equipo',
      }),
      teamSelect,
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
        id: 'userSaveBtn',
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

  // Animate in
  requestAnimationFrame(() => {
    panel.classList.remove('translate-x-full');
    panel.classList.add('translate-x-0');
  });

  // Save handler
  qs('#userSaveBtn', panel).addEventListener('click', async () => {
    const name = (nameInput.value || '').trim();
    const email = (emailInput.value || '').trim().toLowerCase();
    const password = passInput.value || '';
    const role_id = roleSelect.value
      ? parseInt(roleSelect.value, 10)
      : undefined;
    const team_id = teamSelect.value
      ? parseInt(teamSelect.value, 10)
      : undefined;

    if (!name) {
      alert('El nombre es obligatorio');
      return;
    }
    if (!email) {
      alert('El email es obligatorio');
      return;
    }
    if (!password) {
      alert('La contraseña es obligatoria');
      return;
    }

    try {
      await api.apiFetch('/users/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role_id, team_id }),
      });
      close();
      await loadUsers();
    } catch (e) {
      alert(e && e.message ? e.message : 'Error creando usuario');
    }
  });
}

async function openEditUserDrawer(user) {
  const api = http();
  if (!api) {
    console.warn('RS.http no disponible');
    return;
  }

  const roles = await fetchRoles();
  const teams = await fetchTeams();

  const root = buildDrawerRoot();
  const panel = buildDrawerPanel();
  const close = () => closeDrawer(root, panel, 300);
  const backdrop = buildBackdrop(close);

  const title = el('h3', {
    class: 'text-lg font-semibold text-gray-800 mb-4',
    text: 'Editar usuario',
  });

  const nameInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editUserName',
    placeholder: 'Nombre',
    value: user.name || '',
  });
  const emailInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editUserEmail',
    placeholder: 'Email',
    type: 'email',
    value: user.email || '',
  });
  const passInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editUserPass',
    placeholder: 'Nueva contraseña (opcional)',
    type: 'password',
  });

  const roleSelect = el('select', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editUserRole',
  });
  roleSelect.appendChild(el('option', { value: '', text: 'Selecciona rol' }));
  roles.forEach(r =>
    roleSelect.appendChild(el('option', { value: String(r.id), text: r.name }))
  );
  const roleId =
    typeof user.role_id !== 'undefined' && user.role_id !== null
      ? user.role_id
      : user.role && user.role.id;
  if (typeof roleId !== 'undefined' && roleId !== null) {
    roleSelect.value = String(roleId);
  }

  const teamSelect = el('select', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editUserTeam',
  });
  teamSelect.appendChild(
    el('option', { value: '', text: 'Selecciona equipo' })
  );
  teams.forEach(t =>
    teamSelect.appendChild(el('option', { value: String(t.id), text: t.name }))
  );
  const teamId =
    typeof user.team_id !== 'undefined' && user.team_id !== null
      ? user.team_id
      : user.team && user.team.id;
  if (typeof teamId !== 'undefined' && teamId !== null) {
    teamSelect.value = String(teamId);
  }

  const form = el('div', { class: 'space-y-4' }, [
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Nombre',
      }),
      nameInput,
    ]),
    el('div', {}, [
      el('label', { class: 'block text-sm text-gray-700 mb-1', text: 'Email' }),
      emailInput,
    ]),
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Nueva contraseña (opcional)',
      }),
      passInput,
    ]),
    el('div', {}, [
      el('label', { class: 'block text-sm text-gray-700 mb-1', text: 'Rol' }),
      roleSelect,
    ]),
    el('div', {}, [
      el('label', {
        class: 'block text-sm text-gray-700 mb-1',
        text: 'Equipo',
      }),
      teamSelect,
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
        id: 'editUserSaveBtn',
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

  // Animate in
  requestAnimationFrame(() => {
    panel.classList.remove('translate-x-full');
    panel.classList.add('translate-x-0');
  });

  // Save handler
  qs('#editUserSaveBtn', panel).addEventListener('click', async () => {
    const name = (nameInput.value || '').trim();
    const email = (emailInput.value || '').trim().toLowerCase();
    const password = passInput.value || '';
    const role_id = roleSelect.value
      ? parseInt(roleSelect.value, 10)
      : undefined;
    const team_id = teamSelect.value
      ? parseInt(teamSelect.value, 10)
      : undefined;

    if (!name) {
      alert('El nombre es obligatorio');
      return;
    }
    if (!email) {
      alert('El email es obligatorio');
      return;
    }

    const payload = { name, email, role_id, team_id };
    if (password) {
      payload.password = password;
    }

    try {
      await api.apiFetch(`/users/${user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      close();
      await loadUsers();
    } catch (e) {
      alert(e && e.message ? e.message : 'Error actualizando usuario');
    }
  });
}

async function deleteUser(userId) {
  const api = http();
  if (!api) {
    return;
  }
  const ok = window.confirm('¿Eliminar usuario? Se marcará como inactivo.');
  if (!ok) {
    return;
  }
  try {
    await api.apiFetch(`/users/${userId}/state`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: false }),
    });
    await loadUsers();
  } catch (e) {
    alert(e && e.message ? e.message : 'Error eliminando usuario');
  }
}

export function wireUserCreateButton() {
  const btn = qs('#createUserBtn');
  if (!btn) {
    console.warn('createUserBtn no encontrado');
    return;
  }
  btn.addEventListener('click', () => openCreateUserDrawer());
}

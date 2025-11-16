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

export async function loadCategories() {
  const api = http();
  if (!api) {
    return;
  }

  try {
    const rows = await api.apiFetch('/categories/', { method: 'GET' });
    const tbody = qs('#categoriesTableBody');
    if (!tbody) {
      return;
    }

    tbody.innerHTML = '';
    (rows || []).forEach(c => {
      const actionsCell = el(
        'td',
        { class: 'px-4 py-2 text-sm text-right space-x-2' },
        [
          el(
            'button',
            {
              class:
                'px-2 py-1 rounded border border-gray-300 text-gray-700 hover:bg-gray-100',
              onClick: () => openEditCategoryDrawer(c),
            },
            'Editar'
          ),

          el(
            'button',
            {
              class: `${
                c.state
                  ? 'bg-red-600 hover:bg-red-700'
                  : 'bg-green-600 hover:bg-green-700'
              } px-2 py-1 rounded text-white`,
              onClick: () =>
                c.state ? deleteCategory(c.id) : restoreCategory(c.id),
            },
            c.state ? 'Eliminar' : 'Restaurar'
          ),
        ]
      );

      const tr = el('tr', {}, [
        el('td', { class: 'px-4 py-2 text-sm text-gray-800' }, c.name || ''),
        el(
          'td',
          { class: 'px-4 py-2 text-sm text-gray-600' },
          c.description || ''
        ),
        el('td', { class: 'px-4 py-2 text-sm' }, fmtState(!!c.state)),
        actionsCell,
      ]);
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error('loadCategories error:', e);
  }
}

const openEditCategoryDrawer = async category => {
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
    text: 'Editar categoría',
  });

  const nameInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editCategoryName',
    placeholder: 'Nombre de la categoría',
    value: category.name || '',
  });
  const descInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'editCategoryDesc',
    placeholder: 'Descripción',
    value: category.description || '',
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
        id: 'editCategorySaveBtn',
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

  qs('#editCategorySaveBtn', panel).addEventListener('click', async () => {
    const name = (nameInput.value || '').trim();
    const description = (descInput.value || '').trim();
    if (!name) {
      alert('El nombre es obligatorio');
      return;
    }
    try {
      await api.apiFetch(`/categories/${category.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description }),
      });
      close();
      await loadCategories();
    } catch (e) {
      alert(e && e.message ? e.message : 'Error actualizando categoría');
    }
  });
};

const deleteCategory = async categoryId => {
  const api = http();
  if (!api) {
    return;
  }

  try {
    await api.apiFetch(`/categories/${categoryId}/state`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: false }),
    });

    await loadCategories();
  } catch (e) {
    alert(e && e.message ? e.message : 'Error eliminando categoría');
  }
};

const restoreCategory = async categoryId => {
  const api = http();
  if (!api) {
    return;
  }

  try {
    await api.apiFetch(`/categories/${categoryId}/state`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: true }),
    });

    await loadCategories();
  } catch (e) {
    alert(e && e.message ? e.message : 'Error restaurando categoría');
  }
};

export async function openCreateCategoryDrawer() {
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
    text: 'Crear categoría',
  });

  const nameInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'categoryName',
    placeholder: 'Nombre de la categoría',
  });
  const descInput = el('input', {
    class: 'w-full border border-gray-300 rounded px-3 py-2',
    id: 'categoryDesc',
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
        id: 'categorySaveBtn',
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

  qs('#categorySaveBtn', panel).addEventListener('click', async () => {
    const name = (nameInput.value || '').trim();
    const description = (descInput.value || '').trim();
    if (!name) {
      alert('El nombre es obligatorio');
      return;
    }

    try {
      await api.apiFetch('/categories/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description }),
      });
      close();

      await loadCategories();
    } catch (e) {
      alert(e && e.message ? e.message : 'Error creando categoría');
    }
  });
}

export function wireCategoryCreateButton() {
  const btn = qs('#createCategoryBtn');
  if (!btn) {
    return;
  }

  btn.addEventListener('click', () => openCreateCategoryDrawer());
}

export default {
  loadCategories,
  openCreateCategoryDrawer,
  wireCategoryCreateButton,
};

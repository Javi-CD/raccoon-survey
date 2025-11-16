/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

import { qs } from './dom.js';

export function buildBackdrop(onClose) {
  const backdrop = document.createElement('div');
  backdrop.className =
    'fixed inset-0 bg-black bg-opacity-10 z-40 pointer-events-auto';
  backdrop.addEventListener('click', evt => {
    if (evt.target === backdrop) {
      if (onClose) {
        onClose();
      }
    }
  });
  return backdrop;
}

export function buildDrawerRoot() {
  const root = document.createElement('div');
  root.className = 'fixed inset-0 z-50 pointer-events-none';
  return root;
}

export function buildDrawerPanel() {
  const panel = document.createElement('div');
  panel.className =
    'pointer-events-auto fixed right-0 top-0 h-full w-full sm:w-[420px] bg-white shadow-xl p-6 overflow-y-auto z-50 transform transition-transform duration-300 ease-in-out translate-x-full';
  return panel;
}

export function appendToModals(node) {
  const host = qs('#configModals');
  if (host) {
    host.classList.remove('hidden');
    host.appendChild(node);
  } else {
    document.body.appendChild(node);
  }
}

export function closeDrawer(root, panel, durationMs = 300) {
  try {
    if (panel) {
      panel.classList.remove('translate-x-0');
      panel.classList.add('translate-x-full');
    }
    requestAnimationFrame(() => {
      setTimeout(() => {
        if (root && root.parentNode) {
          root.parentNode.removeChild(root);
        }
        const host = qs('#configModals');
        if (host && host.children.length === 0) {
          host.classList.add('hidden');
        }
      }, durationMs);
    });
  } catch (_) {
    // noop
  }
}

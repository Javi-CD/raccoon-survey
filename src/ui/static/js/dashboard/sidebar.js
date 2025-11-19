/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

/* global RS */
document.addEventListener('DOMContentLoaded', async () => {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  const userBtn = document.getElementById('userBtn');
  const sidebarNameEl = document.getElementById('sidebarUserName');
  const navbarNameSpan = userBtn ? userBtn.querySelector('span') : null;

  const openSidebar = () => {
    try {
      if (sidebar && overlay) {
        sidebar.classList.remove('translate-x-full');
        overlay.classList.remove('hidden');
      }
    } catch (_) {
      void 0;
    }
  };

  const closeSidebar = () => {
    try {
      if (sidebar && overlay) {
        sidebar.classList.add('translate-x-full');
        overlay.classList.add('hidden');
      }
    } catch (_) {
      void 0;
    }
  };

  try {
    if (userBtn) {
      userBtn.addEventListener('click', openSidebar);
    }
    if (overlay) {
      overlay.addEventListener('click', closeSidebar);
    }
    if (sidebar) {
      const links = sidebar.querySelectorAll('a');
      links.forEach(link => {
        link.addEventListener('click', () => {
          closeSidebar();
        });
      });
    }
  } catch (_) {
    void 0;
  }

  try {
    const profile = await RS.http.apiFetch('/auth/me', { method: 'GET' });
    const name = (profile && profile.name) || 'Usuario';
    const role = (profile && profile.role) || '';

    if (sidebarNameEl) {
      sidebarNameEl.textContent = name;
    }
    if (navbarNameSpan) {
      navbarNameSpan.textContent = name;
    }

    try {
      if (String(role).toLowerCase() === 'admin') {
        document.querySelectorAll('[data-nav="config"]').forEach(el => {
          el.style.display = 'inline';
        });
      }
    } catch (_) {
      void 0;
    }
  } catch (_) {
    void 0;
  }
});

/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

export function enforceAdminConfigGate() {
  try {
    const cfgEl = document.querySelector('meta[name="rs-config"]');
    const apiBase = (cfgEl && cfgEl.dataset && cfgEl.dataset.apiBaseUrl) || '';
    const homeUrl = (cfgEl && cfgEl.dataset && cfgEl.dataset.homeUrl) || '/';
    const loginUrl =
      (cfgEl && cfgEl.dataset && cfgEl.dataset.loginUrl) || '/login';

    const getSS = k => {
      try {
        return sessionStorage.getItem(k) || '';
      } catch (_) {
        return '';
      }
    };

    const cookieVal = name => {
      try {
        const pref = `${name}=`;
        const raw = document.cookie.split(';').map(s => s.trim());
        const hit = raw.find(c => c.startsWith(pref));
        return hit ? decodeURIComponent(hit.slice(pref.length)) : '';
      } catch (_) {
        return '';
      }
    };

    const access = getSS('rs_access_token') || cookieVal('rs_access_token');
    if (!apiBase || !access) {
      window.location.href = loginUrl;
      return;
    }

    fetch(`${apiBase}/auth/me`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `Bearer ${access}`,
      },
      credentials: 'include',
    })
      .then(r => (r && r.ok ? r.json() : null))
      .then(profile => {
        if (!(profile && profile.role === 'admin')) {
          window.location.href = homeUrl;
        }
      })
      .catch(() => {
        window.location.href = homeUrl;
      });
  } catch (_) {
    // If something goes wrong, fail closed
    window.location.href = '/';
  }
}

// Execute immediately on module load for the Config page
enforceAdminConfigGate();

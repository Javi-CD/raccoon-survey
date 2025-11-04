/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

(() => {
  const cfg = window.RS_CONFIG || {};
  const API_BASE_URL = cfg.apiBaseUrl || '';

  const get = k => {
    try {
      return sessionStorage.getItem(k) || '';
    } catch (_) {
      return '';
    }
  };

  const set = (k, v) => {
    try {
      sessionStorage.setItem(k, v);
    } catch (_) {
      void 0;
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

  if (!get('rs_access_token')) {
    const ca = cookieVal('rs_access_token');
    if (ca) {
      set('rs_access_token', ca);
    }
  }
  if (!get('rs_refresh_token')) {
    const cr = cookieVal('rs_refresh_token');
    if (cr) {
      set('rs_refresh_token', cr);
    }
  }

  const access = get('rs_access_token');
  const refresh = get('rs_refresh_token');

  if (!access && !refresh) {
    window.location.href = cfg.loginUrl || '/login';
    return;
  }

  fetch(`${API_BASE_URL}/auth/me`, {
    method: 'GET',
    headers: { Accept: 'application/json', Authorization: `Bearer ${access}` },
    credentials: 'include',
  })
    .then(r => {
      if (r && r.ok) {
        return true;
      }
      if (!refresh) {
        window.location.href = cfg.loginUrl || '/login';

        return false;
      }

      return fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refresh}`,
        },
        credentials: 'include',
      })
        .then(rr => (rr && rr.ok ? rr.json() : null))
        .then(data => {
          if (!(data && data.access_token)) {
            window.location.href = cfg.loginUrl || '/login';

            return false;
          }

          set('rs_access_token', data.access_token);
          try {
            document.cookie = `rs_access_token=${encodeURIComponent(
              data.access_token
            )}; Max-Age=900; Path=/; SameSite=Lax`;
          } catch (_) {
            void 0;
          }
          return true;
        });
    })
    .catch(() => {
      window.location.href = cfg.loginUrl || '/login';
    });
})();

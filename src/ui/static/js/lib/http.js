/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

(() => {
  window.RS = window.RS || {};
  const cfg = window.RS_CONFIG || {};
  const API_BASE_URL = cfg.apiBaseUrl || '';

  const get = k => {
    try {
      return window.sessionStorage.getItem(k) || '';
    } catch (_) {
      return '';
    }
  };

  const set = (k, v) => {
    try {
      window.sessionStorage.setItem(k, v);
    } catch (_) { void 0; }
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

  const setCookie = (name, value, maxAgeSec = 900) => {
    try {
      document.cookie = `${name}=${encodeURIComponent(value)}; Max-Age=${Number(maxAgeSec)}; Path=/; SameSite=Lax`;
    } catch (_) { void 0; }
  };

  const getAccessToken = () => {
    let a = get('rs_access_token');
    if (!a) {a = cookieVal('rs_access_token');}
    return a || '';
  };

  const getRefreshToken = () => {
    let r = get('rs_refresh_token');
    if (!r) {r = cookieVal('rs_refresh_token');}
    return r || '';
  };
  
  const setAccessToken = token => {
    if (!token) {return;}
    set('rs_access_token', token);
    setCookie('rs_access_token', token, 900);
  };

  const refreshIfNeeded = async () => {
    const refresh = getRefreshToken();
    if (!refresh) {return null;}
    try {
      const resp = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refresh}`,
        },
        credentials: 'include',
      });
      if (!resp || !resp.ok) {return null;}
      const data = await resp.json().catch(() => null);
      const token = data && data.access_token ? data.access_token : null;
      if (token) {
        setAccessToken(token);
        return token;
      }
      return null;
    } catch (_) {
      return null;
    }
  };

  const apiFetch = async (path, options = {}) => {
    const url = path.startsWith('http') ? path : `${API_BASE_URL}${path}`;
    const headers = Object.assign({ Accept: 'application/json' }, options.headers || {});
    const access = getAccessToken();
    if (access) {headers.Authorization = `Bearer ${access}`;}

    let resp = await fetch(url, Object.assign({}, options, { headers, credentials: 'include' }));

    if (resp && resp.status === 401) {
      const newAccess = await refreshIfNeeded();
      if (newAccess) {
        headers.Authorization = `Bearer ${newAccess}`;
        resp = await fetch(url, Object.assign({}, options, { headers, credentials: 'include' }));
      }
    }

    if (!resp || !resp.ok) {
      let msg = 'error';
      try {
        const data = await resp.json();
        msg = data && data.message ? data.message : msg;
      } catch (_) {
        try {
          msg = await resp.text();
        } catch (_) { void 0; }
      }
      const err = new Error(msg);
      err.status = resp ? resp.status : 0;
      throw err;
    }

    const ct = (resp.headers && resp.headers.get && resp.headers.get('Content-Type')) || '';
    if (options.responseType === 'blob' || ct.includes('text/csv')) {
      return resp.blob();
    }
    if (ct.includes('application/json')) {
      return resp.json();
    }
    return resp.text();
  };

  window.RS.http = {
    apiFetch,
    getAccessToken,
    getRefreshToken,
    refreshIfNeeded,
  };
})();
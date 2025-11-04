/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

(() => {
  const el = document.querySelector('meta[name="rs-config"]');
  const cfg = el
    ? {
        apiBaseUrl: el.dataset.apiBaseUrl || '',
        loginUrl: el.dataset.loginUrl || '/login',
        homeUrl: el.dataset.homeUrl || '/',
      }
    : { apiBaseUrl: '', loginUrl: '/login', homeUrl: '/' };
  window.RS_CONFIG = cfg;
})();

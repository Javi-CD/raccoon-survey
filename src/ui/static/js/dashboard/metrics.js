/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

document.addEventListener('DOMContentLoaded', () => {
  const cfg = window.RS_CONFIG || {};
  const API_BASE_URL = cfg.apiBaseUrl || '';

  const get = k => {
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

  let access = get('rs_access_token');
  if (!access) {
    access = cookieVal('rs_access_token');
  }

  const totalEl = document.getElementById('totalSurveys');
  const activeEl = document.getElementById('activeUsers');
  const respEl = document.getElementById('responsesToday');
  const repEl = document.getElementById('reportsGenerated');

  fetch(`${API_BASE_URL}/metrics/dashboard`, {
    method: 'GET',
    headers: { Accept: 'application/json', Authorization: `Bearer ${access}` },
    credentials: 'include',
  })
    .then(r => (r && r.ok ? r.json() : null))
    .then(data => {
      if (!data) {
        // Point out that we finish even if there is no valid data
        try {
          if (window.RS && typeof window.RS.dataReady === 'function') {
            window.RS.dataReady();
          }
        } catch (_) {
          /* noop */
        }
        return;
      }

      try {
        totalEl.textContent = data.cards?.total_surveys ?? '0';
        activeEl.textContent = data.cards?.active_users ?? '0';
        respEl.textContent = data.cards?.responses_today ?? '0';
        repEl.textContent = data.cards?.reports_generated ?? '0';
      } catch (_) {
        void 0;
      }

      try {
        const week = data.charts?.responses_by_week || { labels: [], data: [] };
        const bc = window.RSCharts?.barChart;
        if (bc) {
          bc.data.labels = week.labels || [];
          bc.data.datasets[0].data = week.data || [];
          bc.update();
        }
      } catch (_) {
        void 0;
      }

      try {
        const dist = data.charts?.surveys_distribution || {
          labels: [],
          data: [],
        };
        const pc = window.RSCharts?.pieChart;
        if (pc) {
          pc.data.labels = dist.labels || [];
          pc.data.datasets[0].data = dist.data || [];
          pc.update();
        }
      } catch (_) {
        void 0;
      }
    })
    .catch(() => {
      void 0;
    })
    .finally(() => {
      try {
        if (window.RS && typeof window.RS.dataReady === 'function') {
          window.RS.dataReady();
        }
      } catch (_) {
        /* noop */
      }
    });
});

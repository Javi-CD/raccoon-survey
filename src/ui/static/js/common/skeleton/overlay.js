import {
  buildDashboardSkeleton,
  buildSurveysSkeleton,
  buildReportsSkeleton,
  buildConfigSkeleton,
  buildGenericSkeleton,
} from './builders.js';
import { qs, el } from './dom.js';
import { getPageName } from './page.js';

export const createOverlay = () => {
  const header = qs('header') || qs('#navbar');
  const headerHeight = header ? header.offsetHeight : 0;
  const overlay = el('div', 'skeleton-overlay');
  overlay.style.setProperty('--skeleton-top', `${headerHeight}px`);
  const container = el('div', 'skeleton-container');

  const page = getPageName();
  switch (page) {
    case 'dashboard':
      buildDashboardSkeleton(container);
      break;
    case 'surveys':
      buildSurveysSkeleton(container);
      break;
    case 'reports':
      buildReportsSkeleton(container);
      break;
    case 'config':
      buildConfigSkeleton(container);
      break;
    case 'home':
      buildGenericSkeleton(container);
      break;
    case 'login': {
      const title = el('div', 'skeleton-line tall');
      title.style.width = '32%';
      container.appendChild(title);

      const card = el('div', 'skeleton-block skeleton-login-card');
      container.appendChild(card);

      for (let i = 0; i < 5; i += 1) {
        const line = el('div', 'skeleton-line');
        line.style.width = `${55 + Math.floor(Math.random() * 35)}%`;
        container.appendChild(line);
      }
      break;
    }
    default:
      buildGenericSkeleton(container);
  }

  const status = el('div', 'skeleton-status');
  status.textContent = 'Cargando datos…';
  container.appendChild(status);

  overlay.appendChild(container);
  document.body.appendChild(overlay);
  return overlay;
};

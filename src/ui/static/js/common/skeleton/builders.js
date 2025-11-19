import { el } from './dom.js';

export const buildDashboardSkeleton = container => {
  const title = el('div', 'skeleton-line tall');
  title.style.width = '36%';
  container.appendChild(title);

  const cards = el('div', 'skeleton-grid sm-2 lg-4');
  for (let i = 0; i < 4; i += 1) {
    const card = el('div', 'skeleton-block skeleton-card');
    cards.appendChild(card);
  }
  container.appendChild(cards);

  const chart = el('div', 'skeleton-block skeleton-chart');
  container.appendChild(chart);

  for (let i = 0; i < 4; i += 1) {
    const line = el('div', 'skeleton-line');
    line.style.width = `${50 + Math.floor(Math.random() * 40)}%`;
    container.appendChild(line);
  }
};

export const buildSurveysSkeleton = container => {
  const title = el('div', 'skeleton-line tall');
  title.style.width = '42%';
  container.appendChild(title);

  const header = el('div', 'skeleton-block skeleton-table-header');
  container.appendChild(header);

  for (let i = 0; i < 8; i += 1) {
    const row = el('div', 'skeleton-block skeleton-table-row');
    container.appendChild(row);
  }

  const actions = el('div', 'skeleton-actions');
  const btn1 = el('div', 'skeleton-line skeleton-btn');
  const btn2 = el('div', 'skeleton-line skeleton-btn');
  actions.appendChild(btn1);
  actions.appendChild(btn2);
  container.appendChild(actions);
};

export const buildReportsSkeleton = container => {
  const title = el('div', 'skeleton-line tall');
  title.style.width = '34%';
  container.appendChild(title);

  const grid = el('div', 'skeleton-grid sm-2');
  for (let i = 0; i < 2; i += 1) {
    const chart = el('div', 'skeleton-block skeleton-chart');
    grid.appendChild(chart);
  }
  container.appendChild(grid);
};

export const buildConfigSkeleton = container => {
  const title = el('div', 'skeleton-line tall');
  title.style.width = '38%';
  container.appendChild(title);

  for (let i = 0; i < 5; i += 1) {
    const line = el('div', 'skeleton-line');
    line.style.width = `${55 + Math.floor(Math.random() * 35)}%`;
    container.appendChild(line);
  }

  const tableHeader = el('div', 'skeleton-block skeleton-table-header');
  container.appendChild(tableHeader);
  for (let i = 0; i < 6; i += 1) {
    const row = el('div', 'skeleton-block skeleton-table-row');
    container.appendChild(row);
  }
};

export const buildGenericSkeleton = container => {
  const title = el('div', 'skeleton-line tall');
  title.style.width = '40%';
  container.appendChild(title);

  const block1 = el('div', 'skeleton-block');
  container.appendChild(block1);
  for (let i = 0; i < 6; i += 1) {
    const line = el('div', 'skeleton-line');
    line.style.width = `${60 + Math.floor(Math.random() * 35)}%`;
    container.appendChild(line);
  }
};

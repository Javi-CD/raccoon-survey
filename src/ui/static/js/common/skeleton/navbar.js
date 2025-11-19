import { qs, el } from './dom.js';

// Placeholder navbar to maintain layout stability during initial load
export const createNavbarOverlay = () => {
  const header = qs('header') || qs('#navbar');
  if (!header) {
    return null;
  }
  const h = header.offsetHeight || 0;
  const navOverlay = el('div', 'skeleton-navbar-overlay');
  navOverlay.style.setProperty('--navbar-height', `${h}px`);
  const container = el('div', 'skeleton-navbar-container');

  const left = el('div', 'skeleton-nav-left');
  const logo = el('div', 'skeleton-nav-logo');
  const title = el('div', 'skeleton-nav-title');
  left.appendChild(logo);
  left.appendChild(title);

  const center = el('div', 'skeleton-nav-center skeleton-nav-links');
  for (let i = 0; i < 4; i += 1) {
    const item = el('div', 'skeleton-nav-item');
    center.appendChild(item);
  }

  const right = el('div', 'skeleton-nav-right');
  const avatar = el('div', 'skeleton-nav-avatar');
  right.appendChild(avatar);

  container.appendChild(left);
  container.appendChild(center);
  container.appendChild(right);
  navOverlay.appendChild(container);
  document.body.appendChild(navOverlay);
  return navOverlay;
};

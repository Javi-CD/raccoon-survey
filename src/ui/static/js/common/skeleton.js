/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

import { EVENTS, TIMINGS } from './skeleton/constants.js';
import { qs } from './skeleton/dom.js';
import { createNavbarOverlay } from './skeleton/navbar.js';
import { networkIsSlow } from './skeleton/net.js';
import { createOverlay } from './skeleton/overlay.js';
import { getPageName } from './skeleton/page.js';

let skeletonTimer = null;
let verySlowTimer = null;
let overlayRef = null;
let dataReadySignaled = false;
let navbarOverlayRef = null;

const showSkeleton = () => {
  if (!overlayRef) {
    overlayRef = createOverlay();
  }
  if (!overlayRef) {
    return;
  }
  overlayRef.classList.add('skeleton-visible');
  if (!navbarOverlayRef) {
    navbarOverlayRef = createNavbarOverlay();
  }
  if (navbarOverlayRef) {
    navbarOverlayRef.classList.add('skeleton-visible');
  }

  // After 6s, show slow connection status
  verySlowTimer = setTimeout(() => {
    const status = qs('.skeleton-status', overlayRef);
    if (status) {
      status.textContent = 'Conexión lenta… seguimos intentando.';
    }
  }, TIMINGS.slowStatus);
};

const hideSkeleton = () => {
  if (skeletonTimer) {
    clearTimeout(skeletonTimer);
    skeletonTimer = null;
  }
  if (verySlowTimer) {
    clearTimeout(verySlowTimer);
    verySlowTimer = null;
  }
  if (overlayRef) {
    overlayRef.classList.remove('skeleton-visible');
  }
  if (navbarOverlayRef) {
    navbarOverlayRef.classList.remove('skeleton-visible');
  }
};

const initSkeleton = () => {
  const immediate = networkIsSlow();
  if (immediate) {
    showSkeleton();
  } else {
    skeletonTimer = setTimeout(showSkeleton, TIMINGS.showDelay);
  }

  const setupGlobalHelper = () => {
    window.RS = window.RS || {};
    window.RS.dataReady = () => {
      try {
        dataReadySignaled = true;
        window.dispatchEvent(new Event(EVENTS.DATA_LOADED));
      } catch (_) {
        /* noop */
      }
    };
  };

  // Close overlays when modules signal completion, with a load fallback.
  const setupCloseHandlers = () => {
    window.addEventListener(EVENTS.DATA_LOADED, () => {
      dataReadySignaled = true;
      hideSkeleton();
    });

    window.addEventListener('load', () => {
      setTimeout(() => {
        if (!dataReadySignaled) {
          hideSkeleton();
        }
      }, TIMINGS.loadFallback);
    });
  };

  // Public pages usually do not wait for async data; auto-close quickly.
  const autoCloseOnPublicPages = () => {
    const pageNow = getPageName();
    if (pageNow === 'home' || pageNow === 'login') {
      Promise.resolve().then(() => {
        if (window.RS && typeof window.RS.dataReady === 'function') {
          window.RS.dataReady();
        }
      });
    }
  };

  setupGlobalHelper();
  setupCloseHandlers();
  autoCloseOnPublicPages();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSkeleton);
} else {
  initSkeleton();
}

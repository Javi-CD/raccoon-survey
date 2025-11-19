/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('hamburgerBtn');
  const menu = document.getElementById('mobileMenu');
  const iconBars = document.getElementById('iconBars');
  const iconX = document.getElementById('iconX');

  const closeMenu = () => {
    try {
      if (menu && iconBars && iconX) {
        menu.classList.add('opacity-0');
        menu.classList.add('-translate-y-2');
        setTimeout(() => {
          menu.classList.add('hidden');
        }, 200);
        iconBars.classList.remove('hidden');
        iconX.classList.add('hidden');
      }
    } catch (_) {
      /* noop */
    }
  };

  const openMenu = () => {
    try {
      if (menu && iconBars && iconX) {
        menu.classList.remove('hidden');
        // allow reflow
        setTimeout(() => {
          menu.classList.remove('opacity-0');
          menu.classList.remove('-translate-y-2');
        }, 10);
        iconBars.classList.add('hidden');
        iconX.classList.remove('hidden');

        // Animate "Sign in" link when opening menu
        setTimeout(() => {
          try {
            const loginLink = menu.querySelector('.link-fill');
            if (!loginLink) {
              return;
            }
            // Restart and activate fill animation
            loginLink.classList.remove('fill-active');

            // force reflow to restart transition
            void loginLink.offsetWidth;
            loginLink.classList.add('fill-active');

            // remove active state after ~1.2s
            setTimeout(() => {
              loginLink.classList.remove('fill-active');
            }, 1200);
          } catch (_) {
            /* noop */
          }
        }, 60);
      }
    } catch (_) {
      /* noop */
    }
  };

  const toggle = () => {
    try {
      if (!menu) {
        return;
      }
      const isHidden = menu.classList.contains('hidden');
      if (isHidden) {
        openMenu();
      } else {
        closeMenu();
      }
    } catch (_) {
      /* noop */
    }
  };

  try {
    if (btn) {
      btn.addEventListener('click', toggle);
    }
  } catch (_) {
    /* noop */
  }

  // Close the menu when clicking any link within the mobile menu
  try {
    if (menu) {
      const menuLinks = menu.querySelectorAll('a');
      menuLinks.forEach(link => {
        link.addEventListener('click', () => {
          closeMenu();
        });
      });
    }
  } catch (_) {
    /* noop */
  }

  // Close on resize to md and above
  try {
    window.addEventListener('resize', () => {
      try {
        if (window.innerWidth >= 768) {
          closeMenu();
        }
      } catch (_) {
        /* noop */
      }
    });
  } catch (_) {
    /* noop */
  }
});

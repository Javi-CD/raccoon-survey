document.addEventListener('DOMContentLoaded', () => {
  const cfg = window.RS_CONFIG || {};
  const API_BASE_URL = cfg.apiBaseUrl || '';
  const logoutLink = document.getElementById('logout-link');

  if (!logoutLink) {
    return;
  }

  logoutLink.addEventListener('click', async e => {
    e.preventDefault();

    const get = k => {
      try {
        return sessionStorage.getItem(k) || localStorage.getItem(k) || '';
      } catch (_) {
        return '';
      }
    };

    const access = get('rs_access_token');

    try {
      if (access) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${access}`,
          },
          credentials: 'include',
        });
      }
    } catch (_) {
      void 0;
    }

    try {
      sessionStorage.removeItem('rs_access_token');
      sessionStorage.removeItem('rs_refresh_token');
      localStorage.removeItem('rs_access_token');
      localStorage.removeItem('rs_refresh_token');

      document.cookie = 'rs_access_token=; Max-Age=0; Path=/; SameSite=Lax';
      document.cookie = 'rs_refresh_token=; Max-Age=0; Path=/; SameSite=Lax';
      document.cookie = 'rs_has_session=; Max-Age=0; Path=/; SameSite=Lax';
    } catch (_) {
      void 0;
    }

    window.location.href = cfg.loginUrl || '/login';
  });
});

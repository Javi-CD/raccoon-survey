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

// Page inference kept coarse to choose skeleton shape
export const getPageName = () => {
  const { pathname } = window.location;
  if (pathname.includes('dashboard')) {
    return 'dashboard';
  }
  if (pathname.includes('surveys')) {
    return 'surveys';
  }
  if (pathname.includes('reports')) {
    return 'reports';
  }
  if (pathname.includes('config')) {
    return 'config';
  }
  if (pathname === '/' || pathname.includes('/index')) {
    return 'home';
  }
  if (pathname.includes('/login')) {
    return 'login';
  }
  return 'generic';
};

// Network helpers
export const networkIsSlow = () => {
  const conn =
    navigator.connection ||
    navigator.mozConnection ||
    navigator.webkitConnection;
  if (!conn || !conn.effectiveType) {
    return false;
  }
  return /(^2g$|^3g$)/.test(conn.effectiveType);
};

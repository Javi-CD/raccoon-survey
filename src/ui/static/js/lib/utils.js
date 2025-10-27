(() => {
  window.RS = window.RS || {};

  const fmtDate = iso => {
    if (!iso) {return '—';}
    try {
      const d = new Date(iso);
      return d.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      });
    } catch (_) {
      return String(iso);
    }
  };

  const downloadBlob = (filename, blob) => {
    try {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || 'download';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('downloadBlob error:', e);
    }
  };

  const copyToClipboard = async text => {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text || '');
        return true;
      }
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = text || '';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      return true;
    } catch (e) {
      return false;
    }
  };

  window.RS.utils = {
    fmtDate,
    downloadBlob,
    copyToClipboard,
  };
})();
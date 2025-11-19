// Event names and timing constants centralized
export const EVENTS = { DATA_LOADED: 'rs:data-loaded' };

export const TIMINGS = {
  showDelay: 350, // avoid flicker on fast loads
  slowStatus: 6000, // show slow connection hint
  loadFallback: 1000, // hide after window.load if nobody signaled
};

export const qs = (sel, ctx = document) => ctx.querySelector(sel);

export const el = (tag, className) => {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  return node;
};

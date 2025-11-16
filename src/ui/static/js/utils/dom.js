/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

export const qs = (sel, root = document) => root.querySelector(sel);
export const qsa = (sel, root = document) =>
  Array.from(root.querySelectorAll(sel));

export const el = (tag, attrs = {}, children = []) => {
  const node = document.createElement(tag);

  Object.entries(attrs || {}).forEach(([k, v]) => {
    if (k === 'class') {
      node.className = v || '';
    } else if (k === 'text') {
      node.textContent =
        typeof v !== 'undefined' && v !== null ? String(v) : '';
    } else if (k.startsWith('on') && typeof v === 'function') {
      node.addEventListener(k.slice(2).toLowerCase(), v);
    } else {
      node.setAttribute(
        k,
        typeof v === 'undefined' || v === null ? '' : String(v)
      );
    }
  });

  (Array.isArray(children) ? children : [children]).forEach(c => {
    if (c === null || typeof c === 'undefined') {
      return;
    }
    if (typeof c === 'string') {
      node.appendChild(document.createTextNode(c));
    } else {
      node.appendChild(c);
    }
  });
  return node;
};

/*
Copyright (C) 2025 Raccoon Survey org
This file is part of Raccoon Survey.
Raccoon Survey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License v3 as published by
the Free Software Foundation.
See the LICENSE file distributed with this program for details.
*/

import { wireCategoryCreateButton, loadCategories } from './categories.js';
import { wireTeamCreateButton, loadTeams } from './teams.js';
import { wireUserCreateButton, loadUsers } from './users.js';

const boot = async () => {
  try {
    wireUserCreateButton();
    await loadUsers();
    wireTeamCreateButton();
    await loadTeams();
    wireCategoryCreateButton();
    await loadCategories();
  } catch (e) {
    console.error('config boot error:', e);
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}

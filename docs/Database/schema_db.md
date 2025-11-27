# Database Schema

```sql
-- Teams table
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    state BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    state BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Roles
CREATE INDEX idx_roles_name ON roles(name);
CREATE INDEX idx_roles_state ON roles(state);

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id) ON DELETE SET NULL,
    role_id INT REFERENCES roles(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    state BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Users
CREATE INDEX idx_users_team_id ON users(team_id);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_users_state ON users(state);
CREATE INDEX idx_users_email ON users(email);

-- Surveys table
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    created_by_user_id INT REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_anonymous BOOLEAN DEFAULT TRUE,
    state BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Surveys
CREATE INDEX idx_surveys_team_id ON surveys(team_id);
CREATE INDEX idx_surveys_created_by ON surveys(created_by_user_id);
CREATE INDEX idx_surveys_created_at ON surveys(created_at);
CREATE INDEX idx_surveys_expires_at ON surveys(expires_at);
CREATE INDEX idx_surveys_state ON surveys(state);

-- Survey Tokens table
CREATE TABLE survey_tokens (
    id SERIAL PRIMARY KEY,
    survey_id INT REFERENCES surveys(id) ON DELETE CASCADE,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    employee_identifier VARCHAR(100), -- Optional: Internal ID without personal data
    is_used BOOLEAN DEFAULT FALSE,
    used_at TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Survey Tokens
CREATE INDEX idx_survey_tokens_token ON survey_tokens(token);
CREATE INDEX idx_survey_tokens_survey_id ON survey_tokens(survey_id);
CREATE INDEX idx_survey_tokens_team_id ON survey_tokens(team_id);
CREATE INDEX idx_survey_tokens_expires_at ON survey_tokens(expires_at);
CREATE INDEX idx_survey_tokens_is_used ON survey_tokens(is_used);

-- Questions table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    survey_id INT REFERENCES surveys(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    options JSON,
    is_required BOOLEAN DEFAULT FALSE,
    order_position INT DEFAULT 0,
    state BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Questions
CREATE INDEX idx_questions_survey_id ON questions(survey_id);
CREATE INDEX idx_questions_type ON questions(type);
CREATE INDEX idx_questions_order ON questions(order_position);
CREATE INDEX idx_questions_state ON questions(state);

-- Responses table
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    survey_token_id INT REFERENCES survey_tokens(id) ON DELETE CASCADE,
    answer TEXT NOT NULL,
    state BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Responses
CREATE INDEX idx_responses_question_id ON responses(question_id);
CREATE INDEX idx_responses_survey_token_id ON responses(survey_token_id);
CREATE INDEX idx_responses_created_at ON responses(created_at);
CREATE INDEX idx_responses_state ON responses(state);

-- Audit Logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    entity_id INT NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('create','update','delete','soft_delete','restore','login','logout','assign_role','generate_tokens')),
    changed_by_user_id INT REFERENCES users(id) ON DELETE SET NULL,
    ip_address VARCHAR(45),
    previous_data JSON,
    new_data JSON,
    metadata JSON,
    triggered_by VARCHAR(20) DEFAULT 'manual' CHECK (triggered_by IN ('manual','system')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Audit Logs
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_changed_by ON audit_logs(changed_by_user_id);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_triggered_by ON audit_logs(triggered_by);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    state BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices in Categories
CREATE INDEX idx_categories_name ON categories(name);
CREATE INDEX idx_categories_state ON categories(state);

-- Question Categories table
CREATE TABLE question_categories (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    assigned_by_user_id INT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (question_id, category_id)
);

-- Indices in Question Categories
CREATE INDEX idx_question_categories_question_id ON question_categories(question_id);
CREATE INDEX idx_question_categories_category_id ON question_categories(category_id);
CREATE INDEX idx_question_categories_assigned_by ON question_categories(assigned_by_user_id);
```

---

## Table Explanations

### 1. teams

**Purpose**: groups administrative users and surveys by department/area.

**Fields**:

- `id (PK)`
- `name`
- `description`
- `state` (TRUE = active, FALSE = inactive)
- `created_at`

**Relationships**:

- One team has many administrative users.
- One team has many surveys.
- One team has many survey tokens.

---

### 2. roles

**Purpose**: defines the different roles administrative users can have in the system.

**Fields**:

- `id (PK)`
- `name` (unique) — e.g., "admin", "rrhh"
- `description`
- `state` (TRUE = active, FALSE = inactive)
- `created_at`

**Indexes**:

- `idx_roles_name` for role name lookups.
- `idx_roles_state` to filter active/inactive roles.

**Relationships**:

- One role can be assigned to many administrative users.

---

### 3. users

**Purpose**: stores information for administrative users (HR, Administrators) who require login.

**Fields**:

- `id (PK)`
- `team_id (FK → teams.id)`
- `role_id (FK → roles.id)`
- `name`
- `email (unique)` — only for users with login
- `password_hash` — only for users with login
- `state` (TRUE = active, FALSE = inactive)
- `created_at`

**Indexes**:

- `idx_users_team_id` to filter by team.
- `idx_users_role_id` to filter by role.
- `idx_users_state` to filter active/inactive users.
- `idx_users_email` for fast admin login.

**Relationships**:

- Belongs to a team.
- Has an assigned role.
- Can create many surveys.

---

### 4. surveys

**Purpose**: represents surveys created by administrative users for a specific team.

**Fields**:

- `id (PK)`
- `team_id (FK → teams.id)` — team targeted by the survey
- `created_by_user_id (FK → users.id)` — admin user who created the survey
- `title`
- `description`
- `is_anonymous` (`TRUE` = guarantees full anonymity)
- `state` (TRUE = active, FALSE = inactive)
- `expires_at` — deadline to respond
- `created_at`

**Indexes**:

- `idx_surveys_team_id` to list surveys for a team.
- `idx_surveys_created_by` for auditing who created what.
- `idx_surveys_created_at` to sort or filter by date.
- `idx_surveys_expires_at` to clean up expired surveys.
- `idx_surveys_state` to filter active/inactive surveys.

**Relationships:**

- Belongs to a team.
- Created by an administrative user.
- Has many questions.
- Has many access tokens.

---

### 5. survey_tokens

**Purpose**: manages unique tokens for anonymous employee access to specific surveys.

**Fields**:

- `id (PK)`
- `survey_id (FK → surveys.id)` — associated survey
- `team_id (FK → teams.id)` — employee's team (for metrics)
- `token` (unique) — UUID token for anonymous access
- `employee_identifier` — optional internal ID (e.g., "EMP001") without personal data
- `is_used` — whether the token has been used
- `used_at` — timestamp when it was used
- `expires_at` — token expiration date
- `created_at`

**Indexes**:

- `idx_survey_tokens_token` for fast token validation.
- `idx_survey_tokens_survey_id` to list tokens for a survey.
- `idx_survey_tokens_team_id` for team-based metrics.
- `idx_survey_tokens_expires_at` to clean up expired tokens.
- `idx_survey_tokens_is_used` for participation statistics.

**Relationships**:

- Belongs to a specific survey.
- Associated with a team (for aggregated metrics).
- Has many responses (once used).

**Note**: This is the key mechanism for anonymity. It contains no personally identifiable data.

---

### 6. questions

**Purpose**: defines the questions within each survey.

**Fields**:

- `id (PK)`
- `survey_id (FK → surveys.id)`
- `text` (question content)
- `type` (`text`, `multiple_choice`, `rating`)
- `options` (`JSONB`, only useful for multiple choice)
- `is_required` — whether the question is mandatory
- `order_position` — order of appearance in the survey
- `state` (TRUE = active, FALSE = inactive)
- `created_at`

**Indexes**:

- `idx_questions_survey_id` to get questions for a survey.
- `idx_questions_type` for type filters.
- `idx_questions_order` to order questions correctly.
- `idx_questions_state` to filter active/inactive questions.

**Relationships**:

- Belongs to a survey.
- Has many responses.

---

### 7. responses

**Purpose**: stores fully anonymous responses linked to unique tokens.

**Fields**:

- `id (PK)`
- `question_id (FK → questions.id)`
- `survey_token_id (FK → survey_tokens.id)` — links response to the token
- `answer` (text, numeric value, or selection)
- `state` (TRUE = active, FALSE = inactive)
- `created_at`

**Indexes**:

- `idx_responses_question_id` to get responses per question.
- `idx_responses_survey_token_id` to group responses from the same token.
- `idx_responses_created_at` for temporal analysis.
- `idx_responses_state` to filter active/inactive responses.

**Relationships**:

- Belongs to a question.
- Linked to a survey token.

**Note**: Anonymity is ensured because:

1. There is no direct FK to users.
2. It only links to the token, which contains no personal data.
3. Multiple tokens can belong to the same team without identifying individuals.

---

### 8. audit_logs

**Purpose**: records system events and changes with traceability without compromising employee anonymity.

**Fields**:

- `id (PK)`
- `entity_type` — type of affected entity (e.g., `survey`, `question`, `response`, `role`, `team`, `user`)
- `entity_id` — ID of the affected record in its table
- `action` — action type (`create`, `update`, `delete`, `soft_delete`, `restore`, `login`, `logout`, `assign_role`, `generate_tokens`)
- `changed_by_user_id (FK → users.id)` — admin user who performed the action
- `ip_address` — source IP (IPv4/IPv6)
- `previous_data (JSONB)` — snapshot before change (when applicable)
- `new_data (JSONB)` — snapshot after change (when applicable)
- `metadata (JSONB)` — additional contextual information
- `triggered_by` — event origin (`manual` or `system`)
- `created_at` — event timestamp

**Indexes**:

- `idx_audit_entity` for searches by affected entity.
- `idx_audit_action` for filtering by action type.
- `idx_audit_changed_by` for audits by administrative user.
- `idx_audit_created_at` for temporal ordering and audit windows.
- `idx_audit_triggered_by` to distinguish manual vs system events.

**Relationships**:

- Logical relation to audited entities via (`entity_type`, `entity_id`) without direct FK.
- FK to `users` via `changed_by_user_id` for administrative action traceability.

### 9. categories

**Purpose**: organizes questions by topics (e.g., Culture, Communication, Leadership) to facilitate filters and reports.

**Fields**:

- `id (PK)`
- `name` (unique) — category name
- `description` — optional description
- `state` (TRUE = active, FALSE = inactive)
- `created_at`

**Indexes**:

- `idx_categories_name` for lookups by name.
- `idx_categories_state` to filter active/inactive categories.

**Relationships**:

- Has many relations with questions via `question_categories`.

---

### 10. question_categories

**Purpose**: many-to-many relationship between questions and categories.

**Fields**:

- `id (PK)`
- `question_id (FK → questions.id)`
- `category_id (FK → categories.id)`
- `assigned_by_user_id (FK → users.id)` — admin user who assigned the category
- `created_at` — assignment date

**Indexes**:

- `idx_question_categories_question_id` to query a question's categories.
- `idx_question_categories_category_id` to query a category's questions.
- `idx_question_categories_assigned_by` for assignment audits.

**Relationships**:

- Belongs to a question and a category.
- Logical relation with `users` for assigner traceability.

---

## Global Relationships

```plaintext

teams ──< users (admins/HR only)
roles ──< users (admins/HR only)
teams ──< surveys ──< questions ──< responses
users ──< surveys (created_by)
teams ──< survey_tokens
surveys ──< survey_tokens ──< responses
users ──< audit_logs (changed_by_user_id)
audit_logs ──(entity_type, entity_id)→ auditable entities (logical relation, no FK)
questions ──< question_categories >── categories

```

---

## Index Justification

### Table categories

- `idx_categories_name`: lookups by category name.
- `idx_categories_state`: filter active/inactive categories.

### Table question_categories

- `idx_question_categories_question_id`: get a question's categories.
- `idx_question_categories_category_id`: get questions by category.
- `idx_question_categories_assigned_by`: audit who made the assignment.

### Table roles

- `idx_roles_name` and `idx_roles_state`: lookups by role name and filter active roles.

### Table users

- `idx_users_team_id`, `idx_users_role_id`, and `idx_users_state`: queries by team, role filter, and active users.
- `idx_users_email`: fast administrator login.

### Table surveys

- `idx_surveys_team_id`: list surveys for a specific team.
- `idx_surveys_created_by`: audit who created each survey.
- `idx_surveys_created_at`: chronological reports and ordering.
- `idx_surveys_expires_at`: automatic cleanup of expired surveys.
- `idx_surveys_state`: filter active/inactive surveys.

### Table survey_tokens

- `idx_survey_tokens_token`: ultra-fast validation of access tokens.
- `idx_survey_tokens_survey_id`: manage tokens per survey.
- `idx_survey_tokens_team_id`: aggregated metrics per team without identifying individuals.
- `idx_survey_tokens_expires_at`: cleanup of expired tokens.
- `idx_survey_tokens_is_used`: participation statistics and reuse prevention.

### Table questions

- `idx_questions_survey_id`: get all questions for a survey.
- `idx_questions_type`: filters and validations by question type.
- `idx_questions_order`: ordered presentation of questions.
- `idx_questions_state`: filter active/inactive questions.

### Table responses

- `idx_responses_question_id`: analysis of responses by specific question.
- `idx_responses_survey_token_id`: group responses from the same token (anonymous session).
- `idx_responses_created_at`: temporal analysis and trend charts.
- `idx_responses_state`: filter valid/invalid responses.

### Table audit_logs

- `idx_audit_entity`: quick search by affected entity.
- `idx_audit_action`: filter by action type (CRUD, login, etc.).
- `idx_audit_changed_by`: audit by admin user who made changes.
- `idx_audit_created_at`: temporal ordering and window analysis.
- `idx_audit_triggered_by`: distinguish manual vs system-generated events.

---

## Relational Model

### Anonymity Architecture

The design guarantees complete employee anonymity through:

1. **Separation of identities**: Employees never register in the system
2. **Single-use tokens**: Each employee receives a unique token per survey
3. **Limited traceability**: Only team participation can be tracked, not individuals
4. **Automatic expiration**: Tokens have an expiration date for added security

### Anonymous data flow

```
Admin → Creates survey → Generates tokens → Employee uses token → Responds anonymously
```

### Model benefits

- **Total privacy**: Impossible to identify individual responses
- **Trust**: Employees can answer honestly
- **Compliance**: Aligned with privacy regulations
- **Simplicity**: No need to manage employee users
- **Security**: Single-use tokens prevent unauthorized access

For a visual representation of the relational model, see the ERD diagram in `DER.png`.

---

## Entity-Relationship Diagram (ERD)

![ERD](DER.png)

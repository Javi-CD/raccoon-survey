module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // Type enum - allowed commit types
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
        "chore",
        "ci",
        "build",
        "revert",
        "hotfix",
        "security",
        "deps",
        "config",
      ],
    ],
    // Subject case - allow sentence case and lower case
    "subject-case": [2, "always", ["sentence-case", "lower-case"]],

    // Subject length
    "subject-max-length": [2, "always", 72],
    "subject-min-length": [2, "always", 10],

    // Body and footer rules
    "body-max-line-length": [2, "always", 100],
    "footer-max-line-length": [2, "always", 100],

    // Scope rules - optional but if present, must be lowercase
    "scope-case": [2, "always", "lower-case"],
    "scope-max-length": [2, "always", 20],

    // Header rules
    "header-max-length": [2, "always", 100],

    // Type and subject are required
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
  },
};

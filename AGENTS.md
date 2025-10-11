# 🧪 Verification & Quality Gates

These steps define the local and CI verification pipeline used by all agents.

## 1️⃣ Python Quality

- **Lint:**  
  ```bash
  ruff check --quiet
  ```  
  Reject any changes until **zero issues** remain.

- **Format:**  
  ```bash
  ruff format
  ```  
  Code must follow PEP 8 / Black-style formatting.

- **Safety:**  
  - Catch and handle file I/O errors with `try/except`.  
  - Validate untrusted input at boundaries (web handlers, CLI args, DB queries).  
  - Always use parameterized SQL and output encoding.

- **Documentation:**  
  All public functions require docstrings describing purpose, parameters, and return values.

---

## 2️⃣ TypeScript / React Quality

- **Lint:**  
  ```bash
  eslint . --ext .ts,.tsx --max-warnings=0
  ```  
  Uses the default `@typescript-eslint/recommended` ruleset.  
  Warnings fail the gate; fix or justify before commit.

- **Type Discipline:**  
  - Avoid `any` in exported or public types.  
  - Explicit return types for public functions/components.  
  - Imports must be organized and unused imports removed.

---

## 3️⃣ Repository Hygiene

- Remove commented-out code unless it carries a `TODO:` with an issue reference.  
- Fix grammar and spelling in user-facing text.  
- One trailing newline per file; no trailing spaces.

---

## 4️⃣ Documentation & Scripts

- **Markdown:**  
  ```bash
  markdownlint "**/*.md"
  ```  
  Must pass standard markdownlint rules (headings ordered, no trailing spaces).

- **Shell scripts:**  
  ```bash
  shellcheck path/to/script.sh
  ```  
  Non-trivial scripts must include `set -euo pipefail`.

---

## 5️⃣ Configuration Files

- All `.json`, `.yml`, and `.yaml` files must be valid and consistently formatted.  
- Remove stray keys or invalid schema entries.

---

✅ **Summary**

Agents must complete all above checks successfully before opening a pull request.  
PRs that fail any step will be rejected by the Review Droid during automatic or manual review.

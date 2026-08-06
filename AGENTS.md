# Agent Rules — Paraby UI Framework

This file is the single entry point for **any** AI coding agent (Claude Code,
Cursor, Copilot, Codex, or otherwise) working in this repository. Read it
before making changes. `CLAUDE.md` at the repo root just points here — do not
duplicate these rules elsewhere; update this file and this file only.

> ⚠️ This project has been rewritten more than once (it dropped a Cython
> parser for a pure-Python one — see git log if curious). Docs that describe
> *how the code works* rot fast. Treat anything below describing internals as
> a **starting pointer to go read the real code**, never as ground truth to
> code against blindly. If a claim here conflicts with what you read in the
> source, the source wins — and you should fix this file.

## 1. What this project is

Paraby is a Python UI framework: a `.pui` DSL (declarative, CSS/Flutter-like
syntax) gets **transpiled** into plain Python source that builds a
CustomTkinter UI, then a binder auto-injects widgets and event handlers into
the caller's `.py` file. Full DSL syntax reference: **[`SYNTAX.md`](SYNTAX.md)**
— read it before writing or generating any `.pui` code or touching the parser.
`SYNTAX.md` section 5 has explicit rules for keeping the syntax doc, parser,
and `type_stubs.pyi` in sync whenever the DSL changes — follow them.

## 2. Current architecture (high level — verify against code, don't memorize)

- `src/paraby/core/parser/` — pure Python (no Cython, no `.pyx`, no build
  step): `lexer.py` → `ast_builder.py` → `codegen.py`, orchestrated by
  `transpiler.py`. `widget_registry.py` is the **single source of truth**
  for widget aliases/prefixes (see rule in §3).
- `src/paraby/core/` — runtime plumbing: `runner.py` (load/run `.pui`),
  `binder.py` (AST-scans the caller `.py` file to auto-bind events),
  `events.py`, `patch.py` (monkey-patches CustomTkinter for magic
  attributes), `finder.py` (import hook for `.pui` files), `cli.py`.
- `src/paraby/components/` — widget/window/color logic that talks directly
  to CustomTkinter (`widgets.py`, `window.py`, `colors.py`, `popup.py`,
  `custom_widgets/`).
- `src/paraby/languages/*.json` + `language_manager.py` — i18n for all
  user-facing console messages (`vi`/`en`).
- `tests/` — pytest suite, run with `python -m pytest tests/ -q`.
- `docs/` — living docs only: `SYNTAX.md` (DSL reference), `User_Guide.md` /
  `Huong_dan_su_dung.md` (end-user guides), `QUY_TRINH_SUA_LOI.md` (the
  worktree-based fix/merge workflow used across bugfix rounds on this repo).

## 3. Rules that prevent the mistakes already made in this project

These aren't theoretical — every rule below maps to a real bug found and
fixed in this codebase.

1. **Widget aliases live in exactly one place.** Never hard-code a widget
   type name, alias, or prefix anywhere outside
   `src/paraby/core/parser/widget_registry.py`. Two independent
   re-implementations of the same alias-prefix-matching logic (in `binder.py`
   and `patch.py`) already drifted apart and caused a real bug — they now
   both call shared helpers in `widget_registry.py`. If you need this logic
   somewhere new, import the existing helper; don't re-derive it.

2. **Never interpolate a raw user-supplied value into generated Python
   source.** Every value from a `.pui` file must go through
   `lexer.py::process_value()` (which routes through `repr()` /
   `ast.literal_eval()`) before it lands in codegen output. This is the
   project's only defense against code injection via a `.pui` file, and it
   has a dedicated regression test (`tests/test_injection.py`) — never
   weaken it to "make a feature work."

3. **Don't duplicate the same parsing/matching logic in multiple files.**
   If you find yourself writing the same conditional/lookup a second time,
   stop and extract a shared function instead. This has directly caused bugs
   here before.

4. **Structural boundaries (indent, nesting depth) must be computed
   relative to a local reference point, never an absolute constant.** The
   DSL allows arbitrary nesting (window → loop → frame → widget → ...); code
   that assumes "indent == 0 means top level" breaks as soon as something is
   nested one level deeper than whoever wrote that check imagined.

5. **Prefer fixing the general rule over adding a special case.** If a bug
   fix needs an `if node_type == 'loop': ... else: ...`-style patch repeated
   at multiple call sites, that's a sign the underlying AST/codegen design
   is wrong for that case — fix the general rule, don't scatter patches.

6. **A syntax/parse error must fail loudly and early, not silently produce
   a malformed tree.** E.g. an unclosed `window(`/`widget(`/`loop(` block or
   a typo'd widget name must raise a clear error at parse time — never let
   it fall through and silently corrupt the AST stack (this has been a real
   bug class in `ast_builder.py`).

## 4. Testing — non-negotiable before claiming anything is done

- Run `python -m pytest tests/ -q` after any change to `core/parser/`,
  `core/binder.py`, or `components/`. A clean exit code is **not** proof of
  correctness by itself — read the actual test output.
- **Known flaky quirk on this machine:** the *first* pytest run right after
  creating a fresh git worktree sometimes fails with
  `_tkinter.TclError: Can't find a usable init.tcl` — a one-off Tcl/Tk init
  race, not a real regression. Re-run once before concluding a failure is
  real.
- Never open a real CustomTkinter GUI window during automated testing/CI —
  use the existing mocks/test doubles in `tests/`.
- If a change affects codegen output, verify the generated string is valid
  Python (e.g. via `ast.parse()`), not just that it "contains" an expected
  substring.
- Do not delete or loosen a failing test to make it pass — fix the code, or
  get explicit confirmation the test itself is wrong.

## 5. Workflow for multi-step or exploratory fixes

For anything beyond a one-line fix — especially deep bug-hunting passes —
use an isolated git worktree so you never collide with other work-in-progress
in the main checkout. The exact process (including a real gotcha: a fresh
worktree can be branched from a stale `origin/main` instead of local `main`)
is documented in **[`docs/QUY_TRINH_SUA_LOI.md`](docs/QUY_TRINH_SUA_LOI.md)**
— follow it rather than improvising a new process each time.

## 6. Code modification & transparency

- **Transparent editing:** do NOT use background Python scripts, scratch
  directory regex scripts, or shell commands (`sed`, `awk`, PowerShell
  replacements) to manipulate project source code.
- **Use native tools:** use the dedicated file-editing tools your harness
  provides (e.g. an `Edit`/`replace_file_content`-style tool), not raw shell
  text manipulation, so every change is properly diffed and visible to the
  user.

## 7. Housekeeping

- Don't leave scratch/dev files (fixture dumps, one-off scripts) in the repo
  root — they belong under `.dev/`.
- Don't claim a task is finished without showing the actual test output that
  proves it.
- Keep this file and `SYNTAX.md` in sync with reality. If you notice either
  one describing something that no longer exists, fix it in the same change
  — don't let it rot into the next stale-docs cleanup.

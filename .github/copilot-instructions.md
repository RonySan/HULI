# Copilot Instructions for H.U.L.I

This repository is a very small Python project that implements a simple
interactive command‑line assistant named **H.U.L.I**. The entire application is
defined in `core/huli.py`. There are no tests, no build system, and most of the
files in the workspace are part of a Python virtual environment located under
`env/`.

The purpose of the instructions below is to get an AI coding agent (such as a
Copilot assistants) up and running quickly with edits or extensions to the
behaviour of the assistant.

---

## Project Overview

* **Single entry point**: `core/huli.py` defines `iniciar()` which prints a
  welcome message then enters an infinite input loop. When run as a script the
  function is called immediately.
* **Command handling**: the loop reads a line from `input()`, lower‑cases it
  and compares it against hard‑coded literals (`"sair"`, `"status"`).
  Unrecognised commands elicit a fixed response.
* **Portuguese responses**: all printed text is in Brazilian Portuguese; any new
  messages or prompts should follow the same style and tone.
* **Environment**: a virtual environment lives under `env/`. Sources outside of
  `core/` are not part of the application.

Because the codebase is tiny the ``big picture`` is simply:

1. Start the script with `python core/huli.py` (activate the venv first if
   desired).
2. Type commands and read printed responses.
3. Modify `core/huli.py` to change or add new command handlers.

---

## Common Development Tasks

* **Run the assistant**: `source env/Scripts/activate` (Unix shell) then
  `python core/huli.py`.
* **Add a command**: add another `elif comando.lower() == "...":` block or
  refactor to a dictionary/dispatch table. Keep the input normalisation call
  (`lower()`) to ensure case‑insensitive matching.
* **Handle exit**: the `"sair"` command breaks the loop and prints a farewell
  message referencing "Rony"; maintain this naming if the conversation
  character is extended, or generalise if appropriate.
* **Language consistency**: maintain Portuguese phrasing and accents. Example
  pattern in `core/huli.py`:

  ```python
  elif comando.lower() == "status":
      print("H.U.L.I: Sistemas operacionais funcionando normalmente.")
  ```

* **Extending behaviour**: because there are no tests or CI, manual testing
  consists of running the script and exercising new commands.
  Automated tests may be added under a `tests/` directory if the project
  grows; follow a standard pytest layout and import `core.huli`.

* **Virtual environment**: use the existing one, or recreate with
  `python -m venv env` then `env/Scripts/activate` and install any dependencies
  with `pip install ...`. Right now there are none beyond the standard library.

* **Debugging**: use print statements, `pdb.set_trace()`, or run the script in
  an IDE; the code is synchronous and has no asynchronous/IO complexity.

---

## Project‑specific Conventions

* Commands are matched on the lower‑cased whole line; there is no tokenisation
  or argument parsing. For multi‑word commands, compare against the full string
  (e.g. `"ligar luz"`).
* The assistant speaks as `H.U.L.I` and addresses the user as `Você`; preserve
  those identifiers in log messages or any new output.
* There are no config files or data storage; state is not persisted across runs.
  Adding persistence requires introducing a new module and should be documented
  in `core/`.
* Keep `core/huli.py` as the place for business logic until the project
  naturally needs further decomposition.

---

## What to Look for as the Project Evolves

* When adding complexity (parsers, network calls, plugins), create new
  modules under `core/` and update these instructions accordingly.
* If tests are added, the instructions should list the command (e.g.
  `pytest` from the workspace root) and preferred patterns.
* If external integrations are introduced (APIs, hardware, etc.) their
  configuration and error handling patterns should be documented here.

---

Please review and let me know if there are any unclear areas or additional
details you think an AI agent should know about this repository.
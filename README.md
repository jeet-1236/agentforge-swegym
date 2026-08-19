# SWE-Gym problems, worked by AgentForge

One folder per problem. Each is a real merged pull request from an upstream project, checked out
at the commit *before* the fix, with that PR's own test already applied — so the bug is present
and the test that proves it is there.

The agents are shown only the issue text as filed. The upstream fix is never shown to them; it is
used afterwards to grade the result, by running the project's own FAIL_TO_PASS tests against the
patch (`scripts/swegym_grade.py`).

| problem | upstream | commit |
|---|---|---|
| `getmoto__moto-5502` | getmoto/moto | `bd48bff981` |

Each fix appears as a pull request against this repository, inside its own folder.

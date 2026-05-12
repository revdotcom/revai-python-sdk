# Repo Readiness Report

**Repo:** revai-python-sdk (`revdotcom/revai-python-sdk`)
**Audited:** 2026-05-12
**Based on:** AI in EPD Module 3 — Repo Readiness Checklist (Claire Vo & Zach Davis)
**Audit version:** v2.1 (local + external GitHub checks; Jenkins probed via stored config)
**External validation:** GitHub Actions via `gh` + Jenkins via stored config

## Summary

- **Overall readiness:** Early
- **Score:** 4 ✅ / 2 🟡 / 15 ❌ / 0 🔗 / 5 ➖ (of 26)
- **PASS%:** 4 / 21 applicable = **19%**
- **Tier-1 FAILs:** **10** (items 1, 2, 3, 5, 7, 8, 9, 10, 11, 12)
- **Stack detected:** Python (84 tracked `.py` files; 45 in `src/`, 27 in `tests/`, 10 examples). Packaged via `setuptools` (`setup.py` + `requirements.txt`). Test runner: pytest under tox (Py 3.8–3.11). Lint: flake8.
- **External validation verdict:** GitHub Actions CI fast and reliable on `develop` (median build_test ~25 s, success rate 4/7 on the small recent sample — failures localised to one dependabot PR and one feature branch's early commits). Jenkins "Rev.ai SDK Python pipeline" exists for tag-driven PyPI deploy but **4/4 most-recent builds are FAILUREs (last run 2024-11-27)** — release pipeline appears broken. No agentic review bots active. CodeQL + Dependabot wired at org/UI level (no committed config). 16/20 merged PRs reference a Linear ticket (REVAI-/AISDK-/DOCS-).

### Top 3 Next Actions
1. **Add a root `CLAUDE.md`/`AGENTS.md`** covering: what this SDK wraps (Rev.ai async + streaming + custom-vocab + summarization + translation + LID + topic/sentiment + forced alignment APIs), how the `rev_ai` package is organised (`apiclient.py` / `streamingclient.py` / `generic_api_client.py` / per-feature `*_client.py` + `models/`), the Py 3.8–3.11 + tox + flake8 dev loop, and the release flow (bumpversion → tag → Jenkins → PyPI). Closes items 1, 2, 3, and most of 5 in one move.
2. **Investigate and fix (or retire) the Jenkins release pipeline.** All 4 most-recent builds of `Rev.ai SDK Python pipeline` failed; last successful publish path is unclear. Either repair the Jenkinsfile + pipeline or document the manual `make release` / `twine upload` fallback so the next contributor knows how the package actually ships.
3. **Bring a minimal agent-tooling baseline into the repo:** committed `.claude/settings.json` with a curated `permissions.allow`, at least one tip file (`async-python.md`-style guidance noting flake8 ignores E731/W504/etc., tox + pytest invocation, the `src/` layout quirk), and a `.pre-commit-config.yaml` running flake8 to make the lint contract local-enforceable. Closes items 7, 10, and starts to address 2, 8.

## Tier 1 — Foundation

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 1 | AGENTS.md / CLAUDE.md | ❌ | No `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.windsurfrules`, or `GEMINI.md` anywhere in the tree. |
| 2 | Best practices per-language | ❌ | One line in `README.md:288` — "Remember in your development to follow the PEP8 style guide. Your code editor likely has Python PEP8 linting packages…". flake8 config in `setup.cfg:17-19` (max-line-length=100). No dedicated style guide, no per-language tips dir. |
| 3 | Architecture + operational surface | ❌ | No `ARCHITECTURE.md`, no `docs/` directory at all. README is API usage only. No mention of: environments (dev/test/stage/prod base URLs), runtime hosting, observability, build & deploy. The Jenkinsfile exists at root but is undocumented; users of the SDK get no orientation on the publish path. |
| 4 | DB schema reference | ➖ | N/A — client SDK, no database. |
| 5 | CONTRIBUTING.md | ❌ | No `CONTRIBUTING.md`. README has a "For Rev AI Python SDK Developers" section (line 286) + "Local testing instructions" (line 290) but no PR/commit conventions, no review process, no branching model. |
| 6 | .env.example | ➖ | N/A — SDK consumes a user-supplied access token at construction time; no runtime env-config surface to template. README documents the access-token flow (line 27). |
| 7 | settings.json with pre-approved permissions | ❌ | No `.claude/` directory at all. |
| 8 | Skills directory | ❌ | No `.claude/skills/`, `.agents/skills/`, or `skills/`. |
| 9 | Skill-creator skill | ❌ | Item 8 fails; no skill infra to host one. |
| 10 | Hooks for deterministic checks | ❌ | No `.pre-commit-config.yaml`, no `.githooks/`, no `husky` config. Lint runs in CI only (`.github/workflows/build_test.yml:42-45`); no pre-merge or PostToolUse enforcement. |
| 11 | Hooks for agent friction | ❌ | None. |
| 12 | Tool-call telemetry | ❌ | No `CLAUDE_CODE_ENABLE_TELEMETRY`, no OTLP config, no collector. |

## Tier 2 — DX & Speed

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 13 | Single-command local dev setup | 🟡 | `Makefile` provides `make test` / `make test-all` / `make lint` / `make coverage`. `README.md:290-298` documents the 3-step path: `virtualenv ./sdk-test && . ./sdk-test/bin/activate && tox`. Documented, multi-step, no single `make dev`. |
| 14 | Fast linting (<30s) | ✅ | flake8 configured in `setup.cfg:17-19`, invoked in `Makefile:53-55` and `.github/workflows/build_test.yml:42-45`. CI run completes inside ~25 s total alongside tests. |
| 15 | Fast formatting (<20s) | ❌ | No formatter config — no `.prettierrc`/`pyproject.toml`/`black`/`ruff format`/`autopep8` config. flake8 is style-check only, not autoformat. No pre-commit hook would catch unformatted code. |
| 16 | Fast typecheck (<45s) | ➖ | N/A — no `mypy.ini`, `pyrightconfig.json`, or type-checking layer. Source has minimal type hints. |
| 17 | Reliable tests | ✅ | 21 test files in `tests/` covering apiclient, streaming, captions, custom vocab, async translation/summarization, LID, sentiment, topic extraction, models, utils. `tests/Dockerfile` for matrix testing. `tox.ini` runs pytest across Py 3.8–3.11. `README.md:290` documents how to run. No large `@pytest.mark.skip` blocks observed. |
| 18 | Fast CI (parallelize, cache, smart ordering) | ✅ | `.github/workflows/build_test.yml` — Py 3.8/3.9/3.10/3.11 matrix on `ubuntu-latest`. Phase 2: median duration **~25 s**, p95 ~29 s on `develop`. Well under the "Fast" 5-minute band. |
| 19 | Branch previews | ➖ | N/A — SDK library, not a deployable app. |

## Tier 3 — Advanced

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 20 | Skills marketplace | ❌ | No `.claude/settings.json`, no `enabledPlugins`/`extraKnownMarketplaces` config. |
| 21 | Specs as code | ➖ | N/A — this is a thin Python wrapper around the Rev.ai REST + WebSocket APIs; the canonical spec lives upstream (linked from `README.md:7` → `https://docs.rev.ai/sdk/python/`). No OpenAPI/GraphQL/Protobuf to maintain here. |
| 22 | MCP server configs | ❌ | No `.mcp.json`, no `mcpServers` in any settings file. |
| 23 | Agentic code review | 🔗→❌ | No `.cursor/`, `.coderabbit.yaml`, `.greptile*`, Bugbot config, or Claude Code Action workflow committed. Phase 2 confirmed: **0 bot reviewers/commenters across the last 20 merged PRs.** Reviewers are entirely human (`dmtrrk`, `kirillatrev`, `alexsku`, `k-weng`, `amikofalvy`, `aaron-wilson-rev`, `eugenep-rev`, `jennywong2129`, `beaudrychase`, etc.). |
| 24 | Other deterministic PR guardrails | 🟡 | `.github/workflows/stale.yml` (PRs, `actions/stale@v3`, 30/7 day TTL) + `.github/workflows/stale-branches.yml` (`fpicalausa/remove-stale-branches@v2.4.0`, 30/7 day TTL, feature/fix-prefix only) + `links_fail_fast.yml` (lychee on `**/*.md`, `**/*.html`, `**/*.py`) + `copyright-update.yml` (annual cron). **Org/UI-configured (no committed config):** CodeQL Analyze (fires on PRs — observed on PR #124), Dependabot pip ecosystem (open PR #125 bumping pytest, no `.github/dependabot.yml` in repo). No Semgrep, Chromatic, gitleaks, Snyk, Socket, or similar. Stale-hygiene present is a positive signal. |
| 25 | Agents in the cloud | ❌ | No `claude.yml`, `claude-code-review.yml`, Devin/Replit/Modal config. |
| 26 | Slack + issue-tracker integration | ✅ | Phase 2: **16/20 merged PRs reference a ticket** (`REVAI-4573`, `REVAI-4324`, `REVAI-3918`, `REVAI-3855`, `AISDK-235`, `AISDK-229`, `AISDK-221`, `AISDK-206`, `DOCS-298`). Primary tracker inferred: Linear (REVAI-/AISDK- prefixes). 4 unlabelled PRs are version-bump / housekeeping (#117 "DOCS-298: bump version" still counts; outliers are #110/#109 "Version bump", #103 "more updates", #102 "Update release", #98 license bot). No PR template committed. Slack notifications fire from Jenkinsfile to `#revai-alerts-nonprod` (`Jenkinsfile:127`). |

## External Validation (Phase 2)

### CI Timing (item 18)

| Workflow | Recent runs | Median | p95 | Success rate | Last run |
|---|---|---|---|---|---|
| `build_test.yml` (CI, Py 3.8–3.11 matrix) | 7 (develop branch only — small sample) | 25 s | 29 s | 4/7 (57%) — but 3 failures = 1 dependabot pytest-9.0.3 PR + 2 early commits on one feature branch later fixed | 2026-04-13 (failed dependabot PR) |
| `links_fail_fast.yml` (lychee) | 11 | 16 s | 24 s | 11/11 (100%) | 2026-04-13 |
| `stale-branches.yml` | 10 (last 10 days) | ~10 s | 15 s | 9/10 (90%) | 2026-05-12 |
| `stale.yml` | 0 on develop (cron-only) | — | — | — | — |
| `copyright-update.yml` | 0 | — | — | — | (annual cron, hasn't fired this cycle) |

All workflows comfortably inside the "Fast" band. Sample sizes are small because the repo's merge cadence is low (~1 PR/month).

### Agentic Code Review Activity (item 23)

| Tool | Status | Evidence |
|---|---|---|
| Claude Code Action | Not configured | No workflow, no bot reviewers detected. |
| CodeRabbit | Not configured | No `.coderabbit.yaml`, no `coderabbitai[bot]` comments. |
| Greptile / Bugbot / Sweep / Cursor | Not configured | No config, no bot signals. |

**Bots observed on PRs (last 20):** none. **Undiscovered-locally bots:** none.

### PR Guardrail Firing (item 24)

| Guardrail | Status | Evidence |
|---|---|---|
| CodeQL (org-level) | Verified firing | Check-run `CodeQL` + `Analyze (python)` + `Analyze (actions)` + `Upload Results` observed on PR #124 head SHA and merge commit. Not configured by a committed `codeql.yml` — likely "GitHub default setup" at org level. |
| Dependabot (org/UI-level) | Verified firing | Open PR #125 authored by `app/dependabot` (Bump pytest 6.2.5 → 9.0.3). No `.github/dependabot.yml` in repo. |
| Stale PRs (`actions/stale`) | Verified firing | Cron daily 09:25 UTC; workflow runs visible but not on the develop-branch list (cron runs aren't tied to a branch context the same way). |
| Stale branches (`fpicalausa/remove-stale-branches`) | Verified firing | 10/10 recent runs succeeded (one failure 2026-05-05). |
| Broken-link checker (lychee) | Verified firing | Fires on every push + PR; 11/11 success. |
| Semgrep / Snyk / gitleaks / Chromatic / Sonar / etc. | Not configured | No config files; no matching check-runs or comment bots. |

Comment-driven guardrails: none of brand `atlantis`, `tflint`, `tfsec`, `checkov`, `snyk`, `socket-security`, `gitguardian`, `sonarcloud`, `chromatic`, `percy`, `lighthouse-ci`, `codecov` observed across the 20-PR sample. Group B (`dependabot`, `renovate`, `mend-*`): dependabot is active but only against its own PRs (PR #125), which is expected and doesn't count toward gating per the matcher rule.

### Cloud Agent Usage (item 25)

| Workflow | 30d runs | 7d runs | Success rate | Last invoked |
|---|---|---|---|---|
| (none configured) | — | — | — | — |

### Issue Tracker Linkage (item 26)

- **Ticket linkage rate:** 16/20 recent merged PRs (80%)
- **Tracker inferred:** Linear (`REVAI-*`, `AISDK-*`, `DOCS-*` prefixes — `AISDK-*` is an older Jira project, `REVAI-*`/`DOCS-*` are Linear-era)
- **PR template references ticket ID:** No (no PR template committed in `.github/`)
- **Rework / suffixed-ID pattern:** Some near-duplicate REVAI-3918 PRs (#107, #108, #109, #110) suggest version-bump rework; AISDK-206 reused across #93, #94. Worth a glance but not unusual for an SDK.

### Jenkins (item 18 supplement; Step 10)

| Job | Type | Recent builds | Success rate | Median / p95 | Last run | Notes |
|---|---|---|---|---|---|---|
| `Rev.ai SDK Python pipeline` | `WorkflowJob` (pipeline, single-branch) | 4 | **0/4 (0%)** | 3.3 m / 3.8 m | 2024-11-27 | All 4 most-recent builds **FAILURE**. Pipeline runs on tag push to publish to PyPI per `Jenkinsfile` — Build → Test → Version Check → Deploy. Either the publish has been done manually since #124 merged in March 2026, the pipeline has been silently broken for 14+ months, or the SDK has had no release in that window. **Surface as a recent stability incident.** |

No multi-branch feature pipeline detected for this repo. No `*-feature-test` job matched.

## Known External Systems (captured, not validated in this version)

| Category | System | Config location | Notes |
|---|---|---|---|
| Release pipeline | Jenkins | `Jenkinsfile` (root) + Jenkins job `Rev.ai SDK Python pipeline` | Probed; broken — see above. |
| Slack notifications | Slack channel `CFPMB0BK4` (= `#revai-alerts-nonprod`) | `Jenkinsfile:127` | Hardcoded channel ID; only fires on FAILURE→SUCCESS or SUCCESS→FAILURE transitions. |
| Code scanning | GitHub CodeQL | Org-level / GitHub default setup | No `.github/codeql/*.yml` in repo; verified firing on PR #124. |
| Dependency bumps | Dependabot (pip) | GitHub repo settings UI (no `.github/dependabot.yml`) | Verified open PR #125. |
| Stale automation | `actions/stale` + `fpicalausa/remove-stale-branches` | `.github/workflows/stale.yml`, `.github/workflows/stale-branches.yml` | Both verified firing. |
| Link rot | `lycheeverse/lychee-action` | `.github/workflows/links_fail_fast.yml` + `.lycheeignore` | Verified firing on every push + PR. |
| Copyright bump | `FantasticFiasco/action-update-license-year` | `.github/workflows/copyright-update.yml` | Annual cron — hasn't fired in audit window. |

## Residual Unknowns

- **Jenkins pipeline FAILUREs vs. actual release cadence.** With 0/4 recent Jenkins builds passing but PR #124 merged on 2026-03-04 and a `Bump pytest` PR open on 2026-04-13, it's unclear whether a release went out for #124 and how — manual `twine upload` from a maintainer's machine, a different (unlisted) Jenkins job, or no release at all. Worth a maintainer asking. (Skill does not propose fixes; this is a pointer.)
- **`._Makefile` macOS resource-fork file is tracked at repo root** (`ls -la` shows it as a 4096-byte file). Likely accidental — should probably be gitignored and removed. Surfaced as a hygiene note.
- **`test.py` at repo root** is a one-line `import src.rev_ai.apiclient as client` — looks like a leftover scratch file, not in `tests/`. Surfaced as a hygiene note.
- **`HISTORY.rst` last-updated state vs `bumpversion` config.** `setup.cfg:2` declares `current_version = 2.20.0`; `src/rev_ai/__init__.py` carries the canonical `__version__`. Whether HISTORY.rst is being kept in sync at each bump is not visible from a read-only audit. Possible drift risk.
- **No PR template** in `.github/`. The 80% ticket-linkage rate comes from convention, not enforcement — a template that mentions the ticket ID would lift it further at zero cost.
- **CI matrix is Py 3.8–3.11** but the broader Python ecosystem has moved past 3.8 (EOL Oct 2024). Not a readiness-checklist item per se, but a contributor reading `tox.ini:2` may be unsure whether 3.8 is still a real support target.

## Detailed Findings

### Why "Early" and not "Developing"

The scoring rubric ("Strong: ≥70% PASS AND ≤1 Tier-1 FAIL"; "Developing: ≥40% PASS AND ≤3 Tier-1 FAILs") puts this repo firmly in Early on both axes: 19% PASS and 10 Tier-1 FAILs. The bands are intentionally strict, but the read of this repo is unambiguous — it predates the agent-readiness vocabulary entirely. There is no `.claude/` directory, no AGENTS.md, no CONTRIBUTING.md, no architecture doc, no formatter, no pre-commit. Everything an agent (or a new human contributor) would need to be productive in a few days without asking lives implicitly in the maintainers' heads.

### What this repo does well

Despite landing in Early on the rubric, the repo's runtime fundamentals are solid and would be a fast lift to upgrade:

- **CI is genuinely fast and reliable.** ~25 second matrix build across 4 Python versions is in the top decile.
- **Test suite is substantial and runnable.** 21 test files, tox + pytest, documented run path, a dedicated `tests/Dockerfile` for matrix-Python coverage. Closing item 17 was clearly a priority for the original maintainers.
- **Ticket discipline is high (80%).** This is convention-driven, not enforced — even better signal for the team's habits.
- **Stale-PR and stale-branch automation is a sophisticated touch** for a small SDK. The org-wide rollout note in `stale-branches.yml:1-3` shows this came from a deliberate hygiene initiative.
- **CodeQL + Dependabot quietly running at the org level** mean the repo is meaningfully more guarded than its committed configs would suggest. Worth flagging in any future CLAUDE.md so contributors know what's actually gating their PRs.

### What's missing (knowledge cluster)

Items 1–6: the knowledge cluster is 0/4 PASS, 4 FAIL (with 4 and 6 legitimately N/A). For an SDK, the highest-leverage doc to add is a CLAUDE.md/AGENTS.md that compresses the architectural shape — five entry-point clients (`apiclient.RevAiAPIClient` for async, `streamingclient.RevAiStreamingClient` for WebSocket, plus per-feature clients for custom vocab, LID, sentiment, topic extraction), the `models/` module organisation (`asynchronous/` for job/transcript/summary/translation, top-level for streaming + shared types), and the `BaseClient` inheritance pattern. A contributor today reads `apiclient.py` and `streamingclient.py` to figure out what kind of repo this is — a 50-line orientation file removes that cost.

### What's missing (tooling cluster)

Items 7–12: 0/6 PASS, 6 FAIL. This is where the repo's age shows most. None of these existed as common patterns when the repo was set up. The lowest-friction sequence:

1. Drop in `.claude/settings.json` with a curated `permissions.allow` for the actual commands an agent needs: `Bash(pytest:*)`, `Bash(tox:*)`, `Bash(flake8:*)`, `Bash(python -m pip install:*)`, `Bash(python setup.py:*)`, `Bash(make:*)`. (Item 7.)
2. Add `.pre-commit-config.yaml` running flake8 with the same ignores as `Makefile:53-55` (`F401,W504,E731,E123,E125,E127,E128,E501`). (Items 10, partial 14.)
3. A `.claude/skills/` directory with a single tip file describing how to test a change end-to-end (matrix run, the `src/` layout, the `bumpversion` config) closes 8 (and gives 11 a place to live later).

### What's missing (release cadence)

The Jenkins pipeline situation is the most concrete operational gap surfaced by the audit. 4 builds in two years, all failing, while merges to `develop` continue — either the release path is undocumented + manual, or releases have stopped. A new contributor asking "how does this code get to PyPI?" gets no answer from the repo; the `Jenkinsfile` itself describes a flow that hasn't completed successfully in the visible history. This belongs in the architecture doc the audit's item-3 FAIL is pointing at.

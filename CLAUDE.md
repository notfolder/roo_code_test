# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 言語ルール

**すべての応答・ドキュメント・コード上のコメントは日本語で記述すること。**

## Project Overview

This is a testing repository for an AI-driven waterfall development workflow. The goal is to automate software development by chaining three AI agent phases: requirements definition → detailed design → implementation. All documentation, comments, and responses should be in **Japanese**.

## Agent Workflow

The `agents/` directory contains three prompt definitions used as system prompts for AI agents:

| Agent File | Role | Output |
|---|---|---|
| `REQUREMENTS_DEFINITION_AGENT.md` | IT requirements specialist | Requirements doc → `doc/` directory |
| `DESIGN_SPEC_AGENT.md` | System engineer (design) | Detailed design doc → `doc/` directory |
| `CODING_AGENT.md` | System engineer (implementation) | Full source code based on design |

Execute these phases sequentially. Each agent's output becomes the input for the next phase.

## Technology Stack Preferences (from agents)

When generating designs and code, follow these defaults defined in the agent prompts:

- **Language**: Python (unless otherwise required)
- **Simple GUI**: Streamlit
- **Complex UI**: Vue (Vuetify) + FastAPI backend
  - Frontend: multi-stage Docker build (npm build → nginx)
  - Backend: proxied by nginx at `/api/` endpoints
  - Frontend makes all API requests to `/api/`
- **Database**: PostgreSQL
- **Infrastructure**: Docker Compose (mandatory for all deployments)
- **DB initialization**: Auto-execute schema creation and initial data seeding on startup

## Key Constraints for All Generated Code

- No code abbreviations or mockups — all code must be complete and functional
- Comments in Japanese throughout all source files
- Every class, function, and file must have Japanese comments following the defined coding conventions
- Self-review required after every creation/modification: check for mockups, redundant code, impact on related code
- No future extension plans in documentation — only current requirements
- Docs in `doc/` directory; startup instructions in `README.md`

## Agent Execution Rules

- Requirements and design agents iterate in a create → validate → modify loop until complete
- Each agent must report completeness review results before finishing
- Contradict or gap findings must always be reported
- Minimal user confirmation — only ask when external integration details are genuinely unknown
- Redundant code/design must be identified and eliminated; shared logic must be centralized in dedicated modules

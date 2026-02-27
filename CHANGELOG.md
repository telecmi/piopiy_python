# CHANGELOG

## [1.2.1] - 2026-02-27

### Added
- Created unified `RestClient` for simpler SDK instantiation.
- Added comprehensive examples for `ai_agent`, `voice_call`, and `pcmo_call` actions.
- Included full API documentation within `docs/examples/`.
- Introduced `SDK_RESTRUCTURE.md` to document validation schemas and payload structures.
- Added explicit PCMO action structures (Play, Record, Get Input, Hangup, Connect).

### Changed
- Refactored `AIAgent`, `Hangup` (Voice), `PCMO`, and `Flow` into a modular package structure.
- Cleaned up obsolete markdown files (`STREAM.md`, `STREAM_ACTION.md`).
- Enhanced PyPI metadata in `setup.py` (added keywords, project links, excluded docs/examples from build).
- Improved main `README.md` with clear quickstart instructions and prerequisite information.
- Updated root `client.py` to route all resources through a central HTTP client connection.

### Fixed
- Fixed version numbering consistency.
- Resolved documentation ambiguities regarding failover requirements.

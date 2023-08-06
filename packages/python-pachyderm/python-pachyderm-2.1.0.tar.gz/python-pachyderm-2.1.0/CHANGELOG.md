# Changelog

## 2.1.0

- Added support for admin (PR #139)
- Added support for transactions (PR #138)
- Expose `spout` parameter for `create_pipeline`  (PR #137)

## 2.0.0

- Major, backwards-incompatible refactor. The largest change is to move all functionality into a single `Client` class. See this PR for more details: https://github.com/pachyderm/python-pachyderm/pull/129

## 1.9.7

- Synced with pachyderm core v1.9.7
- Note that this is the last version that will be pinned to pachyderm core versions. Future revisions will rely on semver. See the readme for details.

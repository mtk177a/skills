#!/usr/bin/env bash
set -euo pipefail

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

info() {
  printf '[refresh-apm-lockfile] %s\n' "$*"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

assert_clean_working_repo() {
  local status
  status="$(git status --porcelain=v1 --untracked-files=all)"
  [[ -z "$status" ]] || die "working tree is not clean:
$status"

  [[ ! -e apm_modules ]] || die "apm_modules exists; remove APM deployment artifacts before refreshing the lockfile"

  if [[ -d .agents/skills ]]; then
    local deployed_skill
    deployed_skill="$(find .agents/skills -mindepth 1 -maxdepth 1 ! -name refresh-apm-lockfile -print -quit)"
    [[ -z "$deployed_skill" ]] || die "APM-deployed skill artifact exists: $deployed_skill"
  fi
}

count_manifest_deps() {
  grep -cE '^    - ' "$ROOT/apm.yml" || true
}

count_lock_deps() {
  grep -cE '^  virtual_path: ' "$1/apm.lock.yaml" || true
}

public_source_requires_refresh() {
  local lock="$ROOT/apm.lock.yaml"
  local locked_commits
  local locked_commit_count

  if [[ "$(count_lock_deps "$ROOT")" != "$EXPECTED_DEPS" ]]; then
    info "public source delta: refresh required (manifest and lockfile dependency counts differ)"
    return 0
  fi

  locked_commits="$(awk '/^[[:space:]]*resolved_commit:/ {print $2}' "$lock" | sort -u)"
  locked_commit_count="$(printf '%s\n' "$locked_commits" | awk 'NF {count++} END {print count + 0}')"
  if [[ "$locked_commit_count" != "1" ]]; then
    info "public source delta: refresh required (lockfile does not have one common source commit)"
    return 0
  fi

  if ! git cat-file -e "$locked_commits^{commit}" 2>/dev/null; then
    info "public source delta: refresh required (recorded source commit is unavailable locally)"
    return 0
  fi

  LOCK_BASE_SHA="$locked_commits"
  if git diff --quiet "$locked_commits" "$HEAD_SHA" -- apm.yml skills; then
    info "public source delta: no refresh required"
    info "recorded source commit: $LOCK_BASE_SHA"
    return 1
  fi

  info "public source delta: refresh required"
  info "recorded source commit: $LOCK_BASE_SHA"
  return 0
}

lock_matches_head() {
  local repo_dir="$1"
  local expected_deps="$2"
  local lock="$repo_dir/apm.lock.yaml"

  [[ -f "$lock" ]] || return 1
  [[ "$(count_lock_deps "$repo_dir")" = "$expected_deps" ]] || return 1
  [[ "$(grep -c "resolved_commit: $HEAD_SHA" "$lock" || true)" = "$expected_deps" ]] || return 1
}

require_command git
require_command apm
require_command grep
require_command mktemp
require_command cp
require_command rm
require_command awk
require_command find
require_command sort

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

[[ -f apm.yml ]] || die "apm.yml not found at repository root"
[[ -f apm.lock.yaml ]] || die "apm.lock.yaml not found at repository root"

assert_clean_working_repo

UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)" || die "current branch has no upstream"
LOCAL_SHA="$(git rev-parse HEAD)"
UPSTREAM_SHA="$(git rev-parse "$UPSTREAM")"
[[ "$LOCAL_SHA" = "$UPSTREAM_SHA" ]] || die "HEAD is not pushed to upstream ($UPSTREAM)"

HEAD_SHA="$LOCAL_SHA"
EXPECTED_DEPS="$(count_manifest_deps)"
[[ "$EXPECTED_DEPS" -gt 0 ]] || die "no APM dependencies found in apm.yml"

apm lock --help >/dev/null 2>&1 || die "installed APM CLI does not support 'apm lock'; update APM before refreshing the lockfile"

info "preconditions: passed"
info "repository: $ROOT"
info "upstream: $UPSTREAM"
info "head: $HEAD_SHA"
info "expected dependencies: $EXPECTED_DEPS"

if ! public_source_requires_refresh; then
  info "disposable copy: not created"
  info "APM command used: not run"
  info "resolved commit in lockfile: $LOCK_BASE_SHA"
  info "working repository diff: none"
  info "next: no lockfile commit is needed"
  exit 0
fi

TMP_PARENT="$(mktemp -d /tmp/agent-skills-apm-lock.XXXXXX)"
TMP_REPO="$TMP_PARENT/repo"
KEEP_TMP=1

cleanup() {
  if [[ "${KEEP_TMP:-0}" = "0" ]]; then
    rm -rf "$TMP_PARENT"
  else
    printf '[refresh-apm-lockfile] kept disposable copy for inspection: %s\n' "$TMP_PARENT" >&2
  fi
}
trap cleanup EXIT

info "disposable copy: $TMP_REPO"

git clone "$ROOT" "$TMP_REPO"

APM_COMMAND='apm lock --update --no-policy'
info "running in disposable copy: $APM_COMMAND"
(
  cd "$TMP_REPO"
  apm lock --update --no-policy
)

lock_matches_head "$TMP_REPO" "$EXPECTED_DEPS" || die "disposable lockfile does not match HEAD or dependency count after APM refresh"

info "verifying in disposable copy: apm install --frozen --no-policy"
(
  cd "$TMP_REPO"
  apm install --frozen --no-policy
)

info "verifying in disposable copy: apm audit --ci --no-policy"
(
  cd "$TMP_REPO"
  apm audit --ci --no-policy
)

lock_matches_head "$TMP_REPO" "$EXPECTED_DEPS" || die "verified disposable lockfile no longer matches HEAD or dependency count"

cp "$TMP_REPO/apm.lock.yaml" "$ROOT/apm.lock.yaml"

CHANGED_FILES="$(git diff --name-only)"
if [[ -z "$CHANGED_FILES" ]]; then
  LOCKFILE_CHANGED=0
elif [[ "$CHANGED_FILES" = "apm.lock.yaml" ]]; then
  LOCKFILE_CHANGED=1
else
  die "unexpected working repository diff after copy: $CHANGED_FILES"
fi

info "verifying: apm install --frozen --dry-run --no-policy"
apm install --frozen --dry-run --no-policy

info "verifying: git diff --check"
git diff --check

RESOLVED="$(grep -m 1 'resolved_commit:' apm.lock.yaml | awk '{print $2}')"
info "resolved commit in lockfile: $RESOLVED"
info "APM command used: $APM_COMMAND"
if [[ "$LOCKFILE_CHANGED" = "1" ]]; then
  info "working repository diff:"
  git diff --stat -- apm.lock.yaml
  info "next:"
  printf '  git add apm.lock.yaml\n'
  printf '  git commit -m "fix: refresh APM lockfile after <change>"\n'
else
  info "working repository diff: none"
  info "apm.lock.yaml already matches the current pushed HEAD; no commit is needed"
fi

KEEP_TMP=0

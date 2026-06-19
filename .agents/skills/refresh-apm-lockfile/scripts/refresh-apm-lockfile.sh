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

info "repository: $ROOT"
info "upstream: $UPSTREAM"
info "head: $HEAD_SHA"
info "expected dependencies: $EXPECTED_DEPS"
info "disposable copy: $TMP_REPO"

git clone "$ROOT" "$TMP_REPO"

APM_COMMAND='apm update --yes'
info "running in disposable copy: $APM_COMMAND"
(
  cd "$TMP_REPO"
  apm update --yes
)

if ! lock_matches_head "$TMP_REPO" "$EXPECTED_DEPS"; then
  APM_COMMAND='apm install --update --ssh --no-policy'
  info "lockfile was not refreshed by apm update; running fallback: $APM_COMMAND"
  (
    cd "$TMP_REPO"
    apm install --update --ssh --no-policy
  )
fi

lock_matches_head "$TMP_REPO" "$EXPECTED_DEPS" || die "disposable lockfile does not match HEAD or dependency count after APM refresh"

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

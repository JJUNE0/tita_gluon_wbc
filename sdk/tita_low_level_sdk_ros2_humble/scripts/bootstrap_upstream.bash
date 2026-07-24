#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_root="${1:-${repo_root}/direct_ws/src}"
upstream="${source_root}/ddt_ros2_control"
expected_commit="e7b32d9746df900680641ff2845ffb0b5ffe99ed"
expected_start_hash="0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3"

mkdir -p "${source_root}"
if [[ ! -d "${upstream}/.git" ]]; then
  if command -v vcs >/dev/null; then
    vcs import "${source_root}" < "${repo_root}/ros2.repos"
  else
    command -v git >/dev/null || {
      echo "git or vcs is required" >&2
      exit 1
    }
    git clone https://github.com/DDTRobot/ddt_ros2_control.git "${upstream}"
    git -C "${upstream}" checkout --detach "${expected_commit}"
  fi
fi

actual_commit="$(git -C "${upstream}" rev-parse HEAD)"
if [[ "${actual_commit}" != "${expected_commit}" ]]; then
  echo "Refusing overlay: upstream HEAD ${actual_commit} != ${expected_commit}" >&2
  exit 1
fi

rsync -a "${repo_root}/upstream_overlay/ddt_ros2_control/" "${upstream}/"

actual_start_hash="$(sha256sum "${upstream}/start.bash" | awk '{print $1}')"
if [[ "${actual_start_hash}" != "${expected_start_hash}" ]]; then
  echo "Official start.bash hash mismatch: ${actual_start_hash}" >&2
  exit 1
fi

echo "Pinned upstream and production overlay are ready."
echo "upstream_commit=${actual_commit}"
echo "start_bash_sha256=${actual_start_hash}"

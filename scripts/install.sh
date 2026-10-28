#!/usr/bin/env bash
# Project-local installation. Never overwrite an existing skill or agent.
set -euo pipefail

if [[ $# -ne 1 || ! -d "$1" ]]; then
  echo "用法：bash scripts/install.sh <已存在的目标项目目录>" >&2
  exit 1
fi

source_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
target_root="$(cd -- "$1" && pwd -P)"
skill_target="$target_root/.agents/skills/ui-review"
agent_target="$target_root/.codex/agents"
roles=(visual-reviewer ux-reviewer design-system-reviewer)
destinations=("$skill_target")
for role in "${roles[@]}"; do
  destinations+=("$agent_target/$role.toml")
done

for destination in "${destinations[@]}"; do
  if [[ -e "$destination" || -L "$destination" ]]; then
    echo "拒绝覆盖已有安装：$destination" >&2
    exit 1
  fi
done

# Check sources before making target directories.
test -f "$source_root/ui-review/SKILL.md"
for role in "${roles[@]}"; do
  test -f "$source_root/.codex/agents/$role.toml"
done

mkdir -p -- "$target_root/.agents/skills" "$agent_target"
cp -R -- "$source_root/ui-review" "$skill_target"
for role in "${roles[@]}"; do
  cp -- "$source_root/.codex/agents/$role.toml" "$agent_target/$role.toml"
done

echo "已安装 Skill 与三个角色到：$target_root"
echo "请在目标项目根目录启动："
echo "codex --enable multi_agent --sandbox read-only --ask-for-approval never"

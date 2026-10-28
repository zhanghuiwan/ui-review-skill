#!/usr/bin/env python3
"""Validate repository contracts and installation without invoking a model."""

import re
import subprocess
import tempfile
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    "visual-reviewer": "visual_reviewer",
    "ux-reviewer": "ux_reviewer",
    "design-system-reviewer": "design_system_reviewer",
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def snapshot(root):
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def install(target):
    return subprocess.run(
        ["bash", str(ROOT / "scripts/install.sh"), str(target)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def main():
    skill = ROOT / "ui-review"
    text = (skill / "SKILL.md").read_text()
    header = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    require(header, "SKILL.md 缺少 frontmatter")
    # Deliberately check this project's simple, one-line YAML metadata contract.
    metadata = dict(line.split(": ", 1) for line in header[1].splitlines())
    require(metadata.get("name") == "ui-review", "Skill 名称与安装目录不一致")
    require(bool(metadata.get("description", "").strip()), "Skill 缺少描述")

    for stem, role_name in ROLES.items():
        path = ROOT / ".codex/agents" / f"{stem}.toml"
        config = tomllib.loads(path.read_text())
        require(
            set(config) == {"name", "description", "developer_instructions"},
            f"意外的角色字段：{path}",
        )
        require(config["name"] == role_name, f"角色名称不一致：{path}")
        require(bool(config["description"].strip()), f"角色描述为空：{path}")
        instructions = config["developer_instructions"]
        require("只读" in instructions, f"缺少只读边界：{path}")
        for reference in [f"{stem}.md", "report-template.md"]:
            require((skill / "references" / reference).is_file(), f"引用缺失：{reference}")
            require(f"references/{reference}" in instructions, f"角色引用不一致：{path}")
        require(role_name in text, f"Skill 未包含角色：{role_name}")

    for markdown in [ROOT / "README.md", *skill.rglob("*.md"), *(ROOT / "docs").rglob("*.md")]:
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", markdown.read_text()):
            if "://" not in link and not link.startswith("#"):
                require((markdown.parent / link.split("#", 1)[0]).exists(), f"断开的引用：{markdown}: {link}")

    with tempfile.TemporaryDirectory(prefix="ui-review-install-") as directory:
        project = Path(directory) / "target project & review"
        project.mkdir()
        (project / "business.txt").write_text("user content\n")
        (project / ".codex").mkdir()
        (project / ".codex/config.toml").write_text("# existing user config\n")
        before = snapshot(project)
        result = install(project)
        require(result.returncode == 0, result.stderr)
        installed = project / ".agents/skills/ui-review"
        require(snapshot(installed) == snapshot(skill), "Skill 安装不完整")
        for stem in ROLES:
            relative = Path(".codex/agents") / f"{stem}.toml"
            require((project / relative).read_bytes() == (ROOT / relative).read_bytes(), f"角色安装错误：{stem}")
        after = snapshot(project)
        require(all(after[path] == data for path, data in before.items()), "安装改动了原有文件")
        require(install(project).returncode != 0, "重复安装应拒绝覆盖")
        require(snapshot(project) == after, "拒绝覆盖时仍改动了目标项目")
        require(install(Path(directory) / "missing").returncode != 0, "应拒绝不存在的目标")

        conflict = Path(directory) / "conflict"
        (conflict / ".codex/agents").mkdir(parents=True)
        (conflict / ".codex/agents/ux-reviewer.toml").write_text("# user role\n")
        before_conflict = snapshot(conflict)
        require(install(conflict).returncode != 0, "已有角色应在复制前触发拒绝")
        require(snapshot(conflict) == before_conflict, "角色冲突时仍复制了文件")
        require(not (conflict / ".agents").exists(), "角色冲突后留下了部分 Skill 安装")

    print("PASS: Skill 元数据、3 个 TOML 角色、本地引用与安装契约检查")
    print("PASS: 含空格路径安装、原文件保护、重复安装、角色冲突及无效目标检查")
    print("未执行模型调用、子 Agent 审查或浏览器测试。")


if __name__ == "__main__":
    main()

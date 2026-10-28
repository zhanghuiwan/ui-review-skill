# UI Review Skill

一个面向 Codex 的中文 UI 审查 Skill，从视觉设计、用户体验和 Design System 三个视角审查截图、已运行页面或前端源码，输出有证据、分优先级的改进建议。

默认只读：不修改被审查项目，不自动修复。只需安装 Skill，无需配置独立 Agent。

## 安装

需要已安装 Node.js 和 npm。在需要使用 Skill 的项目目录中执行：

```bash
npx skills add zhanghuiwan/ui-review-skill
```

按提示选择 `ui-review` 和 Codex。也可以直接指定：

```bash
npx skills add zhanghuiwan/ui-review-skill --skill ui-review --agent codex
```

安装后重新打开 Codex 会话，使用 `$ui-review` 调用。安装由 [skills CLI](https://github.com/vercel-labs/skills) 管理，本仓库不提供额外安装脚本。

> 上述仓库简称从默认分支安装；当前变更合并到 `main` 后才可用。合并前可先克隆本次功能分支，在仓库目录执行 `npx skills add . --skill ui-review --agent codex` 试用。

## 使用

审查截图：

```text
$ui-review 请审查我附上的桌面和移动端截图，关注层级、间距、可读性与组件一致性。
只根据可见证据下结论，在对话中返回中文报告，不修改文件。
```

审查已运行页面：

```text
$ui-review 请审查我提供的测试页面，重点检查购物车到支付确认的任务路径。
只做安全的只读检查，不提交订单；无法验证的交互请明确说明。
```

审查源码：

```text
$ui-review 请只读检查 src/components 和 src/styles 的表单、按钮与设计令牌。
引用实际源码位置；没有运行页面时，将渲染与交互效果标为未验证。
```

Skill 会依次读取三份审查指导，合并重复发现，并按 [报告模板](ui-review/references/report-template.md) 输出位置、证据、影响、P0–P3 级别、建议与验收标准。浏览器与模型访问由所在客户端提供；截图或源码不能替代真实交互和无障碍测试。

## 内容

```text
ui-review/
├── SKILL.md
└── references/
    ├── visual-reviewer.md
    ├── ux-reviewer.md
    ├── design-system-reviewer.md
    └── report-template.md
```

[SKILL.md](ui-review/SKILL.md) 定义审查流程与只读边界；`references/` 是 Skill 使用的审查指导和报告模板。

## 许可证

[MIT](LICENSE)。

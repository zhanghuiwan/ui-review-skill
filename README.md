# Codex UI Review Skill

面向开发者的中文 Codex Skill，用可追溯的证据审查 UI、用户体验与 Design System，输出可执行的改进建议。适用于页面截图、已运行的 Web 界面以及前端源码审查。

这是社区项目，与 OpenAI 无隶属关系。项目提供提示词、原生角色配置和报告模板，不包含浏览器、模型服务或自动修复工具。

## 功能特点

- **三种专业视角**：视觉层级与响应式、任务流程与无障碍、组件与设计令牌一致性。
- **证据优先**：每个发现注明页面状态、截图区域、复现步骤或源码位置，区分观察、推断与待验证事项。
- **默认只读**：主审查与三个角色只输出建议，不自行修改被审查项目或执行有副作用的操作。
- **统一报告**：按 P0–P3 分级，记录影响、置信度、建议、验收标准及覆盖限制。
- **可降级运行**：有原生子 Agent 时按角色委派；不支持时由主 Agent 依次采用三个视角，并明确说明执行方式。

## 环境与兼容性

- 安装需要 Git、Bash，以及一个已经存在的目标项目目录。仓库校验脚本需要 Python 3.11+，不依赖第三方 Python 包。
- 本项目配置以 **Codex CLI 0.163.0** 为验证基线，不声明最低兼容版本。其他版本与 IDE／云端客户端请先确认 Skill 和自定义子 Agent 支持情况。
- 使用 Codex 需要自行配置可用的模型访问。真实页面交互还需要所在客户端提供浏览器工具及所需访问权限；本项目不会自动安装浏览器或授予网络权限。
- 只有截图时可以审查视觉表现，不能确认实际交互、键盘行为或屏幕阅读器表现。只有源码时不能宣称已验证渲染效果。

### 已核对的原生规则

| 项目 | 本项目采用的方式 |
| --- | --- |
| 项目级 Skill | `<目标项目>/.agents/skills/ui-review/SKILL.md`，必需的 YAML 字段为 `name`、`description` |
| 原生自定义角色 | `<目标项目>/.codex/agents/*.toml`，包含 `name`、`description`、`developer_instructions` |
| 引用文件 | 保留在 Skill 的 `references/` 下；由 Skill 或角色显式读取，不会自动展开提示词中的路径 |
| 只读权限 | 主会话以 `--sandbox read-only --ask-for-approval never` 启动，子角色继承会话权限；角色提示词也禁止写操作 |

**不要仅在角色 TOML 中写 `sandbox_mode` 就认为隔离已生效。** 在 0.163.0 的角色覆盖实现中，它不属于被应用的覆盖字段。本项目不添加这个容易误导的字段，也不固定模型、推理等级或未经验证的工具权限字段。必须使用下方只读启动命令。沙箱主要限制本地文件写入，不能代替对浏览器或外部工具的副作用约束。

官方依据：[Skills 文档](https://developers.openai.com/codex/skills)、[子 Agent 文档](https://developers.openai.com/codex/subagents)、[0.163.0 角色文件解析](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/agent-roles/src/agent_role_config.rs)、[角色发现](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/agent-roles/src/loader.rs)、[角色覆盖实现](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core/src/agent/role.rs)。升级 Codex 后应重新验证。

## 安装

### 1. 获取项目

在一个尚不存在 `ui-review-skill` 子目录的位置执行：

```bash
git clone https://github.com/zhanghuiwan/ui-review-skill.git
cd ui-review-skill
```

### 2. 安装到需要审查的项目

将下面的绝对路径替换为真实、已存在的项目目录：

```bash
bash scripts/install.sh /absolute/path/to/your-project
```

安装脚本会复制完整 Skill 和三个原生角色文件；不会修改目标项目的业务代码、依赖或 `.codex/config.toml`。若任一安装目标已存在，会在复制前退出，避免覆盖已有配置。更新时请先备份并检查已有安装，再自行合并或移走旧文件；脚本不提供强制覆盖选项。

安装结果：

```text
your-project/
├── .agents/skills/ui-review/
│   ├── SKILL.md
│   └── references/
│       ├── visual-reviewer.md
│       ├── ux-reviewer.md
│       ├── design-system-reviewer.md
│       └── report-template.md
└── .codex/agents/
    ├── visual-reviewer.toml
    ├── ux-reviewer.toml
    └── design-system-reviewer.toml
```

这是项目级安装，不会自动注册为全局 Skill。请遵守目标项目对 `.agents`／`.codex` 文件的版本管理约定。

### 3. 启动只读审查

在目标项目根目录执行：

```bash
codex --version
codex --enable multi_agent --sandbox read-only --ask-for-approval never
```

仅对你信任的项目按 Codex 的提示确认项目信任，否则项目级角色配置可能不加载。安装后请重新启动会话；在支持 Skill 选择的客户端中确认能看到 `ui-review`，再输入下方示例。若当前平台禁止自定义角色或子 Agent，按 Skill 的单 Agent 降级流程运行，不必改变平台策略。

不需要三个角色并发就能使用 Skill。原生子 Agent 的实际创建取决于客户端工具、会话策略和可用并发额度；安装角色文件不代表三个角色已经执行。

## 使用示例

### 审查已运行页面

```text
$ui-review 请审查我已提供的测试页面和结账流程。
目标：让首次购买用户顺利完成下单。
范围：购物车 → 地址 → 支付确认；桌面和移动端。
请先确认你能使用的浏览器工具，只做只读检查，不提交真实订单。
如果原生子 Agent 可用，请分别委派 visual_reviewer、ux_reviewer、
design_system_reviewer，最后合并为中文报告。
```

页面地址、测试账号与允许的操作范围应在真实任务中补充。登录由用户自行在受支持的工具中完成，不要将凭据写入报告。

### 审查截图

```text
$ui-review 请审查我附上的桌面和移动端截图，重点关注层级、间距、
可读性与组件一致性。只根据可见证据下结论，交互和无障碍检查标为待验证。
请在对话中返回报告，不修改文件。
```

### 审查前端源码

```text
$ui-review 请只读检查 src/components 和 src/styles 中的按钮、表单、
设计令牌和状态实现。先阅读项目规范，不运行安装、构建或自动修复命令。
如果没有运行页面，请把渲染和交互效果标为未验证，并引用实际源码位置。
```

### 没有原生子 Agent 时

```text
$ui-review 当前环境不提供子 Agent。请由你依次使用视觉、UX 和 Design System
三个视角审查，并在报告中标明“单 Agent 多视角审查”，不要编造子 Agent 记录。
```

## 工作流程

1. 确定用户任务、审查范围、设备与页面状态，读取已有设计规范。
2. 清点可用证据与工具；记录无法访问的页面及不能执行的检查。
3. 在已授权的安全范围内采集证据，然后按三种视角审查。
4. 合并同一根因的发现，按影响与证据强度排序，不以个人审美替代项目规范。
5. 使用 [报告模板](ui-review/references/report-template.md) 在对话中返回结果。需要修复时另开明确授权的实现任务。

审查期间不安装依赖、不启动会产生输出文件的构建，不替用户提交表单、发消息、下单或变更远程数据。需要运行环境时请用户先准备；截图只使用工具允许的临时位置，不写入被审查项目。

## 审查报告示例

> 以下是虚构的格式示例，不是本仓库或某个真实产品的测试结果。

**范围**：地址表单移动端截图。**执行方式**：单 Agent 多视角。**证据**：用户提供的截图 S1，390 × 844。**未验证**：页面运行、键盘与读屏、真实设备。

| ID | 级别 | 发现 | 证据 | 置信度 |
| --- | --- | --- | --- | --- |
| UI-001 | P2 | 错误信息未指向具体地址字段 | S1，地址表单顶部与字段区域 | 中 |

**UI-001：错误定位信息不足**

- 观察：S1 中只出现表单顶部的“地址无效”，可见字段附近没有对应说明。
- 影响：用户可能需要反复猜测哪个字段应修改；无法仅凭截图确认是否存在程序化错误关联。
- 建议：在无效字段旁说明错误原因，提交后提供可定位到字段的错误摘要。
- 验收：通过浏览器检查无效提交后可定位具体字段；键盘焦点顺序合理，错误信息与字段关联可被辅助技术识别。
- 待验证：DOM 关联、焦点行为、实际错误文案和读屏输出。

没有充分证据时应写“待验证”，不能把示例或推断列为已复现问题。

## 仓库目录

```text
ui-review-skill/
├── README.md
├── LICENSE
├── docs/validation.md              # 已执行检查与验证边界
├── .codex/agents/                  # 三个 Codex 原生 TOML 角色
├── ui-review/
│   ├── SKILL.md                    # 主审查流程与边界
│   └── references/                 # 三种角色提示词与报告模板
└── scripts/
    ├── install.sh                 # 不覆盖已有文件的项目级安装
    └── validate.py                # 静态检查与临时目录安装冒烟检查
```

## 开发与验证

在本仓库根目录执行：

```bash
bash -n scripts/install.sh
python3 scripts/validate.py
git diff --check
```

校验脚本检查 Skill 元数据、引用链接、角色字段与名称、安装后的文件完整性、重复安装拒绝及无效目标路径。不需要模型访问，也不会运行三个审查 Agent。

配置验证与模型运行是两回事：角色能被解析或出现在会话提示词中，不证明真实 UI 审查质量、浏览器可用性或多 Agent 完整执行。首次接入你的客户端时，应使用无敏感数据的测试页面人工检查 Skill 可见性、角色加载、只读权限和报告质量。

本次发布准备的检查范围与结果见 [验证记录](docs/validation.md)。

欢迎通过 Issue 提供脱敏后的输入、Codex 版本、期望结果与实际结果；提交 PR 时请运行上述检查，保持只读边界，不把真实凭据、用户数据或截图中的敏感信息纳入仓库。

## 许可证

本项目采用 [MIT License](LICENSE)，允许使用、修改和分发，需保留版权及许可声明。审查建议按现状提供，不构成完整的无障碍认证或合规保证。

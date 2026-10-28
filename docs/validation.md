# 验证记录

验证日期：2026-10-28。环境：Linux，Codex CLI 0.163.0、Python 3.12.14、Git 2.52.0。

## 已完成

| 检查 | 结果与范围 |
| --- | --- |
| 仓库基线 | 远端默认分支为 `main`，初始提交 `b58e8e54c3359e29649ad391f01caee5a94ee3ba` 仅含 README；在独立功能分支工作 |
| Bash 语法 | `bash -n scripts/install.sh` 通过 |
| 静态与安装契约 | `python3 scripts/validate.py` 通过；检查 Skill 元数据、本地链接、三个角色名称与引用、安装完整性及拒绝覆盖行为 |
| 特殊路径 | 在含空格与 `&` 的临时目标目录完成安装；保留既有业务文件和 `.codex/config.toml` |
| 安装失败边界 | 不存在的目标、重复安装、已有同名角色均被拒绝；角色冲突时没有留下部分 Skill 安装 |
| 官方 schema | 用 `rust-v0.163.0` 的官方配置 schema 校验三个角色的配置部分；`name`、`description` 按该版本的独立角色文件解析规则核对 |
| 原生 Skill 发现 | 本机 app-server 的 `skills/list` 在安装后的临时项目中识别 `ui-review`，返回正确的 `.agents/skills/ui-review/SKILL.md` 路径，发现错误数为 0 |
| 原生角色解析 | 信任临时测试项目后初始化会话，无角色格式告警；加入一个缺少 `developer_instructions` 的无效角色作为对照，Codex 确实发出该文件的解析告警。测试后移除对照文件并恢复原有用户配置 |
| 只读会话配置 | app-server 的 `config/read` 返回 `sandbox_mode = read-only`、`approval_policy = never`；`thread/start` 返回 `readOnly`、网络访问关闭。没有启动模型回合 |
| diff 格式 | `git diff --check` 通过 |

原生发现验证使用本机 app-server 的初始化、配置读取、Skill 列表和会话初始化接口，没有调用 `turn/start`。项目未受信任时实际观察到角色配置被禁用、但 Skill 仍可被发现；因此 README 保留了项目信任与重启会话的说明。

原生角色解析验证不等于三个子 Agent 执行成功，也不等于角色沙箱覆盖生效。0.163.0 的角色覆盖实现不应用角色文件的 `sandbox_mode`；本项目依赖父会话只读启动参数和角色行为约束。

## 未执行与仍需人工确认

- 未调用模型进行真实 UI 审查，未创建三个审查子 Agent，也未记录虚构的 Agent 执行结果。
- 未进行浏览器、真实设备、键盘或屏幕阅读器测试；报告示例是明确标注的虚构格式示例。
- 未验证其他 Codex 版本、IDE 扩展或托管客户端的自定义角色支持情况。
- 使用者首次接入时应确认目标客户端显示 Skill、角色可用且只读策略生效，再用无敏感数据的测试页面检查输出质量。

## 复查入口

在仓库根目录运行 README 中的静态与安装检查，再安装到独立测试项目。使用 README 的只读启动命令，在支持的客户端中检查 Skill 与角色。检查真实行为需要可用模型与浏览器，不能用静态检查替代。

官方规则以固定版本源码为依据：

- [角色文件字段与解析](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/agent-roles/src/agent_role_config.rs)
- [原生角色发现与格式告警](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/agent-roles/src/loader.rs)
- [角色覆盖实际应用字段](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core/src/agent/role.rs)
- [配置 schema](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core/config.schema.json)

# 已确定的项目约定

## 构建与目录

- 文档类为 `ctexbook`，统一使用 XeLaTeX；入口是 `main.tex`。
- 全局宏包、命令和环境分别维护在 `config/packages.tex`、`config/commands.tex` 和 `config/environments.tex`。
- 正文章节放在 `chapters/`，章后例题放在 `examples/`，两者在 `main.tex` 中按阅读顺序装配。
- 原始 PDF、手稿和草稿放在本地 `material/` 或 `materials/`，由 `.gitignore` 排除。

## 环境与编号

- `definition`、`theorem`、`example`、`workedexample` 各自按章独立计数。
- `example` 用于正文短示例，显示为“示例”；`workedexample` 用于章后题集，显示为“例题”。
- `intuition`、`remark`、`pitfall`、`solution`、`technique` 不计数。
- 所有环境标题末尾不加句号。
- 正文示例标签使用 `eg:`，章后例题使用 `ex:`；其他标签前缀见 `docs/style-guide.md`。

## 图像

- 课程图像应尽量由代码复现。绘图脚本放在 `scripts/figures/`，输出放在 `figures/` 的对应章节目录。
- 优先生成矢量 PDF；正文引用的脚本和最终图片都应提交。
- 题图与答案图分开，避免题面提前泄露答案。

## 写作与资料整理

- 正文按“定义—直觉—推导/定理—示例—误区—关联”组织，详细规则见 `docs/style-guide.md`。
- 手写稿先按页面渲染后人工核对；能合理推断但不能确认的细节应明确记录，不把推断冒充原文。
- 每道章后例题必须包含题面、必要的已知图、完整解答、答案图和可迁移的解题技巧。
- 系统的输入输出关系沿用笔记与教材的箭头流程图，即“输入 $\longrightarrow$ 系统 $\longrightarrow$ 输出”；正文不另行引入抽象算子 $\mathcal{T}$，逆系统用前后串联的箭头关系表示。
- “几乎处处相等”、零测集与广义函数判等作为第一章数学预备知识；第四章只引用这些结论解释单位冲激，不展开完整的勒贝格积分或测度论。
- Git 提交与推送必须等待用户明确指令。

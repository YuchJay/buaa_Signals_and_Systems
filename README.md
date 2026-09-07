# 信号与系统：二次学习笔记

这是一个面向长期维护的《信号与系统》个人知识库。目标是在二次学习中重组知识、记录理解与误区，并逐步形成可阅读、可复习的小型教材，而不是复刻课程讲义。

## 目录结构

```text
buaa_Signals_and_Systems/
├── main.tex                    # 文档入口与章节装配顺序
├── .latexmkrc                  # latexmk 默认使用 XeLaTeX
├── .gitignore                  # 忽略构建产物和本地文件
├── README.md                   # 项目说明、构建与协作约定
├── SS.md                       # 本次初始化需求原文
├── config/
│   ├── packages.tex            # 稳定、通用宏包与全局排版配置
│   ├── commands.tex            # 数学符号和变换记号的唯一来源
│   └── environments.tex        # 定义、定理、例题与提示类环境
├── chapters/
│   ├── 00-preface.tex          # 前言与项目范围
│   ├── 01-math-foundations.tex # 数学预备知识
│   ├── 02-signals.tex          # 信号概念、分类与运算（编译示例）
│   ├── 03-systems-and-lti.tex  # 系统性质与 LTI 结构
│   ├── 04-convolution.tex       # 连续/离散卷积与时域系统分析
│   ├── 05-fourier-series.tex   # 周期信号及傅里叶级数
│   ├── 06-ctft.tex             # 连续时间傅里叶变换
│   ├── 07-dtft.tex             # 离散时间傅里叶变换
│   ├── 08-sampling.tex         # 采样、混叠与重建
│   ├── 09-laplace-transform.tex# 拉普拉斯变换与连续时间系统
│   ├── 10-z-transform.tex      # Z 变换与离散时间系统
│   ├── 11-system-analysis.tex  # 系统函数、频率响应与极零分析
│   └── 12-connections-and-review.tex # 跨域联系与综合复习
├── figures/                    # 图片及可复现绘图源文件
├── bibliography/
│   └── references.bib          # 经实际阅读和引用的文献条目
└── docs/
    └── style-guide.md          # 知识库写作与引用规范
```

## 章节设计思路

课程主线按知识依赖展开：先建立信号和系统语言，再用冲激响应引出卷积；随后从周期信号的正交展开进入傅里叶级数，并自然推广到 CTFT 与 DTFT。采样放在两类傅里叶变换之后，便于同时解释频谱复制、混叠和重建。拉普拉斯变换与 Z 变换分别扩展连续、离散傅里叶分析，并把收敛域、系统函数与极零结构连起来。最后单设系统分析和综合复习两章，用于统一因果性、稳定性、频率响应及各表示之间的选择关系。

“系统性质”和“LTI 系统”放在同一章，因为是否线性、时不变直接决定冲激响应表示是否成立；“卷积”单独成章，因为它既是计算工具，也是时域与频域性质之间的桥梁。CTFT 与 DTFT 分章以突出频域周期性和变量结构的差异，但在末节显式对照，避免割裂学习。

## 编译

推荐使用 **XeLaTeX**：它对中文字体和 Unicode 支持成熟，配合 `ctexbook` 配置少，适合在常见 TeX Live 环境中长期维护。

安装 TeX Live（含 `latexmk`）后，在项目根目录运行：

```bash
latexmk main.tex
```

清理中间文件：

```bash
latexmk -c
```

也可直接连续运行两次 `xelatex main.tex`，以生成正确的目录和交叉引用。

## 写作约定

完整规则见 [`docs/style-guide.md`](docs/style-guide.md)。新增章节应保持“问题—定义—直觉—推导—例子—误区—关联”的学习主线。全局符号只在 `config/commands.tex` 中维护；图片按章节建立子目录。

## Git 约定

建议初始化后首次提交为：

```text
chore: initialize LaTeX knowledge base structure
```

后续使用简洁的 Conventional Commits 子集：

- `feat:` 新增章节、知识模块或可复用功能
- `fix:` 修正公式、论证、排版或构建错误
- `docs:` 调整 README、写作规范或非正文说明
- `refactor:` 重组结构或符号而不改变知识结论
- `chore:` 更新依赖、忽略规则等维护工作

应提交 `.tex`、`.bib`、写作规范、绘图源文件以及正文实际使用的最终图片。不要提交 `.aux`、`.log`、`.toc`、`.synctex.gz`、构建缓存和编辑器配置；默认也不提交 `main.pdf`，发布阶段可通过 GitHub Release 单独提供。

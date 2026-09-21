# 项目接手说明

开始修改本项目之前，依次阅读：

1. `docs/project-status/CURRENT.md`：当前进度、未提交改动和下一步；
2. `docs/project-status/DECISIONS.md`：已经确定的结构与技术选择；
3. `docs/style-guide.md`：正文和章后例题的写作规范。

撰写或修改正文、例题及说明文字时，必须按 `humanizer-zh` 技能做一次去 AI 化审校。重点清理模板化开场、机械总结、过多连接词、三段式排比，以及反复出现的“不是……而是……”“不仅……而且……”句式；数学上确有必要的否定和对照可以保留。不得为追求口语化而改动定义、公式、判据或适用条件。

完成一次正文、结构或构建配置修改后，同步更新 `docs/project-status/CURRENT.md`。只有长期有效的决定才写入 `DECISIONS.md`。

不要擅自提交或推送。用户明确要求后再执行 Git commit/push。修改前先检查 `git status`，保留与当前任务无关的用户改动。

完整验证命令为：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
git diff --check
```

正文改动还应检查常见 AI 句式：

```bash
rg -n "不是.*而是|并非.*而是|不仅.*而且|换句话说|这正是|核心问题" chapters examples
```

参考资料目录 `materials/` 只供本地辨读，不纳入 Git。正文引用的绘图脚本和最终图片需要纳入版本控制。

`materials/Alan-V.-Oppenheim-Alan-S.-Willsky-with-S.-Hamid-Signals-and-Systems-Prentice-Hall-1996.pdf` 是本项目后续撰写的教材参考。施工时以 `chapter*.pdf` 课堂笔记确定范围、顺序和需要保留的判据，再用奥本海姆教材核对定义、术语、公式条件、推导和例题选择。两者有实质差异时不得静默改写：正文优先贴合课程笔记，并把差异记入 `docs/source-questions.md` 或向用户确认。教材内容须消化后重述，不作长段照抄。

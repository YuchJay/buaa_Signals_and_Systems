# 项目接手说明

开始修改本项目之前，依次阅读：

1. `docs/project-status/CURRENT.md`：当前进度、未提交改动和下一步；
2. `docs/project-status/DECISIONS.md`：已经确定的结构与技术选择；
3. `docs/style-guide.md`：正文和章后例题的写作规范。

完成一次正文、结构或构建配置修改后，同步更新 `docs/project-status/CURRENT.md`。只有长期有效的决定才写入 `DECISIONS.md`。

不要擅自提交或推送。用户明确要求后再执行 Git commit/push。修改前先检查 `git status`，保留与当前任务无关的用户改动。

完整验证命令为：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
git diff --check
```

参考资料目录 `material/`、`materials/` 只供本地辨读，不纳入 Git。正文引用的绘图脚本和最终图片需要纳入版本控制。

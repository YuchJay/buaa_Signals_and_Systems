# 绘图代码

本目录保存可复现的课程插图代码。脚本按章节分目录，生成文件写入项目根目录下对应的 `figures/<chapter>/`。

第二章插图：

```bash
uv run --with numpy --with matplotlib scripts/figures/ch02_signals/generate.py
```

图像优先输出为矢量 PDF。正文只引用生成结果，不手工修改 PDF；需要调整样式或数据时修改脚本并重新运行。

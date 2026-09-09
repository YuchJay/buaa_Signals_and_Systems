# 第三章插图

`examples/` 中的矢量 PDF 均由
[`scripts/figures/ch03_examples/generate.py`](../../scripts/figures/ch03_examples/generate.py)
生成，用于章后例题的判别过程可视化：

- `linearity-product-integral-answer.pdf`：输入缩放在乘积系统中产生平方缩放；
- `time-invariance-reversal-answer.pdf`：反转系统的两条时移检验路径；
- `causality-variable-limit-answer.pdf`：变上限累加越过当前时刻的依赖区间；
- `memoryless-time-scaling-answer.pdf`：时间缩放系统的输出时刻与输入读取位置；
- `invertibility-calculus-answer.pdf`：积分器与微分器的恢复关系及常数信息损失；
- `stability-sum-difference-answer.pdf`：累加器与差分器对单位阶跃的响应。

不要直接编辑生成的 PDF；需要修改标注、配色或布局时，请修改绘图脚本后重新运行。

"""Draw continuous-time integrator diagrams with XeLaTeX/TikZ.

Run with Python 3 and TeX Live. All PDF figures are generated from this file;
intermediate TeX files are kept in temporary directories.
"""

from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "09-laplace-transform"
PREAMBLE = r"""
\documentclass[tikz,border=6pt]{standalone}
\usepackage[fontset=mac]{ctex}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta}
\definecolor{signalblue}{RGB}{37,102,155}
\definecolor{feedbackred}{RGB}{178,58,42}
\tikzset{
  every node/.style={font=\small},
  flow/.style={signalblue,thick,-{Stealth[length=1.8mm]}},
  feedback/.style={feedbackred,thick,-{Stealth[length=1.8mm]}},
  block/.style={draw,minimum width=10mm,minimum height=8mm},
  sum/.style={circle,draw,minimum size=5.5mm,inner sep=0pt},
}
\begin{document}
\begin{tikzpicture}
"""


def chain(feedback, output, gain=None, order=2, yname="y(t)"):
    """Vertical shared integrator chain; signed gains feed '+' adders."""
    parts = [
        r"\node[left] at (-1,0) {$x(t)$};",
        r"\node[sum] (in) at (0,0) {$+$};",
        r"\draw[flow] (-1,0)--(in);",
        r"\node[sum] (out) at (7.7,0) {$+$};",
        rf"\draw[flow] (out)--(8.4,0) node[right] {{$ {yname} $}};",
    ]
    if gain:
        parts += [
            rf"\node[block] (gain) at (1.4,0) {{$ {gain} $}};",
            r"\draw[flow] (in)--(gain);",
            r"\draw[flow] (gain)--(3.5,0);",
        ]
    else:
        parts.append(r"\draw[flow] (in)--(3.5,0);")
    for k in range(order + 1):
        level = -1.8 * k
        state = (r"w''(t)", r"w'(t)", r"w(t)")[k] if order == 2 else (
            r"w'(t)", r"w(t)"
        )[k]
        parts += [
            rf"\fill[signalblue] (3.5,{level}) circle (1.5pt);",
            rf"\node[above right] at (3.5,{level}) {{$ {state} $}};",
        ]
        if k < order:
            parts += [
                rf"\node[block] (int{k}) at (3.5,{level-.9}) {{$1/s$}};",
                rf"\draw[flow] (3.5,{level})--(int{k});",
                rf"\draw[flow] (int{k})--(3.5,{level-1.8});",
            ]
    # Feedback taps are added before the leading 1/a_2 block.
    if order == 2:
        parts += [
            r"\node[sum] (fb) at (0,-1.8) {$+$};",
            rf"\node[block] (f1) at (1.65,-1.8) {{$ {feedback[0]} $}};",
            r"\draw[feedback] (3.5,-1.8)--(f1);",
            r"\draw[feedback] (f1)--(fb);",
            rf"\node[block] (f0) at (1.65,-3.6) {{$ {feedback[1]} $}};",
            r"\draw[feedback] (3.5,-3.6)--(f0);",
            r"\draw[feedback] (f0)--(0,-3.6)--(fb);",
            r"\draw[feedback] (fb)--(in);",
        ]
    else:
        parts += [
            rf"\node[block] (f0) at (1.65,-1.8) {{$ {feedback[0]} $}};",
            r"\draw[feedback] (3.5,-1.8)--(f0);",
            r"\draw[feedback] (f0)--(0,-1.8)--(in);",
        ]
    present = [k for k, coefficient in enumerate(output) if coefficient is not None]
    if present == [order]:
        # With y=w the output is a wire, rather than an unnecessary output adder.
        parts = [p for p in parts if "(out)" not in p]
        parts.append(
            rf"\draw[flow] (3.5,{-1.8*order})--(8.4,{-1.8*order})"
            rf" node[right] {{$ {yname}=w(t) $}};"
        )
    else:
        if order == 2 and 1 in present and 2 in present:
            parts += [
                r"\node[sum] (lower) at (7.7,-1.8) {$+$};",
                r"\draw[flow] (lower)--(out);",
            ]
        for k in present:
            level = -1.8 * k
            parts.append(
                rf"\node[block] (b{k}) at (5.5,{level}) {{$ {output[k]} $}};"
            )
            parts.append(rf"\draw[flow] (3.5,{level})--(b{k});")
            if order == 2 and 1 in present and 2 in present and k:
                tail = "(lower)" if k == 1 else "(7.7,-3.6)--(lower)"
            else:
                tail = "(out)" if k == 0 else f"(7.7,{level})--(out)"
            parts.append(rf"\draw[flow] (b{k})--{tail};")
    return "\n".join(parts)


def first_order():
    return r"""
\node[left] at (-.9,0) {$x(t)$};
\node[block] (b) at (.3,0) {$b$};
\node[sum] (s) at (2,0) {$+$};
\node[block] (i) at (4.4,0) {$1/s$};
\draw[flow] (-.9,0)--(b);
\draw[flow] (b)--(s);
\draw[flow] (s)--(i) node[midway,above] {$y'(t)$};
\draw[flow] (i)--(7,0) node[right] {$y(t)$};
\fill[signalblue] (6,0) circle (1.5pt);
\node[block] (a) at (4.4,-1.4) {$-a$};
\draw[feedback] (6,0)--(6,-1.4)--(a);
\draw[feedback] (a)--(2,-1.4)--(s);
\node[below] at (4.1,-2) {$y'(t)=bx(t)-ay(t)$};
"""


def primitives():
    return r"""
\node[sum] (s) at (0,0) {$+$};
\draw[flow] (-1.5,0)--(s) node[pos=0,above] {$v_1(t)$};
\draw[flow] (0,1)--(s) node[pos=0,above] {$v_2(t)$};
\draw[flow] (s)--(2.5,0) node[right] {$v_1(t)+v_2(t)$};
\node[anchor=west] at (-1.5,-.8) {(a) 加法器};
\node[block] (g) at (0,-2.1) {$k$};
\draw[flow] (-1.5,-2.1)--(g) node[pos=0,above] {$v(t)$};
\draw[flow] (g)--(2.5,-2.1) node[right] {$kv(t)$};
\node[anchor=west] at (-1.5,-2.9) {(b) 数乘器};
\node[block] (i) at (0,-4.2) {$1/s$};
\draw[flow] (-1.5,-4.2)--(i) node[pos=0,above] {$v(t)$};
\draw[flow] (i)--(2.5,-4.2) node[right] {$q(t)$};
\node[anchor=west] at (-1.5,-5) {(c) 积分器：$q'(t)=v(t)$};
\node[anchor=west] at (-1.5,-5.7) {零初值时 $Q(s)=V(s)/s$};
"""


def cancellation():
    return (
        r"\node[anchor=west] at (-1.1,1) {(a) 二阶结构：$H(s)=(s^2+3s+2)/(s^2+7s+6)$};"
        + chain(("-7", "-6"), ("1", "3", "2"))
        + r"\begin{scope}[shift={(0,-5.4)}]"
        + r"\node[anchor=west] at (-1.1,1) {(b) 约分后：$H(s)=(s+2)/(s+6)$};"
        + chain(("-6",), ("1", "2"), order=1)
        + r"\end{scope}"
    )


def initial_conditions():
    parts = [
        r"\draw[flow] (0,0)--(7,0) node[right] {$t$};",
        r"\draw[flow] (0,-.15)--(0,3.5) node[above] {$y(t)$};",
        r"\draw[gray,dashed] (0,1.5)--(6.5,1.5);",
        r"\node[left] at (0,1.5) {$1$};",
        r"\node[left] at (0,3) {$2$};",
        r"\node[below left] at (0,0) {$0$};",
        r"\draw[signalblue,very thick,domain=0:6.5,samples=100] plot (\x,{1.5*(1-exp(-\x))});",
        r"\draw[gray,very thick] (0,1.5)--(6.5,1.5);",
        r"\draw[feedbackred,very thick,domain=0:6.5,samples=100] plot (\x,{1.5*(1+exp(-\x))});",
        r"\node[signalblue,anchor=west] at (1.7,.4) {$y(0)=0:\quad 1-\mathrm e^{-t}$};",
        r"\node[gray,anchor=west] at (3.7,1.3) {$y(0)=1:\quad 1$};",
        r"\node[feedbackred,anchor=west] at (1.7,2.5) {$y(0)=2:\quad 1+\mathrm e^{-t}$};",
        r"\node at (3.2,4.1) {$y'(t)+y(t)=1,\quad t>0$};",
    ]
    return "\n".join(parts)


def build(name, body):
    with tempfile.TemporaryDirectory(prefix="ch09-blocks-") as directory:
        work = Path(directory)
        source = work / f"{name}.tex"
        source.write_text(
            PREAMBLE + body + "\n\\end{tikzpicture}\n\\end{document}\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", source.name],
            cwd=work, capture_output=True, text=True,
        )
        if result.returncode:
            raise RuntimeError(result.stdout[-4000:])
        shutil.copyfile(work / f"{name}.pdf", OUT / f"{name}.pdf")
    print(f"Generated {OUT / (name + '.pdf')}")


def main():
    figures = {
        "block-elements": primitives(),
        "block-first-order": first_order(),
        "block-second-order": chain(("-a_1", "-a_0"), ("b_2", "b_1", "b_0"), "1/a_2"),
        "block-from-equation": chain(("-4", "-3"), (None, "1", "2")),
        "block-from-system-function": chain(("-5", "-6"), (None, "1", "3")),
        "block-cancellation": cancellation(),
        "block-readback-weighted": chain(("-3", "-2"), (None, "2", "1")),
        "block-readback-lowpass": chain(("-3", "-2"), (None, None, "1")),
        "initial-condition-responses": initial_conditions(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, body in figures.items():
        build(name, body)


if __name__ == "__main__":
    main()

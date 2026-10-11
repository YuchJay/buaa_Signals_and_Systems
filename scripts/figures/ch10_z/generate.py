"""Draw the Z-transform definition and ROC figures using XeLaTeX/TikZ.

Run from any directory with Python 3 and a TeX Live installation containing
standalone, TikZ and ctex. The final PDFs are vector graphics. Intermediate
TeX files stay in a temporary directory.
"""

from concurrent.futures import ThreadPoolExecutor
from math import cos, sin, pi
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "10-z-transform"
PREAMBLE = r"""
\documentclass[tikz,border=5pt]{standalone}
\usepackage[fontset=mac]{ctex}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta}
\definecolor{signalblue}{RGB}{37,102,155}
\definecolor{notered}{RGB}{178,58,42}
\definecolor{roclight}{RGB}{218,235,246}
\tikzset{
  axis/.style={-{Stealth[length=1.5mm]},thin},
  boundary/.style={signalblue,dashed,thick},
  stem/.style={signalblue,thick},
  pole/.style={notered,thick},
  every node/.style={font=\small},
}
\begin{document}
\begin{tikzpicture}
"""


def zaxes(limit=2.0):
    return rf"""
\draw[axis] (-{limit},0)--({limit},0)
  node[right] {{$\operatorname{{Re}}\{{z\}}$}};
\draw[axis] (0,-{limit})--(0,{limit})
  node[above] {{$\operatorname{{Im}}\{{z\}}$}};
"""


def pole(x, y=0):
    return rf"""
\draw[pole] ({x - .06:.4f},{y - .06:.4f})--({x + .06:.4f},{y + .06:.4f});
\draw[pole] ({x - .06:.4f},{y + .06:.4f})--({x + .06:.4f},{y - .06:.4f});
"""


def outside(radius, limit=1.7):
    return rf"""
\fill[roclight,even odd rule]
  (-{limit},-{limit}) rectangle ({limit},{limit}) (0,0) circle ({radius});
"""


def annulus(inner, outer):
    return rf"""
\fill[roclight,even odd rule] (0,0) circle ({outer})
  (0,0) circle ({inner});
"""


def polar():
    return r"""
\draw[axis] (-1.9,0)--(2.0,0) node[right] {$\operatorname{Re}\{z\}$};
\draw[axis] (0,-1.65)--(0,1.9) node[above] {$\operatorname{Im}\{z\}$};
\draw[signalblue,dashed] (0,0) circle (1.4);
\draw[stem,-{Stealth[length=1.5mm]}] (0,0)--(40:1.4)
  node[midway,above left] {$r$};
\fill[signalblue] (40:1.4) circle (1.8pt)
  node[above right] {$z=r\mathrm e^{j\omega}$};
\draw[notered,-{Stealth[length=1.5mm]}] (.48,0) arc (0:40:.48)
  node[midway,right] {$\omega$};
\draw[signalblue,-{Stealth[length=1.5mm]}] (105:1.4) arc (105:150:1.4);
\node at (0,-2.0) {固定 $r$，沿圆周逆时针绕行};
"""


def exponential_pair():
    parts = []
    for row, left in enumerate((False, True)):
        baseline = -4.0 * row
        title = (
            r"$-a^n u[-n-1]$（左边）" if left
            else r"$a^n u[n]$（右边）"
        )
        parts.append(rf"\begin{{scope}}[shift={{(0,{baseline})}}]")
        parts.append(r"\draw[axis] (0,0)--(7,0) node[right] {$n$};")
        parts.append(r"\draw[axis] (2,-1.95)--(2,1.7) node[above] {$x[n]$};")
        parts.append(rf"\node at (3.5,2.15) {{{title}}};")
        for n in range(-3, 6):
            x = 2 + .72 * n
            if not (0 <= x <= 6.4):
                continue
            if left:
                value = -(0.9 ** n) if n < 0 else 0
            else:
                value = 0.9 ** n if n >= 0 else 0
            if value:
                parts.append(
                    rf"\draw[stem] ({x:.3f},0)--({x:.3f},{value:.3f});"
                    rf"\fill[signalblue] ({x:.3f},{value:.3f}) circle (1.5pt);"
                )
            else:
                parts.append(
                    rf"\draw[signalblue,fill=white] ({x:.3f},0) circle (1.5pt);"
                )
            parts.append(rf"\node[below,font=\scriptsize] at ({x:.3f},0) {{$ {n} $}};")
            if left and n == -1:
                parts.append(
                    rf"\node[below,font=\scriptsize] at ({x:.3f},{value - .08:.3f})"
                    rf"{{$-a^{{{n}}}$}};"
                )
            elif not left and 0 <= n <= 3:
                label = "1" if n == 0 else ("a" if n == 1 else rf"a^{n}")
                parts.append(
                    rf"\node[above,font=\scriptsize] at ({x:.3f},{value:.3f})"
                    rf"{{$ {label} $}};"
                )
        parts.append(r"\end{scope}")
        parts.append(rf"\begin{{scope}}[shift={{(10.4,{baseline})}}]")
        parts.append(
            r"\fill[roclight] (0,0) circle (.9);"
            if left else outside(.9, 1.55)
        )
        parts.append(zaxes(1.7))
        parts.append(r"\draw[boundary] (0,0) circle (.9);")
        parts.append(pole(.9))
        parts.append(r"\node[below right] at (.9,0) {$a$};")
        parts.append(
            rf"\node[anchor=south] at (-1.45,1.82) {{$|z|{'<' if left else '>'}|a|$}};"
        )
        parts.append(r"\end{scope}")
    return "\n".join(parts)


def two_annuli():
    parts = [
        r"\begin{scope}",
        annulus(.42, 1.68),
        zaxes(1.95),
        r"\draw[boundary] (0,0) circle (.42);",
        r"\draw[boundary] (0,0) circle (1.68);",
        pole(.42),
        pole(1.68),
        r"\node[below] at (.42,-.12) {$b$};",
        r"\node[below] at (1.68,-.12) {$b^{-1}$};",
        r"\node at (0,2.6) {$0<b<1$：$b<|z|<b^{-1}$};",
        r"\node at (0,-2.35) {双边指数的两个 ROC 相交};",
        r"\end{scope}",
        r"\begin{scope}[shift={(6.6,0)}]",
        annulus(1, 1.5),
        zaxes(1.95),
        r"\draw[boundary] (0,0) circle (1);",
        r"\draw[boundary] (0,0) circle (1.5);",
        pole(1),
        pole(1.5),
        r"\draw[signalblue,fill=white] (0,0) circle (2pt);",
        r"\node[below] at (1,-.12) {$\frac13$};",
        r"\node[below] at (1.5,-.12) {$\frac12$};",
        r"\node at (0,2.6) {$\frac13<|z|<\frac12$};",
        r"\node at (0,-2.35) {混合序列：原点为零点，叉号为极点};",
        r"\end{scope}",
    ]
    return "\n".join(parts)


def trig_sequence(sine=False):
    parts = [
        r"\draw[axis] (-.4,0)--(8.4,0) node[right] {$n$};",
        r"\draw[axis] (0,-1.55)--(0,1.55) node[above] {$x[n]$};",
        r"\node[below left] at (0,0) {$0$};",
        r"\node[left] at (0,1) {$1$};",
        r"\node[left] at (0,-1) {$-1$};",
    ]
    for n in range(13):
        x = n * .6
        value = sin(n * pi / 3) if sine else cos(n * pi / 3)
        if abs(value) < 1e-8:
            value = 0
        parts.append(
            rf"\draw[stem] ({x:.3f},0)--({x:.3f},{value:.3f});"
            rf"\fill[signalblue] ({x:.3f},{value:.3f}) circle (1.5pt);"
        )
        if n and n % 3 == 0:
            parts.append(rf"\node[below,font=\scriptsize] at ({x},0) {{$ {n} $}};")
    parts += [
        rf"\node at (4,2) {{$ {'sin' if sine else 'cos'}(\omega_0n)u[n]"
        r"\quad(\omega_0=\pi/3)$};",
        r"\begin{scope}[shift={(11.2,0)}]",
        outside(1, 1.45),
        zaxes(1.55),
        r"\draw[boundary] (0,0) circle (1);",
        pole(.5, sin(pi / 3)),
        pole(.5, -sin(pi / 3)),
        r"\node[above right,font=\scriptsize] at (.5,.866) {$\mathrm e^{j\omega_0}$};",
        r"\node[below right,font=\scriptsize] at (.5,-.866) {$\mathrm e^{-j\omega_0}$};",
        r"\node[anchor=south] at (-1.45,1.72) {$|z|>1$};",
        r"\end{scope}",
    ]
    if not sine:
        parts[18:18] = [
            r"\node[below] at (-.28,-1.55) {$n<0$ 时为零};"
        ]
    return "\n".join(parts)


def folding():
    return r"""
\fill[roclight] (-.65,-1.7) rectangle (.65,1.7);
\draw[signalblue,dashed] (-.65,-1.7)--(-.65,1.7);
\draw[signalblue,dashed] (.65,-1.7)--(.65,1.7);
\draw[axis] (-1.85,0)--(1.85,0) node[right] {$\sigma$};
\draw[notered,-{Stealth[length=1.5mm]},thick] (0,-1.9)--(0,1.9)
  node[above] {$j\omega$};
\node at (0,2.7) {拉氏变换复频域};
\node at (0,-2.25) {带状区域};
\draw[notered,-{Stealth[length=2mm]},thick] (2.5,.1)--(4.5,.1);
\draw[notered,-{Stealth[length=2mm]},thick]
  (3.25,1.45) arc (-70:125:.55);
\node[notered] at (3.5,-.6) {卷曲、闭合};
\begin{scope}[shift={(7.1,0)}]
  \fill[roclight,even odd rule] (0,0) circle (1.65) (0,0) circle (.6);
  \draw[axis] (-1.95,0)--(1.95,0) node[right] {$\operatorname{Re}\{z\}$};
  \draw[axis] (0,-1.95)--(0,1.95) node[above] {$\operatorname{Im}\{z\}$};
  \draw[signalblue,dashed] (0,0) circle (.6);
  \draw[signalblue,dashed] (0,0) circle (1.65);
  \draw[notered,thick] (0,0) circle (1);
  \draw[notered,-{Stealth[length=1.5mm]},thick] (25:1) arc (25:70:1);
  \node[notered,below right] at (1,0) {$1$};
  \node at (0,2.7) {Z 变换复频域};
  \node at (0,-2.25) {环带，红圈为单位圆};
\end{scope}
"""


def three_rocs():
    parts = []
    for k in range(3):
        parts.append(rf"\begin{{scope}}[shift={{({5.7 * k},0)}}]")
        if k == 0:
            parts.append(outside(1.5, 2))
        elif k == 1:
            parts.append(annulus(.375, 1.5))
        else:
            parts.append(r"\fill[roclight] (0,0) circle (.375);")
        parts += [
            zaxes(2.05),
            r"\draw[boundary] (0,0) circle (.375);",
            r"\draw[boundary] (0,0) circle (1.5);",
            pole(.375),
            pole(1.5),
            r"\draw[signalblue,fill=white] (0,0) circle (1.6pt);",
            r"\node[below] at (.375,-.17) {$\frac12$};",
            r"\node[below] at (1.5,-.17) {$2$};",
        ]
        parts.append(
            rf"\node at (0,2.65) {{{['$|z|>2$', r'$\frac12<|z|<2$', r'$|z|<\frac12$'][k]}}};"
        )
        parts.append(
            rf"\node at (0,-2.45) {{{['两项右边', '第一项右边，第二项左边', '两项左边'][k]}}};"
        )
        parts.append(r"\end{scope}")
    return "\n".join(parts)


def build_one(item):
    name, drawing = item
    xelatex = shutil.which("xelatex")
    if not xelatex:
        raise RuntimeError("XeLaTeX is required to generate these figures.")
    with tempfile.TemporaryDirectory(prefix=f"ch10-z-{name}-") as scratch:
        source = Path(scratch) / f"{name}.tex"
        source.write_text(PREAMBLE + drawing + "\n\\end{tikzpicture}\n\\end{document}\n")
        result = subprocess.run(
            [xelatex, "-interaction=nonstopmode", "-halt-on-error", source.name],
            cwd=scratch, capture_output=True, text=True,
        )
        if result.returncode:
            raise RuntimeError(f"{name} failed:\n{result.stdout[-4000:]}")
        shutil.copy2(source.with_suffix(".pdf"), OUT / f"{name}.pdf")
    return name


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "polar-contour": polar(),
        "exponential-rocs": exponential_pair(),
        "two-sided-rocs": two_annuli(),
        "cosine-roc": trig_sequence(),
        "sine-roc": trig_sequence(sine=True),
        "laplace-z-folding": folding(),
        "inverse-three-rocs": three_rocs(),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(build_one, figures.items()):
            print(f"Generated {OUT / (name + '.pdf')}")


if __name__ == "__main__":
    main()

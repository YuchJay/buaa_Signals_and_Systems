"""Reproduce delay-chain diagrams and two-sided input sketches."""

from concurrent.futures import ThreadPoolExecutor
from generate import OUT, build_one


def chain(feedback, output, gain="1", xlabel="x[n]", ylabel="y[n]"):
    lines = [
        r"\tikzset{flow/.style={signalblue,thick,-{Stealth[length=1.6mm]}},"
        r"sum/.style={circle,draw,minimum size=5mm,inner sep=0pt},"
        r"delay/.style={draw,minimum width=9mm,minimum height=7mm}}",
        rf"\node at (-.8,0) {{$ {xlabel} $}};",
        r"\node[sum] (s) at (.6,0) {$+$};",
        r"\draw[flow] (-.3,0)--(s);",
        rf"\draw[flow] (s)--(3.5,0) node[midway,above] {{$ {gain} $}};",
        r"\fill[signalblue] (3.5,0) circle (1.5pt);",
        r"\node[above] at (3.5,0) {$w[n]$};",
        r"\node[delay] (d1) at (3.5,-1.1) {$z^{-1}$};",
        r"\node[delay] (d2) at (3.5,-2.5) {$z^{-1}$};",
        r"\draw[flow] (3.5,0)--(d1);",
        r"\draw[flow] (d1)--(3.5,-1.7);",
        r"\fill[signalblue] (3.5,-1.7) circle (1.5pt);",
        r"\draw[flow] (3.5,-1.7)--(d2);",
        r"\draw[flow] (d2)--(3.5,-3.1);",
        r"\fill[signalblue] (3.5,-3.1) circle (1.5pt);",
        r"\node[below] at (3.5,-3.1) {$w[n-2]$};",
        r"\node[right,font=\scriptsize] at (3.55,-1.98) {$w[n-1]$};",
        r"\node[sum] (o) at (7.4,0) {$+$};",
        rf"\draw[flow] (o)--(8.7,0) node[right] {{$ {ylabel} $}};",
    ]
    if feedback[1] is None and output[2] is None:
        lines = [line for line in lines if not any(
            token in line for token in ("(d2)", "(3.5,-3.1)", r"$w[n-2]$")
        )]
    if feedback[1] is not None:
        lines += [
            r"\node[sum] (f) at (.6,-1.7) {$+$};",
            rf"\draw[flow] (3.5,-1.7)--(f) node[midway,above] {{$ {feedback[0]} $}};",
            rf"\draw[flow] (3.5,-3.1)--(.6,-3.1)"
            rf" node[midway,above] {{$ {feedback[1]} $}}--(f);",
            r"\draw[flow] (f)--(s);",
        ]
    else:
        lines.append(
            rf"\draw[flow] (3.5,-1.7)--(.6,-1.7)"
            rf" node[midway,above] {{$ {feedback[0]} $}}--(s);"
        )
    if output[1] is not None and output[2] is not None:
        lines.append(r"\node[sum] (g) at (7.4,-1.7) {$+$};")
        lines += [
            rf"\draw[flow] (3.5,-1.7)--(g) node[midway,above] {{$ {output[1]} $}};",
            rf"\draw[flow] (3.5,-3.1)--(7.4,-3.1)"
            rf" node[midway,above] {{$ {output[2]} $}}--(g);",
            r"\draw[flow] (g)--(o);",
        ]
    for k, value in enumerate(output):
        if value is None:
            continue
        if k and output[1] is not None and output[2] is not None:
            continue
        if k == 0:
            lines.append(
                rf"\draw[flow] (3.5,0)--(o) node[midway,above] {{$ {value} $}};"
            )
        else:
            y = -1.7 if k == 1 else -3.1
            lines.append(
                rf"\draw[flow] (3.5,{y})--(7.4,{y})"
                rf" node[midway,above] {{$ {value} $}}"
                rf"--(o);"
            )
    return "\n".join(lines)


def cascade():
    return (
        r"\begin{scope}[shift={(0,0)}]"
        + chain(("1/2", None), ("1", "-1", None), ylabel="c[n]")
          .replace(r" node[right] {$ c[n] $}", "")
          .replace("$w[", "$w_1[")
        + r"\end{scope}"
        + r"\begin{scope}[shift={(10,0)}]"
        + chain(("-1/4", "1/8"), ("1", "-1/2", None), xlabel="c[n]")
          .replace(r"\node at (-.8,0) {$ c[n] $};", "")
          .replace("$w[", "$w_2[")
        + r"\end{scope}"
        + r"\draw[signalblue,thick] (8.7,0)--(9.7,0) node[midway,above] {$c[n]$};"
    )


def stems(values, title, baseline=0, ymax=3.5):
    tick_y = -.7 if any(v < 0 for _, v in values) else 0
    parts = [rf"\begin{{scope}}[shift={{(0,{baseline})}}]"]
    parts += [
        rf"\node[anchor=west] at (-4.6,{ymax+.5}) {{{title}}};",
        r"\draw[axis] (-4.8,0)--(5,0) node[right] {$n$};",
        rf"\draw[axis] (0,-.7)--(0,{ymax}) ;",
    ]
    for n, v in values:
        x = .8 * n
        if v:
            parts += [
                rf"\draw[stem] ({x},0)--({x},{v});",
                rf"\fill[signalblue] ({x},{v}) circle (1.6pt);",
            ]
        else:
            parts.append(rf"\draw[signalblue,fill=white] ({x},0) circle (1.6pt);")
        parts.append(rf"\node[below,font=\scriptsize] at ({x},{tick_y}) {{$ {n} $}};")
        if n in (-1, 0) and v:
            label = f"{int(v)}" if v in (2, 3) else (r"-4/9" if v < 0 else r"4/9")
            parts.append(rf"\node[above,font=\scriptsize] at ({x},{v}) {{$ {label} $}};")
    parts.append(r"\end{scope}")
    return "\n".join(parts)


def split():
    domain = range(-5, 6)
    return "\n".join([
        stems([(n, 3 if n < 0 else 2) for n in domain],
              r"$x[n]=3u[-n-1]+2u[n]$"),
        stems([(n, 3 if n < 0 else 0) for n in domain],
              r"$x_-[n]=3u[-n-1]$", -5),
        stems([(n, 2 if n >= 0 else 0) for n in domain],
              r"$x_+[n]=2u[n]$", -10),
    ])


def even():
    return (
        stems([(n, 2 if n % 2 == 0 else 0) for n in range(-5, 6)],
              r"$x[n]=1+(-1)^n$", ymax=2.5)
        + stems([(n, 4 / 9 * (-1)**n) for n in range(-5, 6)],
                r"$y[n]=\frac49(-1)^n$", -4.2, ymax=1.1)
    )


def main():
    figures = {
        "delay-chain": chain(("-a_1", "-a_2"), ("b_0", "b_1", "b_2"), "1/a_0"),
        "delay-equation-examples": (
            r"\begin{scope}"
            + chain(("-1", "6"), (None, "1", None))
            + r"\end{scope}\begin{scope}[shift={(0,-5)}]"
            + chain(("5", "-6"), ("1", None, "-3"))
            + r"\end{scope}"
        ),
        "delay-readback": chain(("-5/6", "-1/6"), ("1", "-1/4", None)),
        "delay-cascade": cascade(),
        "stable-input-split": split(),
        "stable-even-input": even(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(build_one, figures.items()):
            print(f"Generated {OUT / (name + '.pdf')}")


if __name__ == "__main__":
    main()

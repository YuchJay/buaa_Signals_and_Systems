"""Draw repeated-pole Z-transform pairs with the shared TikZ figure style."""

from generate import OUT, build_one, outside, pole, zaxes


def repeated_pairs(shifted=False):
    parts = []
    for row, left in enumerate((False, True)):
        parts.append(rf"\begin{{scope}}[shift={{(0,{-3.7 * row})}}]")
        parts += [
            r"\draw[axis] (-.5,0)--(7.3,0) node[right] {$n$};",
            r"\draw[axis] (3.3,-.2)--(3.3,2.1) node[above] {$x[n]$};",
        ]
        for n in range(-5, 6):
            xpos = 3.3 + .6 * n
            if shifted:
                value = -n - 1 if left and n <= -2 else 0
                if not left and n >= 0:
                    value = n + 1
            else:
                value = -n if left and n <= -1 else 0
                if not left and n >= 0:
                    value = n
            ypos = .26 * value
            if value:
                parts.append(
                    rf"\draw[stem] ({xpos:.2f},0)--({xpos:.2f},{ypos:.2f});"
                    rf"\fill[signalblue] ({xpos:.2f},{ypos:.2f}) circle (1.5pt);"
                    rf"\node[above,font=\scriptsize] at ({xpos:.2f},{ypos:.2f})"
                    rf"{{$ {value} $}};"
                )
            else:
                parts.append(
                    rf"\draw[signalblue,fill=white] ({xpos:.2f},0) circle (1.5pt);"
                )
            parts.append(
                rf"\node[below,font=\scriptsize] at ({xpos:.2f},0) {{$ {n} $}};"
            )
        title = (
            r"$-(n+1)u[-n-2]$" if left else r"$(n+1)u[n+1]$"
        ) if shifted else (r"$-nu[-n-1]$" if left else r"$nu[n]$")
        parts.append(rf"\node[anchor=west] at (0,2.5) {{{title}}};")
        parts.append(r"\end{scope}")
        parts.append(rf"\begin{{scope}}[shift={{(10.3,{-3.7 * row})}}]")
        parts.append(
            r"\fill[roclight] (0,0) circle (1);"
            if left else outside(1, 1.35)
        )
        parts += [
            zaxes(1.5),
            r"\draw[boundary] (0,0) circle (1);",
            pole(1),
            r"\node[below right] at (1,0) {$1$};",
            rf"\node[anchor=east] at (-.7,1.85) {{$|z|{'<' if left else '>'}1$}};",
            r"\end{scope}",
        ]
    return "\n".join(parts)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for item in (
        ("weighted-exponentials", repeated_pairs()),
        ("squared-pairs", repeated_pairs(shifted=True)),
    ):
        build_one(item)
        print(f"Generated {OUT / (item[0] + '.pdf')}")

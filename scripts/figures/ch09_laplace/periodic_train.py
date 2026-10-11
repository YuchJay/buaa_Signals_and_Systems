"""Generate the one-sided periodic-signal figure for the Laplace chapter.

The drawing is written as PostScript so regeneration does not depend on a
Python plotting package.
"""

from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "figures" / "09-laplace-transform" / "one-sided-periodic.pdf"
EPS = OUT.with_suffix(".eps")

LEFT, RIGHT, PERIOD = 55, 405, 70
BLUE = (0.145, 0.400, 0.608)
RED = (0.698, 0.227, 0.165)
LIGHT_RED = (0.965, 0.820, 0.800)
GRID = (0.84, 0.84, 0.84)


def rgb(color):
    return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} setrgbcolor"


def escaped(value):
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text(x, y, value, size=9, font="Helvetica"):
    return (
        f"/{font} findfont {size} scalefont setfont "
        f"{x:.1f} {y:.1f} moveto ({escaped(value)}) show"
    )


def centered_text(x, y, value, size=9, font="Helvetica"):
    value = escaped(value)
    return (
        f"/{font} findfont {size} scalefont setfont "
        f"({value}) stringwidth pop 2 div {x:.1f} exch sub "
        f"{y:.1f} moveto ({value}) show"
    )


def line(x1, y1, x2, y2):
    return f"newpath {x1:.1f} {y1:.1f} moveto {x2:.1f} {y2:.1f} lineto stroke"


def draw_panel(commands, baseline, top, title, show_amplitude_ticks=True):
    commands.extend([rgb(GRID), "0.45 setlinewidth"])
    for n in range(5):
        x = LEFT + PERIOD * n
        commands.append(line(x, baseline + 40, x, top))

    commands.extend(
        [
            "0 setgray",
            "0.75 setlinewidth",
            line(LEFT, baseline, RIGHT, baseline),
            line(LEFT, baseline, LEFT, top + 4),
            line(RIGHT, baseline, RIGHT - 5, baseline + 2),
            line(RIGHT, baseline, RIGHT - 5, baseline - 2),
            centered_text((LEFT + RIGHT) / 2, top + 14, title, 10),
        ]
    )
    if show_amplitude_ticks:
        commands.extend(
            [
                text(LEFT - 24, baseline + 36, "1", 8),
                text(LEFT - 17, baseline - 3, "0", 8),
            ]
        )
    for n in range(5):
        x = LEFT + PERIOD * n
        commands.append(line(x, baseline - 3, x, baseline + 3))
        commands.append(centered_text(x, baseline - 16, str(n), 8))
    commands.append(text(RIGHT + 5, baseline - 3, "t/T", 9, "Helvetica-Oblique"))
    commands.append(text(LEFT - 28, baseline + 51, "x(t)", 9, "Helvetica-Oblique"))


def build_eps():
    commands = [
        "%!PS-Adobe-3.0 EPSF-3.0",
        "%%BoundingBox: 0 0 420 300",
        "%%Pages: 1",
        "%%EndComments",
        "1 setlinecap 1 setlinejoin",
    ]
    upper_baseline, upper_top = 204, 254
    lower_baseline, lower_top = 78, 128
    draw_panel(
        commands,
        upper_baseline,
        upper_top,
        "one-sided impulse train",
        show_amplitude_ticks=False,
    )
    draw_panel(commands, lower_baseline, lower_top, "one-sided rectangular pulse train")

    commands.extend([rgb(BLUE), "1.35 setlinewidth"])
    for n in range(5):
        x = LEFT + PERIOD * n
        commands.append(
            f"newpath {x:.1f} {upper_baseline:.1f} moveto "
            f"{x:.1f} {upper_baseline + 35:.1f} lineto stroke"
        )
        commands.append(
            f"newpath {x - 3:.1f} {upper_baseline + 34:.1f} moveto "
            f"{x:.1f} {upper_baseline + 40:.1f} lineto "
            f"{x + 3:.1f} {upper_baseline + 34:.1f} lineto closepath fill"
        )
        commands.append(centered_text(x, upper_baseline + 47, "1", 8))

    commands.append(rgb(LIGHT_RED))
    for n in range(5):
        x = LEFT + PERIOD * n
        commands.append(
            f"newpath {x:.1f} {lower_baseline:.1f} moveto "
            f"{x + 35:.1f} {lower_baseline:.1f} lineto "
            f"{x + 35:.1f} {lower_baseline + 40:.1f} lineto "
            f"{x:.1f} {lower_baseline + 40:.1f} lineto closepath fill"
        )

    commands.extend([rgb(RED), "1.25 setlinewidth"])
    for n in range(5):
        x = LEFT + PERIOD * n
        commands.append(
            f"newpath {x:.1f} {lower_baseline:.1f} moveto "
            f"{x:.1f} {lower_baseline + 40:.1f} lineto "
            f"{x + 35:.1f} {lower_baseline + 40:.1f} lineto "
            f"{x + 35:.1f} {lower_baseline:.1f} lineto stroke"
        )
    commands.extend(["showpage", "%%EOF", ""])
    EPS.parent.mkdir(parents=True, exist_ok=True)
    EPS.write_text("\n".join(commands), encoding="ascii")


def main():
    build_eps()
    gs = shutil.which("gs") or "/opt/homebrew/bin/gs"
    subprocess.run(
        [
            gs,
            "-q",
            "-dBATCH",
            "-dNOPAUSE",
            "-dEPSCrop",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={OUT}",
            str(EPS),
        ],
        check=True,
    )
    EPS.unlink(missing_ok=True)


if __name__ == "__main__":
    main()

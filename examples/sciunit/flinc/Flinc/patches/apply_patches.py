#!/usr/bin/env python3
"""
apply_patches.py <sciunit-checkout-dir>

Applies FLINC's changes to a freshly-cloned sciunit checkout by content
match rather than by exact-context .patch files. This is deliberately more
tolerant than `git apply`: each edit is found by a whitespace/quote-style
-flexible regex, is skipped (not an error) if the target text is already
present -- e.g. because upstream has since merged an equivalent change --
and only fails loudly if neither the "before" nor "after" text can be found
at all, which means upstream changed the surrounding code in a way that
needs a human to look at it.
"""
import re
import sys
from pathlib import Path


def apply_edit(path: Path, description: str, already_applied_re: str,
                find_re: str, build_replacement, flags=0):
    text = path.read_text()

    if re.search(already_applied_re, text, flags):
        print(f"NOTE: {description} already present in {path} -- skipping")
        return

    m = re.search(find_re, text, flags)
    if not m:
        print(f"ERROR: could not find expected code for {description} in {path}", file=sys.stderr)
        print("       Upstream likely changed this file -- update apply_patches.py by hand.", file=sys.stderr)
        sys.exit(1)

    replacement = build_replacement(m)
    new_text = text[:m.start()] + replacement + text[m.end():]
    path.write_text(new_text)
    print(f"OK: applied {description} to {path}")


def main():
    if len(sys.argv) != 2:
        print("usage: apply_patches.py <sciunit-checkout-dir>", file=sys.stderr)
        sys.exit(1)

    root = Path(sys.argv[1])

    # ---- 1. FLINC SIGINT patch -------------------------------------------
    # sciunit2/command/exec_/__init__.py: sciunit exec must ignore SIGINT so
    # FLINC's handler.py can forward it to the traced kernel process instead
    # of it killing the sciunit exec / ptu process outright.
    exec_init = root / "sciunit2" / "command" / "exec_" / "__init__.py"
    apply_edit(
        path=exec_init,
        description="FLINC SIGINT patch",
        already_applied_re=r"signal\.signal\(\s*signal\.SIGINT",
        find_re=r"from importlib\.resources import files\n",
        build_replacement=lambda m: (
            m.group(0)
            + "\n"
            + "# for FLINC, to avoid SIGINT causing KeyboardInterruptException\n"
            + "# and exiting sciunit execution\n"
            + "import signal\n"
            + "signal.signal(signal.SIGINT, lambda *_: None)\n"
        ),
    )

    # ---- 2. cmake in-process invocation ----------------------------------
    # setup.py: fetch cmake via setup_requires (same mechanism that already
    # gets docutils, no root/apt-get needed) and invoke it in-process via
    # sys.executable, rather than as a separate 'cmake' console-script that
    # may not be able to import the cmake package in an isolated build env.
    setup_py = root / "setup.py"

    def build_cmake_call(m):
        indent = m.group("indent")
        return (
            f"{indent}# invoke cmake in-process rather than as a separate 'cmake'\n"
            f"{indent}# console-script: setup_requires guarantees the cmake package is\n"
            f"{indent}# importable on THIS interpreter's sys.path, but a standalone\n"
            f"{indent}# 'cmake' command on PATH may resolve to a script tied to a\n"
            f"{indent}# different (e.g. isolated build) environment that can't import it.\n"
            f"{indent}subprocess.check_call([\n"
            f"{indent}    sys.executable, '-c',\n"
            f"{indent}    'import sys; from cmake import cmake; '\n"
            f"{indent}    'sys.argv = [\"cmake\"] + sys.argv[1:]; cmake()',\n"
            f"{indent}    '-DCMAKE_BUILD_TYPE=Release',\n"
            f"{indent}])"
        )

    apply_edit(
        path=setup_py,
        description="cmake in-process invocation",
        already_applied_re=r"from cmake import cmake",
        find_re=r"(?P<indent>[ \t]*)subprocess\.check_call\(\s*\[\s*['\"]cmake['\"]\s*,\s*['\"]-DCMAKE_BUILD_TYPE=Release['\"]\s*\]\s*\)",
        build_replacement=build_cmake_call,
    )

    apply_edit(
        path=setup_py,
        description="cmake added to setup_requires",
        already_applied_re=r"setup_requires\s*=\s*\[[^\]]*['\"]cmake['\"]",
        find_re=r"setup_requires\s*=\s*\[\s*['\"]docutils['\"]\s*\]",
        build_replacement=lambda m: "setup_requires=['docutils', 'cmake']",
    )

    # ensure `import sys` is present (needed by the cmake in-process call)
    text = setup_py.read_text()
    if not re.search(r"^import sys$", text, re.MULTILINE):
        text = re.sub(r"(^import os$)", r"\1\nimport sys", text, count=1, flags=re.MULTILINE)
        setup_py.write_text(text)
        print(f"OK: added 'import sys' to {setup_py}")
    else:
        print(f"NOTE: 'import sys' already present in {setup_py} -- skipping")


if __name__ == "__main__":
    main()

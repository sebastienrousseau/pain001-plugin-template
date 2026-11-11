# SPDX-License-Identifier: Apache-2.0 OR MIT
#
# Rendered with `make demo` (VHS, https://github.com/charmbracelet/vhs),
# which runs it inside the Poetry environment. Renders the template,
# runs the generated plugin's tests, installs it into a scratch
# directory and asks pain001 to find it. Local only; no network.

Output .github/demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1200
Set Height 720
Set Padding 20
Set Theme "Catppuccin Mocha"
Set TypingSpeed 35ms

Hide
Type "export PS1='$ ' && rm -rf /tmp/pain001-demo && clear"
Enter
Show

Type "cookiecutter . --no-input --output-dir /tmp/pain001-demo"
Enter
Sleep 2s

Type "cd /tmp/pain001-demo/pain001-loader-example && ls"
Enter
Sleep 2s

Type "python -m pytest -p no:cacheprovider --no-header"
Enter
Sleep 5s

Type "pip install -q --no-deps --no-build-isolation --target ../site ."
Enter
Sleep 6s

Type "PYTHONPATH=../site python -m pain001 plugins show example"
Enter
Sleep 5s

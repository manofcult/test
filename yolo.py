"""End-to-end test cases of algorithmic style."""

from __future__ import annotations

import textwrap

from integration_tests import integration_utils


def test_factorial() -> None:
    def fact(n):
        if n == 0:
            return 1
        else:
            return n * fact(n - 1)

    latex = textwrap.dedent(
        r"""
        \begin{algorithmic}
            \Function{fact}{$n$}
                \If{$n = 0$}
                    \State \Return $1$
                \Else
                    \State \Return $n \cdot \mathrm{fact} \mathopen{}\left( n - 1 \mathclose{}\right)$
                \EndIf
            \EndFunction
        \end{algorithmic}
        """  # noqa: E501
    ).strip()
    ipython_latex = (
        r"\begin{array}{l}"
        r" \mathbf{function} \ \mathrm{fact}(n) \\"
        r" \hspace{1em} \mathbf{if} \ n = 0 \\"
        r" \hspace{2em} \mathbf{return} \ 1 \\"
        r" \hspace{1em} \mathbf{else} \\"
        r" \hspace{2em}"
        r" \mathbf{return} \ n \cdot"
        r" \mathrm{fact} \mathopen{}\left( n - 1 \mathclose{}\right) \\"
        r" \hspace{1em} \mathbf{end \ if} \\"
        r" \mathbf{end \ function}"
        r" \end{array}"
    )
    integration_utils.check_algorithm(fact, latex, ipython_latex)

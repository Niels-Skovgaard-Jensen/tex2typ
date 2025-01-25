import re
from dataclasses import dataclass


@dataclass
class SyntaxRule:
    pattern: re.Pattern[str]
    replacement: str
    priority: int = 0


SYNTAX_RULES: list[SyntaxRule] = [
    SyntaxRule(pattern=re.compile(r"\\begin{equation}(.*?)\\end{equation}"), replacement=r"$ \1 $", priority=100),
    SyntaxRule(pattern=re.compile(r"\\frac{(.*?)}{(.*?)}"), replacement=r" frac(\1, \2) ", priority=100),
    SyntaxRule(pattern=re.compile(r"\\boldsymbol{(.*?)}"), replacement=r"bold(\1)", priority=90),
    SyntaxRule(pattern=re.compile(r"\\bar{(.*?)}"), replacement=r"overline(\1)", priority=80),
    SyntaxRule(pattern=re.compile(r"\\sqrt{(.*?)}"), replacement=r"sqrt(\1)", priority=70),
    SyntaxRule(pattern=re.compile(r"_{(.*?)}"), replacement=r"_(\1)", priority=20),
    SyntaxRule(pattern=re.compile(r"\^{(.*?)}"), replacement=r"^(\1)", priority=20),
]

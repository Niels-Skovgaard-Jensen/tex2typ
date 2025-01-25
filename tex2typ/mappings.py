from tex2typ.symbol_map import SYMBOL_MAP
from tex2typ.syntax_rules import SYNTAX_RULES, SyntaxRule


class LatexToTypstConverter:
    def __init__(self) -> None:
        self.symbol_map: dict[str, str] = SYMBOL_MAP
        self.rules: list[SyntaxRule] = SYNTAX_RULES

        # Sort rules by priority
        self.rules.sort(key=lambda x: x.priority, reverse=True)

    def convert(self, latex: str) -> str:
        result = latex

        # Apply symbol mappings
        for latex_sym, typst_sym in self.symbol_map.items():
            result = result.replace(latex_sym, typst_sym)

        # Apply pattern rules in priority order
        for rule in self.rules:
            result = rule.pattern.sub(rule.replacement, result)

        return result.strip()


class TypstToLatexConverter:
    def __init__(self) -> None:
        # TODO Implement reverse mappings here
        raise NotImplementedError

    def convert(self, typst: str) -> str:
        # TODO Implement reverse conversion here
        raise NotImplementedError

import ast
import re
from typing import Any, Generator, Tuple

VERSION_PREFIX = re.compile('/v\d+')

__version__ = "0.1"


class Linter:
    name = 'flask'
    version = __version__

    def __init__(self, tree, filename: str) -> None:
        self.tree = tree

    def run(self) -> Generator[Tuple[int, int, str, type], Any, None]:
        for statement in ast.walk(self.tree):
            if isinstance(statement, ast.FunctionDef):
                yield from self._check_function_def(statement)
            elif isinstance(statement, ast.Call):
                yield from self._check_call(statement)

    def _check_function_def(
            self, function_def: ast.FunctionDef,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        for decorator in function_def.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                route_function = decorator.func.attr == 'route'
                args = decorator.args
                str_arg = isinstance(args[0], ast.Str)
                if route_function and str_arg:
                    missing_trailing_slash = len(args) > 0 and not args[0].s.endswith('/')
                    if missing_trailing_slash:
                        yield (
                            decorator.lineno, 0,
                            'F440 Route is Missing Trailing Slash', type(self),
                        )

                for kwarg in decorator.keywords:
                    if kwarg.arg == 'methods' and len(kwarg.value.elts) != 1:
                        yield (
                            decorator.lineno, decorator.col_offset,
                            'F441 Route has more than 1 method', type(self),
                        )

    def _check_call(
            self, call: ast.Call,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        if isinstance(call.func, ast.Attribute) and call.func.attr == 'register_blueprint':
            for kwarg in call.keywords:
                if kwarg.arg == 'url_prefix' and VERSION_PREFIX.fullmatch(kwarg.value.s) is None:
                    yield (
                        call.lineno, call.col_offset,
                        'F450 Blueprint prefix does not match `/v\d+`', type(self),
                    )

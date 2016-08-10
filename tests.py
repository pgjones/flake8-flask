import ast
import re

from flake8_flask import Linter

TEST_CASE = """
@app.route('/no_slash') # F440
def no_slash():
    pass

@app.route('/too_many_methods/', methods=['GET', 'POST']) # F441
def too_many_methods():
    pass

@app.route('/ok/', methods=['GET'])
def ok():
    pass

app.register_blueprint(good_blueprint, url_prefix='/v0')
app.register_blueprint(bad_blueprint, url_prefix='/v0/bob/') # F450
"""


def test_expected_errors() -> None:
    tree = ast.parse(TEST_CASE)
    expected = set()
    for lineno, line in enumerate(TEST_CASE.splitlines()):
        match = re.search(r'# (.*)$', line.strip('\n'))
        if match:
            for error_code in match.group(1).split():
                expected.add((lineno + 1, error_code))
    checker = Linter(tree, '-')
    codes = set()
    for lineno, _, message, _ in checker.run():
        code, _ = message.split(' ', 1)
        codes.add((lineno, code))
    assert codes == expected

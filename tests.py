import re
import unittest

from config_lang_to_toml import eval_value

class TestConfigParsing(unittest.TestCase):

    def test_single_constant(self):

        constants = parse_config_content("""a is 123""")
        self.assertEqual(constants['a'], 123)

    def test_array_constant(self):

        constants = parse_config_content("""arr is (1, 2, 3)""")
        self.assertEqual(constants['arr'], [1, 2, 3])

    def test_nested_array(self):

        constants = parse_config_content("""nested is ((1, 2), (3, 4))""")
        self.assertEqual(constants['nested'], [[1, 2], [3, 4]])

    def test_string_value(self):

        constants = parse_config_content("""str is hello""")
        self.assertEqual(constants['str'], "hello")

    def test_constant_reference(self):

        constants = parse_config_content("""a is 10\nb is .{a}.""")
        self.assertEqual(constants['b'], 10)

    def test_invalid_syntax(self):
        
        with self.assertRaises(SystemExit):
            parse_config_content("""a 123""")


def parse_config_content(content):

    lines = content.splitlines()
    code = '\n'.join(lines)
    code = re.sub(r'!.*', '', code)
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = '\n'.join(line.strip() for line in code.splitlines() if line.strip())

    constants = {}

    for line in code.splitlines():
        if " is " in line:
            name, value = map(str.strip, line.split(" is ", 1))
            if re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', name):
                constants[name] = eval_value(value, constants)
            else:
                raise SystemExit(f"Ошибка синтаксиса: некорректное имя '{name}' в строке '{line}'")

    return constants

if __name__ == "__main__":
    unittest.main()

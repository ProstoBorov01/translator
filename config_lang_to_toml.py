import re
import sys
import toml


def parse_config(input_file):
   
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
        sys.exit(1)

    code = '\n'.join(lines)
    code = re.sub(r'!.*', '', code)

    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)

    code = '\n'.join(line.strip() for line in code.splitlines() if line.strip())

    constants = {}
    output = {}

    for line in code.splitlines():
        if " is " in line:

            name, value = map(str.strip, line.split(" is ", 1))
            if re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', name):
                constants[name] = eval_value(value, constants)
            else:
                print(f"Ошибка синтаксиса: некорректное имя '{name}' в строке '{line}'")
                sys.exit(1)
        elif re.match(r'^\.\{[a-zA-Z][a-zA-Z0-9]*\}\.$', line):
    
            name = re.findall(r'\.\{([a-zA-Z][a-zA-Z0-9]*)\}\.', line)[0]
            if name in constants:
                print(constants[name])
            else:
                print(f"Ошибка: неопределённая константа '{name}' в строке '{line}'")
                sys.exit(1)
        else:
          
            print(f"Ошибка синтаксиса: строка '{line}' не распознана")
            sys.exit(1)

        output[name] = constants[name]

    return output


def eval_value(value, constants):

    value = value.strip()

    if re.match(r'^\d+$', value):
        return int(value)

    if re.match(r'^\(.*\)$', value):
        elements = re.findall(r'[^,\s]+', value[1:-1])
        return [eval_value(el, constants) for el in elements]

    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
        return value

    if value in constants:
        return constants[value]

    raise ValueError(f"Неверное значение: '{value}'")


def config_to_toml(output):
    
    return toml.dumps(output)


def main():

    if len(sys.argv) != 2:
        print("Использование: python script.py <путь к файлу>")
        sys.exit(1)

    input_file = sys.argv[1]
    output = parse_config(input_file)
    toml_output = config_to_toml(output)
    print(toml_output)


if __name__ == "__main__":
    main()

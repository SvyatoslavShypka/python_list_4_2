import sys
from os import environ


def get_env():
    env_dict = {}
    for env in environ:
        if env not in env_dict:
            env_dict[env] = environ[env]
    sorted_dict = dict(sorted(env_dict.items()))
    return sorted_dict


def print_env(sorted_dict, lista):
    processed_output = []
    for key, values in sorted_dict.items():
        if not lista:
            processed_output.append(key + " = " + values)
        else:
            if key in lista:
                processed_output.append(key + " = " + values)
    # Złączamy w jeden String
    processed_text = '\n'.join(processed_output)
    # Wyprowadzamy na stdout
    sys.stdout.buffer.write(processed_text.encode())


if __name__ == "__main__":
    lista = []
    for i in range(1, len(sys.argv)):
        lista.append(sys.argv[i])
    # testowy wydruk     python lab_4_1.py WINDIR OS PATH
    print_env(get_env(), lista)

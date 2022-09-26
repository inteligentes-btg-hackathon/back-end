import base64


class Formatter:
    def cpf(cpf):
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

    def number(number):
        return f'R$ {number:,.2f}'


class Base64Manager:
    def file_to_base64(filepath):
        with open(filepath, "rb") as file:
            base64file = base64.b64encode(file.read())

        return base64file

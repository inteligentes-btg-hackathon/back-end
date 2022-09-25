class Formatter:
    def cpf(cpf):
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

    def number(number):
        return f'R$ {number:,.2f}'

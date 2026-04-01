def formatar_palavra(tipo, palavra_de, genero):
    if tipo != 'Substantivo':
        return palavra_de
    else:
        cores = {'Masculino':'blue',
                  'Feminino':'pink',
                  'Neutro':'gray'}

        return f'<span style = "color:{cores[genero]};">{palavra_de}</span>'
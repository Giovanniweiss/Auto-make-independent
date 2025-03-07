import os
import re
import sys

def gerar_novo_nome(caminho_novo, nome_original, caminho_temp):
    # Remove a extensão do nome original, se houver
    nome_sem_extensao = os.path.splitext(nome_original)[0]

    # 2.1 - Identifica o nome da pasta. Se tiver um padrão yyy, onde y são dígitos, toma como meio do nome.
    pasta_atual = os.path.basename(caminho_novo)
    padrao_yyy = re.compile(r'^\d{3}$')
    if not padrao_yyy.match(pasta_atual):
        return "inválido"
    meio_nome = pasta_atual

    # 2.2 - Identifica o nome da pasta anterior no caminho. Se começar com padrão xxxx, onde x são dígitos, toma como início do nome.
    pasta_anterior = os.path.basename(os.path.dirname(caminho_novo))
    padrao_xxxx = re.compile(r'^\d{4}')
    match_xxxx = padrao_xxxx.match(pasta_anterior)
    if not match_xxxx:
        return "inválido"
    inicio_nome = match_xxxx.group()

    # 2.3 - Na pasta destino, utilizando o padrão de nome, começa uma verificação de nomes
    nome_padrao = f"{inicio_nome}-{meio_nome}-"
    contador = 0

    while contador <= 999:  # Limite de 999 para o contador
        # 2.3.1 - Verifica a existência dos nomes por ordem "xxxx-yyy-000", então "xxxx-yyy-001". Números múltiplos de 10 devem ser pulados, incluindo 000.
        if contador % 10 == 0 and contador != 0:
            contador += 1
            continue
        novo_nome = f"{nome_padrao}{contador:03d}"  # Garante 3 dígitos, preenchendo com zeros à esquerda
        caminho_completo = os.path.join(caminho_novo, novo_nome)

        # Verifica se o nome já existe, ignorando extensões
        nome_existe = any(
            f.startswith(novo_nome) and os.path.isfile(os.path.join(caminho_novo, f))
            for f in os.listdir(caminho_novo)
        )

        if not nome_existe:
            # 2.3.2 - Quando identificar um que não existe ainda, salva este nome ao arquivo temp
            with open(caminho_temp, 'w') as arquivo_temp:
                arquivo_temp.write(novo_nome)
            return novo_nome
        contador += 1

    # Se o contador ultrapassar 999, retorna "inválido"
    return "inválido"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script.py <caminho_novo> <nome_original> <caminho_temp>")
        sys.exit(1)

    caminho_novo = sys.argv[1]
    nome_original = sys.argv[2]
    caminho_temp = sys.argv[3]

    resultado = gerar_novo_nome(caminho_novo, nome_original, caminho_temp)
    print(resultado)
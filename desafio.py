import textwrap
import re

def menu():
    menu = """\n
    ========== MENU ==========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Falha! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Falha! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Falha! Número máximo de saques excedidos. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Falha! O valor informado é inválido. @@@")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================")

def cadastrar_cliente(usuarios):
    nome = input("Informe o nome do cliente: ")
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
    cpf = input("Informe o CPF (somente números): ")
    
    cpf = re.sub(r'\D', '', cpf)
    
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("\n@@@ CPF já cadastrado! @@@")
            return
    
    endereco = input("Informe o endereço (logradouro, numero, bairro, cidade/UF): ")
    
    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    })
    
    print("\n=== Cliente cadastrado com sucesso! ===")

def cadastrar_conta_bancaria(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do cliente para vincular a conta: ")
    
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado:
        conta = {
            'agencia': agencia,
            'numero_conta': numero_conta,
            'usuario': usuario_encontrado
        }
        print(f"\n=== Conta criada com sucesso! Número da conta: {numero_conta} ===")
        return conta
    else:
        print("\n@@@ Usuário não encontrado! @@@")
        return None

def listar_contas(contas):
    if not contas:
        print("\n@@@ Não há contas cadastradas. @@@")
        return
    
    print("\n========== LISTA DE CONTAS ==========")
    for conta in contas:
        print(f"Agência: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print(f"Cliente: {conta['usuario']['nome']}")
        print("-----------------------------------")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            cadastrar_cliente(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = cadastrar_conta_bancaria(agencia=AGENCIA, numero_conta=numero_conta, usuarios=usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação incorreta! Por favor, selecione novamente a operação desejada.")

main()

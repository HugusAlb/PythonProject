import sys
import os
import uuid
import pyfiglet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n\nPressione [ENTER] para voltar ao menu...")

def conectar_banco():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    if getattr(sys, 'frozen', False):
        diretorio_atual = os.path.dirname(sys.executable)
    else:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
    caminho_json = os.path.join(diretorio_atual, "credenciais.json")
    
    if not os.path.exists(caminho_json):
        raise FileNotFoundError(f"O arquivo 'credenciais.json' não foi encontrado na pasta: {diretorio_atual}")

    creds = ServiceAccountCredentials.from_json_keyfile_name(caminho_json, scope)
    client = gspread.authorize(creds)
    
    return client.open("Banco-Alunos").sheet1

def cadastrar(sheet):
    limpar_tela()
    print("--- NOVO CADASTRO ---\n")
    
    nome = input('Digite o nome do aluno: ').lower()
    try:
        idade = int(input('Digite a idade do aluno: '))
        nota = float(input("Digite a nota do aluno: "))
    except ValueError:
        print("\nErro: Idade ou Nota inválidas (digite apenas números).")
        pausar()
        return

    novo_id = str(uuid.uuid4())

    print("\nSalvando na nuvem...")
    
    sheet.append_row([novo_id, nome, idade, nota])
    
    print('\nAluno cadastrado com sucesso!')
    pausar()

def listar(sheet):
    limpar_tela()
    print("--- CARREGANDO DADOS ---\n")
    
    lista_de_alunos = sheet.get_all_records()
    total = len(lista_de_alunos)
    
    limpar_tela()
    print(f'=== LISTA DE ALUNOS ({total} registros) ===\n')
    
    print(f"{'NOME':<20} | {'IDADE':<10} | {'NOTA'}")
    print("-" * 40)
    
    for aluno in lista_de_alunos:
        nome = aluno.get("Nome", "---")
        idade = aluno.get("Idade", "--")
        nota = aluno.get("Nota", "--")
        
        print(f"{nome:<20} | {str(idade) + ' anos':<10} | {nota}")
    
    pausar()

def buscar(sheet):
    limpar_tela()
    procurado = input('Digite o nome do Aluno para buscar: ').lower()
    
    print("\nBuscando...")
    try:
        cell = sheet.find(procurado)
        aluno_dados = sheet.row_values(cell.row)
        
        limpar_tela()
        print(f'--- ALUNO ENCONTRADO ---\n')
        print(f'ID:    {aluno_dados[0]}')
        print(f'Nome:  {aluno_dados[1]}')
        print(f'Idade: {aluno_dados[2]} anos')
        print(f'Nota:  {aluno_dados[3]}')
        
    except gspread.exceptions.CellNotFound:
        print('\nAluno não consta no sistema!')
    
    pausar()

def remover(sheet):
    limpar_tela()
    procurado = input('Digite o nome do Aluno para remover: ').lower()
    
    print("\nProcurando...")
    try:
        cell = sheet.find(procurado)
        sheet.delete_rows(cell.row)
        print(f'\nSucesso! Aluno {procurado} removido da base.')
    except gspread.exceptions.CellNotFound:
        print(f"\nErro: Não foi possível achar o aluno {procurado}")
    
    pausar()

def mediana(sheet):
    limpar_tela()
    print("Calculando média...\n")
    
    lista_de_alunos = sheet.get_all_records()
    
    if not lista_de_alunos:
        print("Não há alunos para calcular a média.")
        pausar()
        return

    soma_notas = 0
    total_alunos = 0
    
    for aluno in lista_de_alunos:
        try:
            nota_str = str(aluno.get("Nota", 0)).replace(',', '.')
            soma_notas += float(nota_str)
            total_alunos += 1
        except ValueError:
            continue
    
    if total_alunos > 0:
        media_final = soma_notas / total_alunos
        print(f'A média das notas da turma é: {media_final:.2f}')
    else:
        print("Não foi possível calcular a média.")
        
    pausar()

def main():
    limpar_tela()
    print("Conectando ao Google Sheets...")
    
    try:
        sheet = conectar_banco()
    except FileNotFoundError as fnf_error:
        print(f"\nERRO DE ARQUIVO:\n{fnf_error}")
        print("\nDICA: Certifique-se de que o arquivo 'credenciais.json' está na mesma pasta do executável.")
        input("\nPressione ENTER para sair...")
        return
    except Exception as e:
        print(f"Erro crítico ao conectar: {e}")
        input("\nPressione ENTER para sair...")
        return

    while True:
        limpar_tela()
        
        try:
            print(pyfiglet.figlet_format('Santa Ursula', font='slant'))
        except:
            print("--- SANTA URSULA ---\n")
            
        print("SISTEMA DE GESTÃO ESCOLAR")
        print("="*30)
        print("1 - Cadastrar Aluno")
        print("2 - Listar Alunos")
        print("3 - Buscar Aluno")
        print("4 - Remover Aluno")
        print("5 - Calcular Média da Turma")
        print("0 - Sair")
        print("="*30)
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '0':
            limpar_tela()
            print('Saindo do sistema. Até logo!')
            input("\nPressione ENTER para fechar a janela...")
            break
        elif opcao == '1':
            cadastrar(sheet)
        elif opcao == '2':
            listar(sheet)
        elif opcao == '3':
            buscar(sheet)
        elif opcao == '4':
            remover(sheet)
        elif opcao == '5':
            mediana(sheet)
        else:
            print("\nOpção inválida!")
            input("Pressione Enter para tentar novamente...")

if __name__ == "__main__":
    main()
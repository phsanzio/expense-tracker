import pandas as pd
import os
import argparse

def load_data():
    if os.path.exists('expenses.csv'):
        df = pd.read_csv('expenses.csv')
    else:
        # Cria DataFrame vazio já com os tipos certos
        df = pd.DataFrame({
            'Nome': pd.Series(dtype='str'),
            'Valor': pd.Series(dtype='float'),
            'Categoria': pd.Series(dtype='str')
        })
    return df

def save_data(df):
    df.to_csv('expenses.csv', index=False)

def add_list(name, value, category):
    df = load_data()
    # Cria a nova linha como DataFrame
    new_data = pd.DataFrame([[name, value, category]], columns=df.columns)

    # Concatena com segurança
    df = pd.concat([df, new_data], ignore_index=True)

    # Salva no CSV
    save_data(df)
    print(f"Despesa '{name}' adicionada com sucesso.")

def update(id, new_value):
    df = load_data()

    #Procura se o ID existe
    if id in df.index:
        #Troca o valor da despesa
        df.loc[id, 'Valor'] = new_value
        #Salva a mudança no CSV
        save_data(df)
        print(f"Despesa ID '{id}' atualizada para R${new_value:.2f}.")
    else:
        print(f"Despesa ID '{id}' não encontrada.")

def list_expenses():
    #Lista todas as despesas
    df = load_data()
    if not df.empty:
        print(df)
    else:
        print("Nenhuma despesa registrada.")

def delete(id):
    df = load_data()

    #Procura se o ID existe
    if id in df.index:
        #Deleta a despesa
        df.drop(id, inplace=True)
        #Salva a mudança no CSV
        save_data(df)
        print(f"Despesa ID '{id}' deletada com sucesso.")
    else:
        print(f'ID {id} não encontrada.')
    
def summary():
    df = load_data()
    total_expenses = df['Valor'].sum()
    print(f"Total das despesas: R${total_expenses:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")

    parser.add_argument('action', choices=['add', 'list', 'summary', 'delete', 'update'])
    parser.add_argument('--description', type=str, help="Descrição da despesa")
    parser.add_argument('--amount', type=float, help="Valor da despesa")
    parser.add_argument('--id', type=int, help="ID da despesa")
    parser.add_argument('--category', type=str, help="Categoria da despesa")
    parser.add_argument('--new_value', type=float, help="Novo valor para a despesa")

    args = parser.parse_args()
    if args.action == 'add':
        if args.description and args.amount and args.category:
            add_list(args.description, args.amount, args.category)
        else:
            print("Erro: Para adicionar uma despesa, forneça a descrição, o valor e a categoria.")
    elif args.action == 'list':
        list_expenses()
    elif args.action == 'delete':
        if args.id is not None:
            delete(args.id)
        else:
            print("Erro: Para deletar, forneça um ID válido.")
    elif args.action == 'update':
        if args.id is not None and args.new_value is not None:
            update(args.id, args.new_value)
        else:
            print("Erro: Para atualizar, forneça um ID e o novo valor.")
    elif args.action == 'summary':
        summary()
    else:
        print('Erro: Comando não existe ou incompleto!')

if __name__ == '__main__':
    main()
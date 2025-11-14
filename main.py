from sistema import GerenciadorDeTarefas

def main():
    gerenciador = GerenciadorDeTarefas()

    while True:
        print("\n--- MENU ---\n1. Adicionar Tarefa\n2. Listar tarefas\n3. Atualizar status de tarefa\n4. Remover tarefa\n5. Ver alertas de prazo\n6. Sair" )
        menu = input().strip()
        match menu:
            case "6":
                print("Gerenciador de tarefas finalizado!")
                break
           
            case "1":
                descricao = input("Descrição da tarefa: ")
                cliente = input("Insira o nome do solicitante/cliente da tarefa: ")
                prazo_input = input("Se houver prazo para conclusão da tarefa, indique aqui (dd/mm/aaaa), se não, deixe vazio: ").strip()
                if prazo_input:
                    try:
                        dia, mes, ano = prazo_input.split('/')
                        prazo = f'{ano}-{mes}-{dia}'
                    except ValueError:
                        print('⚠️Formato inválido! Use o formato dd/mm/aaaa ⚠️')
                        continue
                else:
                    prazo = None

                print("Digite o status da tarefa:\n1. Concluído\n2. Em andamento\n3. Pendente ")
                escolha_status = input().strip()
                if escolha_status == "1":
                    status = "Concluído"
                elif escolha_status == "2":
                    status = "Em andamento"
                elif escolha_status == "3":
                    status = "Pendente"
                else:
                    print("⚠️ Digite uma resposta válida!⚠️")
                    continue

                try:
                    valor = float(input("Digite o valor do serviço: "))
                except ValueError:
                    print("⚠️ Valor inválido! Insira um valor válido!⚠️ ")
                    continue

                gerenciador.adicionar_tarefa(descricao, cliente, status, prazo, valor ) 
                print(f"Tarefa adicionada com sucesso! Status inicial: {status} ✅ ")
           
            case "2":
                tarefas = gerenciador.listar_tarefas()
                if not  tarefas:
                    (print("Nenhuma tarefa registrada! "))
                    continue
                for tarefa in tarefas:
                    print(tarefa)
            
            case "3":
                tarefas = gerenciador.listar_tarefas()
                if not tarefas:
                    print("Nenhuma tarefa registrada! ")
                    continue
                for tarefa in tarefas:
                    print(tarefa)

                try:
                    print("Digite o ID da tarefa que deseja atualizar: ")
                    id_tarefa = int(input().strip())
                except ValueError:
                    print("⚠️ ID inválido ou inexistente! Por favor, insira um ID válido! ⚠️")
                    continue

                print("Digite o novo status da tarefa:\n1. Concluído\n2. Em andamento\n3. Pendente ")
                escolha = input().strip()
                if escolha == "1":
                    novo_status = "Concluído"
                elif escolha ==  "2":
                     novo_status = "Em andamento"
                elif escolha ==  "3":
                     novo_status = "Pendente"
                else:
                    print("⚠️ Digite uma resposta válida!⚠️")
                    continue

                gerenciador.atualizar_status(id_tarefa, novo_status)
                print(f"O status da tarefa {id_tarefa} foi atualizado com sucesso!✅ ")
            
            case "4":
                tarefas = gerenciador.listar_tarefas()
                if not tarefas:
                    print("Nenhuma tarefa registrada! ")
                    continue
                for tarefa in tarefas:
                    print(tarefa)
                
                
                try:
                    print("Digite o ID da tarefa que você deseja remover: ")
                    id_tarefa = int(input())
                except ValueError:
                    print("⚠️ ID inválido ou inexistente! Por favor, insira um ID válido! ⚠️")
                    continue

                gerenciador.remover_tarefa(id_tarefa)
                print(f"A tarefa {id_tarefa} foi removida com sucesso!✅")

            case "5":
                print("Deseja ver a lista de tarefas que vencem no prazo de quantos dias? Digite '0' para ver as tarefas vencidas ")
                dias_vencimento = int(input().strip())
                alertas = gerenciador.verificador_prazos(proximos_dias=dias_vencimento)
                if not alertas:
                    print(f"✅ Nenhuma tarefa para ser entregue nos próximos {dias_vencimento} dias! ✅")
                else:
                    print("\n--- ALERTAS DE PRAZO ---")
                    for alerta in alertas:
                        id, descricao, prazo, mensagem = alerta
                        print(f"Tarefa {id}: {descricao} | Prazo: {prazo} | {mensagem}")
                

    
if __name__ == "__main__":
    main()

#Definir onde os arquivos serão salvos;
#será definido o nome do arquivo;
#o app será escrito e lido;
#será definido se o arquivo será feito ou não;
#usando o log win+ . se cria os emoji;
#a lista SEMPRE começa vazia;
#ao escrever o item será colocado em novas linhas;


print(" Minha Lista de Desejos para o Futuro\n")

NOME_ARQUIVO = " meus_desejos.txt"
desejos = []


try: 


  with open (NOME_ARQUIVO, 'r', encording = 'utf-8') as arquivo:
    for linha in arquivo:

        desejos.append(linha.strip())

        print (f"Meus desejos foram carregados do arquivo '{NOME_ARQUIVO}'!\n")
        
except FileNotFoundError:
        print ("Parece que é sua primeira vez! Vamos criar sua lista de desejos.\n")
except Exception as e:
            print(f"Ocorreu um erro ao carregar os desejos: {e}")

            def salvar_desejos (lista_de_desejos):

try: 

    with open (NOME_ARQUIVO, 'r', encording = 'utf-8') as arquivo: 
      for desejo in lista_de_desejos:
                    arquivo.write (desejo + "\n")
            print("\n✅ Seus desejos foram salvos com sucesso!")
except Exception as e:
            print(f"\n❌ Erro ao salvar os desejos: {e}")    

            while True:
                print("\n--- O que você quer fazer?")
                print("1 - Adicionar um novo desejo")
                print("2 - Ver meus desejos")
                print("3 - Sair")

                opcao = input (" Digite sua opção (1, 2 ou 3)")

                if opcao == "1":
                    novo_desejo = input ("Qual é o seu novo desejo para o futuro?")
                    if novo_desejo.strip():
                     
                        desejos.append(novo_desejo.strip())
                        salvar_desejos(desejos) 
                    else:
                        print ("Desejo pode ser vazio! Tente novamente.")

                  if opcao == "2":
                    print ("\n✨ Seus Desejos para o Futuro ✨")
                    if not desejos: 
                        print ("Ainda nao há desejos na sua lista. Que tal adicionar um?")
                    else: 
                        for i, desejo in enumerate (desejos):
                            print(f"{1+1}. {desejo}")
                    print("-----------------------")

                    if opcao == "3":
                        print ("Até na próxima! Continue sonhando alto!")
                        break
                    else:
                        print ("Opção inválida. Por favor, digite 1, 2 ou 3.")
                

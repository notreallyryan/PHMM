from Process import Requests

def main():
    Requester = Requests.Requests()
    threshold = float(input("Enter threshold decimal to use for model building. \n" + 
                      "The fraction of amino acids observed at an index must exceed this number to be considered a key feature. \n"))
    
    print("\nTraining Models...")
    Requester.make_model(threshold)
    print("Training Done! \n")

    print("Reading Queries...")
    Requester.make_queries()
    print("Queries loaded! \n")

    print("Loaded Models: ")
    models = Requester.return_loaded_models()
    print(*models, sep=', ')

    print("\nLoaded Queries: ")
    queries = Requester.return_loaded_queries()
    print(*queries, sep=', ')

    Running = True

    while Running:
        user_input = input("\nPlease input a valid Query to test: \n")
        print("\n")

        while user_input not in queries:
            user_input = input("Invalid input! Please re-enter a valid query. \n")
            print("\n")

        print("Processing...\n")
        Most_likely = Requester.return_most_likely(user_input)
        print(user_input + " best matches the protein family model "+ Most_likely + "\n")

        while True:
            Cont = input("Process another query? [Y/N]\n")
            if Cont == "Y": break
            elif Cont == "N":
                Running = False
                break
            else: print("\nInvalid input.\n")
        

if __name__ == '__main__':
    main()
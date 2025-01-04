from md5_core import md5_with_viz

def main():
    print("MD5 Hashing Process Demonstration")
    print("=================================")
    
    while True:
        print("\nChoose an option:")
        print("1. Hash a string")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == '1':
            text = input("\nEnter text to hash: ")
            print("\nStarting MD5 hashing process...")
            print("--------------------------------")
            
            result = md5_with_viz(text.encode('utf-8'))
            
            print("\nFinal MD5 hash:")
            print(result)
            
        elif choice == '2':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()

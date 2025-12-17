import sys
from src.im_controller import IMController

def main():
    controller = IMController()
    print("Marathi Phonetic Input CLI (Type 'exit' to quit)")
    print("-----------------------------------------------")
    
    while True:
        try:
            text = input("English > ")
            if text.lower() in ['exit', 'quit']:
                break
            
            suggestions = controller.get_suggestions(text)
            
            # Display best match and others
            print(f"Best Match > {suggestions[0]}")
            if len(suggestions) > 1:
                print(f"All Options > {', '.join(suggestions)}")
            print("-" * 20)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

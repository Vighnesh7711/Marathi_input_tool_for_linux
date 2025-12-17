import sys
import os
from src.im_controller import IMController

def main():
    print("Maza Marathi - Learning Mode Test")
    print("-------------------------------------------")
    
    # Initialize controller
    controller = IMController()
    
    # Check if user dict exists and clear it for clean test (optional, but good for demo)
    if os.path.exists(controller.user_dict_path):
        print(f"Loading existing user dictionary from {controller.user_dict_path}")
    else:
        print("No user dictionary found. Starting fresh.")

    while True:
        try:
            text = input("\nType English (or 'exit'): ")
            if text.lower() in ['exit', 'quit']:
                break
            
            suggestions = controller.get_suggestions(text)
            
            print(f"Suggestions:")
            for i, s in enumerate(suggestions):
                print(f"  {i+1}. {s}")
                
            choice = input(f"Select word (1-{len(suggestions)}) to 'commit' and learn, or Enter for defaults: ")
            
            if choice.strip() and choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(suggestions):
                    selected = suggestions[idx]
                    print(f"Committing: {selected}")
                    
                    # SIMULATE IBus logic: Train on commit
                    controller.train(text, selected)
                    print("(Learned preference!)")
                    
                    # Verify immediate effect (RAM)
                    new_suggestions = controller.get_suggestions(text)
                    print(f"creating new suggestions order: {new_suggestions}")
                else:
                    print("Invalid selection.")
            else:
                print("No selection made.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

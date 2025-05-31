#!/usr/bin/env python
from activities import activities, history
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    print("Welcome to the Library Management System!")
    
    while True:
        clear_screen()
        working_activities = history[-1] if history else activities
        
        # Print menu
        current_menu = "Main Menu" if not history else "Sub Menu"
        print(f"\n{current_menu}:")
        for key, value in working_activities.items():
            print(f"{key}. {value['message']}")
        
        selection = input("\nSelect an option: ").strip()
        
        if selection.lower() == "exit":
            break
            
        if selection == "0":  # Go back
            if history:
                history.pop()
            continue
            
        if selection in working_activities:
            activity = working_activities[selection]
            
            if "action" in activity:
                try:
                    activity["action"]()
                    input("\nPress Enter to continue...")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    input("Press Enter to continue...")
            
            if "options" in activity:
                history.append(activity["options"])
        else:
            print("❌ Invalid selection!")
            input("Press Enter to continue...")
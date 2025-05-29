
#/usr/bin/env python
from activities import activities, current_activity, history

if __name__ == "__main__":
    print("Welcome to the book keeping application!!")

    while True:
        working_activities = current_activity if current_activity != None else activities

        for key, value in working_activities.items():
            print(f"{key}. {value['message']}")

        selection = input("\nSelect an option: ")

        if selection == "exit":
            break

        if selection == "0":
            history.pop()
            current_activity = None if len(history) == 0 else history[-1]
            continue

        if selection in activities:
            if "action" in working_activities[selection]:
                working_activities[selection]["action"]()
        
            if "options" in working_activities[selection]:
                current_activity = working_activities[selection]["options"]
                history.append(current_activity)
        
        else:
            print("Please select an option!!!")
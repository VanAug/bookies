import actions

history = []
current_activity = None

activities = {
    "1": {
        "message": "View Library",
        "options": {
            "1": {"message": "View Books", "action": actions.view_books},
            "2": {"message": "View Users", "action": actions.view_users},
            "3": {"message": "View Authors", "action": actions.view_authors},
            "4": {"message": "View Borrow Logs", "action": actions.view_borrow_logs},
            "0": {"message": "Go Back"}
        }
    },
    "2": {"message": "Add User", "action": actions.add_user},
    "3": {"message": "Add Author", "action": actions.add_author},
    "4": {"message": "Add Book", "action": actions.add_book},
    "5": {"message": "Mark as Borrowed", "action": actions.mark_as_borrowed},
    "6": {"message": "Mark as Returned", "action": actions.mark_as_returned},
    "7": {"message": "View Available Books", "action": actions.get_available_books},
    "8": {"message": "View Borrowed Books", "action": actions.get_borrowed_books},
    "9": {
        "message": "Delete Items",
        "options": {
            "1": {"message": "Delete User", "action": actions.delete_user},
            "2": {"message": "Delete Author", "action": actions.delete_author},
            "3": {"message": "Delete Book", "action": actions.delete_book},
            "0": {"message": "Go Back"}
        },
    },
    "10": {
        "message": "Search",
        "options": {
            "1": {"message": "Search User", "action": actions.find_user},
            "2": {"message": "Search Author", "action": actions.find_author},
            "3": {"message": "Search Book", "action": actions.find_book},
            "0": {"message": "Go Back"}
        }
    },
    "Exit": {"message": "Exit Application"}
}
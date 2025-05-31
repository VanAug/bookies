
import actions

history = [] #track history of menus
current_activity = None

activities = {
    "1" : {
        "message" : "View Library",
        "options" : {
            "1" : {
                "message" : "View Books",
                "action" : actions.view_books
            },
            "2" : {
                "message" : "View Users",
                "action" : actions.view_users
            },
            "3" : {
                "message" : "View Authors",
                "action" : actions.view_authors
            },
            "4" : {
                "message" : "View Borrow Logs",
                "action" : actions.view_borrow_logs
            },
            "0" : {
                "message" : " Go Back"
            }
        }
    },
    "2" : {
        "message" : "Add User",
        "action" : actions.add_user
    },
    "3" : {
        "message" : "Add author",
        "action" : actions.add_author
    },
    "4" : {
        "message" : "Add book",
        "action" : actions.add_book
    },
    "5" : {
        "message" : "Mark as Borrowed.",
        "action" : actions.mark_as_borrowed
    },
    "6" : {
        "message" : "Mark as Returned",
        "action" : actions.mark_as_returned
    },
    "7" : {
        "message" : "View available books.",
        "action" : actions.get_available_books
    },
    "8" : {
        "message" : "View borrowed books.",
        "action" : actions.get_borrowed_books
    },
    "Exit" : {
        "message" : "Exit application.",
    },
}
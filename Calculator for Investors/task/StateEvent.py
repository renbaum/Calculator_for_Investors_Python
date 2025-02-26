from enum import Enum
from database import Database

class State(Enum):
    EXIT = 0
    MAIN_MENU = 1
    CRUD_MENU = 2
    TOP_TEN_MENU = 3
    LIST_COMPANIES = 4
    DELETE_COMPANY = 5
    UPDATE_COMPANY = 6
    READ_COMPANY = 7
    CREATE_COMPANY = 8
    LIST_COMPANIES_BY_ROA = 9
    LIST_COMPANIES_BY_ROE = 10
    LIST_COMPANIES_BY_ND_EBITDA = 11

class StateEvent:
    def __init__(self, state):
        from menu import Menu
        self.state = state
        self.menu = Menu()
        self.database = Database()

    def handle_state(self) -> bool:
        state_actions = {
            State.MAIN_MENU: self.menu.main_menu,  # Maps states to respective functions.
            State.CRUD_MENU: self.menu.crud_menu,
            State.TOP_TEN_MENU: self.menu.top_ten_menu,
        }
        if self.state == State.EXIT:
            return False  # Exit the loop.

        action = state_actions.get(self.state)
        if action:
            self.state = action()  # Call the mapped function and update state.
        else:
            print("Not implemented!")  # Handle unspecified state.
            print()
            self.state = State.MAIN_MENU

        return True

    def get_state(self) -> State:
        return self.state

    def set_state(self, state: State):
        self.state = state

    def main_loop(self):
        while True:
            if not self.handle_state():
                break
        print("Have a nice day!")


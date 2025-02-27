from database import Database
from state import State
from menu import Menu


class StateEvent:
    def __init__(self, state):
        self.state = state
        self.menu = Menu()
        self.database = Database()

    def handle_state(self) -> bool:
        state_actions = {
            State.MAIN_MENU: self.menu.main_menu,  # Maps states to respective functions.
            State.CRUD_MENU: self.menu.crud_menu,
            State.TOP_TEN_MENU: self.menu.top_ten_menu,
            State.CREATE_COMPANY: self.database.create_company,
            State.READ_COMPANY: self.database.read_company,
            State.UPDATE_COMPANY: self.database.update_company,
            State.DELETE_COMPANY: self.database.delete_company,
            State.LIST_COMPANIES: self.database.list_companies,
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


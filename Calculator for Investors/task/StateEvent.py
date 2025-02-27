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
            State.MAIN_MENU: (self.menu.main_menu, None),  # Maps states to respective functions and their required params.
            State.CRUD_MENU: (self.menu.crud_menu, None),
            State.TOP_TEN_MENU: (self.menu.top_ten_menu, None),
            State.CREATE_COMPANY: (self.database.create_company, None),
            State.READ_COMPANY: (self.database.read_company, None),
            State.UPDATE_COMPANY: (self.database.update_company, None),
            State.DELETE_COMPANY: (self.database.delete_company, None),
            State.LIST_COMPANIES: (self.database.list_companies, None),
            State.LIST_COMPANIES_BY_ND_EBITDA: (self.database.list_companies_by_calc, State.LIST_COMPANIES_BY_ND_EBITDA),
            State.LIST_COMPANIES_BY_ROE: (self.database.list_companies_by_calc, State.LIST_COMPANIES_BY_ROE),
            State.LIST_COMPANIES_BY_ROA: (self.database.list_companies_by_calc, State.LIST_COMPANIES_BY_ROA),
        }
        if self.state == State.EXIT:
            return False  # Exit the loop.

        action = state_actions.get(self.state)
        if action:
            func, param = action
            self.state = func(param) if param else func()  # Call the mapped function with or without parameters.
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


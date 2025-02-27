from state import State

class Menu:
    def __init__(self):
        pass

    def main_menu(self):
#        print()
        print("MAIN MENU")
        print("0 Exit")
        print("1 CRUD operations")
        print("2 Show top ten companies by criteria")
#        print()
        return self.choice_main_menu()

    def choice_main_menu(self):
        answer = self.get_user_choice()
        match answer:
            case 0: return State.EXIT
            case 1: return State.CRUD_MENU
            case 2: return State.TOP_TEN_MENU
            case _:
                print("Invalid option!")
#                print()
                return State.MAIN_MENU

    def top_ten_menu(self):
        print()
        print("TOP TEN MENU")
        print("0 Back")
        print("1 List by ND/EBITDA")
        print("2 List by ROE")
        print("3 List by ROA")
#        print()
        return self.choice_top_ten_menu()

    def choice_top_ten_menu(self):
        answer = self.get_user_choice()
        match answer:
            case 0: return State.MAIN_MENU
            case 1: return State.LIST_COMPANIES_BY_ND_EBITDA
            case 2: return State.LIST_COMPANIES_BY_ROE
            case 3: return State.LIST_COMPANIES_BY_ROA
            case _:
                print("Invalid option!")
#                print()
                return State.MAIN_MENU

    def crud_menu(self):
        print()
        print("CRUD MENU")
        print("0 Back")
        print("1 Create a company")
        print("2 Read a company")
        print("3 Update a company")
        print("4 Delete a company")
        print("5 List all companies")
#        print()
        return self.choice_crud_menu()

    def choice_crud_menu(self):
        answer = self.get_user_choice()
        match answer:
            case 0: return State.MAIN_MENU
            case 1: return State.CREATE_COMPANY
            case 2: return State.READ_COMPANY
            case 3: return State.UPDATE_COMPANY
            case 4: return State.DELETE_COMPANY
            case 5: return State.LIST_COMPANIES
            case _:
                print("Invalid option!")
#                print()
                return State.MAIN_MENU

    def get_user_choice(self) -> int:
        print("Enter an option:")
        answer = input()
        if answer.isdigit(): return int(answer)
        return 99
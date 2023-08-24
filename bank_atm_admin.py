from datetime import datetime

admin = {
    "name": "ibrahim",
    "password": "1122",
}

users = {
    "Ahmet": {
        "password": "1234",
        "balance": 0,
    },
    "Zeynep": {
        "password": "4321",
        "balance": 0
    },
    "Alberto": {
        "password": "4422",
        "balance": 0
    }
}

processes = {
    "Ahmet": {
        "deposits": [],
        "withdrawals": [],
        "transfers": [],
    },
    "Zeynep": {
        "deposits": [],
        "withdrawals": [],
        "transfers": [],
    },
    "Alberto": {
        "deposits": [],
        "withdrawals": [],
        "transfers": [],
    },
}


def formatDateTime(dateTime):
    return dateTime.strftime("%d/%m/%y %H:%M:%S")


def select_option(options, title):
    text = title + "\n"
    for index, option in enumerate(options):
        text += str(index + 1) + ". " + option + "\n"
    while True:
        index = input(text)
        if not index.isdigit():
            continue
        index = int(index)
        if index < 1 or index > len(options):
            continue
        return index


def fill_form(form_fields, title):
    print(title)
    res = {}
    for form_field in form_fields:
        res[form_field] = input('Please enter ' + form_field + ': ')
    return res


def admin_menu():
    options = [
        "Add User",
        "Remove User",
        "Display All Users",
        "Exit"
    ]
    title = "Please enter the number of the service:"

    while True:
        index = select_option(options, title)
        if index == 1:
            add_user_page()
        elif index == 2:
            remove_user_page()
        elif index == 3:
            display_all_users_page()
        elif index == 4:
            break


def user_menu(user_name):
    options = [
        "Withdraw Money",
        "Deposit Money",
        "Transfer Money",
        "My Account Information",
        "Logout",
    ]
    title = "Please enter the number of the service"

    while True:
        index = select_option(options, title)
        if index == 1:
            withdraw_money_page(user_name)
        elif index == 2:
            deposit_money_page(user_name)
        elif index == 3:
            transfer_money_page(user_name)
        elif index == 4:
            my_account_information_page(user_name)
        elif index == 5:
            break


def admin_login():
    d = fill_form(["Admin Name", "Admin Password"], "Please enter admin credentials")

    if d["Admin Name"] == admin["name"] and d["Admin Password"] == admin["password"]:
        admin_menu()
    else:
        print("You logged in incorrectly, try again please.")
        admin_login()


def add_user_page():
    d = fill_form(["User Name", "User Password"], "Please enter new user credentials")
    if d["User Name"] in users.keys():
        print("User Name is Already Exists")
        add_user_page()
        return
    if len(d["User Password"]) < 4:
        print("Please Enter Longer Password")
        add_user_page()
        return

    users[d["User Name"]] = {"password": d["User Password"], "balance": 0}
    processes[d["User Name"]] = {"deposits": [], "withdrawals": [], "transfers": []}


def remove_user_page():
    d = fill_form(["User Name"], "")
    if d["User Name"] in users.keys():
        del users[d["User Name"]]
        del processes[d["User Name"]]
    else:
        print("This user is not exist")


def display_all_users_page():
    print(f'There are {len(users.keys())} users using Istinye Bank')
    for i, user_name in enumerate(users.keys()):
        print(f'{i}) {user_name} {users[user_name]["password"]}')


def user_login():
    d = fill_form(["User Name", "User Password"], "Please enter user credentials")

    if d["User Name"] in users.keys() and users[d["User Name"]]["password"] == d["User Password"]:
        user_menu(d["User Name"])
    else:
        print("You logged in incorrectly, try again please.")
        user_login()


def withdraw_money_page(user_name):
    d = fill_form(["Amount"], "Hello withdraw money page")
    amount = int(d["Amount"])

    if users[user_name]["balance"] < amount:
        print("You cannot do this withdrawal, you don't have enough money in your account.")
        return

    dateTime = datetime.now()
    processes[user_name]["withdrawals"].append(
        {
            "amount": amount,
            "date": dateTime,
        }
    )
    users[user_name]["balance"] -= amount


def deposit_money_page(user_name):
    d = fill_form(["Amount"], "Hello deposit money page")
    amount = int(d["Amount"])

    dateTime = datetime.now()
    processes[user_name]["deposits"].append(
        {
            "amount": amount,
            "date": dateTime,
        }
    )
    users[user_name]["balance"] += amount


def transfer_money_page(user_name):
    d = fill_form(["To User Name", "Amount"], "Hello Transfer money page")
    amount = int(d["Amount"])
    to_user_name = d["To User Name"]

    if users[user_name]["balance"] < amount:
        print("You cannot do this transfer, you don't have enough money in your account.")
        return
    if to_user_name not in users.keys():
        print("There is not such a user")
        return

    dateTime = datetime.now()

    processes[user_name]["transfers"].append(
        {
            "incoming": False,
            "to_user_name": to_user_name,
            "amount": amount,
            "date": dateTime,
        }
    )
    users[user_name]["balance"] -= amount

    processes[to_user_name]["transfers"].append(
        {
            "incoming": True,
            "from_user_name": user_name,
            "amount": amount,
            "date": dateTime,
        }
    )
    users[to_user_name]["balance"] += amount


def my_account_information_page(user_name):
    print("Hello user information page")
    print(f'username: {user_name}')
    print(f'password: {users[user_name]["password"]}')
    print(f'balance: {users[user_name]["balance"]}')

    actions = []
    for action in processes[user_name]["withdrawals"]:
        actions.append(
            (action["date"], f'Withdrawal at {formatDateTime(action["date"])} with amount {action["amount"]}')
        )
    for action in processes[user_name]["deposits"]:
        actions.append(
            (action["date"], f'Deposit at {formatDateTime(action["date"])} with amount {action["amount"]}')
        )
    for action in processes[user_name]["transfers"]:
        if action["incoming"] == False:
            actions.append(
                (action["date"],
                 f'Money tranfer at {formatDateTime(action["date"])} with amount {action["amount"]} to {action["to_user_name"]}')
            )
        else:
            actions.append(
                (action["date"],
                 f'Money tranfer at {formatDateTime(action["date"])} with amount {action["amount"]} from {action["from_user_name"]}')
            )

    def get_date(x):
        return x[0]

    actions.sort(key=get_date)
    for action in actions:
        print(action[1])


def welcome():
    while True:  # Bu while işlemlerden çıkış yapınca login ekrarına dönmek içindi
        print("— Welcome to ISTINYE Bank (v.0.2) —\n")
        now = datetime.now()
        print("   -------------------")
        print(" /      İSTANBUL       \ ")
        print("| ", (formatDateTime(now)), " |")
        print(" \                     /")
        print("   -------------------")

        options = [
            "Admin Login",
            "User Login",
            "Exit"
        ]
        option = select_option(options, "")
        if option == 1:
            admin_login()
        elif option == 2:
            user_login()
        elif option == 3:
            break


welcome()








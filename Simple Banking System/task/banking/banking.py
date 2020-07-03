import random
import sqlite3

conn = sqlite3.connect("card.s3db",timeout=10)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS card(id INTEGER,number TEXT,pin TEXT,balance INTEGER DEFAULT 0)")

conn.commit()


def generate():
    credit_card = "400000"
    pin = ""
    num_sum = 0
    for x in range(9):
        credit_card += str(random.randint(0, 9))
    for x in range(4):
        pin += str(random.randint(0, 9))

    # Checks if card is valid
    for x in range(len(credit_card)):
        num = int(credit_card[x])
        if (x + 1) % 2 != 0:
            num = num * 2
            if num > 9:
                num -= 9
            num_sum += num
        else:
            num_sum += num
    for x in range(10):
        if (num_sum + x) % 10 == 0 and str(x):
            credit_card += str(x)
            return credit_card, pin
    generate()

def luhn(ccn):
    c = [int(x) for x in ccn[::-2]]
    u2 = [(2 * int(y)) // 10 + (2 * int(y)) % 10 for y in ccn[-2::-2]]
    return sum(c + u2) % 10 == 0
def check_card(credit_card, pin):
    input1 = input("Enter your card number:\n")
    input2 = input("Enter your PIN:\n")
    check = cur.execute("SELECT number FROM card WHERE number = {} AND pin = {}".format(input1,input2)).fetchone()
    if check is None:
        print("Wrong card number or PIN!")
        menu(0,0)
    if input1 == check[0]:
        print("You have successfully logged in!")
        menu2(input1, input2)
    else:
        print("Wrong card number or PIN!")
        menu(0, 0)


def create_acc(credit_card, pin):
    print("Your card has been created\nYour card number:\n" + credit_card + "\nYour card PIN:\n" + pin)
    return credit_card, pin


def log_in(credit_card, pin):
    check_card(credit_card, pin)


def add_income(credit_card, pin):
    add = int(input("Enter the amount you want to deposit: "))

    cur.execute("UPDATE card SET balance = (SELECT balance FROM card WHERE number = {}) + {} WHERE number = {}".format(credit_card,add,credit_card))
    conn.commit()
    print(cur.execute("SELECT balance FROM card WHERE number = {}".format(credit_card)).fetchone()[0])
    menu2(credit_card,pin)

def balance(credit_card,pin):
    print("Balance:",int(cur.execute("SELECT balance FROM card WHERE number = {}".format(credit_card)).fetchone()[0]))
    menu2(credit_card,pin)


def transfer(credit_card,pin):
    balance = int(cur.execute("SELECT balance FROM card WHERE number = {}".format(credit_card)).fetchone()[0])
    print("Transfer")
    cc = input("Enter card number:")
    if not luhn(cc):
        print("Probably you made mistake in the card number. Please try again!")
        menu2(credit_card,pin)
    if cur.execute("SELECT number FROM card WHERE number = {}".format(cc.strip())).fetchone() is None:
        print("Such a card does not exist.")
        menu2(credit_card,pin)
    if cc != credit_card:
        print("You can't transfer money to the same account!")
        menu2(credit_card,pin)

    money = int(input("How much money do you want to transfer:"))
    if money < 0:
        print("Not a legal amount!")
        menu2(credit_card, pin)
    if money > balance:
        print("Not enough money!")
        menu2(credit_card, pin)
    cur.execute("UPDATE card SET balance = (SELECT balance FROM card WHERE number = {}) + {} WHERE number = {}".format(cc,money,cc))
    conn.commit()
    print(cur.execute("SELECT balance FROM card WHERE number = {}".format(credit_card)).fetchone()[0])
    cur.execute("UPDATE card SET balance = (SELECT balance FROM card WHERE number = {}) - {} WHERE number = {}".format(
        credit_card, money, credit_card))
    conn.commit()
    print(cur.execute("SELECT balance FROM card WHERE number = {}".format(credit_card)).fetchone()[0])
    print("Success!")

    menu2(credit_card,pin)



def close_acc(credit_card,pin):
    cur.execute("DELETE FROM card WHERE number = {}".format(credit_card))
    conn.commit()
    menu(credit_card,pin)


def menu2(credit_card, pin):
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    action = int(input())
    if action == 1:
        balance(credit_card,pin)
    elif action == 2:
        add_income(credit_card, pin)
    elif action == 3:
        transfer(credit_card,pin)
    elif action == 4:
        close_acc(credit_card,pin)
    elif action == 5:
        menu(credit_card, pin)
    else:
        print("Bye!")
        exit()


def menu(credit_card, pin):
    print("1. Create an account\n2. Log into account\n0. Exit")
    action = int(input())
    if action == 1:
        credit_card, pin = generate()
        cur.execute("INSERT INTO card (number,pin,balance) VALUES ({},{},{})".format(credit_card, pin, 0))
        conn.commit()
        create_acc(credit_card, pin)
        menu(credit_card, pin)
    elif action == 2:
        log_in(credit_card, pin)
    else:
        print("Bye!")
        exit()


def main():
    credit_card, pin = generate()
    cur.execute("INSERT INTO card (number,pin,balance) VALUES ({},{},{})".format(credit_card,pin,0))
    conn.commit()
    menu(credit_card, pin)


if __name__ == "__main__":
    main()

conn.close()

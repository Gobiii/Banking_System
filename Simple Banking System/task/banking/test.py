import random
import sqlite3
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("SQL QUERY")
cur.commit()


def generate():
    flag = False
    credit_card = "400000"
    pin = ""
    num_sum = 0
    for x in range(9):
        credit_card += str(random.randint(0,9))
    for x in range(4):
        pin += str(random.randint(0, 9))

    # Checks if card is valid
    for x in range(len(credit_card)):
        num = int(credit_card[x])
        if (x+1) % 2 != 0:
            num = num * 2
            print(num)
            if num > 9:
                num -= 9
            num_sum += num
        else:
            print(num)
            num_sum += num
    print(num_sum)
    for x in range(10):
        if (num_sum + x) % 10 == 0 and str(x):
            credit_card += str(x)
            print(x)
            return credit_card,pin
    generate()
a,b = generate()
print(a,b)

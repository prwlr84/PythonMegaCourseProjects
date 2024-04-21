import pandas as pd


df = pd.read_csv('hotels.csv', dtype={'id': str})


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def is_available(self):
        return df.loc[df['id'] == self.hotel_id, 'available'].squeeze() == 'yes'


class Ticket:
    def __init__(self, c_name, booking):
        self.booking = booking
        self.c_name = c_name

    def generate(self):
        content = f"""
            Thanks! Its booked!
            {self.c_name}
            {self.booking.name}
            """
        print(content)


class Card:
    def __init__(self, u_name, nr, cvc, date):
        self.name = u_name
        self.nr = nr
        self.cvc = cvc
        self.date = date

    def valid(self):
        return self.nr in ['123456678', '87654321']


class SecureCard(Card):
    def auth(self, c, p):
        cd, pw = ['1234', '4321']
        return c == cd and p == pw


print(df)
hotel_id_input = input('Enter hotel ID:')
hotel = Hotel(hotel_id_input)

if hotel.is_available():
    name = input('Enter your name:')
    number = input("Enter card nr:")
    code = input("Enter card cvc:")
    exp = input("Enter card expiry date:")
    credit_card = SecureCard(name, number, code, exp)
    if credit_card.valid():
        p = input("Enter auth code:")
        c = input("Enter auth password:")
        if credit_card.auth(c, p):
            hotel.book()
            ticket = Ticket(name, hotel)
            print(ticket.generate())
        else: print('Auth issue')
    else: print('Not valid')
else:
    print('Not available')

if __name__ == '__main__':
    print('PyCharm')

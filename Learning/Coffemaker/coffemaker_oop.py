class CoffeeMaker:
    water_suply = 0
    milk_suply = 0
    coffee_suply = 0
    cups_suply = 0
    money_suply = 0

    def __init__(self, water=400, milk=540, beans=120, cups=9, money=550):
        CoffeeMaker.water_suply = water
        CoffeeMaker.milk_suply = milk
        CoffeeMaker.coffee_suply = beans
        CoffeeMaker.cups_suply = cups
        CoffeeMaker.money_suply = money


    def inventory(self):
        print("The coffee machine has:")
        print(self.water_suply,"of water")
        print(self.milk_suply,"of milk")
        print(self.coffee_suply,"of coffee beans")
        print(self.cups_suply,"of disposable cups")
        print(self.money_suply,"of money")
        return

    def buy(self):
        self.choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        if self.choice == "1":
            print(self.check_suply(250, 0, 16, 1, 4))
        elif self.choice == "2":
            print(self.check_suply(350, 75, 20, 1, 7))
        elif self.choice == "3":
            print(self.check_suply(200, 100, 12, 1, 6))
        elif self.choice == "exit":
            return

    def fill(self):
        CoffeeMaker.water_suply += int(input("Write how many ml of water do you want to add:"))
        CoffeeMaker.milk_suply += int(input("Write how many ml of milk do you want to add:"))
        CoffeeMaker.coffee_suply += int(input("Write how many grams of coffee beans do you want to add:"))
        CoffeeMaker.cups_suply += int(input("Write how many disposable cups of coffee do you want to add:"))
        return

    def take(self):
        print("I gave you $" + str(CoffeeMaker.money_suply))
        CoffeeMaker.money_suply = 0

    def check_suply(self, water, milk, coffee, cups, money):
        if CoffeeMaker.water_suply < water:
            return "Sorry, not enough water!"
        if CoffeeMaker.milk_suply < milk:
            return "Sorry, not enough milk!"
        if CoffeeMaker.coffee_suply < coffee:
            return "Sorry, not enough coffee!"
        if CoffeeMaker.cups_suply < cups:
            return "Sorry, not enough cups!"
        CoffeeMaker.water_suply -= water
        CoffeeMaker.coffee_suply -= coffee
        CoffeeMaker.milk_suply -= milk
        CoffeeMaker.money_suply += money
        CoffeeMaker.cups_suply -= 1
        return "I have enough resources, making you a coffee!"
        
    def operation(self):
        while True:
            self.action = input("Write action (buy, fill, take, remaining, exit):")
            if self.action == "buy":
                self.buy()
            elif self.action == "fill":
                self.fill()
            elif self.action == "take":
                self.take()
            elif self.action == "remaining":
                self.inventory()
            elif self.action == "exit":
                return

cm = CoffeeMaker()
cm.operation()

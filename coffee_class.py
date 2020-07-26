# refactor coffee machine program to have a single class and a single method to interface with user.

class CoffeeMachine():
    # number of coffee machines. Just want one.
    n_machines = 0

    # coffee properties (price, ingredients), are always true in class
    COFFEE = {"1": [4, 250, 0, 16], "2": [7, 350, 75, 20], "3": [6, 200, 100, 12]}

    # starting ingredients are always the same. Store as dict this time.
    contents = {"money": 550, "water": 400, "milk": 540, "beans": 120, "cups": 9}

    # valid choices: to make sure user put the right thing in
    valid_choices = ["buy", "fill", "take", "remaining", "exit"]
  
    def __init__(self):
        # set starting state of machine
        # self.state = "home"
        # call the UI_method (handles user input)
        # self.UI_method()
        self.redirect()        

    # Only want one coffee machine
    def __new__(cls):
        if cls.n_machines < 1:
            return object.__new__(cls)
        return None

    # UI_method: depending on machine state, the prompt varies. Only way to get user input.
    def UI_method(self):
        if self.state == "home":
            # Keep prompting until valid input
            while True:
                choice = input("Write action (buy, fill, take, remaining, exit):\n").lower()
                # check for valid input
                if choice in self.valid_choices:
                    break
            # update state of machine
            self.state = choice
            # call UI again to redirect
            self.UI_method()
        elif self.state == "buy":
            # Keep prompting until valid input
            # while True:    
            drink = input("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n").lower()
            if drink in self.COFFEE.keys():
                self.buy(drink)
            elif drink == "back":
                print()
                self.redirect()
        elif self.state == "fill":
            # prompt for filling
            self.contents["water"] = self.contents["water"] + int(input("\nWrite how many ml of water do you want to add:\n"))
            self.contents["milk"] = self.contents["milk"] + int(input("Write how many ml of milk do you want to add:\n"))
            self.contents["beans"] = self.contents["beans"] + int(input("Write how many grams of coffee beans do you want to add:\n"))
            self.contents["cups"] = self.contents["cups"] + int(input("Write how many disposable cups of coffee do you want to add:\n"))
            print()
            # redirect home
            self.redirect()
        elif self.state == "take":
            self.take()
        elif self.state == "remaining":
            self.remaining()
        elif self.state == "exit":
            return False
            #self.exit()
        return
        
    # Buy drink. User already chose. This handles checking if enough ingredients, updating ingredients, and updating status.
    def buy(self, drink):
        # Check if enough ingredients. If not enough in any, redirect home.
        if self.contents["cups"] == 0:
            print("Sorry, not enough disposable cups!\n")
            self.redirect()
        elif self.contents["water"] < self.COFFEE[drink][1]:
            print("Sorry, not enough water!\n")
            self.redirect()
        elif self.contents["milk"] < self.COFFEE[drink][2]:
            print("Sorry, not enough milk!\n")
            self.redirect()
        elif self.contents["beans"] < self.COFFEE[drink][3]:
            print("Sorry, not enough coffee beans!\n")
            self.redirect()
        else:
            print("I have enough resources, making you a coffee!\n")
        # update amounts
            self.contents["cups"] = self.contents["cups"] - 1
            self.contents["water"] = self.contents["water"] - self.COFFEE[drink][1]
            self.contents["milk"] = self.contents["milk"] - self.COFFEE[drink][2]
            self.contents["beans"] = self.contents["beans"] - self.COFFEE[drink][3]
            self.contents["money"] = self.contents["money"] + self.COFFEE[drink][0]

        # Update to home state, redirect home
        self.redirect()

    # Remove all money, print out how much there was, update to 0, redirect
    def take(self):
        # remove all money
        print("\nI gave you $" + str(self.contents["money"]) + "\n")
        self.contents["money"] = 0
        self.redirect()

    # Show remaining ingredients. After that, update state to home.
    def remaining(self):
        print("\nThe coffee machine has:")
        print(self.contents["water"], "of water")
        print(self.contents["milk"], "of milk")
        print(self.contents["beans"], "of coffee beans")
        print(self.contents["cups"], "of disposable cups")
        print("$" + str(self.contents["money"]) + " of money\n")
        
        # update state, redirect home
        self.redirect()

    # Method below resets state to home and redirect to home prompt (this happens a lot)
    def redirect(self):
        self.state = "home"
        #self.UI_method()

    # Exit
    #def exit(self):
        #return False


def main():
    # create an instance of the coffee machine
    coffee = CoffeeMachine()

    # Keep prompting user 
    while coffee.state != "exit":
        # Choice() is the method that interacts with user. Output depends on state of machine.
        coffee.UI_method()

main()
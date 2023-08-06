class Submarin:
    '''
    Test 1
        ว่างายยยยย
    '''

    def __init__(self,price=15000,budget=100000):
        self.captain = "xuouCaptan"
        self.sub_name = "PV_Boat"
        self.price = price #Million
        self.kilo = 0
        self.budget = budget
        self.totalcost = 0

    def Missile(self):
        print('We are Department of Missile')

    def Calcommission(self):
        '''this is find commission'''
        percent = self.price * (10/100) #10 Percent
        print('Loong! You got: {} Million Bath'.format(percent))

    def Goto(self,enemypoint,distance) : #distance is kilo
        #print('let\'s go') like #print("let's go")
        print(f"let's go to {enemypoint} Distance : {distance} Km")
        self.kilo = self.kilo+distance
        self.Fuel()

    def Fuel(self): #น้ำมัน
        deisel = 20 #20 baht/litre
        cal_feul_cost = self.kilo * deisel
        print('Current Feul Cost: {:,d} Baht'.format(cal_feul_cost)) #print({:,d}) print({:,.2f}) print({:,.0f})
        self.totalcost += cal_feul_cost

    @property
    def BudgetRemaining(self):
        remaining = self.budget - self.totalcost
        print('Current Feul Cost: {:,.2f} Baht'.format(remaining))
        return remaining

class ElectricSubmarin(Submarin):

    def __init__(self,price=15000,budget=100000):
        self.sub_name = 'name rua dam nam'
        self.battery_distance = 100000
        #Submarine can go out 100000 km/100 percent
        super().__init__(price,budget)

    def Battery(self):
        allbattery = 100
        calculate = (self.kilo/ self.battery_distance)*100
        print("We have battery Remaining: {}%".format(allbattery-calculate))

    def Fuel(self): #น้ำมัน
        kilowatcost = 5 #kilo wat
        cal_feul_cost = self.kilo * kilowatcost
        print('Current Power Cost: {:,d} Baht'.format(cal_feul_cost)) #print({:,d}) print({:,.2f}) print({:,.0f})
        self.totalcost += cal_feul_cost

#print(__name__)
if __name__ == '__main__':
    Tesla = ElectricSubmarin(40000,2000000)
    print(Tesla.captain)
    print(Tesla.budget)
    Tesla.Goto("Japan", 10000)
    #Tesla.Fuel()
    print(Tesla.BudgetRemaining)
    Tesla.Battery()

    print('----------------------------')

    Kongtabbok = Submarin(40000,2000000)
    print(Kongtabbok.captain)
    print(Kongtabbok.budget)
    Kongtabbok.Goto("Japan", 10000)
    print(Kongtabbok.BudgetRemaining)









'''
kongtab = Submarin(53456)
kongtab.Calcommission()
print(kongtab.kilo)
#kongtab.Fuel()
kongtab.Goto("China",7000)
print(kongtab.kilo)
kongtab.Fuel()
current_budget = kongtab.BudgetRemaining
print(current_budget * 0.2)
'''

'''
print("-----------")
kongtabbok = Submarin(70000)
print('before...')
print("captain is : "+kongtabbok.captain)
print('after...')
kongtabbok.captain = "supansaaa Kak Captain"
print("captain is : "+kongtabbok.captain)
'''

'''
print("---------------")

sub = ["Srivara" , "PV_Boat2" , 5000]
print(sub[0])'''

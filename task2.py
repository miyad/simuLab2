import numpy as np
import csv
import heapq
cumulative_probabilites = [0.8,0.95,1.00] #rout type 1,2,3
cum_prob = [0.5,0.8,0.9,1.0]#type of group of people
ARRIVAL, DEPART, EXIT = 1, 2, 3 # global flag variables
def return_row(file):
    f = open(file,'r')
    usable = csv.reader(f)
    arr = []
    for j in usable:
        for k in j:
            a = list(map(float,k.split()))
            arr.append(a)
    return arr
def generate_job_type():##return the type of new job
    uniform = np.random.uniform(0.0,1.0,1)[0]
    i = 0
    for prob in cumulative_probabilites:
        if prob >=uniform:
            #if i == 0:
                #print("i am for not 0 div")
            return i+1
        i = i + 1
    print("Ivalid Job type, return -1")
    return -1
def generate_job_group():
    uniform = np.random.uniform(0.0,1.0,1)[0]
    i = 0
    for prob in cum_prob:
        if prob >=uniform:
            return i+1
        i = i + 1
    print("Ivalid Job type, return -1")
    return -1
class Customer:
    def __init__(self,appeared_at,station_index,group_id,type):
        self.appeared_at = appeared_at
        self.customer_total_delay = 0
        self.total_queue_delay = 0
        self.station_index = station_index
        self.group_id = group_id
        self.type = type
class HotFood:
    def __init__(self,s,ST):#number of server
        #ST is a tuple having (a,b) of service time dist U(a,b)
        self.ST = (ST[0]/s,ST[1]/s)
        self.queue = []
        self.total_queue_delay = 0
        self.served = 0
        self.area_qt = 0
        self.last_event_time = 0
        self.is_server_busy = False
        pass
    def next_depart(self,current_time):
        return current_time + np.random.uniform(self.ST[0],self.ST[1],1)[0]
class Sandwitch:
    def __init__(self,s,ST): #number of server
        #ST is a tuple (a,b) of U(a,b)
        self.ST = (ST[0]/s,ST[1]/s)
        self.queue = []
        self.total_queue_delay = 0
        self.served = 0
        self.area_qt = 0
        self.last_event_time = 0
        self.is_server_busy = False
        pass
    def next_depart(self,current_time):
        return current_time + np.random.uniform(self.ST[0],self.ST[1],1)[0]
class Cashier:
    def __init__(self,s):#numebr of server,queue and service time tuple 
        self.queue = []
        for i in range(s):
            self.queue.append([])
        self.is_cashier_busy = []
        for i in range(s):
            self.is_cashier_busy.append(False)
        self.total_queue_delay = 0
        self.served = 0
        self.area_qt = 0
        self.last_event_time = 0
        self.k = s
        pass
    def is_all_cashier_busy(self):
        for i in self.is_cashier_busy:
            if not i:
                return False
        return True
class Event:
    def __init__(self,customer,event_type):
        self.customer = customer
        self.event_type = event_type
        pass
    def __lt__(self,event):
        return True #this is dummy comparator
    def process(self,cafe):
        if self.event_type == ARRIVAL:
            if self.customer.group_id not in cafe.disc_group:
                cafe.disc_group[self.customer.group_id] = True #this gruop is marked
                cafe.total_group += 1 #id increment to new group
                next_arrival = cafe.clock + np.random.exponential(cafe.inter_arrival_time,1)[0]
                grp = generate_job_group()
                cafe.area_shop += cafe.total_customer*(cafe.clock-cafe.time_last_customer_change)
                cafe.time_last_customer_change = cafe.clock
                for i in range(grp):
                    type = generate_job_type()
                    customer = Customer(next_arrival,type, cafe.total_group,type)
                    event = Event(customer, ARRIVAL)
                    cafe.schedule_event(next_arrival,event)
                    cafe.total_customer += 1
                    
            if self.customer.station_index == 1:
                if cafe.hot_food.is_server_busy:
                    if len(cafe.hot_food.queue) > 0:
                        cafe.hot_food.area_qt += len(cafe.hot_food.queue)*(cafe.clock-cafe.hot_food.last_event_time)
                        #print("dif = ",cafe.clock-cafe.hot_food.last_event_time, "len = ",len(cafe.hot_food.queue))
                    cafe.hot_food.queue.append((cafe.clock,self.customer))
                    cafe.hot_food.last_event_time = cafe.clock
                
                else:
                    next_depart = cafe.clock + np.random.uniform(cafe.hot_food.ST[0],cafe.hot_food.ST[1],1)[0]
                    cafe.schedule_event(next_depart,Event(self.customer,DEPART))
                    cafe.hot_food.is_server_busy = True
                   
            if self.customer.station_index == 2:
                if cafe.sandwitch.is_server_busy:
                    if len(cafe.sandwitch.queue) > 0:
                        cafe.sandwitch.area_qt += len(cafe.sandwitch.queue)*(cafe.clock-cafe.sandwitch.last_event_time)
                    cafe.sandwitch.queue.append((cafe.clock,self.customer))
                    cafe.sandwitch.last_event_time = cafe.clock
                else:
                    next_depart = cafe.clock + np.random.uniform(cafe.sandwitch.ST[0],cafe.sandwitch.ST[1],1)[0]
                    cafe.schedule_event(next_depart,Event(self.customer,DEPART))
                    cafe.sandwitch.is_server_busy = True
            if self.customer.station_index == 3:
                next_depart = cafe.clock + np.random.uniform(cafe.drint_ST[0],cafe.drint_ST[1],1)[0]
                cafe.schedule_event(next_depart,Event(self.customer, DEPART))
            if self.customer.station_index == 4:
                if cafe.cashier.is_all_cashier_busy():
                    mn = 10**10 #inf
                    index = -1
                    for i in range(cafe.cashier.k):
                        if mn > len(cafe.cashier.queue[i]):
                            mn = len(cafe.cashier.queue[i])
                            index = i
                    cafe.cashier.queue[index].append((cafe.clock,self.customer))
                    if len(cafe.cashier.queue[index]) > 0:
                        cafe.cashier.area_qt += len(cafe.cashier.queue[index])*(cafe.clock-cafe.cashier.last_event_time)
                        cafe.cashier.last_event_time = cafe.clock
                else:
                    for i in range(cafe.cashier.k):
                        if not cafe.cashier.is_cashier_busy[i]:
                            cafe.cashier.is_cashier_busy[i]  = True
                    ac_time = np.random.uniform(5.0,10.0,1)[0]#ac time for drinks
                    if self.customer.type == 1:
                        ac_time += np.random.uniform(20.0,40.0,1)[0]
                    elif self.customer.type == 2:
                        ac_time += np.random.uniform(5.0,15.0,1)[0]
                    cafe.schedule_event(cafe.clock+ac_time,Event(self.customer, DEPART))

        elif self.event_type == DEPART:
            
            if self.customer.station_index == 1:
                cafe.hot_food.served += 1
                self.customer.station_index = 3 #go to drinks after hot food
                cafe.schedule_event(cafe.clock,Event(self.customer,ARRIVAL))
                if len(cafe.hot_food.queue) > 0:
                    q_len = len(cafe.hot_food.queue)
                    t,c = cafe.hot_food.queue.pop(0)
                    cafe.hot_food.area_qt += q_len*(cafe.clock-cafe.hot_food.last_event_time)
                    cafe.hot_food.total_queue_delay += (cafe.clock-t)
                    print(cafe.clock-t," len = ",q_len," age  = ",cafe.clock-c.appeared_at)
                    self.customer.total_queue_delay += (cafe.clock-t)
                    
                    cafe.schedule_event(cafe.hot_food.next_depart(cafe.clock),Event(c,DEPART))
                    cafe.hot_food.last_event_time = cafe.clock
                else:
                    cafe.hot_food.is_server_busy = False
                
            if self.customer.station_index == 2:
                cafe.sandwitch.served +=1
                self.customer.station_index = 3 #go to drink after sandwitch
                cafe.schedule_event(cafe.clock,Event(self.customer,ARRIVAL))
                if len(cafe.sandwitch.queue) > 0:
                    q_len = len(cafe.sandwitch.queue)
                    t, c = cafe.sandwitch.queue.pop(0)
                    cafe.sandwitch.area_qt += q_len*(cafe.clock-cafe.sandwitch.last_event_time)
                    cafe.sandwitch.total_queue_delay += (cafe.clock-t)
                    self.customer.total_queue_delay += (cafe.clock-t)
                    cafe.schedule_event(cafe.sandwitch.next_depart(cafe.clock),Event(c,DEPART))
                    cafe.sandwitch.last_event_time = cafe.clock
                else:
                    cafe.sandwitch.is_server_busy = False
            if self.customer.station_index == 3:
                self.customer.station_index = 4 #go to cahier after drinks
                cafe.schedule_event(cafe.clock,Event(self.customer,ARRIVAL))
            if self.customer.station_index == 4:
                cafe.area_shop += cafe.total_customer*(cafe.clock-cafe.time_last_customer_change)
                cafe.time_last_customer_change = cafe.clock
                cafe.cashier.served += 1
                cafe.total_customer -= 1
                print("#######################customer = ",cafe.total_customer)
                index = -1
                busy_cahier_set = []
                for i in range(cafe.cashier.k):
                    if cafe.cashier.is_cashier_busy[i]:
                        busy_cahier_set.append(i)
                t = np.random.uniform(0,len(busy_cahier_set)-0.1,1)[0]
                index = int(t)
                if(index >= len(busy_cahier_set)):
                    index-=1
                print("index = ",index," set len = ",len(busy_cahier_set))
                if len(busy_cahier_set) > 0 and len(cafe.cashier.queue[busy_cahier_set[index]]) > 0:
                    q_len = len(cafe.cashier.queue[busy_cahier_set[index]])
                    t, c = cafe.cashier.queue[busy_cahier_set[index]].pop(0)
                    cafe.cashier.area_qt += q_len*(cafe.clock-cafe.cashier.last_event_time)
                    cafe.cashier.last_event_time = cafe.clock
                    cafe.cashier.total_queue_delay += (cafe.clock-t)
                    self.customer.total_queue_delay += (cafe.clock-t)
                    
                else:
                    if len(busy_cahier_set) > 0:
                        cafe.cashier.is_cashier_busy[busy_cahier_set[index]] = False
                    else:
                        cafe.cashier.is_cashier_busy[0] = False
                self.customer.customer_total_delay = cafe.clock-self.customer.appeared_at
                print("______________________  = ",cafe.clock,self.customer.appeared_at)
                cafe.served_customer_set.append(self.customer)
                
class Cafeteria:
    def __init__(self,h,s,c,inter_arrival_time):#total number of server at hot food, sandwitch, cashier
        self.hot_food = HotFood(h,(50,120))
        self.sandwitch = Sandwitch(s,(60,180))
        self.cashier = Cashier(c)
        self.drint_ST = [5,20]
        self.clock = 0
        self.inter_arrival_time = inter_arrival_time
        self.eventq = []
        self.total_done_customer = 0
        self.area_shop = 0
        self.total_customer = 0
        self.time_last_customer_change = 0
        self.total_sim_time = 0
        self.disc_group = {} #this is a dictionary
        #this track and prevents excessive arrival 
        self.total_group = 0
        self.served_customer_set = []
        pass
    def schedule_event(self,time,event):
        heapq.heappush(self.eventq,(time,event))
    
    def run(self,total_sim_time):
        self.total_sim_time = total_sim_time
        self.schedule_event(self.total_sim_time, Event(None,EXIT))
        first_arrivaal_time = np.random.exponential(self.inter_arrival_time,1)[0]
        self.time_last_customer_change = first_arrivaal_time
        group = generate_job_group()
        for i in range(group):
            self.total_group = 1 #start with group 1 then will increase furter
            type = generate_job_type()
            customer = Customer(first_arrivaal_time,type, self.total_group,type)
            event = Event(customer,ARRIVAL)
            self.schedule_event(first_arrivaal_time, event)
            self.total_customer += 1
        while len(self.eventq) > 0:
            time, event = heapq.heappop(self.eventq)
            if event.event_type == EXIT:
                break
            self.clock = time
            #print("time = ",time)
            event.process(self)
        pass
def main():
    data = return_row("input2.txt")
    cafe = Cafeteria(int(data[0][0]),int(data[0][1]),int(data[0][2]),30)
    cafe.run(5400)
    print(cafe.total_customer)
    print(cafe.total_group)
    print(cafe.inter_arrival_time)
    print("___________Average Delay in Queue____")
    print("Hot Food: ",cafe.hot_food.total_queue_delay/cafe.hot_food.served)
    print("Sandwitch: ",cafe.sandwitch.total_queue_delay/cafe.sandwitch.served)
 
    print("Cashier: ",cafe.cashier.total_queue_delay/cafe.cashier.served)
   
    
    print("___________Average Queue length___________")
    print("Hot food: ",cafe.hot_food.area_qt/cafe.total_sim_time)
    print("Sandwitch: ",cafe.sandwitch.area_qt/cafe.total_sim_time)
    print("Cashier: ",cafe.cashier.area_qt/(2*cafe.total_sim_time))
    
    print("_______Avg Customer Delay in Queue_________")
    delay1 = []
    delay2 = []
    delay3 = []
    weighted_delay = 0
    for i in cafe.served_customer_set:
        if i.type == 1:
            delay1.append(i.total_queue_delay)
            weighted_delay += 0.8*i.customer_total_delay
        if i.type == 2:
            delay2.append(i.total_queue_delay)
            weighted_delay += 0.15*i.customer_total_delay
        if(i.type==3):
            delay3.append(i.total_queue_delay)
            weighted_delay += 0.05*i.customer_total_delay
    print("Customer type 1:",np.mean(delay1))
    print("Customer type 2: ",np.mean(delay2))
    print("Customer type 3: ",np.mean(delay3))
    print("\nCustomer average weighted delay = ",weighted_delay/cafe.cashier.served)
    
    print("Avg Customer in system = ",cafe.area_shop/cafe.total_sim_time)
if __name__ == "__main__":
    main()
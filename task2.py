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
    def __init__(self,type,appeared_at,station_index):
        self.type = type
        self.appeared_at = appeared_at
        self.customer_total_delay = 0
        self.station_index = station_index
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
class Cashier:
    def __init__(self,s,ST):#numebr of server,queue and service time tuple 
        self.queue = []
        for i in range(s):
            self.queue.append([])
        self.total_queue_delay = 0
        self.served = 0
        self.area_qt = 0
        self.last_event_time = 0
        pass
class Event:
    def __init__(self,customer,event_type):
        self.customer = customer
        self.event_type = event_type
        pass
    def __lt__(self,event):
        return True #this is dummy comparator
    def process(self,cafe):
        if self.event_type == ARRIVAL:
            if self.customer.type == 1:
                if self.customer.station_index == 0:
                    if cafe.hot_food.is_server_busy:
                        cafe.hot_food.queue.append((cafe.clock,self.customer))
                    else:
                        cafe.hot_food.is_server_busy = True
                        self.customer.station_index+=1
                        servcie_time = cafe.clock+np.random.uniform(cafe.hot_food.ST[0],cafe.hot_food.ST[1],1)[0]
                        cafe.schedule_event(servcie_time,Event(self.customer,DEPART))
                if self.customer.station_index == 1:
                    if cafe.sandwitch.is_server_busy:
                        cafe.sandwitch.queue.append((cafe.clock,self.customer))
                    else:
                        cafe.sandwitch.is_server_busy = True
                        self.customer.station_index+=1
                        servcie_time = cafe.clock+np.random.uniform(cafe.sandwitch.ST[0],cafe.sandwitch.ST[1],1)[0]
                        cafe.schedule_event(servcie_time,Event(self.customer,DEPART))
                if self.customer.station_index == 2
        elif self.event_type == DEPART:
            print ("this is depart")
        pass
class Cafeteria:
    def __init__(self,h,s,c,inter_arrival_time):#total number of server at hot food, sandwitch, cashier
        self.hot_food = HotFood(h,(50,120))
        self.sandwitch = Sandwitch(s,(60,180))
        self.clock = 0
        self.inter_arrival_time = inter_arrival_time
        self.eventq = []
        self.total_done_customer = 0
        self.done_customer_set = 0
        self.area_shop = 0
        self.total_customer = 0
        self.time_last_customer_change = 0
        self.total_sim_time = 0
        self.customer_count = 0
        pass
    def schedule_event(self,time,event):
        heapq.heappush(self.eventq,(time,event))
    def recurrent_incomming(self,offset):
        arrival_time = offset+np.random.exponential(self.inter_arrival_time,1)[0]
        if offset > self.total_sim_time:
            return
        group = generate_job_group()
        for i in range(group):
            type = generate_job_type()
            customer = Customer(type,arrival_time,0)
            event = Event(customer,ARRIVAL)
            self.schedule_event(arrival_time,event)
        offset = arrival_time
        self.recurrent_incomming(offset)
    def run(self,total_sim_time):
        self.total_sim_time = total_sim_time 
        self.schedule_event(self.total_sim_time,Event(None,EXIT))
        self.recurrent_incomming(0.0)
        while len(self.eventq) > 0:
            time, event = heapq.heappop(self.eventq)
            if event.event_type == EXIT:
                break
            self.clock = time
            print("time = ",time)
            event.process(self)
        pass
def main():
    data = return_row("input2.txt")
    cafe = Cafeteria(int(data[0][0]),int(data[0][1]),int(data[0][2]),30)
    cafe.run(5400)
    print(cafe.customer_count)
if __name__ == "__main__":
    main()
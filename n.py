import numpy as np
import csv
import heapq
ARRIVAL, DEPART, EXIT = 1, 2, 3
cumulative_probabilites = []
rout = []
service_time_set = []
def return_row(file):
    f = open(file,'r')
    usable = csv.reader(f)
    arr = []
    for j in usable:
        for k in j:
            a = list(map(float,k.split()))
            arr.append(a)
    return arr
def generate_job():##return the type of new job
    uniform = np.random.uniform(0.0,1.0,1)[0]
    i = 0
    for prob in cumulative_probabilites:
        if prob >=uniform:
            return i+1
        i = i + 1
    print("Ivalid Job type, return -1")
    return -1
class Event:
    def __init__(self,job,event_type):
        self.job = job
        self.event_type = event_type #arrival or depart
    def process(self, shop):
        if self.event_type == ARRIVAL:
            #first schedule new arrival if it is new incomming job to shop
            if self.job.current_rout_index == -1:
                next_arrival_time = shop.clock + np.random.exponential(shop.job_inter_arrival_time,1)[0]
                type = generate_job()
                next_job = Job(type,rout[type-1],service_time_set[type-1],next_arrival_time)
                event = Event(next_job,ARRIVAL)
                shop.schedule_event(next_arrival_time,event)
            #next complete the current arrival tasks
            self.job.current_rout_index+=1 #go to next station
            station_index = self.job.rout[self.job.current_rout_index]
            if shop.station_set[station_index].total_idle_machine ==0:
                #should insert a tuple of inserting time,event in the queue
                shop.station_set[station_index].queue.push((shop.clock,self.job))
            pass
        if self.event_type == DEPART:
            print("this is depart")
class Job:
    def __init__(self, type,rt,service_time_set,appeared_at):
        self.type = type
        self.service_time_set = []
        for i in service_time_set:
            self.service_time_set.append(i)
        self.rout = []
        for i in rt:
            self.rout.append(i)
        self.current_rout_index = -1 #currently outside of the rout (station)
        self.job_delay_in_queue = 0
        self.jod_total_delay = 0
        self.appeared_at = appeared_at

class Station:
    def __init__(self, k):
        self.queue = [] #queue of the jobs, it will contain job objects having all the info of each job
        self.total_machine = k
        self.total_idle_machine = k
        self.total_queue_delay = 0
        self.served = 0
        self.area_qt = 0
    def print_station(self):
        print("queue = ",self.queue)
        print("total machine = ",self.total_machine)
        print("total idle machine = ",self.total_idle_machine)
        print("total queue delay = ",self.total_queue_delay)
        print("total served = ",self.served)
        print("area qt = ",self.area_qt)

class Shop():
    def __init__(self,total_station, number_of_machine_set, job_inter_arrival_time):
        self.evnetq = [] #this is a priority queue aka heap
        self.total_done_jobs = 0
        self.total_station = total_station
        self.clock = 0
        self.number_of_machine_set = number_of_machine_set
        self.job_inter_arrival_time = job_inter_arrival_time
        self.station_set = []
        for i in number_of_machine_set:
            self.station_set.append(Station(i))
    def print_station_set(self):
        for i in range(self.total_station):
            print("station no ",i+1)
            self.station_set[i].print_station()
    def schedule_event(self,time,event):
        heapq.heappush(self.evnetq,(time,event))
        pass
    def run(self, total_sim_time):
        #first schedule when this shop will close
        self.schedule_event(total_sim_time,Event(None,EXIT))
        #then schedule the first arrival event that will make arrival recurrently
        first_arrival_time = np.random.exponential(self.job_inter_arrival_time,1)[0]
        type = generate_job()
        first_job = Job(type,rout[type-1],service_time_set[type-1],first_arrival_time)
        event = Event(first_job,ARRIVAL)
        self.schedule_event(first_arrival_time,event)
        while len(self.evnetq) > 0:
            time, event = heapq.heappop(self.evnetq)
            print("time = ",time)
            if event.event_type == EXIT:
                break
            self.clock = time #clock time is the time of current event
            event.process(self)
        pass
def main():
    data = return_row("input.txt")
    total_station = int(data[0][0])
    number_of_machine_set = []
    for i in data[1]:
        number_of_machine_set.append(int(i))
    print(total_station)
    print(number_of_machine_set)
    job_inter_arrival_time = data[2][0]
    print(job_inter_arrival_time)
    total_job_type = int(data[3][0])
    print(total_job_type)
    job_probabilities = data[4]
    print(job_probabilities)
    number_of_station_of_job = []
    for i in data[5]:
        number_of_station_of_job.append(int(i))
    print(number_of_station_of_job)
    for i in range(total_job_type):
        t_rout = [] #data contains double value only, to make them int we create temporary t_rout
        for j in data[6+2*i]:
            t_rout.append(int(j))
        rout.append(t_rout)
        service_time_set.append(data[6+2*i+1])
    print(rout)
    print("now see the times")
    print(service_time_set)
    cumulative_probabilites.append(job_probabilities[0])
    for i in range(1,len(job_probabilities)):
        cumulative_probabilites.append(cumulative_probabilites[-1]+job_probabilities[i])
    i = 0
    shop = Shop(total_station,number_of_machine_set,job_inter_arrival_time)
    #shop.print_station_set()
    shop.run(8)
if __name__ == "__main__":
    main()
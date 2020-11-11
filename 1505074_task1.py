import numpy as np
import csv
import heapq
ARRIVAL, DEPART, EXIT = 1, 2, 3
cumulative_probabilites = []
rout = []
service_time_set = []
total_job_type = 0
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
            #print("this is arrival")
            #first schedule new arrival if it is new incomming job to shop
            if self.job.current_rout_index == -1:
                next_arrival_time = shop.clock + np.random.exponential(shop.job_inter_arrival_time,1)[0]
                type = generate_job()
                next_job = Job(type,rout[type-1],service_time_set[type-1],next_arrival_time)
                event = Event(next_job,ARRIVAL)
                shop.schedule_event(next_arrival_time,event)
                shop.area_shop+=(shop.total_customer)*(shop.clock-shop.time_last_cust_chng)
                shop.time_last_cust_chng = shop.clock
                shop.total_customer+=1

            #next complete the current arrival tasks
            self.job.current_rout_index+=1 #go to next station
            station_index = self.job.rout[self.job.current_rout_index]-1 #for zero indexing
            if shop.station_set[station_index].total_idle_machine ==0:
                #should insert a tuple of inserting time,event in the queue
                shop.station_set[station_index].area_qt+=(len(shop.station_set[station_index].queue)*(shop.clock-shop.station_set[station_index].last_event_time))
                shop.station_set[station_index].queue.append((shop.clock,self.job))
                shop.station_set[station_index].last_event_time = shop.clock
            else:
                shop.station_set[station_index].total_idle_machine-=1
                service_mean = self.job.service_time_set[self.job.current_rout_index]
                service_time = np.random.exponential(service_mean/2.0,2).sum()
                depart_at = shop.clock + service_time
                shop.schedule_event(depart_at,Event(self.job,DEPART))
            pass
        if self.event_type == DEPART:
            #print("this is depart")
            #first we decide what to do whith this departed job
            station_index = self.job.rout[self.job.current_rout_index]-1
            shop.station_set[station_index].served+=1
            if self.job.current_rout_index+1 >= len(self.job.rout):
                #this means completeness of a job
                shop.total_done_jobs+=1
                self.job.job_total_delay+=(shop.clock-self.job.appeared_at)
                shop.done_job_set.append(self.job)

                shop.area_shop+=(shop.total_customer)*(shop.clock-shop.time_last_cust_chng)
                shop.time_last_cust_chng = shop.clock
                shop.total_customer-=1
            else:
                #pass
                shop.schedule_event(shop.clock,Event(self.job,ARRIVAL))
            if len(shop.station_set[station_index].queue) > 0:
                q_len = len(shop.station_set[station_index].queue)
                time, job = shop.station_set[station_index].queue.pop(0)
                shop.station_set[station_index].last_event_time = shop.clock
                job.job_delay_in_queue+=shop.clock-time
                service_mean = self.job.service_time_set[self.job.current_rout_index]
                service_time = np.random.exponential(service_mean/2.0,2).sum()
                shop.schedule_event(shop.clock+service_time,Event(job,DEPART))
                q_delay = shop.clock-time
                self.job.job_delay_in_queue+=q_delay
                shop.station_set[station_index].total_queue_delay+=q_delay
                shop.station_set[station_index].area_qt+=(q_len*q_delay)
            else:
                shop.station_set[station_index].total_idle_machine+=1
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
        self.job_total_delay = 0
        self.appeared_at = appeared_at

class Station:
    def __init__(self, k):
        self.queue = [] #queue of the jobs, it will contain job objects having all the info of each job
        self.total_machine = k
        self.total_idle_machine = k
        self.total_queue_delay = 0
        self.served = 0
        self.area_qt = 0
        self.last_event_time = 0
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
        self.done_job_set = []
        self.total_sim_time = 0
        self.area_shop = 0
        self.total_customer = 0
        self.time_last_cust_chng = 0
    def print_station_set(self):
        for i in range(self.total_station):
            print("station no ",i+1)
            self.station_set[i].print_station()
    def schedule_event(self,time,event):
        heapq.heappush(self.evnetq,(time,event))
        pass
    def run(self, total_sim_time):
        self.total_sim_time = total_sim_time
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
            #print("time = ",time)
            if event.event_type == EXIT:
                for i in range(len(self.station_set)):
                    #print(i.last_event_time)
                    #self.station_set[i].area_qt+=(self.total_sim_time-self.station_set[i].last_event_time)*len(self.station_set[i].queue)
                    pass
                break
            self.clock = time #clock time is the time of current event
            event.process(self)
        pass
    def finish(self):
        pass
    def print_result(self):
        for i in self.done_job_set:
            print("queue delay = ",i.job_delay_in_queue)
            print("total delay = ",i.job_total_delay)
        for i in self.station_set:
            print(i.total_queue_delay/i.served)
        pass
    def get_job_queue_delay(self,total_job_type):
        freq  = []
        sum_time = []
        for i in range(total_job_type):
            freq.append(0)
            sum_time.append(0.0)
        for i in self.done_job_set:
            freq[i.type-1]+=1
            sum_time[i.type-1]+=i.job_delay_in_queue
        return freq,sum_time
    def get_job_total_delay(self,total_job_type):
        freq  = []
        sum_time = []
        for i in range(total_job_type):
            freq.append(0)
            sum_time.append(0.0)
        for i in self.done_job_set:
            freq[i.type-1]+=1
            sum_time[i.type-1]+=i.job_total_delay
        return freq,sum_time
    def get_station_average_q_len(self):
        queue_len = []
        for i in self.station_set:
            queue_len.append(i.area_qt/self.total_sim_time)
        return queue_len
    def get_station_average_q_delay(self):
        queue_delay = []
        for i in self.station_set:
            queue_delay.append(i.total_queue_delay/i.served)
        return queue_delay
def main():
    f = open("output1.txt",'w')
    data = return_row("input1.txt")
    total_station = int(data[0][0])
    number_of_machine_set = []
    for i in data[1]:
        number_of_machine_set.append(int(i))
    #print(total_station)
    #print(number_of_machine_set)
    job_inter_arrival_time = data[2][0]
    #print(job_inter_arrival_time)
    total_job_type = int(data[3][0])
    #print(total_job_type)
    job_probabilities = data[4]
    #print(job_probabilities)
    number_of_station_of_job = []
    for i in data[5]:
        number_of_station_of_job.append(int(i))
    #print(number_of_station_of_job)
    for i in range(total_job_type):
        t_rout = [] #data contains double value only, to make them int we create temporary t_rout
        for j in data[6+2*i]:
            t_rout.append(int(j))
        rout.append(t_rout)
        service_time_set.append(data[6+2*i+1])
    #print(rout)
    #print("now see the times")
    #print(service_time_set)
    cumulative_probabilites.append(job_probabilities[0])
    for i in range(1,len(job_probabilities)):
        cumulative_probabilites.append(cumulative_probabilites[-1]+job_probabilities[i])
    i = 0
    shop = Shop(total_station,number_of_machine_set,job_inter_arrival_time)
    #shop.print_station_set()
    shop.run(8)
    #shop.print_result()
    #print(shop.total_done_jobs)
    #print(shop.get_job_queue_delay(total_job_type))
    #print(shop.get_job_total_delay(total_job_type))
    #print(shop.get_station_average_q_len())
    #print(shop.get_station_average_q_delay())
    job_queue_delay = []
    job_freq = []
    job_total_delay = []
    q_len = []
    total_q_delay_at_station = []
    for i in range(total_station):
        q_len.append(0.0)
        total_q_delay_at_station.append(0)
    for i in range(total_job_type):
        job_queue_delay.append(0.0)
        job_freq.append(0)
        job_total_delay.append(0.0)
    total_done_job = 0
    total_cust_in_system = 0
    for _ in range(30):
        shop = Shop(total_station,number_of_machine_set,job_inter_arrival_time)
        shop.run(8)
        freq,q_delay = shop.get_job_queue_delay(total_job_type)
        job_queue_delay = np.add(job_queue_delay,q_delay)
        job_freq = np.add(job_freq,freq)
        freq,t_delay = shop.get_job_total_delay(total_job_type)
        job_total_delay = np.add(job_total_delay,t_delay)

        q_len = np.add(q_len,shop.get_station_average_q_len())
        total_done_job+=shop.total_done_jobs
        total_q_delay_at_station = np.add(total_q_delay_at_station,shop.get_station_average_q_delay())
        
        total_cust_in_system+=(shop.area_shop/8.0)
    f.write("Queueing delay of each job: ")
    for i in range(total_job_type):
        f.write("\njob type "+str(i+1)+" average total queue delay = "+str(job_queue_delay[i]/job_freq[i])+" total delay = "+str(job_total_delay[i]/job_freq[i]))
    f.write("\n\nAverage queue length of each station")
    for i in range(len(q_len)):
        f.write("\nstation no "+str(i+1)+" average number in queue = "+str(q_len[i]/30.0))
    
    f.write("\n\nAverage job in whole system at a moment = "+str(total_cust_in_system/30.0))
    f.write("\n\nAverage total done job of system per day = "+str(total_done_job/30.0))

    f.write("\n\nAverage queue delay at stations: ")
    for i in range(len(total_q_delay_at_station)):
        f.write("\nstation no "+str(i+1)+" average queue delay = "+str(total_q_delay_at_station[i]/30.0))
    mx = -10**10
    mx_index = -1
    for i in range(len(total_q_delay_at_station)):
        if mx < total_q_delay_at_station[i]:
            mx = total_q_delay_at_station[i]
            mx_index = i

    f.write("\n\nDecision Choice = ")
    f.write("\nAs the average queue delay is greatest in station "+str(mx_index+1))
    f.write("\nSo, new machine should be set at station "+str(mx_index+1))
    f.write("\nThis choice is made on the basis of 'Limiting Theory' which reveals the bottle-neck criteria") 
    f.close()
if __name__ == "__main__":
    main()
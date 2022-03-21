import altair as alt
import datetime as dt
import pandas as pd

alt.renderers.enable('altair_viewer')

task = { (50,12) : 'T1', (40,10) : 'T2', (30,10) : 'T3' }

algorithm = 0 # Let's change this to user input through UI to select the algorithm 0 -> EDF ; 1 -> RM

if(algorithm == 0):
        
    def schEDF(tsk):
        s = 0
        for key in tsk:
            s = s + int(key[1]) / int(key[0])

        print(round(s,3))
        print()

        if(s <= 1):
            schedulability = True
        else:
            schedulability = False

        return schedulability, s

    schedulability, s = schEDF(task)


    if(schedulability):
        result=[] # A list to store the final result of algorithm
        queue = [] # A list to store the Tasks

        p = 120 # Time T until which the tasks are to be scheduled

        # Adding the tasks from dictonary into the list "queue"
        for v in task.values():
            queue.append(v)

        tasks = [] # A list to store all the deadlines of tasks from time T = 0 to T = p
        deadline = [] # A list to store the execution times of individual tasks

        # Adding the execution times of individual tasks into the list "deadline"
        for key in task:
            deadline.append( int(key[0]) )

        dead_max = max(deadline)# finding the maximum execution time of the given tasks

        # Calculating all the deadlines from time T = 0 to T = p (including the immediate deadlines after time p)
        for i in range(0,len(task)):
            for j in range(1,p+dead_max):
                a = []
                if(j % deadline[i] == 0):
                    a.append(j)
                    a.append(queue[i])
                    tasks.append(a)

        tasks = sorted(tasks) # Sorting based on the deadlines

        release = [] # A list to store all the release times of tasks from time T = 0 to T = p

        # Manually adding the time T = 0
        for v in task.values():
            temp = []
            temp.append(0)
            temp.append(v)
            release.append(temp)

        # Calculating all the release times from time T = 0 to T = p
        for i in range(0,len(task)):
            for j in range(1,p+1):
                if(j % deadline[i] == 0):
                    temp = []
                    temp.append(j)
                    temp.append(queue[i])
                    release.append(temp)

        release = sorted(release) # Sorting based on the release times

        current_time = 0 # A varialble to keep track of current time

        pending = [] # A list to store all the tasks released at a given time (current time)

        change_status = False #Variables to keep track if the task execution has changed from one to another 
        change_task = 'Tx'

        while(current_time <= p): # Checking the condition if our current time is less than the ending time p
            # Calculating the tasks released at a given time (current time)
            for i in release:
                if(i[0] == current_time):
                    temp = []
                    temp.append(list(task.keys())[list(task.values()).index(i[1])][1])
                    temp.append(i[1])
                    pending.append(temp)

            # Checking if more than one task is ready to run; 
            if(len(pending)>1):

                # If the execution has changed from one task to another, We are storing the current time and the Task which was being executed till now in the list "result"
                if(change_status):
                    r=[]
                    r.append(change_task)
                    r.append(current_time)
                    result.append(r)
                    change_status = False

                c_task  = tasks[0][1] #As we have more than one task ready to run, We have to check which task has the earliest deadline by using the list "tasks"

                # Choosing the task which has earliest deadline to run and adding that to the list "result"
                for x in pending:
                    if(x[1] == c_task):
                        r=[]
                        r.append(c_task)
                        r.append(current_time)
                        result.append(r)

                        x[0] = x[0] - 1 #reducing the execution time of the task by 1
                        current_time = current_time+1 #increasing the current time by 1

                        # If the task's execution time has become 0 (i.e., it has executed fully we are storing it to the list "result"
                        if(x[0] == 0):
                            r=[]
                            r.append(c_task)
                            r.append(current_time)
                            result.append(r)

                            pending.remove(x) # Removing the task from pending list, as it's execution is complete
                            tasks.pop(0) # Removing the task from deadlines list "tasks", as it's execution is complete

                        break

            # If there is only one pending task, We have no option but to run the task
            elif (len(pending)==1):

                c_task  = pending[0][1]

                r=[]
                r.append(c_task)
                r.append(current_time)
                result.append(r)

                pending[0][0] = pending[0][0] - 1 #reducing the execution time of the task by 1
                current_time = current_time+1 #increasing the current time by 1

                # If the task's execution time has become 0 (i.e., it has executed fully we are storing it to the list "result"
                if(pending[0][0] == 0):
                    r=[]
                    r.append(pending[0][1])
                    r.append(current_time)
                    result.append(r)

                    pending.pop(0) # Removing the task from pending list, as it's execution is complete
                    tasks.pop(0) # Removing the task from deadlines list "tasks", as it's execution is complete

                change_status = True
                change_task = c_task

            # If there is no pending task, We are just incrementing the current time
            elif (len(pending)==0):
                current_time = current_time+1
                change_status = False

        result_copy = result # We have our results 


        error = False
        e = -1

        # We are going through results and prepare a final list of tasks with the execution start time and end time
        if(result[len(result)-1][0] == result[len(result)-2][0]):
            error = True
            e = result[len(result)-1][1]

        final_result = []
        x = 0
        s = True
        counter = 0
        while(x < len(result)-1):
            if(s):
                final_result.append(result[x])
                s = False
            if(result[x][0] == result[x+1][0]):
                x = x+1
            else:
                final_result[counter].append(result[x][1])
                counter = counter + 1
                s = True
                x = x+1
        if(error):
            if(len(final_result[len(final_result)-1])<3):
                if(error):
                    final_result[len(final_result)-1].append(e)

        # We have our Final results 
        for q in final_result:
            print(q)

        #Using altair to plot a chart
        data1 = []
        data2 = []
        data3 = []
        for q in final_result:
            data1.append(q[1])
            data2.append(q[2])
            data3.append(q[0])

        data = pd.DataFrame()
        data['Time'] = data1
        data[' '] = data2
        data['Tasks'] = data3

        chart = alt.Chart(data).mark_bar().encode(
            x='Time',
            x2=' ',
            y='Tasks',
            color=alt.Color('Tasks', scale=alt.Scale(scheme='dark2'))
        ).properties(
            width=2160,
            height=80
        )

        chart.show()

    else:
        print("Not Schedulable")
else:
    # RM algorithm
    

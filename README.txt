In This project I created a process simulator for 4 schedulers: FCFS, SJF, HRRN and RR.
The script is getting 4 agruments:
arg[1]= the type of scheduler (FCFS=1, SJF=2, HRRN=3 and RR=4)
arg[2]= lambda that will be used to compute the processes' arrival time 
arg[3]= service time for the processes
arg[4]= quantum time for Round Robin scheduler

To compile the code:

the code is in python 3, therefore, the bash script should be:

rm sim.txt
for ((i = 10; i < 31; i++)); do
python3 Project1OS.py 4 $i 0.04 0.01
done

get rid of the command: rm sim.txt if you wish to have everything under one file instead of each 
run creating a new sim.txt file.

the program is creating a txt file to the current directory.

About the program:
the program creates instances for every process, event and also creates a CPU instance for keeping track on whether it is busy/free
there are functions for each scheduler, according to the argument passed in.
the main function takes the arguments and pass them to the simulator function with the right arguments, which then
are used with the scheduler function accordinly.






#functions
    
def time():
    global g
    global j
    g=int(g)
    j=int(j)
    a=g*60+j
    g=a//60
    j=a%60
    if len(str(g))==1:
        g='0'+str(g)
    if len(str(j))==1:
        j='0'+str(j)
    return(g,j)

def roundtime():
    global j
    global g
    j=int(j)
    if j<30 and j!=0:
        a= 30-j
        j+=a
    elif j>30 and j<60:
        a=60-j
        j+=a
    time()
    return(g,j)

def create():
        global g
        global j
        global cur
        z=0
        a='Incomplete'
        x=input('\nEnter Day Name: ')
        cur.execute("Create table %s(S_No INT, Slot_Duration CHAR(11), Task_Name VARCHAR(20), Status CHAR(10))"%(x,))
        y=0
        g, j=datetime.datetime.now().strftime('%H'), datetime.datetime.now().strftime('%M')
        print('\nStarting Time:\n1. Current Time \t2. Customize Time (24 hr format)')
        i=int(input('Enter Choice Number- '))
        if i==1:
            roundtime()
        elif i==2:
            g, j=input('Enter Hour- '), input('Enter Minutes- ')
        dict={}
        b=int(input('\nEnter Number of Slots: '))
        print('\nDuration of Slots: \n1. Same \t2. Different')
        k=int(input('Enter Choice Number- '))
        if k==1:
            c=int(input('Enter Duration of Slots (in mins)- '))
        print('\n', end='')
        for d in range(0,b):
            z+=1
            if k==2:
                c=int(input('Enter Duration of Slot (in mins): '))
            time()
            l=str(g)+':'+str(j)
            j=int(j)+c
            time()
            if int(g)*60+int(j)>1440:
                print('The time has exceeded 23:59. Create another Schedule for the next day.')
                break
            elif int(g)==24 and int(j)==0:
                g, j =23, 59
                y+=1
                if y>1:
                    print('The time has exceeded 23:59. Create another Schedule for the next day.')
                    break
            e=input('Enter Task Name: ')
            f=str(g)+':'+str(j)
            h=str(l)+'-'+str(f)
            cur.execute("Insert into %s(S_No, Slot_Duration, Task_Name, Status) values(%s, '%s', '%s', '%s')"%(x,z,h,e,a))
            sql.commit()
        return()

def modify():
        global cur
        h=input('\nEnter Name of Day to be Modified: ')
        z=h
        try:
            cur.execute('Describe %s'% (h,))
        except pymysql.err.ProgrammingError:
            print('Schedule for', h, 'does not exist. Create one first.')
            h=0
        if h!=0:
            print('\nModify:\n1. Task Name\t2. Duration of Slot')
            a=input('Enter Choice Number- ')
            if a=='1':
                b=input('\nEnter Old Name of Task to be Modified- ')
                c=input('Enter New Task Name- ')
                cur.execute("Select S_No from %s where task_name='%s'"%(z,b))
                d=str(cur.fetchone()[0])
                cur.execute("Update %s set Task_Name='%s' where S_No='%s'"%(z,c,d))
                print('Task Name has been modified.')
            elif a=='2':
                b=input('\nEnter Name of Task to be Modified- ')
                c=input('Enter New Slot Duration- ')
                cur.execute("Select S_No from %s where task_name='%s'"%(z,b))
                d=str(cur.fetchone()[0])
                cur.execute("Update %s set Slot_Duration='%s' where S_No=%s"%(z,c,d))
                print('Slot Duration has been modified.')
            sql.commit()
        return()

def add():
        global cur
        b=input('\nEnter Name of Day to be Edited: ')
        h=b
        try:
            cur.execute('Describe %s'% (h,))
        except pymysql.err.ProgrammingError:
            print('Schedule for', h, 'does not exist. Create one first.')
            h=0
        if h!=0:
            c=input('Enter Duration of New Slot- ')
            d=input('Enter Task Name of New Slot- ')
            cur.execute("Select count(*) from %s"%(b,))
            q=int(cur.fetchone()[0])+1
            cur.execute("Insert into %s values('%s', '%s', '%s', 'Incomplete')"%(b,q,c,d))
            print('Task has been added.')
        sql.commit()
        return()

def delete():
    global cur
    print('\nDelete: \n1. Complete Schedule \t2. Specific Day \t3. Specific Task')
    b=input('Enter Choice Number- ')
    if b=='1':
        cur.execute('Drop database Schedule_Manager')
        print('\nThe complete schedule has been deleted.')
        h=0
    elif b=='2': 
        h=input('\nEnter Name of Day to be Deleted: ')
        c=h
    elif b=='3':
        h=input('\nEnter Name of Day to be Edited: ')
        c=h
    if b!='1':
        try:
            cur.execute('Describe %s'% (c,))
        except pymysql.err.ProgrammingError:
            print('Schedule for', c, 'does not exist. Create one first.')
            h=0
    if h!=0 and b=='2':
        cur.execute("Drop table %s"%(c,))
        print('The schedule for',c,'has been deleted.')
    elif h!=0 and b=='3':
        d=input('Enter Name of Task to be Deleted- ')
        cur.execute("Delete from %s where Task_Name='%s'"%(c,d))
        print('The task with name',d,'has been deleted.')
    sql.commit()
    return()
    
def search():
    global cur
    h=input('\nEnter Name of Day to be Searched: ')
    c=h
    try:
        cur.execute('Describe %s'% (c,))
    except pymysql.err.ProgrammingError:
        print('Schedule for', c, 'does not exist. Create one first.')
        h=0
    if h!=0:
        print('\nSearch by: 1. Task Name \t2. Slot Duration')
        h=input('Enter Choice Number: ')
        if h=='1':
            a=input('\nEnter Task Name to be Searched: ')
            cur.execute("Select * from %s where Task_Name='%s'"%(c,a))
        elif h=='2':
            a=input('\nEnter Slot Duration to be Searched: ')
            cur.execute("Select * from %s where Slot_Duration='%s'"%(c,a))
        o=cur.fetchone()
        print ('\n{:<21} {:<21} {:<50}'. format('Duration', 'Task', 'Status'))
        print ('{:<21} {:<21} {:<50}'. format(o[1], o[2], o[3]))
    return()

def display():
    global cur
    h=input('\nEnter Name of Day to be Displayed: ')
    c=h
    try:
        cur.execute('Describe %s'% (c,))
    except pymysql.err.ProgrammingError:
        print('Schedule for', c, 'does not exist. Create one first.')
        h=0
    if h!=0:
        cur.execute('Select * from %s'%(c,))
        o=cur.fetchall()
        print ('{:<15} {:<21} {:<21} {:<50}'. format('S.No.','Duration', 'Task', 'Status'))
        j=0
        for i in o:
            j+=1
            print ('{:<15} {:<21} {:<21} {:<50}'. format(j, i[1], i[2], i[3]))
    return()
    
def mark_completed():
    global cur
    b=input('\nEnter Name of Day to be Edited-')
    h=b
    try:
        cur.execute('Describe %s'% (h,))
    except pymysql.err.ProgrammingError:
        print('Schedule for', h, 'does not exist. Create one first.')
        h=0
    if h!=0:
        c=input('\nEnter Name of Task to be Marked as Complete-')
        cur.execute("Select S_No from %s where Task_Name='%s'"%(b,c))
        d=str(cur.fetchone()[0])
        cur.execute("Update %s set Status='Complete' where S_No=%s"%(b,d))
    sql.commit()
    return()

def progress():
    global cur
    b=input('\nEnter Name of Day to Calculate Progress-')
    h=b
    try:
        cur.execute('Describe %s'% (h,))
    except pymysql.err.ProgrammingError:
        print('Schedule for', h, 'does not exist. Create one first.')
        h=0
    if h!=0:
        cur.execute("Select count(*) from %s where Status='Complete'"%(b,))
        p=int(cur.fetchone()[0])
        cur.execute("Select count(*) from %s where Status='Incomplete'"%(b,))
        q=int(cur.fetchone()[0])
    print('\nNumber of Tasks Completed = ', p)
    print('Number of Incomplete Tasks = ', q)
    g=p+q
    s=(p/g)*100
    print('Percentage of Work Done =', s)
    if s==0:
        print('\nNo tasks were completed today. Try harder next time!')
    elif s>0 and s<50:
        print('\nGood effort! Be more consistent.')
    elif s==50:
        print('\nKeep going, success is near!')
    elif s>50 and s<75:
        print('\nAlmost there!')
    elif s==75 or (s>75 and s<100):
        print('\nExcellent achievement!')
    elif s==100:
        print('\nAll tasks were completed. GOAL REACHED!')
    return()


#main

print('\n\tWELCOME TO SCHEDULE MANAGER')
flag=True
import datetime
import pymysql
sql=pymysql.connect(host='localhost', user='root', password='mysql')
cur=sql.cursor()
try:
    cur.execute('Create database Schedule_Manager')
except pymysql.err.ProgrammingError:
    empty=0
cur.execute('Use Schedule_Manager')
sql.commit()
while flag==True:
          print('\n\t\t[Main Menu]')
          print('\n\n1. Create\t\t2. Modify\n3. Add\t\t\t4. Delete \n5. Search \t\t6. Display  \n7. Mark as Completed \t8. Check Progress \n9. Exit')
          a=input('\nEnter Choice Number: ')
          if a=='1':
              create()
          elif a=='2':
              modify()
          elif a=='3':
              add()
          elif a=='4':
              delete()
          elif a=='5':
              search()
          elif a=='6':
              display()
          elif a=='7':
              mark_completed() 
          elif a=='8':
              progress()
          else:
            print('\nExit!')
            flag=False

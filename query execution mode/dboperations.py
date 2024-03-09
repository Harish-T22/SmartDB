import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="pass")
mycursor=mydb.cursor()

def enableautocommit():
    global mycursor
    mycursor.execute("set autocommit=1")
    
def disableautocommit():
    global mycursor
    mycursor.execute("set autocommit=0")

def alldbs():
    global mycursor
    mycursor.execute("show databases")
    listdb=[]
    for i in mycursor:
        listdb.append(i[0])
    return listdb

def alltb():
    global mycursor
    mycursor.execute("show tables")
    listtb=[]
    for i in mycursor:
        listtb.append(i[0])
    return listtb

def createdb(dbname):
    global mycursor
    mycursor.execute("create database "+dbname)

def usedb(dbname):
    global mycursor
    mycursor.execute("use "+dbname)

def dropdb(dbname):
    global mycursor
    mycursor.execute("drop database "+dbname)
    
def connect_db(dbname):
    global mydb
    global mycursor
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="pass",database=dbname)
    mycursor=mydb.cursor()

def createtb(tbname):
    global mycursor
    query="create table "+tbname+" ("
    nxtfield="yes"
    primary=0
    while(nxtfield=="yes"):
        print("Enter the field details")
        fname=input("Enter the Field name:")
        ftype=input("Enter the Field type:")
        fsize=int(input("Enter the Field size:"))
        key=input("Do you want to set any key(constraint) to this Field?:").lower()
        if (key=="yes"):
           keyval=input("Enter the Constraint:")
           
        null=input("Do you want to allow NULL values in this Field?(yes or no):").lower()
        
        default=input("Do you want to set any default value to this Field?:").lower()
          
        if(default=="yes"):
           defaultval=input("Enter the default value:")
        elif (ftype=="int" or ftype=="integer" and key !=""):
           autoinc=input("Do you want to set autoincrement to this Field?:")
            
        query+=fname+" "+ftype+" ("+str(fsize)+")"
        if (key=="yes"):
            query+=" "+keyval+" "
            key=""
        if (null=="no"):
            query+=" not null "
            nul=""
        if (default=="yes"):
            query+=" default "+defaultval+" "
            default=""
        if (autoinc=="yes"):
            query+=" auto_increment "
            autoinc=""
            
        
        nxtfield=input("Do you want to add another field?")
        if(nxtfield=="yes"):
            query+=","
    query+=")"
    print(query)
    mycursor.execute(query)
    print("Table has been Created successfully")
    mycursor.execute("desc "+tbname)
    for i in mycursor:
        print(i)

def altertb(tbname):
    global mycursor
    nxtfield="yes"
    query="alter table "+tbname+" "
    option=input("What do you want to do with ",tbname) 
    if("add" in option and "colum" in option):
        query+="add column ("
        while(nxtfield=="yes"):
            print("Enter the field details")
            fname=input("Enter the Field name:")
            ftype=input("Enter the Field type:")
            fsize=int(input("Enter the Field size:"))
            query+=fname+" "+ftype+" ("+str(fsize)+")"
            nxtfield=input("Do you want to add another field?")
            if(nxtfield=="yes"):
                   query+=","
        query+=")"
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)

 
    elif(("drop" in option or "delete" in option) and "colum" in option):
        query+="drop column "
        while(nxtfield=="yes"):
            fname=input("Enter the Field name to drop:")
            query+=fname
            nxtfield=input("Do you want to add another field?")
            if(nxtfield=="yes"):
                query+=",drop column "
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)

              
    elif(("modify" in option or "change" in option)and "colum" in option):
        query+="modify "
        while(nxtfield=="yes"):
            fname=input("Enter the Field name to modify:")
            ftype=input("Enter the Field type:")
            fsize=int(input("Enter the Field size:"))
            query+=fname+" "+ftype+" ("+str(fsize)+")"
            nxtfield=input("Do you want to modify another field?")
            if(nxtfield=="yes"):
                 query+=",modify "
        mycursor.execute(query)
        print("Table has been Modified successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)
              
    elif(("rename" in option and "colum" in option) or ("change name" in option and "colum" in option)):
        query+="rename column "
        while(nxtfield=="yes"):
            fname=input("Enter the Field name to rename:")
            newfname=input("Enter the new Field name:")
            query+=fname+" to "+newfname
            nxtfield=input("Do you want to rename another field?")
            if(nxtfield=="yes"):
                query+=",rename column "
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)
 
    elif("rename" in option ):
        newtbname=input("Enter the new Table name:")
        query+="rename "+newtbname
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+newtbname)
        for i in mycursor:
            print(i)

def droptb(tbname):
    global mycursor
    mycursor.execute("drop table "+tbname)

def truncatetb(tbname):
    global mycursor
    mycursor.execute("truncate table "+tbname)

def renametb(tbname,newtbname):
    global mycursor
    mycursor.execute("rename table "+tbname+" to "+newtbname)

def insertrec(tbname):
    global mycursor
    insnext="yes"
    query="insert into "+tbname+" values "
    mycursor.execute("desc "+tbname)
    mylist=list(mycursor)
    while(insnext=="yes"):
        for i in mylist:
            i0=str(i[0])
            i1=str(i[1])
            print("Enter value for the field "+i0+"("+i1[2:len(i1)-1]+"):")
            value=input()
            if (mylist.index(i)==0):
                query+="("
            if ("varchar" in i1):
                query+="'"+value+"'"
            else:
                query+=value
            if (mylist.index(i)!=len(mylist)-1):
                query+=","
            else:    
                query+=")"
        insnext=input("Do you want to insert another record?")
        if(insnext=="yes"):
            query+=","
    mycursor.execute(query)

def updaterec(tbname):
    global mycursor
    quotation=0
    updnext="yes"
    query="update "+tbname+" set "
    mycursor.execute("desc "+tbname)
    mylist=list(mycursor)
    fieldlist=[]
    for i in mylist:
        fieldlist.append(i[0])
    
    while(updnext=="yes"):
        fname=input("Enter the Field name:")
        while(fname not in fieldlist):
            print("Sorry, there is no Field with name ",fname)
            fname=input("Enter the Field name:")
        else:
            fval=input("Enter the value to update:")
            query+=fname+"="
            for i in mylist:
                if (i[0]==fname and "varchar" in str(i[1])):
                    query+="'"
                    quotation=1
            query+=fval
            if (quotation==1):
                query+="'"
                quotation=0
        updnext=input("Do you want to update any other?:")
        if(updnext=="yes"):
            query+=","
    condfield=input("Which record(s) you want to update? give condition")
    query+=" where "+condfield
    mycursor.execute(query)

def selectrec(tbname,selallrec,selallfield):
    global mycursor
    if(selallrec=="yes" and selallfield=="yes"):
        query="select * from "+tbname
    elif(selallfield=="yes"):
        query="select * from "+tbname+" where "
        condfield=input("Which record(s) you want to display? give condition")
        query+=condfield
    elif(selallrec=="yes"):
        query="select "
        nxtfield="yes"
        mycursor.execute("desc "+tbname)
        mylist=list(mycursor)
        fieldlist=[]
        for i in mylist:
           fieldlist.append(i[0])
        while(nxtfield=="yes"):
           fname=input("Enter the Field name:")
           while(fname not in fieldlist):
             print("Sorry, there is no Field with name ",fname)
             fname=input("Enter the Field name:")
           query+=fname
           nxtfield=input("Do you want to display another Field?:")
           if(nxtfield=="yes"):
              query+=","
        query+=" from "+tbname
    else:
        query="select "
        nxtfield="yes"
        mycursor.execute("desc "+tbname)
        mylist=list(mycursor)
        fieldlist=[]
        for i in mylist:
           fieldlist.append(i[0])
        while(nxtfield=="yes"):
           fname=input("Enter the Field name:")
           while(fname not in fieldlist):
             print("Sorry, there is no Field with name ",fname)
             fname=input("Enter the Field name:")
           query+=fname
           nxtfield=input("Do you want to display another Field?:")
           if(nxtfield=="yes"):
              query+=","
        query+=" from "+tbname+" where "
        condfield=input("Which record(s) you want to display? give condition")
        query+=condfield
    mycursor.execute(query)
    for i in mycursor:
        print(i)
    
def deleterec(tbname):
    global mycursor
    query="delete from "+tbname+" where "
    condfield=input("Which record(s) you want to delete? give condition")
    query+=condfield
    mycursor.execute(query)
def desctb(tbname):
    global mycursor
    mycursor.execute("desc "+tbname)
    for i in mycursor:
        print(i)
def commit():
    global mycursor
    mycursor.execute("commit")
    
    
    

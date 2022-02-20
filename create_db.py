import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root"
    )
    mycursor = mydb.cursor()
    
    mycursor.execute("CREATE DATABASE IF NOT EXISTS empmangsys")

    print('Database Created Successfully!!')
       
    mydb.commit()
except Exception as ex:
    messagebox.showerror('Error', f'Error Occured Due To {ex}')

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="empmangsys"
    )
    mycursor = mydb.cursor()
    
    mycursor.execute('''CREATE TABLE IF NOT EXISTS `admin` (
  `ADMINID` int NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Gender` char(6) NOT NULL,
  `Email` varchar(225) NOT NULL,
  `Mobile` char(13) NOT NULL,
  `Username` char(8) NOT NULL,
  `Password` varchar(225) NOT NULL,
  PRIMARY KEY (`ADMINID`)
);''')

    mycursor.execute('''CREATE TABLE  IF NOT EXISTS `department` (
  `Name` varchar(255) NOT NULL,
  `Department_Head` varchar(255) NOT NULL,
  PRIMARY KEY (`Name`)
);''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `employee` (
  `EMPID` int NOT NULL,
  `Name` varchar(255) NOT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` char(6) NOT NULL,
  `Mobile` char(13) DEFAULT NULL,
  `Email` varchar(255) NOT NULL,
  `DOJ` date NOT NULL,
  `Profile` varchar(255) NOT NULL,
  `Department` varchar(255) NOT NULL,
  `Salary` decimal(7,2) NOT NULL,
  `Conveyance` decimal(7,2) NOT NULL,
  PRIMARY KEY (`EMPID`),
  KEY `Department` (`Department`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`Department`) REFERENCES `department` (`Name`)
);''')

    mycursor.execute(''' CREATE TABLE IF NOT EXISTS `salary` (
  `EMPID` int NOT NULL,
  `Basic_Salary` decimal(7,2) DEFAULT NULL,
  `Overtime_Rs` decimal(7,2) DEFAULT NULL,
  `Conveyance_Rs` decimal(7,2) DEFAULT NULL,
  `Deduction_Rs` decimal(7,2) DEFAULT NULL,
  `Net_Salary_Rs` decimal(7,2) DEFAULT NULL,
  `Last_Updated` varchar(255) DEFAULT NULL,
  KEY `EMPID` (`EMPID`),
  CONSTRAINT `salary_ibfk_1` FOREIGN KEY (`EMPID`) REFERENCES `employee` (`EMPID`)
)''')

    print('Database Tables Created Successfully!!')
       
    mydb.commit()
except Exception as ex:
    messagebox.showerror('Error', f'Error Occured Due To {ex}')
    
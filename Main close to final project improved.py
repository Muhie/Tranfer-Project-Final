import random
from array import array
from datetime import date
import datetime
from datetime import datetime
from traceback import print_exc
import pyodbc
import time
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from BookingSytemV11 import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets


class Theatre(QDialog):
    def __init__(self): #initialiatising all values that need to be set at the start of the program.
        super(QDialog, self).__init__()
        self.ui = Ui_Cinema()
        self.ui.setupUi(self)
        self.statementsearch = ""
        self.ui.Buy_PB.clicked.connect(self.GetInputs)
        self.show()
        self.ui.SeatE_PB_2.clicked.connect(self.choosefull)
        self.ui.SeatE_PB.clicked.connect(self.chooseEmpty)
        self.ui.Seat_PB.clicked.connect(self.chooseALL)
        self.ui.NewShow_pb.clicked.connect(self.NewPerformances)
        self.ui.Customer_PB.clicked.connect(self.FindCust)
        self.ui.Reset.clicked.connect(self.Reset)
        today = date.today()
        nowy = datetime.now().year
        nowm = now = datetime.now().month
        nowd = now = now = datetime.now().day # not allowing a date more than a year after the current date to prevent random tables being created like in 2040.
        self.ui.PERFORMANCE_LE.setMinimumDate(QtCore.QDate(today))
        self.ui.PERFORMANCE_LE.setMaximumDate(QtCore.QDate(nowy+1, nowm, nowd))
        self.ui.ADULT_SB.valueChanged.connect(self.SBvaluechange)
        self.ui.CHILD_SB.valueChanged.connect(self.SBvaluechange)
        self.ui.OAP_SB.valueChanged.connect(self.SBvaluechange)
        self.ui.pushButton.clicked.connect(self.SearchCustData)
        self.totalprice = 0
        self.BuySeatSQL = ""
        self.StandardDate = '""'
        self.ui.Table_Table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.Table_Table.cellClicked.connect(self.cell_was_clicked)
        self.total = []
        self.totalFormatSQL = []
        self.runingcount = 0
        self.SeatID = ''
        self.BookingRef = ''
        self.changeheaders = 0
        self.totalfullseats = 0
        self.adult = 10
        self.childprice = 5
        self.oap_Price = 0
        self.value = 0
        self.length = 0
        self.setrowcount = 0
    def Reset(self):
        self.ui.CustType_LE.setText("")
        self.totalFormatSQL.clear()
        self.total.clear()
        self.runingcount = 0
    def Seats_Selected(self):
        self.ui.CustType_LE.setText(self.selected_Seat)
    def cell_was_clicked(self):
        current_row = self.ui.Table_Table.currentRow()
        current_column = self.ui.Table_Table.currentColumn()
        try:
            cell_value = self.ui.Table_Table.item(current_row, current_column).text()
            if cell_value == "EMPTY":
                if self.ui.BlockSeats.isChecked() == True:
                    #Allowing for blocking of seats
                    self.runingcount = 0
                    self.totalseats = 1
                    self.seatRow = current_row
                    self.seatColumn = current_column
                    self.Seats_Selected()
                else:
                    pass
                self.seatRow = current_row
                self.seatColumn = current_column
                self.Seats_Selected()
            else:
                print("cell is not EMPTY, the seat must be empty to be added.")
        except:
            print("cell is not EMPTY, the seat must be empty to be added.")
    def Seats_Selected(self):
        self.totalseats = self.ui.ADULT_SB.value() + self.ui.CHILD_SB.value() + self.ui.OAP_SB.value() + self.ui.VIP_SB.value()
        if self.ui.BlockSeats.isChecked() == True:
            self.totalseats = 1
        else:
            pass
        if self.runingcount >= self.totalseats: #not allowing more seats than the total number of seats selected to be booked
            print("ignor if blocked seats is checked, else please check that you have a enough seats booked.")
            return
        else:
            pass
        self.seatColumn += 1
        self.seatRow += 1
        if not self.total:
            pass
        else:
            self.total.append(",")
        if self.seatColumn == 1: #finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "A"
            self.total.append(self.seatColumn) 
            self.total.append(self.seatRow)     
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
        elif self.seatColumn == 2:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "B"
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
        
        elif self.seatColumn == 3:
            self.seatColumn = "C"#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
           
        elif self.seatColumn == 4:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "D"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
        
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
           
        elif self.seatColumn == 5:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "E"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            print(self.total)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
           
        elif self.seatColumn == 6:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "F"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            print(self.total)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
            
        elif self.seatColumn == 7:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "G"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            print(self.total)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
            
        elif self.seatColumn == 8:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "H"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            print(self.total)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
        
        elif self.seatColumn == 9:#finding the seat selected, appending to the list on the gui wiget and not allowing for full seats to be booked
            self.seatColumn = "I"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            print(self.total)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
           
        elif self.seatColumn == 10:
            self.seatColumn = "J"
            seat = self.seatRow,self.seatColumn
            self.total.append(self.seatColumn)
            self.total.append(self.seatRow)
            print(self.total)
            makeitastring = ''.join(map(str, self.total))
            self.ui.CustType_LE.setText(makeitastring)
            self.runingcount += 1
            self.totalFormatSQL.append(self.seatColumn) 
            self.totalFormatSQL.append(self.seatRow)
            self.Seat_Row = self.totalFormatSQL[1::2]
            self.Seat_Col = self.totalFormatSQL[0::2]
        else:
            print("If you would like to add more seats please, add more ticket holders.")
            pass
    def GetInputs(self):
        if self.ui.BlockSeats.isChecked() == True:
            self.length = len(self.Seat_Row)
            self.MakeSeatsFull()
        else:
            pass
        Name = self.ui.NAME_LE_2.text() #not allowing any empty inputs!
        if Name == "" or Name =="full" or Name == "empty" or Name =="FULL" or Name == "EMPTY":
            print("Name is empty, please add a value to this field")
            return
        else:
            self.NameFinal = Name
            print(self.NameFinal)
        Phone = self.ui.PHONE_LE.text()
        if Phone == "07" or "": #not allowing any empty inputs!
            print("Phone is empty, please add a value to this field")
            return
        else:
            for i in range(0,11):
                if Phone[i].isdigit():
                    pass
                else:
                    return
            self.PhoneFinal = Phone
            print(self.PhoneFinal)
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        print(self.StandardDate)
        Row = self.ui.CustType_LE.text()
        #self.Col = self.ui.Col_SB.value()
        self.length = len(self.Seat_Row)
        if self.length != self.totalseats:
                print("please enter the correct amount of seats, for the number of people booked.")
        else:
            self.MakeSeatsFull()
    def MakeSeatsFull(self):
        print(self.length)
        for i in range(0,self.length):
            print(i)
            RawDate = self.ui.PERFORMANCE_LE.date()
            self.StandardDate = RawDate.toPyDate()
            date = self.StandardDate
            self.dateformatted = (f'"{date}"')
            frow = self.Seat_Row[i]
            fcol = self.Seat_Col[i]
            print(frow)
            print(fcol)
            self.commitSQl = "UPDATE {} SET {} = 'FULL' WHERE Seatrow = {}".format(self.dateformatted,fcol,frow)
            print(self.commitSQl)
            #self.ui.BlockSeats.setChecked(False)
            self.Commiting()
            print("successfully added customers to the database.")
            i+=1
        if self.ui.BlockSeats.isChecked() == True:
            pass
            self.ui.CustType_LE.setText("")
            self.runingcount = 0
            self.totalFormatSQL.clear()
            self.total.clear()
            self.chooseALL()
        else:
            print("inserting customer details to the databse")
            self.insert_customers()
            self.ui.CustType_LE.setText("")
            self.runingcount = 0
            self.totalFormatSQL.clear()
            self.total.clear()   
    def SBvaluechange(self): #changing the running count of the spin box, with the smart pricing algorithm attached.
        now = date.today()
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        date_Difference = self.StandardDate - now
        if date_Difference.days < 5:
            self.adult = 5
            self.childprice = 2.0
            self.oap_Price = 2.5
        else:
            self.adult = 10
            self.childprice = 5
            self.oap_Price = 5
        self.totalprice = self.ui.ADULT_SB.value()*self.adult + self.ui.CHILD_SB.value()*self.childprice + self.ui.OAP_SB.value()*self.oap_Price
        self.ui.PAY_LE.setText(str(self.totalprice))
    def chooseALL(self):
        self.ui.Table_Table.setRowCount(20)
        self.ui.CustType_LE.setText("")
        self.totalFormatSQL.clear()
        self.total.clear()
        self.runingcount = 0
        self.totalfullseats = 0
        self.ui.CustType_LE.setText("")
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        date = self.StandardDate
        self.dateformatted = (f'"{date}"')
        self.FindSQL = "Select A,B,C,D,E,F,G,H,I,J from {}".format(self.dateformatted)
        self.conformation = "ALL" #selecting all seats form the date selected!
        self.changeheaders = 0
        self.totalfullseats = 0
        self.Show_Search_Data()
        self.Searching()
        self.value = 1
        self.FindSQL = "SELECT tCustomer.PhoneNumber, tCustomer.Name, tBooking.BookingRef, tBooking.date, tSeat.SBooked, tSeat.PricePaid FROM tCustomer INNER JOIN tBooking ON  tCustomer.PhoneNumber = tBooking.PhoneNumber INNER JOIN tTicket on tBooking.BookingRef = tTicket.BookingRef INNER JOIN tSeat on tSeat.SeatID = tTicket.SeatID WHERE tBooking.date = '{}'".format(self.dateformatted)

        self.Searching()
        self.value = 0
        self.show()
    def choosefull(self):
        self.ui.Table_Table.setRowCount(20)
        self.ui.CustType_LE.setText("")
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        date = self.StandardDate
        self.dateformatted = (f'"{date}"')
        self.FindSQL = "Select A,B,C,D,E,F,G,H,I,J from {}".format(self.dateformatted)
        self.conformation = "FULL" # only choosing full seats for the pb full!
        self.changeheaders = 0
        self.Show_Search_Data()
        self.Searching()
        self.show()
    def chooseEmpty(self):
        self.ui.Table_Table.setRowCount(20)
        print(self.ui.SearchSeats.text())
        self.totalfullseats = 0
        self.ui.CustType_LE.setText("")
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        date = self.StandardDate
        self.dateformatted = (f'"{date}"')
        self.FindSQL = "Select A,B,C,D,E,F,G,H,I,J from {}".format(self.dateformatted)
        self.conformation = "EMPTY" #choosing only empty seats for the pb empty seats!
        self.changeheaders = 0
        self.Show_Search_Data()
        self.Searching()
        self.Searching()
    def NewPerformances(self):
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        print(self.StandardDate)
        date = self.StandardDate
        self.dateformatted = (f'"{date}"')
        self.customerTable = "tCust" + self.dateformatted
        self.BookingTable = "tBooking" + self.dateformatted
        self.TicketTable = "tTicket" + self.dateformatted
        self.SeatTable = "tSeats" + self.dateformatted
        print(self.SeatTable)
        self.commitSQl = "CREATE TABLE {}(Seatrow int PRIMARY KEY NOT NULL, DATEOP DATE NOT NULL, A VARCHAR(8) NOT NULL, B VARCHAR(8) NOT NULL, C VARCHAR(8) NOT NULL, D VARCHAR(8) NOT NULL, E VARCHAR(8) NOT NULL, F VARCHAR(8) NOT NULL, G VARCHAR(8) NOT NULL, H VARCHAR(8) NOT NULL, I VARCHAR(8) NOT NULL, J VARCHAR(8) NOT NULL)".format(self.dateformatted)
        self.Commiting() #call a function to create a table!
        self.PopulateTable()
    def PopulateTable(self):
        date = self.StandardDate
        for i in range(1,21):
            self.commitSQl = "insert into ""{}"" values('{}','{}','EMPTY','EMPTY','EMPTY','EMPTY','EMPTY','EMPTY','EMPTY','EMPTY','EMPTY','EMPTY')".format(self.dateformatted,i,date)
            self.Commiting() #call a function to insert the rows into the table!
    def insert_customers(self):
        self.SeatID = self.dateformatted + self.NameFinal
        self.BookingRef = self.dateformatted + self.PhoneFinal
        self.formmatted_Seats = self.ui.CustType_LE.text()
        self.commitSQl = "insert into tCustomer values('{}','{}') insert into tBooking values('{}','{}','{}') insert into tTicket values('{}','{}') insert into tSeat Values('{}','{}','{}')".format(self.PhoneFinal,self.NameFinal,self.BookingRef,self.dateformatted,self.PhoneFinal,self.BookingRef,self.SeatID,self.SeatID,self.formmatted_Seats,self.totalprice)
        print(self.commitSQl)
        self.Commiting()
    def SearchCustData(self):
        if self.ui.NAME_LE_2.text() != "":
             self.FindSQL = "SELECT tCustomer.PhoneNumber, tCustomer.Name, tBooking.BookingRef, tBooking.date, tSeat.SBooked, tSeat.PricePaid FROM tCustomer INNER JOIN tBooking ON  tCustomer.PhoneNumber = tBooking.PhoneNumber INNER JOIN tTicket on tBooking.BookingRef = tTicket.BookingRef INNER JOIN tSeat on tSeat.SeatID = tTicket.SeatID WHERE tCustomer.Name = '{}' AND tBooking.date = '{}'".format(self.ui.NAME_LE_2.text(),self.dateformatted)
             self.changeheaders = 1
             self.conformation = ""
             self.Searching()
             self.Show_Search_Data()
        elif self.ui.SearchSeats.text() != "":
             temp = self.ui.SearchSeats.text()
             self.FindSQL = "SELECT tCustomer.PhoneNumber, tCustomer.Name, tBooking.BookingRef, tBooking.date, tSeat.SBooked, tSeat.PricePaid FROM tCustomer INNER JOIN tBooking ON  tCustomer.PhoneNumber = tBooking.PhoneNumber INNER JOIN tTicket on tBooking.BookingRef = tTicket.BookingRef INNER JOIN tSeat on tSeat.SeatID = tTicket.SeatID WHERE tSeat.SBooked like '%{}%' AND tBooking.date = '{}'".format(temp,self.dateformatted)
             self.changeheaders = 1
             self.conformation = ""
             self.Searching()
             self.Show_Search_Data()
        elif self.ui.PHONE_LE.text() != "":
             self.FindSQL = "SELECT tCustomer.PhoneNumber, tCustomer.Name, tBooking.BookingRef, tBooking.date, tSeat.SBooked, tSeat.PricePaid FROM tCustomer INNER JOIN tBooking ON  tCustomer.PhoneNumber = tBooking.PhoneNumber INNER JOIN tTicket on tBooking.BookingRef = tTicket.BookingRef INNER JOIN tSeat on tSeat.SeatID = tTicket.SeatID WHERE tCustomer.PhoneNumber = '{}' AND tBooking.date = '{}'".format(self.ui.PHONE_LE.text(),self.dateformatted)
             self.changeheaders = 1
             self.conformation = ""
             self.Searching()
             self.Show_Search_Data()
    def FindCust(self):
        RawDate = self.ui.PERFORMANCE_LE.date()
        self.StandardDate = RawDate.toPyDate()
        date = self.StandardDate
        self.dateformatted = (f'"{date}"')
        print(self.dateformatted)
        self.value = 1
        self.setrowcount = 1
        self.FindSQL = "SELECT tCustomer.PhoneNumber, tCustomer.Name, tBooking.BookingRef, tBooking.date, tSeat.SBooked, tSeat.PricePaid FROM tCustomer INNER JOIN tBooking ON  tCustomer.PhoneNumber = tBooking.PhoneNumber INNER JOIN tTicket on tBooking.BookingRef = tTicket.BookingRef INNER JOIN tSeat on tSeat.SeatID = tTicket.SeatID WHERE tBooking.date = '{}'".format(self.dateformatted)
        self.value = 1
        self.changeheaders = 1
        self.conformation = ""
        self.Searching()
        self.Show_Search_Data()
        self.value = 0
        self.setrowcount = 0
    
    def Commiting(self):#inserting, updating and deleting values from the tables!
        statementSQL=self.commitSQl
        try:
            cs = (
                "Driver={SQL Server};"
                "Server=RX-ORIGIN\MSSQLSERVER01;"
                "Database=Muhie;"
                "Trusted_Connection=yes;"
                "UID=RX-ORIGIN\16mal;"
            )
            cnxn = pyodbc.connect(cs)
            print("Connected")
            if cs is not None:
                cursor = cnxn.cursor()
                cursor.execute(statementSQL)
                cursor.commit()
        except pyodbc.DatabaseError as err:
            print("SQL Error, Plese check you have everything formatted correctly: {}".format(err))
        finally:
            cnxn.close()
            print("Connection Closed")
    def Searching(self):#Searching for values!
        totalRev = 0
        statementSQL = self.FindSQL
        try:

            cs = (
                "Driver={SQL Server};"
                "Server=RX-ORIGIN\MSSQLSERVER01;"
                "Database=Muhie;"
                "Trusted_Connection=yes;"
                "UID=RX-ORIGIN\16mal;"
            )
            cnxn = pyodbc.connect(cs)
            print("Connected")
            if cs is not None:
                cursor = cnxn.cursor()
                cursor.execute(statementSQL)
                records = cursor.fetchall()
                if self.value == 1:
                    self.arraytobesortedaytobesorted = []
                    for row in records:
                        total = total =+ 1
                        total = row[5]
                        value = float(row[5])
                        self.arraytobesortedaytobesorted.append(value)
                        rawValue = total.strip("")
                        revenueMake = float(rawValue)
                        totalRev = totalRev + revenueMake
                    self.ui.AvalibleSeats_2.setText(str(totalRev))
                    def QuickSort(arr):
                        elements = len(arr)
                        
                        #Base case
                        if elements < 2:
                            return arr
                        
                        current_position = 0 #Position of the partitioning element

                        for i in range(1, elements): #Partitioning loop
                            if arr[i] <= arr[0]:
                                current_position += 1
                                temp = arr[i]
                                arr[i] = arr[current_position]
                                arr[current_position] = temp

                        temp = arr[0]
                        arr[0] = arr[current_position] 
                        arr[current_position] = temp #Brings pivot to it's appropriate position
                        
                        left = QuickSort(arr[0:current_position]) #Sorts the elements to the left of pivot
                        right = QuickSort(arr[current_position+1:elements]) #sorts the elements to the right of pivot

                        arr = left + [arr[current_position]] + right #Merging everything together
                        
                        return arr
                    if len(self.arraytobesortedaytobesorted) > 10:
                        array_to_be_sorted = self.arraytobesortedaytobesorted
                        print("The Most Paying customers in using quick sort order are: ",QuickSort(array_to_be_sorted))
                    else:
                        pass
                    def bubbleSort(arr):
                        n = len(arr)
                    
                        # Traverse through all array elements
                        for i in range(n-1):
                        # range(n) also work but outer loop will
                        # repeat one time more than needed.
                    
                            # Last i elements are already in place
                            for j in range(0, n-i-1):
                    
                                # traverse the array from 0 to n-i-1
                                # Swap if the element found is greater
                                # than the next element
                                if arr[j] > arr[j + 1] :
                                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    
                    # Driver code to test above

                    if len(self.arraytobesortedaytobesorted) == 1 or len(self.arraytobesortedaytobesorted) == 0:
                        pass
                    elif len(self.arraytobesortedaytobesorted) < 10:
                        arr = self.arraytobesortedaytobesorted
                        bubbleSort(arr)
                        print ("Most paying customers using buble sort is:")
                        for i in range(len(arr)):
                            print("% d" % arr[i],end=" ")
                    else:
                        pass
            if self.setrowcount == 1:
                self.ui.Table_Table.setRowCount(len(self.arraytobesortedaytobesorted))
            else:
                self.ui.Table_Table.setRowCount(20)

 

        except pyodbc.DatabaseError as err:
            print("SQL Error, Plese check you have everything formatted correctly: {}".format(err))
            self.ui.Table_Table.clearContents()

        finally:
            cnxn.close()

    def Show_Search_Data(self):#showing the search values in the table
        # clean table
        self.ui.Table_Table.clearContents()
        statementSQL = self.FindSQL

        # populate table headers
        if self.changeheaders == 1:
            self.ui.Table_Table.setColumnCount(6)
            col = ["Phone","Customer","BookRef","Date","Seats Booked","PricePaid"]
            self.ui.Table_Table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.ui.Table_Table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            self.ui.Table_Table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            self.ui.Table_Table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            self.ui.Table_Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            self.ui.Table_Table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        else:
            col = ["A","B", "C", \
               "D", "E","F","G" , "H","I","J"]
            self.ui.Table_Table.setColumnCount(10)
        self.ui.Table_Table.setHorizontalHeaderLabels(col)
        #statementSQL = self.FindSQL
        try:

            cs = (
                "Driver={SQL Server};"
                "Server=RX-ORIGIN\MSSQLSERVER01;"
                "Database=Muhie;"
                "Trusted_Connection=yes;"
                "UID=RX-ORIGIN\16mal;"
            )
            cnxn = pyodbc.connect(cs)

            if cs is not None:
                cursor = cnxn.cursor()
                cursor.execute(statementSQL)
                rows = cursor.fetchall()
                
                

                noRow = 0
                for tuple in rows:
                    noCol = 0
                    for column in tuple:
                        satuKolum = QTableWidgetItem(str(column))
                        if column == self.conformation:
                            self.ui.Table_Table.setItem(noRow, noCol, satuKolum)
                            if column == "FULL":
                                self.ui.Table_Table.item(noRow, noCol).setBackground(QtGui.QColor(255,0,0))
                            elif column == "EMPTY":
                                self.ui.Table_Table.item(noRow, noCol).setBackground(QtGui.QColor(0,100,0))
                        elif self.conformation == "":
                            self.ui.Table_Table.setItem(noRow, noCol, satuKolum)
                        elif self.conformation == "ALL":
                            self.ui.Table_Table.setItem(noRow, noCol, satuKolum)
                            if column == "FULL":
                                self.totalfullseats += 1
                                self.ui.Table_Table.item(noRow, noCol).setBackground(QtGui.QColor(255,0,0))
                                formmated = str(200-self.totalfullseats)
                                self.ui.AvalibleSeats.setText(formmated)

                            elif column == "EMPTY":
                                if self.totalfullseats == 0:
                                    self.ui.AvalibleSeats.setText("200")
                                    self.ui.AvalibleSeats_2.setText("0")
                                self.ui.Table_Table.item(noRow, noCol).setBackground(QtGui.QColor(0,100,0))
                        noCol += 1
                    noRow += 1
        except pyodbc.DatabaseError as err:
            print("SQL Error, Plese check you have everything formatted correctly: {}".format(err))
            self.ui.Table_Table.clearContents()
            
        finally:
            cnxn.close()





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Start = Theatre()
    Start.show()
    sys.exit(app.exec())

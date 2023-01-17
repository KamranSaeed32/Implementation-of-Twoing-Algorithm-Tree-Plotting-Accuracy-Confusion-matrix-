import numpy as num
import pandas as pd
from scipy.io import arff
from math import *
import decimal
import csv
import os

Tree=[]
otheritem=0
file_path=""
record_path=""
listem=[]
TRight_TLeft=""
Heading=[]
Heading_Copy=[]
Deletedstring=[]
Different_Dataset=[]
Eligibility_Results=[]
otheritem=[]
highestvalue=0;
Dataset=[]
Total_Data=0
To_Continue=0
Question=0
needtorurnightiteration = 0
needtorunleftiteration = 0
crossvalidate=0

def First_function(file_path):

    global Heading_Copy
    Arff_File(file_path)
    global combo
    global Total_Data
    Heading_Copy=Heading[:]
    for i in range(0,Heading_Copy.__len__()):
        if(Dataset[1][i].isdigit() == 1):
            Heading_Copy.pop(i)
    Heading_Copy.pop(Heading_Copy.__len__()-1)
    Heading_Copy.append("All")
    Total_Data=Dataset.__len__()
    Secondfunction()





def Secondfunction():

  global Eligibility_Results
  global Heading_Copy
  global highestvalue
  global Deletedstring
  global otheritem
  print("Next Iteration Start:")
  del Eligibility_Results[:]
  Number=1
  TRight_TLeft = "\n\n\n"
  for i in range(0,Heading_Copy.__len__()-1):
    Calculation(Heading.index(Heading_Copy[i]))
    for i in range(0, len(Eligibility_Results)):
        TRight_TLeft += "- - - - - - - - Candidate Section #" + str(Number) + " - - - - - - - -\nT_Left = " + str(
        Eligibility_Results[i][0]) + "\n" \
                                   "T_Right = " + str(Eligibility_Results[i][1]) + "\n" \
                                                                                 "Eligibility Criteria = " + str(
            Eligibility_Results[i][2]) + "\n"
        if highestvalue<=Eligibility_Results[i][2]:
            highestvalue=Eligibility_Results[i][2]
            Deletedstring=Eligibility_Results[i][1]
            otheritem=Eligibility_Results[i][0]

        else:
            highestvalue=highestvalue
        Number += 1
    del Eligibility_Results[:]

  print(TRight_TLeft)

def  Arff_File(file_path):
    global TRight_TLeft
    global To_Continue
    with open(file_path) as f:
        for g in(f.readlines()):
            if(To_Continue == 1):
                Temporary=g.split(",")
                Temporary[Temporary.__len__()-1]=Temporary[Temporary.__len__()-1].replace("\n","")
                Dataset.append(Temporary)
            if(g.lower().__contains__("@attribute")):
                Temporary=g.split(" ")
                Heading.append(Temporary[1])
            if(g.lower().__contains__("@data") == 1):
                To_Continue=1


def Calculation(T_index):
    global Different_Dataset
    del Different_Dataset[:]
    for data in Dataset:
        if(Different_Dataset.__contains__(data[T_index]) != 1):
            Different_Dataset.append(data[T_index])

    Main_Transaction(0,T_index)


def Main_Transaction(T_Index_Use,T_index):
    global Different_Dataset
    global Eligibility_Results
    if(T_Index_Use < Different_Dataset.__len__()):
        T_Left = []
        TRight = []
        del T_Left[:]
        del TRight[:]

        for i in range(0, Different_Dataset.__len__()):
            if (i == T_Index_Use):
                T_Left.append(Different_Dataset[i])
            else:
                TRight.append(Different_Dataset[i])

        T_left_No = 0
        for data in Dataset:
            if (data[T_index] == T_Left[0]):
                T_left_No += 1
        T_right_No = 0
        for data in Dataset:
            for eleman in TRight:
                if (eleman == data[T_index]):
                    T_right_No += 1
        global Total_Data
        P_left=T_left_No/Total_Data
        P_right=T_right_No/Total_Data
        Conditions =[]
        del Conditions[:]
        for data in Dataset:
            if(Conditions.__contains__(data[data.__len__()-1])!= 1):
                Conditions.append(data[data.__len__()-1])
        Tleft_Condition=[]
        TRight_Condition=[]

        del Tleft_Condition[:]
        del TRight_Condition[:]
        for i in range(Conditions.__len__()):
            Tleft_Condition.append(0)
            TRight_Condition.append(0)

        for data in Dataset:
            for tsol in T_Left:
                if(tsol == data[T_index]):
                    for i in range (0,Conditions.__len__()):
                        if(data[data.__len__()-1] == Conditions[i]):
                            Tleft_Condition[i]+=1

        for data in Dataset:
            for tsag in TRight:
                if (tsag == data[T_index]):
                    for i in range(0, Conditions.__len__()):
                        if (data[data.__len__() - 1] == Conditions[i]):
                            TRight_Condition[i] += 1

        P_Tleft_Condition=[]

        del P_Tleft_Condition[:]
        total=0

        for ts in Tleft_Condition:
            total+=ts


        for ts in Tleft_Condition:
            P_Tleft_Condition.append(ts/total)

        P_TRight_Condition = []

        del P_TRight_Condition[:]
        total = 0
        for ts in TRight_Condition:
            total += ts
        for ts in TRight_Condition:
            P_TRight_Condition.append(ts / total)

        doncek=0
        for i in range(0,P_Tleft_Condition.__len__()):
            doncek+=(fabs(P_Tleft_Condition[i]-P_TRight_Condition[i]))

        Suitability=2*P_left*P_right*doncek
        yuvarlanmis_Suitability=decimal.Decimal(Suitability)
        deger=yuvarlanmis_Suitability.__float__()


        Temporarydizi=[T_Left,TRight,round(deger,2)]
        Eligibility_Results=Eligibility_Results[:]
        Eligibility_Results.append(Temporarydizi)

        T_Index_Use+=1
        return Main_Transaction(T_Index_Use,T_index)


    else:
            return




def getCSVFromArff(fileName):
   with open(fileName + '.arff', 'r') as fin:
      data = fin.read().splitlines(True)
   i = 0
   cols = []
   for line in data:
      line = line.lower()
      if ('@data' in line):
         i+= 1
         break
      else:

         i+= 1
         if (line.startswith('@attribute')):
            if('{' in line):
               cols.append(line[11:line.index('{')-1])
            else:
               cols.append(line[11:line.index(' ', 11)])
   headers = ",".join(cols)
   with open(fileName + '.csv', 'w') as fout:
      fout.write(headers)
      fout.write('\n')
      fout.writelines(data[i:])

def csvtoarff(file_path):
    fileToRead = file_path
    if(whichfiletoconvert==1):
        fileToWrite = "output.arff" #name as how you'll save your arff file.
    elif(whichfiletoconvert==2):
        fileToWrite = "output2.arff"  # name as how you'll save your arff file
    relation = "World Cup 2014" #how you'll like to call your relation as.

    dataType = [] # Stores data types 'nominal' and 'numeric'
    columnsTemp = [] # Temporary stores each column of csv file except the attributes
    uniqueTemp = [] # Temporary Stores each data cell unique of each column
    uniqueOfColumn = [] # Stores each data cell unique of each column
    dataTypeTemp = [] # Temporary stores the data type for cells on each column
    finalDataType = [] # Finally stores data types 'nominal' and 'numeric'
    attTypes = [] # Stores data type 'numeric' and nominal data for attributes
    p = 0 # pointer for each cell of csv file

    writeFile = open(fileToWrite, 'w')

#Opening and Reading a CSV file
    f = open(fileToRead, 'r')
    reader = csv.reader(f)
    allData = list(reader)
    attributes = allData[0]
    totalCols = len(attributes)
    totalRows = len(allData)
    f.close()

# Add a '0' for each empty cell
    for j in range(0,totalCols):
       for i in range(0,totalRows):
          if 0 == len(allData[i][j]):
             allData[i][j] = "0"

# check for comams or blanks and adds single quotes
    for j in range(0,totalCols):
       for i in range(1,totalRows):
          allData[i][j] = allData[i][j].lower()
          if "\r" in allData[i][j] or '\r' in allData[i][j] or "\n" in allData[i][j] or '\n' in allData[i][j]:
             allData[i][j] = allData[i][j].rstrip(os.linesep)
             allData[i][j] = allData[i][j].rstrip("\n")
             allData[i][j] = allData[i][j].rstrip("\r")
          try:
             if allData[i][j] == str(float(allData[i][j])) or allData[i][j] == str(int(allData[i][j])):
                print
          except ValueError as e:
                allData[i][j] = "" + allData[i][j] + ""

# fin gives unique cells for nominal and numeric
    for j in range(0,totalCols):
       for i in range(1,totalRows):
          columnsTemp.append(allData[i][j])
       for item in columnsTemp:
          if not (item in uniqueTemp):
             uniqueTemp.append(item)
       uniqueOfColumn.append("{" + ','.join(uniqueTemp) + "}")
       uniqueTemp = []
       columnsTemp = []

# Assigns numeric or nominal to each cell
    for j in range(1,totalRows):
       for i in range(0,totalCols):
          try:
             if allData[j][i] == str(float(allData[j][i])) or allData[j][i] == str(int(allData[j][i])):
                dataType.append("numeric")
          except ValueError as e:
                dataType.append("nominal")

    for j in range(0,totalCols):
       p = j
       for i in range(0,(totalRows-1)):
          dataTypeTemp.append(dataType[p])
          p += totalCols
       if "nominal" in dataTypeTemp:
          finalDataType .append("nominal")
       else:
          finalDataType .append("numeric")
       dataTypeTemp = []

    for i in range(0,len(finalDataType )):
       if finalDataType [i] == "nominal":
          attTypes.append(uniqueOfColumn[i])
       else:
          attTypes.append(finalDataType[i])

# Show comments
    writeFile.write("%\n% Comments go after a '%' sign.\n%\n")
    writeFile.write("%\n% Relation: " + relation +"\n%\n%\n")
    writeFile.write("% Attributes: " + str(totalCols) + " "*5
       + "Instances: " + str(totalRows-1) + "\n%\n%\n\n")

# Show Relation
    writeFile.write("@relation " + relation + "\n\n")

# Show Attributes
    for i in range(0,totalCols):
       writeFile.write("@attribute" + " " + attributes[i]
          + " " + attTypes[i] + "\n")

# Show Data
    writeFile.write("\n@data\n")
    for i in range(1,totalRows):
       writeFile.write(','.join(allData[i])+"\n")



def checkdatavalidation(data,Deletedstring):
    Deletedstring2=Deletedstring[0].replace("'","")
    x=-1
    y=-1
    i=0
    j=0
    k=0
    for i in range(len(data.axes[0])):
        for j in range (len(data.axes[1])):
            temp=[]
            temp=data.iat[i,j]
            if(temp==Deletedstring[0]):
                x=i
                y=j
                break
        if(x>=0 or y>=0):
            break
    last_column =data.iloc[: , -1]
    global crossvalidate
    temp=[]
    temp=last_column[x].replace("'", "")
    if(temp=="yes"):
        crossvalidate=1
    else:
        crossvalidate=2
def generatefile1(data):
    global whichfiletoconvert
    columnname=[]
    Deletedstring[0].replace("'", "")
    if(len(Deletedstring)==1):
        columnname = data.columns[(data == Deletedstring[0]).any()].tolist()
        data = data[data[columnname[0]].str.contains(Deletedstring[0]) == True]
        data.to_csv('output.csv', index=None)
        data = pd.read_csv("output.csv", encoding='latin1')
        data.drop(columnname[0], inplace=True, axis=1)
        data.to_csv('output.csv', index=None)
    else:
        columnname = data.columns[(data == Deletedstring[0]).any()].tolist()
        data = data[data[columnname[0]].str.contains(otheritem[0]) == False]
        data.to_csv('output.csv', index=None)
    data = pd.read_csv("output.csv", encoding='latin1')
    whichfiletoconvert = 1
    csvtoarff('output.csv')


def generatefile2(data):
    global whichfiletoconvert
    columnname=[]
    otheritem[0].replace("'", "")
    if (len(otheritem) == 1):
        columnname = data.columns[(data == otheritem[0] ).any()].tolist()
        data = data[data[columnname[0]].str.contains(otheritem[0]) == True]
        data.to_csv('output2.csv', index=None)
        data.drop(columnname[0], inplace=True, axis=1)
        data.to_csv('output2.csv', index=None)
    else:
        columnname = data.columns[(data == otheritem[0]).any()].tolist()
        data = data[data[columnname[0]].str.contains(Deletedstring[0]) == False]
        data.to_csv('output2.csv', index=None)

    data = pd.read_csv("output.csv", encoding='latin1')
    whichfiletoconvert = 2
    csvtoarff('output2.csv')




def firstiteration(data):
    columnname=[]
    Deletedstring[0].replace("'","")
    columnname=data.columns[(data ==Deletedstring[0] ).any()].tolist()
    Tree.append(columnname)
    last_column = data.iloc[:, -1]
    tempp=[]
    tempp=otheritem[0].replace("'","")
    x=-1
    y=-1
    for i in range(len(data.axes[0])-1):
        for j in range(len(data.axes[1])-1):
            if(data.iat[i, j]==Deletedstring[0]):
                x=i
                y=j
                break
        if(x>=0 or y>=0):
            break
    last_column =data.iloc[: , -1]
    testingclass1=0
    testingclass2=0
    testingclass12=0
    testingclass22=0
    generatedata1=0
    generatedata2=0
    global needtorunrightiteration
    global needtorunleftiteration

    for k in range (len(data.axes[0])-1):
        if(data.iat[k,y]==Deletedstring[0]):
            temp=[]
            temp=last_column[k].replace("'","")

            if(temp=="Yes" or temp =="yes"):
                testingclass1 = 1
            else:
                testingclass2=1
    if(testingclass1==1 and testingclass2==1):
        generatedata1=1
        needtorunrightiteration = 1;
    for k in range (len(data.axes[0])-1):
        if(data.iat[k,y]==otheritem[0]):
            if(last_column[k]=="yes"):
                testingclass12 = 1
            else:
                testingclass22=1
    otheritem2=0;
    otheritem2=testingclass12
    if(testingclass12==1 and testingclass22==1):
        generatedata2=1
        needtorunleftiteration = 1;
    else:
        if(testingclass12==1):
           Tree.append(otheritem)
           Tree.append(": Yes")
        else:
            Tree.append(otheritem)
            checkdatavalidation(data, otheritem)
            if (crossvalidate == 1):
                Tree.append("Yes")
            elif (crossvalidate == 2):
                Tree.append(": No")

    if(generatedata1==1):
        Tree.append(Deletedstring)
        generatefile1(data)
        if(generatedata2==1):
            generatefile2(data)
    else:
        print("complete")


#**********MAIN******************************************
file_path =  ('twoing.arff')
First_function(file_path)
Tree.append("Twoing Dataset")
getCSVFromArff("twoing")
data = pd.read_csv("twoing.csv",encoding='latin1')
firstiteration(data)
for i in range(2):
    if(needtorunrightiteration == 1):
        data=("output.arff")
        file_path = ""
        record_path = ""
        listem = []
        TRight_TLeft = ""
        Heading = []
        Heading_Copy = []
        Deletedstring = []
        Different_Dataset = []
        Eligibility_Results = []
        otheritem = []
        otheritem=0
        highestvalue = 0;
        Dataset = []
        Total_Data = 0
        To_Continue = 0
        Question = 0
        needtorurnightiteration = 0
        needtorunleftiteration = 0
        First_function(data)
        getCSVFromArff("output")
        data = pd.read_csv("output.csv", encoding='latin1')
        firstiteration(data)
        if(needtorunleftiteration==1):
            data = ("output2.arff")
            file_path = ""
            record_path = ""
            listem = []
            TRight_TLeft = ""
            Heading = []
            Heading_Copy = []
            Deletedstring = []
            Different_Dataset = []
            Eligibility_Results = []
            otheritem = []
            highestvalue = 0;
            Dataset = []
            Total_Data = 0
            To_Continue = 0
            Question = 0
            otheritem = 0
            needtorurnightiteration = 0
            needtorunleftiteration = 0

            First_function(data)
            getCSVFromArff("output2")
            data = pd.read_csv("output2.csv", encoding='latin1')
            firstiteration(data)
data = pd.read_csv("output.csv", encoding='latin1')
secondlast_column=[]
secondcolumnname=[]
secondlast_column =data.iloc[: , -2]
last_columnf =data.iloc[: , -1]
secondcolumnname = data.columns[(data == secondlast_column[1]).any()].tolist()
Tree.append(secondcolumnname)
o=0
ij=0
for ij in range (len(secondlast_column)):
    temp=[]
    temp=last_columnf[ij].replace("'","")
    if(temp=="yes"):
        Tree.append(secondlast_column[ij])
        Tree.append(": Yes")
    else:
        Tree.append(secondlast_column[ij])
        Tree.append(": No")
print("Tree :",Tree)
sp=2
step=0
space='-'
for jk in range(len(Tree)):
    print("*",space*(jk+sp), "{",Tree[jk],":")
    sp=sp+1
    if(Tree[jk]==": Yes" or Tree[jk]==": No"):
        sp = sp-4
#********************Defining Rules according to plotted tree**************
predictedresult=[]
data = pd.read_csv("twoingtest.csv", encoding='latin1')
for i in range (len(data)):
    if(data.iat[i,2]=="civil"):
        predictedresult.append("yes")
    elif(data.iat[i,2]=="Information_technology" and data.iat[i,1]=="under_graduate"):
        predictedresult.append("no")
    elif (data.iat[i, 2] == "Information_technology" and data.iat[i, 1] == "primary"):
        predictedresult.append("yes")
    elif (data.iat[i, 2] == "Information_technology" and data.iat[i, 1] == "secondary_school" and data.iat[i,0]=="normal"):
        predictedresult.append("yes")
    else:
        predictedresult.append("no")

#********************Accuracy********************
data = pd.read_csv("twoingtest.csv", encoding='latin1')
last_column =data.iloc[: , -1]
TP=0
TN=0
FP=0
FN=0
correct=0
wrong=0
for ij in range(len(last_column)):
    if(predictedresult[ij]==last_column[ij]):
        correct=correct+1
        if(predictedresult[ij]=="yes"):
            TP=TP+1
        else:
            TN=TN+1
    else:
        wrong=wrong+1
        if(predictedresult[ij]=="no"):
            FP=FP+1
        else:
            FN=FN+1
Accuracy=0
Accuracy=correct/len(predictedresult)*100
print("Accuracy :", Accuracy)
print("Confusion Matrix")
print("[ TP :",TP,",TN :",TN,",FP :",FP,",FN :",FN,"]")












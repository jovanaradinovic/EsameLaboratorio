
import datetime 

class ExamException(Exception): #create a class for exceptions

    pass
 
class CSVTimeSeriesFile: #create a class that read timeseries that can compute the average variance 
    def __init__ (self,name): 
        self.name = name 
        if not isinstance(name, str): 
            raise ExamException("Error: name non è una stringa")
        pass   

    def is_date(self,string): #create a list to see if the date is actually a date
        format="%Y-%m" #define a format
        try:
            datetime.datetime.strptime(string,format) #return true if the string is a date
            return True

        except ValueError: 
            return False

    def get_data(self): #create a list to return a list of the list 
        
        complete_list = [] #empty list  to save all the values
 
        try:
            my_file = open(self.name, 'r')
        except Exception as e: 
           raise ExamException(f"Error happened while reading a file '{e}'") 
 
        for line in my_file: 

            elements = line.split(",") 

            if elements[0] != 'date': #ignore first element which is heading

                try: #set the date and the value
                    date = str(elements[0])
                    #control if the date makes sense using my helping function
                    if not self.is_date(date): 
                    # run if the output of is_date is false and go to the next loop
                        continue

                    value = int(elements[1]) #make the value an integer if it is not don't accept it

                    if value < 0:
                        continue #if value is a negative number don't accept it and continue
                except:
                    continue

                if len(complete_list) > 0: #check if the timestamps is a duplicate of any of the preview timestamps saved
                    for item in complete_list: #loop through the preview timestamps 
                        prev_date = item[0] #save the data value on the previews timestamp

                        if date == prev_date:
                            raise ExamException("Timestamp is a duplicate") 

                    prev_date = complete_list[-1][0] 
                    if date < prev_date:
                        raise ExamException("Timestamp isn't in order")

                complete_list.append([date,value]) #append the date and value lists to the main list for every step

        my_file.close()

        if not complete_list:
            raise ExamException("File is empty")  

        return complete_list 

def detect_similar_monthly_variations(time_series,years): 

   
    if not years: 
        raise ExamException("Error list is empty") 

    if len(years) != 2: 
        raise ExamException("Error list has less then two years")

    if not isinstance(time_series, list): 
        raise ExamException("Error time_series is not list of a list")

    elif not isinstance(time_series[0], list):
        raise ExamException("Error time_series is not list of the list")

    if years[0] == years[1]: 
        raise ExamException("Error two years are the same")

    if years[1] != years[0] + 1:
        raise ExamException("Error first and second year aren't consecutive")

    if years[0] > years[1]:
        raise ExamException("Error first year is smaller then the second year")

    if years[0] < int(time_series[0][0][:4]):
        raise ExamException("Error first year is not in the list")

    if years[1] > int(time_series[-1][0][:4]):
        raise ExamException("Error last year is not in the list")
    
    data = [[],[]]  #list with two lists in  it to  indicate two  years
    j = years[0] #j variable which starts from the first  year

    for i in time_series: 
        if int(i[0][:4])<=years[1] and int(i[0][:4]) >= years [0]: #take first  charachters and convert them to int, and they need to be comprehended between first and second year
            if j  !=  int(i[0][:4]):# j isn't the same for first and second year
                data[1].append(i[1])
            else:
                data[0].append(i[1])

    values=[] #create a list to add values
    values.append(monthly_difference(data[0])) #difference between months in first and second year
    values.append(monthly_difference(data[1]))
    
    values=yearly_difference(values[0],values[1]) 
    return values

def monthly_difference(month): 
    values= [] #create a list to add values
    i = 1
    while i < 12: 
        difference = abs(month[i] - month[i - 1])  #difference of the consecuttive months
        values.append(difference) #add the difference
        i = i + 1
    return values
   
def yearly_difference(first_year,second_year): 
    values = [] 
    i = 0
    while i < 11:
        difference = abs(first_year[i] - second_year[i]) #difference of the  two copies of the same months in different years
        if difference <= 2:  #if the difference is greater than 2, append True, if not append False
             values.append(True)
        else:
            values.append(False)
        i = i + 1
    return values



#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#years = [1949, 1950]
#print(time_series)
#print(detect_similar_monthly_variations(time_series, years))
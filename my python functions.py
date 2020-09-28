#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Question 1 - This function takes a list and returns the absolute value of numeric values which are in a list
                # or a nested list

def absolute_num(t):
    a = []                                      #each function call, create an empty list a which will contain absolute values
    for i in t:           
        
        if type(i) == int or type(i) == float:  
            a.append(abs(i))                    #add absolute value of the numeric values to the list a 
        else:
            try:
                r = float(i)             #check if string can be converted to a numeric
                if r%1 ==0:              #if decimal value is 0, convert to an integer
                    r = int(r)
                a.append(abs(r))         #if value can be converted to a numeric, add the absolute value to a
            except ValueError:
                if i.lower() == 'true':
                    a.append(1)          #if string Boolean True, set to 1
                elif i.lower() == 'false':
                    a.append(0)          #if string Boolean False, set to 0
            except TypeError:                   #check if element is an iterable element
                if type(i) == list:             #if it's a list element, it can be evaluated
                    r = absolute_num(i)         #call function recursively
                    if r != []:                 #make sure function returns a valid list before adding nested list  
                        a.append(r)             #append nested list to a
            except:                            
                continue                        #continue to next element in list if element not able to be processed
    return a


# In[1]:


t = [6.5, [3,5, ['FALSE','ham;','100.00']],'INF-510', -1, 0.1, True, 'US', 3, '-3.75', -5000, ['nested','strings', 'need attention'],'five', -3.567,(4), {'candy' : 4500}, ('hi','bye'), ['5','-9',7, [100.00,100]]]
a = absolute_num(t)
print(a)


#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Question 2 - read csv file and return as a dictionary with column headers as dict keys and columns as correpsonding columns' dict values
def read_csv(filename):
    d = dict()
    c = h = i = 0           #counters -(h)header row, (i)current column number position, (c)total number of columns 
    t = []                  #list to store column position of matching dictionary key (column header)
    try:
        with open(filename, 'r') as fin:   #opening as read access only with context manager to auto-close 
                                           #file at end of block
            for line in fin:
                words = line.split(',')
                for w in words:
                    w = w.rstrip()
                    try:
                        w = float(w)        #check if numeric value and convert from string to numeric
                        if w%1 == 0:        #if decimal is 0, convert to integer
                            w = int(w)
                    except ValueError:
                        if w.lower() =='true':   #convert boolean string values to boolean type
                            w = True
                        elif w.lower() == 'false':
                            w = False
                    if h == 0:              #if it's the 1st line (header), set value as key in dictionary d
                        d[w] = []           #setting value to empty list which will be filled below
                        t.append(w)         #index of list t will match column # in csv file as we loop through
                                            #value of list in t will match key in dictionary
                        c += 1              #c i counter for number of columns in file
                    else:
                        d[t[i]].append(w)   #for non-header rows, lookup key for dictionary in list t, based upon 
                                            #current column number, which is i
                        i += 1              #go to next column
                        if i == c:          #if at end of columns, reset back to next line, first column
                            i = 0
                h = 1          
    except FileNotFoundError as e:
        print(f'Error: Cannot open file.{e}')
    except IOError as e:
        print(f'IO Error: Cannot open file.{e}')
    except PermissionError as e:
        print(f'Error: Cannot open file due to permissions. Need access rights.{e}')
    except Exception as e:
        print(f'Unexpected Error. {e}')

    return d   
                


# In[2]:


filename = 'crime_data.csv'
d = read_csv(filename)
for k in d:
    print(f'{k}:\n{d[k]}\n')


# In[ ]:




#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Question 4 - Read a csv file, tranpose it and write the new transposed data as a csv file
def transpose_file(infile, outfile):
    import csv
    c = h = i = 0           #counters -(h)header row, (i)current column number position, (c)total number of columns 
    tr = []                 #list to store transposed data to be written
    try:
        with open(infile, 'r', encoding = 'utf-8') as fin:   
                                           #opening as read access only with context manager to auto-close 
                                           #file at end of block. 
            for line in fin:
                words = line.split(',')
                for w in words:
                    w = w.rstrip()
                    try:
                        w = float(w)        #check if numeric value and convert from string to numeric
                        if w%1 == 0:        #if decimal is 0, convert to integer
                            w = int(w)
                    except ValueError:
                        if w.lower() =='true':   #convert boolean string values to boolean type
                            w = True
                        elif w.lower() == 'false':
                            w = False
                    if h == 0:              #if it's the 1st line (header), create nested list and append value
                        tr.append([w])           
                        c += 1              #c is counter for number of columns in file
                    else:
                        tr[i].append(w)     #append values to list using corresponding index/column i for non-header rows 
                                            #current column number is i
                        i += 1              #go to next column
                        if i == c:          #if at end of columns, reset back to next line, first column
                            i = 0
                h = 1    
         
        try:                                #only create output file if input file was successfully opened
            with open(outfile, 'w', newline='') as csvfile:  #opening as write access with context manager to auto-close 
                                                             #file at end of block
                tw = csv.writer(csvfile, delimiter=',')      #define writer object as comma delimited
                for i in tr:
                    tw.writerow(i)                           #for each index in list tw, write a row
                
        except IOError as e:                                 #Exceptions for output file
            print(f'IO Error: Cannot open file.{e}')
        except PermissionError as e:
            print(f'Error: Cannot create file due to permissions. Need access rights.{e}')
        except csv.Error as e:
            print(f'Error: problem parsing file into csv format.{e}')      
        except Exception as e:
            print(f'Unexpected Error. {e}')
                
    except FileNotFoundError as e:                           #Exceptions for input file
        print(f'Error: Cannot open file.{e}')
    except IOError as e:
        print(f'IO Error: Cannot open file.{e}')
    except PermissionError as e:
        print(f'Error: Cannot open file due to permissions. Need access rights.{e}')
    except Exception as e:
        print(f'Unexpected Error. {e}')
           


# In[2]:


import sys
if len(sys.argv) < 3:
    print('Too few arguments! Please specify an input file and an output file.')
infile = sys.argv[1]
outfile = sys.argv[2]
transpose_file(infile, outfile)


# In[ ]:






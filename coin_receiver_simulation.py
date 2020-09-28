#!/usr/bin/env python
# coding: utf-8

# Question 3
'''Coin Receiver Simulation - 
        only accepts 10 cent, 25 cent and 50 cent coins
        Enter -1 to stop program
'''
def coin_sim():
    coin = input('Enter a coin! ')   
    total = five = two = fifty = quarter = dime = 0  #initializing 
    while coin != '-1':      #continue accepting input until -1
        if coin != '25' and coin != '50' and coin !='10':
            print('Please enter a valid coin value!')
            coin = input('Enter a coin! ')
            continue
        else:
            coin = int(coin)     #cast string input to an integer value
            total += coin        #continue totaling their coin entries
            coin = input('Enter a coin! ')
    dollars = int(total / 100)   #find the dollar part of value
    cents = total % 100          #find the remainder which is the coin (cent) value
    print('I can make change as:')
    if dollars >= 5:             #find the largest denomination and only print > 0 values
        five = int(dollars/5)
        dollars = dollars % 5
        print(five,'$5 bill')
    if dollars >=2:
        two = int(dollars/2)
        dollars = dollars % 2
        print(two,'$2 bill')
    if dollars >=1:
        print(dollars,'$1 bill')
    if cents >= 50:
        fifty = int(cents/50)
        cents = cents % 50
        print(fifty,'50 cent coin')
    if cents >= 25:
        quarter = int(cents/25)
        cents = cents % 25
        print(quarter,'25 cent coin')
    if cents >= 10:
        dime = int(cents/10) 
        print(dime,'10 cent coin')
#print the total amount entered by the user and only print > 0 values
    if int(total/100) > 0 and total%100 > 0:
        print('For a total of $',int(total/100),'dollars and',total%100,'cents')
    elif int(total/100) > 0:
        print('For a total of $',int(total/100),'dollars')
    else:
        print('For a total of',total%100,'cents')  


coin_sim()



'''Doing multiplication using only addition and recursion
    Naive version with b non-negative only
'''
def recProduct(a,b):
    if b >= 0:       #add a to result b times
        return a + recProduct(a, b-1) 
    else:
        return -a    #subtract an a for 0



print(recProduct(0,5))
print(recProduct(1,5))
print(recProduct(-1,5))
print(recProduct(3,4))


'''Doing multiplication using only addition and recursion
    Works for positive and/or negative values
'''
def recProduct2(a,b):
    if b >= 0:
        return a + recProduct(a, b-1)
    elif b < 0:      #if b is negative, subtract a from result b times
        return a - recProduct(a, abs(b-1)) 
    else:
        return -a



print(recProduct2(-5,-0))
print(recProduct2(-1,-5))
print(recProduct2(-1,5))
print(recProduct2(1,5))


'''Assuming user enters an integer in this solution
    User is guessing a random number 1-10 and program counts how many
    tries it takes user to guess correctly!
    '''
import random
r = random.randint(1,10)
u = int(input('Please enter a guess from 1-10'))
count = 1
while r != u:
    print('Your guess:',u)
    if 10 < u  or u < 1:
        u = int(input('Not valid!! Please enter an integer from 1-10'))
        continue
    else:
        count += 1
        if u < r:
            u = int(input('Not it! Your guess was too low. Guess again from 1-10'))
        else:
            u = int(input('Not it! Your guess was too high. Guess again from 1-10'))
print('You guessed correct! It was',r,'! You took', count, 'tries.')



# Second Solution with Exception Checking
'''User is guessing a random number 1-10 and program counts how many
    tries it takes user to guess correctly!
    '''
import random
r = random.randint(1,10)
u = None
def get_input():
    try:
        u = int(input('Please enter a guess from 1-10'))
        print('Your guess:',u)
        return u 
    except ValueError:
        print('Please enter only integers, not characters or decimals.')
        return None

while u == None:
    u = get_input()
    
count = 1
while r != u:
    if 10 < u  or u < 1:
        print('Not valid!!')
        u = get_input()
        continue
    else:
        count += 1
        if u < r:
            print('Not it! Your guess was too low. Guess again.')
            u = None
            while u == None:
                u = get_input()
        else:
            print('Not it! Your guess was too high. Guess again.')
            u = None
            while u == None:
                u = get_input()
print('You guessed correct! It was',r,'! You took', count, 'tries.')


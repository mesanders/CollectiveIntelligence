#!/usr/bin/env python

from math import sqrt

# Load Critics from text file

f = open("../resources/preferencesDataset", 'r')
critics = eval(f.read())
f.close()


# Testing the external data set.
def verifyExists():
    for i in critics:
        for x in critics[i]:
            print(i, ",", x,",", critics[i][x])



print("Test 1: " + repr(critics['Lisa Rose']['Lady in the Water']))
print("Test 2: " + repr(critics['Toby']))

### Calculate similarity score: Few ways 1) Euclidean Distance and Pearson Correlation
# Euclidean Distance is a simple score. It is pretty much a Chart
# To calculate the distance between two entities in a chart, take the difference in each axis,
# take the difference of the values then square them and add them together then take the square root of the sum
# Sum of Squares

# Example if one user rated a movie 4.5 and the other user rated it a 4 and another movie in commone one rated 1 and two rated it 2
diffMovie1 = 4.5 - 4
diffMovie2 = 1 - 2

#sum of squares will have a range and the lower the number the more similar where 0 is the most similar.
sumOfSquares = sqrt(pow(diffMovie1, 2) + pow(diffMovie2, 2))
print(sumOfSquares)
# This formula calculates the distance, which will be smaller for people who are more similar
# However if you want a function that gives higher value for people who are similar make it divisible by 1 and add 1
# The sumOfSquaresDiff changes the formula so that the values are always 0-1, 1 being higher
sumOfSquaresDiff = 1/(1 + sumOfSquares)
print(sumOfSquaresDiff)

# let's put this in a function:
# This returns the distance based similarity score for person1, and person2
def sim_distance(prefs, person1, person2):
    # Store list of shared items
    list_of_shared_items = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            list_of_shared_items[item] = 1

    # If they have no ratings in common, return 0
    if len(list_of_shared_items) == 0: return 0

    # Add up the squares of ALL the differences
    # This uses a list iteration at the end: for item in list_of_shared_items, and sums the results
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in list_of_shared_items])
    # The return takes the sum of the squares, and then we take the square root of the overall sums to get
    # the "OVERALL" similarity of two people. Each individual in the sum of squares can show how similar individual
    # movies between two people is then added together.
    return 1/(1 + sqrt(sum_of_squares))

### Calling the function just made with the list of critics and their movies that we loaded from file

print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
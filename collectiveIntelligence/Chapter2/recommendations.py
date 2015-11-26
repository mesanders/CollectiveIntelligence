#!/usr/bin/env python

from math import sqrt

# Load Critics from text file

f = open("../resources/preferencesDataset", 'r')
critics = eval(f.read())
f.close()


# Testing the external data set.
def get_critic_names():
    criticnames = []
    for i in critics:
        criticnames.append(i)

    return criticnames

criticnames = get_critic_names()

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
# The closer the result is to 1 the more similar the people are

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

#print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))

## Let's get all combination of pairs of people
def pairs_of_people(criticnames):
    # Nifty little list comprehension
    return [(criticnames[i], criticnames[k]) for i in range(0, len(criticnames) - 1) for k in range(i + 1, len(criticnames)) ]


combination_list = pairs_of_people(criticnames)

#for per1, per2 in combination_list:
    #print("person1: ", per1, "\t", "person2: ", per2, "\t", sim_distance(critics, per1, per2))

## Pearson Correlation Score
## The correlation coeficient is a measure of how well two sets of data fit on a straight line.
# Another aspect of Pearson score, is that it corrects for "grade inflation."
# The Euclidean distance score will say two critics are dissimilar because one might be consistently harsher than the other
# Pearson correlation on the other hand checks the similarity of the the line between how they rate movies. Instead
# of just based on the raw numbers, but how they rate movies compared to others.

def sim_pearson(critics, per1, per2):
    # Get list of mutually rated items into a dictionary, we are just using the dictionary for quick lookups. If we
    # Used a list it would become slow with a greater number of items. Therefore we set the mapped value to 1,
    list_of_items = {}
    # Go through all the movies that person 1 had seen that were seen by person 2
    for item in critics[per1]:
        if item in critics[per2]: list_of_items[item] = 1

    #Find the number of elements that are similar
    num_similar_items = len(list_of_items)

    if num_similar_items == 0: return 0

    # Add up all the preferences
    sum1 = sum([critics[per1][movie] for movie in list_of_items])
    sum2 = sum([critics[per2][movie] for movie in list_of_items])

    # Sum up the squares of each person for similar items
    sum_of_squares_person1 = sum([pow(critics[per1][movie], 2) for movie in list_of_items])
    sum_of_squares_person2 = sum([pow(critics[per2][movie], 2) for movie in list_of_items])

    # Next step is to get the product of the similar items between each person, then take the sum of those products
    product_sums = sum([critics[per1][movie] * critics[per2][movie] for movie in list_of_items])

    # The person score is the sum of the products minus the product of the individual sums, divided by the number of
    # movies that they have in common: which is the numerator, and then get the denomitator, which is the square root
    # of the product of the sum_of squares for each person - sum squared for that person, divided by the number of similar items
    step1 = product_sums - (sum1 * sum2/num_similar_items)
    step2 = sqrt((sum_of_squares_person1 - pow(sum1, 2)/num_similar_items)* (sum_of_squares_person2 - pow(sum2, 2) / num_similar_items))

    if step2 == 0: return 0

    # Divide step 1 by step 2 and that is the pearson score
    return step1/step2

print("\n\n")

# Test peaarson score between Lisa and Gene
print("Lisa Rose compared to Gene Seymour for the Euclidean Distance", sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
print("Lisa Rose compared to Gene Seymour for the Pearson Score", sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))


for per1, per2 in combination_list:
    print("EUCLIDEAN:", per1, "  and ", per2, "\t", sim_distance(critics, per1, per2))
    print("PEARSON SCORE:", per1, "  and  ", per2, "\t", sim_pearson(critics, per1, per2))
    pass


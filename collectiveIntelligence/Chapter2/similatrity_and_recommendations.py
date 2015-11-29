#!/usr/bin/env python

# One of the common constructs in this example is to use a dictionary.
# When using a dictionary you will see that the .setdefault method comes up.
# It will sect the dict[key] = default if the key is not already in the dictionary. This is good for initializing dictionaries in dictionaries.

# Similarity can be measured using multiple methods. The book gives two methods: Euclidean Distance and Pearson Correlation.
# The book notes that there are multiple methods that can be used, and it's up to the implementer. Other's include:
# Jaccard coefficient or Manhattan distance , as long as they have the same signature and return a float where higher is worth more.
#
# Read http://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples
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
#
# This method will return the result of -1 to 1. A value of 1 means, that people have exactly the same rating for
# Every item.
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

print()
# Test peaarson score between Lisa and Gene
print("Lisa Rose compared to Gene Seymour for the Euclidean Distance", sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
print("Lisa Rose compared to Gene Seymour for the Pearson Score", sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))
print()

def show_the_scores_compared_to_eachotehr():
    for per1, per2 in combination_list:
        print("EUCLIDEAN:", per1, "  and ", per2, "\t", sim_distance(critics, per1, per2))
        print("PEARSON SCORE:", per1, "  and  ", per2, "\t", sim_pearson(critics, per1, per2))
        pass



### Ranking Critics
## NOw that there is a function for comparing two people, the next function scores everyone against a given person and finds
# the closest match.

# Returns the best matches for person from the critics dictionary.
# Number of results and sim function are optional
# Returns the top similar critics to a specific person
def topMatches(critics, person, n=5, similarity=sim_pearson):
    scores = [(similarity(critics, person, other), other) for other in critics if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Prints the top matches to Toby and the score
print(topMatches(critics, 'Toby'))

### So far the functions just find people are related, the recommendations are by taking the similarity score multiplied
# By what they rated the item which will then give an estimation on what the first user would give the rating.

# Get recommendations for a person by using a weighted average of every other user's ratings
# The code loops through every other person in the critics dictionary. It calculates how similar they are to the pseron specified
# It then calculates how similar each other person is to the other person. It then goes through every item for which the other person scores.
# the final score of each item is calculated in the line "total[item+=critics[other_person][item]*sim" - The score for each
# item is multiplied by the similarity and these products are all added together. The scores are then normalized by dividing
# each of them by the similarity sum and sorted results are returned.
def getRecommendations(critics, person, similarity=sim_pearson):
    totals = {}
    similarity_sums = {}
    for other_person in critics:
        # make sure the other_person and person aren't the same
        if other_person == person: continue

        sim = similarity(critics, person, other_person)

        # ignore scores of zero or lower
        if sim <= 0: continue

        for item in critics[other_person]:
            # Only give scores for movies that person has not seen
            if item not in critics[person] or critics[person][item] == 0:
                # Similarity * Score -- or take the weight of the score
                totals.setdefault(item, 0)
                totals[item] += critics[other_person][item] * sim

                # sum of the similarities
                similarity_sums.setdefault(item, 0)
                similarity_sums[item] += sim

    # Create the normalized list
    rankings = [(total/similarity_sums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

print("")
print(getRecommendations(critics, 'Toby'))
print(getRecommendations(critics, "Michael Phillips"))


### It's possible to instead of finding people who are similar and recommend products for a given person,
### that you can find products that are to find movies that are similar based on how people rated them
### to do that the first thing you have to do is create a dictionary of movies, and who rated them instead of
### how people rated movies
def transformCriticsToMovies(critics):
    result = {}
    for person in critics:
        for item in critics[person]:
            result.setdefault(item, {})

            # Flib item and person
            result[item][person] = critics[person][item]
    return result

# Create a dictionary of movies
movies = transformCriticsToMovies(critics)
print(movies)
# The following reuses the same function, but takes in the name of the film in the second argument instead of
# the name of the person to compare to.
print(topMatches(movies, 'Superman Returns'))


## it's also possible to recommend critics for a movie:
print(getRecommendations(movies, 'Just My Luck'))

### Instead of "collaborative filtering" which is the use of people's opinions and preferences for recommendations
### one can also use item based filtering. Item-based filtering changes less often
def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other item they are most similar to.
    result = {}

    # INvert the preference matrix to be item-centric
    itemPrefs = transformCriticsToMovies(prefs)

    c = 0
    for item in itemPrefs:
        # status update for large datasets
        c+=1
        if c%100 == 0:
            print("%d / %d" % (c, len(itemPrefs)))

        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item)
        result[item] = scores

    return result

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSimilarity = {}

    # Loop over items rated by the user, and then loop over items similar to it, and weighted sum of the items that are similar
    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            if item2 in userRatings:
                continue

            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # Sum of all the similarities
            totalSimilarity.setdefault(item2, 0)
            totalSimilarity[item2] += similarity 

        # Divide each total score by the total weighting to get an average
    rankings = [(score/totalSimilarity[item], item) for item, score in scores.items()]


    # Return the rankings from higest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings

itemsim = calculateSimilarItems(critics)
print("Calculating similar items: \n\t" + str(itemsim))
print("\nCalculated Recommended items:\n\t", getRecommendedItems(critics, itemsim, 'Toby'))
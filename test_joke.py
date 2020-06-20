import pandas
import random

def test_joke():
    df = pandas.read_csv('jokes.csv')
    jokes_list = df.values.tolist()
    random_joke = random.choice(jokes_list)
    return random_joke[0]

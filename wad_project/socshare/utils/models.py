import random

def random_name():
    adj = [
        'Suspicious','Speedy','Small',
        'Adventurous','Funny','Silly',
        'Organised','Fluffy','Sad',
        'Lumpy','Soft','Crazy','Upset'
        ]
    animals = [
        'Rat','Koala','Seal','Otter',
        'Kangaroo','Cat','Panda','Dog',
        'Snake','Wolf','Zebra','Elephant',
        'Seagull','Rabbit','Horse','Bee'
    ]
    return ' '.join([random.choice(adj),random.choice(animals)])
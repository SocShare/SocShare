import random
import cfscrape

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

def decode_hexcodes(encoded):
    # Have to bypass SRC's weak email protection :)
    while '&' in encoded:
        loc = encoded.find('&')
        end = encoded.find(';')+1
        string = encoded[loc:end]
        encoded=encoded.replace(string,chr(int(string[2:-1])))
    return encoded

def find_encoded_email(html):
    # Unique string identifiers make this easy
    identify = 'Email: <a href="/cdn-cgi/l/email-protection#'
    html = html[html.find(identify):]
    html = html[html.find('">')+2:html.find('</a></span>')]
    return html

def compare_email(url, email):
    scraper = cfscrape.create_scraper()
    r = scraper.get(url)
    encoded = find_encoded_email(r.text)
    if email.lower() == decode_hexcodes(encoded).lower():
        return True
    return False
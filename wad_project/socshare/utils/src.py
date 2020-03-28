import cfscrape

def decode_hexcodes(encoded):
    # Have to bypass SRC's email spam protection
    while '&' in encoded:
        loc = encoded.find('&')
        end = encoded.find(';')+1
        string = encoded[loc:end]
        # Quick dirty method to replace the encoded hex
        encoded=encoded.replace(string,chr(int(string[2:-1])))
    return encoded

def find_encoded_email(html):
    # Unique string identifiers make this easy
    identify = 'Email: <a href="/cdn-cgi/l/email-protection#'
    # Simple parsing to isolate encoded email in the HTML
    html = html[html.find(identify):]
    html = html[html.find('">')+2:html.find('</a></span>')]
    return html

def search_for_url(scraper, email):
    r = scraper.get('https://www.glasgowstudent.net/?s='+email)
    search = '<a href="https://www.glasgowstudent.net/clubs/listings/'
    url = r.text[r.text.find(search)+9:]
    url = url[:url.find('">')]
    return url if 'https' in url else None

def check_email(email):
    # Bypass cloudflare checks using cfscrape
    scraper = cfscrape.create_scraper()
    url = search_for_url(scraper,email)
    if url==None: return False
    r = scraper.get(url)
    # If the email matches, then we're good to go
    if email.lower() == decode_hexcodes(find_encoded_email(r.text)).lower():
        return True
    return False
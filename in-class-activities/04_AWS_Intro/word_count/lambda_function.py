import requests

def get_desc_wc(isbn_list):
    '''
    Takes in a list of ISBNs and returns a list of description
    word counts corresponding to each ISBN (via the Google
    Books API).
    '''
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    wc_list = []
    for isbn in isbn_list:
        r = requests.get(url + isbn)
        data = r.json()
        # Try to get description, but if there is none, set
        # word count to be 0 for that book
        try:
            description = data['items'][0]['volumeInfo']['description']
            wc_list.append(len(description.split()))
        except KeyError:
            wc_list.append(0)
    return wc_list

def lambda_handler(event, context):
    wc = get_desc_wc(event['isbn'])
    return wc

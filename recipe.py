import requests
from bs4 import BeautifulSoup

base_url_edam = "https://api.edamam.com/search"
app_id = "9c45eaed"
app_key = "3af8be29d3ed887b660c9130fa78bf96"

def requestEdam(search_term):
    search_term = str(search_term)
    request_str = ("https://api.edamam.com/search?" + "app_id=" + app_id +
        "&app_key=" + app_key + "&q=" + search_term + "&from=0&to=1")
    print(request_str)
    r = requests.get(request_str)
    recipe_json = r.json()
    print(recipe_json["hits"][0]["recipe"]["url"])

if __name__ == "__main__":
    requestEdam("chicken")

import requests
from bs4 import BeautifulSoup

base_url = "http://forkthecookbook.com"
search_base_url = "http://forkthecookbook.com/search-recipes"

def get_recipe_URLs(search_term):
    links_list = []
    r = requests.get(search_base_url + "?q=" + search_term)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("a", {"class":"gallery-link"}, href=True)
    for i in range(len(soup)):
        links_list.append(soup[i]['href'])
    return links_list


if __name__ == "__main__":
    links_list = get_recipe_URLs("chicken")
    print(links_list)

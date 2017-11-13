import requests
from bs4 import BeautifulSoup

base_url = "http://forkthecookbook.com"
search_base_url = "http://forkthecookbook.com/search-recipes"
url = "http://www.forkthecookbook.com/recipes/braised-chicken-tomatoes-potatoes-peas-1bafa"

def get_recipe_names(search_term):
    names_list = []
    r = requests.get(search_base_url + "?q=" + search_term)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("a", {"class":"gallery-link"}, href=True)
    for i in range(len(soup)):
        names_list.append(soup[i].find("h2", {"class":"recipe-title"}).get_text())  
    return names_list

def get_recipe_URLs(search_term):
    links_list = []
    r = requests.get(search_base_url + "?q=" + search_term)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("a", {"class":"gallery-link"}, href=True)  #<a href="/recipes/braised-chicken-tomatoes-potatoes-peas-1bafa" class="recipe-listing-item gallery-link">
    for i in range(len(soup)):  
        links_list.append(base_url+soup[i]['href'])
    return links_list

def get_recipe_ingredients(url):
    ingredients_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all({"class":"recipe-ingredients"}, href=True)
    for i in range(len(soup)):
        ingredients_list.append(soup[i].find("td", {"class":"recipe-ingredients"}).get(text))
    return ingredients_list

def get_recipe_instructions(url)



if __name__ == "__main__":
    links_list = get_recipe_URLs("chicken")
    print(links_list)
    names_list = get_recipe_names("chicken")
    print(names_list)
    #ingredients_list = get_recipe_ingredients("chicken")
    #print(ingredients_list)


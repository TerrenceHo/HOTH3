import requests
from bs4 import BeautifulSoup

base_url = "http://forkthecookbook.com"
search_base_url = "http://forkthecookbook.com/search-recipes"
specific_url = "http://www.forkthecookbook.com/recipes/chicago-pizza-burgers-eac03"

def get_recipe_names(search_term):
    names_list = []
    r = requests.get(search_base_url + "?q=" + search_term)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("a", {"class":"gallery-link"}, href=True)
    for i in range(len(soup)):
        names_list.append(soup[i].find("h2", {"class":"recipe-title"}).get_text())  
    return names_list

def get_single_recipe_name(specific_url):
    name = ""
    r = requests.get(specific_url)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.find("title").get_text()

    name=name.split("|")[0]
    print (name)
    return name

def get_recipe_URLs(search_term):
    links_list = []
    r = requests.get(search_base_url + "?q=" + search_term)
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("a", {"class":"gallery-link"}, href=True)  #<a href="/recipes/braised-chicken-tomatoes-potatoes-peas-1bafa" class="recipe-listing-item gallery-link">
    for i in range(len(soup)):  
        links_list.append(base_url+soup[i]['href'])
    return links_list

def get_data(specific_url):
    ingredients_list = []
    instructions_list = []
    r = requests.get(specific_url)
    soup = BeautifulSoup(r.text, "html.parser")

    ingredients_list = soup.find_all("td", class_="recipe-ingredients")
    for i in range(len(ingredients_list)):
        ingredients_list[i] = " ".join(ingredients_list[i].get_text().strip().split())
    
    instructions_list = soup.find("td", class_="recipe-instructions").find_all("li")
    for i in range(len(instructions_list)):
        instructions_list[i] = " ".join(instructions_list[i].get_text().strip().split())    #size of 1

    return ingredients_list, instructions_list

if __name__ == "__main__":
    #links_list = get_recipe_URLs("chicken")
    #print(links_list)
    #names_list = get_recipe_names("chicken")
    #print(names_list)
    ingredients_list, instructions_list = get_data(specific_url)

    print(ingredients_list)

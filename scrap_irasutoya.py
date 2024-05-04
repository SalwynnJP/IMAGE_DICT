from bs4 import BeautifulSoup as bs
import requests
import json
import re
from tqdm import tqdm

# Define the URL to scrape
url_de_base = "https://www.irasutoya.com/"

def soup_creation(url):
    """
    Returns the BeautifulSoup analysis of an HTML page (its soup)

    Args:
        url (str): Link to the page to be scraped

    Returns:
        soup : Soup of the scraped page
    """
    # Download the page
    response = requests.get(url)
    # Get the HTML of the downloaded response
    html = response.content
    # Analyze the HTML with "lxml" lexical and grammar analyzer
    return bs(html, "lxml")

def get_main_page_all_links(soup):
    """
    Analyzes the main page of the site and retrieves all available theme links

    Args:
        soup (html): Soup of the scraped page

    Returns:
        list : List of all scraped links on the page
    """
    links = soup.find_all("div", id="section_banner")
    lst_of_links = []

    for link in links:
        for link_of_link in link.find_all('a'):
            lst_of_links.append(link_of_link.get('href'))
    return lst_of_links

def get_sub_page_all_links(soup):
    """
    Analyzes the sub page of the site and retrieves all available sub-theme links

    Args:
        soup (html): Soup of the scraped page

    Returns:
        list : List of all scraped links on the sub-page
    """
    links = soup.find_all("div", id="banners")
    lst_of_links = []

    for link in links:
        for link_of_link in link.find_all('a'):
            lst_of_links.append(link_of_link.get('href'))
    return lst_of_links

def next_page(soup):
    """
    Function which allows to get the link to the next page if it exists

    Args:
        soup (html): Soup of the scraped page

    Returns:
        str or None : String of the link to the next page if it exists
    """
    try:
        link_next_page = soup.find('div', id='page_link').find_all("a")[-2].get('href')
        return link_next_page
    except:
        return None

def recup_data(soup, main_dic) -> None:
    """
    Collecting useful data and creating a dictionary to handle them

    Args:
        soup (html): Soup of the scraped page

    Returns:
        dict_of_data : dictionary of the scraped data
    """
    all_data = soup.find_all('div', class_='boxim')

    for data in tqdm(all_data, desc="Extracting data"):
        script_content = data.find('a').script

        # Using regular expressions to extract the link and text
        match = re.search(r'bp_thumbnail_resize\("(.*?)","(.*?)"\)', script_content.string)

        if match:
            image_link = match.group(1)
            image_text = match.group(2).split('&')[0].split('のイラスト')[0]

            if image_link and image_text:
                main_dic[image_text] = {}
                main_dic[image_text]['img_url'] = image_link
                main_dic[image_text]['description'] = image_text

def append_to_json(data_to_append, json_file_path):
    """
    Ajoute des données à un fichier JSON existant.

    Args:
    - data_to_append (dict): Les données à ajouter au fichier JSON.
    - json_file_path (str): Le chemin vers le fichier JSON existant.
    """
    # Écrit les données mises à jour dans le fichier JSON
    with open(json_file_path, 'a+') as json_file:
        json.dump(data_to_append, json_file, indent=4, ensure_ascii=False)

def scrap_page(url, main_dic):
    """
    This function scrapes the given URL and saves the data in a JSON file.

    Parameters:
    url (str): The URL of the page to scrape.
    file_name (str): The name of the JSON file to save the data in.

    Returns:
    None
    """

    # Create soup for the current page
    actual_page = soup_creation(url)

    # Scrape the current page
    recup_data(actual_page, main_dic)
    
    # Get the next page to analyze if it exists
    next_page_url = next_page(actual_page)

    # Recursion of the function if the next page exists
    if next_page_url is not None:
        scrap_page(next_page_url, main_dic)

def main(url_de_base, file_name):
    '''
    Collects all links to sub-pages, then retrieves images + descriptions from all sub-sub-pages,
    then navigates between them until the last one before reiterating the process

    Args:
        file_name (str): Raw filename without extension
        data (list): List of links
    '''

    # Create soup for the current page
    main_page = soup_creation(url_de_base)

    # Retrieve all desired links from the current page
    links_theme = get_main_page_all_links(main_page)
    
    # Creation of the main_dic that will keep all the data in it
    main_dic = {}

    for part_of_link in links_theme:
        if part_of_link.startswith("/p/"):
            
            try :
                # Create soup for the theme page
                page_theme = soup_creation(url_de_base + part_of_link)
                links_sub_theme = get_sub_page_all_links(page_theme)

                for sub_link in links_sub_theme:
                    # Create soup for the sub-theme page
                    scrap_page(sub_link, main_dic)
                    
            except:
                continue
            
            
    
                
    append_to_json(main_dic, file_name)
            

if __name__ == '__main__':
    main(url_de_base, 'data_collection/irasutoya_kana_bis.json')
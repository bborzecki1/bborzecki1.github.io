import re
import requests
from bs4 import BeautifulSoup

def get_tiktokers_data():
    response = requests.get('https://www.favikon.com/blog/the-20-most-famous-tiktok-influencers-in-the-world')
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('div', class_="rich-text-2 tablecontent w-richtext")
    tiktokers = container.find_all('a', limit=10)
    tiktokers_data = []
    for tiktoker in tiktokers:
        name = tiktoker.getText()
        tiktokers_data.append(name)
    return tiktokers_data

def format_tiktoker_name(name):
    name = name.split(". ")[1].split(" - ")[0]
    name = name.replace(" ", "_")
    name = name.replace("’", "%27")
    return name

def generate_markdown_file(tiktokers_data, output_file):
    with open(f"{output_file}.md", 'w', encoding='utf-8') as file:
        file.write("""---
layout: post
title:  "Top 10 Tiktokers in 2022"
date:   2024-03-16 18:22:17 +0100
categories: jekyll 
permalink: /tiktokers
---

# Welcome to the page dedicated to the most influential and popular individuals on the TikTok platform in 2022. TikTok has become a social media phenomenon, allowing users to share short video clips that often go viral and amass millions of followers worldwide.

# Below, you'll find a list of the top ten most well-known TikTokers in 2022, along with their follower counts. Each of them has a significant impact on the TikTok community, constantly creating content that engages and inspires millions of people around the globe.

""")
        for name in tiktokers_data:
            clear_name = format_tiktoker_name(name)
            url = f"/tiktokers/{clear_name}"
            generate_markdown_subfile(clear_name)
            file.write(f"## [{name}]({url})\n\n")

def generate_markdown_subfile(output_name):
    name = output_name.replace( "%27","’")
    with open(f"{name}.md", 'w', encoding='utf-8') as file:
        file.write(f"""---
layout: page
permalink: /tiktokers/{output_name}/
---
### {name.replace("_"," ")}
\n
{get_wiki_photo(output_name)} \n
{get_wiki_data(output_name)}
""")

def get_wiki_data(clear_name):
    url = f"https://en.wikipedia.org/wiki/{clear_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('div', class_="mw-content-ltr mw-parser-output")
    paragraph = container.find_all('p')[1].get_text()
    paragraph = re.sub(r"\[\d+\]", "", paragraph)
    return paragraph

def get_wiki_photo(clear_name):
    url = f"https://en.wikipedia.org/wiki/{clear_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('a', class_="mw-file-description")
    photo = container.find('img').get('src')
    img_tag = f'<img src="{photo}">'
    return img_tag


output_file = "2024-03-16-tiktokers"
tiktokers_data = get_tiktokers_data()
generate_markdown_file(tiktokers_data, output_file)

print("Plik Markdown został wygenerowany.")





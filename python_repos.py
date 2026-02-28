import requests
import plotly.express as px 
import textwrap


url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"

headers = {"accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"status code: {r.status_code}")

response_dict = r.json()
print(f"Complete results: {not response_dict['incomplete_results']}")
repo_dicts = response_dict['items']
repo_names, repo_links, stars, hover_texts = [], [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict['name']
    repo_names.append(repo_dict['name'])
    star=repo_dict['stargazers_count']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"  
    repo_links.append(repo_link)   
    stars.append(repo_dict['stargazers_count'])
    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    if description:
        disc = textwrap.wrap(description, width=50, max_lines=5)
        better_disc='<br />'.join(disc)
        hover_text = f"Name:{repo_name}<br />Owner:{owner}<br />Description:{better_disc}<br />Stars:{star}"
    else:
        hover_text = f"Name:{repo_name}<br />Owner:{owner}<br />Description:No description from the owner<br />Stars:{star}"
    
    hover_texts.append(hover_text)
title = "Most starred Python projects on GitHub"
labels = {'x': 'Repository', 'y':'Stars'}
fig = px.bar(x=repo_links, y=stars, title = title, labels=labels)
fig.update_layout(title_font_size = 28, xaxis_title_font_size=20, yaxis_title_font_size=20)
fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6,
                  hoverinfo='text',hovertext=hover_texts,
                  hovertemplate="%{hovertext}<extra></extra>")
fig.show()
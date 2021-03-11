import json
from joblinks import *
import PySimpleGUI as sg

"""
Joblinks Browser

Install python packages:
pip install -r requirements.txt
"""


def build_catalogue_tree(treedata, cat):
    for site in cat:
        treedata.Insert('', site, site, values=[len(cat[site])])
        for ad_dict in cat[site]:
            ad_title = ad_dict['headline'] + "\n" + ad_dict['employer']
            treedata.Insert(site, ad_dict['url'], ad_title,  values=[ad_dict['municipality']])
            treedata.Insert(ad_dict['url'], ad_dict['url'] + '-thisurl', ad_dict['url'], values=[ad_dict['employer']])
            for i in range(len(ad_dict['other_urls'])):
                treedata.Insert(ad_dict['url'], ad_dict['url'] + f'-child{i}', ad_dict['other_urls'][i], values=[])


# Query dialog popup
layout = [  [sg.Text('Query'), sg.InputText(default_text='Python', key='-INPUT-')],
            [sg.Checkbox('Prefer loading from saved JSON file', default=True, key='-CHECK1-')],
            [sg.Checkbox('Only show ads with multiple links', default=True, key='-CHECK2-')],
            [sg.OK()]]
window = sg.Window('Make query', layout)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'OK'):
        break
window.close()
del window

# User dialog choices
query = values['-INPUT-']
try_using_file = values['-CHECK1-']
only_show_multihits = values['-CHECK2-']

# Get ads
file_suffix = " multihits" if only_show_multihits else ""
json_filename = query.lower() + " " + f"catalogue{file_suffix}.json";
if try_using_file:
    try:
        f = open(json_filename, "r", encoding="utf-8")
        cat = json.load(f)
        f.close()
    except:
        try_using_file = False

if not try_using_file:
    if only_show_multihits:
        cat = get_ads_catalogue_only_multihits(query)
    else:
        cat = get_ads_catalogue(query)


# Build Tree View
treedata = sg.TreeData()
build_catalogue_tree(treedata, cat)
layout = [[sg.Text(f"Query = {query}")],
          [sg.Tree(data=treedata,
                   headings=['          ', ],
                   auto_size_columns=True,
                   num_rows=25,
                   col0_width=120,
                   key='-TREE-',
                   show_expanded=False,
                   enable_events=True,
                   justification="left"),
           ],
          [sg.Button('Close')]]
window = sg.Window('Joblinks Browser', layout)

while True:     # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Close'):
        break
    # print(event, values)
window.close()

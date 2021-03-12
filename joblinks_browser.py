import json
from joblinks import *
import PySimpleGUI as sg

"""
Joblinks Browser

Installation:
1. pip install -r requirements.txt
2. Set URL in joblinks.py
"""


def query_dialog_popup():
    layout = [[sg.Text('Query'), sg.InputText(default_text='Python', key='-INPUT-')],
              [sg.Checkbox('Prefer loading from saved JSON file', default=True, key='-CHECK1-')],
              [sg.Checkbox('Only show ads with multiple links', default=False, key='-CHECK2-')],
              [sg.OK()]]
    window = sg.Window('Make query', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            break
    window.close()
    del window
    if event == sg.WIN_CLOSED:
        exit()
    return values['-INPUT-'], values['-CHECK1-'], values['-CHECK2-']


def get_ads(query, try_using_file, only_show_multihits):
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
    return cat


def filter_by_municipality(cat, municip):
    filtered_cat = {}
    for site in cat:
        filtered_cat[site] = []
        for ad_dict in cat[site]:
            if municip in ad_dict['municipality']:
                filtered_cat[site].append(ad_dict)
    return filtered_cat


def build_catalogue_tree(treedata, cat, municip):
    if municip != '':
        cat = filter_by_municipality(cat, municip)
    for site in cat:
        treedata.Insert('', site, site, values=[len(cat[site])])
        for ad_dict in cat[site]:
            this_municip = ad_dict['municipality'][0] if municip == '' else municip
            treedata.Insert(site, ad_dict['url'], ad_dict['headline'],  values=[this_municip])
            treedata.Insert(ad_dict['url'], ad_dict['url'] + '-thisurl', ad_dict['url'], values=[ad_dict['employer']])
            for i in range(len(ad_dict['other_urls'])):
                treedata.Insert(ad_dict['url'], ad_dict['url'] + f'-child{i}', ad_dict['other_urls'][i], values=[])


def catalogue_tree_view(cat, municip):
    treedata = sg.TreeData()
    build_catalogue_tree(treedata, cat, municip)
    layout = [[sg.Text(f"Query = {query}")],
              [sg.Text('Filter by municipality'),
               sg.InputText(default_text=municip, key='-FILTER-'),
               sg.Button('Relaunch')],
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
              [sg.Button('End')]]
    window = sg.Window('Joblinks Browser', layout)
    while True:     # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'End', 'Relaunch'):
            break
    window.close()
    del window
    return event in (sg.WIN_CLOSED, 'End'), values['-FILTER-']


# User dialog choices
query, try_using_file, only_show_multihits = query_dialog_popup()

catalogue = get_ads(query, try_using_file, only_show_multihits)

municipality = ''
finished = False
while not finished:
    finished, municipality = catalogue_tree_view(catalogue, municipality)

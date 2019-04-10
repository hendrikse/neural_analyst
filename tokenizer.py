import difflib
import re

def prepaire_data(html_str):
    token_list = html_str.lower().replace('<', ' <')
    token_list = token_list.replace('>', '> ')
    token_list = token_list.replace(' />', '/>')
    token_list = token_list.replace('/>', '/> ')
    token_list = token_list.replace('\n', ' ')
    token_list = token_list.replace('\t', ' ')
    token_list = re.split(' +', token_list)
    return token_list


def html_diff(html_path_1, html_path_2):
    f = open(html_path_1, "r")
    origin_html = f.read()
    f.close()
    f = open(html_path_2, "r")
    mod_html= f.read()
    f.close()
    origin_html = prepaire_data(origin_html)
    mod_html = prepaire_data(mod_html)
    diff = difflib.ndiff(origin_html, mod_html)
    delta = list()
    for line in diff:
        if line.startswith('+'):
            delta.append(line.replace("+ ", ""))
    return delta



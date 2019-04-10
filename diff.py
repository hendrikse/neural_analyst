import difflib
import re

def prepaireData(html_str):
    token_list = html_str.lower().replace('<', ' <')
    token_list = token_list.replace('>', '> ')
    token_list = token_list.replace(' />', '/>')
    token_list = token_list.replace('/>', '/> ')
    token_list = token_list.replace('\n', ' ')
    token_list = token_list.replace('\t', ' ')
    token_list = re.split(' +', token_list)
    return token_list

f = open("html_orig", "r")
text_A= f.read()
f.close()
f = open("HTML_mod", "r")
text_B= f.read()
f.close()

#delta = difflib.Differ().compare(text_A.splitlines(), text_B.splitlines())

#case_a = 'afrykbnerskojęzyczny'
#case_b = 'afrykanerskojęzycznym'

#output_list = [li for li in difflib.ndiff(text_A, text_B) if li[0] != ' ']

text_A = prepaireData(text_A)
text_B = prepaireData(text_B)
diff = difflib.ndiff(text_A, text_B)
delta = list()
for line in diff:
    if line.startswith('+'):
        delta.append(line.replace("+ ", ""))

print(delta)
#print("".join(diff))
#print('\n'.join(diff))
#print(diff)



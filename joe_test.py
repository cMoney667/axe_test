import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
import time
import requests
from lxml import etree
import sys

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

xmlDict = []

print("Please paste in the link to xml sitemap")
url = input()
r = requests.get(url)
root = etree.fromstring(r.content)

toolbar_width = len(root)
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width + 1))

print(f'The number of sitemap tags are {len(root)}')
print('Select folder name')
foldername = input()
printProgressBar(0, toolbar_width, prefix='Progress:', suffix='Complete', length= 50)
for sitemap in root:
    children = sitemap.getchildren()
    url = children[0].text
    if '#' in url:
        url = url.replace('#', '')
    xmlDict.append(url)

for i, target in enumerate(xmlDict, start=0):
    if 'https://' in target:
        no_http_target = target.lstrip('https://')
    elif 'http://' in target:
        no_http_target = target.lstrip('http://')
    else:
        no_http_target = target
    if no_http_target.endswith('/'):
        t_filename = no_http_target.rstrip('/')
    else:
        t_filename = no_http_target.replace("/", "_")

    if '.' in t_filename:
        no_dot_filename = t_filename.replace('.', '_')
    else:
        no_dot_filename = t_filename

    if not os.path.exists(foldername):
        os.makedirs(foldername)
    target_file = open(f'{foldername}/{no_dot_filename}-a11y.txt', 'w+')
    target_file.write(f'Page tested: {target}\n')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    # print(target)
    driver.get(target)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    # print(results)
    for result in results["violations"]:
        target_file.write(f'\n\nDescription:\n{result["description"]} -- {len(result["nodes"])}\n')
        target_file.write(f'Help URL: \n{result["helpUrl"]}\n')
        # target_file.write(f'{result}')
    driver.close()
    printProgressBar(i + 1, toolbar_width, prefix='Progress:', suffix='Complete', length=toolbar_width)
#     sys.stdout.write("-")
#     sys.stdout.flush()
# sys.stdout.write("]\n")

# print('Enter the site you would like to test')
# target = input().strip()
# print('Select folder name')
# foldername = input()
# print('Enter template name')
# templateName = input()

# if 'https://' in target:
#     no_http_target = target.lstrip('https://')
# elif 'http://' in target:
#     no_http_target = target.lstrip('http://')
# else:
#     no_http_target = target
# if no_http_target.endswith('/'):
#     t_filename = no_http_target.rstrip('/')
# else:
#     t_filename = no_http_target.replace("/", "_")

# if '.' in t_filename:
#     no_dot_filename = t_filename.replace('.', '_')
# else:
#     no_dot_filename = t_filename

# if not os.path.exists(foldername):
#     os.makedirs(foldername)
# target_file = open(f'{foldername}/{no_dot_filename}-a11y.txt', 'w+')
# target_file.write(f'Page tested: {target}\n')
# target_file.write(f'Template:{templateName}\n')

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
# # print(target)
# driver.get(target)
# axe = Axe(driver)
# axe.inject()
# results = axe.run()
# # print(results)
# for result in results["violations"]:
#     target_file.write(f'\n\nDescription:\n{result["description"]} -- {len(result["nodes"])}\n')
#     target_file.write(f'Help URL: \n{result["helpUrl"]}\n')
#     target_file.write(f'{result}')
# driver.close()

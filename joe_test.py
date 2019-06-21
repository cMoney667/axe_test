import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
import time

print('Enter the site you would like to test')
target = input().strip()
print('Select folder name')
foldername = input()
print('Enter template name')
templateName = input()

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
target_file = open(f'{foldername}/{no_dot_filename}-a11y.txt', 'w')
target_file.write(f'Page tested: {target}\n')
target_file.write(f'Template:{templateName}\n')

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# print(target)
driver.get(target)
axe = Axe(driver)
axe.inject()
results = axe.run()
for result in results["violations"]:
  target_file.write(f'\n\nDescription:\n{result["description"]} - {len(result["nodes"])}\n')
  target_file.write(f'Help URL: \n{result["helpUrl"]}\n')
driver.close()

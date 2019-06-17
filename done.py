import os

print('Please select the folder')
foldername = input()
done_file = open(f'{foldername}/{foldername}-adascan.docx', 'w')
print('What is the citys name?')
city_name = input()
done_file.write(f"{city_name.title()} - ADA Scan\n\n")
for filename in os.listdir(foldername):
  with open(foldername+'/'+filename, 'r') as f:
    for line in f.readlines():
      done_file.write(line)
  done_file.write('\n\n-------------------------------------------------------\n\n')
done_file.write('\n\n\nTime to Complete 5-8 Hours')
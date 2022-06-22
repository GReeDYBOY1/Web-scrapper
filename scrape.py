# Jimmy
import requests
from bs4 import BeautifulSoup as bss4
import csv
from itertools import zip_longest
import math

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

students = []
id_numbers = []
degrees = []
links = []
percentage = []

for i in range(33223001, 33223096):
    print ("****" , i , "******")
    if requests.get(f"http://app1.helwan.edu.eg/EngHelwan/HasasnUplist.asp?z_dep=%3D&z_gro=%3D&z_st_settingno=%3D&x_gro=%C7%E1%CB%C7%E1%CB%C9&x_dep=%E5%E4%CF%D3%C9+%C7%E1%C7%E1%DF%CA%D1%E6%E4%ED%C7%CA+%E6%C7%E1%C7%CA%D5%C7%E1%C7%CA+%E6%C7%E1%CD%C7%D3%C8%C7%CA&z_st_name=LIKE&x_st_name=&x_st_settingno={i}&Submit=++++%C8%CD%CB++++") is not None :
        url = requests.get(f"http://app1.helwan.edu.eg/EngHelwan/HasasnUplist.asp?z_dep=%3D&z_gro=%3D&z_st_settingno=%3D&x_gro=%C7%E1%CB%C7%E1%CB%C9&x_dep=%E5%E4%CF%D3%C9+%C7%E1%C7%E1%DF%CA%D1%E6%E4%ED%C7%CA+%E6%C7%E1%C7%CA%D5%C7%E1%C7%CA+%E6%C7%E1%CD%C7%D3%C8%C7%CA&z_st_name=LIKE&x_st_name=&x_st_settingno={i}&Submit=++++%C8%CD%CB++++")
        url.encoding = 'windows-1256'
        soup = bss4(url.text, 'lxml')

        if soup.find("tr", {"class": "ewTableRow"}) is not None:
            link = soup.find("tr", {"class": "ewTableRow"}).find("a").attrs['href']
            link_natiga = "http://app1.helwan.edu.eg/EngHelwan/" + link
            links.append(link_natiga)

print ("\n")
for i , l in enumerate(links):
    url = requests.get(l)
    url.encoding = 'windows-1256'
    soup = bss4(url.text, 'lxml')
    tables = soup.findAll("table", {"width": "1000"})
    table1 = tables[0]
    rows = table1.findAll("font", {"face": "Traditional Arabic", "size": "5"})
    name = rows[3]
    #print(name.text)
    students.append(name.text)
    id = rows[5].text
    #print(id)
    id_numbers.append(id)
    table2 = tables[1]
    rows2 = table2.findAll("font", {"size": "4"})

    total = 0
    index = [3,7,11,19,27,43,51,59,67,75]
    for b in index:
        if (rows2[b].text.strip() != ""):
            total += int(rows2[b].text.strip())

    degrees.append(total)
    percent = truncate(((total / 1500) * 100), 2)
    percentage.append(percent)

    print(i+1,"-" ,students[i], " : ", rows2[3].text.strip(), rows2[11].text.strip(), rows2[19].text.strip(),
          rows2[27].text.strip(),rows2[43].text.strip(),rows2[51].text.strip(),rows2[59].text.strip(),rows2[67].text.strip(),rows2[75].text.strip(),
          rows2[7].text.strip(), "-----> ",total, "-----> ", percent , "%")

student_row = [students, id_numbers, degrees, percentage]
exported = zip_longest(*student_row)

with open('tessst.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['اسم الطالب', 'رقم الجلوس', 'المجموع' ,'النسبة المئوية'])
    writer.writerows(exported)
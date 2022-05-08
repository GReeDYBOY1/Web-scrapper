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

for i in range(32220001, 32220291):
    print ("****" , i , "******")
    if requests.get(f"http://app1.helwan.edu.eg/EngHelwan/HasasnUplist.asp?z_dep=%3D&z_gro=%3D&z_st_settingno=%3D&x_gro=%C7%E1%CB%C7%E1%CB%C9&x_dep=%E5%E4%CF%D3%C9+%C7%E1%DE%E6%EC+%E6%C7%E1%C7%E1%C7%CA+%C7%E1%DF%E5%D1%C8%ED%C9&z_st_name=LIKE&x_st_name=&x_st_settingno={i}&Submit=++++%C8%CD%CB++++") is not None :
        url = requests.get(f"http://app1.helwan.edu.eg/EngHelwan/HasasnUplist.asp?z_dep=%3D&z_gro=%3D&z_st_settingno=%3D&x_gro=%C7%E1%CB%C7%E1%CB%C9&x_dep=%E5%E4%CF%D3%C9+%C7%E1%DE%E6%EC+%E6%C7%E1%C7%E1%C7%CA+%C7%E1%DF%E5%D1%C8%ED%C9&z_st_name=LIKE&x_st_name=&x_st_settingno={i}&Submit=++++%C8%CD%CB++++")
        url.encoding = 'windows-1256'
        soup = bss4(url.text, 'lxml')

        if soup.find("tr", {"class": "ewTableRow"}) is not None:
            link = soup.find("tr", {"class": "ewTableRow"}).find("a").attrs['href']
            link_natiga = "http://app1.helwan.edu.eg/EngHelwan/" + link
            links.append(link_natiga)
        # else :
        #     url = requests.get(f"http://app1.helwan.edu.eg/EngHelwan/HasasnUplist.asp?z_dep=%3D&z_gro=%3D&z_st_settingno=%3D&x_gro=%C7%E1%CB%C7%E1%CB%C9&x_dep=%E5%E4%CF%D3%C9+%C7%E1%DE%E6%EC+%E6%C7%E1%C7%E1%C7%CA+%C7%E1%DF%E5%D1%C8%ED%C9&z_st_name=LIKE&x_st_name=%E3&x_st_settingno={i}&Submit=++++%C8%CD%CB++++")
        #     url.encoding = 'windows-1256'
        #     soup = bss4(url.text, 'lxml')
        #     link = soup.find("tr", {"class": "ewTableRow"}).find("a").attrs['href']
        #     link_natiga = "http://app1.helwan.edu.eg/EngHelwan/" + link
        #     links.append(link_natiga)

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
    if (rows2[3].text.strip() != ""):
        total += int(rows2[3].text.strip())
    if (rows2[11].text.strip() != ""):
        total += int(rows2[11].text.strip())
    if (rows2[19].text.strip() != ""):
        total += int(rows2[19].text.strip())
    if (rows2[27].text.strip() != ""):
        total += int(rows2[27].text.strip())

    #total = int(rows2[3].text.strip()) + int(rows2[11].text.strip()) + int(rows2[19].text.strip()) + int(rows2[27].text.strip())
    #print(total)
    degrees.append(total)
    percent = truncate(((total / 650) * 100), 2)
    percentage.append(percent)
    # print ("************************   " ,  i  , "   ************************")
    print(i+1,"-" ,students[i], " : ", rows2[3].text.strip(), rows2[11].text.strip(), rows2[19].text.strip(),
          rows2[27].text.strip()
          , "-----> ", percent , "%")
student_row = [students, id_numbers, degrees, percentage]
exported = zip_longest(*student_row)

with open('final.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['اسم الطالب', 'رقم الجلوس', 'المجموع' ,'النسبة المئوية'])
    writer.writerows(exported)
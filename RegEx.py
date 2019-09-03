from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

list_lastname = []
list_firstname = []
list_surname = []
list_organization = []
list_position = []
list_phone = []
list_phone_add = []
list_email = []
list_header = [['lastname','firstname','surname','organization','position','phone','email']]

for item in contacts_list:
  if item != list_header[0]:
    list_organization.append(item[3])
    list_position.append(item[4])
    list_email.append(item[6])
    str_contacts = ','.join(item)
    pattern = re.compile("[А-Я][а-я]+")
    res = pattern.findall(str_contacts)

    if len(res) != 0:
      list_lastname.append(res[0])
      list_firstname.append(res[1])
      if len(res) >= 3:
        list_surname.append(res[2])
      else:
        list_surname.append('')

    pattern = re.compile("[+]*\d+[ ]*[(]*\d+[)]*[ -]*\d+[-]*\d+[-]*\d+")
    res = pattern.findall(str_contacts)
    str_item = ''
    if res != []:
      for item in res[0]:
        if item not in "+ ()-":
          str_item += item
      tele = '+7'+'('+str_item[1:4]+')'+str_item[4:7]+'-'+str_item[7:9]+'-'+str_item[9:]
      list_phone.append(tele)
    else:
      list_phone.append('')

    pattern = re.compile("доб. \d+")
    add = pattern.findall(str_contacts)
    if add != []:
      list_phone_add.append(' '+add[0])
    else:
      list_phone_add.append('')
list_telephone = [list_phone[i] + list_phone_add[i] for i in range(0, len(list_phone))]

contacts_list_2 = []
for item in range(0, len(list_lastname)):
  contacts_list_2.append([list_lastname[item], list_firstname[item], list_surname[item], list_organization[item], list_position[item], list_telephone[item], list_email[item]])
list_num = []
list_double = []
for item in range(0, len(contacts_list_2)):
  for i in range(1, len(contacts_list_2)-item):
    if (contacts_list_2[item][0] == contacts_list_2[item+i][0]) and (contacts_list_2[item][1] == contacts_list_2[item+i][1]):

      list_1 = []
      
      for n in range(0, len(contacts_list_2[item])):

        if contacts_list_2[item][n] == contacts_list_2[item+i][n]:
          list_1.append(contacts_list_2[item][n])
        elif contacts_list_2[item][n] != '':
          list_1.append(contacts_list_2[item][n])
        elif contacts_list_2[item+i][n] != '':
          list_1.append(contacts_list_2[item+i][n])
        else:
          list_1.append(contacts_list_2[item][n])
      list_double.append(list_1)
      list_num.append([item, item+i])

contacts_list_3 = []
for item in range(0, len(contacts_list_2)):
  if item not in sum(list_num, []):
    contacts_list_3.append(contacts_list_2[item])
contacts_list = list_header+contacts_list_3+list_double
pprint(list_header+contacts_list_3+list_double)

with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list)

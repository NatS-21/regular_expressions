from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
contacts = contacts_list[1:]

def normalize_phone(phone):
    pattern = re.compile(
        r"(\+7|8)?\s*\(?(\d{3})\)?[\s\-]*"
        r"(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})"
        r"(?:\s*\(?(доб\.?)\s*(\d+)\)?)?"
    )
    
    result = pattern.sub(
        lambda m: f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
                  + (f" доб.{m.group(7)}" if m.group(7) else ""),
        phone
    )
    
    return result


new_contacts = []

for contact in contacts:
    
    fio = " ".join(contact[:3]).split(" ")
    
    lastname = fio[0] if len(fio) > 0 else ""
    firstname = fio[1] if len(fio) > 1 else ""
    surname = fio[2] if len(fio) > 2 else ""
    
    contact[0] = lastname
    contact[1] = firstname
    contact[2] = surname
    
    contact[5] = normalize_phone(contact[5])
    
    new_contacts.append(contact)


contacts_dict = {}

for contact in new_contacts:
    key = (contact[0], contact[1])
    
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        
        for i in range(len(existing)):
            if existing[i] == "" and contact[i] != "":
                existing[i] = contact[i]


contacts_list = [header] + list(contacts_dict.values())

pprint(contacts_list)


with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

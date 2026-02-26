from pprint import pprint
import csv
import re


with open("phonebook_raw.csv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    contacts_list = list(reader)

header = contacts_list[0]
contacts = contacts_list[1:]



def normalize_phone(phone):
    pattern = re.compile(
        r"(\+7|8)?\s*"
        r"\(?(\d{3})\)?[\s\-]*"
        r"(\d{3})[\s\-]*"
        r"(\d{2})[\s\-]*"
        r"(\d{2})"
        r"(?:\s*\(?(доб\.?)\s*(\d+)\)?)?"
    )

    def repl(m):
        base = f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
        ext = f"доб.{m.group(7)}" if m.group(7) else ""
        return base + (f" {ext}" if ext else "")

    return pattern.sub(repl, phone)



new_contacts = []

for contact in contacts:

    
    new_contact = [""] * 7

    
    fio = " ".join(contact[:3]).split()

    if len(fio) > 0:
        new_contact[0] = fio[0]
    if len(fio) > 1:
        new_contact[1] = fio[1]
    if len(fio) > 2:
        new_contact[2] = fio[2]

    
    new_contact[3] = contact[3] if len(contact) > 3 else ""
    new_contact[4] = contact[4] if len(contact) > 4 else ""
    new_contact[5] = normalize_phone(contact[5]) if len(contact) > 5 else ""
    new_contact[6] = contact[6] if len(contact) > 6 else ""

    new_contacts.append(new_contact)



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
    writer = csv.writer(f, delimiter=",")
    writer.writerows(contacts_list)
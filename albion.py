import tkinter as tk
from tkinter import ttk
import os
from math import ceil


title = 'albion'
size = '700x900'

font = ('Arial', 10)
width = 20

towns_text = 'Название города'
item_text = 'Название предмета'
price_text = 'Цена предмета'
tax_text = 'Налог'
glory_text = 'Количество славы'
return_percent_text = 'Возврат ресурсов'
add_text = '+'
remove_text = '-'
resource_label_text = 'Материалы'
resource_text = 'Материал'
resource_count_text = 'Количество'
resource_price_text = 'Цена'
magazine_text = 'Журнал'
magazine_empty_text = 'Цена пустого'
magazine_full_text = 'Цена заполненого'
magazine_glory_text = 'Количество славы'
radio_count_text = 'Количество'
radio_money_text = 'Деньги'
results_button_text = 'Посчитать'

resources_objects = []

items = {}
resources = {}
magazines = {}
towns = ('Caerleon', 'Thetford', 'Fort Sterling', 'Lymhurst', 'Bridgewatch', 'Martlock')


def format(data):
    data = data.replace('\n', '')
    data = data.replace(', ', ',')

    index = 0
    tabs = 0

    for i in data[::]:
        if i == '{':
            tabs += 1
            data = data[:index] + '{\n' + tabs * 4 * ' ' + data[index + 1:]
            index += 1 + tabs * 4
        if i == ',':
            data = data[:index] + ',\n' + tabs * 4 * ' ' + data[index + 1:]
            index += 1 + tabs * 4
        if i == '}':
            tabs -= 1
            data = data[:index] + '\n' + tabs * \
                4 * ' ' + '}' + data[index + 1:]
            index += 1 + tabs * 4
        if i == '[':
            tabs += 1
            data = data[:index] + '[\n' + tabs * 4 * ' ' + data[index + 1:]
            index += 1 + tabs * 4
        if i == ']':
            tabs -= 1
            data = data[:index] + '\n' + tabs * \
                4 * ' ' + ']' + data[index + 1:]
            index += 1 + tabs * 4
        index += 1

    return data


def add():
    global resources_objects

    resource_frame = tk.Frame(resources_frame)

    resource_label = tk.Label(resource_frame, text=resource_text, font=font)
    resource_label.grid(column=0, row=0)
    resource_combobox = ttk.Combobox(resource_frame, values=list(resources.keys()), width=width, font=font)
    resource_combobox.bind('<<ComboboxSelected>>', resource_load)
    resource_combobox.grid(column=1, row=0)
    count_label = tk.Label(resource_frame, text=resource_count_text, font=font)
    count_label.grid(column=0, row=1)
    count_entry = tk.Entry(resource_frame, width=width, font=font)
    count_entry.grid(column=1, row=1)
    money_label = tk.Label(resource_frame, text=resource_price_text, font=font)
    money_label.grid(column=0, row=2)
    money_entry = tk.Entry(resource_frame, width=width, font=font)
    money_entry.grid(column=1, row=2)

    resources_objects.append([resource_frame, resource_combobox, count_entry, money_entry])
    resources_frame.grid_remove()
    for i in range(len(resources_objects)):
        resources_objects[i][0].grid(column=i, row=0)
    buttons_frame.grid(column=len(resources_objects), row=0)


def remove():
    global resources_objects

    for element in resources_objects.pop():
        element.grid_remove()
    resources_frame.grid_remove()
    for i in range(len(resources_objects)):
        resources_objects[i][0].grid(column=i, row=0)
    buttons_frame.grid(column=len(resources_objects), row=0)


def town_save():
    town = towns_combobox.get()

    item_save()
    resource_save()
    magazine_save()

    data = {'items': items, 'resources': resources, 'magazines': magazines, 'return_percent': float(return_percent_entry.get())}
    data = str(data)

    data = format(data)

    with open(f'{town}.txt', 'w', encoding='utf-8') as file:
        file.write(data)


def town_load(event=None):
    global items
    global resources
    global magazines

    town = towns_combobox.get()
    if f'{town}.txt' in os.listdir():
        with open(f'{town}.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            if data != '':
                data = eval(data)
                items = data['items']
                resources = data['resources']
                magazines = data['magazines']
                return_percent_entry.delete(0, tk.END)
                return_percent_entry.insert(0, str(data['return_percent']))
                item_combobox['values'] = list(items.keys())
                for resource in resources_objects:
                    resource[1]['values'] = list(resources.keys())
                magazine_combobox['values'] = list(magazines.keys())


def item_save():
    item = item_combobox.get()
    if item in items.keys():
        items[item].clear()
        items[item]['price'] = int(price_entry.get())
        items[item]['tax'] = int(tax_entry.get())
        items[item]['glory'] = int(glory_entry.get())
        items[item]['magazine'] = magazine_combobox.get()
        items[item]['resources'] = {}
        for resource in resources_objects:
            items[item]['resources'][resource[1].get()] = int(resource[2].get())


def item_load(event=None):
    item = item_combobox.get()
    if item in items.keys():
        price_entry.delete(0, tk.END)
        price_entry.insert(0, items[item]['price'])
        tax_entry.delete(0, tk.END)
        tax_entry.insert(0, items[item]['tax'])
        glory_entry.delete(0, tk.END)
        glory_entry.insert(0, items[item]['glory'])
        while len(resources_objects) < len(items[item]['resources']):
            add()
        while len(resources_objects) > len(items[item]['resources']):
            remove()
        for i in range(len(resources_objects)):
            resource = list(items[item]['resources'].keys())[i]
            if resource in resources.keys():
                resources_objects[i][1].current(list(resources.keys()).index(resource))
            resources_objects[i][2].delete(0, tk.END)
            resources_objects[i][2].insert(0, items[item]['resources'][resource])
            resources_objects[i][3].delete(0, tk.END)
            resources_objects[i][3].insert(0, resources[resource])

        magazine = items[item]['magazine']

        if magazine in magazines.keys():
            magazine_combobox.current(list(magazines.keys()).index(magazine))
            magazine_load()


def resource_save():
    for resource in resources_objects:
        resources[resource[1].get()] = int(resource[3].get())


def resource_load(event=None):
    resource = event.widget.get()
    if resource in resources.keys():
        event.widget.master.children['!entry2'].delete(0, tk.END)
        event.widget.master.children['!entry2'].insert(0, resources[resource])


def magazine_save():
    magazine = magazine_combobox.get()
    magazines[magazine]['empty'] = int(magazine_empty_entry.get())
    magazines[magazine]['full'] = int(magazine_full_entry.get())
    magazines[magazine]['glory'] = int(magazine_glory_entry.get())


def magazine_load(event=None):
    magazine = magazine_combobox.get()
    if magazine in magazines.keys():
        magazine_empty_entry.delete(0, tk.END)
        magazine_empty_entry.insert(0, magazines[magazine]['empty'])
        magazine_full_entry.delete(0, tk.END)
        magazine_full_entry.insert(0, magazines[magazine]['full'])
        magazine_glory_entry.delete(0, tk.END)
        magazine_glory_entry.insert(0, magazines[magazine]['glory'])


def data_save():
    with open('data.txt', 'w', encoding='utf-8') as file:
        data = {
            'town': towns_combobox.get(),
            'item': item_combobox.get(),
            'radio': clicked.get(),
            'entry': radio_entry.get()
        }
        data = str(data)
        data = format(data)
        file.write(data)


def data_load():
    if 'data.txt' in os.listdir():
        with open('data.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            if data != '':
                data = eval(data)
                towns_combobox.current(towns.index(data['town']))
                town_load()
                item_combobox.current(list(items.keys()).index(data['item']))
                item_load()
                clicked.set(data['radio'])
                radio_entry.insert(0, data['entry'])


def results():
    town_save()
    data_save()

    item = item_combobox.get()
    price = items[item]['price']
    tax = items[item]['tax']
    glory = items[item]['glory']
    return_percent = float(return_percent_entry.get())
    magazine = magazine_combobox.get()
    magazine_glory = magazines[magazine]['glory']
    magazine_empty = magazines[magazine]['empty']
    magazine_full = magazines[magazine]['full']
    n = int(radio_entry.get())

    n0 = n
    spent = 0

    resources_obtained = {}
    for resource in resources_objects:
        resources_obtained[resource[1].get()] = n * int(resource[2].get())
        spent += int(resource[2].get()) * int(resource[3].get())

    if clicked.get() == 0:

        magazine_filling = 0

        n1 = n
        while n1 > 0:
            n2 = float('inf')
            for resource in resources_objects:
                resources_obtained[resource[1].get()] = resources_obtained[resource[1].get()] % (n1 * int(resource[2].get())) +\
                    round(n1 * int(resource[2].get()) * return_percent / 100)
                n2 = min(n2, resources_obtained[resource[1].get()] // int(resource[2].get()))

            n1 = n2
            n += n1

    magazine_completed = n * glory // magazine_glory
    magazine_filling = n * glory % magazine_glory
    earn_magazine = magazine_completed * (magazine_full - magazine_empty)
    earn_all = earn_magazine + price * n - (tax * n + spent * n0)
    earn = earn_all // n0
    spent_all = spent * n0 + ceil(n * glory / magazine_glory) * magazine_empty
    print(n, n0)

    results_label['text'] = f'Заполнено {magazine_completed} журналов, в не полном журнале {magazine_filling} славы\n'
    results_label['text'] += f'Прибыль с журналов {earn_magazine}\n'
    results_label['text'] += f'Прибыль за один предмет {earn} (с учётом всего)\n'
    results_label['text'] += f'Прибыль за всё {earn_all}, потрачено {spent_all}\n'
    results_label['text'] += f'Коэффициент прибыльности {earn_all / spent_all}'


window = tk.Tk()
window.title(title)
window.geometry(size)

# CEATE ELEMENTS

padx = 10
pady = 5

towns_frame = tk.Frame(window)
towns_frame.pack(padx=padx, pady=pady)
towns_label = tk.Label(towns_frame, text=towns_text, font=font)
towns_label.grid(column=0, row=0)
towns_combobox = ttk.Combobox(towns_frame, values=towns, width=width, font=font)
towns_combobox.bind('<<ComboboxSelected>>', town_load)
towns_combobox.grid(column=1, row=0)


item_frame = tk.Frame(window)
item_frame.pack(anchor=tk.W, padx=padx, pady=pady)

item_label = tk.Label(item_frame, text=item_text, font=font)
item_label.grid(column=0, row=0, sticky=tk.W)
item_combobox = ttk.Combobox(item_frame, values=list(items.keys()), width=width, font=font)
item_combobox.bind('<<ComboboxSelected>>', item_load)
item_combobox.grid(column=1, row=0)

price_label = tk.Label(item_frame, text=price_text, font=font)
price_label.grid(column=0, row=1, sticky=tk.W)
price_entry = tk.Entry(item_frame, width=width, font=font)
price_entry.grid(column=1, row=1)

tax_label = tk.Label(item_frame, text=tax_text, font=font)
tax_label.grid(column=0, row=2, sticky=tk.W)
tax_entry = tk.Entry(item_frame, width=width, font=font)
tax_entry.grid(column=1, row=2)

glory_label = tk.Label(item_frame, text=glory_text, font=font)
glory_label.grid(column=0, row=3, sticky=tk.W)
glory_entry = tk.Entry(item_frame, font=font, width=width)
glory_entry.grid(column=1, row=3)

return_percent_label = tk.Label(item_frame, text=return_percent_text, font=font)
return_percent_label.grid(column=0, row=4, sticky=tk.W)
return_percent_entry = tk.Entry(item_frame, font=font, width=width)
return_percent_entry.grid(column=1, row=4)


resource_label = tk.Label(window, text=resource_label_text, font=font)
resource_label.pack(padx=padx, pady=pady)

resources_frame = tk.Frame(window)
resources_frame.pack(anchor=tk.W, padx=padx, pady=pady)
buttons_frame = tk.Frame(resources_frame)
buttons_frame.grid(column=0, row=0)
add_button = tk.Button(buttons_frame, text=add_text, command=add, font=font, width=2, height=1)
add_button.grid(column=0, row=0)
remove_button = tk.Button(buttons_frame, text=remove_text, command=remove, font=font, width=2, height=1)
remove_button.grid(column=0, row=1)


magazine_frame = tk.Frame(window)
magazine_frame.pack(anchor=tk.W, padx=padx, pady=pady)
magazine_label = tk.Label(magazine_frame, text=magazine_text, font=font)
magazine_label.grid(column=0, row=0, sticky=tk.W)
magazine_combobox = ttk.Combobox(magazine_frame, values=list(magazines.keys()), width=width, font=font)
magazine_combobox.bind('<<ComboboxSelected>>', magazine_load)
magazine_combobox.grid(column=1, row=0)
magazine_empty_label = tk.Label(magazine_frame, text=magazine_empty_text, font=font)
magazine_empty_label.grid(column=0, row=1, sticky=tk.W)
magazine_empty_entry = tk.Entry(magazine_frame, width=width, font=font)
magazine_empty_entry.grid(column=1, row=1)
magazine_full_label = tk.Label(magazine_frame, text=magazine_full_text, font=font)
magazine_full_label.grid(column=0, row=2, sticky=tk.W)
magazine_full_entry = tk.Entry(magazine_frame, width=width, font=font)
magazine_full_entry.grid(column=1, row=2)
magazine_glory_label = tk.Label(magazine_frame, text=magazine_glory_text, font=font)
magazine_glory_label.grid(column=0, row=3, sticky=tk.W)
magazine_glory_entry = tk.Entry(magazine_frame, font=font, width=width)
magazine_glory_entry.grid(column=1, row=3)


radio_frame = tk.Frame(window)
radio_frame.pack(anchor=tk.W, padx=padx, pady=pady)
clicked = tk.IntVar()
radio_count = tk.Radiobutton(radio_frame, text=radio_count_text, value=0, variable=clicked, font=font)
radio_count.grid(column=0, row=0)
radio_money = tk.Radiobutton(radio_frame, text=radio_money_text, value=1, variable=clicked, font=font)
radio_money.grid(column=1, row=0)
radio_entry = tk.Entry(radio_frame, width=width, font=font)
radio_entry.grid(column=2, row=0)


results_frame = tk.Frame(window)
results_frame.pack(anchor=tk.W, padx=padx, pady=pady)
results_button = tk.Button(results_frame, text=results_button_text, command=results, font=font)
results_button.grid(column=0, row=0)
results_label = tk.Label(results_frame, font=font)
results_label.grid(column=1, row=0)

data_load()

window.mainloop()

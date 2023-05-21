import datetime
from tkinter import *
import tkinter.ttk as ttk
import urllib.request
import xml.dom.minidom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


def clicked():
    selectCountryFrom = comboCountryFrom.get()
    nominalFrom = 0
    valueFrom = 0
    selectCountryTo = comboCountryTo.get()
    nominalTo = 0
    valueTo = 0
    inpData = entry1.get()
    mainTags = dom.getElementsByTagName("Valute")
    for node in mainTags:
        name = node.getElementsByTagName('Name')
        if name[0].childNodes[0].nodeValue == selectCountryFrom:
            nominal = node.getElementsByTagName('Nominal')
            nominalFrom = nominal[0].childNodes[0].nodeValue
            value = node.getElementsByTagName('Value')
            valueFrom = value[0].childNodes[0].nodeValue
        if name[0].childNodes[0].nodeValue == selectCountryTo:
            nominal = node.getElementsByTagName('Nominal')
            nominalTo = nominal[0].childNodes[0].nodeValue
            value = node.getElementsByTagName('Value')
            valueTo = value[0].childNodes[0].nodeValue
    first = float(inpData.replace(',', '.')) * float(valueFrom.replace(',', '.')) / float(nominalFrom.replace(',', '.'))
    second = first / float(valueTo.replace(',', '.')) / float(nominalTo.replace(',', '.'))
    answer['text'] = str(second)


def updateComboPeriod():
    if radio_state.get() == 1:
        year = 2022
        dates = []
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    date = datetime.date(year, month, day)
                    formatted_date = date.strftime('%d.%m.%Y')
                    dates.append(formatted_date)
                except ValueError:
                    pass
        comboValue = []
        for i in range(-1, len(dates) - 7, 7):
            comboValue.append(dates[i+1] + '-' + dates[i+7])
        comboPeriod.config(values=comboValue)
    elif radio_state.get() == 2:
        year = 2022
        month_names_ru = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                          'ноябрь', 'декабрь']

        months_with_year = [f"{month_name} {year}" for month_name in month_names_ru]
        comboPeriod.config(values=months_with_year)
    elif radio_state.get() == 3:
        cvartals = ['1-ый квартал 2022', '2-ый квартал 2022', '3-ый квартал 2022', '4-ый квартал 2022',]
        comboPeriod.config(values=cvartals)
    else:
        years = ['2022', '2021', '2020', '2019']
        comboPeriod.config(values=years)


def plot():
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=tab2)
    canvas.get_tk_widget()
    y = []
    x = []
    path = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=22/04/2022"
    year = 2022
    comboValues = []
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                date = datetime.date(year, month, day)
                formatted_date = date.strftime('%d.%m.%Y')
                comboValues.append(formatted_date)
            except ValueError:
                pass
    Country = comboChoose.get()
    if radio_state.get() == 1:
        period = comboPeriod.get()
        firstdata = period[0:10]
        seconddata = period[11::]
        f_ind = comboValues.index(firstdata)
        t_ind = comboValues.index(seconddata)
        x = comboValues[f_ind:t_ind+1]
        for i in range(7):
            head, sep, tail = path.partition('=')
            url = urllib.request.urlopen(head + '=' + x[i].replace('.', '/'))
            dom = xml.dom.minidom.parse(url)
            dom.normalize()
            listOfNodes = dom.getElementsByTagName('Valute')
            for node in listOfNodes:
                name = node.getElementsByTagName('Name')
                if name[0].childNodes[0].nodeValue == Country:
                    nominal = node.getElementsByTagName('Nominal')
                    nominal = nominal[0].childNodes[0].nodeValue
                    value = node.getElementsByTagName('Value')
                    value = value[0].childNodes[0].nodeValue
                    y.append(float(value.replace(',', '.'))/float(nominal.replace(',', '.')))
                    break
    if radio_state.get() == 2:
        month = comboPeriod.get()
        n = 0
        num = ""
        if month == 'январь 2022':
            num = '01'
            n = 31
        if month == 'февраль 2022':
            num = '02'
            n = 28
        if month == 'март 2022':
            num = '03'
            n = 31
        if month == 'апрель 2022':
            num = '04'
            n = 30
        if month == 'май 2022':
            num = '05'
            n = 31
        if month == 'июнь 2022':
            num = '06'
            n = 30
        if month == 'июль 2022':
            num = '07'
            n = 31
        if month == 'август 2022':
            num = '08'
            n = 31
        if month == 'сентябрь 2022':
            num = '09'
            n = 30
        if month == 'октябрь 2022':
            num = '10'
            n = 31
        if month == 'ноябрь 2022':
            num = '11'
            n = 30
        if month == 'декабрь 2022':
            num = '12'
            n = 31
        firstdata = "01." + num + ".2022"
        seconddata = str(n) + "." + num + ".2022"
        f_ind = comboValues.index(firstdata)
        t_ind = comboValues.index(seconddata)
        x = comboValues[f_ind:t_ind + 1]
        for i in range(0, n):
            head, sep, tail = path.partition('=')
            url = urllib.request.urlopen(head + '=' + x[i].replace('.', '/'))
            dom = xml.dom.minidom.parse(url)
            dom.normalize()
            listOfNodes = dom.getElementsByTagName('Valute')
            for node in listOfNodes:
                name = node.getElementsByTagName('Name')
                if name[0].childNodes[0].nodeValue == Country:
                    nominal = node.getElementsByTagName('Nominal')
                    nominal = nominal[0].childNodes[0].nodeValue
                    value = node.getElementsByTagName('Value')
                    value = value[0].childNodes[0].nodeValue
                    y.append(float(value.replace(',', '.')) / float(nominal.replace(',', '.')))
                    break
        for a in range(n):
            x[a] = a + 1
    if radio_state.get() == 3:
        period3 = comboPeriod.get()
        if period3[0] == '1':
            for i in range(1, 4):
                for j in range(1, 4):
                    firstdata = str(j * 7 + 3) + '/' + '0' + str(i) + '/2022'
                    x.append(firstdata.replace('/', '.'))
                    head, sep, tail = path.partition('=')
                    url = urllib.request.urlopen(head + '=' + firstdata)
                    dom = xml.dom.minidom.parse(url)
                    dom.normalize()
                    listOfNodes = dom.getElementsByTagName('Valute')
                    for node in listOfNodes:
                        name = node.getElementsByTagName('Name')
                        if name[0].childNodes[0].nodeValue == Country:
                            nominal = node.getElementsByTagName('Nominal')
                            nominal = nominal[0].childNodes[0].nodeValue
                            value = node.getElementsByTagName('Value')
                            value = value[0].childNodes[0].nodeValue
                            y.append(float(value.replace(',', '.')) / float(nominal.replace(',', '.')))
                            break
        if period3[0] == '2':
            for i in range(4, 7):
                for j in range(1, 4):
                    firstdata = str(j * 7 + 3) + '/' + '0' + str(i) + '/2022'
                    x.append(firstdata.replace('/', '.'))
                    head, sep, tail = path.partition('=')
                    url = urllib.request.urlopen(head + '=' + firstdata)
                    dom = xml.dom.minidom.parse(url)
                    dom.normalize()
                    listOfNodes = dom.getElementsByTagName('Valute')
                    for node in listOfNodes:
                        name = node.getElementsByTagName('Name')
                        if name[0].childNodes[0].nodeValue == Country:
                            nominal = node.getElementsByTagName('Nominal')
                            nominal = nominal[0].childNodes[0].nodeValue
                            value = node.getElementsByTagName('Value')
                            value = value[0].childNodes[0].nodeValue
                            y.append(float(value.replace(',', '.')) / float(nominal.replace(',', '.')))
                            break
        if period3[0] == '3':
            for i in range(7, 10):
                for j in range(1, 4):
                    firstdata = str(j * 7 + 3) + '/' + '0' + str(i) + '/2022'
                    x.append(firstdata.replace('/', '.'))
                    head, sep, tail = path.partition('=')
                    url = urllib.request.urlopen(head + '=' + firstdata)
                    dom = xml.dom.minidom.parse(url)
                    dom.normalize()
                    listOfNodes = dom.getElementsByTagName('Valute')
                    for node in listOfNodes:
                        name = node.getElementsByTagName('Name')
                        if name[0].childNodes[0].nodeValue == Country:
                            nominal = node.getElementsByTagName('Nominal')
                            nominal = nominal[0].childNodes[0].nodeValue
                            value = node.getElementsByTagName('Value')
                            value = value[0].childNodes[0].nodeValue
                            y.append(float(value.replace(',', '.')) / float(nominal.replace(',', '.')))
                            break
        if period3[0] == '4':
            for i in range(10, 13):
                for j in range(1, 4):
                    firstdata = str(j * 7 + 3) + '/' + '0' + str(i) + '/2022'
                    x.append(firstdata.replace('/', '.'))
                    head, sep, tail = path.partition('=')
                    url = urllib.request.urlopen(head + '=' + firstdata)
                    dom = xml.dom.minidom.parse(url)
                    dom.normalize()
                    listOfNodes = dom.getElementsByTagName('Valute')
                    for node in listOfNodes:
                        name = node.getElementsByTagName('Name')
                        if name[0].childNodes[0].nodeValue == Country:
                            nominal = node.getElementsByTagName('Nominal')
                            nominal = nominal[0].childNodes[0].nodeValue
                            value = node.getElementsByTagName('Value')
                            value = value[0].childNodes[0].nodeValue
                            y.append(float(value.replace(',', '.')) / float(nominal.replace(',', '.')))
                            break
    if radio_state.get() == 4:
        period4 = comboPeriod.get()
        month_names_ru = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                          'ноябрь', 'декабрь']
        for i in range(1, 13):
            if i < 10:
                firstdata = '14/' + '0' + str(i) + '/' + period4
            else:
                firstdata = '14/' + str(i) + '/' + period4
            x.append(month_names_ru[i-1])
            head, sep, tail = path.partition('=')
            url = urllib.request.urlopen(head + '=' + firstdata)
            dom = xml.dom.minidom.parse(url)
            dom.normalize()
            listOfNodes = dom.getElementsByTagName('Valute')
            for node in listOfNodes:
                name = node.getElementsByTagName('Name')
                if name[0].childNodes[0].nodeValue == Country:
                    nominal = node.getElementsByTagName('Nominal')
                    nominal = nominal[0].childNodes[0].nodeValue
                    value = node.getElementsByTagName('Value')
                    value = value[0].childNodes[0].nodeValue
                    y.append(float(value.replace(',', '.')) / float(nominal.replace(',', '.')))
                    break

    ax.plot(x, y)
    ax.grid(b=True)
    ax.tick_params(axis='both', labelsize=7, rotation=45)
    canvas.draw()
    canvas.get_tk_widget().grid(column=3, row=5, columnspan=3, rowspan=5)


window = Tk()
window.geometry("1200x700")  # Creating window
window.title("Калькулятор валют")  # Name of window
tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text="Калькулятор валют")
tab_control.add(tab2, text="Динамика курса")
tab_control.pack(expand=1, fill="both")

url = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=22/04/2022")
dom = xml.dom.minidom.parse(url)
dom.normalize()
CountryFrom = dom.getElementsByTagName("Name")
for i in range(len(CountryFrom)):
    CountryFrom[i] = CountryFrom[i].childNodes[0].nodeValue

comboCountryFrom = ttk.Combobox(tab1, values=CountryFrom, state="readonly", width=30)
comboCountryFrom.grid(column=0, row=0, padx=10, pady=10)
comboCountryFrom.current(0)

comboCountryTo = ttk.Combobox(tab1, values=CountryFrom, state="readonly", width=30)
comboCountryTo.grid(column=0, row=1, padx=10, pady=10)
comboCountryTo.current(0)

buttonConvert = Button(tab1, text="Конвертировать", command=clicked)
buttonConvert.grid(column=3, row=0, padx=10, pady=10)

entry1 = Entry(tab1)
entry1.grid(column=1, row=0)

answer = Label(tab1, text='0')
answer.grid(column=1, row=1, padx=10, pady=10)
# Page 2
butttonGraphic = Button(tab2, text="Построить график", command=plot)
butttonGraphic.grid(column=0, row=4, padx=10, pady=10)

text = Label(tab2, text="Валюта", justify=CENTER, width=15)
text.grid(column=0, row=0)

comboChoose = ttk.Combobox(tab2, values=CountryFrom, state="readonly", width=30)
comboChoose.grid(column=0, row=1, pady=10, padx=10)
comboChoose.current(0)

lab = Label(tab2, text="Период", justify=CENTER, width=15)
lab.grid(column=1, row=0)

comboPeriod = ttk.Combobox(tab2, width=30)
comboPeriod.grid(column=2, row=4)

radio_state = IntVar()
radio_state.set(1)
R1 = Radiobutton(tab2, text="Неделя", value=1, variable=radio_state, command=updateComboPeriod)
R2 = Radiobutton(tab2, text="Месяц", value=2, variable=radio_state, command=updateComboPeriod)
R3 = Radiobutton(tab2, text="Квартал", value=3, variable=radio_state, command=updateComboPeriod)
R4 = Radiobutton(tab2, text="Год", value=4, variable=radio_state, command=updateComboPeriod)
R1.grid(column=1, row=1)
R2.grid(column=1, row=2)
R3.grid(column=1, row=3)
R4.grid(column=1, row=4)

period = Label(tab2, text="Выбор периода", width=30, justify=CENTER)
period.grid(column=2, row=0)

window.mainloop()
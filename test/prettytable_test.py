# -*- coding: utf-8 -*-

import json

from prettytable import PrettyTable
from prettytable import from_json

def make_table():
    lstEmployee = json.loads('''
        [{"final":2716,"pay":2800,"tax":84,"name":"A"},{"final":3630,"pay":3800,"tax":170,"name":"B"},{"final":4530,"pay":4800,"tax":270,"name":"C"},{"final":6330,"pay":6800,"tax":470,"name":"D"},{"final":6960,"pay":7500,"tax":540,"name":"E"},{"final":8760,"pay":9500,"tax":740,"name":"F"},{"final":13410,"pay":15000,"tax":1590,"name":"G"},{"final":21410,"pay":25000,"tax":3590,"name":"H"},{"final":25160,"pay":30000,"tax":4840,"name":"I"},{"final":28910,"pay":35000,"tax":6090,"name":"J"},{"final":32410,"pay":40000,"tax":7590,"name":"K"},{"final":39410,"pay":50000,"tax":10590,"name":"L"},{"final":46160,"pay":60000,"tax":13840,"name":"M"},{"final":52660,"pay":70000,"tax":17340,"name":"N"},{"final":61910,"pay":85000,"tax":23090,"name":"O"},{"final":70160,"pay":100000,"tax":29840,"name":"P"},{"final":565160,"pay":1000000,"tax":434840,"name":"Q"}]
    ''')

    table = PrettyTable()
    table.field_names = ['name', 'pay', 'tax', "final"]
    for dictItem in lstEmployee:
        lstRow = []
        for szKey in ['name', 'pay', 'tax', "final"]:
            lstRow.append(dictItem[szKey])

        table.add_row(lstRow)

    return table

def main():
    table = PrettyTable()
    table.field_names = ['Name', 'Age', 'City']
    table.add_row(["Alice", 20, "Adelaide"])
    table.add_row(["Bob", 20, "Brisbane"])
    table.add_row(["Chris", 20, "Cairns"])
    table.add_row(["David", 20, "Sydney"])
    table.add_row(["Ella", 20, "Melbourne"])

    print(table)

    tableEmployee = make_table()
    print(tableEmployee)

if __name__ == '__main__':
    main()
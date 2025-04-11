import pandas

Thanh = pandas.read_csv('Thanh.csv')
Khang = pandas.read_csv('Khang.csv')

Thanh = Thanh.sort_values(by = 'Player')

# print(Khang.compare(Thanh))

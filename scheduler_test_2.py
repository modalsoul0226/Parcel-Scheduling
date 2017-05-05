from domain import Parcel, Truck
from scheduler import *

parcel_algm = ['non-decreasing_volume', 'non-increasing_volume',
               'non-decreasing_destination', 'non-increasing_destination']
truck_algm = ['non-increasing', 'non-decreasing']
algm = []
source = 'New York'
for i in parcel_algm:
    for j in truck_algm:
        algm.append([i, j])
# print(algm)
# for each in algm:
#     if each[0] == 'nondecreasing_volume':
#         print(each[0], each[1])
for each in algm:
    parcel_normal = [['1', 'A', 40], ['2', 'B', 15], ['3', 'C', 20],
                     ['4', 'A', 5], ['5', 'A', 5], ['6', 'B', 10],
                     ['20', 'A', 200]]
    truck_normal = [['20', 100], ['21', 25], ['22', 60]]
    parcels = []
    trucks = []
    for i in parcel_normal:
        temp = Parcel(i[0], source, i[1], i[2])
        parcels.append(temp)
    for j in truck_normal:
        temp = Truck(j[0], j[1])
        trucks.append(temp)
    g = GreedyScheduler(each[0], each[1])
    v = g.schedule(parcels, trucks)
    for m in v:
        print(m.get_parcel()[0])
    print(each)
    for k in trucks:
        print(k.get_volume(), k.get_destination(), k.get_parcel())
    print('===============================')

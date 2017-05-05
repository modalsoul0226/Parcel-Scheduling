# Parcel-Scheduling
The code is designed to try out different algorithms to perform parcel scheduling and compare their performance.

In this experiment, each parcel has a source and a destination, which are the name of the city the parcel came from, and where it must be delivered to, respectively. We will not deal with specific addresses within cities. Each parcel also has a volume, which is a positive integer.

Each truck can store multiple parcels, but as a volume capacity, also a positive integer. (Each truck has its own volume capacity.) The total sum of the volumes of the parcel on a truck cannot exceed its volume capacity. Each truck also has a route, which is a list of city names that it is scheduled to travel through.
Parcel IDs are unique, that is, no two parcels can have the same ID. Truck IDs are also unique.

**Depot**

In this experiment, there is a special city that all parcels and trucks start from. We'll refer to this city as the depot. (So you can imagine all parcels have been shipped from their source city to the depot.) Our algorithms will schedule delivery of parcels from the depot to their destinations.

**Truck routes**

At the beginning of the experiment, all trucks are in the depot, are empty, and have no other cities on their route. Routes will be determined during the experiment.
We will use a very simple algorithm for choosing a truck's route, given the parcels that it has been assigned to deliver: Every time it is decided that a parcel will go onto a truck, if the parcel's destination is not already on that truck's route, the destination is added to the end of the route.

You will implement two different algorithms for choosing which parcel goes on which truck.

(1) **Random algorithm**
The random algorithm will go through the parcels in random order. For each parcel, it will schedule it onto a randomly chosen truck (from among those trucks that have capacity to add that parcel). Because of this randomness, each time you run your random algorithm on a given problem, it may generate a different solution.

(2) **Greedy algorithm**
The greedy algorithm tries to be more strategic. Like the random algorithm, it processes parcels one at a time, and picks the "best" truck it can for each parcel, but without looking ahead to possible consequences of the choice (that's why we call it "greedy").
The greedy algorithm has configurable features: the order in which parcels are considered, and how a truck is chosen for each parcel, described below.

**Parcel order**
There are four possible orders that the algorithm could use to process the parcels:
In order by parcel volume, either smallest to largest (non-decreasing) or largest to smallest (non-increasing).
In order by parcel destination, either smallest to largest (non-decreasing) or largest to smallest (non-increasing). Since destinations are strings, larger and smaller is determined by comparing strings (city names) alphabetically.
Ties are broken using the order in which the parcels are read in from our data file (see below).

**Truck choice**
When the greedy algorithm processes a parcel, it must choose which truck to assign it to. The algorithm does the following to compute the eligible trucks:
It only considers trucks that have enough unused volume to add the parcel.
Among these trucks, if there are any that already have the parcel's destination on their route, only those trucks are considered. Otherwise, all trucks that have enough unused volume are considered.
Given the eligible trucks, the algorithm can be configured one of two ways to make a choice:
choose the eligible truck with the most available space, or
choose the eligible truck with the least available space
Ties are broken using the order in which the trucks are read in from our data file. If there is no eligible truck, then the parcel is not scheduled onto any truck.
Observations about the Greedy Algorithm

Since there are four options for parcel priority and two options for truck choice, our greedy algorithm can be configured eight different ways in total.
Notice that there is no randomness in the greedy algorithm; it is completely "deterministic". This means that no matter how many times you run your greedy algorithm on a given problem, it will always generate the same solution.
Putting it all together

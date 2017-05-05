"""Assignment 1 - Scheduling algorithms (Task 4)

This module contains the abstract Scheduler interface, as well as the two
classes RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.

Your task is to implement RandomScheduler and GreedyScheduler.
You may *not* change the public interface of these classes, except that
you must write appropriate constructors for them.  The two constructors do not
need to have the same signatures.

Any attributes you use must be private, so that the public interface is exactly
what is specified by the Scheduler abstract class.
"""
from random import shuffle, choice
from container import PriorityQueue


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.

    You may add *private* methods to this class so make them available to both
    subclasses.
    """
    def schedule(self, parcels, trucks, verbose=False):
        """Schedule the given parcels onto the given trucks.

        Mutate the trucks so that they store information about which
        parcels they will deliver and what route they will take.
        Do *not* mutate the parcels.

        Return the parcels that do not get scheduled onto any truck, due to
        lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.

        @type self: Scheduler
        @type parcels: list[Parcel]
            The parcels to be scheduled for delivery.
        @type trucks: list[Truck]
            The trucks that can carry parcels for delivery.
        @type verbose: bool
            Whether or not to run in verbose mode.
        @rtype: list[Parcel]
            The parcels that did not get scheduled onto any truck, due to
            lack of capacity.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """Implement the Random algorith. The random algorithm will
    go through the parcels in random order.
    For each parcel, it will schedule it onto a randomly chosen truck
    (from among those trucks that have capacity to add that parcel).
    Because of this randomness, each time, it may generate
    a different solution.
    """
    def schedule(self, parcels, trucks, verbose=False):
        """Mutate the trucks so that they store information about which
        parcels they will deliver and what route they will take.
        Parcel objects in the parcels will not be mutated.
        Return the parcels that do not get scheduled onto any truck, due to
        lack of capacity.

        @type self: Scheduler
        @type parcels: list[Parcel]
            The parcels to be scheduled for delivery.
        @type trucks: list[Truck]
            The trucks that can carry parcels for delivery.
        @type verbose: bool
            Whether or not to run in verbose mode.
        @rtype: list[Parcel]
            The parcels that did not get scheduled onto any truck, due to
            lack of capacity.
        """
        shuffle(parcels)
        ass_parcels = parcels[:]
        for each in parcels:
            data = each.get_parcel()
            parcel_volume = data[-1]
            destination = data[-2]
            truck = choice(trucks)
            choice_region = trucks[:]
            while 1:
                if truck.get_volume() >= parcel_volume:
                    trucks.remove(truck)
                    truck.load_parcel(data[0], destination, parcel_volume)
                    trucks.append(truck)
                    ass_parcels.remove(each)
                    break
                else:
                    choice_region.remove(truck)
                    if choice_region:
                        truck = choice(choice_region)
                    else:
                        break
        return ass_parcels


class GreedyScheduler(Scheduler):
    """The greedy algorithm tries to be more strategic. Like the
    random algorithm, it processes parcels one at a time,
    and picks the "best" truck it can for each parcel, but without
    looking ahead to possible consequences of the choice
    The greedy algorithm has configurable features: the order in which
    parcels are considered, and how a truck is chosen for each parcel.

    Parcel order:
    There are four possible orders that the algorithm could use to
    process the parcels:
    In order by parcel volume, either smallest to largest (non-decreasing)
    or largest to smallest (non-increasing).
    In order by parcel destination, either smallest to largest (non-decreasing)
    or largest to smallest (non-increasing).

    Truck choice:
    It only considers trucks that have enough unused volume to add the parcel.
    Among these trucks, if there are any that already have the parcel's
    destination on their route, only those trucks are considered.
    Otherwise, all trucks that have enough unused volume are considered.
    Given the eligible trucks, the algorithm can be configured
    one of two ways to make a choice:
        choose the eligible truck with the most available space, or
        choose the eligible truck with the least available space

    If there is no eligible truck, then the parcel is not scheduled
    onto any truck.

    === Private Attribute ===
    @type _fun1: function
        Specify the algorithm for the choice of parcel.
    @type _fun2: function
        Specify the algorithm for the choice of truck.
    """
    def __init__(self, parcel_algm, truck_algm):
        """Decide which algorithms should Parcel and Truck adopt.

        @type parcel_algm: str
        @type truck_algm; str
        @rtype: None
        """
        def nondecreasing_volume(a, b):
            """Sort the parcels with increasing volume.

            @type a: obj
            @type b: obj
            @rtype: bool
            """
            return a.get_parcel()[-1] < b.get_parcel()[-1]

        def nonincreasing_volume(a, b):
            """Sort the parcels with decreasing volume.

            @type a: obj
            @type b: obj
            @rtype: bool
            """
            return a.get_parcel()[-1] > b.get_parcel()[-1]

        def nondecreasing_destination(a, b):
            """Sort the parcels with increasing destination.

            @type a: obj
            @type b: obj
            @rtype: bool
            """
            return a.get_parcel()[-2] < b.get_parcel()[-2]

        def nonincreasing_destination(a, b):
            """Sort the parcels with decreasing destination.

            @type a: obj
            @type b: obj
            @rtype: bool
            """
            return a.get_parcel()[-2] > b.get_parcel()[-2]

        def truck_most_space(a, b):
            """Sort the trucks with decreasing available space.

            @type a: obj
            @type b: obj
            @rtype: bool
            """
            return a.get_volume() > b.get_volume()

        def truck_least_space(a, b):
            """Sort the trucks with increasing available space.

            @type a: obj
            @type b: obj
            @rtype: bool
            """
            return a.get_volume() < b.get_volume()

        if parcel_algm == 'non-decreasing_volume':
            self._fun1 = nondecreasing_volume
        elif parcel_algm == 'non-increasing_volume':
            self._fun1 = nonincreasing_volume
        elif parcel_algm == 'non-decreasing_destination':
            self._fun1 = nondecreasing_destination
        elif parcel_algm == 'non-increasing_destination':
            self._fun1 = nonincreasing_destination
        else:
            raise NameError

        if truck_algm == 'non-increasing':
            self._fun2 = truck_most_space
        elif truck_algm == 'non-decreasing':
            self._fun2 = truck_least_space
        else:
            raise NameError

    def schedule(self, parcels, trucks, verbose=False):
        """Mutate the trucks so that they store information about which
        parcels they will deliver and what route they will take.
        The parcels will not be mutated.
        Return the parcels that do not get scheduled onto any truck, due to
        lack of capacity.

        @type self: Scheduler
        @type parcels: list[Parcel]
            The parcels to be scheduled for delivery.
        @type trucks: list[Truck]
            The trucks that can carry parcels for delivery.
        @type verbose: bool
            Whether or not to run in verbose mode.
        @rtype: list[Parcel]
            The parcels that did not get scheduled onto any truck, due to
            lack of capacity.
        """
        parcel_queue = PriorityQueue(self._fun1)
        for each in parcels:
            parcel_queue.add(each)
        while not parcel_queue.is_empty():
            target_parcel = parcel_queue.remove()
            parcel_data = target_parcel.get_parcel()
            truck_1st = []
            truck_2nd = []
            for each in trucks:
                if each.get_volume() >= parcel_data[-1]:
                    truck_1st.append(each)
            for i in truck_1st:
                if parcel_data[-2] in i.get_destination():
                    truck_2nd.append(i)
            if not len(truck_2nd):
                truck_2nd = truck_1st
            truck_queue = PriorityQueue(self._fun2)
            for j in truck_2nd:
                truck_queue.add(j)
            if not truck_queue.is_empty():
                truck_choice = truck_queue.remove()
                indx = trucks.index(truck_choice)
                trucks.remove(truck_choice)
                truck_choice.load_parcel(parcel_data[0], parcel_data[-2],
                                         parcel_data[-1])
                parcels.remove(target_parcel)
                trucks.insert(indx, truck_choice)
        return parcels


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='.pylintrc')

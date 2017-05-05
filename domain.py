"""Assignment 1 - Domain classes (Task 2)

This module contains all of the classes required to represent the entities
in the experiment, including at least a class Parcel and a class Truck.
"""


class Parcel:
    """A class responsible for storing the data for a specific parcel
    and any operations neccessary related to the parcel. Each parcel has a
    source and a destination, which are the name of the city the parcel
    came from, and where it must be delivered to, respectively. Each parcel
    also has a volume, which is a positive integer.

    >>> p = Parcel('001', 'New York', 'London', 100)
    >>> p.get_parcel()
    ['001', 'New York', 'London', 100]
    """
    def __init__(self, parcel_id, source, destination, parcel_volume):
        """Initialize the data for the parcel.

        @type self: Parcel
        @type parcel_id: str
        @type source: str
        @type destination:str
        @type parcel_volume: int
        @rtype = None
        """
        self.parcel_id = parcel_id
        self.destination = destination
        self.parcel_volume = parcel_volume
        self.source = source

    def get_parcel(self):
        """Get the data of a parcel.

        @type self: Parcel
        @rtype: list
        """
        return [self.parcel_id, self.source, self.destination,
                self.parcel_volume]


class Truck:
    """A class responsible for storing the data for a truck and any
    operations neccessary related to the truck. Each truck can store multiple
    parcels, but as a volume capacity, also a positive integer.
    (Each truck has its own volume capacity.) The total sum of the
    volumes of the parcel on a truck cannot exceed its volume capacity.
    Each truck also has a route, which is a list of city names
    that it is scheduled to travel through.

    >>> t = Truck('100', 1000)
    >>> t.load_parcel('001', 'London', 100)
    >>> t.get_volume()
    900
    >>> t.get_destination()
    ['London']
    >>> t.get_parcel()
    ['001']
    """
    def __init__(self, truck_id, volume):
        """Initialize the list containing destinations of delivery and the
        volume of the truck.

        @type self: Truck
        @type truck_id: str
        @type volume:int
        @rtype: None
        """
        self.truck_id = truck_id
        self.destination_list = []
        self.parcel_list = []
        self.truck_volume = volume
        self.original_volume = volume

    def load_parcel(self, parcel_id, destination, parcel_volume):
        """Load the parcel onto the truck and record its data.

        @type self: Truck
        @type parcel_id: str
        @type destination: str
        @type parcel_volume: int
        @rtype: None
        """
        self.parcel_list.append(parcel_id)
        if destination not in self.destination_list:
            self.destination_list.append(destination)
        self.truck_volume -= parcel_volume

    def get_volume(self):
        """Get the remaining volume of the truck

        @type self: Truck
        @rtype: int
        """
        return self.truck_volume

    def enough_volume(self):
        """Check if the truck has enough volume for a parcel.

        @type self: Truck
        @rtype: bool
        """
        return self.truck_volume > 0

    def get_destination(self):
        """Get the destinaiton list of a truck.

        @type self: Truck
        @rtype:list
        """
        return self.destination_list

    def get_parcel(self):
        """Get the parcel list consisting of parcel_ids.

        @type self: Truck
        @rtype: list
        """
        return self.parcel_list

    def get_id(self):
        """Get the id of a truck.

        @type self: Truck
        @rtype: str
        """
        return self.truck_id

    def add_depot(self, depot):
        """Add the depot city to the destination list of Truck

        @type self: Truck
        @type depot: str
        @rtype: None
        """
        self.destination_list.append(depot)

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='.pylintrc')
    import doctest
    doctest.testmod()

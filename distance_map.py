"""Assignment 1 - Distance map (Task 1)

This module contains the class DistanceMap, which is used to store and lookup
distances between cities.  This class does not read distances from the map file.
All reading from files is done in module experiment.

Your task is to design and implement this class.

Do not import any modules here.
"""


class DistanceMap:
    """Used to store and look up distanc between cities.

    >>> d = DistanceMap()
    >>> d.store('Belleville', 'Guelph', 265)
    >>> d.load_distance('Belleville', 'Guelph')
    265
    >>> d.load_distance('Guelph', 'Belleville')
    'Unknown'
    """
    def __init__(self):
        """Initialize the dict:distance_between_cities which is used to
        store
        disance btween cities

        @rtype: None
        """
        self.distance_between_cities = {}

    def store(self, city1, city2, distance):
        """Store the distance between cities. The distance from city1 to
        city2 can be different from city2 to city1 due to reasons
        like one-way roads.

        @type city1: str
        @type city2: str
        @type distance: int
        @rtype: None
        """
        self.distance_between_cities[city1 + 'to' + city2] = distance

    def load_distance(self, city1, city2):
        """Return the distance between two cities. If the file only
        specifies a distance in one direction, the distance in the
        other direction should be considered unknown

        @type city1: str
        @type city2: str
        """
        return self.distance_between_cities.get(city1 + 'to' + city2,
                                                'Unknown')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='.pylintrc')

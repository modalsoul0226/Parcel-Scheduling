"""Assignment 1 - Running experiments (Tasks 5 & 6)

This module contains class SchedulingExperiment.  It can create an experiment
with input data and an algorithm configuration specified in a dictionary, then
run the experiment, generate statistics as the result of the experiment, and
(optionally) report the statistics.

This module is responsible for all the reading of data from the data files.

To test your code, we will construct instances of SchedulingExperiment, call
its methods, and examine the dictionary of statistics that method run
returns.

If you defined any domain classes other than Parcel and Truck, you may import
them here.  You may not import external libraries.
"""
from scheduler import RandomScheduler, GreedyScheduler
from domain import Parcel, Truck
from distance_map import DistanceMap


class SchedulingExperiment:
    """An experiment in scheduling parcels for delivery.

    To complete an experiment involves four stages:

    1. Read in all data from necessary files, and create corresponding objects.
    2. Run a scheduling algorithm to assign parcels to trucks.
    3. Compute statistics showing how good the assignment of parcels to trucks
       is.
    4. Report the statistics from the experiment.

    Precondition:
    There is always at least one parcel and one truck,
    and that at least one truck will be used. It is assumed that the map file
    contains every distance need in order to compute the statistics.
    """
    def __init__(self, config):
        """Initialize a new experiment from a configuration dictionary.

        Precondition: <config> contains keys and values as specified
        in Assignment 1.

        @type config: dict[str, str]
            The configuration for this experiment, including
            the data files and algorithm configuration to use.
        @rtype: None
        """
        self.config = config
        self.rem_parcels = None
        self.parcels = None
        self.trucks = None

    def run(self, report=False):
        """Run the experiment and return statistics on the outcome.

        If <report> is True, print a report on the statistics from this
        experiment.  Either way, return the statistics in a dictionary.

        If <self.verbose> is True, print step-by-step details
        regarding the scheduling algorithm as it runs.

        @type self: SchedulingExperiment
        @type report: bool
            Whether or not to print a report on the statistics.
        @rtype: dict[str, int | float]
            Statistics from this experiment. Keys and values are as specified
            in Step 6 of Assignment 1.
        """
        data = ['parcel_order', 'parcel_priority', 'truck_order',
                'parcel_file', 'truck_file', 'depot_location',
                'algorithm', ]
        for each in data:
            if each not in self.config:
                return 'Data not complete!'

        parcel_algm = \
            self.config['parcel_order'] + '_' + self.config['parcel_priority']
        truck_algm = self.config['truck_order']
        self.parcels = read_parcels(self.config['parcel_file'])
        self.trucks = read_trucks(self.config['truck_file'],
                                  self.config['depot_location'])
        if self.config['algorithm'] == 'random':
            random = RandomScheduler()
            self.rem_parcels = random.schedule(self.parcels, self.trucks)
        elif self.config['algorithm'] == 'greedy':
            greedy = GreedyScheduler(parcel_algm, truck_algm)
            self.rem_parcels = greedy.schedule(self.parcels, self.trucks)
        else:
            raise NameError

        if report:
            self._print_report()
        result = self._compute_stats()
        return result

    def _compute_stats(self):
        """Compute the statistics for this experiment.

        Precondition: _run has already been called.

        @type self: SchedulingExperiment
        @rtype: Dict[str, int | float]
            Statistics from this experiment. Keys and values are as specified
            in Step 6 of Assignment 1.
        """
        stats = {}
        num_of_trucks = len(self.trucks)
        stats['fleet'] = num_of_trucks

        empty_trucks = []
        used_trucks = []
        for i in self.trucks:
            if not i.get_parcel():
                empty_trucks.append(i)
            else:
                used_trucks.append(i)
        stats['unused_trucks'] = len(empty_trucks)

        total_dist = 0
        fullness = 0
        stats['unused_space'] = 0
        distance_dict = read_distance_map(self.config['map_file'])
        for j in used_trucks:
            count = 0
            sole_dist = 0
            dest_list = j.get_destination()
            if len(dest_list) == 1:
                sole_dist = 0
            while count != (len(dest_list) - 1):
                dist = distance_dict[dest_list[count] + 'to' +
                                     dest_list[count + 1]]
                sole_dist += dist
                count += 1
            total_dist += sole_dist
            sole_fullness = (j.original_volume -
                             j.get_volume()) / j.original_volume
            sole_fullness *= 100
            fullness += sole_fullness
            stats['unused_space'] += j.get_volume()

        stats['avg_distance'] = total_dist / len(used_trucks)
        stats['avg_fullness'] = fullness / len(used_trucks)
        stats['unscheduled'] = len(self.rem_parcels)
        return stats

    def _print_report(self):
        """Report on the statistics for this experiment.

        This method is *only* for debugging purposes for your benefit, so
        the content and format of the report is your choice; we
        will not call your run method with <report> set to True.

        Precondition: _compute_stats has already been called.

        @type self: SchedulingExperiment
        @rtype: None
        """
        print(self.config['parcel_order'] + '_' +
              self.config['parcel_priority'])
        print(self.config['truck_order'])
        for k in self.trucks:
            print(k.get_id(),
                  k.get_volume(), k.get_destination(), k.get_parcel())
        print('------------------')
        print(self._compute_stats())
        print('=====================================')

# ----- Helper functions -----


def read_parcels(parcel_file):
    """Read parcel data from <parcel_file> and return a list of parcel objects
    storing information regarding to parcel_id, source, destination and volume.

    @type parcel_file: str
        The name of a file containing parcel data in the form specified in
        Assignment 1.
    @rtype: list[object]
        The list containing objects storing the information
    of pacels in the parcel_file.
    """
    parcels = []
    with open(parcel_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            pid = int(tokens[0].strip())
            source = tokens[1].strip()
            destination = tokens[2].strip()
            volume = int(tokens[3].strip())
            temp = Parcel(pid, source, destination, volume)
            parcels.append(temp)

    return parcels


def read_distance_map(distance_map_file):
    """Read distance data from <distance_map_file> and return the dictionary
    containing the distance between two cities.

    @type distance_map_file: str
        The name of a file containing distance data in the form specified in
        Assignment 1.
    @rtype: Dict[str, int]
        Return the dictionary containing the distance between two cities.
    """
    distance_map = DistanceMap()
    with open(distance_map_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            c1 = tokens[0].strip()
            c2 = tokens[1].strip()
            dist = int(tokens[2].strip())
            distance_map.store(c1, c2, dist)

    return distance_map.distance_between_cities


def read_trucks(truck_file, depot_location):
    """Read truck data from <truck_file> and return a list of truck objects
    storing information regarding to truck_id, and volume.

    @type truck_file: str
        The name of a file containing truck data in the form specified in
        Assignment 1.
    @type depot_location: str
        The city where all the trucks (and packages) are at the start of the
        experiment.
    @rtype: list[object]
        Return a list of truck objects storing information
        regarding to truck_id, and volume.
    """
    trucks = []

    with open(truck_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            tid = int(tokens[0])
            capacity = int(tokens[1])
            temp = Truck(tid, capacity)
            temp.add_depot(depot_location)
            trucks.append(temp)

    return trucks


def sanity_check(config_file):
    """Configure and run a single experiment on the scheduling problem
    defined in <config_file>

    Precondition: <config_file> is a json file with keys and values
    as in the dictionary format defined in Assignment 1.

    @type config_file: str
    @rtype: None
    """
    # Read an experiment configuration from a file and build a dictionary
    # from it.
    import json
    with open(config_file, 'r') as file:
        configuration = json.load(file)
    # Create and run an experiment with that configuration.
    experiment = SchedulingExperiment(configuration)
    experiment.run(report=True)
    # experiment.run()

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='.pylintrc')

    # ------------------------------------------------------------------------
    # The following code can be used as a quick and dirty check to see if your
    # experiment can run without errors. Feel free to uncomment it for testing
    # purposes, but you should remove it before submitting your final version.
    # ------------------------------------------------------------------------
    sanity_check('data/demo.json')

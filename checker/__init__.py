
import errors

class Results:
    """
    Check results.
    Properties:
     - errors: set of check errors
     - stops_platforms_trals: list of pairs (stop, platform, trail) of route
    """
    def __init__(self):
        self.errors = set()
        self.stops_platforms_trals = []

class Stop:
    def __init__(self, osm_stop):
        self.osm_stop = osm_stop

class Platform:
    def __init__(self, osm_platform):
        self.osm_platform = osm_platform

class Check:
    def __init__(self, osm_relation, stops_reference, route_type):
        self.osm_relation = osm_relation
        self.stops_reference = stops_reference
        self.route_type = route_type
        self.stops_platforms = []
        self.results = Results()

        self._errors = {}

    def add_error(self, error_type):
        if error_type not in self._errors:
            error = errors.errors[error_type]()
            self.results.errors.add(error)
            return error
        else:
            return self._errors[error_type]

class Checker:
    @staticmethod
    def check_route_variant(osm_relation, stops_reference, route_type):
        """
        Check route variant and return resuls object.

        osm_relation: osm relation object
        stops_reference: list of stop names
        route_type: reference type of route, i.e. 'bus'
        """
        check = Check(osm_relation, stops_reference, route_type)
        Checker._get_stops(check)
        Checker._generate_stops_platforms_trails(check)

        return check.results

    @staticmethod
    def _get_stops(check):
        stop, platform = None, None
        found_ways = False

        def save_pair():
            check.stops_platforms.append(stop, platform)
            stop, platform = None, None

        for role, member in osm_relation.members:
            if found_ways and role != "":
                check.add_error("TYPE_WRONG_SORTING")

            if role in ("stop", "stop_exit_only", "stop_entry_only"):
                if stop:
                    save_pair()
                    check.add_error("TYPE_NO_PLATFORM_FOR_STOP")
                stop = Stop(member)
            elif role in ("platform", "platform_exit_only", "platform_entry_only"):
                if not stop:
                    check.add_error("TYPE_EXTRA_PLATFORM_FOR_STOP")
                else:
                    platform = Platform(member)
                    save_pair()
            elif role == "":
                if not found_ways:
                    found_ways = True
            else:
                check.add_error("TYPE_WRONG_ROLE")

    @staticmethod
    def _generate_stops_platforms_trails(check):
        check.results.stops_platforms_trals = [(stop, platform, None)
            for stop, platform in check.stops_platforms ]


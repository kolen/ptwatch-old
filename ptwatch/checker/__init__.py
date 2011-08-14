
import errors
import checks

class Results:
    """
    Check results.
    Properties:
     - errors: set of check errors
     - stops_platforms_trals: list of pairs (stop, platform, trail) of route
    """
    def __init__(self):
        self.errors = {}
        self.stops_platforms_trals = []

class Stop:
    def __init__(self, osm_stop):
        self.osm_stop = osm_stop

class Platform:
    def __init__(self, osm_platform):
        self.osm_platform = osm_platform

class Trail:
    def __init__(self):
        pass

class Check:
    def __init__(self, osm_relation, stops_reference, route_type):
        self.osm_relation = osm_relation
        self.stops_reference = stops_reference
        self.route_type = route_type
        self.stops_platforms = []
        self.stops_ids = set()
        self.ways_directions_breaks = [] # (way, direction, break_after)
        self.results = Results()

    def add_error(self, error_type):
        if error_type not in self.results.errors:
            error = errors.errors[error_type]()
            self.results.errors[error_type] = error
            return error
        else:
            return self.results.errors[error_type]

class Checker:
    @staticmethod
    def check_route(osm_relation, stops_reference, route_type):
        """
        Check route and return results object.

        osm_relation: osm relation object
        stops_reference: list of stop names
        route_type: reference type of route, i.e. 'bus'
        """
        check = Check(osm_relation, stops_reference, route_type)
        Checker._get_stops(check)
        Checker._generate_stops_platforms_trails(check)

        for c in checks.checks:
            c(check)

        return check.results

    @staticmethod
    def _get_stops(check):
        stop, platform = None, None
        found_ways = False

        for role, member in check.osm_relation.members:
            if found_ways and role != "":
                check.add_error("TYPE_WRONG_SORTING")

            if role in ("stop", "stop_exit_only", "stop_entry_only"):
                if stop:
                    check.stops_platforms.append((stop, platform))
                    check.stop_ids.add(stop.id)
                    stop, platform = None, None
                    check.add_error("TYPE_NO_PLATFORM_FOR_STOP")
                stop = Stop(member)
            elif role in ("platform", "platform_exit_only", "platform_entry_only"):
                if not stop:
                    check.add_error("TYPE_EXTRA_PLATFORM_FOR_STOP")
                else:
                    platform = Platform(member)
                    check.stops_platforms.append((stop, platform))
                    check.stops_ids.add(stop.osm_stop.id)
                    stop, platform = None, None
            elif role == "":
                if not found_ways:
                    found_ways = True
            else:
                check.add_error("TYPE_WRONG_ROLE")


    @staticmethod
    def _generate_stops_platforms_trails(check):
        check.results.stops_platforms_trals = [(stop, platform, None)
            for stop, platform in check.stops_platforms ]


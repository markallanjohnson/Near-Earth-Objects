"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import datetime


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self,
                 designation = '',
                 name = None,
                 diameter = float('nan'),
                 hazardous = False,
                 **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = designation

        self.name = name
        if self.name == '':
            self.name = None

        self.diameter = diameter
        if self.diameter == '':
            self.diameter = float('nan')
        else:
            self.diameter = float(diameter)

        self.hazardous = hazardous
        if self.hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        if self.name is not None:
            return f'{self.designation} ({self.name})'
        else:
            return f'{self.designation}'

    @property
    def danger(self):
        """ Return if a NEO is or is not hazardous """
        if self.hazardous:
            return f"potentially hazardous."
        else:
            return f"not potentially hazardous"

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} has a diameter of {self.diameter} km and is {self.danger}"


    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self,
                 designation = '',
                 time = None,
                 distance = 0.0,
                 velocity = 0.0,
                 neo = None,
                 **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = designation
        try:
            self.time = cd_to_datetime(time)
        except Exception:
            self.time = None
        else:
            self.time = cd_to_datetime(time)

        # handles distance = ""
        try:
            self.distance = float(distance)
        except Exception:
            self.distance = 0.0
        else:
            self.distance = float(distance)

        # handles velocity = ""
        try:
            self.velocity = float(velocity)
        except Exception:
            self.velocity = 0.0
        else:
            self.velocity = float(velocity)


        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        if self.time is not None:
            return datetime_to_str(self.time) # build a formatted representation of the approach time.
        else:
            return self.time

    @property
    def fullname(self):
        return self.neo.fullname

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time_str}, '{self.fullname}' approaches Earth at a distance of {self.distance} au "
                f"and a velocity of {self.velocity} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")


# from helpers.py
def cd_to_datetime(calendar_date):
    """Convert a NASA-formatted calendar date/time description into a datetime.

    NASA's format, at least in the `cd` field of close approach data, uses the
    English locale's month names. For example, December 31st, 2020 at noon is:

        2020-Dec-31 12:00

    This will become the Python object `datetime.datetime(2020, 12, 31, 12, 0)`.

    :param calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")

# from helpers.py
def datetime_to_str(dt):
    """Convert a naive Python datetime into a human-readable string.

    The default string representation of a datetime includes seconds; however,
    our data isn't that precise, so this function only formats the year, month,
    date, hour, and minute values. Additionally, this function provides the date
    in the usual ISO 8601 YYYY-MM-DD format to avoid ambiguities with
    locale-specific month names.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")

"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from filters import limit
from database import NEODatabase

db = NEODatabase()
cas = db._approaches


def write_to_csv(results= limit(cas), filename='data/neos_write.csv'):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')

    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        for row in results:
            writer.writerow((row.time,
                             row.distance,
                             row.velocity,
                             row.neo.designation,
                             row.neo.name,
                             row.neo.diameter,
                             row.neo.hazardous))

def write_to_json(results= limit(cas), filename='data/cad_write.json'):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as outfile:
        daters = []
        for ca in results:
            neo_dict = {'datetime_utc': ca.time_str,
                        'distance_au': ca.distance,
                        'velocity_km_s': ca.velocity,
                        "neo": {
                                'designation': ca.neo.designation,
                                'name': ca.neo.name,
                                'diameter_km': ca.neo.diameter,
                                'potentially_hazardous': ca.neo.hazardous
                                }
                        }
            daters.append(neo_dict)
        json.dump(daters, outfile)

write_to_json()

"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path = 'data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []

    with open(neo_csv_path, 'r') as infile:

        reader = csv.DictReader(infile)
        for line in reader:
            des, name, pha, diameter = line['pdes'], line['name'], line['pha'], line['diameter']
            neo = NearEarthObject(designation = des,
                                  name = name,
                                  diameter = diameter,
                                  hazardous = pha)
            neos.append(neo)
        return neos

def load_approaches(cad_json_path = 'data/cad.json'):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []

    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
        close_approaches = contents['data']
        for ca in close_approaches:
            ca_dict = dict(zip(contents['fields'], ca))
            des, cd, dist, v_rel = ca_dict['des'], ca_dict['cd'], ca_dict['dist'], ca_dict['v_rel']
            ca_object = CloseApproach(designation = des,
                                      time = cd,
                                      distance = dist,
                                      velocity = v_rel)
            approaches.append(ca_object)
        return approaches

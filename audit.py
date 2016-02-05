import xml.etree.cElementTree as ET
from collections import Counter, defaultdict
from sets import Set
import re
import pprint
import time

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
full_street_names = ["Street", "Avenue", "Boulevard", "Drive", "Court",
    "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Mall",
    "Terrace"]

def audit_street_type(filename):
    street_types = Counter()

    with open(filename, "r") as f:

        # Iterate over elemnts
        for _, elem in ET.iterparse(f, events=("start",)):
            if elem.tag == 'node' or elem.tag == 'way':
                # Iterate over tags for an element
                for tag in elem.iter("tag"):
                    if tag.attrib["k"] == 'addr:street':
                        # Last word/letters of street address
                        m = street_type_re.search(tag.attrib["v"])
                        if m:
                            # Add ending to dictionary
                            street_type = m.group()
                            if street_type not in full_street_names:
                                street_types[street_type] += 1

    return street_types

def audit_node_tag_types(filename):
    tag_types = Counter()

    with open(filename, "r") as f:
        for _, elem in ET.iterparse(f, events=("start",)):
            if elem.tag == 'node':
                # Iterate over tags for an element
                for tag in elem.iter("tag"):
                    tag_types[tag.attrib["k"]] += 1

    return tag_types

def auit_addr_tag_types(filename):
    tag_types = defaultdict(Set)

    with open(filename, "r") as f:
        for _, elem in ET.iterparse(f, events=("start",)):
            if elem.tag == 'node':
                # Iterate over tags for an element
                for tag in elem.iter("tag"):
                    if "addr" in tag.attrib["k"]:
                        if tag.attrib["k"] in tag_types:
                            if tag.attrib["v"] not in tag_types[tag.attrib["k"]]:
                                tag_types[tag.attrib["k"]].append(tag.attrib["v"])
                        else:
                            tag_types[tag.attrib["k"]] = [tag.attrib["v"]]

    return tag_types

def audit_state_mn_zip(filename):
    zips = []
    for n in range(1,10): zips.append("5540" + str(n))
    for n in range(10, 89): zips.append("554" + str(n))

    states = Set()

    _in = 0
    not_in = 0

    with open(filename, "r") as f:
        for _, elem in ET.iterparse(f, events=("start",)):
            if elem.tag == 'node':
                # Iterate over tags for an element
                for tag in elem.iter("tag"):
                    if "addr:postcode" == tag.attrib["k"]:
                        value = tag.attrib["v"]
                        if value in zips:
                            _in += 1
                        else:
                            not_in += 1

                    elif "addr:state" == tag.attrib["k"]:
                        states.add(tag.attrib["v"])

    print (_in, not_in, states)

def audit_amenity_tag(filename):
    tag_types = Counter()

    with open(filename, "r") as f:
        for _, elem in ET.iterparse(f, events=("start",)):
            if elem.tag == 'node':
                # Iterate over tags for an element
                for tag in elem.iter("tag"):
                    if "amenity" in tag.attrib["k"]:
                        tag_types[tag.attrib["v"]] += 1

    return tag_types

def test():
    osm_file = "minneapolis-saint-paul_minnesota.osm"

    start = time.time()
    #street_types = audit_street_type(osm_file)
    #tag_types = audit_node_tag_types(osm_file)
    #addr_met_tags = auit_addr_tag_types(osm_file)
    audit_state_mn_zip(osm_file)
    #amenity_tags = audit_amenity_tag(osm_file)
    end = time.time()

    #pprint.pprint(dict(amenity_tags))
    print "Audit took {0} seconds".format((end-start))

if __name__ == '__main__':
    test()
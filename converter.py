#!/usr/local/bin/python
import sys
import json
import requests
import config
import re
import numpy as np

# curl -k -H "Authorization: Bearer {myToken}" https://stash.site.local/rest/api/1.0/projects/{name}/repos/{destination}/raw/{path}.properties?at=refs/heads/master

if __name__ == '__main__':

    # get code from gitlab repo
    myToken = config.KEY
    myUrl = 'https://stash.site.local/rest/api/1.0/projects/{name}/repos/{destination}/raw/{path}.properties?at=refs/heads/master'
    head = {'Authorization': myToken}

    r = requests.get(myUrl, headers=head, verify=False)

    # # sanity check log
    print(r.status_code, r.reason)
    
    # # set path for where to write the code from the request
    path = "test.properties"
    #
    # # write the curl request to the path file
    with open(path, 'w') as outfile:
        outfile.write(str(r.content))

    # convert the java.properties file to a JSON format
    text_file = open((path + ".json"), "w")
    f = open(path)
    lines = f.read().splitlines()
    f.close()

    # separate num.name value from other values
    regex = re.findall("^\d+\.name", '\n'.join(lines), re.MULTILINE)

    # get only num from num.name
    only_numbers = ', '.join(regex).replace('.name', '').split(', ')
    
    # combines related data based off of num.name into respective arrays
    def group_by_flaw_number(file_data):
        # add function here

    related_data_arrays = group_by_flaw_number(lines)


    def create_objs():
        # add function here

    create_objs()

    text_file.close()

    print "wrote to", (path + ".json")

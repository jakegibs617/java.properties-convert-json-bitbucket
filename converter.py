#!/usr/local/bin/python
import sys
import json
import requests
import config
import re
# curl -k -H "Authorization: 
Bearer {myToken}" https://stash.site.local/rest/api/1.0/projects/{name}/repos/{destination}/raw/{path}.properties?at=refs/heads/master
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
    
# combines related data based off of num.name into respective arrays
def group_by_flaw_number(file_data):
    arr = []
    length = len(file_data)
    prev = None
    all_nums = []
    indices = []
    
    # get first index of num
    for index, data in enumerate(file_data):
        flaw_num = ''.join(re.findall("^\d+|^-\d+", ''.join(data)))
        all_nums.append(flaw_num)
        if flaw_num.strip() != '':
            first_index = all_nums.index(flaw_num)
            indices.append(int(first_index))
            
    # get last index of num
    for index, data in enumerate(file_data):
        flaw_num = ''.join(re.findall("^\d+|^-\d+", ''.join(data)))
        if flaw_num.strip() != '':
            last_index = length - all_nums[::-1].index(flaw_num) - 1
            indices.append(int(last_index))
    removed_sorted_indices = sorted(list(dict.fromkeys(indices)))
    
    # slice out from first to last index of the flaw number
    for index, i in enumerate(removed_sorted_indices):
        if prev != None:
            arr.append(file_data[prev:i + 1])
        prev = i
    return arr

related_data_arrays = group_by_flaw_number(lines)

def create_objs():
    data = {}
    for index, arrays in enumerate(related_data_arrays):
        # get flaw num by num.name field
        flaw_num_name = ''.join(re.findall("^\d+.name|^-\d+.name", ''.join(arrays)))
        flaw_num      = flaw_num_name.replace('.name', '')
        # need to get even arrays only
        if index % 2 == 0:
            data = {
                flaw_num : {}
            }
            obj = {}
            for line in arrays:
                # skip comments
                if line.startswith( '#' ): continue
                arr = line.split('=')
                key = arr[0].strip()
                key = key.replace(flaw_num+'.', '')
                val = arr[1].strip()
                obj[key] = val
            data = {
                flaw_num : obj
            }
            j_data = json.dumps(data, indent=4, separators=(',', ': '))
            text_file.write(j_data)
            
create_objs()

text_file.close()

print "wrote to", (path + ".json")

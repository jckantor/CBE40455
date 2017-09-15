# Script to read list of groups from a csv and create them on the portal.
from arcgis.gis import *
import argparse
import csv

try:
    #region read cmd line args
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Portal url of the form: https://portalname.domain.com/webadaptor')
    parser.add_argument('-u','--user', help='Administrator username', default='admin')
    parser.add_argument('-p','--password', help='Administrator password', default='x]984<ngb3!')
    parser.add_argument('-l', '--log', help='Path to log file', default='python_process.log')

    args = parser.parse_args()
    #endregion

    # Read the log file in append mode
    log_file = open(args.log, 'a')

    log_file.write("\n")
    log_file.write("=====================================================================\n")
    log_file.write("CREATING GROUPS")

    # connect to gis
    gis = GIS(args.url, args.user, args.password)

    with open("groups.csv", 'r') as groups_csv:
        groups = csv.DictReader(groups_csv)
        for group in groups:
            try:
                log_file.write("\nCreating group: "+ group['title'] + "  ##  ")
                result = gis.groups.create_from_dict(group)
                if result:
                    log_file.write("success")

            except Exception as create_ex:
                print("Error... ", str(create_ex))

    log_file.close()
    print("0")
except:
    print("1")
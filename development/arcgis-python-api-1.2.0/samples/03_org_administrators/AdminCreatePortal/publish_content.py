# Publisher persona
# Script to publish content for each user.

from arcgis.gis import *
import csv
import json
import argparse

try:
    #region read cmd line args
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Portal url of the form: https://portalname.domain.com/webadaptor')
    parser.add_argument('-u','--user', help='Administrator username', default='admin')
    parser.add_argument('-p','--password', help='Administrator password', default='x]984<ngb3!')
    parser.add_argument('-l','--log', help='Path to log file',default='python_process.log')

    args = parser.parse_args()
    #endregion

    # Read the csv containing user accounts and their territory info
    csv_path = "users.csv"

    # Read the log file in append mode
    log_file = open(args.log, 'a')
    log_file.write("\n")
    log_file.write("=====================================================================\n")
    log_file.write("PUBLISHING USER CONTENT")

    # Read template web map
    template_webmap_dict = dict()
    with open('user_content/web_map.json', 'r') as webmap_file:
                template_webmap_dict = json.load(webmap_file)

    # Connect to the GIS
    gis = GIS(args.url, args.user, args.password)

    # Loop through each user and publish the content
    with open(csv_path, 'r') as csv_handle:
        reader = csv.DictReader(csv_handle)
        for row in reader:
            try:
                data_to_publish = 'user_content/' + row['assigned_state'] + ".csv"

                log_file.write("\nPublishing " + data_to_publish + " # ")
                added_item = gis.content.add({}, data = data_to_publish)
                published_item = added_item.publish()

                if published_item is not None:
                    # publish web map
                    log_file.write('webmaps' + " ## ")
                    user_webmap_dict = template_webmap_dict
                    user_webmap_dict['operationalLayers'][0].update({'itemId': published_item.itemid,
                                                                     'layerType': "ArcGISFeatureLayer",
                                                                     'title': published_item.title,
                                                                     'url': published_item.url + r"/0"})

                    web_map_properties = {'title': '{0} {1} response locations'.format(row['Firstname'], row['Lastname']),
                                          'type': 'Web Map',
                                          'snippet': 'Regions under the supervision of' +\
                                                     '{0} {1}'.format(row['Firstname'], row['Lastname']),
                                          'tags': 'ArcGIS API for Python',
                                          'typeKeywords': "Collector, Explorer Web Map, Web Map, Map, Online Map",
                                          'text': json.dumps(user_webmap_dict)}

                    web_map_item = gis.content.add(web_map_properties)

                    #Reassign ownership of items to current user. Transfer webmaps in a new
                    # folder with user's last name
                    log_file.write("success. Assigning to: " + "  #  ")
                    result1 = published_item.reassign_to(row['username'])
                    new_folder_name = row['Lastname'] + "_webmaps"
                    result2 = web_map_item.reassign_to(row['username'], target_folder=new_folder_name)

                    #share webmap to user's groups
                    groups_list1 = row['groups'].split(',')
                    groups_list = [gname.lstrip() for gname in groups_list1] #remove white spaces in name
                    result3 = web_map_item.share(groups=groups_list)
                    if (result1 and result2 and result3) is not None:
                        log_file.write(row['username'])
                    else:
                        log_file.write("error")
                else:
                    log_file.write(" error publishing csv")

            except Exception as pub_ex:
                log_file.write("Error : " + str(pub_ex))
    log_file.close()
    print("0")
except Exception as global_ex:
    print("1")
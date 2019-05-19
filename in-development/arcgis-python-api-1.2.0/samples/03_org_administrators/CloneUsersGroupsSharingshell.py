from __future__ import print_function
#
#   This example demonstrates how to stage a new Portal with user accounts,
#     Groups, and Group Memebership in order to establish a shell of a Portal
#     that is "ready to go" for users to start contributing content.
#
#   This copies all Users accounts, Groups, Group Sharing, and Group membership
#     from a source Portal to a target Portal.
#
#   This assumes that the Target Portal is a new, clean installation and there
#     would be no conflicts of usernames or group names during the copy process.
#
#   This script does NOT copy any User content.
#

import sys
import six
from arcgis.gis import *

if six.PY3:
    from urllib.error import URLError
else:
    # unresolved reference in Python3, but should work if running from Python2
    from urllib2 import URLError

def copy_user(target, user, password):
    # See if the user has firstName and lastName properties
    try:
        firstname = user.firstName
        lastname = user.lastName
    except:
        # if not, split the fullName
        fullName = user.fullName
        firstname = fullName.split()[0]
        try:
            lastname = fullName.split()[1]
        except:
            lastname = ' '

    try:
        testuser = target.users.get(user.username)
        if not testuser is None:
            print("\tUsername {} already exists in Target Portal; skipping user creation.\n".format(user.username))
            return testuser

        target_user = target.users.create(user.username, password, firstname, lastname,
                                          user.email, user.description, user.role, user.provider, user.idpUsername)

        # update user properties from existing user
        target_user.update(user.access, user.preferredView,
                           user.description, user.tags, user.get_thumbnail_link(),
                           culture=user.culture, region=user.region)

        # update user role; assumes no custom roles
        if 'role' in user and not user.role == 'org_user':
            target_user.update_role(user.role)

        return target_user

    except:
        print("Unable to create user "+ user.username)
        return None

def copy_group(target, source, group):
    ''' Copy group to the target portal.'''
    GROUP_COPY_PROPERTIES = ['title', 'description', 'tags', 'snippet', 'phone', 'access', 'isInvitationOnly']
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a new groups with the subset of properties we want to
        # copy to the target portal. Handle switching between org and
        # public access when going from an org in a multitenant portal
        # and a single tenant portal
        target_group = {}

        for property_name in GROUP_COPY_PROPERTIES:
            target_group[property_name] = group[property_name]

        if target_group['access'] == 'org' and target.properties['portalMode'] == 'singletenant':
            target_group['access'] = 'public'
        elif target_group['access'] == 'public' and source.properties['portalMode'] == 'singletenant' \
             and target.properties['portalMode'] == 'multitenant' and 'id' in target.properties: # is org
            target_group['access'] = 'org'

        # Handle the thumbnail (if one exists)
        thumbnail_file = None
        if 'thumbnail' in group:
            target_group['thumbnail'] = group.download_thumbnail(temp_dir)

        # Create the group in the target portal
        copied_group = target.groups.create_from_dict(target_group)

         # Reassign all groups to correct owners, add users, and find shared items
        members = group.get_members()
        copied_group.reassign_to(members['owner'])
        if members['users']:
            copied_group.add_users(members['users'])

        # remove the admin user copying this group from the copied group if that
        #   username is not part of the group in the Source Portal
        if not target.users.me.username in members['users']:
            copied_group.remove_users(target.users.me.username)

        return copied_group

# Wrap source GIS connection with error handling to determine why it may fail
try:
    source = GIS("https://gleneagle.esri.com:7443/arcgis", "portaladmin", "secretpwd")
except URLError as e:
    sys.exit("Invalid Source Portal URL...")
except RuntimeError as e2:
    sys.exit("Invalid Source Portal username/password...")

# Wrap target GIS connection with error handling to determine why it may fail
try:
    target = GIS("https://ps002233.esri.com/portal", "portaladmin", "secretpwd", verify_cert=False)
except URLError as e:
    sys.exit("Invalid Taget Portal URL...")
except RuntimeError as e2:
    sys.exit("Invalid Target Portal username/password...")

# Get all users from the Source Portal; set max_users to make sure you get all users
sourceusers = source.users.search(max_users=500)

# Create a list of "system" Portal users that we will ignore during copy
systemusers = ['system_publisher', 'esri_nav', 'esri_livingatlas', 'esri_boundaries', 'esri_demographics', str(source.users.me.username)]

for user in sourceusers:
    if not user.username in systemusers:
        print('Copying {}...'.format(user.username))
        if user.provider == 'arcgis':
            copy_user(target, user, 'TestPassword@123')
        elif user.provider == 'enterprise':  # web tier authenticated users
            copy_user(target, user, 'NoPwdUsed')

# Get list of groups from the Source Portal and also from Target Portal (for cleanup purposes)
sourcegroups = source.groups.search()
targetgroups = target.groups.search()

# Create a list of "system" Portal Groups that we will ignore during copy
systemgroups = ['Navigator Maps', 'Featured Maps and Apps']

# Let's make sure in our Target Portal, existing Groups don't already exist.
#   This is useful in testing and cleaning up Groups before trying again.
#   The assumption is this script is copying to a new, clean Portal.
for tg in targetgroups:
    for sg in sourcegroups:
        if sg.title == tg.title and (not tg.owner in systemusers) and (not tg.title in systemgroups):
            print("Cleaning up group {} in target Portal...".format(tg.title))
            tg.delete()
            break

for grp in sourcegroups:
    if not grp.title in systemgroups:
        print('Copying Group {}...'.format(grp.title))
        tgt_group = copy_group(target, source, grp)



"""
This script creates a followers network for a given user

Authors
-------
Roberto Maestre Martinez - rmaestre@paradigmatecnologico.com
F. Javier Alba - fjalba@paradigmatecnologico.com

Paradigma labs 2012. http://labs.paradigmatecnologico.com/
"""

import requests
import json
import sys

MAX_IDS = 1000
MAX_RECURSION_LEVEL = 2

class RateLimitReachedError(Exception):
    pass

def obtain_users_info(ids = [], screen_names=[]):
    check_rate_limit()
    result = []
    #transform ids into strings:
    ids = map(lambda x: str(x), ids)
    string_ids = ','.join(ids)
    screen_names = ','.join(screen_names)
    url = 'https://api.twitter.com/1/users/lookup.json?'
    if string_ids and screen_names:      
        url += 'user_id=%s&screen_name=%s' % (string_ids, screen_names)
    elif string_ids:
        url += 'user_id=%s' % string_ids
    else:
        url += 'screen_name=%s' % screen_names
    print url
    content = requests.get(url).content
    data = json.loads(content)
    if 'error' in data:
        print 'Error: %s' % data['error']
        return
    for user_info in data:
        relevant_info = {
            'screen_name' : user_info['screen_name'],
            'profile_image_url': user_info['profile_image_url'],
            'followers_count': user_info['followers_count'],
            'indegree' : 0
        }
        result.append(relevant_info)
    return result

#generar tsv
def generate_tsv (follower_network, user_name, min_indegree):
    tsv_output = open('%s_follower_network.tsv' % user_name, 'w')
    #edge_size is always 1 in this example
    edge_size = 1
    for (origin_name, target_name) in follower_network['edges']:
        origin_info = follower_network['nodes'][origin_name]
        target_info = follower_network['nodes'][target_name]
        if (origin_info['indegree'] > min_indegree and target_info['indegree'] > min_indegree):     
            line = '%s\t%s\t%s\t%s\t%s\t%s\t%s' % ( origin_name, 
                                                        origin_info['followers_count'],
                                                        origin_info['profile_image_url'],
                                                        target_name,
                                                        target_info['followers_count'],
                                                        target_info['profile_image_url'],
                                                        edge_size
                                                    )
            tsv_output.write("%s\n" % line)      
    tsv_output.close()

#generate dot
def generate_dot(follower_network, user_name, min_indegree):
    dot_output = open('%s_follower_network.dot' % user_name, 'w')
    network_str = ''
    for (origin_name, target_name) in follower_network['edges']:
        origin_info = follower_network['nodes'][origin_name]
        target_info = follower_network['nodes'][target_name]
        if (origin_info['indegree'] > min_indegree and target_info['indegree'] > min_indegree):
            network_str += '\t%s -> %s\n' % (origin_name, target_name)
    
    dot_output.write('digraph G{\n%s}' % network_str)
    dot_output.close()

def check_rate_limit():
    url = 'https://api.twitter.com/1/account/rate_limit_status.json'
    content = requests.get(url).content
    data = json.loads(content)
    remaining = data['remaining_hits']
    if  remaining == 0:
        raise RateLimitReachedError()
    else: print "remaining_hits = %s" % str(remaining)

def traverse_followers(user_name, follower_network, recursion_level, max_recursion_level):
    check_rate_limit()
    # retrieve up to MAX_IDS user followers:
    url = 'https://api.twitter.com/1/followers/ids.json?screen_name=%s&cursor=-1' % user_name
    print url
    content = requests.get(url).content
    data = {}
    try:
        data = json.loads(content)
    except:
        print 'Error! rate limit?'
        return

    if 'error' in data:
        print 'Error: %s' % data['error']
        return

    followers_ids = data['ids'][:MAX_IDS]

    #obtain info for each follower (in batches of 100)
    for i in range(0, len(followers_ids), 100):
        id_group = followers_ids[i:i+100]
        followers_info = obtain_users_info(ids = id_group)
        if followers_info is not None:
            for follower_info in followers_info:
                follower_name = follower_info['screen_name']
                #add node info (if not exists yet)
                if follower_name not in follower_network['nodes']:
                    follower_network['nodes'][follower_name] = follower_info
                #add edge
                follower_network['edges'].append((follower_name, user_name))
                follower_network['nodes'][user_name]['indegree'] += 1
                if recursion_level < max_recursion_level:
                    traverse_followers(follower_name, follower_network, recursion_level+1, max_recursion_level)

if __name__ == "__main__":
    # USER
    # obtain main user info
    main_user_name = sys.argv[1]
    main_user_info = obtain_users_info(screen_names=[main_user_name])[0]

    follower_network =  {   'nodes' : {},
                            'edges': []
                        }
    follower_network['nodes'][main_user_name] = main_user_info

    try:
        traverse_followers(main_user_name, follower_network, 1, MAX_RECURSION_LEVEL)
    except RateLimitReachedError as e:
        print "Ooops! we reached the rate limit!!! Follower Network will not be complete."
    except:
        print "Some error occurred!. We will go on with the current Follower Network!"

    #pp(follower_network)

    generate_tsv(follower_network, main_user_name, 1)
    generate_dot(follower_network, main_user_name, 0)
    

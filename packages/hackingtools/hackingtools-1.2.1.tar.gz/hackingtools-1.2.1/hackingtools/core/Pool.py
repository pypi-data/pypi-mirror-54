from . import Config, Logger, Utils
if Utils.amIdjango(__name__):
    from core.library import hackingtools as ht
else:
    import hackingtools as ht
from django.urls import resolve
from colorama import Fore
import sys, requests, json

# Nodes Pool Treatment

nodes_pool = []
MY_NODE_ID = Utils.randomText(length=32, alphabet='mixalpha-numeric-symbol14')

def switchPool():
    ht.switchPool()

def addNodeToPool(node_ip):
    global nodes_pool
    if node_ip and not node_ip in nodes_pool:
        nodes_pool.append(node_ip)

def send(node_request, functionName):
    creator_id = MY_NODE_ID
    pool_nodes = getPoolNodes()
    try:
        if ht.wantPool():
            function_api_call = resolve(node_request.path_info).route
            pool_it = node_request.POST.get('__pool_it_{func}__'.format(func=functionName), False)
            if pool_it:
                if pool_nodes:
                    params = dict(node_request.POST)
                    if 'pool_list' in params:
                        if not params['pool_list']:
                            params['pool_list'] = []
                    if not 'creator' in params:
                        params['creator'] = creator_id
                    response, creator = __sendPool__(creator=params['creator'], function_api_call=function_api_call, params=dict(params), files=node_request.FILES)
                    
                    global nodes_pool
                    for n in nodes_pool:
                        # Call to inform about my services
                        for serv in ht.Connections.getMyServices():
                            service_for_call = '{node_ip}/core/pool/add_pool_node/'.format(node_ip=n)
                            add_me_to_theis_pool = requests.post(service_for_call, data={'pool_ip':serv},  headers=ht.Connections.headers)
                            if add_me_to_theis_pool.status_code == 200:
                                Logger.printMessage(message="send", description='Saving my service API REST into {n} - {s} '.format(n=n, s=serv), color=Fore.YELLOW)

                    if 'creator' in params and params['creator'] == creator_id and response:
                        if isinstance(response, str):
                            return ({ 'res' : response, 'nodes_pool' : nodes_pool }, False)
                        if isinstance(response, dict):
                            data = { 'res' : response['data'], 'nodes_pool' : nodes_pool }
                            return (data, False)
                        return (str(response.text), False)
                    if response:
                        return (response, creator) # Repool
                    return (None, None)
                else:
                    return (None, None)
            else:
                return (None, None)
        else:
            Logger.printMessage(message='send', description='Disabled pool... If want to pool, change WANT_TO_BE_IN_POOL to true', color=Fore.YELLOW)
            return (None, None)
    except Exception as e:
        raise
        Logger.printMessage(message='send', description=str(e), is_error=True)
        return (None, None)

def __sendPool__(creator, function_api_call='', params={}, files=[]):
    # We have 3 diferent nodes list:
    #   1- nodes_pool : We know those nodes for any call
    #   2- pool_list : is inside params['pool_list'] and has the list of all pools that know this pool request
    #   3- nodes : Are the nodes we can call from out nodes_pool and that the aren't inside pool_list
    # Finally we add all pool_list nodes that aren't inside our nodes_pool to nodes_pool list

    global nodes_pool

    nodes = [] # Nodes to send this call. Thay have to be nodes that haven't received this yet.
    pool_list = [] # The pool_list is a list for getting all the nodes that have been notified by this call.

    mine_function_call = False

    try:
        pool_list = params['pool_list']
        for service in ht.Connections.getMyServices():
            if service in pool_list:
                mine_function_call = True
                Logger.printMessage(message='__sendPool__', description='It\'s my own call', color=Fore.YELLOW)
                return (None, None)
    except:
        pass
    
    nodes = nodes_pool
    if pool_list:
        nodes = list(set(nodes_pool) - set(pool_list))

    # Get all nodes in pool_list as known for us if we don't have any
    if not nodes_pool:
        nodes_pool = pool_list

    # I save pool_list items i don't have yet on my pools

    nodes_pool = nodes_pool + list(set(pool_list) - set(nodes_pool))

    my_own_call = False

    if pool_list:
        for service in ht.Connections.getMyServices():
            if service in pool_list:
                my_own_call = True
                pool_list.remove(service)

    # Remove any posible service with my public, local or lan IP
    if nodes_pool:
        for service in ht.Connections.getMyServices():
            removeNodeFromPool(service)

    if len(nodes) > 0:
        if not mine_function_call and not my_own_call:
            for node in nodes:
                try:
                    if ht.Connections.serviceNotMine(node):
                        node_call = '{node_ip}/pool/execute/'.format(node_ip=node)

                        params['pool_list'] = pool_list

                        for serv in ht.Connections.getMyServices():
                            params['pool_list'].append(serv)
                            
                        params['is_pool'] = True

                        params['functionCall'] = function_api_call
                        
                        r = requests.post(node_call, files=files, data=params, headers=dict(Referer=node))

                        if r.status_code == 200:
                            for n in pool_list:
                                if ht.Connections.serviceNotMine(n) and not n == node:
                                    addNodeToPool(n)
                            Logger.printMessage(message='__sendPool__', description=('Solved by {n}'.format(n=node)))
                            return (json.loads(str(r.text)), params['creator'])

                except Exception as e:
                    Logger.printMessage(message='__sendPool__', description=str(e), color=Fore.YELLOW)
        else:
            Logger.printMessage(message='__sendPool__', description='Returned to me my own function called into the pool', debug_module=True)
    else:
        Logger.printMessage(message='__sendPool__', description='There is nobody on the pool list', debug_module=True)

    return (None, None)

def getPoolNodes():
    global nodes_pool
    return nodes_pool

def removeNodeFromPool(node_ip):
    global nodes_pool
    if node_ip in nodes_pool:
        nodes_pool.remove(node_ip)

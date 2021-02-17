import re, json

def convertToJson(report:dict) -> json:
    return json.dumps(report, indent=4)

def reportOs(systems:list) -> dict:
    host_to_os = dict()
    for system in systems:
        hostname = system.getHostname()
        os = system.getOs()
        host_to_os[hostname] = os
    return host_to_os

def reportOsReverse(systems:list) -> dict:
    os_to_host = dict()
    for system in systems:
        hostname = system.getHostname()
        os = system.getOs()
        if (os not in os_to_host.keys()):
            os_to_host[os] = [hostname]
        elif (os in os_to_host.keys()):
            os_to_host[os].append(hostname)
    return os_to_host



def reportHardware(systems:list) -> dict:
    host_to_hardware = dict()
    for system in systems:
        hostname = system.getHostname()
        hardware = system.getHardware()
        host_to_hardware[hostname] = hardware
    return host_to_

def reportHardwareReverse(systems:list) -> dict:
    hardware_to_host = dict()
    for system in systems:
        hostname = system.getHostname()
        hardware = system.getHardware()
        if (hardware not in hardware_to_host.keys()):
            hardware_to_host[hardware] = [hostname]
        else:
            hardware_to_host[hardware].append(hostname)
    return hardware_to_host



def reportNetworkAdaptersAndWlans(systems:list) -> dict:
    host_to_network = dict()
    for system in systems:
        hostname = system.getHostname()
        wlans = system.getNetworkWlans()
        adapters = system.getNetworkAdapters()
        if (hostname not in host_to_network.keys()):
            host_to_network[hostname] = {'wlans': [], 'adapters': []}
        host_to_network[hostname]['wlans'] = wlans
    return host_to_network

def reportNetworkAdapters(systems:list) -> dict:
    host_to_adapters = dict()
    for system in systems:
        hostname = system.getHostname()
        adapters = system.getNetworkAdapters()
        host_to_adapters[hostname] = adapters
    return host_to_adapters

def reportWlans(systems:list) -> dict:
    host_to_wlans = dict()
    for system in systems:
        hostname = system.getHostname()
        wlans = system.getNetworkWlans()
        host_to_wlans[hostname] = wlans
    return host_to_wlans



def reportUsers(systems:list) -> dict:
    host_to_users = dict()
    for system in systems:
        hostname = system.getHostname()
        users = system.getUsers()
        host_to_users[hostname] = users
    return host_to_users 

def reportUsersReverse(systems:list) -> dict:
    user_to_host = dict()
    for system in systems:
        hostname = system.getHostname()
        users = system.getUsers()
        for user in users:
            if (user not in user_to_host.keys()):
                user_to_host[user] = [hostname]
            else:
                user_to_host[user].append(hostname)
    return user_to_host

def reportAdmins(systems:list) -> dict:
    host_to_admins = dict()
    for system in systems:
        hostname = system.getHostname()
        admins = system.getAdmins()
        host_to_admins[hostname] = admins
    return host_to_admins

def reportAdminsReverse(systems:list) -> dict:
    admin_to_host = dict()
    for system in systems:
        hostname = system.getHostname()
        admins = system.getAdmins()
        for admin in admins:
            if (admin not in admin_to_host.keys()):
                admin_to_host[admin] = [hostname]
            else:
                admin_to_host[admin].append(hostname)
    return admin_to_host

def reportDefaultUsers(systems:list) -> dict:
    host_to_users = dict()
    for system in systems:
        hostname = system.getHostname()
        users = system.getDefaultUsers()
        host_to_users[hostname] = users
    return host_to_users

def reportDefaultUsersReverse(systems:list) -> dict:
    user_to_host = dict()
    for system in systems:
        hostname = system.getHostname()
        users = system.getDefaultUsers()
        for user in users:
            if (user not in user_to_host.keys()):
                user_to_host[user] = [hostname]
            else:
                user_to_host[user].append(hostname)
    return user_to_host



def reportPrograms(systems:list) -> dict:
    host_to_programs = dict()
    for system in systems:
        hostname = system.getHostname()
        programs = system.getPrograms()
        host_to_programs[hostname] = programs
    return host_to_programs

def reportProgramsReverse(systems:list) -> dict:
    program_to_host = dict()
    for system in systems:
        hostname = system.getHostname()
        programs = system.getPrograms()
        for program, version in programs.items():
            key = ', '.join([program,version])
            if (key not in program_to_host.keys()):
                program_to_host[key] = [hostname]
            else:
                program_to_host[key].append(hostname)
    return program_to_host

def reportHostsWithIdenticalPrograms(systems:list) -> list: #Returns List of Sets e.g., [{}]
    program_to_host = reportProgramsReverse(systems)
    hostsWithSharedPrograms = []
    for hosts in program_to_host.values():
        if (hosts not in hostsWithSharedPrograms):
            hostsWithSharedPrograms.append(hosts)
    
    host_to_programs = reportPrograms(systems)
    hostsToCompare = convertToHostsForComparison(hostsWithSharedPrograms)
    matchingHosts = dict()
    for host1, host2 in hostsToCompare.items():
        if (programsAreIdentical(host_to_programs[host1], host_to_programs[host2])):
            if (not hostPairExists(matchingHosts, host1, host2)):
                matchingHosts[host1] = host2
    
    hostSetsIdentical = []
    hostGroups = groupMatchingHosts(matchingHosts)
    if (hostGroups):
        for key in hostGroups:
            hostSet = hostGroups[key]
            hostSetsIdentical.append(hostSet)

    return hostSetsIdentical

def programsAreIdentical(hostOnePrograms:dict, hostTwoPrograms:dict) -> bool:
    for key, val in hostOnePrograms.items():
        if (key in hostTwoPrograms):
            continue
        else:
            return False
    for key, val in hostTwoPrograms.items():
        if (key in hostOnePrograms):
            continue
        else:
            return False
    return True

def reportHostsWithUniquePrograms(systems:list) -> set:
    hosts = set()
    for system in systems:
        hosts.add(system.getHostname())
    hostSetsIdentical = reportHostsWithIdenticalPrograms(systems)
    hostSetIdenticalUnion = set()
    for hostSet in hostSetsIdentical:
        for host in hostSet:
            hostSetIdenticalUnion.add(host)
    hostSetUnique = hosts.difference(hostSetIdenticalUnion)
    return hostSetUnique

def programsDifference(hostOnePrograms:dict, hostTwoPrograms:dict) -> set: #Host 1 minus Host 2
    hostOneProgramsSet = set()
    for program, version in hostOnePrograms.items():
        hostOnePrograms.add(program)

    hostTwoProgramsSet = set()
    for program, version in hostOnePrograms.items():
        hostTwoPrograms.add(program)

    difference = hostOneProgramsSet.difference(hostTwoProgramsSet)
    return difference



def reportServices(systems:list) -> dict:
    host_to_services = dict()
    for system in systems:
        hostname = system.getHostname()
        services = system.getServices()
        host_to_services[hostname] = services
    return host_to_services
#LEFT OFF HERE. Complete front-end, get better idea of visual display needs, come back and refine functions based on GUI expectations
def reportServicesReverse(systems:list) -> dict:
    return



def groupMatchingHosts(matchingHosts:dict) -> dict:
    hostGroups = dict()
    groupCounter = 1

    for host1, host2 in matchingHosts.items():
        
        key = findKeyForHostInNestedHostDict(host1, hostGroups)
        if (key == ""):
            key = "group" + str(groupCounter)
            hostGroups[key] = {host1, host2}
            groupCounter += 1
        elif (key != ""):
            hostGroups[key].add(host2)
        
        key = findKeyForHostInNestedHostDict(host2, hostGroups)
        if (key == ""):
            key = "group" + str(groupCounter)
            hostGroups[key] = {host2, host1}
        elif (key != ""):
            hostGroups[key].add(host1)
    return hostGroups #Returns a dictionary with Set values

def findKeyForHostInNestedHostDict(host:str, hostGroups:dict) -> str:
    key = ""
    if (hostGroups == {}):
        return key
    else:
        for group in hostGroups:
            if host in hostGroups[group]:
                key = group
    return key

def convertToHostsForComparison(hostsWithSharedProperties:list) -> dict:
    #parameter should be list of lists
    hostsToCompare = dict()
    for hosts in hostsWithSharedProperties:
        length = len(hosts)
        for i in range(length):
            for j in range(length):
                host1 = hosts[i]
                host2 = hosts[j]
                if (host1 != host2):
                    if (not hostsToCompare):
                        hostsToCompare[hosts[i]] = hosts[j]
                    elif (not hostPairExists(hostsToCompare, host1, host2)):
                        hostsToCompare[hosts[i]] = hosts[j]
    return hostsToCompare

def hostPairExists(hostsToCompare:dict, host1:str, host2:str) -> bool:
    if (host1 in hostsToCompare and hostsToCompare[host1] == host2):
        return True
    elif (host2 in hostsToCompare and hostsToCompare[host2] == host1):
        return True
    else:
        return False



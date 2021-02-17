import re

class WinSys:
    def __init__(self, data:list, option:str): #Option = 'cli' or 'script'
        self.sections = parseData(data, option)
        
        self.configs = {
            'sectionOne': parseSystemSpecifications(self.sections[1]),
            'sectionTwo': parseNetworkInformation(self.sections[2]),
            'sectionThree' : parseLocalUsers(self.sections[3]),
            'sectionFour' : parseLocalGroup(self.sections[4]),
            'sectionFive' : parseDefaultUsers(self.sections[5]),
            'sectionSix' : parsePrograms(self.sections[6]),
            'sectionSeven' : parseServices(self.sections[7]),
            'sectionEight' : parseListeningPorts(self.sections[8]),
            'sectionNine' : parseGpresult(self.sections[9]),
            'sectionTen' : parseSecurityPolicies(self.sections[10]),
            'sectionEleven': parseSecurityUpdates(self.sections[11]),
            'sectionTwelve': parseTimeSettings(self.sections[12]),
            'sectionThirteen': parseScreenSaverSettings(self.sections[13]),
            'sectionFourteen': parseRdpSecurityLevel(self.sections[14]),
            'sectionFifteen': parseInactiveAndDisabledUsers(self.sections[15])
        }

    def getHostname(self) -> str:
        return self.configs['sectionOne']['hostname']

    def getOs(self) -> str:
        os = self.configs['sectionOne']['osName'] + ' ' + self.configs['sectionOne']['osVersion'] + ' ' + self.configs['sectionOne']['osConfiguration']
        return os

    def getHardware(self) -> str:
        hardware = self.configs['sectionOne']['osManufacturer'] + ' ' + self.configs['sectionOne']['systemModel'] + ' ' + self.configs['sectionOne']['systemType']
        return hardware

    def getDomainName(self) -> str:
        domainName = self.configs['sectionOne']['domainName']
        return domainName

    def getNetworkAdapters(self) -> list:
        return self.configs['sectionTwo']['adapters']

    def getNetworkWlans(self) -> list:
        return self.configs['sectionTwo']['wlan']

    def getUsers(self) -> list:
        return self.configs['sectionThree']['users']
    
    def getAdmins(self) -> list:
        return self.configs['sectionFour']['admins']

    def getDefaultUsers(self) -> list:
        return self.configs['sectionFive']['defaultUsers']

    def getPrograms(self) -> dict:
        return self.configs['sectionSix']['programs']

    def getServices(self) -> list:
        return self.configs['sectionSeven']['services']

    def getListeningPorts(self) -> dict:
        return self.configs['sectionEight']['listeningPorts']

    def getGpresult(self) -> list:
        return self.configs['sectionNine']['gpresult']

    def getPasswordPolicies(self) -> dict:
        return self.configs['sectionTen']['passwordPolicies']

    def getAccountLockoutPolicies(self) -> dict:
        return self.configs['sectionTen']['accountLockoutPolicies']

    def getAuditPolicies(self) -> dict:
        return self.configs['sectionTen']['auditPolicies']

    def getPrivilegeRights(self) -> dict: #Raw values. Future state - translate to GUI aligned param names in reporting functions
        return self.configs['sectionTen']['privilegeRights']

    def getRegistryValues(self) -> dict: #Raw values. Future state - translate to GUI aligned param names in reporting functions
        return self.configs['sectionTen']['registryValues']

    def getSecurityUpdates(self) -> dict:
        return self.configs['sectionEleven']['securityUpdates']
    
    def getTimeSource(self) -> str:
        return self.configs['sectionTwelve']['source'] 
    
    def getTimePeer(self) -> str:
        return self.configs['sectionTwelve']['peer']
    
    def getScreenSaverTimeout(self) -> str:
        return self.configs['sectionThirteen']['screenSaverTimeout']

    def getRdpSecurityLevel(self) -> str:
        return self.configs['sectionFourteen']['minEncryptionLevel']

    def getInactiveUsers(self) -> list:
        return self.configs['sectionFifteen']['inactiveUsers']

    def getDisabledUsers(self) -> list:
        return self.configs['sectionFifteen']['disabledUsers']

    def getAllUsers(self) -> list:
        return self.configs['sectionFifteen']['disabledUsers']

def parseData(data:list, option:str) -> list:
    sectionsList = []
    if (option == 'cli'):
        sectionsList = parseCLIOutputToSections(data)
    elif (option == 'script'):
        sectionsList = parseScriptDataToSections(data)
    else:
        print("ERROR, parseData(data, option) must receive option of 'cli' or 'script'")
        return
    return sectionsList

def parseScriptDataToSections(data:list) -> list: #Future state, should handle both Script and Config.txt output
    #Returns list of 15 lists
    sectionsList = []
    counter = 0 #Counter value should match section number
    section = []
    regex = '\A---- [0-9].+----'
    for line in data:
        sectionBreakMatch = re.search(regex, line)
        if (sectionBreakMatch != None):
            counter += 1
            sectionCopy = section.copy() #So that section.clear() does not remove data from sectionsList. Probably should find better way to do this eventually.
            sectionsList.append(sectionCopy)
            section.clear()
        else:
            section.append(line)
    sectionsList.append(section)
    if (counter != 15):
        print("Error: Should contain 15 sections. Program detected " + str(counter))
    return sectionsList

def parseCLIOutputToSections(data:list):
    #Program to handle CLI Output files
    return

def parseSystemSpecifications(section:list) -> dict:
    configs = {
        'hostname': "",
        'osName': "",
        'osVersion': "",
        'osConfiguration': "",
        'osManufacturer': "",
        'systemModel': "",
        'systemType': "",
        'domainName': "",
    }
    for line in section:
        if ("Host Name:" in line and configs['hostname'] == ""):
            hostname = line.replace('Host Name:','').strip().lower()
            configs['hostname'] = hostname
        if ("OS Name:" in line and configs['osName'] == ""):
            osName = line.replace('OS Name:','').strip()
            configs['osName'] = osName
        if ("OS Version:" in line and configs['osVersion'] == ""):
            osVersion = line.replace("OS Version:","").strip()
            configs["osVersion"] = osVersion
        if ("OS Configuration:" in line and configs['osConfiguration'] == ""):
            osConfiguration = line.replace("OS Configuration:","").strip()
            configs["osConfiguration"] = osConfiguration            
        if ("System Manufacturer:" in line and configs['osManufacturer'] == ""):
            osManufacturer = line.replace("System Manufacturer:","").strip()
            configs['osManufacturer'] = osManufacturer
        if ("System Model:" in line and configs['systemModel'] == ""):
            systemModel = line.replace("System Model:","").strip()
            configs['systemModel'] = systemModel
        if ("System Type:" in line and configs['systemType'] == ""):
            systemType = line.replace("System Type:","").strip()
            configs['systemType'] = systemType
        if ("Domain:" in line and configs['domainName'] == ""):
            domainName = line.replace("Domain:","").strip()
            configs['domainName'] = domainName
    return configs
        
def parseNetworkInformation(section:list) -> dict:
    configs = {
        'adapters': [],
        'wlan': []
    }
    readingNetstat = True
    readingIpconfig = False
    readingNetsh = False
    adapter = ""
    wlan = ""
    for line in section:
        if (readingNetstat):
            if ("running ipconfig" in line):
                readingNetstat = False
                readingIpConfig = True
        elif (readingIpConfig):
            if ("adapter" in line):
                adapter += line.strip()
            elif ('IPv4 Address. ' in line):
                ipAddress = line.replace("IPv4 Address. . . . . . . . . . . :","").strip()
                adapter += ipAddress
                configs['adapters'].append(adapter)
                adapter = ""
            elif ("Media disconnected" in line):
                adapter = ""
            if ("running netsh wlan" in line):
                readingIpConfig = False
                readingNetsh = True
        elif (readingNetsh):
            if ("Interface name :" in line):
                wlan += line.strip()
            elif ("SSID" in line and not "BSSID" in line):
                wlan += " | " + line.strip()
                configs['wlan'].append(wlan)
                wlan = ""
    return configs

def parseLocalUsers(section:list) -> dict:
    configs = {
        'users': []
    }
    readingUsers = False
    for line in section:
        if ("The command completed successfully" in line or "#########################" in line):
            readingUsers = False
        if (readingUsers):
            user = line.split(" ", 1)[0]
            configs['users'].append(user)
        if ("---------------------" in line):
            readingUsers = True
    return configs
        
def parseLocalGroup(section:list) -> dict:
    configs = {
        'admins': []
    }
    readingAdmins = False
    lineCount = 0
    for line in section:
        if ("The command completed successfully" in line or "#########################" in line):
            readingAdmins = False
        if (readingAdmins):
            regex = '\A\s+\Z'
            blankLine = re.search(regex, line)
            if (blankLine == None):
                if ("--------------" not in line):
                    admin = line.split(" ", 1)[0].strip()
                    configs['admins'].append(admin)
        if ('Members' in line):
            readingAdmins = True
    return configs
        
def parseDefaultUsers(section:list) -> dict:
    configs = {
        'defaultUsers': []
    }
    readingAdministrator = False
    readingGuest = False
    for line in section:
        if ("User name" in line and "Administrator" in line):
            readingAdministrator = True
        if (readingAdministrator):
            if ("Account active" in line and "No" not in line):
                configs['defaultUsers'].append("Administrator account active")
        if ("User name" in line and "Guest" in line):
            readingAdministrator = False
            readingGuest = True
        if (readingGuest):
            if ("Account active" in line and "No" not in line):
                configs['defaultUsers'].append("Guest account active")
    return configs

def parsePrograms(section:list) -> dict:
    configs = {
        'programs': {}
    }
    readingPrograms = False
    for line in section:
        if ("#######################" in line):
            readingPrograms = False
        if (readingPrograms):
            regex = '\A\s+\Z'
            blankLine = re.search(regex, line)
            if (blankLine == None):
                try:
                    program, version = re.sub(' +', ' ', line.strip()).rsplit(" ", 1)
                except ValueError:
                    print("Error: parseProgram() Value Error. Needs both [program, version] values")
                    print("parseProgram() has skipped line: " + line)
                configs['programs'][program.strip()] = version.strip()
        if ("Name" in line and "Version" in line):
            readingPrograms = True
    return configs

def parseServices(section:list) -> dict:
    configs = {
        'services': []
    }
    readingServices = False
    for line in section:
        if ("###############################" in line or "running tasklist:" in line):
            readingServices = False
        if (readingServices):
            regex = '\A\s+\Z'
            blankLine = re.search(regex, line)
            if (blankLine == None):
                service = re.sub(' +', ',', line.strip()).split(",", 1)[0]
                configs['services'].append(service)
        if ("DisplayName" in line and "StartName" in line):
            readingServices = True
    return configs
    
def parseListeningPorts(section:list) -> dict:
    configs = {
        'listeningPorts': {}
    }
    readingActiveConnections = False
    readingService = False
    listeningPort = ""
    for line in section:
        if ("########################" in line):
            readingActiveConnections = False
        if (readingActiveConnections):
            regex = '\A\s+\Z'
            blankLine = re.search(regex, line)
            if (blankLine == None):
                if (readingService):
                    service = line.strip()
                    configs['listeningPorts'][listeningPort] = service
                    readingService=False
                    listeningPort = ""
                if (not readingService):
                    if ("LISTENING" in line):
                        localAddress = line.strip().split(' ', 1)[1].strip().split(' ', 1)[0].strip()
                        listeningPort += localAddress
                        readingService = True           
        if ("Active Connections" in line):
            readingActiveConnections = True
    return configs 

def parseGpresult(section:list) -> dict:
    configs = {
        'gpresult': []
    }
    readingAppliedGroupPolicies = False
    for line in section:
        if ("The following GPOs were not applied because they were filtered" in line or "The computer is a part of the following security groups" in line):
            readingAppliedGroupPolicies = False
        if (readingAppliedGroupPolicies):
            if ("---------------------" in line):
                pass
            elif (not line):
                pass
            else:
                configs['gpresult'].append(line.strip())
        if ("Applied Group Policy Objects" in line):
            readingAppliedGroupPolicies = True
    return configs

def parseSecurityPolicies(section:list) -> dict:
    configs = {
        'passwordPolicies': {},
        'accountLockoutPolicies': {},
        'auditPolicies': {},
        'privilegeRights': {}, #Raw
        'userRightsAssignments': {}, #Translated/Refined (currently empty)
        'registryValues': {}, #Raw
        'securityOptions': {} #Translated/Refined (currently empty)
    }
    #States
    readingSystemAccess = False
    readingEventAudit = False
    readingRegistryValues = False
    readingPrivilegeRights = False
    for line in section:
        #Line Reading Based on State
        if (readingSystemAccess):
            config = parseSecurityPoliciesSystemAccess(line)
            if (config != {}):
                configName = list(config.keys())[0].lower()
                if ("password" in configName):
                    configs['passwordPolicies'].update(config)
                elif ("lockout" in configName):
                    configs['accountLockoutPolicies'].update(config)
        elif (readingEventAudit):
            config = parseSecurityPoliciesEventAudit(line)
            if (config != {}):
                configs['auditPolicies'].update(config)
        elif (readingRegistryValues):
            config = parseSecurityPoliciesRegistryValues(line)
            if (config != {}):
                configs['registryValues'].update(config)
        elif (readingPrivilegeRights):
            config = parseSecurityPoliciesPrivilegeRights(line)
            if (config != {}):
                configs['privilegeRights'].update(config)
        #State Management
        if ("[System Access]" in line):
            readingSystemAccess = True
        elif ("[Event Audit]" in line):
            readingSystemAccess = False
            readingEventAudit = True
        elif ("[Registry Values]" in line):
            readingEventAudit = False
            readingRegistryValues = True
        elif ("[Privilege Rights]" in line):
            readingRegistryValues = False
            readingPrivilegeRights = True
        elif (readingPrivilegeRights and "[Version]" in line):
            readingPrivilegeRights = False
        elif (readingPrivilegeRights and "#######################" in line):
            readingPrivilegeRights = False
    return configs

def parseSecurityPoliciesSystemAccess(line:str) -> dict:
    config = {}
    if ("MaximumPasswordAge" in line):
        config['maximumPasswordAge'] = line.split("=", 1)[1].strip()
    if ("MinimumPasswordLength" in line):
        config['minimumPasswordLength'] = line.split("=", 1)[1].strip()
    if ("PasswordComplexity" in line):
        config['passwordComplexity'] = line.split("=", 1)[1].strip()
    if ("PasswordHistorySize" in line):
        config['passwordHistorySize'] = line.split("=", 1)[1].strip()
    if ("ClearTextPassword" in line):
        config['clearTextPassword'] = line.split("=", 1)[1].strip()
    if ("LockoutBadCount" in line):
        config['lockoutBadCount'] = line.split("=", 1)[1].strip()
    if ("ResetLockoutCount" in line):
        config['resetLockoutCount'] = line.split("=", 1)[1].strip()
    if ("LockoutDuration" in line):
        config['lockoutDuration'] = line.split("=", 1)[1].strip()
    return config
    
def parseSecurityPoliciesEventAudit(line:str) -> dict:
    config = {}
    if ("AuditSystemEvents" in line):
        config['auditSystemEvents'] = line.split("=", 1)[1].strip()
    if ("AuditLogonEvents" in line):
        config['auditLogonEvents'] = line.split("=", 1)[1].strip()
    if ("AuditObjectAccess" in line):
        config['auditObjectAccess'] = line.split("=", 1)[1].strip()
    if ("AuditPrivilegeUse" in line):
        config['auditPrivilegeUse'] = line.split("=", 1)[1].strip()
    if ("AuditPolicyChange" in line):
        config['auditPolicyChange'] = line.split("=", 1)[1].strip()   
    if ("AuditAccountManage" in line):
        config['auditAccountManage'] = line.split("=", 1)[1].strip()
    if ("AuditProcessTracking" in line):
        config['auditProcessTracking'] = line.split("=", 1)[1].strip()
    if ("AuditDSAccess" in line):
        config['auditDSAccess'] = line.split("=", 1)[1].strip()
    if ("AuditAccountLogon" in line):
        config['auditAccountLogon'] = line.split("=", 1)[1].strip()
    return config

def parseSecurityPoliciesRegistryValues(line:str) -> dict:
    #Currently only populations configs['registryValues']. Does not populate 'securityOptions' yet. Will add in future when upgrading reporting capabilities
    config = {}
    if (line.startswith("MACHINE")):
        path = line.split(",", 1)[0].strip()
        value = line.split(",", 1)[1].strip()
        config[path] = value
    return config

def parseSecurityPoliciesPrivilegeRights(line:str) -> dict:
    #Currently outputs only raw values.
    configs = {}
    if ("[Version]" in line):
        return configs
    else:
        parameter = line.split("=", 1)[0].strip()
        value = line.split("=", 1)[1].strip()
        configs[parameter] = value
    return configs

def parseSecurityUpdates(section:list) -> dict:
    configs = {
        'securityUpdates': {}
    }

    date_regex = r"^\d{1,2}\/\d{1,2}\/\d{1,4}"
    hotfix_regex = r"^(KB)[0-9]*"

    for line in section:
        if ("Security Update" in line):
            columns = re.sub(' +', ' ', line).split(' ')
            hotFixId = "ERROR"
            date = "ERROR"
            for value in columns:
                if re.match(date_regex, value):
                    date = value
                
                if re.match(hotfix_regex, value):
                    hotFixId = value

            configs['securityUpdates'][hotFixId] = date
    return configs

def parseTimeSettings(section:list) -> dict:
    configs = {
        'source': "",
        'peer': ""
    }
    readingStatus = False
    readingPeers = False
    for line in section:
        if (readingStatus):
            if ("Source:" in line):
                ipAddress = line.split(":", 1)[1].strip().split(",", 1)[0].strip()
                configs['source'] = ipAddress
        elif (readingPeers):
            if ("Peer:" in line):
                ipAddress = line.split(":", 1)[1].strip().split(",", 1)[0].strip()
                configs['peer'] = ipAddress
        if ("running w32tm /query /status" in line):
            readingStatus = True
        elif ("running w32tm /query /configuration" in line):
            readingStatus = False
        elif ("running w32tm /query /peers:" in line):
            readingPeers = True
        elif ("running w32tm /query /source" in line):
            readingPeers = False
    return configs

def parseScreenSaverSettings(section:list) -> dict:
    configs = {
        'screenSaverTimeout': ""
    }
    for line in section:
        if ("ScreenSaveTimeout" in line and "REG_" in line):
            configs['screenSaverTimeout'] = re.sub(' +', ' ', line.strip()).split(' ', 2)[2]
    return configs

def parseRdpSecurityLevel(section:list) -> dict:
    #minEncryptionValue: 0x3 = 'High', 0x4 = 'FIPS Compliant'
    configs = {
        'minEncryptionLevel': ""
    }
    for line in section:
        if ("MinEncryptionLevel" in line and "REG_" in line):
            configs['minEncryptionLevel'] = re.sub(' +', ' ', line.strip()).split(' ', 2)[2]
    return configs

def parseInactiveAndDisabledUsers(section:list) -> dict:
    configs = {
        'inactiveUsers': [],
        'disabledUsers': [],
        'allUsers': []
    }
    readingDisabledUsers = False
    readingInactiveUsers = False
    readingAllUsers = False
    for line in section:
        regex = '\A\s+\Z'
        blankLine = re.search(regex, line)
        if ("running dsquery user -disabled" in line):
            readingDisabledUsers = True
            continue
        elif ("dsquery user -limit 0 -inactive" in line):
            readingDisabledUsers = False
            readingInactiveUsers = True
            continue
        elif ("dsquery user -limit 0:" in line):
            readingInactiveUsers = False
            readingAllUsers = True
            continue
        if (blankLine == None):
            if (readingDisabledUsers):
                configs['disabledUsers'].append(line.strip())
            elif (readingInactiveUsers):
                configs['inactiveUsers'].append(line.strip())
            elif (readingAllUsers):
                configs['allUsers'].append(line.strip())
    return configs      

    


    


    


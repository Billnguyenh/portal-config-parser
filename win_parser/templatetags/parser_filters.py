from django import template
import json
import re

register = template.Library()

@register.filter(name='decode_json')
def decode_json(json_text):
    json_dec = json.decoder.JSONDecoder()
    return json_dec.decode(json_text)

@register.filter(name='clean_registry_path')
def clean_registry_path(registry_name):
    last_directory_name = registry_name.rsplit('\\', 1)[1].rsplit('=', 1)[0]
    return last_directory_name

@register.filter(name='split_security_options_values')
def split_security_options_values(values_string):
    values_list = values_string.split(',')
    return values_list



SECURITY_OPTIONS_CONVERSION = {
    'RequireSignOrSeal': {
        'RequireSignOrSeal':'Domain member: Digitally encrypt or sign secure channel data (always)',
        '1':'Enabled',
        '0':'Disabled'
    },
    'SealSecureChannel': {
        'SealSecureChannel':'The setting Domain member: Digitally encrypt secure channel data (when possible) must be configured to enabled.',
        '1':'Enabled',
        '0':'Disabled'
    },
    'InactivityTimeoutSecs': {
        'InactivityTimeoutSecs':'The machine inactivity limit must be set to 15 minutes, locking the system with the screen saver.',
    },
    'EnableSecuritySignature': {
        'EnableSecuritySignature':'The setting Microsoft network client/server: Digitally sign communications (if server agrees) must be configured to Enabled.',
        '1':'Enabled',
        '0':'Disabled'
    },
    'RequireSecuritySignature': {
        'RequireSecuritySignature':'The setting Microsoft network client/server: Digitally sign communications (always) must be configured to Enabled.',
        '1':'Enabled',
        '0':'Disabled'
    },
    'NoLMHash': {
        'NoLMHash':'Network security: Do not store LAN Manager hash value on next password change',
        '1':'Enabled',
        '0':'Disabled'
    },
    'LmCompatibilityLevel': {
        'LmCompatibilityLevel': 'Network security: LAN Manager authentication level',
        '0':'Client devices use LM and NTLM authentication, and they never use NTLMv2 session security. Domain controllers accept LM, NTLM, and NTLMv2 authentication.',
        '1':'Client devices use LM and NTLM authentication, and they use NTLMv2 session security if the server supports it. Domain controllers accept LM, NTLM, and NTLMv2 authentication.',
        '2':'Client devices use NTLMv1 authentication, and they use NTLMv2 session security if the server supports it. Domain controllers accept LM, NTLM, and NTLMv2 authentication.',
        '3':'Client devices use NTLMv2 authentication, and they use NTLMv2 session security if the server supports it. Domain controllers accept LM, NTLM, and NTLMv2 authentication.',
        '4':'Client devices use NTLMv2 authentication, and they use NTLMv2 session security if the server supports it. Domain controllers refuse to accept LM authentication, and they will accept only NTLM and NTLMv2 authentication.',
        '5':'Client devices use NTLMv2 authentication, and they use NTLMv2 session security if the server supports it. Domain controllers refuse to accept LM and NTLM authentication, and they will accept only NTLMv2 authentication.',
    },
    'LDAPClientIntegrity': {
        'LDAPClientIntegrity':'Network security: LDAP client signing requirements',
        '0':'No signing/sealing',
        '1':'Negotiate signing/sealing',
        '2':'Require signing/sealing'
    }
}

@register.filter(name='is_in_security_options_sample')
def is_in_security_options_sample(registry_name:str) -> bool:
    policy_name = clean_registry_path(registry_name)
    if policy_name in SECURITY_OPTIONS_CONVERSION:
        return True
    return False

@register.filter(name='convert_security_options_string_tuple_to_readable_list_tuple')
def convert_security_options_string_tuple_to_readable_list_tuple(string_tuple):
    key, val = string_tuple.split(';', 1)
    if key in SECURITY_OPTIONS_CONVERSION:
        readable_policy_name = SECURITY_OPTIONS_CONVERSION[key][key]
        if val in SECURITY_OPTIONS_CONVERSION[key]:
            readable_policy_value = SECURITY_OPTIONS_CONVERSION[key][val]
        else:
            readable_policy_value = val
    else:
        readable_policy_name = " Error: " + key + ' is not in sample.'
        readable_policy_value = val
    return readable_policy_name, readable_policy_value

@register.filter(name='translate_rdp_security_level')
def translate_rdp_security_level(level:str) -> str:
    if '4' in level:
        return 'FIPS'
    elif '3' in level:
        return 'High'
    elif '2' in level:
        return 'Client Compatible'
    elif '1' in level:
        return 'Low'
    else:
        return 'Not Configured'

@register.filter(name='translate_screen_saver_timeout')
def translate_screen_saver_timeout(value:str) -> str:
    if re.match(r'^[0-9]+', value):
        return value
    else:
        return 'Not Configured'

@register.filter(name='translate_time_configuration')
def translate_time_configuration(value:str) -> str:
    if value == "":
        return 'Not Configured'
    else:
        return value

@register.filter(name='translate_privilege_rights_values_to_list')
def translate_privilege_rights_values_to_list(values:str) -> list:
    #Reference: https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/security-identifiers-in-windows
    SID_DICT = {
        'S-1-0':'Null Authority',
        'S-1-0-0':'Nobody',
        'S-1-1':'World Authority',
        'S-1-1-0':'Everyone',
        'S-1-2':'Local Authority',
        'S-1-2-0':'Local',
        'S-1-3':'Creator Authority',
        'S-1-3-0':'Creator Owner',
        'S-1-3-1':'Creator Group',
        'S-1-3-4':'Owner Rights',
        'S-1-4':'Non-unique Authority',
        'S-1-5':'NT Authority',
        'S-1-5-1':'Dialup',
        'S-1-5-2':'Network',
        'S-1-5-3':'Batch',
        'S-1-5-4':'Interactive',
        'S-1-5-5-X-Y':'Logon Session',
        'S-1-5-6':'Service',
        'S-1-5-7':'Anonymous',
        'S-1-5-9':'Enterprise Domain Controllers',
        'S-1-5-10':'Principal Self',
        'S-1-5-11':'Authenticated Users',
        'S-1-5-12':'Restricted Code',
        'S-1-5-13':'Terminal Server Users',
        'S-1-5-14':'Remote Interactive Logon',
        'S-1-5-17':'This Organization',
        'S-1-5-18':'Local System',
        'S-1-5-19':'NT Authority',
        'S-1-5-20':'NT Authority',
        'S-1-5-21domain-500':'Administrator',
        'S-1-5-21domain-501':'Guest',
        'S-1-5-21domain-502':'KRBTGT',
        'S-1-5-21domain-512':'Domain Admins',
        'S-1-5-21domain-513':'Domain Users',
        'S-1-5-21domain-514':'Domain Guests',
        'S-1-5-21domain-515':'Domain Computers',
        'S-1-5-21domain-516':'Domain Controllers',
        'S-1-5-21domain-517':'Cert Publishers',
        'S-1-5-21root domain-518':'Schema Admins',
        'S-1-5-21root domain-519':'Enterprise Admins',
        'S-1-5-21domain-520':'Group Policy Creator Owners',
        'S-1-5-21domain-526':'Key Admins',
        'S-1-5-21domain-527':'Enterprise Key Admins',
        'S-1-5-21domain-553':'RAS and IAS Servers',
        'S-1-5-32-544':'Administrators',
        'S-1-5-32-545':'Users',
        'S-1-5-32-546':'Guests',
        'S-1-5-32-547':'Power Users',
        'S-1-5-32-548':'Account Operators',
        'S-1-5-32-549':'Server Operators',
        'S-1-5-32-550':'Print Operators',
        'S-1-5-32-551':'Backup Operators',
        'S-1-5-32-552':'Replicators',
        'S-1-5-32-582':'Storage Replica Administrators',
        'S-1-5-64-10':'NTLM Authentication',
        'S-1-5-64-14':'SChannel Authentication',
        'S-1-5-64-21':'Digest Authentication',
        'S-1-5-80':'NT Service'
    }
    raw_values_list = values.split(',')

    translated_list = []

    for raw_value in raw_values_list:
        raw_value = raw_value.lstrip('*')
        if raw_value in SID_DICT:
            translation = SID_DICT[raw_value]
            translated_list.append(translation)
        else:
            translated_list.append(raw_value)
    
    return translated_list

        

#!/usr/bin/python

import ConfigParser
import os
import json
import logging 

def required_fields_check( logger, required_fields_file, modulename, acct, componentname, json_file_path ):
    MOD_ACCT = 'accounts'
    MOD_USERS = 'users'
    MOD_TS = 'transfersites'
    MOD_SUB = 'subscriptions'

    ACCT_FIELDS = 'accountsfields'
    USERS_FIELDS = 'usersfields'
    SUBSCRIPTION_FIELDS = 'subscriptionfields'

    SSH_PROTOCOL = 'ssh'
    SSH_FIELDS = 'sshfields'
    FTP_PROTOCOL = 'ftp'
    FTP_FIELDS = 'ftpfields'
    SMB_PROTOCOL = 'smb'
    SMB_FIELDS = 'smbfields'
    FM_PROTOCOL = 'folder'
    FM_FIELDS = 'fmfields'

    STATUS_PASS = 'PASSED'
    STATUS_FAIL = 'FAILED'

    conf_sec = ''
    req_list_name = ''
    transfersite_data = ''
    retVal = STATUS_PASS
    protocol = None

    logging.basicConfig(filename = log_filename, level = logging.DEBUG, format = ' %(asctime)s %(levelname)s %(message)s ', datefmt = '%m/%d/%Y %I:%M:%S %p')

    if module == MOD_ACCOUNTS:
        conf_sec = MOD_ACCOUNTS
        req_list_name = ACCT_FIELDS
    elif module == MOD_USERS:
        conf_sec = MOD_USERS
        req_list_name = USERS_FIELDS
    elif module == MOD_SUB:
        conf_sec = MOD_SUB
        req_list_name = SUBSCRIPTION_FIELDS
    elif module = MOD_TS:
        if protocol == "None":
            with open ( json_file_path ) as transfersite:
                transfersite_data = json.load( transfersite )
                protocol = transfersite_data['protocol']
            conf_sec = ""
            re_list_name = ""
        if protocol == SSH_PROTOCOL:
            conf_sec = SSH_PROTOCOL
            req_list_name = SSH_FIELDS
        elif protocol == FTP_PROTOCOL:
            conf_sec = FTP_PROTOCOL
            req_list_name = FTP_FIELDS
        elif protocol == SMB_PROTOCOL:
            conf_sec = SMB_PROTOCOL
            req_list_name = SMB_FIELDS
        elif protocol == FM_PROTOCOL:
            conf_sec = FM_PROTOCOL
            req_list_name = FM_FIELDS
    #Read and validate required fields in the json
    config = ConfigParser.RawConfigParser()
    if os.path.exists( required_fields_file ):
        config.read(required_fields_file)
        req_fields_list = config.get( conf_sec, req_list_name ).split( "," )
        if os.path.exists( json_file_path ):
            with open( json_file_path ) as data_collections:
                file_data = json.load( data_collections )
                if module == MOD_TS or module == MOD_SUB or module == MOD_ACCT:
                    for x in req_fields_list:
                        if x not in file_data or len( file_data[x] ) == 0:
                            logging.warning( 'Requried Field ' + x +' NOT FOUND, or empty check the json.' )
                            retVal = STATUS_FAIL
                elif module == MOD_USERS:
                    for x in req_fields_list:
                        if x == 'name' and x not in file_data['users'][0] and len(file_data['users'][0]['name'] == 0:
                            logging.warning( 'Requried Field ' + x +' NOT FOUND, or empty check the json.' )
                            retVal = STATUS_FAIL
        else:
             logging.warning( 'FILE NOT FOUND: ' + json_file_path )
             retVal = STATUS_FAIL
    else:
        logging.warning( 'FILE NOT FOUND: ' + required_fields_file)
        retVal = STATUS_FAIL
    return(retVal)



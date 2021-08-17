#! /usr/bin/python2.7

##############################################################################
# Revision History
# Date          Author               Desc
# 7/21/21       Mugunthan            Initial Draft
#
#
##############################################################################
# Import modules goes here
import datetime
import logging
import subprocess
import json
import sys
import os
import re
import csv
import ConfigParser

sys.path.insert(0, '/home/ubuntu/mugunthan/repo/MFTAuto/scripts')
from req_fields_validation import require_fields_check

#Constants goes here
ACCT_MOD = 'accounts'
USR_MOD = 'users'
TS_MOD = 'transfersites'
SUB_MOD = 'subscriptions'
STATUS_PASS = 'PASSED'
STATUS_FAIL = 'FAILED'

MOD_CREATE = 'create'
MOD_UPDATE = 'update'

SSH_PROTOCOL = 'ssh'
FTP_PROTOCOL = 'ftp'
FM_PROTOCOL = 'fm'
SMB_PROTOCOL = 'smb'

#Resources path
resource_path = '/home/ubuntu/mugunthan/repo/MFTAuto/resources'

#Required fields config path
req_fields_file = resource_path + '/requiredfields.properties'

#Template files config path
acct_template_file = resource_path + '/accountstemplate.json'
user_template_file = resource_path + '/usertemplate.json'
ssh_template_file = resource_path + '/sshtemplate.json'
ftp_template_file = resource_path + '/ftptemplate.json'
fm_template_file = resource_path + '/fmtemplate.json'
smb_template_file = resource_path + '/smbtemplate.json'
sub_template_file = resource_path + '/subscriptiontemplate.json'

#Read/get the imput filename
wr_csv_file = sys.argv[1]
#Read/get the repos path where the new/modified fiels to be placed
service_acct_path = sys.argv[2]

#Logger
log_date = datetime.datetime.now()
log_filename = wr_csv_file + ".log"
#Check for log file already exist or not
if os.path.isfile( log_filename ):
    os.remove( log_filename )
#Init the logger
logging.basicConfig( filename = log_filename, level = logging.DEBUG, format = ' %(asctime)s %(levelname)s %(message)s ', datefmt = '%m/%d/%Y %I:%M:%S %p' )
logging.info( "******************************* Process Started ****************************" )
logging.info( "Read WR CSV file "+ wr_csv_file)

#Read the WR custom csv file
with open( wr_csv_file ) as csvfile:
    readCSV = csv.reader( csvfile, delimiter = ',' )
    for row in readCSV:
        logging.info( "Processing: "+ str( row ))
        new_data = None
        file_data = None
        module = row[0]
        acct = row[1]
        componentname = row[2]
        create_update = row[3]
        fields = row[4]
        print fields
        if fields != 'fields' or fields == '':
            fields_list = fields.split(";")
            dict = { k:v for k,v in (x.split(':') for x in fields_list) }
            if dict.get( 'protocol' ) != None:
                ts_protocol = str(dict.get('protocol'))
            else:
                ts_protocol = None
        else:
            logging.info( 'Fields column is empty, moving to next row' )

        logging.info( '--- Account Name: '+ acct +' Module Name: '+ module +' Component Name: '+ componentname +' Create/Update: '+ create_update )
        #Check for target dirs exists/not
        if module == ACCT_MOD:
            acct_dir = service_acct_path +'/'+ acct
            json_filepath = acct_dir +'/'+ acct +'_account.json'
            if not os.path.exists( acct_dir ):
                os.makedirs( acct_dir )
                logging.info( 'Service Account dir does not exists: '+ acct_dir )
            else:
                logging.info( 'Service Account dir exists: '+ acct_dir )
        elif module == USR_MOD:
            acct_dir = service_acct_path +'/'+ acct
            json_filepath = acct_dir +'/'+ acct +'_user.json'
            if not os.path.exists( acct_dir ):
                os.makedirs( acct_dir )
                logging.info( 'Service Account dir does not exists: '+ acct_dir )
            else:
                logging.info( 'Service Account dir exists: '+ acct_dir )
        elif module == TS_MOD:
            ts_dir = service_acct_path +'/'+ acct +'/'+ TS_MOD
            json_filepath = ts_dir +'/'+ componentname +'.json'
            if not os.path.exists( ts_dir ):
                os.makedirs( ts_dir )
                logging.info( 'Service Account Transfersites dir does not exists: '+ ts_dir )
            else:
                logging.info( 'Service Account Transfersites dir exists: '+ ts_dir )
        elif module == SUB_MOD:
            sub_dir = service_acct_path +'/'+ acct +'/'+ SUB_MOD +'/'+ componentname
            child_dir_check = componentname.find( '/' )
            if child_dir_check > 0:
                component_filename = componentname[ componentname.reindex( '/' )+ 1: ]
                json_filepath = sub_dir + '/' + component_filename + '.json'
            else:
                json_filepath = sub_dir + '/' + componentname + '.json'
            if not os.path.exists( sub_dir ):
                os.makedirs( sub_dir )
                logging.info( 'Service Account Subcription dir does not exists: '+ sub_dir )
            else:
                logging.info( 'Service Account Subscription dir exists: '+ sub_dir )

        if create_update == MOD_CREATE and module != 'route' :
            if module == ACCT_MOD:
                with open ( acct_template_file ) as acct_template_data:
                    new_data = json.load( acct_template_data )
                    for k,v in dict.items():
                        if k in new_data:
                            new_data[k] = v
                        elif k == 'email':
                            new_data['contact']['email'] = v
                        elif k == 'phone':
                            new_data['contact']['phone'] = v
                        else:
                            logging.info( 'Key/Not Found in the tempalte: ' + k )
            elif module == USR_MOD:
                with open ( user_template_file ) as user_template_data:
                    new_data = json.load( user_template_data )
                    for k,v in dict.items():
                        if k in new_data:
                            new_data[k] = v
                        elif k == 'username':
                            new_data['users'][0]['passwordCredentials']['username'] = v
                        elif k == 'password':
                            new_data['users'][0]['passwordCredentials']['password'] = v
                        elif k in new_data['users'][0]:
                            new_data['users'][0][k] = v
                        else:
                            logging.info( 'Key/Not Found in the tempalte: ' + k )
            elif module == TS_MOD:
                if 'account' not in dict:
                    dict['acctount'] = acct
                if 'name' not in dict:
                    dict['name'] = componentname 
                if ts_protocol == SSH_PROTOCOL:
                    with open ( ssh_template_file ) as ssh_template_data:
                        new_data = json.load( ssh_template_data )
                        for k,v in dict.items():
                            new_data[k] = v
                elif ts_protocol == FTP_PROTOCOL:
                    with open ( ftp_template_file ) as ftp_template_data:
                        new_data = json.load( ftp_template_data )
                        for k,v in dict.items():
                            new_data[k] = v
                elif ts_protocol == SMB_PROTOCOL:
                    with open ( smb_template_file ) as smb_template_data:
                        new_data = json.load( smb_template_data )
                        for k,v in dict.items():
                            new_data[k] = v
                elif ts_protocol == FM_PROTOCOL:
                    with open ( fm_template_file ) as fm_template_data:
                        new_data = json.load( fm_template_data )
                        for k,v in dict.items():
                            new_data[k] = v
            elif module == SUB_MOD:
                with open ( sub_template_file ) as sub_template_data:
                    new_data = json.load( sub_template_data)
                    for k,v in dict.items():
                        new_data[k] = v
        if new_data:
            with open ( json_filepath, 'w' ) as write_to_file:
                json.dump( new_data, write_to_file, indent = 4 )
                logging.info( 'New file successfully created: '+ json_filepath )

        if create_update == MOD_UPDATE and module != 'route':
            if os.path.exists ( json_filepath ):
                with open ( json_filepath, 'r' ) as open_json_file:
                    file_data = json.load( open_json_file )
                    if module == ACCT_MOD:
                        for k,v in dict.items():
                            if k in file_data:
                                file_data[k] = v
                            elif k == 'email':
                                file_data['contact']['email'] = v
                            elif k == 'phone':
                                file_data['contact']['phone'] = v
                            else:
                                logging.info( 'Key/Not Found in the tempalte: ' + k )
                    elif module == USR_MOD:
                        for k,v in dict.items():
                            if k in file_data:
                                file_data[k] = v
                            elif k == 'username':
                                file_data['users'][0]['passwordCredentials']['username'] = v
                            elif k == 'password':
                                file_data['users'][0]['passwordCredentials']['password'] = v
                            elif k in file_data['users'][0]:
                                file_data['users'][0][k] = v
                            else:
                                logging.info( 'Key/Not Found in the tempalte: ' + k )
                    elif module == TS_MOD or module == SUB_MOD:
                        for k,v in dict.items():
                            if k in file_data:
                                logging.info( 'Old value for '+ k +': '+ file_data[k])
                                file_data[k] = v
                                logging.info( 'New value for '+ k +': '+ file_data[k])
                            else:
                                logging.info( 'Inserting new key & value '+ k +': '+ file_data[k])
                                file_data[k] = v
                with open ( json_filepath, 'w' ) as write_json_file:
                    json.dump( file_data, write_json_file, indent = 4 )
        if module != 'route':
            logging.info( 'Verification and validation started for file '+ json_filepath )
            validation_status = require_fields_check( log_filename, req_fields_file, module, acct, componentname, json_filepath )
            logging.info( 'Verification and validation status '+ validation_status + ' for file '+ json_filepath)
            if validation_status != STATUS_PASS:
                logging.info( 'Please check the reason for failure and fix it and re-run' )

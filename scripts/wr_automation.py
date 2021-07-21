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
import ConfigParaser

sys.path.insert(0, '/home/ubuntu/mugunthan/repo/MFTAuto/scripts')
from require_feilds_validation import require_feilds_check

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
resource_path = '/home/ubuntu/mugunthan/repo/MFTAuto/scripts/resources'

#Required fields config path
req_fields_file = resource_path + '/requiredfields.properties'

#Template files config path
aact_tempalte_file = resource_path + '/accttemplate.json'
usr_template_file = resource_path + '/usertemplate.json'
ssh_template_file = resource_path + '/sshtemplate.json'
ftp_template_file = resource_path + '/ftptemplate.json'
fm_template_file = resource_path + '/fmtemplate.json'
smb_template_file = resource_path + '/smbtemplate.json'
sub_tempalte_file = resource_path + '/subtemplate.json'

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
        if fields != 'fields':
            field_list = fields.split(";")
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
        elif module = USR_MOD:
            acct_dir = service_acct_path +'/'+ acct
            json_filepath = acct_dir +'/'+ acct +'_user.json'
            if not os.path.exists( acct_dir ):
                os.makedirs( acct_dir )
                logging.info( 'Service Account dir does not exists: '+ acct_dir )
            else:
                logging.info( 'Service Account dir exists: '+ acct_dir )
        elif module = TS_MOD:
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

        if create_update == MOD_CREATE:
            if module 








ACCT_MOD = 'accounts'
USR_MOD = 'users'
TS_MOD = 'transfersites'
SUB_MOD

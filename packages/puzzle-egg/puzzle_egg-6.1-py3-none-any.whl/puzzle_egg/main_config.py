#
#.NOTES
#------------------------------------------------------
# Date          	: 16--2019
# Script name       : main_config.py
# Description       : 
# Created by        : Alice Bom
# Copyright         : @2019
# Comments          : - 
#------------------------------------------------------



#from calimero import azure_key_vault as akv
#import tempparameters as tp

class Config:

    def __init__(self,sp_client_id, sp_tenant_id,sp_secret_key,key_vault_connection_string, runtype='production'):
        # make connection to the keyvault
        self.kvclient = ""
        # main database
        self.param_db = ""
        # main sql server
        self.param_srv = ""
        self.param_dl = ""
        self.param_logpath = ""
        self.param_db_port = ""
        self.param_dl_connection_prefix = ""
        self.param_dl_connection_post = ""


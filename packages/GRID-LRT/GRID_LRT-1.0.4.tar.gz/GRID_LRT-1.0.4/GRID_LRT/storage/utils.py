from datetime import datetime
import warnings
from subprocess import Popen, PIPE
import re
import sys
import GRID_LRT.auth.grid_credentials as grid_creds
from GRID_LRT.auth.get_picas_credentials import get_picas_cred
from GRID_LRT import token
from GRID_LRT.Staging.srmlist import srmlist
from GRID_LRT.storage.gsifile import GSIFile


class SafePopen(Popen):
    def __init__(self, *args, **kwargs):
        if sys.version_info.major == 3 :
            kwargs['encoding'] = 'utf8'
        return super(SafePopen, self).__init__(*args, **kwargs)

def get_srmdir_from_token_task(token_type, view, key = 'RESULTS_DIR'):
    """Creates a list of files from a set of tokens. Returns a GSIFile object"""
    pc=get_picas_cred()
    th=Token.Token_Handler(t_type=token_type, uname=pc.user, pwd=pc.password, dbn=pc.database)
    tokens=th.list_tokens_from_view(view)
    srmdir, OBSID, pipeline_step = None, None, None
    for t in tokens: #TODO: Do this with a proper view
        if not pipeline_step:
            pipeline_step = th.database[t['id']]['pipeline_step']
            OBSID = th.database[t['id']]['OBSID']
        if srmdir is not None: break
        if OBSID:
            srmdir_location = str(th.database[t['id']][key])+"/"+pipeline_step+"/"+str(OBSID)
            srmdir = GSIFile(srmdir_location)
    return srmdir

def make_srmlist_from_srmdir(srmdir):
    slist = srmlist()
    for i in srmdir.list_dir():
        slist.append(i.location)
    return slist


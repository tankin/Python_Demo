# -*- coding: utf-8 -*-
import subprocess
import locale
import sys

def SvnAction(command, errorInfo, debug=True):
    if debug:
        print(command)
        sys.stdout.flush()
    
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    retcode = proc.poll()
    enc = locale.getpreferredencoding()
    cont = str(out.decode(enc))
    errCont = str(err.decode(enc))
    if retcode != 0:
        print("-- svn Error --")
        print(errCont)
        raise RuntimeError(errorInfo)
    return cont


def Svn_Info(dir):
    command = "svn info \"%s\"" % (dir)
    return SvnAction(command, "Error : Svn_Info, %s" % (command))

def Svn_Info_Last_Changed_Author(dir):
    command = "svn info \"%s\" --show-item last-changed-author" % (dir)
    return SvnAction(command, "Error : Svn_Info_Last_Changed_Author, %s" % (command))

def Svn_Info_Last_Changed_Revision(dir):
    command = "svn info \"%s\" -r HEAD --show-item last-changed-revision" % (dir)
    rev = SvnAction(command, "Error : Svn_Info_Last_Changed_Revision, %s" % (command))
    rev = rev.replace("\r\n", "")
    return rev

def Svn_Info_Last_Changed_Revision_Old(dir):
    command = "svn info \"%s\" -r HEAD --xml" % (dir)
    cont = SvnAction(command, "Error : Svn_Info_Last_Changed_Revision_Old, %s" % (command))
    startPos = cont.rfind("<commit")
    pos = cont.find("revision=", startPos)
    pos2 = cont.find(">", startPos)
    rev = cont[pos + len("revision=")+1 : pos2-1]
    return rev


def Svn_Add(path):
    command = "svn add \"%s\"" % (path)
    return SvnAction(command, "Error : Svn_Add, %s" % (command))

def Svn_Add_Force(dir):
    command = "svn --force add \"%s\"" % (dir)
    return SvnAction(command, "Error: Svn_Add_Force, %s" % (command))

def Svn_Del(path):
    command = "svn del \"%s\"" % (path)
    return SvnAction(command, "Error: Svn_Del, %s" % (command))

def Svn_Commit(path, comment):
    command = "svn commit \"%s\" -m \"%s\"" % (path, comment)
    return SvnAction(command, "Error : Svn_Commit, %s" % (command))

def Svn_Checkout(url, path):
    command = "svn checkout %s \"%s\"" % (url, path)
    return SvnAction(command, "Error : Svn_Checkout, %s" % (command))

# depth : 'exclude', 'empty', 'files', 'immediates', 'infinity'
def Svn_Checkout_Depth(url, path, depth):
    command = "svn checkout --depth=%s \"%s\" \"%s\"" % (depth, url, path)
    return SvnAction(command, "Error : Svn_Checkout_Depth, %s" % (command))


# svn diff will automatically merge duplicate file info to single one info
# no need to filter file manually
# Caution: if path is ended with "\", svn will pop up Error
# output: include the whole path, be care of the path ahead of "Assets\"
def Svn_Diff(path, fromRevision, toRevision):
    command = "svn diff \"%s\" --summarize -r %s:%s" % (path, fromRevision, toRevision)
    return SvnAction(command, "Error : Svn_Diff, %s" % (command))

def Svn_Update(path):
    command = "svn update \"%s\"" % (path)
    return SvnAction(command, "Error : Svn_Update, %s" % (command))

# depth : 'exclude', 'empty', 'files', 'immediates', 'infinity'
def Svn_Update_Depth(path, depth):
    command = "svn update --set-depth=%s \"%s\"" % (depth, path)
    return SvnAction(command, "Error : Svn_Update_Depth, %s" % (command))

def Svn_Switch(url, path):
    command = "svn switch --accept theirs-full %s %s" % (url, path)
    return SvnAction(command, "Error : Svn_Switch, %s" % (command))

def Svn_List(url):
    command = "svn list %s" % (url)
    return SvnAction(command, "Error : Svn_List, %s" % (command))

def Svn_SetExternalLink(path, links):
    #f.write("StreamingAssets https://192.168.40.221:8833/svn/mlrelease2017/branches/Android-%s/Android\n" % (branchName))
    with open("svnext.txt", "w") as f:
        index = 0
        size = len(links)
        for link in links:
            if len(link) > 0:
                index = index + 1
                if index != size:
                    f.write(link + '\n')
                else:
                    f.write(link)        
    
    command = "svn propset svn:externals -F svnext.txt %s" % (path)
    return SvnAction(command, "Error : Svn_SetExternalLink, %s" %(command))
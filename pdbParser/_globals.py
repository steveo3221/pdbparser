import os
import sys
import imp
__parameters_path__ = os.path.join( os.path.dirname(os.path.realpath(__file__)), "pdbParserParams.py")



def get_parameters():
    if not os.path.exists(__parameters_path__) or True:
        write_parameters(params={})
    # load and return
    (path, name) = os.path.split(__parameters_path__)
    (name, ext) = os.path.splitext(name)
    (file, filename, data) = imp.find_module(name, [path])
    try:
        mod = imp.load_module(name, file, filename, data)
        params = mod.parameters
    except:
        print "Unable to load module '%s'"%filename
        params = {}
    return params
    

def write_parameters(params=None, insureVMD=True):
    if params is None:
        params={}
    assert isinstance(params, dict), "params must be a dict"
    # open file
    try:
        fd = open(__parameters_path__, 'w')
    except:
        print "Can't open %s for writing pdbParser parameters"%__parameters_path__
        return
    # check if vmd path parameter exists, if not guess it as the following hoping that VMD is installed
    if not params.has_key('VMD_PATH') and insureVMD:
        if sys.platform == "win32":
            exePath = None
            for p in [fname for fname in os.listdir("C:\\") if "Program Files" in fname]:
                path = os.path.join("C:\\", p, "University of Illinois", "VMD", "vmd.exe")
                if os.path.exists(path):
                    exePath = path
            params["VMD_PATH"] = exePath
        elif sys.platform == "darwin":
            exePath = None
            if os.path.exists('/Applications'):
                exePath = '/Applications'
                files = [fname for fname in os.listdir(exePath) if 'VMD' in fname]
                if not len(files):
                    exePath = None
            if exePath is not None:
                exePath = os.path.join(exePath, files[0], 'Contents', 'vmd')
                files = [fname for fname in os.listdir(exePath) if 'vmd_MACOS' in fname] 
                if not len(files):
                    exePath = None
            if exePath is not None:
                exePath = os.path.join(exePath, files[0])
            params["VMD_PATH"] = exePath
        else:
            exePath = None
            if os.path.exists("/usr/local/bin/vmd"):
                exePath = "/usr/local/bin/vmd"
            params["VMD_PATH"] = exePath
    # write lines
    lines  = "# This file is generated by pdbParser" + "\n"
    lines += "parameters = {}" + "\n"
    for k, v in params.items():
        if isinstance(k, basestring):
            if isinstance(v, basestring):
                lines += "parameters['%s'] = '%s'\n"%(k.encode('string-escape'), v.encode('string-escape'))
            else:
                lines += "parameters['%s'] = %s\n"%(k.encode('string-escape'), v)
        elif isinstance(v, basestring):
            lines += "parameters[%s] = '%s'\n"%(k, v.encode('string-escape'))
        else:
            lines += "parameters[%s] = %s\n"%(k, v)
    # write params  
    try:     
        fd.write(lines) 
    except:
        print "Unable to write pdbParser parameters to file %s"%__parameters_path__
    fd.close()
        
def update_parameters(params):
    p = get_parameters()
    p.update(params)
    write_parameters(params)
    
def set_vmd_path(path):
    params = get_parameters()
    params["VMD_PATH"] = path
    write_parameters(params)

def get_parameter_value(key):
    params = get_parameters()
    return params.get(key, None)
    
    
    
    
    
    
    
    


#guide_save & load
import json
fileName = '/Users/siddarthmehraajm/Documents/GitHub/AutoRiggingFramework/TSL-codebase/Extra/cape.json'

def writeJson(dataToWrite,fileName):
        if '.json' not in fileName:
            fileName+='.json'
            
        print("> write to json file is seeing: {0}".format(fileName))
        
        with open(fileName,'w') as jsonFile:
            json.dump(dataToWrite,jsonFile,indent = 2)
                        
        print ("Data was successfully written to {0}".format(fileName))        
        return fileName



def readJsonFile(fileName):
    try:
        with open(fileName,'r') as jsonFile:
            return json.load(jsonFile)
    except:
        raise RuntimeError("Could not read {0}".format(fileName))
        
def extract_data(obj = None):
    values = []
    if obj:
        trs = cmds.getAttr('%s.translate'%obj)
        rot = cmds.getAttr('%s.rotate'%obj)
        scl = cmds.getAttr('%s.scale'%obj)
        values.append(trs)
        values.append(rot)
        values.append(scl)
        
    return  values

def save_guides_data(fileName):
    
    data_dict = {}
    
    gds = pm.ls('*_gd',an=1)
    for i in gds:
        data = extract_data(str(i))
        data_dict[str(i)]= data
    
    jsn_file = writeJson(data_dict,fileName)    
        

def load_guides(fileName):
    
    data_dic = readJsonFile(fileName)
    keysList = list(data_dic.keys())
    for i in keysList:
        pass
        pm.setAttr(i+'.translate',((data_dic[i])[0])[0])
        pm.setAttr(i+'.rotate',((data_dic[i])[1])[0])
        pm.setAttr(i+'.scale',((data_dic[i])[2])[0])



#save_guides_data(fileName)
#load_guides(fileName)

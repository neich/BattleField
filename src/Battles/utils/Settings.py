"""
    Settings module.
    Import settings data from a xml file and defines an API interface to query them
"""

import xml.etree.cElementTree
import os
import inspect
import ast



# Default settings file
SETTINGS_XML = "settings.xml"



# Class to parse settings file
# WARNING: This class loads the xml at the constructor. You should use SETTINGS object (defined below) to avoid reparsing the xml each time
class Settings:
    
    
    # Inits the setting class. xmlfile is the setttings xml file. If is None, the default file is used
    def __init__(self, xmlfile = None):

        if (not xmlfile):
            path = inspect.getfile(self.__class__)
            xmlfile = os.path.dirname(path) + '/' + SETTINGS_XML 

        self.__tree = xml.etree.cElementTree.parse(xmlfile)
        self.__root = self.__tree.getroot()
        self.__xmlfilename = xmlfile
        
        
    # Returns a setting FLOAT value using tag and subtag values. Subtag is optional. Paths are allowed  for any parameter    
    # The root is none, search by self.__root node. Otherwise, use the given element
    # Note that if root isnt None and category is None, given root is used as a leaf node, and it is converted to the data type
    # If required is true and the tag isnt found, an error message is shown
    def Get_F(self, category = None, tag = None, subtag = None, root = None, required = True, default = 0.0):
        
        if (not category and root != None):
            return float(root.text)
        else:
            ret = self.__GetValue(category, tag = tag, subtag = subtag, root = root, required = required)
            if (ret == None):
                return default
            
            else:
                return float(ret)
 
 
    # Returns an integer
    def Get_I(self, category = None, tag = None, subtag = None, root = None, required = True, default = 0):
        
        if (not category and root != None):
            return int(root.text)
        else:
            ret = self.__GetValue(category, tag = tag, subtag = subtag, root = root, required = required)
            if (ret == None):
                return default
            else:
                return int(ret)


    # Returns a boolean
    def Get_B(self, category = None, tag = None, subtag = None, root = None, required = True, default = False):
        
        if (not category and root != None):
            return root.text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE']
        else:
            ret = self.__GetValue(category, tag = tag, subtag = subtag, root = root, required = required)
            if (ret == None):
                return default
            else:
                return ret in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE']
    
    
    # Returns an array
    def Get_A(self, category = None, tag = None, subtag = None, root = None, required = True):
        
        if (not category and root != None):
            return ast.literal_eval(root.text)
        else:
            ret = self.__GetValue(category, tag = tag, subtag = subtag, root = root, required = required)
            if (ret ==  None):
                return None
            else:
                return ast.literal_eval(ret)
        
    
    # Returns a string
    def Get_S(self, category = None, tag = None, subtag = None, root = None, required = True):    
        if (not category and root != None):
            return root.text
        else:
            return self.__GetValue(category = category, tag = tag, subtag = subtag, root = root, required = required)
    
    
    
       
    
    def __GetValue(self, category, tag = None, subtag = None, root = None, required = True):
    
        if (root == None):
            cat = self.__root.find(category)
        else:
            cat = root.find(category)
            
        if (cat == None):
            if (required):
                print "Error in settings file: " + category + " tag not found"
            return None
        
        if (not tag):
            ret = cat.text
        else:        
        
            cat_tag = cat.find(tag)
            if (cat_tag == None):
                if (required):
                    print "Error in settings file: " + tag + " tag not found"
                return None
            
            if (not subtag):
                ret = cat_tag.text
            else:
                cat_subtag = cat_tag.find(subtag)
                if (cat_subtag == None):
                    if (required):
                        print "Error in settings file: " + subtag + " tag not found"
                    return None
                
                ret = cat_subtag.text
        
        return ret
    

    # Changes a value on the xml. This method doesnt store the modified xml, just changes the value in memory
    def SetValue(self, value, category, tag = None, subtag = None, root = None, required = True):
    
        if (root == None):
            cat = self.__root.find(category)
        else:
            cat = root.find(category)
            
        if (cat == None):
            if (required):
                print "Error in settings file: " + category + " tag not found"
            return None
        
        if (not tag):
            cat.text = value
            return
        else:        
        
            cat_tag = cat.find(tag)
            if (cat_tag == None):
                if (required):
                    print "Error in settings file: " + tag + " tag not found"
                return None
            
            if (not subtag):
                cat_tag.text = value
                return
            else:
                cat_subtag = cat_tag.find(subtag)
                if (cat_subtag == None):
                    if (required):
                        print "Error in settings file: " + subtag + " tag not found"
                    return None
                
                cat_subtag.text = value
                return
        
        


    
    
    # Returns true if given tag exists
    def HasTag(self, category, tag = None, subtag = None, root = None):
        
        if (root == None):
            cat = self.__root.find(category)
        else:
            cat = root.find(category)
            
        if (cat == None):
            return False
        
        if (not tag):
            return True
        else:        
        
            cat_tag = cat.find(tag)
            if (cat_tag == None):
                return False
            
            if (not subtag):
                return True
            else:
                cat_subtag = cat_tag.find(subtag)
                if (cat_subtag == None):
                    return False
                
                return True


    # Returns true if given tag contains the given value
    def HasTagValue(self, value, category, tag = None, subtag = None, root = None):
        
        if (not value):
            return False
        
        if (root == None):
            cat = self.__root.find(category)
        else:
            cat = root.find(category)
            
        if (cat == None):
            return False
        
        if (not tag):
            if (RemoveQuotes(cat.text) == value):
                return True
            else:
                return False
        else:        
        
            cat_tag = cat.find(tag)
            if (cat_tag == None):
                return False
            
            if (not subtag):
                if (RemoveQuotes(cat_tag.text) == value):
                    return True
                else:
                    return False
            else:
                cat_subtag = cat_tag.find(subtag)
                if (cat_subtag == None):
                    return False
                
                if (RemoveQuotes(cat_subtag.text) == value):
                    return True
                else:
                    return True
        
        
    
    
    # Returns a list of all child elements with given key
    def GetCollection(self, category, key, tag = None, subtag = None, root = None, required = True):
        
        if (root == None):
            cat = self.__root.find(category)
        else:
            cat = root.find(category)

        if (cat == None):
            if (required):
                print "Error in settings file: " + category + " tag not found"
            return None
        
        if (not tag):
            ret = cat.findall(key)
        else:
            cat_tag = cat.find(tag)
            if (cat_tag == None):
                if (required):
                    print "Error in settings file: " + tag + " tag not found"
                return None
            
            if (not subtag):
                ret = cat_tag.findall(key)
            else:
                cat_subtag = cat_tag.find(subtag)
                if (cat_subtag == None):
                    if (required):
                        print "Error in settings file: " + subtag + " tag not found"
                    return None
                
                ret = cat_subtag.findall(key)
        
        return ret


    # Conversion of elements    
         
        
    
    
# Settings object. It should be used instead of Settings class (in some way, its a kind of singleton)
SETTINGS = Settings()






def RemoveQuotes(text):
    
    ret = ""
    for ch in text:
        if (ch != '\"'):
            ret = ret + ch

    return ret



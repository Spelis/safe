
#!  REQUIRED CODE: ------------------------------#
                                                 #
from sys import path                             #
path.insert(0, './plugins')                      #
                                                 #
def use(plugin_name):                            #
    return eval(f'__import__("{plugin_name}")')  #
                                                 #
# -----------------------------------------------#

#* example for importing a plugin: random = use('random')

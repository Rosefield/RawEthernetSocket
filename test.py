from http import *

resp = ""
get = HTTPGet('http://david.choffnes.com/classes/cs4700sp15/2MB.log')

print get.getFilename()


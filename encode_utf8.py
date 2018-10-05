import os 
import codecs 
import chardet 
  
def convert(filename): 
	try: 
		content=codecs.open(filename,'r').read() 
		source_encoding=chardet.detect(content)['encoding'] 
		print source_encoding
		if source_encoding != "UTF-8" or source_encoding != "utf-8":
			content=content.decode(source_encoding,errors = 'ignore').encode("UTF-8") 
			codecs.open(filename,'w').write(content) 
	except IOError as err: 
		print("I/O error:{0}".format(err)) 
  
def explore(dir):
	for root,dirs,files in os.walk(dir):
		for file in files: 
			if os.path.splitext(file)[1]=='.lua': 
				print file
				path=os.path.join(root,file) 
				convert(path)
  
def main(): 
	explore(os.getcwd() + "/src")
  
if __name__=="__main__": 
	main()
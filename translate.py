#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import sys
from chardet import detect
reload(sys)
sys.setdefaultencoding('utf8')
#print sys.getdefaultencoding()

def listFiles(dirPath):
	fileList=[]
	for root,dirs,files in os.walk(dirPath):
		for fileObj in files:
			fileList.append(os.path.join(root,fileObj))
	return fileList
 
def main():
	fileDir = os.getcwd() + "/src"
	logData = open("./log.txt", 'w+')
	fileList = listFiles(fileDir)
	fData = open("Language.lua", "r+")
	fData.seek(0, 0)
	fData.truncate()
	fData.write('local Language = {\n')
	#print(fileList)
	for fileObj in fileList:
		num = 1
		strCounter = 1
		f = open(fileObj,'r+')
		fileName = os.path.basename(fileObj).split('.')[0]
		all_the_lines=f.readlines()
		f.close() 
 
		strTable = []
		numStrTable = []
		numStrTable.append(fileName+' = {\n')
 
		if ("cocos/" in fileObj) or (os.path.basename(fileObj).split('.')[1] != "lua") :
			print >> logData,"ignore file : " + fileObj
			continue
		fileStart = False
		for line in all_the_lines: 
			regex = re.compile("(['\"])(?:\\\.|.)*?\\1")
			regex1 = re.compile(u"[\u4e00-\u9fa5]+")
			regex2 = re.compile(u"print")
			regex3 = re.compile(u"cclog")
			line2 = line.decode('utf8')	# writable line
			line1 = line.decode('utf8')	# temp line
			# ingore print and cclog
			if len(regex2.findall(line1)) + len(regex3.findall(line1)) == 0 :
				# iterate over all found quotes pairs
				for match in regex.finditer(line1):	
					start = match.start()
					end = match.end()	
					temp = line1[start:end]
					counter = 0
					for match1 in regex1.finditer(temp):
						counter += 1
					if counter > 0:
						nStr = 'Language.str%s'%strCounter
						if not fileStart:
							print >> logData,'[file] ' + fileObj
							fileStart = True
						print >> logData,'[line] %d'% (num) + temp + " ------> " + nStr				
						line2 = line2.replace( temp, nStr)					
						mStr = 'str%s'%strCounter
						numStrTable.append(mStr+' = '+temp+',\n')
						strCounter += 1
 
			strTable.append(line2)
			num = num + 1
 
		numStrTable.append('},\n')
		# if fit str exits insert require str
		if strCounter > 1 :
			# 另起路径
			'''
			dirPath = fileObj.replace( "dir1", "dir2")
			targetPath = dirPath.split(os.path.basename(dirPath))[0]
			if os.path.exists(targetPath) == 0 :
				os.mkdir(targetPath)
				'''
			# 当前文件上修改
			targetF = open(fileObj,'w')
			targetF.seek(0, 0)
			targetF.truncate()
			
			targetF.write('''local Language = require("Language").''' + fileName + "\n")
			for lines in strTable :
				targetF.write(lines)
 
			targetF.close() 
 
			# write Language data 
			for lines2 in numStrTable :
				fData.write(lines2)
	
	fData.write('}\nreturn Language')
	fData.close()  
 
if __name__=='__main__':
	main() 
 

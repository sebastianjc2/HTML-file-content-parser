# Filename: CaballeroSebastian_066_P2.py

### ADD YOUR NAME, STUDENT ID AND SECTION NUMBER BELOW ###
# NAME: Sebastian J. Caballero Diaz
# STUDENT ID: 802-19-2461
# SECTION: 066

"""Parse the contents of an HTML file and output the internal resources used.

We are looking for tags of interest: a, script, link, and img.
Within each tag of interest we're looking for a particular attribute of
interest (href for a & link, src for script & img).
A list is created for each type of tag, storing all of the internal 
resources referenced by tags of that type.
Finally, the results are stored in an output file.

Input:  The file index.html will be used as an input file
Output: The results will be stored in a file named index_resources.txt
"""

def load_data():
	"""Returns the contents of index.html in a list, or None if an error occurs."""
	try:
		fh = open('index.html')
	except:
		lstOfLines = None
	else: # Only gets executed if no exception was raised
		lstOfLines = fh.readlines()
		fh.close()
	return lstOfLines


def get_tag_of_interest(line):
	"""Return a tag of interest if one is found in the line, or None otherwise."""
	if '<a ' in line:
		startTag = line.find('<a ')
	elif '<script' in line:
		startTag = line.find('<script')
	elif '<link' in line:
		startTag = line.find('<link')
	elif '<img' in line:
		startTag = line.find('<img')
	else:
		return None     #No tags of interest found
	# Now retrieve the openingTag from what is found
	endTag = line.find('>', startTag)
	openingTag = line[startTag:endTag + 1]
	return openingTag
	# Look for any of the tags of interest within this line.
	# If one is found, return that tag (from '<' to '>' of the opening tag only)
	# For example:
	#    If line is "Here is a <a href='sample.html' target='_blank'>sample</a> link",
	#    then we would return "<a href='sample.html' target='_blank'>".


def get_attr_of_interest(openingTag):
	"""Return value of attribute of interest if one is in the tag, or None otherwise."""
	if openingTag.startswith('<a ') or openingTag.startswith('<link'): # Both are with href so can be merged
		if 'href' in openingTag:
			hrefPos = openingTag.find('href')
			startAttr = openingTag.find('"', hrefPos) # Look for the quotes after href to not include any quote that could be before
			endAttr = openingTag.find('"', startAttr + 1) #Find the final quote starting one position after the first so it doesnt find the same one
			res = openingTag[startAttr+1:endAttr]
			if res.startswith('http'):
				return None # http is not local so it wont be included
			return res
		else:
			return None  #No attribute of interest found
	elif openingTag.startswith('<script') or openingTag.startswith('<img'): # both include src so can be merged
		if 'src' in openingTag:
			srcPos = openingTag.find('src')
			startAttr = openingTag.find('"', srcPos)
			endAttr = openingTag.find('"', startAttr + 1)
			res = openingTag[startAttr+1:endAttr]
			if res.startswith('http'):
				return None
			return res
		else:
			return None  #No attribute of interest found
	# Look for the attribute of interest for the tag specified.
	# If it is found, return that attribute's value (should be between quotes).
	# For example:
	#    If openingTag is "<a href='sample.html' target='_blank'>",
	#    then we would return "sample.html".
	# Remember to avoid external resources and mailing hyperlinks.
	# Note: It's possible that a tag of interest has no attribute of interest.
	pass # Remove this line once you add your code


def write_results(outFH, sectionName, listOfResources):
	"""Write the resources of a particular section to an already opened file."""
	if len(listOfResources) != 0: # If there is not a single resource for one of the sections, don't write it
		outFH.write(sectionName + '\n')
		for i in listOfResources: # Iterate through the list and write each resource
			outFH.write(i + '\n')
	# outFH should be the file handle of an output file
	# Remember that the section name must be followed by a colon,
	# and the list of resources must be in alphabetical order.
	# If there are no resources for a section, nothing should be outputted.


def main():
	linesInFile = load_data()	
	if linesInFile is None:
		print('ERROR: Could not open index.html!')
		exit()
	# Make the list of resources
	css = []
	javaScript = []
	image = []
	hyperlink = []

	for line in linesInFile:
		openingTag = get_tag_of_interest(line)
		if openingTag is not None: # if it retrieved something, then:
			res = get_attr_of_interest(openingTag)
			if res is not None: # If there's an attribute, then:
			#append the attributes to the lists
				if openingTag.startswith('<a '):
					hyperlink.append(res)
				elif openingTag.startswith('<script'):
					javaScript.append(res)
				elif openingTag.startswith('<link'):
					css.append(res)
				elif openingTag.startswith('<img'):
					image.append(res)
	#open the new file that is going to be made and write on it
	outFH = open('index_resources.txt', 'w')
	#make sure the lists are in alphabetical order
	hyperlink.sort()
	javaScript.sort()
	css.sort()
	image.sort()
	#write the results for each list
	write_results(outFH, 'CSS:', css)
	write_results(outFH, 'JavaScript:', javaScript)
	write_results(outFH, 'Images:', image)
	write_results(outFH, 'Hyperlinks:', hyperlink)
	outFH.close() # Close the file

	# Loop through linesInFile and process each line
	# In each line look for a tag of interest.
	# If such a tag is found, within that tag look for an attribute of interest
	# If such an attribute is found, store its value in a list, depending
	#    on what type of tag it was.
	# Once you loop through all of the lines, write the results.
	# For each section of output, call write results with the "title" of that 
	#     section and the list of resources for that section.
	#     To minimize I/O, open the output file once, before your calls to
	#     write_result, and then close it after all calls to write_results.


# This line makes python start the program from the main function
# unless our code is being imported
if __name__ == '__main__':
    main()

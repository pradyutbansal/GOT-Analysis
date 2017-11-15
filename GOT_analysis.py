import string
import csv

episodes = 10
new_scene_word = [ "TITLE SEQUENCE\n","CUT TO", "EXT","INT", "ALL","MEN"]


ignored_words = ["The","I","Ill","But","Hes","Shes", "Im","Will","On","One","Many","In","Slow","Zoom","Wall",
            "My", "He", "His","Him","Hers", "Her","She", "We", "Their", "You", "Your", "It","Its","If","Throne",
            "This", "That", "There", "A","They","Theyre","Theyll","Battle","Cut","Both","An",
            "Who","Whos","O", "Oh","Why", "What","When","Where","More","Faith","Sept", "Only","To","Together","How",
            "House", "Houses", "Clan", "Lords", "Ladies", "Kings", "Dothraki", "Grace", 
            "Father", "Mother", "Uncle", "Aunt", "Brother", "Brothers", "Sons","Grandmother","Grandfather", 
            "Not", "Stone", "Men", "Man", "Guard", "Was", "Bread", "Wind", "Tongue", "Another","Crowd", "Of","Kingsguard"]

title_words = ["Lord", "Lady", "King", "Queen", "Regent", "Steward", "Prince", "Princess","Nights",
            "Ser", "Maester", "Captain", "Commander", "Magister", "Master", "Builder",
            "Septon", "Knight", "Shipwright", "Goodwife", "Ranger", "Squire","Protector",
            "Khal", "Ko","Oldtown","Man #2","Man #1","Girl","Woman", "Guard","Captain","Guard Captain"]
house_names = ["Lannister", "Frey", "Bolton","Stark","Mormont", "Baelish","Tully","Greyjoy","Clegane"]
general_words = ["Young", "Old", "Fat", "Big", "Little", "Bastard", "Boy", "Men","Ah","Try", "Sooner","Get","Ant","Alredy","Do"
            "High", "Great", "Grand", "First", "Second", "See","Mmhmmm", "Go","Sometimes","Much","Youre","Think"
            "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", 
            "Black", "Red", "Green", "Blue", "White","North","South","East","West","Andals", "Kingdoms",
            "Land", "Lands", "Sea", "Seas", "Island", "Islands", "Isles", "Bay", "River", "Shore", "Point", 
            "City", "Cities", "Alley", "Gate", "Keep", "Market", "Tower", "Hall", "Rock", "Castle", "Lane", 
            "Cruel", "Bold", "Brave", "Good", "Strong", "Bitter", "Sweet", "Bad", "Bless", "Ive", "Aside",
            "Flowers", "Storm", "Bull", "Long", "Spring", "Bear", "Hot", "Pie", "Ben", "Iron", "Watch","Wedding",
            "Horn","Name","Still", "And", "Please", "Listen", "Come","Once","Would"]
ignored_characters = ["MEN","MALE VOICE #1", "MALE VOICE #2"]

all_ignored_words = ignored_words+title_words+general_words+house_names

def generate_all_characters(file):
	all_character_dict={}
	with open(file, mode = 'rU') as infile:
		reader = csv.DictReader(infile)
		for row in reader:
			all_character_dict.setdefault(row[0],row[1:])
	return all_character_dict



def create_basic_log(text_file):
	script = open(text_file,'r')
	character_log = []	
	for line in script.readlines():
		words = strip_non_ascii(line)
		words = words.split(":")
		if(words[0].isupper()):
			if (words[0] in new_scene_word):
				character_log.append([words[0]])
			if(words[0] not in (new_scene_word+ignored_characters)):
				character_log[len(character_log)-1].append(words[0])

	script.close()
	return character_log

def create_stage_direction_log(text_file):
	script = open(text_file,'r')
	directions_log = []	
	for line in script.readlines():
		line = line.strip("\n")
		words = strip_non_ascii(line)
		words = words.split(":")
		if(words[0].isupper()):
			if (words[0] in new_scene_word):
				directions_log.append([words[0]])
			if (words[0] == 'CREDITS'):
				directions_log.append([words[0]])
		else:
			if(words[0] not in (new_scene_word)):
				directions_log[len(directions_log)-1].append(words[0])
	script.close()
	return directions_log

def create_script_log(text_file):
	script = open(text_file,'r')
	script_log = []	
	for line in script.readlines():
		words = strip_non_ascii(line)
		words = words.split(":")
		if(words[0].isupper()):
			if (words[0] in new_scene_word):
				script_log.append([words[0]])
			if(words[0] not in (new_scene_word)):
				script_log[len(script_log)-1].append(words)
	script.close()
	return script_log

def character_finder(line):
	line = line.translate(None, string.punctuation.replace("-",""))
	line = strip_non_ascii(line)
	
	words = line.split()
	characters = []

	for i in words:
		if(i.isupper() and i.title() not in all_ignored_words):
			characters.append(i)
	return characters



def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def clean_log(character_log):
	for scene in (character_log):
		if(scene[0] != 'CREDITS'):
			scene.pop(0)
	character_log = [scene for scene in character_log if scene!=[]]
	return character_log



def make_character_list(character_log):
	character_list =[]
	for scene in character_log:
		if(len(scene) > 0):
			inscene_characters = list(set(scene))
			for character in inscene_characters:
				if character not in character_list:
					character_list.append(character)
	return character_list

def update_character_list():
	pass
'''
makes a dictionary of dictionaries to work as a matrix to keep track of the interaction.
'''
def make_matrix(character_list):
	temp_dict = dict((k,0) for k in character_list)
	matrix = dict((k,(dict((k,[0 for x in range(episodes)]) for k in character_list))) for k in temp_dict)
	return matrix

'''
creates an interactiong based on being present in the scene together. Also keeps track
of which episode the interaction occurred in.
'''
def make_interactions_1 (character_log,matrix):	
	temp_matrix = matrix
	episode = 0
	for scene in character_log:
		if(len(scene) > 0):
			inscene_characters = list(set(scene))
			if('CREDITS' in inscene_characters):
				episode += 1
			for character1 in inscene_characters:
				for character2 in inscene_characters:
					if(character1 != character2):
						temp_matrix[character1][character2][episode] +=1
	return temp_matrix

'''
Interactions are based on speech and the order of speaking. A->B->C
'''
def make_interactions_2(character_log,matrix):
	temp_matrix = matrix
	episode = 0
	for scene in character_log:
		if(len(scene) > 0):
			inscene_characters = list(set(scene))
			if('CREDITS' in inscene_characters):
				episode += 1
			for i in range(1,len(scene)):
				character1 = scene[i-1]
				character2 = scene[i]
				if(character1 != character2):
					temp_matrix[character1][character2][episode] += 1
	return temp_matrix


#Adds a connection to everybody in the scene when a name is spoken
def make_interactions_3(script_log,matrix,character_log):

	temp_matrix = matrix
	episode = 0
	for scene in script_log:
		inscene_characters = list(set(character_log[script_log.index(scene)])) 
		for dialogue in scene:
			if(dialogue[0] not in all_ignored_words):
				character1 = dialogue[0]
			referenced_characters = character_finder(dialogue[1])
			if(character1 == 'CREDITS'):
				episode += 1
			for character2 in referenced_characters:
				if(character2 in temp_matrix[character1]):
					temp_matrix[character1][character2][episode] += 1	
					temp_matrix = connect(temp_matrix,inscene_characters,character2,episode)				
				elif(character2 not in temp_matrix[character1]):
					temp_matrix[character1][character2] = [0 for x in range(episodes)]
					temp_matrix[character1][character2][episode] += 1
					temp_matrix = connect(temp_matrix,inscene_characters,character2,episode)				
					if(character2 not in character_list):
						character_list.append(character2)
				else:
					temp_matrix[character1][character2][episode] += 1
					temp_matrix = connect(temp_matrix,inscene_characters,character2,episode)				
		
	return temp_matrix

##Makes a matrix based on interactions in the stage directions in a scene
def make_interactions_4(stage_direction_log,matrix):
	temp_matrix = matrix
	episode = 0
	for scene in stage_direction_log:
		if(len(scene) > 0):
			stage_direction = ". ".join(scene)
			described_characters = character_finder(stage_direction)
			inscene_characters = list(set(described_characters))
			if(inscene_characters == ["CREDITS"]):
				episode += 1
			for character1 in inscene_characters:
			 	for character2 in described_characters:
			 		if(character1 != character2):
			 			if(character1 not in temp_matrix.keys()):
			 				temp_matrix[character1]={}
			 				if(character2 not in temp_matrix[character1]):
			 					temp_matrix[character1][character2] = [0 for x in range(episodes)]
								temp_matrix[character1][character2][episode] += 1
								temp_matrix = connect(temp_matrix,inscene_characters,character2,episode)
							else:
								temp_matrix[character1][character2][episode] +=1
			 			elif(character2 not in temp_matrix[character1]):
			 					temp_matrix[character1][character2] = [0 for x in range(episodes)]
								temp_matrix[character1][character2][episode] += 1
								temp_matrix = connect(temp_matrix,inscene_characters,character2,episode)
						else:
							temp_matrix[character1][character2][episode] +=1				
			
	return temp_matrix



#Creates a new connection between characters in a scene and a given character
def connect(matrix,inscene_characters,character2,episode):
	for character1 in inscene_characters:
		if(character1 not in matrix):
			matrix[character1]={}
		if(character2 not in matrix[character1]):
			matrix[character1][character2] = [0 for x in range(episodes)]
		matrix[character1][character2][episode]+=1
	return matrix

def write_to_txt(matrix,file,type):
	page = open(file,"w")
	page.write("Source,Target,Weight,Type\n")
	log = ""
	episode = 1
	character_list = make_node_list(matrix)
	for character1, interactions in matrix.iteritems():
		for character2, degree in interactions.iteritems():
			log = character1 + "," + (character2) + "," + str(sum(degree)) + "," + type + "\n"
			if(sum(degree) != 0 and character2 != character1):
				page.write(log)
	page.close()


def write_timestamps_txt(matrix,file,type):
	page = open(file,"w")
	page.write("Source,Target,Weight,Start,End,Type\n")
	log = ""
	entry_dict = {}
	character_list = make_node_list(matrix)
	for character1, interactions in matrix.iteritems():
		for character2, degree in interactions.iteritems():
			episode = 1
			for value in degree:
				log = character1 + "," +character2 + "," + str(value) + "," + str(episode*5)+ "," +str(5*(episode +1))+","+ type +"\n"
				episode += 1
				if(value != 0 and (character2 != character1) and (character1.title() not in all_ignored_words and character2.title() not in all_ignored_words)):
					page.write(log)
	page.close()

def write_txt_nodes(matrix,file):
	page = open(file,"w")
	page.write("Id,Label\n")
	log = []
	log = make_node_list(matrix)
	for character in log:
			node = str(log.index(character)+1)+","+ character+"\n" 
			page.write(node)
	page.close()



def write_node_timestamps_txt(matrix,file):
	page = open(file,"w")
	page.write("Id,Label,Start,End\n")
	log = ""
	entry_dict = {}
	character_list = make_node_list(matrix)
	for character1, interactions in matrix.iteritems():
		for character2, degree in interactions.iteritems():
			episode = 1
			for value in degree:
				episode += 1
				if(value != 0 and (character2 != character1) and (character1.title() not in all_ignored_words and character2.title() not in all_ignored_words)):
					#page.write(log)
					if(character1 not in entry_dict):
						entry_dict[character1] = episode*5
					if(character2 not in entry_dict):
						entry_dict[character2] = episode*5
					else:
						entry_dict[character1] = min(entry_dict[character1],(episode*5))
						entry_dict[character2] = min(entry_dict[character2],(episode*5))
	for character1,scene in sorted(entry_dict.iteritems()):
		log = character1 + ","+character1+","+str(scene)+","+str(55)+"\n"
		page.write(log)
	page.close()
def make_node_list(matrix):
	log = []
	for character1, interactions in matrix.iteritems():
		log.append(character1)
		for character2, degree in interactions.iteritems():
			log.append(character2)
	log = sorted(list(set(log)))
	return log

############################################
#CALLS
#Character_log is the order in whihc the characters come in throught the scene
# character_log = create_basic_log()
# character_log = clean_log(character_log) 

# # #character_list is the list of all characters
# character_list = make_character_list(character_log)
# matrix = make_matrix(character_list)
# # # matrix = make_interactions_2(character_log,matrix)
# stage_direction = clean_log(create_script_log())
# # # print(character_log[7])

# matrix = make_interactions_3(stage_direction, matrix, character_log)
# # #print(clean_log(stage_direction))
# # # #matrix["DAVOS"]['DAVOS'] =1
# # print((matrix["BRAN"]["HODOR"]))
# # # print(matrix['SANSA'])
# # write_timestamps_txt(matrix,"timelog_int_3")
#write_txt_nodes(matrix,"node_list")


#############################
#Interaction 1
character_log = create_basic_log("season5.txt")
character_log = clean_log(character_log) 
character_list = make_character_list(character_log)
matrix = make_matrix(character_list)
matrix1 = make_interactions_1(character_log,matrix)
# write_to_txt(matrix1,"S5_int_1_edges","undirected")
# write_timestamps_txt(matrix1,"S5_timelog_int_1_edges",'undirected')

############################################
##INTERACTION 2
# character_log = create_basic_log("season5.txt")
# character_log = clean_log(character_log) 
# character_list = make_character_list(character_log)
# matrix = make_matrix(character_list)
matrix = make_interactions_2(character_log,matrix)
# write_to_txt(matrix2,"S5_log_int_2_edges","undirected")
# write_timestamps_txt(matrix2,"S5_timelog_int_2_edges","undirected")

#######################################################
##INTERACTION 3
# character_log = create_basic_log("season5.txt")
# character_log = clean_log(character_log) 
# character_list = make_character_list(character_log)
# matrix = make_matrix(character_list)
script_log = clean_log(create_script_log("season5.txt"))
matrix = make_interactions_3(script_log,matrix,character_log)
# write_to_txt(matrix3,"S5_log_int_3_edges.csv","Directed")
# write_timestamps_txt(matrix3,"S5_timelog_int_3_edges.csv","Directed")




###############################################
##INERACTION 4
# character_log = create_basic_log("season5.txt")
# character_log = clean_log(character_log) 
# character_list = make_character_list(character_log)
# matrix = make_matrix(character_list)
stage_direction_log = clean_log(create_stage_direction_log("season5.txt"))
matrix4 = make_interactions_4(stage_direction_log,matrix)
write_to_txt(matrix4,"S5_log_int_all_edges.csv","undirected")
write_timestamps_txt(matrix4,"S5_timelog_int_all_edges.csv","undirected")
write_node_timestamps_txt(matrix4,"nodes.csv")
print(matrix4["DAVOS"])
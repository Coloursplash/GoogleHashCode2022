# Google Hashcode 2022

import math as m

#---------------------------------------
# GLOBALS
#---------------------------------------

FILENAME = "inp.txt"

contributors = []
projects = []
curr_day = 0
points = 0

#---------------------------------------
# CLASSES
#---------------------------------------

class Contributor:

    # skill issue
    def __init__(self, name: str, skills: dict):
        self.name = name
        self.skills = skills
        
        self.working = False # is the contributor currently doing a project?
        self.position = "" # empty, contributor, mentee or mentor
    
    def get_skill_level(self, skill_name: str):
        if skill_name in self.skills:
            lvl = self.skills[skill_name]
        else: lvl = 0
        return lvl
    
    def __repr__(self):
        return self.name

class Project:

    def __init__(self, name: str, duration: int, score: int, best_before: int, roles: dict):
        self.name = name
        self.duration = duration
        self.score = score
        self.best_before = best_before
        self.roles = roles

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True 
    else:
        return False

def needed_skills(skills, roles):
    output = {}

    for i in skills.keys():
        if i in roles.keys() and skills[i] >= roles[i]:
            output[i] = skills[i]

    return output


def do_project(contributors, project):
    global projects_sorted, contributors_sorted, curr_day, points
    
    end_day = curr_day + project.duration    

    points += 1 if (project.score - max(1, end_day - project.best_before)) <= 1 else (project.score - max(1, end_day - project.best_before)) 

   
    
    #print(f"we were {end_day - project.best_before} days late for project {project.name}")

    for i in contributors:
        i.working = True

    # picking optimised mentors and mentees 
    # sorted_mentors = sorted(contributors, key=lambda x: m.prod(needed_skills(x.skills, project.roles).items()) ) # smallest to biggest? 
    
    for i in contributors:
        for j in list(i.skills.keys()):
            if j in list(project.roles.keys()): 
                # apologies for bad code. This says:
                # Is a skill (required for the project) 1 less or equal to the skill level required by the role 
                #r = list(project.roles.keys())
                #a = skills[j] == project.roles[r[list(project.roles.values()).index(j)]] 
                #b = skills[j]+1 == project.roles[list(project.roles.keys())[list(project.roles.values()).index(j)]]
                #if a or b

                #print("\n\n\n\n")
                #print(i.skills.keys())
                #print(i)
                #print(project.name)
                #print(list(project.roles.keys()))
                #print(list(project.roles.keys())[list(project.roles.keys()).index(j)])
                #print(skills)
                #print(j)

                

                if i.skills[j] == project.roles[list(project.roles.keys())[list(project.roles.keys()).index(j)]]:
                    i.skills[j] += 1
    
    curr_day = end_day

#---------------------------------------
# INPUT
#---------------------------------------

with open(FILENAME, 'r') as f:
    contents = f.readlines()

no_contributors, no_projects = map(int, contents[0].strip().split(' '))

line_idx = 1 # skip first line

for i in range(no_contributors):
    name, no_skills = contents[line_idx].strip().split(' ')[0], int(contents[line_idx].strip().split(' ')[1])
    skills = {}

    line_idx += 1

    for i in range(no_skills):
        skills[contents[line_idx].strip().split(' ')[0]] = int(contents[line_idx].strip().split(' ')[1])
        line_idx += 1
    
    contributors.append(Contributor(name, skills))

for i in range(no_projects):
    tmp = contents[line_idx].strip().split(' ')
    name = tmp[0]
    duration = int(tmp[1])
    score = int(tmp[2])
    best_before = int(tmp[3])
    no_roles = int(tmp[4])

    roles = {}

    line_idx += 1

    for i in range(no_roles):
        roles[contents[line_idx].strip().split(' ')[0]] = int(contents[line_idx].strip().split(' ')[1])
        line_idx += 1
    
    projects.append(Project(name, duration, score, best_before, roles))

#---------------------------------------
# MAIN
#---------------------------------------

projects_sorted = sorted(projects, key=lambda x: x.score, reverse = True)
tmp = {}
for contributor in contributors:
    max_lvl = 0
    for skill in contributor.skills:
        max_lvl = max(max_lvl, contributor.skills[skill])
    tmp[str(max_lvl)] = contributor

tmplist = sorted(list(tmp.items()))

sorted_contributors = []
for item in tmplist:
    sorted_contributors.append(item[1])

output = []

#while len(projects_sorted) > 0:
#print("test")
for project in projects_sorted:

    
    
    # can do project
    cohort = []
    cohort_names = []
    tmp_contributors = sorted_contributors 

    for i in list(project.roles.keys()):
        for contributor in tmp_contributors:
            if i in list(contributor.skills.keys()) : #common_member(list(contributor.skills.keys()), project.roles.keys()):
                if contributor.skills[i] >= project.roles[i]:
                    cohort.append(contributor)
                    cohort_names.append(contributor.name)
                    tmp_contributors.remove(contributor)
                    continue
    
    
    #do_project(cohort, project)
    
    if len(cohort) == len(project.roles):
        output.append([project.name, cohort_names])
        print(project.name, cohort_names)

        do_project(cohort, project)

        #projects_sorted.remove(project)

print(points)

with open("output.txt", "w") as f:
    content = str(len(projects_sorted)) + '\n'
    for pair in output:
        content += pair[0] + '\n' + " ".join(pair[1]) + '\n'
    f.write(content)

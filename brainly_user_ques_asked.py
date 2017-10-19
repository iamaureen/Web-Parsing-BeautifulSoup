import requests
from bs4 import BeautifulSoup
import json

#parses through user profile url and extracts all the user activity related info

page = requests.get("https://brainly.com/profile/ishratahmedmren-4755517/submitted")
print(page.status_code) #prints status_code property

#parse this document using BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify()) #prints the byte content in html format
#
question = {} #store info about each question that is Answered by the user
question_list = [] #store the list of questions answered
#
div_tasks_solved = soup.find_all('div', {"id":"tasks-solved"})
# print(len(div_tasks_solved)) #length=1; because only one div is present with this class

# #finds all the li in the above div and store it into task_list
for li in div_tasks_solved:
    task_list = li.find_all('li', class_ ="task")
    #print(task_list)

#prints number of tasks in the task_list
#print(len(task_list))

# each task has a task-header and task-content
# get the task header, #get the task content

for tasks in task_list:
    #contains metadata about the question
    task_header = tasks.find('div', class_ ="task-header")
    task_header = task_header.find('span', class_ = "fleft")

    #get the name who posted the question
    name = task_header.find('a', class_="title").text
    question['questionAnsweredBy'] = name

    #get the rank
    rank = task_header.find('span', class_="level").select('a')[0].text
    question['answererRank'] = rank

    #get the category
    category = task_header.find('span', class_="category").select('a')[0].text
    question['questionCategory'] = category



    task_content = tasks.find('div', class_ ="task-content")
    #print(task_content)
    for a in task_content.find_all('a'):
        #get question ID
        #print(a.get('href').split("/")[2])
        question['questionID'] = a.get('href').split("/")[2]
        #get question text
        question['questionText'] = a.text.replace("\n", " ")
        question_list.append(question.copy())



#print(question_list)
#print(json.dumps(question_list))
#https://stackoverflow.com/questions/37661863/convert-a-list-to-json-objects
print(json.dumps({'questionAnswered': question_list}))




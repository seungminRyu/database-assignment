from django.core.checks import messages
from django.db.models import fields
from django.shortcuts import render
from django.views import generic
from django.db import connection
import csv

def getInsertStudentsSql():
    path = 'myapp/templates/myapp/students.csv'
    f = open(path, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    arr = []

    for line in rdr:
        stuID = '\"' + line[0] + '\"'
        name = '\"' + line[1] + '\"'
        score = line[2]
        county = '\"' + line[3] + '\"'
        str = '(' + stuID + ',' + name + ',' + score + ',' + county + ')'
        arr.append(str)
    
    insertSql = 'INSERT INTO Students(studentID, name, score, county)'
    valuesSql = 'VALUES ' + ",".join(arr)
    ret = insertSql + valuesSql
    f.close
    return ret

def getInsertProfessorsSql():
    path = 'myapp/templates/myapp/professors.csv'
    f = open(path, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    arr = []

    for line in rdr:
        facID = '\"' + line[0] + '\"'
        name = '\"' + line[1] + '\"'
        age = line[2]
        county = '\"' + line[3] + '\"'
        str = '(' + facID + ',' + name + ',' + age + ',' + county + ')'
        arr.append(str)
    
    insertSql = 'INSERT INTO Professors(facultyID, name, age, county)'
    valuesSql = 'VALUES ' + ",".join(arr)
    ret = insertSql + valuesSql
    f.close
    return ret

def getInsertCountiesSql():
    path = 'myapp/templates/myapp/counties.csv'
    f = open(path, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    arr = []

    for line in rdr:
        name = '\"' + line[0] + '\"'
        population = line[1]
        city = '\"' + line[2] + '\"'
        str = '(' + name + ',' + population + ',' + city + ')'
        arr.append(str)
    
    insertSql = 'INSERT INTO Counties(countyName, population, city)'
    valuesSql = 'VALUES ' + ",".join(arr)
    ret = insertSql + valuesSql
    f.close
    return ret

def getInsertCovidSql():
    path = 'myapp/templates/myapp/covid.csv'
    f = open(path, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    arr = []

    for line in rdr:
        ID = '\"' + line[0] + '\"'
        city = '\"' + line[1] + '\"'
        str = '(' + ID + ',' + city + ')'
        arr.append(str)
    
    insertSql = 'INSERT INTO COVID(patientID, city)'
    valuesSql = 'VALUES ' + ",".join(arr)
    ret = insertSql + valuesSql
    f.close
    return ret

def getStudents():
    cursor = connection.cursor()
    sql = "SELECT * FROM Students"
    result = cursor.execute(sql)
    students = cursor.fetchall();

    connection.commit
    connection.close()
    ret = []
    for student in students:
        row = {
            'studentID': student[0],
            'name': student[1],
            'score': student[2],
            'county': student[3],
        }
        ret.append(row)
    return ret
    
def getProfessors():
    cursor = connection.cursor()
    sql = "SELECT * FROM Professors"
    result = cursor.execute(sql)
    professors = cursor.fetchall();

    connection.commit
    connection.close()
    ret = []
    for professor in professors:
        row = {
            'facultyID': professor[0],
            'name': professor[1],
            'age': professor[2],
            'county': professor[3],
        }
        ret.append(row)
    return ret
    
def getCounties():
    cursor = connection.cursor()
    sql = "SELECT * FROM Counties"
    result = cursor.execute(sql)
    counties = cursor.fetchall();

    connection.commit
    connection.close()
    ret = []
    for county in counties:
        row = {
            'countyName': county[0],
            'population': county[1],
            'city': county[2],
        }
        ret.append(row)
    return ret

def getCOVID():
    cursor = connection.cursor()
    sql = "SELECT * FROM COVID"
    result = cursor.execute(sql)
    covids = cursor.fetchall();

    connection.commit
    connection.close()
    ret = []
    for covid in covids:
        row = {
            'patientID': covid[0],
            'city': covid[1],
        }
        ret.append(row)
    return ret

def getQuery1():
    cursor = connection.cursor()
    sql = "SELECT county, AVG(score) FROM Students group by county"
    result = cursor.execute(sql)
    query1 = cursor.fetchall();

    connection.commit
    connection.close()
    ret = []
    for record in query1:
        row = {
            'county': record[0],
            'avgScore': record[1],
        }
        ret.append(row)
    return ret

def home(request):
    targetFile = request.GET.get('target')
    sql = ''
    message = ''

    # csv에서 데이터 읽기
    if targetFile:
        if targetFile == 'students':
            sql = getInsertStudentsSql()
        elif targetFile == 'professors':
            sql = getInsertProfessorsSql()
        elif targetFile == 'covid':
            sql = getInsertCovidSql()
        elif targetFile == 'counties':
            sql = getInsertCountiesSql()

        # sql에 데이터 저장
        try:
            cursor = connection.cursor()
            result = cursor.execute(sql)
            categories = cursor.fetchall();

            connection.commit
            connection.close()
            print("Success inserting values")
            message = targetFile + ' db에 데이터를 추가하였습니다'
        except:
            connection.rollback()
            print("Failed inserting values")
    
    students = getStudents()
    professors = getProfessors()
    counties = getCounties()
    covids = getCOVID()

    query1 = getQuery1()
    
    return render(request, 'myapp/index.html', {
        'students': students,
        'professors': professors,
        'counties': counties,
        'covids': covids,
        'query1': query1,
        'message': message
    })

# 이전 파일 
# def search(request):
#     students = Students.objects.all()
#     keyword = request.GET.get('q')
#     result = []
#     for object in students.filter(firstname__contains=keyword):
#         result.append(object)
#     resultExist = False
#     if (len(result) == 0):
#         resultExist = False
#     else :
#         resultExist = True
#     return render(request, 'myapp/search.html', {"results": result, "resultExist": resultExist})

# def create(request):
#     form = StudentsForm()
#     return render(request, 'myapp/create.html', {"form": form})

# def check_post(request):
#     if request.method == "POST":
#         form = StudentsForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.student_save()
#             message = "학생정보를 추가하였습니다."
#             return render(request, 'myapp/success.html', {"message": message})
#     else:
#         form = StudentsForm()
#         return render(request, 'myapp/create.html', {"form": form})

# class Student_update(generic.UpdateView):
#     model = Students
#     template_name = 'myapp/update.html'
#     fields = ('id', 'firstname', 'secondname', 'major', 'age', 'address')
#     success_url = '/'

#     def form_valid(self, form):
#         form.save()
#         return render(self.request, 'myapp/success.html', {"message": "학생정보를 수정했습니다."})

#     def get(self, request, *arg, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         context = self.get_context_data(object=self.object, form=form)
#         return self.render_to_response(context)

# class Student_delete(generic.DeleteView):
#     model = Students
#     template_name = 'myapp/delete.html'
#     success_url = '/'
#     context_object_name = 'student'

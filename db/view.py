from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pymysql
import json
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
MY_MSG={
   0 : 'where',
   1 : 'and'
}
MY_MSG2={
   0 : '',
   1 : ','
}
MY_MSG3={
   0 : '(',
   1 : ','
}

@csrf_exempt
def Major_add(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get("data")
         majorID = mydata['majorID']
         majorName = mydata['majorName']
         majorAddress = mydata['majorAddress']
         majorResp = mydata['majorResp']
         schoolID = mydata['schoolID']
         attributes = {
               'majorID' : majorID,
               'majorName' : majorName,
               'majorAddress' : majorAddress,
               'majorResp' : majorResp,
               'schoolID' : schoolID
         }
         flag = 0
         sql = "insert into Major(majorID,majorName,majorAddress,majorResp,schoolID) VALUES"
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}'{}'".format(sql,my_msg,value)
            else:
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}{}".format(sql,my_msg,"NULL")
         sql = sql + ')'
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def Major_delete(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         majorID = mydata['majorID']
         majorName = mydata['majorName']
         majorAddress = mydata['majorAddress']
         majorResp = mydata['majorResp']
         schoolID = mydata['schoolID']
         sql = "delete from Major"
         flag = 0
         attributes = {
            'majorID' : majorID,
            'majorName' : majorName,
            'majorAddress' : majorAddress,
            'majorResp' : majorResp,
            'schoolID' : schoolID
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")

         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def Major_change(request):
   try:
      with connection.cursor() as cursor:
         changed_field = json.loads(request.body).get('changed_field')
         newdata = json.loads(request.body).get('newdata')
         sql = "update Major set"
         flag = 0
         for key,value in newdata.items():
            if value != "":
               my_msg = MY_MSG2[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         flag = 0
         for key,value in changed_field.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def Major_search(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get("data")
         majorID = mydata['majorID']
         majorName = mydata['majorName']
         majorAddress = mydata['majorAddress']
         majorResp = mydata['majorResp']
         schoolID = mydata['schoolID']
         sql = "select * from Major"
         flag = 0
         attributes = {
            'majorID' : majorID,
            'majorName' : majorName,
            'majorAddress' : majorAddress,
            'majorResp' : majorResp,
            'schoolID' : schoolID
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
         datas = cursor.fetchall()
         count = 0
         return_data = []
         for data in datas:
            count = count + 1
            return_data.append(data)
      result = {
         'error' : 0,
         'msg' : sql,
         'data'  : return_data,
         'count' : count 
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")



@csrf_exempt
def Course_add(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         courseName = mydata['courseName']
         courseType = mydata['courseType']
         majorID = mydata['majorID']
         attributes = {
            'courseID' : courseID,
            'courseName' : courseName,
            'courseType' : courseType,
            'majorID' : majorID
            }
         flag = 0
         sql = "insert into Course(courseID,courseName,courseType,majorID) VALUES"
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}'{}'".format(sql,my_msg,value)
            else:
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}{}".format(sql,my_msg,"NULL")
         sql = sql + ')'
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def Course_delete(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         courseName = mydata['courseName']
         courseType = mydata['courseType']
         majorID = mydata['majorID']
         sql = "delete from Course"
         flag = 0
         attributes = {
            'courseID' : courseID,
            'courseName' : courseName,
            'courseType' : courseType,
            'majorID' : majorID
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")

         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def Course_change(request):
   try:
      with connection.cursor() as cursor:
         changed_field = json.loads(request.body).get('changed_field')
         newdata = json.loads(request.body).get('newdata')
         sql = "update Course set"
         flag = 0
         for key,value in newdata.items():
            if value != "":
               my_msg = MY_MSG2[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         flag = 0
         for key,value in changed_field.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def Course_search(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         courseName = mydata['courseName']
         courseType = mydata['courseType']
         majorID = mydata['majorID']
         sql = "select * from Course"
         flag = 0
         attributes = {
            'courseID' : courseID,
            'courseName' : courseName,
            'courseType' : courseType,
            'majorID' : majorID
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
         datas = cursor.fetchall()
         count = 0
         return_data = []
         for data in datas:
            count = count + 1
            return_data.append(data)
      result = {
         'error' : 0,
         'data'  : return_data,
         'count' : count 
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def CourseRecord_add(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         teacherID = mydata['teacherID']
         courseYear = mydata['courseYear']
         courseSem = mydata['courseSem']
         courseDay = mydata['courseDay']
         courseClass = mydata['courseClass']
         attributes = {
            'courseID' : courseID,
            'teacherID' : teacherID,
            'courseYear' : courseYear,
            'courseSem' : courseSem,
            'courseDay' : courseDay,
            'courseClass' : courseClass
            }
         flag = 0
         sql = "insert into CourseRecord(courseID,teacherID,courseYear,courseSem,courseDay,courseClass) VALUES"
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}'{}'".format(sql,my_msg,value)
            else:
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}{}".format(sql,my_msg,"NULL")
         sql = sql + ')'
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def CourseRecord_delete(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         teacherID = mydata['teacherID']
         courseYear = mydata['courseYear']
         courseSem = mydata['courseSem']
         courseDay = mydata['courseDay']
         courseClass = mydata['courseClass']
         sql = "delete from CourseRecord"
         flag = 0
         attributes = {
            'courseID' : courseID,
            'teacherID' : teacherID,
            'courseYear' : courseYear,
            'courseSem' : courseSem,
            'courseDay' : courseDay,
            'courseClass' : courseClass
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")

         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def CourseRecord_change(request):
   try:
      with connection.cursor() as cursor:
         changed_field = json.loads(request.body).get('changed_field')
         newdata = json.loads(request.body).get('newdata')
         sql = "update CourseRecord set"
         flag = 0
         for key,value in newdata.items():
            if value != "":
               my_msg = MY_MSG2[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         flag = 0
         for key,value in changed_field.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def CourseRecord_search(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         teacherID = mydata['teacherID']
         courseYear = mydata['courseYear']
         courseSem = mydata['courseSem']
         courseDay = mydata['courseDay']
         courseClass = mydata['courseClass']
         sql = "select * from CourseRecord"
         flag = 0
         attributes = {
            'courseID' : courseID,
            'teacherID' : teacherID,
            'courseYear' : courseYear,
            'courseSem' : courseSem,
            'courseDay' : courseDay,
            'courseClass' : courseClass
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
         datas = cursor.fetchall()
         count = 0
         return_data = []
         for data in datas:
            count = count + 1
            return_data.append(data)
      result = {
         'error' : 0,
         'data'  : return_data,
         'count' : count 
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def ScoreRecord_add(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         studentID = mydata['studentID']
         recordScore = mydata['recordScore']
         recordYear = mydata['recordYear']
         recordSem = mydata['recordSem']
         attributes = {
            'courseID' : courseID,
            'studentID' : studentID,
            'recordScore' : recordScore,
            'recordYear' : recordYear,
            'recordSem' : recordSem
            }
         flag = 0
         sql = "insert into ScoreRecord(courseID,studentID,recordScore,recordYear,recordSem) VALUES"
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}'{}'".format(sql,my_msg,value)
            else:
               my_msg = MY_MSG3[flag]
               flag = 1
               sql = "{}{}{}".format(sql,my_msg,"NULL")
         sql = sql + ')'
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def ScoreRecord_delete(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         studentID = mydata['studentID']
         recordScore = mydata['recordScore']
         recordYear = mydata['recordYear']
         recordSem = mydata['recordSem']
         sql = "delete from ScoreRecord"
         flag = 0
         attributes = {
            'courseID' : courseID,
            'studentID' : studentID,
            'recordScore' : recordScore,
            'recordYear' : recordYear,
            'recordSem' : recordSem
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")

         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def ScoreRecord_change(request):
   try:
      with connection.cursor() as cursor:
         changed_field = json.loads(request.body).get('changed_field')
         newdata = json.loads(request.body).get('newdata')
         sql = "update ScoreRecord set"
         flag = 0
         for key,value in newdata.items():
            if value != "":
               my_msg = MY_MSG2[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         flag = 0
         for key,value in changed_field.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
      connection.commit()
      result = {
         'error' : 0,
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def ScoreRecord_search(request):
   try:
      with connection.cursor() as cursor:
         mydata = json.loads(request.body).get('data')
         courseID = mydata['courseID']
         studentID = mydata['studentID']
         recordScore = mydata['recordScore']
         recordYear = mydata['recordYear']
         recordSem = mydata['recordSem']
         sql = "select * from ScoreRecord"
         flag = 0
         attributes = {
            'courseID' : courseID,
            'studentID' : studentID,
            'recordScore' : recordScore,
            'recordYear' : recordYear,
            'recordSem' : recordSem
            }
         for key,value in attributes.items():
            if value != "":
               my_msg = MY_MSG[flag]
               flag = 1
               sql = "{} {} {} = {}".format(sql,my_msg,key,"\'" + str(value) + "\'")
         cursor.execute(sql)
         datas = cursor.fetchall()
         count = 0
         return_data = []
         for data in datas:
            count = count + 1
            return_data.append(data)
      result = {
         'error' : 0,
         'data'  : return_data,
         'count' : count 
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")


@csrf_exempt
def Search_Course(request):
   try:
      with connection.cursor() as cursor:
         search_key = json.loads(request.body).get('msg_data')
         Course_attributes = [
            'courseID',
            'courseName',
            'courseType',
            'majorID'
         ]
         CourseRecord_attributes = [
            'courseID',
            'teacherID',
            'courseYear',
            'courseSem',
            'courseDay',
            'courseClass'
         ]
         search_tables = {
            'Course' : Course_attributes,
            'CourseRecord' : CourseRecord_attributes
         }
         return_data = []
         for key,value in search_tables.items():
            flag = 0
            sql = "select * from " + key
            for key1,value1 in search_key.items():
               if key1 in value:
                  my_msg = MY_MSG[flag]
                  flag = 1
                  sql = "{} {} {} = {}".format(sql,my_msg,key1,"\'" + value1 + "\'")
            if flag != 0:
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  data['table'] = key
                  return_data.append(data)
         k = len(return_data)        
         for i in range(k):
            data = return_data[i]
            sql = ""
            if data["table"] == "Course":
               sql = "select * from CourseRecord where courseID = {}".format(data['courseID'])
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  if data not in return_data:
                     return_data.append(data)
            elif data["table"] == "CourseRecord":
               sql = "select * from Course where courseID = {}".format(data['courseID'])
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  if data not in return_data:
                     return_data.append(data)
      count = len(return_data)
      result = {
         'type'  : 'Course',
         'error' : 0,
         'data'  : return_data,
         'count' : count
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[1]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

@csrf_exempt
def Search_Student(request):
   try:
      with connection.cursor() as cursor:
         search_key = json.loads(request.body).get('msg_data')
         Student_attributes = [
            'studentID',
            'studentDate',
            'studentEmail',
            'classID',
            'personID',
            'changeID'
         ]
         Person_attributes = [
            'personID',
            'personType',
            'personName',
            'personSex',
            'personBirth',
            'personCountry',
            'personAddress',
            'personPost',
            'personPhone'
         ]
         Class_attributes = [
            
         ]
         search_tables = {
            'Student' : Student_attributes,
            'Person' : Person_attributes,
            'Class'  : Class_attributes
         }
         
         return_data = []
         for key,value in search_tables.items():
            flag = 0
            sql = "select * from " + key
            for key1,value1 in search_key.items():
               if key1 in value:
                  my_msg = MY_MSG[flag]
                  flag = 1
                  sql = "{} {} {} = {}".format(sql,my_msg,key1,"\'" + value1 + "\'")
            if flag != 0:
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  if key == "Student":
                     data['studentDate'] = str(data['studentDate'])
                  if key == "Person":
                     data['personBirth'] = str(data['personBirth'])
                  data['table'] = key
                  return_data.append(data)
         k = len(return_data)        
         for i in range(k):
            data = return_data[i]
            sql = ""
            if data["table"] == "Student":
               sql = "select * from Person where personID = {}".format(data['personID'])
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  data['personBirth'] = str(data['personBirth'])
                  if data not in return_data:
                     return_data.append(data)
               sql = "select * from Class where classID = {}".format(data['classID'])
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  data['classDate'] = str(data['classDate'])
                  if data not in return_data:
                     return_data.append(data)
            elif data["table"] == "Person":
               sql = "select * from Student where personID = {}".format(data['personID'])
               cursor.execute(sql)
               datas = cursor.fetchall()
               for data in datas:
                  data["studentDate"] = str(data['studentDate'])
                  if data not in return_data:
                     return_data.append(data)
      count = len(return_data)
      result = {
         'type'  : 'Student',
         'error' : 0,
         'data'  : return_data,
         'count' : count 
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")
   except Exception as e:
      error = e.args[0]
      result = {
         'error' : 1,
         '错误信息'   : error
         }
      json_return = json.dumps(result,ensure_ascii=False)
      return HttpResponse(json_return,content_type="application/json,charset=utf-8")

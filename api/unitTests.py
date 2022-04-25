import subprocess #used to run curl commands




command = "curl -k https://131.104.49.113/" #base get request to server

#example url:http://127.0.0.1:5000/

#Test api/courses 
p1 = subprocess.run(command+ 'api/courses?is_ottawa=true&is_guelph=false',shell=True,capture_output=True,text=True) 
p1_expected = '{"code": 400 ,"message": "Bad Request"}'
if p1.stdout == p1_expected:
    print("Passed Test 1")
else:
    print("Failed Test 1")
    print(p1.stdout)

p1 = subprocess.run(command+ 'api/courses?is_ottawa=false&is_guelph=true&subject=ACCT&course_num=4220&course_name=Advanced Financial Accounting',shell=True,capture_output=True,text=True) #run curl to get output
p1_expected = '{"code": 400 ,"message": "Bad Request"}'
if p1.stdout == p1_expected:
    print("Passed Test 2")
else:
    print("Failed Test 2")
    print(p1.stdout)

p1 = subprocess.run(command+ 'api/courses?is_ottawa=true&is_guelph=false&subject=ACCT&course_num=4220&course_name=Advanced Financial Accounting',shell=True,capture_output=True,text=True) #run curl to get output
p1_expected = '{"code": 400 ,"message": "Bad Request"}'
if p1.stdout == p1_expected:
    print("Passed Test 3")
else:
    print("Failed Test 3")
    print(p1.stdout)



#Test api/guelphMajorSearch 
p1 = subprocess.run(command+ 'api/guelphMajorSearch?subject="ACCT"',shell=True,capture_output=True,text=True) #run curl to get output
p1_expected = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
'''
if p1.stdout == p1_expected:
    print("Passed Test 4")
else:
    print("Failed Test 4")
    print(p1.stdout)


#Test api/ottawaCourseSearch
p1 = subprocess.run(command+ 'api/ottawaCourseSearch?subject="ACCT"',shell=True,capture_output=True,text=True) #run curl to get output
p1_expected = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
'''
if p1.stdout == p1_expected:
    print("Passed Test 5")
else:
    print("Failed Test 5")
    print(p1.stdout)







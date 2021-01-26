from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Error, User, Match, Solution
from django.urls import reverse
from random import randint
from sendEmail.views import send

from django.contrib import messages

from django.contrib import auth

def search_title(request):
    errorTitle = request.POST['errorTitle']
    errors = Error.objects.all()
    search_error = errors.filter(title__contains= errorTitle)
    content = {'search_errors':search_error, "matchs": Match.objects.all(), "users": User.objects.all()}
    return render(request, 'error_manage_system/search_title.html', content)


def index(request):
    if 'user_id' in request.session.keys():
        if request.method=="POST":
            status_temp = request.POST.get('Filter')
            if status_temp == 'outstanding':
                status = False
                errors = Error.objects.filter(status=status)
            elif status_temp == 'resolved':
                status = True
                errors = Error.objects.filter(status=status)
            else:
                errors = Error.objects.all()
            content = {"errors": errors, "matchs": Match.objects.all(), "users": User.objects.all()}
            return render(request, 'error_manage_system/index.html', content)

        else:
            errors = Error.objects.all()
            content = {"errors": errors, "matchs": Match.objects.all(), "users": User.objects.all()}
            return render(request, 'error_manage_system/index.html', content)
    else:
        content = {"messages": ""}
        return redirect('main_signin', content)

# def myError(request):
#     return render(request, 'error_manage_system/my_error.html')

def myError(request):

    id_list = []
    for i in Match.objects.all():
        if i.user_id == request.session.get('user_id'):
            id_list.append(i.error_id)

    if 'user_id' in request.session.keys():
        if request.method=="POST":
            status_temp = request.POST.get('Filter')
            if status_temp == 'outstanding':
                status = False
                errors = Error.objects.filter(status=status)
            elif status_temp == 'resolved':
                status = True
                errors = Error.objects.filter(status=status)
            else:
                errors = Error.objects.all()
            content = {"errors": errors, "id_list": id_list, "user_my": User.objects.get(id=i.user_id)}
            return render(request, 'error_manage_system/my_error.html', content)

        else:
            errors = Error.objects.all()
            content = {"errors": errors, "id_list": id_list, "user_my": User.objects.get(id=i.user_id)}
            return render(request, 'error_manage_system/my_error.html', content)
    else:
        return redirect('main_signin')


def loggingError(request):
    return render(request, 'error_manage_system/logging_error.html')

def createError(request):
    errorTitle = request.POST['title']
    errorMessage = request.POST['message']
    errorCode = request.POST['code']
    errorDescription = request.POST['description']
    new_error = Error(title=errorTitle, message=errorMessage, code=errorCode, status=False, description=errorDescription)
    new_error.save()
    
    new_match = Match(user_id=request.session.get('user_id'), error_id=new_error.id)
    new_match.save()
    return HttpResponseRedirect(reverse("index"))
    # return render(request, 'error_manage_system/index.html')

def myDetailError(request, e_id):
    detail_error = Error.objects.get(id=e_id)
    if detail_error.status:
        detail_solution = Solution.objects.get(error_id=e_id)
        content = {"detail_error": detail_error, "detail_solution": detail_solution}
    else:
        content = {"detail_error": detail_error}
    return render(request, 'error_manage_system/my_detail_error.html', content)

def update_error(request, e_id):
    errorTitle = request.POST['title']
    errorID = request.POST['id']
    errorMessage = request.POST['message']
    errorCode = request.POST['code']
    errorDescription = request.POST['description']
    update_E = Error.objects.get(id=errorID)
    update_E.title = errorTitle
    update_E.message = errorMessage
    update_E.code = errorCode
    update_E.description = errorDescription
    update_E.save()

    
    solution_status = request.POST['solution_status']
    print(solution_status)
    if solution_status == "1":
        print(solution_status)
        update_S = Solution.objects.get(error_id=errorID)
        solutionCode = request.POST['sol_code']
        solutionDescription = request.POST['sol_description']
        
        update_S.solution_code = solutionCode
        update_S.solution_description = solutionDescription
        update_S.save()

    return HttpResponseRedirect(reverse("index"))

def detailError(request, e_id):
    detail_error = Error.objects.get(id=e_id)
    if detail_error.status:
        detail_solution = Solution.objects.get(error_id=e_id)
        content = {"detail_error": detail_error, "detail_solution": detail_solution}
    else:
        content = {"detail_error": detail_error}
    return render(request, 'error_manage_system/detail_error.html', content)

def logging_solution(request, e_id):
    match_error = Error.objects.get(id=e_id)
    content = {"match_error": match_error}
    return render(request, 'error_manage_system/logging_solution.html', content)

def createSolution(request, e_id):
    match = Match.objects.get(error_id=e_id)
    er_id = match.error_id
    us_id = match.user_id
    # solution 저장
    solutionCode = request.POST['solution_code']
    solutionDescription = request.POST['solution_description']
    new_solution = Solution(solution_code=solutionCode, solution_description=solutionDescription, error_id=er_id, user_id=us_id)
    new_solution.save()
    # error status True
    error_status_up = Error.objects.get(id=er_id)
    error_status_up.status = True
    error_status_up.save()
    return HttpResponseRedirect(reverse("index"))


def deleteError(request, e_id):
    delete_match = Match.objects.get(error_id=e_id)
    delete_error = Error.objects.get(id=e_id)
    delete_error.delete()
    delete_match.delete()
    return HttpResponseRedirect(reverse("my_error"))

def signup(request):
    return render(request, 'error_manage_system/signup_init.html')

def join(request):
    print(request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name=name, user_email=email, user_password=pw)
    user.save()
    code = randint(1000, 9999)
    response = redirect('main_verifyCode')
    response.set_cookie('code', code)
    response.set_cookie('user_id', user.id)
    # 이메일 발송 함수 호출
    send_result = send(email, code)
    if send_result:
        return response
    else:
        return HttpResponse("이메일 발송에 실패했습니다.")

# def login(request):
#     loginEmail = request.POST['loginEmail']
#     loginPW = request.POST['loginPW']
#     user = User.objects.get(user_email=loginEmail)
#     if user.user_password == loginPW:
#         request.session['user_id'] = user.id
#         request.session['user_name'] = user.user_name
#         request.session['user_email'] = user.user_email
#         return redirect('index')
#     else:
#         return redirect('main_login')

def login(request):
    loginEmail = request.POST.get('loginEmail', None)
    loginPW = request.POST.get('loginPW', None)
    try:
        user = User.objects.get(user_email=loginEmail)
    except:
        return redirect('main_signin')
    if user.user_password == loginPW:
        request.session['user_id'] = user.id
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('index')
    else:
        return redirect('main_signin')


# def login(request):
#     loginEmail = request.POST.get('loginEmail', None)
#     loginPW = request.POST.get('loginPW', None)
#     try:
#         user = User.objects.get(user_email=loginEmail)
#     except:
#         content = {"messages": "존재하지 않는 이메일 입니다."}
#         return redirect('main_signin', content)
#     if user.user_password == loginPW:
#         request.session['user_id'] = user.id
#         request.session['user_name'] = user.user_name
#         request.session['user_email'] = user.user_email
#         return redirect('index')
#     else:
#         content = {"messages": "비밀번호가 일치하지 않습니다."}
#         return redirect('main_signin', content)




def logout(request):
    request.session.clear()
    auth.logout(request)
    return redirect('main_signin')

# def logout(request):
#     # del request.session['user_name']
#     # del request.session['user_email']
#     request.session.clear()
#     auth.logout(request)
#     return redirect('main_signin')

def signin(request):
    return render(request, 'error_manage_system/signin_init.html')
    
def verifyCode(request):
    return render(request, 'error_manage_system/verifyCode_init.html')


def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id=request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user', user)
        request.session['user_name']=user.user_name
        request.session['user_email']=user.user_email
        return response
    else:
        redirect('main_varifyCode')
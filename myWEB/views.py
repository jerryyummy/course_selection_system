from django.shortcuts import render
from .models import Select, Student, Teacher, Class, ScoreTable, Teach, College
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse


def home(request):
    return render(request, 'home.html')


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect("/index")
            else:
                context["msg"] = "用户已被锁定，请联系管理员"
                return render(request, "home.html", context=context)
        else:
            context["msg"] = "用户名或密码错误"
            return render(request, "home.html", context=context)


def get_user_info(request):
    ret = {}
    result = Student.objects.filter(student_id=request.user.username)
    if result.exists():
        ret = {'student_id': result[0].student_id, 'name': result[0].name, 'gender': result[0].gender,
               'age': result[0].age, 'college_name': result[0].college_number.college_name}
        return 'student', ret
    result = Teacher.objects.filter(teacher_id=request.user.username)
    if result.exists():
        ret = {'teacher_id': result[0].teacher_id, 'name': result[0].name, 'position': result[0].position,
               'college_name': result[0].college_number.college_name}
        return 'teacher', ret
    return 'admin', ret


@login_required
def show_info(request):
    status, context = get_user_info(request)
    if status == 'student' or status == 'teacher':
        context['status'] = status
        return render(request, "info.html", context=context)
    return HttpResponseRedirect("/")


@login_required
def index(request):  # 首页
    status, context = get_user_info(request)
    if status == 'student' or status == 'teacher':
        context['status'] = status
        return render(request, "index.html", context=context)
    return HttpResponseRedirect("/")


@login_required
def logout_view(request):  # 安全退出
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def select_course(request):  # 学生选课
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    if request.method == 'GET':  # 首次访问
        result = Select.objects.filter(student_id=request.user.username)  # 获得课程查询结果
        classtable = []
        for course in result:
            try:
                classtable.append(
                    {
                        'class_id': course.class_id.class_id,
                        'teacher_name': Teach.objects.filter(class_id=course.class_id)[0].teacher_id.name,
                        'class_name': course.class_id.class_name,
                        'class_semester': course.class_id.class_semester,
                        'class_time': course.class_id.class_time,
                        'class_credit': course.class_id.class_credit
                    }
                )
            except:
                pass
        context['classtable'] = classtable
        return render(request, 'select_course.html', context=context)
    elif request.method == 'POST':  # 填表选课
        for i in range(0, 1):
            class_id = context['class_id'] = request.POST['class_id']
            teacher_id = context['teacher_id'] = request.POST['teacher_id']
            class_semester = '2020-2021春季学期'
            if len(class_id) and len(teacher_id):  # 输入了相关字段
                result = Class.objects.filter(class_id=class_id, class_semester=class_semester)
                if not result.exists():  # Class表中不存在这门课
                    context['result'] = '选课失败：不存在该课程'
                    continue
                flag = False
                for elem in Class.objects.filter(class_id=class_id, class_semester=class_semester):  # 查询是否已经选择相关课程
                    result = Select.objects.filter(
                        student_id=request.user.username,
                        class_id=elem.class_id
                    )
                    item = Teach.objects.filter(class_id=class_id)
                    if result.exists() or not item.exists():
                        flag = True
                        break
                if flag:
                    context['result'] = '选课失败：已选同类型课程或者没有老师教授该课程'
                    continue

                item = Select(
                    class_id=Class.objects.filter(class_semester=class_semester, class_id=class_id)[0],
                    student_id=Student.objects.filter(student_id=request.user.username)[0]
                )
                item.save()
                context['result'] = '选课成功'

            elif len(class_id) or len(teacher_id):
                context['result'] = '选课失败：课程号或工号未填写完整'

            result = Select.objects.filter(student_id=request.user.username)
            classtable = []
            for course in result:
                try:
                    classtable.append(
                        {
                            'class_id': course.class_id.class_id,
                            'teacher_name': Teach.objects.filter(class_id=course.class_id)[0].teacher_id.name,
                            'class_name': course.class_id.class_name,
                            'class_semester': course.class_id.class_semester,
                            'class_time': course.class_id.class_time,
                            'class_credit': course.class_id.class_credit
                        }
                    )
                except:
                    pass
            context['classtable'] = classtable
        return render(request, 'select_course.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def drop_course(request):  # 学生退课
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        result = Select.objects.filter(student_id=request.user.username)  # 获得课程查询结果
        classtable = []
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'teacher_name': Teach.objects.filter(class_id=course.class_id)[0].teacher_id.name,
                    'class_name': course.class_id.class_name,
                    'class_semester': course.class_id.class_semester,
                    'class_time': course.class_id.class_time,
                    'class_credit': course.class_id.class_credit
                }
            )
        context['classtable'] = classtable
        return render(request, 'drop_course.html', context=context)
    elif request.method == 'POST':
        class_id = request.POST['class_id']
        teacher_id = request.POST['teacher_id']
        class_semester = '2020-2021春季学期'
        result = Select.objects.filter(student_id=request.user.username)  # 获得课程查询结果
        classtable = []
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'teacher_name': Teach.objects.filter(class_id=course.class_id)[0].teacher_id.name,
                    'class_name': course.class_id.class_name,
                    'class_semester': course.class_id.class_semester,
                    'class_time': course.class_id.class_time,
                    'class_credit': course.class_id.class_credit
                }
            )
        context['classtable'] = classtable
        if len(class_id) and len(teacher_id):
            result = Select.objects.filter(class_id=class_id, student_id=request.user.username)
            item = Teach.objects.filter(class_id=class_id, teacher_id=teacher_id)
            if not result.exists():
                context['result'] = '退课失败：未选此门课程'
                return render(request, 'drop_course.html', context=context)
            elif not item.exists() or result[0].class_id != item[0].class_id:
                context['result'] = '退课失败，没有教师开设该课程'
            else:
                item = Select.objects.get(
                    class_id=Class.objects.filter(class_semester=class_semester, class_id=class_id)[0],
                    student_id=Student.objects.filter(student_id=request.user.username)[0]
                )
                item.delete()
                context['result'] = '退课成功'
        else:
            context['result'] = '退课失败：课程号或工号未填写完整'
            return render(request, 'drop_course.html', context=context)
        result = Select.objects.filter(class_id=class_id)
        classtable = []
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'teacher_name': Teach.objects.filter(class_id=course.class_id)[0].teacher_id.name,
                    'class_name': course.class_id.class_name,
                    'class_semester': course.class_id.class_semester,
                    'class_time': course.class_id.class_time,
                    'class_credit': course.class_id.class_credit
                }
            )
        context['classtable'] = classtable
        return render(request, 'drop_course.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def query_score(request):  # 学生成绩查询
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    result = ScoreTable.objects.filter(student_id_id=request.user.username, class_semester='2020-2021春季学期')
    print(result)
    classtable = []
    for course in result:
        classtable.append(
            {
                'class_id': course.class_id.class_id,
                'class_name': course.class_id.class_name,
                'final_score': course.final_score,
            }
        )
    context['classtable'] = classtable
    return render(request, 'query_score.html', context=context)


@login_required
def query_course(request):  # 学生课程查询
    status, context = get_user_info(request)
    if status != 'student':
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        return render(request, 'query_course.html', context=context)
    elif request.method == 'POST':
        result = Class.objects.all()
        context['class_semester'] = request.POST['class_semester']
        if context['class_semester']:
            result = result.filter(class_semester=context['class_semester'])
        context['class_id'] = request.POST['class_id']
        if context['class_id']:
            result = result.filter(class_id=context['class_id'])
        context['class_name'] = request.POST['class_name']
        if context['class_name']:
            result = result.filter(class_name=context['class_name'])
        context['teacher_id'] = request.POST['teacher_id']
        if context['teacher_id']:
            result = result.filter(teach__teacher_id__teacher_id__contains=context['teacher_id'])
        context['teacher_name'] = request.POST['teacher_name']
        if context['teacher_name']:
            result = result.filter(teach__teacher_id__name__contains=context['teacher_name'])

        classtable = []

        for course in result:
            if not Teacher.objects.filter(teach__class_id=course.class_id).exists():
                break
            classtable.append(
                {
                    'class_id': course.class_id,
                    'teacher_name': Teacher.objects.filter(teach__class_id=course.class_id)[0].name,
                    'class_name': course.class_name,
                    'class_semester': course.class_semester,
                    'class_time': course.class_time,
                    'class_credit': course.class_credit
                }
            )
        context['classtable'] = classtable
        return render(request, 'query_course.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def setup_course(request):  # 教师开课
    status, context = get_user_info(request)
    if status != 'teacher':
        return HttpResponseRedirect("/")
    result = Teach.objects.filter(teacher_id=request.user.username)
    classtable = []
    for course in result:
        classtable.append({
            'class_id': course.class_id.class_id,
            'class_name': course.class_id.class_name,
            'class_time': course.class_id.class_time,
            'class_credit': course.class_id.class_credit,
        })
    context['classtable'] = classtable
    if request.method == 'GET':
        return render(request, 'setup_course.html', context=context)
    elif request.method == 'POST':
        context['class_id'] = class_id = request.POST['class_id']
        context['class_name'] = class_name = request.POST['class_name']
        class_semester = '2020-2021春季学期'
        if len(class_id) and len(class_name):
            class_id_object = Class.objects.filter(class_semester=class_semester, class_id=class_id)
            class_name_object = Class.objects.filter(class_semester=class_semester, class_name=class_name)
            if class_id_object.exists() and class_name_object.exists():
                result = Teach.objects.filter(
                    class_id=class_id_object[0].class_id,
                    # teacher_id=request.user.username
                )
                if result.exists():
                    context['result'] = '开课失败：该课程已经开设'
                    return render(request, 'setup_course.html', context=context)
            if class_id_object.exists():
                if Class.objects.filter(class_semester=class_semester, class_id=class_id)[0].class_name != class_name:
                    context['result'] = '开课失败：输入课程名与课程号冲突'
                    return render(request, 'setup_course.html', context=context)
            item = Teach(
                class_id_id=class_id,
                teacher_id_id=Teacher.objects.filter(teacher_id=request.user.username)[0].teacher_id
            )
            item.save()
            context['result'] = '开课成功'
            result = Teach.objects.filter(class_id=class_id, teacher_id=request.user.username)
            classtable = []
            for course in result:
                classtable.append({
                    'class_id': course.class_id.class_id,
                    'class_name': course.class_id.class_name,
                    'class_time': course.class_id.class_time,
                    'class_credit': course.class_id.class_credit,
                })
            context['classtable'] = classtable
            return render(request, 'setup_course.html', context=context)
        elif len(class_id) or len(class_name):
            context['result'] = '开课失败：存在未填写字段'
            return render(request, 'setup_course.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def cancel_course(request):  # 教师取消开课
    status, context = get_user_info(request)
    if status != 'teacher':
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        result = Teach.objects.filter(teacher_id=request.user.username)
        classtable = []
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'class_name': course.class_id.class_name,
                    'class_time': course.class_id.class_time,
                    'class_credit': course.class_id.class_credit,
                    'number_of_people': len(Select.objects.filter(
                        class_id=course.class_id.class_id
                    ))
                }
            )
        context['classtable'] = classtable
        return render(request, 'cancel_course.html', context=context)
    elif request.method == 'POST':
        class_id = request.POST['class_id']
        if len(class_id):
            result = Teach.objects.filter(
                class_id=class_id,
                teacher_id=request.user.username
            )
            if not result.exists():
                context['result'] = '取消开课失败：不存在该课程'
            else:
                item = Teach.objects.get(class_id=class_id, teacher_id=request.user.username)
                item.delete()
                context['result'] = '取消开课成功'
        classtable = []
        result = Teach.objects.filter(class_id=class_id, teacher_id=request.user.username)
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'class_name': course.class_id.class_name,
                    'class_time': course.class_id.class_time,
                    'class_credit': course.class_id.class_credit,
                    'number_of_people': len(Select.objects.filter(
                        class_id=course.class_id.class_id
                    ))
                }
            )
        context['classtable'] = classtable
        return render(request, 'cancel_course.html', context=context)
    return HttpResponseRedirect("/")


@login_required
def publish_score(request):  # 教师发布成绩
    status, context = get_user_info(request)
    if status != 'teacher':
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        result = ScoreTable.objects.filter(class_semester='2020-2021春季学期',
                                           teacher_id_id=request.user.username)  # 获得本学期打的成绩表
        classtable = []
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'class_name': course.class_id.class_name,
                    'class_semester': course.class_semester,
                    'student_id': course.student_id.student_id,
                    'name': course.student_id.name,
                    'usual_score': course.usual_score,
                    'test_score': course.test_score,
                    'final_score': course.final_score,
                }
            )
        context['classtable'] = classtable
        return render(request, 'publish_score.html', context=context)
    elif request.method == 'POST':
        class_id = context['class_id'] = request.POST['class_id']
        student_id = context['student_id'] = request.POST['student_id']
        usual_score = request.POST['usual_score']
        test_score = request.POST['test_score']
        final_score = request.POST['final_score']
        class_semester = '2020-2021春季学期'
        if len(class_id) and len(student_id) and usual_score and test_score and final_score:
            result = Teach.objects.filter(
                teacher_id=request.user.username,
                class_id=class_id
            )
            item = Select.objects.filter(
                student_id=student_id,
                class_id=class_id
            )
            if result.exists() and item.exists() and result[0].class_id != item[0].class_id:
                context['result'] = '成绩发布失败：学生没有选该课程'

            if not result.exists():
                context['result'] = '成绩发布失败：错误的课程号'

            else:
                assert len(result) == 1
                result = ScoreTable.objects.filter(
                    student_id=student_id,
                    class_semester=class_semester,
                    class_id=class_id,
                    teacher_id=request.user.username
                )
                if not result.exists():
                    item = ScoreTable(
                        class_id_id=class_id,
                        class_semester=class_semester,
                        student_id_id=student_id,
                        teacher_id_id=request.user.username,
                        usual_score=usual_score,
                        test_score=test_score,
                        final_score=final_score
                    )
                    item.save()
                    context['result'] = '成绩发布成功'
                else:
                    result[0].update(usual_score=usual_score, test_score=test_score, final_score=final_score)
                    context['result'] = '成绩修改成功'
        elif len(class_id) and len(student_id) and usual_score and test_score and final_score:
            context['result'] = '成绩发布失败：表单未填写完整'
        result = ScoreTable.objects.filter(class_semester='2020-2021春季学期', teacher_id_id=request.user.username)
        classtable = []
        for course in result:
            classtable.append(
                {
                    'class_id': course.class_id.class_id,
                    'class_name': course.class_id.class_name,
                    'class_semester': course.class_semester,
                    'student_id': course.student_id.student_id,
                    'name': course.student_id.name,
                    'usual_score': course.usual_score,
                    'test_score': course.test_score,
                    'final_score': course.final_score,
                }
            )
        context['classtable'] = classtable
        return render(request, 'publish_score.html', context=context)
    return HttpResponseRedirect("/")

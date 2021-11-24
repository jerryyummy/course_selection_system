from django.db import models


# Create your models here.
class College(models.Model):  # 院系表
    college_number = models.CharField(max_length=10, primary_key=True)  # 院系号
    college_name = models.CharField(max_length=20, blank=False)  # 名称


class Student(models.Model):  # 学生表
    choice = (
        ('man','男'),
        ('woman','女')
    )
    student_id = models.CharField(max_length=20, primary_key=True)  # 学号
    name = models.CharField(max_length=10, blank=False)  # 姓名
    gender = models.CharField(max_length=10, choices=choice)
    age = models.IntegerField()
    college_number = models.ForeignKey(College, on_delete=models.CASCADE)


class Teacher(models.Model):  # 教师表
    teacher_id = models.CharField(max_length=20, primary_key=True)  # 工号
    name = models.CharField(max_length=10, blank=False)  # 姓名
    college_number = models.ForeignKey(College, on_delete=models.CASCADE)  # 院系号
    position = models.CharField(max_length=10)  # 职称


class Class(models.Model):  # 开课表
    class_semester = models.CharField(max_length=20, blank=False)  # 学期
    class_id = models.CharField(max_length=20, blank=False, primary_key=True)  # 课号
    class_name = models.CharField(max_length=20, blank=False)  # 课名
    class_time = models.TimeField(max_length=20, blank=False)  # 上课时间
    class_credit = models.IntegerField()


class Teach(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)


class Select(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)


class ScoreTable(models.Model):  # 成绩表
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)  # 学号
    class_semester = models.CharField(max_length=20, blank=False)  # 学期
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)  # 课号
    usual_score = models.FloatField(blank=True)  # 平时成绩
    test_score = models.FloatField(blank=True)  # 考试成绩
    final_score = models.FloatField(blank=True)  # 总评成绩
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

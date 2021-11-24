# wxk.shu.edu.cn
伪上海大学选课系统（数据库课程项目）

## 关于
框架：Python + Django + Mysql + Bootstrap
数据库命名沿用了学校教材的方式（即拼音首字母命名法）
第一次做Web开发，必然有诸多疏漏不妥之处，虚心求教

## TODO
- 实现学生选课和教师开课课时冲突的检测

## 主要页面介绍

### “/”
伪上海大学统一身份认证登录页面
- 学号/工号密码登录
- 使用session记住登录状态

<img src="/README/登录.png" />

### “/index/”
首页
- 根据登录账户信息展示学生或教师信息
- 学生提供选课、退课、成绩查询、课程查询功能
- 教师提供开设课程、取消开课、发布成绩功能

<img src="/README/首页.png" />

### “/index/xk/”
学生选课页面
- 根据课程号和工号快捷录入，支持一次录入最多四个
- 同页面跳转返回录入结果“信息未填写完整”、“不存在该课程”、“已选同类型课程”、“选课成功”
- 页面内提供学生已选课程（课程号、课程名称、工号、教师名称、上课时间）作为参考
- 不允许学生在同一学期重复选不同教师的重复课程（占课）

<img src="/README/学生选课.png" />

### “/index/tk/”
学生退课页面
- 根据课程号和工号进行退课
- 同页面跳转返回退课结果“信息未填写完整”、“未选此门课程”、“退课成功”
- 页面内提供学生已选课程（课程号、课程名称、工号、教师名称、上课时间）作为参考

<img src="/README/学生退课.png" />

### “/index/cjcx/”
学生成绩查询页面
- 返回本学期所选课程的成绩，如未发布则返回“尚未发布”

<img src="/README/学生成绩查询.png" />

### “/index/kccx/”
学生课程查询页面
- 根据学期（包含）、课程号（开始）、课程名称（包含）、工号（是）、教师名称（包含）、上课时间（包含），筛选相关课程
- 查询结果返回课程号、课程名称、工号、教师名称、上课时间、学期

<img src="/README/学生课程查询.png" />

### “/index/kskc/”
教师开设课程页面
- 根据课程号、课程名称、上课时间开设课程
- 同页面跳转返回开课结果“信息未填写完整”、“课程已经开设”、“课程号冲突”、“开课成功”
- 允许不同教师在同一学期开设相同课程号和相同课程名的不同课程
- 不允许教师开设相同课程号但课程名不同的课程（课程号冲突）
- 页面内提供教师已开课程（课程号、课程名称、上课时间）作为参考

<img src="/README/教师开课.png" />

### “/index/qxkk/”
教师取消开课页面
- 根据课程号取消开课
- 同页面跳转返回取消开课结果“不存在该课程”、“取消开课成功”
- 取消开课会级联删除已选该课程的学生相应的选课信息
- 页面内提供教师已开课程（课程号、课程名称、上课时间、选课人数）作为参考

<img src="/README/教师取消开课.png" />

### “/index/fbcj/”
教师发布成绩页面
- 根据课程号、学号、平时成绩、考试成绩、总评成绩发布成绩
- 同页面跳转返回成绩发布结果“信息未填写完整”、“错误的课程号或学号”、“成绩发布成功”、“成绩修改成功”
- 前端拦截填写错误的成绩信息（不在0-100内）
- 页面内提供教师已开课程的花名单（课程号、课程名称、上课时间、学号、姓名、平时成绩、考试成绩、总评成绩）作为参考

<img src="/README/教师发布成绩.png" /># course_selection_system

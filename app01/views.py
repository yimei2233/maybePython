from django.shortcuts import render, HttpResponse
import pymysql
import os

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
import pymysql
from app01.utiles import tools
from django.urls import reverse
import random
import json
import re


# Create your views here.

#
#  数据库连接
#
def mysql():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        db='blue',
        port=13306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


#
#  主页显示
#


def index(req):
    if not req.session.get('userInfo'):
        return redirect('/login/')

    conn = mysql()
    cursor = conn.cursor()

    sub_sql = ''
    category = ''
    category = req.GET.get('category')
    if category == '类型' or category == None:
        category = ''
    print(category)
    keywords = ''
    keywords = req.POST.get('keywords')
    if not keywords:
        keywords = req.GET.get('keywords', '')
    # 判断是否是搜索、分类
    if keywords and category:
        sub_sql = f'where name like "%{keywords}%" and category="{category}" '
    elif keywords:
        sub_sql = f'where name like "%{keywords}%"'
    elif category:
        sub_sql = f'where category="{category}" '

    page = int(req.GET.get('page', 1))
    page_size = 10  # 每页显示条数
    start = (page - 1) * page_size
    cursor.execute(f'''select *from games4399 {sub_sql} ''')
    res = cursor.fetchall()  # 总条数，连库获取
    total_count = len(res)
    if total_count == 0:
        total_count_new = 1
    else:
        total_count_new = total_count
    # 总种类
    ctg_sql = f'''where name like "%{keywords}%"'''
    sql = f'''SELECT category FROM games4399 {ctg_sql} GROUP BY category'''
    cursor.execute(sql)
    tp = cursor.fetchall()  # 所有游戏类型games.sort(key=lambda x: x['category'])
    tp.sort(key=lambda x: x['category'])
    sql = f'''select *from games4399 {sub_sql} limit {start},{page_size}'''
    cursor.execute(sql)
    res = cursor.fetchall()
    # 进行搜索替换
    if keywords:
        for index, item in enumerate(res):
            item['name'] = item['name'].replace(keywords,
                                                f'<span style="color:red; font-weight:bold;">{keywords}</span>')
            res[index] = item

    page_string = tools.handle_page(page, total_count_new, page_size, keywords=keywords, category=category)
    return render(req, 'table_complete.html',
                  {'res': res, 'lenth': total_count_new, 'page_string': page_string, 'keywords': keywords, 'tp': tp,
                   'category': category})


#
#  登录逻辑实现
#
def login(req):
    return render(req, 'login.html')


def handle_login(req):
    conn = mysql()
    cursor = conn.cursor()

    # 获取 POST 数据
    name = req.POST.get('name')
    password = req.POST.get('password')

    sql = '''select id,username,password from admin where username = %s and password = %s'''
    cursor.execute(sql, (name, password))
    conn.commit()
    result = cursor.fetchone()
    if not result:
        msg = '用户不存在！'
        url = '/login/'
        return redirect(f'/tips/?msg={msg}&url={url}', )

    id = result['id']
    if id:
        # 设置session
        # session的设置是基于请求对象
        req.session['userInfo'] = result
        # 获取：都是基于req对象
        # print('session值是', req.session.get('userInfo', '缺省值yyy'))
        # 10 min
        req.session.set_expiry(10*60)
        return redirect('/index/')
    else:
        return redirect('/login/')


def table_complete(req):
    return render(req, 'table_complete.html')


#
#  添加游戏
#

def add(req):
    conn = mysql()
    cursor = conn.cursor()
    sql = f'''SELECT category FROM games4399 GROUP BY category'''
    cursor.execute(sql)
    tp = cursor.fetchall()  # 所有游戏类型games.sort(key=lambda x: x['category'])
    tp.sort(key=lambda x: x['category'])
    return render(req, 'form_validate.html', {'tp': tp})


def handle_add(req):
    name = req.POST.get('name')
    category = req.POST.get('category')
    size = float(req.POST.get('size'))
    date = req.POST.get('date')
    introduce = req.POST.get('introduce')
    comment = req.POST.get('comment')
    hot = req.POST.get('hot')
    img = req.FILES.get('img')
    img_url = 'https://imga999.5054399.com/upload_pic/2011/9/14/' + img.name

    conn = mysql()
    cursor = conn.cursor()

    path = os.path.abspath('app01/static/game_img/' + img.name)
    for chunk in img.chunks():
        with open(path, 'wb') as f:
            f.write(chunk)

    sql = '''insert into games4399 values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(sql, (name, category, size, date, introduce, comment, hot, img_url, img.name))
    conn.commit()
    return redirect('/index/')


#
#  修改游戏信息
#
def revise(req):
    id = req.GET.get('id')
    conn = mysql()
    cursor = conn.cursor()
    cursor.execute(f'''select *from games4399 where id={id}''')
    res = cursor.fetchone()
    sql = f'''SELECT category FROM games4399 GROUP BY category'''
    cursor.execute(sql)
    tp = cursor.fetchall()  # 所有游戏类型games.sort(key=lambda x: x['category'])
    tp.sort(key=lambda x: x['category'])
    return render(req, 'revise.html', {'res': res, 'tp': tp})


def table(req):
    return render(req, 'table.html')


#
#  注册实现
#
def register(req):
    return render(req, 'register.html')


def handle_register(req):
    conn = mysql()
    cursor = conn.cursor()

    username = req.POST.get('username')
    pwd = req.POST.get('password')
    pwd2 = req.POST.get('password2')
    url = '/register/'

    if pwd == pwd2:
        sql = '''select id from admin where username = %s'''
        cursor.execute(sql, (username,))
        conn.commit()
        id = cursor.fetchone()
        if not id:
            sql = '''insert into admin values(NULL,%s,%s,now(),now())'''
            cursor.execute(sql, (username, pwd,))
            conn.commit()
            msg = '添加成功！'
            return redirect(f'/tips/?msg={msg}&url={url}')
        else:
            msg = '该用户以存在！'
            return redirect(f'/tips/?msg={msg}&url={url}')
    msg = '密码不一致！'
    return redirect(f'/tips/?msg={msg}&url={url}')


#
#  修改管理员密码信息
#

def reinfo(req):
    result = req.session.get('userInfo', 'xxx')
    username = result['username']

    return render(req, 'reinfo.html', {'username': username})


def handle_reinfo(req):
    conn = mysql()
    cursor = conn.cursor()
    result = req.session.get('userInfo', 'xxx')
    id = result['id']
    mpass = req.POST.get('mpass')
    newpass = req.POST.get('newpass')
    renewpass = req.POST.get('renewpass')
    url = f'/reinfo/'
    if newpass != renewpass:
        msg = '两次密码不一致！'
        return redirect(f'/tips/?msg={msg}&url={url}')
    sql = '''select * from admin where id = %s and password = %s'''
    cursor.execute(sql, (id, mpass))
    ans = cursor.fetchone()
    if ans:
        sql = 'update admin set password = %s where id = %s'
        cursor.execute(sql, (newpass, id))
        conn.commit()
        msg = '修改成功'
        return redirect(f'/tips/?msg={msg}&url={url}')
    else:
        msg = '原密码不正确'
    return redirect(f'/tips/?msg={msg}&url={url}')


#
#  输入密码错误的提示（修改密码时）
#
def tips(req):
    msg = req.GET.get('msg')
    url = req.GET.get('url')
    return render(req, 'tips.html', {'msg': msg, 'url': url})


#
#  删除与批量删除
#
def handle_delete(req):
    id = req.GET.get('id')

    conn = mysql()
    cursor = conn.cursor()
    cursor.execute(f'''select img_name from games4399 where id = {id}''')
    img_name = cursor.fetchone()['img_name']
    print(img_name)
    cursor.execute(f'''delete from games4399 where id ={id}''')
    conn.commit()
    path = os.path.abspath('app01/static/game_img/' + img_name)
    os.remove(path)
    return redirect('/index/')


def handle_deletes(req):
    id_list = req.POST.getlist('id')
    print(id_list)
    conn = mysql()
    cursor = conn.cursor()
    for id in id_list:
        cursor.execute(f'''select img_name from games4399 where id = {id}''')
        img_name = cursor.fetchone()['img_name']
        print(img_name)
        cursor.execute(f'''delete from games4399 where id ={id}''')
        conn.commit()
        path = os.path.abspath('app01/static/game_img/' + img_name)
        os.remove(path)
    return redirect('/index/')


#
#  修改游戏数据信息
#

def handle_revise(req):
    id = req.POST.get('id')
    name = req.POST.get('name')
    category = req.POST.get('category')
    size = float(req.POST.get('size'))
    date = req.POST.get('date')
    introduce = req.POST.get('introduce')
    comment = req.POST.get('comment')
    hot = req.POST.get('hot')
    img = req.FILES.get('img')
    img_name = req.POST.get('img_name')
    if img:
        img_path = os.path.abspath('app01/static/game_img/' + img_name)
        os.remove(img_path)  # 删除旧图片
        img_new_path = os.path.abspath('app01/static/game_img/' + img.name)
        for chunk in img.chunks():
            with open(img_new_path, 'wb') as f:
                f.write(chunk)  # 存入新图片
        img_name = img.name
    img_url = 'https://imga999.5054399.com/upload_pic/2011/9/14/' + img_name

    conn = mysql()
    cursor = conn.cursor()

    sql = '''update games4399 set name=%s,category=%s,size=%s,date=%s,introduce=%s,comment=%s,hot=%s,img_name=%s ,img_url=%s where id =%s'''
    cursor.execute(sql, (name, category, size, date, introduce, comment, hot, img_name, img_url, id))
    conn.commit()

    return redirect('/index/')


###
###
###
# 前端可视化
def echart(req):
    return render(req, 'echart.html')


def handle_one(req):
    conn = mysql()
    cursor = conn.cursor()
    dt = {}
    sql = '''select category,count(*) from games4399 group by category'''
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    category = []
    count = []
    for item in data:
        category.append(item['category'])
        count.append(item['count(*)'])
    dt['category'] = category
    dt['count'] = count
    return JsonResponse(dt)


def handle_two(req):
    dt = {}
    conn = mysql()
    cursor = conn.cursor()
    sql = '''select category , avg(hot) from games4399 group by category'''
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in range(len(data)):
        a = data[i]['category']
        b = data[i]['avg(hot)']
        data[i].clear()
        data[i]['name'] = a
        data[i]['value'] = b
    dt['data'] = data
    return JsonResponse(dt)


def handle_three(req):
    dt = {}
    conn = mysql()
    cursor = conn.cursor()
    sql = '''select category , avg(comment) from games4399 group by category'''
    cursor.execute(sql)
    data = cursor.fetchall()
    category = []
    avg = []
    for item in data:
        category.append(item['category'])
        avg.append(item['avg(comment)'])
    dt['category'] = category
    dt['avg'] = avg

    return JsonResponse(dt)


def handle_four(req):
    dt = {}
    conn = mysql()
    cursor = conn.cursor()
    sql = '''select hot,comment from games4399'''
    cursor.execute(sql)
    data = cursor.fetchall()
    a = []
    b = []
    for item in data:
        a.append(item['hot'])
        a.append(item['comment'])
        b.append(a)
        a = []
    dt['data'] = b
    return JsonResponse(dt)


def handle_five(req):
    dt = {}
    conn = mysql()
    cursor = conn.cursor()
    sql = '''select category,avg(size),avg(hot),avg(comment) from games4399 group by category'''
    cursor.execute(sql)
    data = cursor.fetchall()
    ls = []
    for item in data:
        ls.append(item['avg(size)'])
        ls.append(item['avg(hot)'])
        ls.append(item['avg(comment)'])
        dt[item['category']] = ls
        ls = []
    print(dt)
    return JsonResponse(dt)

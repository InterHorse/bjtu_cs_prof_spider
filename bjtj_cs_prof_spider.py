#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
Created on 2020-02-23

@author: Ma Yuzhe
"""

import requests
from bs4 import BeautifulSoup
import MySQLdb

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
}

# 导师类
class Professor(object):
    def __init__(self, name, url):
        # 姓名
        self.name = name
        # 网址
        self.url = url

# 获取网页内容
def getHTMLText(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "爬取失败"

# 连接数据库
def connectMysql():
    global db
    db = MySQLdb.connect("localhost", "root", "123456", "bjtu_professors", charset='utf8')

# 插入导师信息
def insertProfessor(professor):
    name = professor.name
    title = professor.title
    url = professor.url
    imgUrl = professor.img
    base = professor.base
    eduBg = professor.eduBg
    workExp = professor.workExp
    resOri = professor.resOri
    resumeMajor = professor.resumeMajor
    sciResPro = professor.sciResPro
    teachWork = professor.teachWork
    paper = professor.paper
    treatise = professor.treatise
    patent = professor.patent
    softwarePatent = professor.softwarePatent
    honor = professor.honor
    partTimeJob = professor.partTimeJob

    cursor = db.cursor()

    sql = "INSERT INTO professors(name, title, url, img_url, base, edu_bg, work_exp, research_orientation, resume_major, \
       scientific_research_project, teach_work, paper, treatise, patent, software_patent, honor, part_time_job) \
       VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          (MySQLdb.escape_string(name).decode('utf-8'), MySQLdb.escape_string(title).decode('utf-8'),
           MySQLdb.escape_string(url).decode('utf-8'),
           MySQLdb.escape_string(imgUrl).decode('utf-8'),
           MySQLdb.escape_string(base).decode('utf-8'), MySQLdb.escape_string(eduBg).decode('utf-8'),
           MySQLdb.escape_string(workExp).decode('utf-8'),
           MySQLdb.escape_string(resOri).decode('utf-8'), MySQLdb.escape_string(resumeMajor).decode('utf-8'),
           MySQLdb.escape_string(sciResPro).decode('utf-8'),
           MySQLdb.escape_string(teachWork).decode('utf-8'), MySQLdb.escape_string(paper).decode('utf-8'),
           MySQLdb.escape_string(treatise).decode('utf-8'),
           MySQLdb.escape_string(patent).decode('utf-8'), MySQLdb.escape_string(softwarePatent).decode('utf-8'),
           MySQLdb.escape_string(honor).decode('utf-8'),
           MySQLdb.escape_string(partTimeJob).decode('utf-8'))

    print(sql)
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    print()

# 解析目录页，获得每个导师的详情页地址
def parseProfessorsList(professorList, html):
    # 域名
    url = 'http://faculty.bjtu.edu.cn'
    # 创建 soup
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('div', attrs={'class': 'row'})
    # 第二个 row 导师信息块，根据 class="teacher_card" 解析
    i = rows[1].find_all('div', attrs={'class': 'teacher_card'})
    # 遍历
    for professors in i:
        # 找到 a 标签
        a = professors.find("a")
        # 拼接导师详情地址
        pro = Professor(a.text.strip(), url + a.get('href'))
        professorList.append(pro)

# 解析导师详情页
def parseProfessorsDetail(professor):
    professor.base = ''
    professor.eduBg = ''
    professor.workExp = ''
    professor.resOri = ''
    professor.resumeMajor = ''
    professor.sciResPro = ''
    professor.teachWork = ''
    professor.paper = ''
    professor.treatise = ''
    professor.patent = ''
    professor.softwarePatent = ''
    professor.honor = ''
    professor.partTimeJob = ''

    html = getHTMLText(professor.url, headers)
    soup = BeautifulSoup(html, 'html.parser')
    wrap = soup.find(id="wrap")

    # 头像
    img = wrap.find("img")
    professor.img = img.get('src') + ""

    # title
    title = wrap.find(class_='border_p')
    professor.title = title.text.strip() + ""

    details = wrap.find_all(class_='mainleft_box')
    for detail in details:
        column = detail.find(class_='h4border').text.strip()
        [s.extract() for s in detail(class_='h4border')]
        contentOri = detail.text.strip()
        content = ''
        for line in contentOri.splitlines():
            if line == '':
                continue
            line = line.strip() + '\n'
            content = content + line
        content = content.rstrip('\n') + ""

        if column == '基本信息':
            professor.base = content
        elif column == '教育背景':
            professor.eduBg = content
        elif column == '工作经历':
            professor.workExp = content
        elif column == '研究方向':
            professor.resOri = content
        elif column == '招生专业':
            professor.resumeMajor = content
        elif column == '科研项目':
            professor.sciResPro = content
        elif column == '教学工作':
            professor.teachWork = content
        elif column == '论文/期刊':
            professor.paper = content
        elif column == '专著/译著':
            professor.treatise = content
        elif column == '专利':
            professor.patent = content
        elif column == '软件著作权':
            professor.softwarePatent = content
        elif column == '获奖与荣誉':
            professor.honor = content
        elif column == '社会兼职':
            professor.partTimeJob = content
        print(content)
    insertProfessor(professor)


def main():
    # 存放每个导师详情页地址
    professorList = []
    # 遍历 7 页导师目录页
    for i in range(1, 7):
        url = 'http://faculty.bjtu.edu.cn/cs/sdxx.html?page=' + str(i)
        print("正在爬取第 '%s' 页导师：" % (i))
        print(url + '\n')
        # 获取网页内容
        html = getHTMLText(url, headers)
        parseProfessorsList(professorList, html)
    print("爬取链接完成")
    connectMysql()
    for professor in professorList:
        parseProfessorsDetail(professor)
    db.close()

if __name__ == '__main__':
    main()

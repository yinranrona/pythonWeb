
from django.shortcuts import render, HttpResponse, redirect
from wbsapp.models.indexModel import Project, LabelManage, Label1st, Label2nd, Label3rd, Label4th, Person, Comment
from django.template import Context, Template
from wbsapp.form import CommentForm
from django.core import serializers
from django.db.models import F
import json
from datetime import date, datetime
import pprint

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.timestamp()
    raise TypeError (f'Type {obj} not serializable')

# Create your views here.
# 全てのラベル
def getAllLabels():
    pj_lst = list(Project.objects.all().values('taskID').distinct())
    labelTaskLstAll = []
    for pj in pj_lst:
        pj['children'] = []
        labelTaskLst = []
        labelTaskLst.append(pj)
        label_lst = list(LabelManage.objects.filter(taskID=pj['taskID']).values('labelID', 'labelName'))
        label1_lst = list(Label1st.objects.filter(taskID=pj['taskID']).values('labelID', 'labelName'))
        label2_lst = list(Label2nd.objects.filter(taskID=pj['taskID']).values('labelID', 'labelName'))
        label3_lst = list(Label3rd.objects.filter(taskID=pj['taskID']).values('labelID', 'labelName'))
        label4_lst = list(Label4th.objects.filter(taskID=pj['taskID']).values('labelID', 'labelName'))
        label_lst.extend(label1_lst)
        label_lst.extend(label2_lst)
        label_lst.extend(label3_lst)
        label_lst.extend(label4_lst)
        # label_lst = [pj, *label_lst]
        # labelTaskLst.append(label_lst)
        # labelTaskLstAll.extend(labelTaskLst)
        # print(label_lst)
        # print(labelTaskLst[0]['children'])
        labelTaskLst[0]['children'] = label_lst
        labelTaskLstAll.append(labelTaskLst)
    return labelTaskLstAll

# タスクIDに関するラベル
def getAllLabelsByTaskID(taskID):
    allLabels = getAllLabels()
    for label in allLabels:
        for inner_label in label:
            if inner_label['taskID'] == taskID:
                return inner_label['children']
    return

def project(request):
    # print(request.session['userid'])
    try:
        request.session['userid']
    except:
        return redirect(to='login')

    # queryset = request.GET.get('labelID')
    # if queryset:
    #     project_list = Project.objects.filter(labelID=queryset)
    # else:
    #     project_list = Project.objects.all()
    project_list = Project.objects.all()
    project_list_all = list(Project.objects.all().values('taskID', 'taskName').distinct())

    actualTimeTaskID = request.POST.get('actualTimeTaskID')
    if actualTimeTaskID:
        p = Project.objects.get(taskID=actualTimeTaskID)

        actualTimeFlag = request.POST.get('actualTimeFlag')
        if actualTimeFlag == 'actualStartTimeStamping':
            p.actualStartTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if actualTimeFlag == 'actualFinishTimeStamping':
            p.actualFinishTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        p.dtupdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.save()

    context = {}
#    project_list = Project.objects.all()
    userInfo = Person.objects.get(personID=request.session['userid'])

    # def json_serial(obj):
    #     if isinstance(obj, (datetime, date)):
    #         return obj.isoformat()
    #     raise TypeError (f'Type {obj} not serializable')

    person_list = Person.objects.all()
    # labelManage_list = LabelManage.objects.all()
    # 全てのラベルの取得
    labelMan_list = list(LabelManage.objects.all().values('labelID', 'labelName').distinct())
    label1_list = list(Label1st.objects.all().values('labelID', 'labelName').distinct())
    label2_list = list(Label2nd.objects.all().values('labelID', 'labelName').distinct())
    label3_list = list(Label3rd.objects.all().values('labelID', 'labelName').distinct())
    label4_list = list(Label4th.objects.all().values('labelID', 'labelName').distinct())
    labelMan_list.extend(label1_list)
    labelMan_list.extend(label2_list)
    labelMan_list.extend(label3_list)
    labelMan_list.extend(label4_list)

    labelManage_list_all = []
    labelManage_list = list(LabelManage.objects.all().values('labelID', 'labelName').distinct())
    for labelManage in labelManage_list:
        # print(labelManage)
        labelManage_1st_list = list(LabelManage.objects.filter(labelID=labelManage['labelID']).values(id=F('labelChildID__labelID'), name=F('labelChildID__labelName')).distinct())
        labelManage_1st_taskInfo_list = list(LabelManage.objects.filter(labelID=labelManage['labelID']).values(key=F('taskID__taskID')
        , contentName=F('taskID__taskName')
        , personID=F('taskID__personID')
        , personName=F('taskID__personID__personName')
        , personImage=F('taskID__personID__personImage')
        , planStartTime=F('taskID__planStartTime')
        , planFinishTime=F('taskID__planFinishTime')
        , actualStartTime=F('taskID__actualStartTime')
        , actualFinishTime=F('taskID__actualFinishTime')).distinct())
        for label in labelManage_1st_taskInfo_list:
            label['labelGroup'] = getAllLabelsByTaskID(label['key'])
        # print(labelManage_1st_taskInfo_list)
        # print('--------------')
        if labelManage_1st_list[0]['id'] is None and labelManage_1st_taskInfo_list[0]['key'] is None:
            continue
        if labelManage_1st_list[0]['id'] is None and labelManage_1st_taskInfo_list[0]['key'] is not None:
            labelManage_1st_list = labelManage_1st_taskInfo_list
        if labelManage_1st_list[0]['id'] is not None and labelManage_1st_taskInfo_list[0]['key'] is not None:
            labelManage_1st_list.extend(labelManage_1st_taskInfo_list)
        labelManage['key'] = labelManage['labelID']
        del labelManage['labelID']
        labelManage['contentName'] = labelManage['labelName']
        del labelManage['labelName']
        # print(labelManage_1st_list)
        # [{'id': 4, 'name': '課題解決'}, {'id': 5, 'name': 'ddsss'}]
        labelManage1stList = []
        for labelManage1st in labelManage_1st_list:
            # print(labelManage1st)
            # {'id': 4, 'name': '課題解決'}
            # {'id': 5, 'name': 'ddsss'}
            if labelManage1st.get('id') is not None:
                labelManage_2nd_list = list(Label1st.objects.filter(labelID=labelManage1st['id']).values(id=F('labelChildID__labelID'), name=F('labelChildID__labelName')).distinct())
                labelManage_2nd_taskInfo_list = list(Label1st.objects.filter(labelID=labelManage1st['id']).values(key=F('taskID__taskID')
                , contentName=F('taskID__taskName')
                , personID=F('taskID__personID')
                , personName=F('taskID__personID__personName')
                , personImage=F('taskID__personID__personImage')
                , planStartTime=F('taskID__planStartTime')
                , planFinishTime=F('taskID__planFinishTime')
                , actualStartTime=F('taskID__actualStartTime')
                , actualFinishTime=F('taskID__actualFinishTime')).distinct())
                for label in labelManage_2nd_taskInfo_list:
                    label['labelGroup'] = getAllLabelsByTaskID(label['key'])
                # print(labelManage_2nd_list)
                # print(labelManage_2nd_taskInfo_list)
                if labelManage_2nd_list[0]['id'] is None and labelManage_2nd_taskInfo_list[0]['key'] is None:
                    continue
                if labelManage_2nd_list[0]['id'] is None and labelManage_2nd_taskInfo_list[0]['key'] is not None:
                    labelManage_2nd_list = labelManage_2nd_taskInfo_list
                if labelManage_2nd_list[0]['id'] is not None and labelManage_2nd_taskInfo_list[0]['key'] is not None:
                    labelManage_2nd_list.extend(labelManage_2nd_taskInfo_list)
                labelManage1st['key'] = labelManage1st['id']
                del labelManage1st['id']
                labelManage1st['contentName'] = labelManage1st['name']
                del labelManage1st['name']

            # [{'id': 56, 'name': 'バッチ修正'}, {'id': 99, 'name': '重要課題'}]
            # [{'id': None, 'name': None}]
            # labelManage_2nd_taskInfo_list = list(Label1st.objects.filter(labelID=labelManage1st['id']).values(id=F('taskID__taskID'), name=F('taskID__taskName')).distinct())
            # print(labelManage_2nd_list)
                labelManage2ndList = []
                for labelManage2nd in labelManage_2nd_list:
                    # print(labelManage2nd)
                    # if labelManage2nd['id'] is None:
                        # break
                    if labelManage2nd.get('id') is not None:
                        labelManage_3rd_list = list(Label2nd.objects.filter(labelID=labelManage2nd['id']).values(id=F('labelChildID__labelID'), name=F('labelChildID__labelName')).distinct())
                        labelManage_3rd_taskInfo_list = list(Label2nd.objects.filter(labelID=labelManage2nd['id']).values(key=F('taskID__taskID')
                        , contentName=F('taskID__taskName')
                        , personID=F('taskID__personID')
                        , personName=F('taskID__personID__personName')
                        , personImage=F('taskID__personID__personImage')
                        , planStartTime=F('taskID__planStartTime')
                        , planFinishTime=F('taskID__planFinishTime')
                        , actualStartTime=F('taskID__actualStartTime')
                        , actualFinishTime=F('taskID__actualFinishTime')).distinct())
                        for label in labelManage_3rd_taskInfo_list:
                            label['labelGroup'] = getAllLabelsByTaskID(label['key'])
                        # print(labelManage_3rd_list)
                        # print(labelManage_3rd_taskInfo_list)
                        if labelManage_3rd_list[0]['id'] is None and labelManage_3rd_taskInfo_list[0]['key'] is None:
                            continue
                        if labelManage_3rd_list[0]['id'] is None and labelManage_3rd_taskInfo_list[0]['key'] is not None:
                            labelManage_3rd_list = labelManage_3rd_taskInfo_list
                        if labelManage_3rd_list[0]['id'] is not None and labelManage_3rd_taskInfo_list[0]['key'] is not None:
                            labelManage_3rd_list.extend(labelManage_3rd_taskInfo_list)
                        labelManage2nd['key'] = labelManage2nd['id']
                        del labelManage2nd['id']
                        labelManage2nd['contentName'] = labelManage2nd['name']
                        del labelManage2nd['name']

                        labelManage3rdList = []
                        for labelManage3rd in labelManage_3rd_list:
                            if labelManage3rd.get('id') is not None:
                                labelManage_4th_list = list(Label3rd.objects.filter(labelID=labelManage3rd['id']).values(id=F('labelChildID__labelID'), name=F('labelChildID__labelName')).distinct())
                                labelManage_4th_taskInfo_list = list(Label3rd.objects.filter(labelID=labelManage3rd['id']).values(key=F('taskID__taskID')
                                , contentName=F('taskID__taskName')
                                , personID=F('taskID__personID')
                                , personName=F('taskID__personID__personName')
                                , personImage=F('taskID__personID__personImage')
                                , planStartTime=F('taskID__planStartTime')
                                , planFinishTime=F('taskID__planFinishTime')
                                , actualStartTime=F('taskID__actualStartTime')
                                , actualFinishTime=F('taskID__actualFinishTime')).distinct())
                                for label in labelManage_4th_taskInfo_list:
                                    label['labelGroup'] = getAllLabelsByTaskID(label['key'])
                                if labelManage_4th_list[0]['id'] is None and labelManage_4th_taskInfo_list[0]['key'] is None:
                                    continue
                                if labelManage_4th_list[0]['id'] is None and labelManage_4th_taskInfo_list[0]['key'] is not None:
                                    labelManage_4th_list = labelManage_4th_taskInfo_list
                                if labelManage_4th_list[0]['id'] is not None and labelManage_4th_taskInfo_list[0]['key'] is not None:
                                    labelManage_4th_list.extend(labelManage_4th_taskInfo_list)
                                labelManage3rd['key'] = labelManage3rd['id']
                                del labelManage3rd['id']
                                labelManage3rd['contentName'] = labelManage3rd['name']
                                del labelManage3rd['name']

                                labelManage4thList = []
                                for labelManage4th in labelManage_4th_list:
                                    # print(labelManage4th)
                                    if labelManage4th.get('id') is not None:
                                        labelManage_5th_list = list(Label4th.objects.filter(labelID=labelManage4th['id']).values(key=F('taskID__taskID')
                                        , contentName=F('taskID__taskName')
                                        , personID=F('taskID__personID')
                                        , personName=F('taskID__personID__personName')
                                        , personImage=F('taskID__personID__personImage')
                                        , planStartTime=F('taskID__planStartTime')
                                        , planFinishTime=F('taskID__planFinishTime')
                                        , actualStartTime=F('taskID__actualStartTime')
                                        , actualFinishTime=F('taskID__actualFinishTime')).distinct())
                                        for label in labelManage_5th_list:
                                            label['labelGroup'] = getAllLabelsByTaskID(label['key'])
                                        labelManage4th['key'] = labelManage4th['id']
                                        del labelManage4th['id']
                                        labelManage4th['contentName'] = labelManage4th['name']
                                        del labelManage4th['name']

                                        labelManage5thList = []
                                        for labelManage5th in labelManage_5th_list:
                                            labelManage5thList.append(labelManage5th)
                                        # print(labelManage5th)
                                        labelManage4th['children'] = labelManage5thList
                                    labelManage4thList.append(labelManage4th)

                                labelManage3rd['children'] = labelManage4thList
                            labelManage3rdList.append(labelManage3rd)

                        labelManage2nd['children'] = labelManage3rdList
                    labelManage2ndList.append(labelManage2nd)

                labelManage1st['children'] = labelManage2ndList
            labelManage1stList.append(labelManage1st)
            # print(labelManage1st)
        # print(labelManage1stList)
        labelManage['children'] = labelManage1stList
        labelManage_list_all.append(labelManage)
    # pprint.pprint(labelManage_list_all)
    # print(json.dumps(labelManage_list_all))
    context['labelManage_list_all'] = json.dumps(labelManage_list_all, default=json_serial)
    # labelManage_list_all.append(labelManage_list)
    # print(labelManage_list_all)

    # time_list = TimeManage.objects.all()
    context['project_list'] = project_list
    context['project_list_all'] = json.dumps(project_list_all, default=json_serial)
    context['person_list'] = person_list
    context['labelManage_list'] = labelMan_list
    # print(labelMan_list)
    # context['labelTaskLstAll'] = labelTaskLstAll
    context['userImage'] = userInfo.personImage
    # context['time_list'] = time_list
    # context['form_time'] = form_time
    index_page = render(request, 'index.html', context)
    return index_page

#タスク削除
def project_delete(request, task_id):
    p = Project.objects.get(taskID=task_id)
    p.delete()
    labelManage = list(LabelManage.objects.all().values('taskID').distinct())
    for label in labelManage:
        if task_id == label['taskID']:
            p = Project.objects.get(taskID=taskID)
            l = LabelManage.objects.get(taskID=task_id)
            l.taskID.remove(p)
    label1st = list(Label1st.objects.all().values('taskID').distinct())
    for label in label1st:
        if task_id == label['taskID']:
            p = Project.objects.get(taskID=taskID)
            l = Label1st.objects.get(taskID=task_id)
            l.taskID.remove(p)
    label2nd = list(Label2nd.objects.all().values('taskID').distinct())
    for label in label2nd:
        if task_id == label['taskID']:
            p = Project.objects.get(taskID=taskID)
            l = Label2nd.objects.get(taskID=task_id)
            l.taskID.remove(p)
    label3rd = list(Label3rd.objects.all().values('taskID').distinct())
    for label in label3rd:
        if task_id == label['taskID']:
            p = Project.objects.get(taskID=taskID)
            l = Label3rd.objects.get(taskID=task_id)
            l.taskID.remove(p)
    label4th = list(Label4th.objects.all().values('taskID').distinct())
    for label in label4th:
        if task_id == label['taskID']:
            p = Project.objects.get(taskID=taskID)
            l = Label4th.objects.get(taskID=task_id)
            l.taskID.remove(p)

    return redirect(to='project')

#タスク追加
def project_add(request):
    projectAll = Project.objects.all();
    if projectAll:
        taskID = Project.objects.order_by('-pk')[:1].values()[0]['taskID'] + 1
    else:
        taskID = 1

    ConfirmationModel = Project.objects.filter( pk = taskID )

    if len(ConfirmationModel) != 0:
        print('登録エラー')
    else:
         if request.method == 'GET':
            taskName = request.GET.get('taskname')
            # label_id = request.GET.get('label_id')
            planStartTime = request.GET.get('planstarttime')
            planFinishTime = request.GET.get('planfinishtime')
            print(planStartTime)

            person_id = request.GET.get('person_id')
            personID = Person.objects.get(personID=person_id)

            label_ids = request.GET.get('label_id')
            label_id_vec = label_ids.split(',')

            p = Project(taskID=taskID, taskName=taskName, personID=personID, planStartTime=planStartTime, planFinishTime=planFinishTime)
            p.dtcreate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            p.save()
            for label_id in label_id_vec:
                # labelID = LabelManage.objects.get(labelID=label_id)
                # p.labelID.add(labelID)
                labelManage = list(LabelManage.objects.all().values('labelID').distinct())
                for label in labelManage:
                    if int(label_id) == int(label['labelID']):
                        p = Project.objects.get(taskID=taskID)
                        l = LabelManage.objects.get(labelID=label_id)
                        l.taskID.add(p)
                label1st = list(Label1st.objects.all().values('labelID').distinct())
                for label in label1st:
                    if int(label_id) == int(label['labelID']):
                        p = Project.objects.get(taskID=taskID)
                        l = Label1st.objects.get(labelID=label_id)
                        l.taskID.add(p)
                label2nd = list(Label2nd.objects.all().values('labelID').distinct())
                for label in label2nd:
                    if int(label_id) == int(label['labelID']):
                        p = Project.objects.get(taskID=taskID)
                        l = Label2nd.objects.get(labelID=label_id)
                        l.taskID.add(p)
                label3rd = list(Label3rd.objects.all().values('labelID').distinct())
                for label in label3rd:
                    if int(label_id) == int(label['labelID']):
                        p = Project.objects.get(taskID=taskID)
                        l = Label3rd.objects.get(labelID=label_id)
                        l.taskID.add(p)
                label4th = list(Label4th.objects.all().values('labelID').distinct())
                for label in label4th:
                    if int(label_id) == int(label['labelID']):
                        p = Project.objects.get(taskID=taskID)
                        l = Label4th.objects.get(labelID=label_id)
                        l.taskID.add(p)

    return redirect(to='project')

#タスク変更
def project_modifiedSave(request):

    if request.method == 'GET':
        taskID = request.GET.get('taskID')
        taskName = request.GET.get('taskname')
        planStartTime = request.GET.get('planstarttime')
        planFinishTime = request.GET.get('planfinishtime')
        actualStartTime = request.GET.get('actualstarttime')
        actualFinishTime = request.GET.get('actualfinishtime')

        person_id = request.GET.get('person_id')
        if person_id:
            personID = Person.objects.get(personID=person_id)

        label_ids = request.GET.get('label_id')
        if label_ids:
            label_id_vec = label_ids.split(',')

        p = Project.objects.get(taskID=taskID)
        if taskName:
            p.taskName = taskName
        if personID:
            p.personID = personID
        if planStartTime:
            p.planStartTime = datetime.strptime(planStartTime, '%Y-%m-%d %H:%M:%S')
        if planFinishTime:
            p.planFinishTime = datetime.strptime(planFinishTime, '%Y-%m-%d %H:%M:%S')
        if actualStartTime:
            p.actualStartTime = datetime.strptime(actualStartTime, '%Y-%m-%d %H:%M:%S')
        if actualFinishTime:
            p.actualFinishTime = datetime.strptime(actualFinishTime, '%Y-%m-%d %H:%M:%S')

        # p = Project(taskID=taskID, taskName=taskName, personID=personID, planStartTime=planStartTime, planFinishTime=planFinishTime)
        p.dtupdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if label_id_vec:
            p.labelID.clear()
            for label_id in label_id_vec:
                labelID = LabelManage.objects.get(labelID=label_id)
                p.labelID.add(labelID)
        p.save()

        return redirect(to='project')

def detail(request, page_num, error_form=None):
    # context = {}
    # project = Project.objects.get(taskID=page_num)
    # context['project'] = project
    # index_page = render(request,'detail.html',context)
    # return index_page
    try:
        request.session['userid']
    except:
        return redirect(to='login')

    context = {}
    form = CommentForm
    project = Project.objects.get(taskID=page_num)
    context['project'] = project
    # context['comment_list'] = comment_list
    if error_form is not None:
        context['form'] = error_form
    else:
        context['form'] = form
    return render(request, 'detail.html', context)

def detail_comment(request, page_num):
    form = CommentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        p = Project.objects.get(taskID=page_num)
        c = Comment(name=name, comment=comment, taskID=p)
        c.dtcreate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.save()
    else:
        return detail(request, page_num, error_form=form)

    return redirect(to='detail', page_num=page_num)


# def detail_timeManage(request):
#
#     p = Project.objects.get(taskID=form.getvalue('taskID'))
#
#     print(form.getvalue('taskID'))
#     p.actualStartTime = form.getvalue('timeA')
#     p.actualFinishTime = form.getvalue('timeB')
#     p.save
#     return redirect(to='detail')
#     index_page = render(request,'detail.html',context)
#     return index_page

# def pjlabel(request):
#     queryset = request.GET.get('projectTitle')
#     if queryset:
#         pjlabel_list = Pjlabel.objects.filter(projectTitle=queryset)
#     else:
#         pjlabel_list = Pjlabel.objects.all()
#     context = {}
#     #pjlabel_list = Pjlabel.objects.all()
#     context['pjlabel_list'] = pjlabel_list
#     index_page = render(request, 'index.html', context)
#     return index_page
#
# def person(request):
#     context = {}
#     person_list = Person.objects.all()
#     context['person_list'] = person_list
#     index_page = render(request, 'index.html', context)
#     return index_page

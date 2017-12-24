from django.http import QueryDict
from django.shortcuts import render,HttpResponse
# Create your views here.
from django.utils.safestring import mark_safe

def testPage(request):
    print("request.GET.URL=%s"%request.GET.urlencode())
    abc = QueryDict(mutable=True)
    abc["hello"]="world"
    print(abc["hello"])
    pagelist=[]
    for i in range(1,200):
        pagelist.append("pagenum=%s"%i)
    pager_obj = Pagination(request.GET.get('page',1),len(pagelist),request.path_info)
    html = pager_obj.page_html()
    # per_page_count=10
    # totoal_count=len(pagelist)
    # max_page_count,b=divmod(totoal_count,per_page_count)
    # if b:
    #     max_page_count+=1
    # start = (current_page-1)*per_page_count
    # end = current_page*per_page_count
    # html=[]
    # for i in range(1,max_page_count+1):
    #     if i==current_page:
    #         temp='<li class="active"><a href="/divpage/?page=%s">%s</a></li>'%(i,i)
    #     else:
    #         temp = '<li><a href="/divpage/?page=%s">%s</a></li>' % (i, i)
    #     html.append(temp)
    # pagehtml="".join(html)
    # print("pagehtml是啥%s类型是啥%s==="%(pagehtml,type(pagehtml)))
    return render(request,"divpage.html",{"pagelist":pagelist[pager_obj.start:pager_obj.end],"data":html})

def test01(request):
    """
     popup功能测试
    :param request:
    :return:
    """
    return render(request,"index.html")

def savedata(request):
    """
     popup功能测试，保存数据并跳转
    :param request:
    :return:
    """
    if request.method=="POST":
        command=request.POST.get("username")
        print("command==%s"%command)
        return render(request,"closeHtml.html",{"command":command})
    return render(request,"saveData.html")
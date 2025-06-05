from django.shortcuts import render 
from . import si_services, isi_services
from .models import PageView  # Import the model
from django.utils.timezone import now 

def index(request): 
    try :
        PageView.objects.create(student_id=id, page='details', date_time=now())
    except : 
        PageView.objects.create(student_id = 'unknown', page='details', date_time=now())

    return render(request, 'main/index.html')

def si_stats(request):
    try :
        PageView.objects.create(student_id=id, page='details', date_time=now())
    except : 
        PageView.objects.create(student_id = 'unknown', page='details', date_time=now())

    si_students = si_services.get_students()
    context = sorted(si_students, key=lambda d: d['moy_gen'],reverse = True)
    
    subjects = si_services.get_subjects()
    subjects = list(subjects.keys())
    
    context = { 
        'students': context,
        'subjects': subjects,
    }
    return render(request, 'main/si_stats.html', context)

def isi_stats(request):
    try :
        PageView.objects.create(student_id=id, page='details', date_time=now())
    except : 
        PageView.objects.create(student_id = 'unknown', page='details', date_time=now())

    isi_students = isi_services.get_students()
    context = sorted(isi_students, key=lambda d: d['moy_gen'],reverse = True)
    subjects = isi_services.get_subjects()
    subjects = list(subjects.keys())
    context = { 
        'students': context,
        'subjects': subjects,
        
        'studentspassed' : len(list(filter(lambda d: d['res'] == "A" , context))),
        'studentscontrole' : len(list(filter(lambda d: d['res'] == "C" , context)))
    }
    return render(request, 'main/isi_stats.html', context)
 
def student_details(request,id) :
    try :
        PageView.objects.create(student_id=id, page='details', date_time=now())
    except : 
        PageView.objects.create(student_id = 'unknown', page='details', date_time=now())

        
    id = int(id)
    si_students =  si_services.get_students()
    isi_students = isi_services.get_students() 
    students = si_students + isi_students  
    is_isi = list(filter(lambda d: d['id'] == id, isi_students)) != [] 
    student = (list(filter(lambda d: d['id'] == id, students))[0])
    major = 'SI'
    subjects = si_services.get_subjects()  
    if is_isi : 
        major = "ISI"
        subjects = isi_services.get_subjects() 
    
    first_term_subjects = []
    for sub in  subjects.items() :
        if sub[1]["sem"] == 1 :
            subject = {
                "name" : sub[0],
                "grade" : student[sub[0]],
                "coef" : sub[1]["coef"]
            }
            first_term_subjects.append(subject)

    
    first_term = {
        "average" : student['moy_gen1'],
        "rank" : student['rang1'],
        "subjects" :first_term_subjects
    } 

    second_term_subjects = []
    for sub in  subjects.items() :
        if sub[1]["sem"] == 2 :
            subject = {
                "name" : sub[0],
                "grade" : student[sub[0]],
                "coef" : sub[1]["coef"]
            }
            second_term_subjects.append(subject)

    second_term = {
        "average" : student['moy_gen2'],
        "rank" : student['rang2'],
        "subjects" : second_term_subjects
    }

    context = {  
        **student, 
        "major":major,
        "first_term" : first_term,
        "second_term" : second_term,


    }
    return render(request, 'main/spesific_student.html',context)


 

def all_views(request):
    views = PageView.objects.all().order_by('-date_time')  # Most recent first
    context = {
        'views': views
    }
    return render(request, 'main/page_views.html', context)

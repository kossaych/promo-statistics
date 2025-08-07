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
    return render(request, 'main/isi_stats.html', context)

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
 
def stats(request): 
    si_students = si_services.get_students()
    isi_students = isi_services.get_students()
    students = si_students + isi_students

    context = sorted(students, key=lambda d: d['moy_gen'],reverse = True)
    subjects = isi_services.get_subjects()
    subjects = list(subjects.keys())
    context = { 
        'students': context,
        'subjects': subjects,
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

 
def compare_students(request):
    # Tracking view
    try:
        PageView.objects.create(student_id="compare", page='compare', date_time=now())
    except:
        PageView.objects.create(student_id='unknown', page='compare', date_time=now())

    # Récupération des IDs depuis query string: /compare/?student_ids=1&student_ids=2
    student_ids = request.GET.getlist('student_ids')
    student_ids = [int(id) for id in student_ids if id.isdigit()]
    print("Comparing students with IDs:", student_ids)

    # Récupération de tous les étudiants
    si_students = si_services.get_students()
    isi_students = isi_services.get_students()
    all_students = si_students + isi_students

    # Filtrer ceux à comparer
    students = [s for s in all_students if s['id'] in student_ids]

    if not students:
        return render(request, 'main/compare.html', {
            'students': [],
            'subjects': [],
            'error': "Aucun étudiant trouvé à comparer."
        })

    # Déterminer toutes les matières uniques présentes
    all_subjects = set()
    for student in students:
        for key in student.keys():
            if key not in ['id','ML','E','rang_A','rang_S','rang_ML','rang_E','num', 'nom', 'prenom', 'moy_gen', 'moy_gen1', 'moy_gen2', 'rang', 'A', 'S', 'res', 'rang1', 'rang2']:
                all_subjects.add(key)

    all_subjects = list(all_subjects)
    all_subjects.sort()

    context = {
        'students': students,
        'subjects': all_subjects
    }

    return render(request, 'main/compare.html', context)

from django.core.checks import messages
from django.db.models import fields
from django.shortcuts import render
from .models import Students
from .forms import StudentsForm
from django.views import generic

def home(request):
    students = Students.objects.all()
    return render(request, 'myapp/index.html', {"students": students})

def search(request):
    students = Students.objects.all()
    keyword = request.GET.get('q')
    result = []
    for object in students.filter(firstname__contains=keyword):
        result.append(object)
    resultExist = False
    if (len(result) == 0):
        resultExist = False
    else :
        resultExist = True
    return render(request, 'myapp/search.html', {"results": result, "resultExist": resultExist})

def create(request):
    form = StudentsForm()
    return render(request, 'myapp/create.html', {"form": form})

def check_post(request):
    if request.method == "POST":
        form = StudentsForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.student_save()
            message = "학생정보를 추가하였습니다."
            return render(request, 'myapp/success.html', {"message": message})
    else:
        form = StudentsForm()
        return render(request, 'myapp/create.html', {"form": form})

class Student_update(generic.UpdateView):
    model = Students
    template_name = 'myapp/update.html'
    fields = ('id', 'firstname', 'secondname', 'major', 'age', 'address')
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'myapp/success.html', {"message": "학생정보를 수정했습니다."})

    def get(self, request, *arg, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

class Student_delete(generic.DeleteView):
    model = Students
    template_name = 'myapp/delete.html'
    success_url = '/'
    context_object_name = 'student'
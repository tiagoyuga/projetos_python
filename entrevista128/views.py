from django.shortcuts import render

# Create your views here.
def post_list(request):
    return render(request, 'entrevista128/post_list.html', {})
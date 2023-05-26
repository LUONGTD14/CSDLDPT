from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from app.common import predictNewData, getNameFromLabel


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        resultPredict = predictNewData(myfile)
        label = getNameFromLabel(resultPredict[1])
        print(resultPredict[1])
        print(label)
        uploaded_file_url = myfile.name
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'label': label
        })
    return render(request, 'core/simple_upload.html')



import re

from django.shortcuts import render, redirect

from .forms import JsonInputDateForm
from .models import JsonInputDate


def convert_to_list_of_dict(data: str) -> list[dict]:
    normalise_date = []
    pattern = r'({[\S\s]+?})'
    for one_dict_entry in re.findall(pattern, data, flags=re.DOTALL):
        pattern_for_name = r'(\s"name": "(.{1,49})"[,\s]+)'
        pattern_for_data = r'(\s"date": "(\d{4}-\d{2}-\d{2}_\d{2}:\d{2})"[\S\s]+?)'
        name = re.findall(pattern_for_name, one_dict_entry)[0][-1]
        date = re.findall(pattern_for_data, one_dict_entry)[0][-1]
        normalise_date.append({
            'name': name,
            'date': date,
        })
    return normalise_date


def index(request):
    if request.method == 'POST':
        form = JsonInputDateForm(data=request.POST)
        if form.is_valid():
            entries = convert_to_list_of_dict(form.cleaned_data['text'])
            for entry in entries:
                new_entry = JsonInputDate.objects.create(**entry)
                new_entry.save()
            return redirect('index')
    else:
        form = JsonInputDateForm()
    context = {
        'form': form,
    }
    return render(request, template_name='main/index.html', context=context)


def show_all_entries(request):
    entries = JsonInputDate.objects.all()
    context = {
        'entries': entries,
    }
    return render(request, template_name='main/entries.html', context=context)

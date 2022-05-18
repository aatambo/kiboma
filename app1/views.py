import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from .algorithm import Apriori_algorithm, items_sort
from .forms import FileUploadForm


def perform_apriori(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = FileUploadForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            csv_file = request.FILES["csv"]
            content = csv_file.read().decode()
            request.session["csv"] = csv_file.name
            request.session["content"] = content
            request.session["min_support"] = form.cleaned_data["min_support"]
            return redirect("csv-results")

    else:
        form = FileUploadForm()

    return render(request, "csv_form.html", {"form": form})


def view_results(request, csv=None):
    try:
        form = FileUploadForm()
        content = request.session["content"]
        min_support = request.session["min_support"]
        csv = request.session["csv"]

        file_contents = []
        for line in content.split("\n"):
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(list(map(str.strip, line.split(",")[1:])))
            file_contents.append(record)

        start = datetime.datetime.now()
        items = Apriori_algorithm(file_contents, min_support)
        end = datetime.datetime.now()
        program_run_time = str((end - start))
        result = items_sort(items)
        all_items = len(items)

        context = {
            "min_support": min_support,
            "csv": csv,
            "items": items,
            "all_items": all_items,
            "program_run_time": program_run_time,
        }
        messages.success(request, f"Successfull!")

        return render(request, "csv_results.html", context)
    except:
        return redirect("csv-form")

from django.shortcuts import render,redirect
from .forms import UserInterestsForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import user_interests
from users.models import Profile
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from .models import Survey, Question, Answer, Submission
from .forms import SurveyForm, QuestionForm, OptionForm, AnswerForm, BaseAnswerFormSet


def home(request):
    users = str(User.objects.count())
    
    context = {
        'users':users,
    }
    return render(request,'survey_app/home.html',context)

@login_required
def user_profile(request):
    return render(request, 'survey_app/user_profile.html')

@login_required
def user_interest(request):
    if request.method == 'POST':
        form = UserInterestsForm(request.POST)
        if form.is_valid():
        	interest = form.save(commit=False)
        	interest.user = request.user
        	interest.save()

        	messages.success(request, f'Thankyou for the submission')
        	return redirect('home')
    else:
        form = UserInterestsForm()
    return render(request, 'survey_app/user_interests_form.html', {'form': form})


# class update_interest(SuccessMessageMixin,UpdateView):
#     model = user_interests
#     template_name = 'survey_app/user_interests_update_form.html'
#     fields = ['sports','music','science']
#     success_message = (f'Interests updated successfully')
#     success_url = reverse_lazy('user-profile')

@login_required
def updateinterestview(request):
    print("we are here at update view")
    if request.method == 'POST':
        i_form = UserInterestsForm(request.POST,instance=request.user.user_interests)
    
        if i_form.is_valid():
            i_form.save()

            print("update successful")
            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile') # we are redirecting for a get request, if we refresh

    else:
        i_form = UserInterestsForm(instance=request.user.user_interests)

    context = {
        'form': i_form,
    }

    return render(request, 'survey_app/user_interests_update_form.html', {'form': i_form})

@login_required
def survey_list(request):
    """User can view all their surveys"""
    surveys = Survey.objects.filter(creator=request.user).order_by("-created_at").all()
    return render(request, "survey_app/list.html", {"surveys": surveys})


@login_required
def detail(request, pk):
    """User can view an active survey"""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user, is_active=True
        )
    except Survey.DoesNotExist:
        raise Http404()

    questions = survey.question_set.all()

    # Calculate the results.
    # This is a naive implementation and it could be optimised to hit the database less.
    # See here for more info on how you might improve this code: https://docs.djangoproject.com/en/3.1/topics/db/aggregation/
    for question in questions:
        option_pks = question.option_set.values_list("pk", flat=True)
        total_answers = Answer.objects.filter(option_id__in=option_pks).count()
        for option in question.option_set.all():
            num_answers = Answer.objects.filter(option=option).count()
            option.percent = 100.0 * num_answers / total_answers if total_answers else 0

    host = request.get_host()
    public_path = reverse("survey-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    
    num_submissions = survey.submission_set.filter(is_complete=True).count()
    return render(
        request,
        "survey_app/detail.html",
        {
            "survey": survey,
            "public_url": public_url,
            "questions": questions,
            "num_submissions": num_submissions,
        },
    )


@login_required
def create(request):
    """User can create a new survey"""
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.creator = request.user
            survey.save()
            return redirect("survey-edit", pk=survey.id)
    else:
        form = SurveyForm()

    return render(request, "survey_app/create.html", {"form": form})


@login_required
def delete(request, pk):
    """User can delete an existing survey"""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        survey.delete()

    return redirect("survey-list")


@login_required
def edit(request, pk):
    """User can add questions to a draft survey, then acitvate the survey"""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user, is_active=False
        )
    except Survey.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey-detail", pk=pk)
    else:
        questions = survey.question_set.all()
        return render(request, "survey_app/edit.html", {"survey": survey, "questions": questions})


@login_required
def question_create(request, pk):
    """User can add a question to a draft survey"""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect("survey-option-create", survey_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "survey_app/question.html", {"survey": survey, "form": form})


@login_required
def option_create(request, survey_pk, question_pk):
    """User can add options to a survey question"""
    survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question_id = question_pk
            option.save()
    else:
        form = OptionForm()

    options = question.option_set.all()
    return render(
        request,
        "survey_app/options.html",
        {"survey": survey, "question": question, "options": options, "form": form},
    )


def start(request, pk):
    """Survey-taker can start a survey"""
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    if request.method == "POST":
        sub = Submission.objects.create(survey=survey)
        return redirect("survey-submit", survey_pk=pk, sub_pk=sub.pk)

    return render(request, "survey_app/start.html", {"survey": survey})


def submit(request, survey_pk, sub_pk):
    submission = Submission.objects.all()
    if submission == True:
        return redirect('home')
    """Survey-taker submit their completed survey."""
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=survey_pk, is_active=True
        )
    except Survey.DoesNotExist:
        raise Http404()

    try:
        sub = survey.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()

    
    questions = survey.question_set.all()
    options = [q.option_set.all() for q in questions]
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(
                        option_id=form.cleaned_data["option"], submission_id=sub_pk,
                    )

                sub.is_complete = True
                sub.save()
            return redirect("survey-thanks", pk=survey_pk)

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)

    question_forms = zip(questions, formset)
    return render(
        request,
        "survey_app/submit.html",
        {"survey": survey, "question_forms": question_forms, "formset": formset},
    )


def thanks(request, pk):
    """Survey-taker receives a thank-you message."""
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    return render(request, "survey_app/thanks.html", {"survey": survey})

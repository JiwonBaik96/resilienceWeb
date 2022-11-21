from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from .forms import CustomUserCreateForm, CustomUserAuthenticationForm, CustomUserChangeForm


# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        signup_form = CustomUserCreateForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, f'환영합니다 {user.username}님')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.add_message(request, messages.WARNING, f'사용자 정보를 다시한번 확인해 주세요!')
    else:
        signup_form = CustomUserCreateForm()
        return render(request=request, template_name="main/register.html", context={"register_form": signup_form})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, f'한번에 한명만 로그인 할 수 있어요!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == 'POST':
        login_form = CustomUserAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, login_form.get_user())
            messages.add_message(request, messages.SUCCESS, f'환영합니다 {user.username}님')
            return redirect("main:map")

        messages.add_message(request, messages.WARNING, f'ID와 비밀번호를 확인해 주세요!')
    else:
        login_form = CustomUserAuthenticationForm()
        return render(request=request, template_name="main/login.html", context={"login_form": login_form})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def logout(request):
    user = request.user
    messages.add_message(request, messages.SUCCESS, f'안녕하가세요 {user.username}님')
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def user_detail(request, username):
    login_form = CustomUserAuthenticationForm()
    signup_form = CustomUserCreateForm()
    user_info = get_object_or_404(User, username=username)
    genre = list(map(int, user_info.genres.split('-')))
    if set(genre) == {0}:
        movies = Movie.objects.all().order_by('-audience')[:5]
        images = []
        for movie in movies:
            images.append(movie.poster_url.format('w200'))

    else:
        GEN = []
        SUM = sum(genre)
        result = []
        for i in range(len(genre)):
            GEN.append([str(i), (genre[i] * 100) // SUM])
            if GEN[i][1] >= 20:
                cnt = GEN[i][1] // 20
                for c in range(cnt):
                    result.append(i)
                    GEN[i][1] -= 20
        GEN.sort(key=lambda x: x[1], reverse=True)
        for i in range(5 - len(result)):
            result.append(int(GEN[i][0]))
        movies = []
        images = []
        i = 0
        for r in result:
            genres = Genre.objects.get(id=r)
            movie = genres.movies.all().order_by('-ratio')[i]
            while movie in movies:
                i += 1
                movie = genres.movies.all().order_by('-ratio')[i]
            movies.append(movie)
            images.append(movie.poster_url.format('w200'))
            i = 0

    return render(request, 'accounts/user_detail.html', {
        'images': images,
        'login_form': login_form,
        'signup_form': signup_form,
        'user_info': user_info,
        'movies': movies
    })


@login_required
@require_http_methods(['POST'])
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_superuser:
        messages.add_message(request, messages.SUCCESS, f'{user.username}님의 계정을 성공적으로 삭제하였습니다.')
        user.delete()
        return redirect('accounts:admin_page')


@login_required
@require_http_methods(['GET', 'PATCH'])
def user_edit(request, user_id):
    login_form = CustomUserAuthenticationForm()
    signup_form = CustomUserCreateForm()
    user = get_object_or_404(User, id=user_id)
    change_form = CustomUserChangeForm(instance=user)
    if request.user.is_superuser:
        if request.method == 'PATCH':
            change_form = CustomUserChangeForm(data=request.data, instance=user)
            if change_form.is_valid():
                change_form.save()
                return redirect('accounts:admin_page')
        context = {
            'login_form': login_form,
            'signup_form': signup_form,
            'change_form': change_form,
        }
        return render(request, 'accounts/user_edit.html', context)


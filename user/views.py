from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import SignUpForm, LoginForm
from django.urls import reverse_lazy
# mail activation
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_str
from .models import CustomUser, Profile
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from user_ads.models import RealEstateLike
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404



def send_activation_email(request, user):
    token_generator = default_token_generator
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    activation_url = request.build_absolute_uri(
        f'/activate/{uid}/{token}'
    )
    html_message = render_to_string('mail/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })
    send_mail(
        subject='Activate your account',
        message=None,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def reactivate_user(request, email):
    user = CustomUser.objects.get(email=email)
    if user.is_active:
        messages.info(request, 'Your account is already active')
        return redirect('login')
    send_activation_email(request, user)
    return redirect('activation_sent')


def sign_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # make profile before save user...
            Profile.objects.create(user=user)

            send_activation_email(request, user)
            # send activation email
            # token_generator = default_token_generator
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = token_generator.make_token(user)
            # activation_url = request.build_absolute_uri(
            #     f'/activate/{uid}/{token}'
            # )
            # html_message = render_to_string('mail/activation_email.html', {
            #     'user': user,
            #     'activation_url': activation_url,
            # })
            # send_mail(
            #     subject='Activate your account',
            #     message=None,
            #     html_message=html_message,
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[user.email],
            #     fail_silently=False,
            # )
            return redirect(to='activation_sent')
    context = { 'form': form,
                'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
                }
    return render(request, 'registration/sign_up.html', context)


def activation_sent(request):
    return render(request, 'registration/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    token_generator = default_token_generator
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return redirect('activation_success')

    else:
        messages.error(request, 'Activation link is invalid or has expired')
        return redirect('activation_error')
        # send new link


def activation_success(request):
    return render(request, 'registration/activation_success.html')


def activation_error(request):
    return render(request, 'registration/activation_error.html')


def login_view(request):
    next_url = 'home'
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or 'home'
                return redirect(next_url)
        else:
            # next for not active user
            email = str(form.cleaned_data.get('username'))
            not_activ_list = CustomUser.objects.filter(is_active=False)
            for user_not_active in not_activ_list:
                if email == user_not_active.email:
                    user = CustomUser.objects.get(email=email)
                    return render(request, 'registration/resend_activation_email.html', {"user": user})

    elif request.method == "GET":
        next_url = request.GET.get('next') or 'home'
        form = LoginForm(initial={'next': next_url})
    context = { "form": form,
                "next_url": next_url,
                'ENABLE_RECAPTCHA': settings.ENABLE_RECAPTCHA,
                }
    return render(request, 'registration/login.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')


@login_required
def passwordChange_Done(request):
    return render(request, 'registration/pass_change_done.html')


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_sent')

    def form_valid(self, form):
        # Get the user associated with the email address entered in the form
        email = form.cleaned_data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None and user.is_active:
            # If user is active, send the password reset email
            return super().form_valid(form)
        elif user is not None and not user.is_active:
            # If user is not active, redirect to a page with instructions to activate account
            return redirect('reactivate_user', email=email)
        else:
            # If user doesn't exist, display a generic error message
            # fix it
            form.add_error(
                'email', 'There is no user with this email address.')
            return self.form_invalid(form)


def passwordReset_Sent(request):
    return render(request, 'registration/pass_reset_sent.html')


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_done')


def passwordReset_Done(request):
    return render(request, 'registration/pass_reset_done.html')


@login_required
def profile(request):
    real_estate_ads = request.user.realestate_set.all()
    context = {
        'real_estate_ads': real_estate_ads,
        'user': request.user,
    }
    return render(request, 'user/profile.html', context)


# class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
# only for superuser
class ProfileDetailView(UserPassesTestMixin, generic.DetailView):

    model = Profile
    template_name = 'user/profile_detail.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user = profile.user
        real_estates = user.realestate_set.all()
        context['real_estates'] = real_estates
        return context


@login_required
def profile_delete(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST.get('password')
        if user.check_password(password):
            user.delete()
            logout(request)
            messages.success(request, 'Your account has been deleted')
            return redirect('home')
        else:
            messages.error(
                request, 'Incorrect password. Account was not deleted.')
    return render(request, 'registration/delete_user.html')

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
# Create your views here.


from tools.confman import get_lang

UNIVERSAL_LANG = get_lang(sections=["universal"])

def RegisterView(request):
    '''
    This view will display the registration page and when submitting a
    registration it will enter here.

    If submitting a registration POST will contain the following.
        first_name - Users first name
        last_name - Users last name
        date_of_birth - When user was born
        gender - Gender of the user. Is one of the following
            Male
            Female
            Other
        gender_other - If user choose gender=Other this will contain a text.
        email - Users email.
        password - Users entered non hashed password
        repassword - reentered password to dubble check that user entered the
            right one.
        agree_terms - Värdet ska vara 'accept'
    '''

    login_lang = get_lang(sections=["login"])  # Get language text for form.
    wrong_password_enterd = True  # ROBIN!!!!!! TITTA HÄR!!! Ändra denna till true om lösenordet är fel

    # Check if a user have submitted a form.
    if request.method == 'POST':
        registerUser()

        return HttpResponseRedirect(reverse('home:index')) # ROBIN!!!!! TITTA HÄR! Den här ska användas vid redirekt när man har successfully loggat in.

    args = {
        'POST': request.POST,
        'menu_titles': UNIVERSAL_LANG["universal"]["titles"],
        'form': login_lang["login"]["form"],
        'alerts': login_lang['login']['long_texts']['alerts'],
        'pattern': login_lang['login']['long_texts']['allowed_chars'],
        'wrong_password_enterd': wrong_password_enterd  # A check if right password was entered
    }
    return render(request, 'login/register.html', args)


def registerUser(): # Place function somewere else.
    return None

def LoginView(request):
    login_lang = get_lang(sections=["login"])
    wrong_login_enterd = False
    args = {
        'post': request.POST,
        'menu_titles': UNIVERSAL_LANG["universal"]["titles"],
        'form': login_lang["login"]["form"],
        'alerts': login_lang['login']['long_texts']['alerts'],
        'wrong_password_enterd': wrong_login_enterd  # A check if right login was entered
    }

    return render(request, 'login/login.html', args)

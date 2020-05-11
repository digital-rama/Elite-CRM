from manpower.models import SuperVisors, profilePic


def profile_Piccture(request):
    if request.user.is_staff:
        profile = profilePic.objects.all()
        profile_pic = profile[0].profile_pic.url
    else:
        usern = request.user.username
        super_id = SuperVisors.objects.get(username=usern)
        profile_pic = super_id.image.url

    return {'profile_pic': profile_pic}

import operator
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
from .base import register
from materialize_nav.settings import mysettings


__all__ = ["render_user_chip", "render_user_image", "render_user_background"]


def get_user_thumbnail(user):
    """Return the users thumbnail or None if not found."""
    try:
        return operator.attrgetter(mysettings.USER_THUMBNAIL_PROPERTY)(user)
    except:
        return static(mysettings.USER_THUMBNAIL)


def get_user_background_image(user):
    """Return the users background image or None if not found."""
    try:
        return operator.attrgetter(mysettings.USER_BACKGROUND_PROPERTY)(user)
    except:
        return static(mysettings.USER_BACKGROUND_IMAGE)


@register.inclusion_tag("materialize_nav/user/user_chip.html")
def render_user_chip(user, show_full_name=False, default_user_image=None):
    d = {"user": user, "show_full_name": show_full_name,
         'account_icon': mark_safe('<i class="material-icons">account_circle</i>'),
         'thumbnail': get_user_thumbnail(user)}
    return d


@register.inclusion_tag("materialize_nav/user/user_image.html")
def render_user_image(user, style="", class_names="", default_user_image=None):
    d = {"user": user, "style": style, "class_names": class_names,
         'thumbnail': get_user_thumbnail(user)}
    return d


@register.inclusion_tag("materialize_nav/user/user_background.html", takes_context=True)
def render_user_background(context, user, url=None, thumbnail=None, background_image=None):
    """Render the side bar with the user background and profile picture."""
    d = context.flatten().copy()
    d.update({"user": user, "url_path": context["request"].path})

    # URL
    if url is None:
        url = 'profile'
    d['user_url'] = url

    # User Image
    if thumbnail is None:
        thumbnail = get_user_thumbnail(user)
    d['thumbnail'] = thumbnail

    # Background Image
    if background_image is None:
        background_image = get_user_background_image(user)
    d['background_image'] = background_image

    return d

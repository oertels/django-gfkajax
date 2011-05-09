from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

@staff_member_required
def get_object(request):

    ct = request.POST.get('ct', None)
    fk = request.POST.get('fk', None)

    if not fk:
        return HttpResponse('-- no object selected --')
    # Get db-objects for content type and foreign key object
    ct_obj = ContentType.objects.get(id=ct)
    fk_obj = ct_obj.model_class().objects.get(id=fk)

    if hasattr(fk_obj, 'gfk_render'):
        return HttpResponse(mark_safe(fk_obj.gfk_render()))
    else:
        if hasattr(fk_obj, '__unicode__'):
            return HttpResponse(fk_obj.__unicode__())
        else:
            return HttpResponse(str(fk_obj))

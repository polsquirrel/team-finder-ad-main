from django.core.paginator import Paginator

from projects.constants import PROJECTS_PER_PAGE


def paginate_queryset(request, queryset, per_page=PROJECTS_PER_PAGE):
    page_param = request.GET.get("page")
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_param)

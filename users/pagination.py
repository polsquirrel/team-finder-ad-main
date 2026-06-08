from django.core.paginator import Paginator

from users.constants import USERS_PER_PAGE


def paginate_queryset(request, queryset, per_page=USERS_PER_PAGE):
    page_param = request.GET.get("page")
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_param)

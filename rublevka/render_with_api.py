# -*- coding: utf-8 -*-

from django.shortcuts import render


# Используя этот декоратор над вью мы добиваемся следующего:
# 1. Результирующий вью возвращает рендер HTML шаблона render(request, templateName, locals())
# 2. Декорируемый вью должен вернуть переменные для подстановки в шаблон
# 3. Если в запросе есть параметр api, используется суффикс api_ для файла шаблона.
def render_with_api(templateName):
    def render_with_api_decor(f):
        def render_with_api_wrapper(request, *args, **kwargs):
            templateFile = templateName
            if 'api' in request.GET:
                templateFile = 'api_' + templateName
            return render(request, templateFile, f(request, *args, **kwargs))
        return render_with_api_wrapper
    return render_with_api_decor

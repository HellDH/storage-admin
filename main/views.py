from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Sum

from rest_framework.views import APIView

from main.models import Supply

@method_decorator(staff_member_required, name='dispatch')
class InventPageView(APIView):
    def post(self, request):
        data_name = request.POST.getlist('datanm')
        data_count = request.POST.getlist('datacn')

        processed_data = []
        
        for record in range(len(data_name)):
            data_untag = Supply.objects.all().filter(name=data_name[record]). \
                    aggregate(Sum('count'))
            
            processed_data.append(f"Соответствие товара {data_name[record]}: {int(data_count[record]) - data_untag['count__sum']}")

        return JsonResponse({"response": processed_data})

    def get(self, request):
        return render(request, 'graph/invent_template.html')

@method_decorator(staff_member_required, name='dispatch')
class AnalysisPageView(APIView):
    def post(self, request):
        data = Supply.objects.all()
        labels = [item.name for item in data]
        values = [item.count for item in data]

        context = {
            'labels': labels,
            'values': values,
        }

        return render(request, 'graph/charts.html', context)

    def get(self, request):
        return render(request, 'graph/charts.html')

def index(request):
    return redirect('admin/', permanent=True)


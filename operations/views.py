import sys
sys.path.append("..")

import io
import base64

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from django.shortcuts import render

from main import models

def charts_view(request):
    queryset = models.Supply.objects.all()
    names = [s.name for s in queryset]
    amounts = [s.count for s in queryset]
    
    # Создание графика с помощью Matplotlib
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot(names, amounts)
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.grid(True)
    
    # Сохранение графика в буфер
    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    
    # Преобразование буфера в строку base64
    png_str = base64.b64encode(buf.getvalue()).decode('utf8')
    
    # Передача строки base64 в контекст шаблона
    context = {
        'png_str': png_str,
    }
    
    return render(request, 'sales_chart.html', context)


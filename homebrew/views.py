from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.forms.fields import TextInput
### Can add @method_decorator(login_required) to views now ...
from .models import Batch, SourceIngredient, Box, Comment, Label, Sugar, Yeast

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.barcode.qr import QrCodeWidget 
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics import renderPDF
from io import BytesIO
from django.db.models import Q


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'homebrew/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['batch_list'] = Batch.objects.order_by('-pot_start_date')[:20]
        context['box_list'] = Box.objects.all()
        return context

class BatchListView(generic.ListView):
    model = Batch

    def get_queryset(self):
        if self.request.GET.has_key('search'):
            search = self.request.GET['search']
            query = Batch.objects.filter(Q(sourceingredient__name__icontains=search) | Q(label__name__icontains=search) | Q(sugar__name__icontains=search) | Q(yeast__name__icontains=search))
            if search.isdigit():
                print('Its a digit')
                #How do you append this?
                id_query = Batch.objects.filter(Q(id__exact=search))
                query = query | id_query
                #query = query.filter(Q(id__exact=search))
            return query
        return Batch.objects.all()

class BatchCreateView(CreateView):
    model = Batch
    fields = ['sourceingredient', 'yeast', 'yeast_volume', 'sugar', 'sugar_volume', 'pot_start_date', 'bottling_date', 'start_specific_gravity', 'end_specific_gravity', 'start_temperature', 'avg_predicted_temperature', 'label', 'maker_comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BatchCreateView, self).form_valid(form)

class BatchUpdateView(UpdateView):
    model = Batch
    fields = ['sourceingredient', 'yeast', 'yeast_volume', 'sugar', 'sugar_volume', 'pot_start_date', 'bottling_date', 'start_specific_gravity', 'end_specific_gravity', 'start_temperature', 'avg_predicted_temperature', 'label', 'maker_comment']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BatchUpdateView, self).form_valid(form)

class BatchDetailView(generic.TemplateView):
    ### Change this to a template view, and make it show
    # the recent comments, with a link to all comments. 
    template_name = 'homebrew/batch_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BatchDetailView, self).get_context_data(**kwargs)
        context['batch'] = self.batch
        context['comments'] = Comment.objects.filter(batch=self.batch)[:5]
        return context

    def dispatch(self, *args, **kwargs):
        self.batch = get_object_or_404(Batch, pk=kwargs['pk'])
        return super(BatchDetailView, self).dispatch(*args, **kwargs)

class IngredientView(generic.TemplateView):
    template_name = 'homebrew/ingredient_list.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientView, self).get_context_data(**kwargs)
        context['sourceingredient_list'] = SourceIngredient.objects.all()
        context['sugar_list'] = Sugar.objects.all()
        context['yeast_list'] = Yeast.objects.all()
        return context

class SourceIngredientDetailView(generic.DetailView):
    model = SourceIngredient

class SourceIngredientCreateView(CreateView):
    model = SourceIngredient
    fields = ['name', 'comment', 'bottle_time', 'volume', 'label', 'source_ean']

class SourceIngredientUpdateView(UpdateView):
    model = SourceIngredient
    fields = ['name', 'comment', 'bottle_time', 'volume', 'label', 'source_ean']

#class SourceIngredientDelete(DeleteView):

class SugarCreateView(CreateView):
    model = Sugar
    fields = ['name', 'comment']

class SugarUpdateView(UpdateView):
    success_url=reverse_lazy('homebrew:ingredient_view')
    model = Sugar
    fields = ['name', 'comment']

class YeastCreateView(CreateView):
    model = Yeast
    fields = ['name', 'comment']

class YeastUpdateView(UpdateView):
    success_url=reverse_lazy('homebrew:ingredient_view')
    model = Yeast
    fields = ['name', 'comment']

class CommentCreateView(CreateView):
    ### TODO: Should only be able to comment while boxes that contain batch still has bottles in ....., or not after two boths after ready 
    model = Comment
    #fields = ['viewpoint', 'batch']
    #success_url='/homebrew/comment/thanks/'
    success_url=reverse_lazy('homebrew:comment_thanks')
    def get_form_class(self):
        if self.batch is None:
            return modelform_factory(Comment, fields=('batch', 'viewpoint'), widgets={'batch': TextInput()})
        return modelform_factory(Comment, fields=('viewpoint',))

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['batch'] = self.batch
        return context

    def dispatch(self, *args, **kwargs):
        if 'pk' in kwargs:
            self.batch = get_object_or_404(Batch, pk=kwargs['pk'])
        else:
            self.batch = None
        return super(CommentCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.batch is not None:
            form.instance.batch = self.batch
        return super(CommentCreateView, self).form_valid(form)
        #form.batch = self.request.

class CommentThanksView(generic.TemplateView):
    template_name = 'homebrew/comment_thanks.html'

class BoxDetailView(generic.DetailView):
    model = Box

class BoxCreateView(CreateView):
    model = Box
    fields = ['name', 'comment', 'batch', 'bottle_capacity', 'max_bottles', 'number_bottles', 'comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BoxCreateView, self).form_valid(form)

class BoxUpdateView(UpdateView):
    model = Box
    fields = ['name', 'comment', 'batch', 'bottle_capacity', 'max_bottles', 'number_bottles', 'comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BoxUpdateView, self).form_valid(form)

class BoxDeleteView(DeleteView):
    model = Box
    success_url = reverse_lazy('homebrew:index')

class LabelListView(generic.ListView):
    model = Label

class LabelCreateView(CreateView):
    model = Label

class LabelUpdateView(UpdateView):
    model = Label

class LabelDeleteView(DeleteView):
    model = Label
    success_url = reverse_lazy('homebrew:label_list')

class LabelDetailView(generic.DetailView):
    model = Label



class L7160(object):
    WIDTH = 63.5 * mm
    HEIGHT = 38.1 * mm
    ACROSS = 3
    DOWN = 7
    #MARGIN_TOP = 13 * mm
    MARGIN_TOP = 15 * mm
    MARGIN_LEFT = 7 * mm
    VERTICAL_GAP = 2.5 * mm
    HORIZONTAL_GAP = 0 * mm

    def LabelPosition(self, index):
        y,x = divmod(index, self.ACROSS)
        x1 = self.MARGIN_LEFT + ( x * (self.WIDTH + self.VERTICAL_GAP))
        y1 = self.MARGIN_TOP + ( y * (self.HEIGHT + self.HORIZONTAL_GAP))
        return x1, y1

    def generate_qr(self, text):
        pass
        qr_code = QrCodeWidget(text, barLevel='Q')
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        self.qr_draw = Drawing(20, 20, transform=[40./width,0,0,40./height,0,0])
        self.qr_draw.add(qr_code) 

    def generate_ean(self, text):
        ####  For some reason this keeps replacing the (correct) check digit
        ## with a 0 .... 
        barcode_eanbc13 = Ean13BarcodeWidget(text, barHeight=self.HEIGHT * 0.20)
        bounds = barcode_eanbc13.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        self.ean_draw = Drawing(30, 30)
        self.ean_draw.add(barcode_eanbc13)

    def set_text(self, text):
        self.text = text

    def set_image(self, image_path):
        self.image_path = image_path

    def draw_labels(self, canv):
        for pos in range( 0, self.ACROSS * self.DOWN ):
            x, y = self.LabelPosition( pos )
            #canv.rect( x, y, self.WIDTH, self.HEIGHT )
            canv.drawImage(self.image_path, x, y + self.HEIGHT * 0.30, self.WIDTH , self.HEIGHT * 0.70, preserveAspectRatio=True)
            tx = canv.beginText( x + self.WIDTH * 0.01, y+self.HEIGHT * 0.24)
            tx.setFont( 'Helvetica', 8, 8 )
            tx.textLines( self.text )
            #    
            canv.drawText( tx )
            #barcode = code39.Extended39("0001")
            #barcode.drawOn(canv, x + width *0.5, y+height * 0.05)
            renderPDF.draw(self.qr_draw, canv, x + self.WIDTH * 0.75, y -3 ) #+ HEIGHT )
            renderPDF.draw(self.ean_draw, canv, x + 4, y) # + HEIGHT)

def batch_label(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer = BytesIO()
    label = L7160()
    canv = canvas.Canvas( buffer, pagesize=A4 )
    canv.setPageCompression( 0 )
    if batch.label is None:
        label.set_image(batch.sourceingredient.label.image.path)
    else:
        label.set_image(batch.label.image.path)
    label.set_text(batch.label_text)
    label.generate_qr("http://homebrew.blackhats.net.au/homebrew/comment/%s/" % batch.id)
    label.generate_ean(batch.sourceingredient.ean13)
    label.draw_labels(canv)
    canv.showPage()
    canv.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

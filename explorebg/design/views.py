from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from explorebg.design.forms import DesignForm, EditDesignForm
from explorebg.design.models import Design, LikeDesign


class AddDesignView(CreateView):
    template_name = 'add_design.html'
    form_class = DesignForm
    success_url = reverse_lazy('design list')

    @method_decorator(permission_required('explorebg.add_design', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddDesignView, self).dispatch(*args, **kwargs)


class DesignListView(LoginRequiredMixin, ListView):
    model = Design
    template_name = 'design_list.html'
    context_object_name = 'design_photos'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super(DesignListView, self).get_context_data(**kwargs)
        is_liked = {}
        designs = Design.objects.all()
        for design in designs:
            if design.likedesign_set.filter(user_id=self.request.user.id).first():
                is_liked[design.name] = True
            else:
                is_liked[design.name] = False
        context['is_liked'] = is_liked
        return context


class DeleteDesignView(LoginRequiredMixin, DeleteView):
    template_name = 'delete_design.html'
    model = Design
    success_url = reverse_lazy('design list')

    @method_decorator(permission_required('explorebg.delete_design', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeleteDesignView, self).dispatch(*args, **kwargs)


class EditDesignView(LoginRequiredMixin, UpdateView):
    model = Design
    template_name = 'edit_design.html'
    form_class = EditDesignForm
    success_url = reverse_lazy('design list')

    @method_decorator(permission_required('explorebg.change_design', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(EditDesignView, self).dispatch(*args, **kwargs)


@login_required
def like_design(request, pk):
    design = Design.objects.get(pk=pk)
    like_object_by_user = design.likedesign_set.filter(user_id=request.user.id).first()

    if like_object_by_user:
        like_object_by_user.delete()
    else:
        like = LikeDesign(
            design=design,
            user=request.user,
        )
        like.save()
    return redirect('design list')

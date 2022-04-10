from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from explorebg.design.forms import DesignForm, EditDesignForm
from explorebg.design.models import Design, LikeDesign


class AddDesignView(PermissionRequiredMixin, CreateView):
    permission_required = 'design.add_design'
    template_name = 'design/add_design.html'
    form_class = DesignForm
    success_url = reverse_lazy('design list')


class DesignListView(LoginRequiredMixin, ListView):
    model = Design
    template_name = 'design/design_list.html'
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


class DeleteDesignView(PermissionRequiredMixin, DeleteView):
    permission_required = 'design.delete_design'
    template_name = 'design/delete_design.html'
    model = Design
    success_url = reverse_lazy('design list')


class EditDesignView(PermissionRequiredMixin, UpdateView):
    permission_required = 'design.change_design'
    model = Design
    template_name = 'design/edit_design.html'
    form_class = EditDesignForm
    success_url = reverse_lazy('design list')


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

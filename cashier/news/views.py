from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from cashier.mixins.mixins import OwnerOrSuperUserRequiredMixin
from cashier.news.forms import CommentForm
from cashier.news.models import News, Comment


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    ordering = ['-pk']
    template_name = 'home_view.html'
    context_object_name = 'news'
    paginate_by = 5

class CommentNewsView(LoginRequiredMixin, ListView):
    model = Comment
    ordering = ['-pk']
    template_name = 'news_details.html'
    context_object_name = 'all_comments'
    paginate_by = 5
    def get(self, request, *args, **kwargs):
        news_object = News.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        self.queryset = news_object.comment_set.all()
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = CommentForm()
        context['news_object'] = news_object
        return self.render_to_response(context)
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            temp_form = form.save(commit=False)
            temp_form.News = News.objects.get(pk=pk)
            temp_form.user = self.request.user
            temp_form.save()
        return HttpResponseRedirect(reverse_lazy('comment_news_view', kwargs={'pk' : pk}))

class DeleteCommentView(DeleteView):
    model = Comment
    context_object_name = 'form'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user or request.user.is_superuser:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(reverse_lazy('comment_news_view', kwargs={'pk': self.object.News.id}))

    def get_success_url(self):
        self.success_url = reverse_lazy('comment_news_view', kwargs={'pk': self.object.News.id})
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
    template_name = 'delete_comment.html'
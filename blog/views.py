from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.text import slugify
from django.contrib import messages
from django.urls import reverse_lazy as _
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from .form import EmailPostForm
from .models import Post, Tag


# Create your views here.
class PostListView(ListView):
    queryset = Post.objects.filter(status=Post.PostStatus.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


class TagListView(ListView):
    queryset = Tag.objects.filter()
    context_object_name = 'tags'
    template_name = 'blog/post/tags_list.html'


def posts_by_tag(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    posts = Post.objects.filter(tag=tag)
    return render(request, 'blog/post/posts_by_tag.html', {'tag': tag, 'posts': posts})


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "tag", "body", "image"]
    template_name = 'blog/post/post_creation.html'

    def get_success_url(self):
        messages.success(self.request, 'Your post has been created successfully.')
        return _('blog:post_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.status = 'published'
        obj.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "tag", "body", "image"]
    template_name = 'blog/post/post_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update
        return context

    def get_success_url(self):
        messages.success(self.request, 'Your post has been updated successfully.')
        return _('blog:post_list')

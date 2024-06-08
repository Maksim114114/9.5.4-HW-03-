from django import forms

from .models import Post



class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_author'].label = 'id_автора'
        self.fields['title'].label = 'Заголовок'
        self.fields['post_text'].label = 'пост'
        #self.fields['categories'].empty_label = None
        self.fields['event'].label = 'событие(formss.py)'
        self.fields['categories'].label = 'Категория(formss.py)'

        # self.fields['post_author_id'].label = 'Автор'


    class Meta:
        model = Post

        fields = ['post_author',
                  'event',
                  'title',
                  'categories',
                  'post_text',

                  ]
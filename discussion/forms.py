from django import forms
from . import models

class CreateDiscussionForm(forms.ModelForm):

    class Meta:
        model = models.Discussion
        fields = ['category', 'title', 'content', 'privacy_status', 'secondary_tag', 'ter_tag']#'tertiary_tag',]
        #exclude = ('updated', 'created')

    def __init__(self, *args, **kwargs):
        super(CreateDiscussionForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'id':'category_id', 'class':'form_class'})
        self.fields['title'].widget.attrs.update({'id':'title_id', 'class':'form_class'})
        self.fields['content'].widget.attrs.update({'id':'content_id', 'class':'form_class'})
        self.fields['secondary_tag'].widget.attrs.update({'id':'secondary_tag_id', 'class':'form_class'})
        #self.fields['tertiary_tag'] = forms.CharField()
        self.fields['ter_tag'].label = 'Tertiary Tag'
        self.fields['ter_tag'].widget.attrs.update({'id':'tertiary_tag_id', 'class':'form_class'})
        self.fields['privacy_status'].widget.attrs.update({'id':'privacy_id', 'class':'form_class'})


class CreateDiscussorForm(forms.ModelForm):
    class Meta:
        model = models.Discussor
        fields = ['reply_to', 'context', 'content','secondary_tag', 'ter_tag']
        #exclude = ('updated', 'created')

    def __init__(self, *args, **kwargs):
        super(CreateDiscussorForm, self).__init__(*args, **kwargs)
        self.fields['reply_to'].widget.attrs.update({'id':'reply_to_id', 'class':'discussor_form_class'})
        self.fields['context'].widget.attrs.update({'id':'context_id', 'class':'discussor_form_class'})
        self.fields['content'].widget.attrs.update({'id':'content_id', 'class':'discussor_form_class'})
        self.fields['secondary_tag'].widget.attrs.update({'id':'secondary_tag_id', 'class':'discussor_form_class'})

        discussion_id =[]#= kwargs.pop('objectid')
        if discussion_id:
            discussion_object = models.Discussion.objects.get(pk=discussion_id)
            self.fields['reply_to'].queryset = models.DiscussionTimeLine.objects.filter(discussion = discussion_object)
            self.fields['secondary_tag'].queryset = models.SecondaryTag.objects.filter(category = discussion_object.category)
            self.fields['ter_tag'].label = 'Tertiary Tag'
            self.fields['ter_tag'].widget.attrs.update({'id':'tertiary_tag_id', 'class':'form_class'})        

       

class CreateNewDiscussorForm(forms.Form):

    reply_to = forms.ModelChoiceField(queryset = models.DiscussionTimeLine.objects.all(), required=True)
    context = forms.CharField(max_length = 100)
    content = forms.CharField(widget=forms.Textarea)
    secondary_tag = forms.ModelChoiceField(queryset=models.SecondaryTag.objects.all())
    ter_tag = forms.CharField(label='Tertiary tag', max_length=1000)

    class Meta:
        fields = ['reply_to', 'context', 'content','secondary_tag', 'ter_tag',]
        #exclude = ('updated', 'created')

    def __init__(self, *args, **kwargs):
        discussion_id = kwargs.pop('objectid')
        analyser = kwargs.pop('analyser')
        super(CreateNewDiscussorForm, self).__init__(*args, **kwargs)
        self.__name__ = 'DiscussorForm'
        self.fields['reply_to'].widget.attrs.update({'id':'reply_to_id', 'class':'discussor_form_class'})
        self.fields['context'].widget.attrs.update({'id':'context_id', 'class':'discussor_form_class'})
        self.fields['content'].widget.attrs.update({'id':'content_id', 'class':'discussor_form_class'})
        self.fields['secondary_tag'].widget.attrs.update({'id':'secondary_tag_id', 'class':'discussor_form_class'})
        self.fields['ter_tag'].widget.attrs.update({'id':'tertiary_tag_id', 'class':'form_class'})

        if discussion_id:
            discussion_object = models.Discussion.objects.get(pk=discussion_id)
            queryset = models.DiscussionReply.objects.filter(discussion = discussion_object).exclude(analyser=analyser)
            self.fields['reply_to'].queryset = queryset #models.DiscussionReply.objects.filter(discussion = discussion_object)
            #for now lets show all the secondary tags.
            #self.fields['secondary_tag'].queryset = models.SecondaryTag.objects.filter(category = discussion_object.category)
            self.fields['secondary_tag'].queryset = models.SecondaryTag.objects.all()


class DiscussionAndDiscussorUpdateForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class ConfirmForm(forms.Form):
    YES = 'YES'
    NO = 'NO'
    CONFIRM_STATUS = (
        (NO, 'no'),
        (YES, 'yes')
    )
    confirm = forms.ChoiceField(choices = CONFIRM_STATUS)
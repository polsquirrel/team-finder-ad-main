from django import forms

from projects.models import Project, PROJECT_STATUS_CHOICES

GITHUB_DOMAIN = "github.com"
GITHUB_LINK_ERROR = "Ссылка должна вести на GitHub"


class BaseGithubForm(forms.ModelForm):
    def clean_github_url(self):
        github_link = self.cleaned_data.get("github_url")
        if github_link and GITHUB_DOMAIN not in github_link:
            raise forms.ValidationError(GITHUB_LINK_ERROR)
        return github_link


class ProjectForm(BaseGithubForm):
    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "status": forms.Select(choices=PROJECT_STATUS_CHOICES),
        }

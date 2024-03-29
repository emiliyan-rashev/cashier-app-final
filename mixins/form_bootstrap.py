class BootStrapFormMixin:
    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        self.apply_bootstrap_classes(form)
        return form

    def apply_bootstrap_classes(self, form):
        for field_name, curr_field in form.fields.items():
            if "class" not in curr_field.widget.attrs:
                curr_field.widget.attrs["class"] = ""
            if curr_field.__class__.__name__ not in ["CharField"]:
                if curr_field.widget.input_type not in ["checkbox", "radio"]:
                    curr_field.widget.attrs["class"] += " form-control"
                else:
                    if curr_field.__class__.__name__ not in ["ChoiceField"]:
                        curr_field.widget.attrs["class"] += " form-check-input"
            else:
                curr_field.widget.attrs["class"] += " form-control"
            if curr_field.help_text:
                curr_field.widget.attrs["aria-describedby"] = f"{field_name}HelpBlock"
                curr_field.help_text = (
                    f'<small id="{field_name}HelpBlock" class="form-text text-muted">'
                    f"{curr_field.help_text}</small>"
                )

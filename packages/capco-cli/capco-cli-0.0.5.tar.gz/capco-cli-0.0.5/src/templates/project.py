class Project:

    @classmethod
    def generate(cls, template, options, target_dir):
        rendered = template.render(options)
        rendered.write(target_dir)
        return cls

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('../templates'))


def render_template(name, values=None, **kwargs):
    template = env.get_template(name)

    if values:
        rendered_template = template.render(values, **kwargs)
    else:
        rendered_template = template.render(**kwargs)

    return rendered_template

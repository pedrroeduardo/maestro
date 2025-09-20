from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


class IconNode(template.Node):
    def __init__(self, name_expr, attrs):
        self.name_expr = name_expr                # FilterExpression
        self.attrs = attrs                        # dict[str, FilterExpression]

    def render(self, context):
        name = self.name_expr.resolve(context)

        style = "fas"
        if "style" in self.attrs:
            style_val = self.attrs["style"].resolve(context)
            if style_val:
                style = str(style_val)

        class_bits = [f"{style} fa-{name}"]
        if "class" in self.attrs:
            extra = self.attrs["class"].resolve(context)
            if extra:
                class_bits.append(str(extra).strip())

        final_class = " ".join(class_bits).strip()

        other_attrs = []
        for key, expr in self.attrs.items():
            if key in {"class", "style"}:
                continue
            val = expr.resolve(context)
            if val is None or val == "":
                continue
            other_attrs.append(f'{key}="{conditional_escape(val)}"')

        html = f'<i class="{conditional_escape(final_class)}"'
        if other_attrs:
            html += " " + " ".join(other_attrs)
        html += "></i>"

        return mark_safe(html)


@register.tag(name="icons")
def do_icon(parser, token):
    """
    Sintax:
        {% icon "chevron-left" %}
        {% icon "chevron-left" class="text-gray-500" %}
        {% icon "chevron-left" :class="collapsed && 'rotate-180'" %}
        {% icon "github" style="fab" class="text-blue-500" data-track="x" %}
    """

    bits = token.split_contents()
    tag_name = bits.pop(0)
    if not bits:
        raise template.TemplateSyntaxError(f'"{tag_name}" require at least the name of the icon.')

    name_expr = parser.compile_filter(bits.pop(0))

    attrs = {}
    for bit in bits:
        if "=" not in bit:
            raise template.TemplateSyntaxError(
                f'Invalid Argument {tag_name}: "{bit}". Use key="value".'
            )
        key, value = bit.split("=", 1)
        attrs[key] = parser.compile_filter(value)

    return IconNode(name_expr, attrs)

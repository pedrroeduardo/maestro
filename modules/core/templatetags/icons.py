import re

from django import template
from django.contrib.staticfiles import finders
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

_icons_cache = {}

def normalize_svg(svg_text: str, classes: str = "", force_current_color: bool = True, strip_root_size: bool = True, force_inner_fill: bool = False) -> str:
    if strip_root_size:
        svg_text = re.sub(r'\s(width|height)="[^"]*"', '', svg_text, flags=re.I)

    if classes:
        if re.search(r'<svg[^>]*\bclass="', svg_text, flags=re.I):
            svg_text = re.sub(r'(<svg[^>]*\bclass=")([^"]*)"', lambda m: f'{m.group(1)}{m.group(2)} {conditional_escape(classes)}"', svg_text, count=1, flags=re.I)
        else:
            svg_text = re.sub(r'<svg\b', f'<svg class="{conditional_escape(classes)}"', svg_text, count=1, flags=re.I)

    if force_current_color:
        if not re.search(r'<svg[^>]*\bfill="', svg_text, flags=re.I):
            svg_text = re.sub(r'<svg\b', '<svg fill="currentColor"', svg_text, count=1, flags=re.I)
        if not re.search(r'<svg[^>]*\bstroke="', svg_text, flags=re.I):
            svg_text = re.sub(r'<svg\b', '<svg stroke="currentColor"', svg_text, count=1, flags=re.I)

    return svg_text

def get_svg_icon(name: str):
    if name in _icons_cache:
        return _icons_cache[name]

    file_path = finders.find(f'icons/{name}.svg')
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            _icons_cache[name] = mark_safe(f.read())
    else:
        _icons_cache[name] = None
    return _icons_cache[name]


class IconNode(template.Node):
    def __init__(self, name_expr, attrs):
        self.name_expr = name_expr
        self.attrs = attrs

    def render(self, context):
        name = str(self.name_expr.resolve(context)).strip()

        custom = False
        if "custom" in self.attrs:
            val = self.attrs["custom"].resolve(context)
            if isinstance(val, str):
                custom = val.lower() in {"true", "1", "yes"}
            else:
                custom = bool(val)

        if custom:
            svg = get_svg_icon(name)
            if svg:
                base_class = ""
                if "class" in self.attrs:
                    base_class = str(self.attrs["class"].resolve(context)).strip()

                svg = normalize_svg(
                    svg_text=svg,
                    classes=base_class,
                    force_current_color=True,
                    strip_root_size=True,
                    force_inner_fill=False
                )
                return mark_safe(svg)

            return mark_safe(f'<span title="{name}">⍰</span>')

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
            if key in {"class", "style", "custom"}:
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
    Uso:
        {% icons "chevron-left" %}                       -> Font Awesome
        {% icons "chevron-left" custom=True %}           -> SVG from Project
        {% icons "github" style="fab" class="text-blue" %}
    """
    bits = token.split_contents()
    tag_name = bits.pop(0)
    if not bits:
        raise template.TemplateSyntaxError(f'"{tag_name}" requer ao menos o nome do ícone.')

    name_expr = parser.compile_filter(bits.pop(0))

    attrs = {}
    for bit in bits:
        if "=" not in bit:
            raise template.TemplateSyntaxError(
                f'Argumento inválido em {tag_name}: "{bit}". Use key="value".'
            )
        key, value = bit.split("=", 1)
        attrs[key] = parser.compile_filter(value)

    return IconNode(name_expr, attrs)

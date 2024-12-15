from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except (ValueError, TypeError):
        return value
    

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter
def divide(value, arg):
    return float(value) / float(arg)

@register.filter
def get_type_display(value):
    # Dictionary mapping penalty types to their display names
    penalty_type_choices = {
        'harcelement': 'Harcèlement',
        'annulation_tardive': 'Annulation Tardive',
        'point_descente_faux' : 'Point de descente incorrect',
        'nombre_places_incorrect' : 'Nombre de places incorrect',
        'disponibilite_bagages_incorrecte' : 'Disponibilité des bagages incorrecte',
        'paiement_non_effectue' : 'Paiement non effectué',

    }
    return penalty_type_choices.get(value, value)



@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter(name='star_rating')
def star_rating(value, max_stars=5):
    """
    Generate a star rating HTML string based on the given value.
    
    :param value: Numeric value to convert to stars
    :param max_stars: Maximum number of stars (default 5)
    :return: HTML string with filled and empty stars
    """
    # Ensure value is between 0 and max_stars
    value = max(0, min(float(value), max_stars))
    
    # Calculate full, half, and empty stars
    full_stars = int(value)
    half_star = 1 if value - full_stars >= 0.5 else 0
    empty_stars = max_stars - full_stars - half_star
    
    # Generate star HTML
    star_html = ''
    
    # Full stars
    star_html += '<span class="stars">'
    star_html += '<i class="fas fa-star text-warning"></i>' * full_stars
    
    # Half star
    if half_star:
        star_html += '<i class="fas fa-star-half-alt text-warning"></i>'
    
    # Empty stars
    star_html += '<i class="far fa-star text-warning"></i>' * empty_stars
    
    star_html += '</span>'
    
    return star_html
# In your app's templatetags/custom_filters.py


@register.filter
def reverse_number1(value):
    try:
        return str(value)[::-1]  # Reverse the string of the number
    except Exception:
        return value
@register.filter(name='reverse_number')
def reverse_number(value, maximum=10):
    """
    Reverses a number within a given maximum range.
    
    Example:
    - If maximum is 10 and value is 3, returns 8
    - If maximum is 10 and value is 1, returns 10
    - If maximum is 10 and value is 10, returns 1
    
    :param value: Number to be reversed
    :param maximum: Maximum range of numbers
    :return: Reversed number
    """
    try:
        value = int(value)
        return maximum - value + 1
    except (ValueError, TypeError):
        return value
    


@register.filter(name='minus')
def minus(value, subtract):
    """
    Subtracts a number from another number.
    
    :param value: Number to subtract from
    :param subtract: Number to subtract
    :return: Result of subtraction
    """
    try:
        return int(value) - int(subtract)
    except (ValueError, TypeError):
        return value

@register.filter(name='range')
def range_filter(number):
    """
    Generates a range of numbers from 0 to number-1.
    
    :param number: Upper bound of the range
    :return: Range of numbers
    """
    return range(number)



@register.filter(name='make_list')
def make_list(value):
    """
    Convert a number to a list of that length.
    
    Usage in template:
    {% for i in 10|make_list %}
        <!-- do something -->
    {% endfor %}
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return []


from django import template

register = template.Library()

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
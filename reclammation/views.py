from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReclamationForm
from .models import Reclamation

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReclamationForm


def creer_reclamation(request):
    """
    Vue pour créer une réclamation.
    Nécessite une authentification préalable.
    """
    if request.method == 'POST':
        # Passage de request.FILES pour le téléchargement de fichiers
        # Passage de l'utilisateur courant pour filtrer les groupes
        form = ReclamationForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            # Sauvegarde avec l'utilisateur connecté
            reclamation = form.save(commit=False)
            reclamation.utilisateur = request.user
            
            # Gérer le groupe si sélectionné
            if form.cleaned_data.get('groupe'):
                reclamation.groupe = form.cleaned_data['groupe']
                reclamation.statut_participation = 'groupe'
            
            reclamation.save()
            
            messages.success(request, "Votre réclamation a été soumise avec succès.")
            return render(request, 'reclamation/succes_reclamation.html', {'reclamation': reclamation})  # Assurez-vous que cette route existe
        else:
            # Messages d'erreur plus détaillés
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier les informations saisies.")
    else:
        # Passage de l'utilisateur courant pour filtrer les groupes
        form = ReclamationForm(user=request.user)
    
    return render(request, 'reclamation/reclamation_form.html', {'form': form})

# Contenu des règles générales
RULES_TEXT = """
Règlementation et Pénalités pour le Service de Covoiturage - Wasalni
Règles Générales
1. Les réclamations doivent être soumises dans les 48 heures suivant l'incident.
2. Fournir des preuves (captures d'écran, documents, etc.) est recommandé.
3. Les réclamations abusives ou non fondées peuvent entraîner des sanctions.
4. Un utilisateur peut consulter l'état de ses réclamations à tout moment.
5. Toutes les réclamations seront traitées dans un délai de 7 jours ouvrables.
Introduction
Ce document décrit les lois, conditions et conséquences liées aux infractions dans le cadre de
l'utilisation de notre service de covoiturage Wasalni.
Les règles sont mises en place pour assurer une expérience sûre, équitable et agréable pour tous
les utilisateurs.
1. Lois Générales
1. Les utilisateurs doivent respecter les règles du site, y compris la fourniture d'informations exactes.
2. Les passagers doivent arriver au point de rendez-vous à l'heure convenue.
3. Le conducteur doit assurer la sécurité des passagers et respecter le trajet convenu.
2. Pénalités et Conditions
Règlementation et Pénalités pour le Service de Covoiturage - Wasalni
Les pénalités sont appliquées en cas de violation des règles. Voici les types de pénalités :
- Annulation tardive (passager ou conducteur) :
* Condition : Annulation dans les 12 heures avant le départ.
* Conséquence : Une pénalité mineure avec une réduction de la note d'évaluation.
- Annulation sans informer :
* Condition : Non-information préalable d'une annulation.
* Conséquence : Réduction significative du score général.
- Harcèlement ou comportement inapproprié :
* Condition : Plainte confirmée via le système de réclamation, accompagnée de preuves.
* Conséquence : Suspension temporaire ou permanente du compte.
- Paiement non effectué :
* Condition : Paiement non réalisé pour un trajet confirmé.
* Conséquence : Restriction d'accès au service jusqu'à régularisation.
- Point de descente incorrect :
* Condition : Informations incorrectes concernant le point de descente.
* Conséquence : Pénalité moyenne et avertissement.
- Nombre de places incorrect :
* Condition : Déclaration erronée sur le nombre de places disponibles.
* Conséquence : Avertissement ou suspension temporaire.
Règlementation et Pénalités pour le Service de Covoiturage - Wasalni
- Disponibilité des bagages incorrecte :
* Condition : Incohérence dans les informations sur les bagages.
* Conséquence : Réduction du score d'évaluation.
- Mauvaise évaluation injustifiée :
* Condition : Une évaluation abusive pour influencer les autres utilisateurs.
* Conséquence : Avertissement ou suppression de l'évaluation concernée.
3. Processus de Réclamation
Les utilisateurs peuvent déposer une réclamation en cas de litige ou de problème avec un trajet.
Processus :
1. Soumettre une réclamation via le formulaire en ligne.
2. Fournir des preuves tangibles (captures d'écran, documents, etc.).
3. L'équipe analysera les preuves fournies et prendra une décision dans un délai de 48 heures.
4. En cas de nécessité, un email de vérification sera envoyé.
4. Conséquences sur les Évaluations
Chaque pénalité affectera directement ou indirectement la note globale de l'utilisateur :
- Une évaluation négative est ajoutée en cas de pénalité confirmée.
- Les suspensions peuvent être appliquées pour les comportements graves.
Règlementation et Pénalités pour le Service de Covoiturage - Wasalni
- Les comportements réguliers non conformes peuvent entraîner une réduction progressive du score
global.
5. Analyse et Décisions via IA
Wasalni utilise des technologies avancées d'intelligence artificielle pour analyser les données des
réclamations et des évaluations.
Cela permet de garantir des décisions justes et rapides, tout en identifiant les comportements
récurrents problématiques.
6. Sanctions Supplémentaires
- Bannissement temporaire : En cas de violations fréquentes, un utilisateur peut être suspendu pour
une période déterminée.
- Suppression de compte : Les infractions graves ou récurrentes peuvent entraîner la suppression
définitive du compte.
- Réduction de score : Toute infraction confirmée impactera le score général de l'utilisateur.
"""



def regles_generales(request):
    """
    Affiche les règles générales et permet de télécharger un PDF.
    """
    if request.GET.get('download') == 'pdf':
        # Génération du PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "Règles Générales")
        lines = RULES_TEXT.splitlines()
        y = 750  # Position verticale de départ
        for line in lines:
            p.drawString(100, y, line)
            y -= 20  # Espacement entre les lignes
        p.showPage()
        p.save()
        buffer.seek(0)

        # Envoi du PDF comme réponse
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="regles_generales.pdf"'
        return response

    # Sinon, rendre la page HTML
    return render(request, 'reclamation/regles_generales.html', {'rules': RULES_TEXT})


def espace_reclamation(request):
    """
    Vue pour afficher l'espace principal des réclamations.
    """
    return render(request, 'reclamation/main_page.html')

def liste_reclamations(request):
    reclamations = Reclamation.objects.filter(utilisateur=request.user).order_by('-date_reclamation')
    return render(request, 'reclamation/liste.html', {'reclamations': reclamations})

def detail_reclamation(request, reclamation_id):
    reclamation = Reclamation.objects.filter(utilisateur=request.user).order_by('-date_reclamation').first()
    return render(request, 'reclamation/detail.html', {'reclamation': reclamation})


def delete_reclamation(request):
     reclamation = Reclamation.objects.filter(evaluateur=request.user).order_by('-date_evaluation').first()
     if reclamation is not None:
        # Supprimer l'évaluation
        reclamation.delete()

    # Rediriger vers la page d'accueil ou une autre page après suppression
     return redirect('home1')
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import datetime
import json
from io import BytesIO
from reportlab.lib.enums import TA_CENTER 
from reportlab.lib.enums import TA_JUSTIFY  # Add this line


from .models import Reclamation

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

def header_wasalni(canvas, doc):
    # Save the current state of the canvas
    canvas.saveState()
    
    # Set the background color for the header (light mauve/purple)
    canvas.setFillColor(colors.Color(0.8, 0.6, 0.8))  # RGB values for a mauve color
    canvas.rect(0, 750, 600, 50, fill=1)  # Rectangle to cover the top part with color
    
    # Set text styles
    styles = getSampleStyleSheet()
    canvas.setFont('Helvetica-Bold', 16)
    canvas.setFillColor(colors.white)  # White text for contrast
    
    # Add the title text to the header
    canvas.drawString(30, 770, "Waselni - Reclamation PDF")  # Adjust position as needed

    # Optional: Add some subtitle or description below the title
    canvas.setFont('Helvetica', 10)
    canvas.drawString(30, 755, "Some additional information or tagline here")

    # You can customize further such as adding logos or other design elements
    
    # Restore the state of the canvas
    canvas.restoreState()


@login_required
def telecharger_reclamation_pdf(request, reclamation_id):
    """
    View to download a specific reclamation in PDF format.
    Requires prior authentication with all details.
    """
    # Get the reclamation or return a 404 error
    reclamation = get_object_or_404(Reclamation, id=reclamation_id)
    
    # Check additional permissions if needed
    if reclamation.utilisateur != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You do not have permission to download this reclamation.")
    
    # Create an in-memory buffer for the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=72, 
        leftMargin=72, 
        topMargin=90,  # Increased for the header 
        bottomMargin=72
    )
    
    # Text styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        textColor=colors.HexColor('#4CAF50'),  # Green Wasalni color
        alignment=TA_CENTER
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading3'],
        textColor=colors.HexColor('#003366'),  # Dark blue
        spaceAfter=6
    )
    
    details_style = ParagraphStyle(
        'Details',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        leading=12
    )
    
    # List of elements to add to the PDF
    elements = []
    
    # Main title
    elements.append(Paragraph("Détails Complets de la Réclamation", title_style))
    elements.append(Spacer(1, 12))
    
    # Personal Information
    elements.append(Paragraph("Informations Personnelles", section_style))
    
    # Create a table for personal information
    personal_data = [
        ["Nom et Prénom", reclamation.nom_prenom],
        ["Numéro de Téléphone", reclamation.numero_telephone],
        ["Statut Personnel", reclamation.get_statut_personnel_display()],
        ["Type de Participation", reclamation.get_statut_participation_display()]
    ]
    
    personal_table = Table(personal_data, colWidths=[200, 300])
    personal_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6F2E6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(personal_table)
    elements.append(Spacer(1, 12))
    
    # Incident details
    elements.append(Paragraph("Détails de l'Incident", section_style))
    
    incident_data = [
        ["Date de l'Incident", reclamation.date_incident.strftime('%d/%m/%Y')],
        ["Heure de l'Incident", reclamation.heure_incident.strftime('%H:%M')],
        ["Lieu de l'Incident", reclamation.lieu_incident],
        ["Statut de la Réclamation", reclamation.get_statut_display()]
    ]
    
    incident_table = Table(incident_data, colWidths=[200, 300])
    incident_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6F2E6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(incident_table)
    elements.append(Spacer(1, 12))
    
    # Incident description
    elements.append(Paragraph("Description Détaillée", section_style))
    elements.append(Paragraph(reclamation.description_incident, details_style))
    elements.append(Spacer(1, 12))
    
    # Witnesses (if any)
    if reclamation.temoins:
        elements.append(Paragraph("Témoins", section_style))
        
        # Convert witnesses into list of lists
        temoins_data = [["Nom", "Contact", "Rôle"]]
        try:
            temoins = json.loads(reclamation.temoins) if isinstance(reclamation.temoins, str) else reclamation.temoins
            for temoin in temoins:
                temoins_data.append([
                    temoin.get('nom', 'N/A'),
                    temoin.get('contact', 'N/A'),
                    temoin.get('role', 'N/A')
                ])
        except (json.JSONDecodeError, TypeError):
            temoins_data.append(["Erreur de lecture des témoins", "", ""])
        
        temoins_table = Table(temoins_data, colWidths=[200, 150, 150])
        temoins_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6F2E6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(temoins_table)
        elements.append(Spacer(1, 12))
    
    # Group information (if applicable)
    if reclamation.groupe:
        elements.append(Paragraph("Informations de Groupe", section_style))
        group_data = [
            ["Nom du Groupe", reclamation.groupe.nom],
            # Add any other relevant group fields
        ]
        
        group_table = Table(group_data, colWidths=[200, 300])
        group_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6F2E6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(group_table)
        elements.append(Spacer(1, 12))
    
    # Additional information
    additional_info = [
        ["Date de Réclamation", reclamation.date_reclamation.strftime('%d/%m/%Y %H:%M')]
    ]
    
    if reclamation.preuve:
        additional_info.append(["Preuve Jointe", reclamation.preuve.name])
    
    additional_table = Table(additional_info, colWidths=[200, 300])
    additional_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6F2E6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(additional_table)
    
    # Footer function
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(colors.gray)
        # Footer text
        canvas.drawString(
            doc.leftMargin,
            0.5 * inch,
            f"Document généré automatiquement par Wasalni - {datetime.date.today().strftime('%d/%m/%Y')}"
        )
        # Page number
        canvas.drawRightString(
            doc.width + doc.leftMargin + doc.rightMargin,
            0.5 * inch,
            f"Page {doc.page}"
        )
        canvas.restoreState()
    
    # Attach header and footer to the document
    doc.build(elements, onFirstPage=header_wasalni, onLaterPages=footer)
    
    # Get the PDF value from the buffer
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    
    # Return the PDF as a response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reclamation_{reclamation.id}.pdf"'
    response.write(pdf)
    return response

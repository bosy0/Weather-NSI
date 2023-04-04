'''
                      [LIFESCORE.PY]
                 CODE PRINCIPAL DE LIFE-SCORE
Syntaxe de nos variables : 
    - Les boutons s'écrivent btn_NOM
    - Les fenêtres s'écrivent windowNOM
    - Les textes (classe interface.CTkLabel) s'écrivent msg_NOM
    - Les listes s'écrivent list_NOM
    - Les dictionnaires s'écrivent dico_NOM

Pour tous les widgets du code, leurs création dépendait de notre mémoire sur Tkinter et de la documentation sur CustomTkinter 
'https://github.com/TomSchimansky/CustomTkinter/wiki/'
Les valeurs (de taille, de police, de couleur,... ont été trouvées après plusieurs essais par nous même)
De même pour les placements, nos connaissances de Tkinter nous ont permis de retrouver certaines méthodes avec des arguments précis (.place(relx et rely))
'''



# Bibliothèques essentielles pour la mise à jour des autres bibliothèques
import subprocess
import sys
import os





# Message de bienvenue sur le terminal
print(  "####################################################",
      "\n##                   LIFE-SCORE                   ##",
      "\n##              Terminal de débogage              ##",
      "\n####################################################\n\n",)










'''
MODULE DE MISE A JOUR DES BIBLIOTHEQUES

- Idée de Nathan
- Réalisé par Thor
- Redémarrage requis par Nathan
'''

# Message sur le terminal
print(  "################################",
      "\n##  Installation des modules  ##",
      "\n################################\n\n",)

# Verifie si tout les modules dans requirements.txt sont present, sinon ils sont installés.
nouvelle_bibliotheque = False
nom_du_repertoire = os.path.dirname(__file__) # Cherche le chemin du repertoire courant

# Liste des modules deja installé
list_pip = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE).stdout.decode("utf-8")

# On installe tous les modules individuellement pour pouvoir les afficher un par un
for module in open(os.path.join(nom_du_repertoire,os.pardir, "requirements.txt"), "r").readlines(): # os.pardir équivaut à ../ en linux
    moduleSeul = module.split(">")[0] # Format module>=x.x.x

    if moduleSeul + "==" in list_pip:
        print(moduleSeul, "-> Module présent")
    else: 
        print(moduleSeul, "-> Module installé")
        output = subprocess.run([sys.executable, "-m", "pip", "install", module], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
        nouvelle_bibliotheque = True

        if output == "": # output == "" quand il y a une erreur d'installation
            raise ConnectionError("Erreur de connection, verifiez votre connection d'internet!")


# Pour éviter de lancer le programme sans avoir bien installé les bibliothèques - Fait par Nathan
if nouvelle_bibliotheque == True :
    print("\n\n\n\n\n********************\n[ATTENTION]\nVeuillez redémarrer le programme pour appliquer l'instation des bibliothèques.\n\n********************\n\n\n\n\n")

    sys.exit(os.system(f"{sys.executable} ./LifeSCORE.py"))
print("\n\n")



'''
BIBLIOTHEQUES

'''
# Nos autres fichiers
import update # Importe les fonctions et met à jour les modules en meme temps
from classes import * # Import de nos classes créées

# Interface graphique
from tkinter import * # On utilise certaines fonctions de Tkinter avec Customtkinter
import customtkinter as interface # On utilisera Customtkinter principalement pour le style
from tkintermapview import TkinterMapView # Pour les cartes de la ville
import tkinter.font # Permet d'avoir accès à plusieurs polices d'écritures pour les textes
from PIL import Image # pour les logos et les boutons de CTK

# Lecture de données (csv)
import pandas
import csv
import math

# Autre(s)
from time import sleep, strftime, localtime # Sleep met en pause le programme, strftime convertit le temps et localtime redonne le temps de l'ordinateur

'''
VARIABLES GLOBALES (utilisées à travers plusieurs fonctions)

- Idée de Raphaël (au fur et à mesure que le code avançait, plusieurs variables ont été ajoutées)
'''
global msg_principal        # STR | On pose les questions a travers ce texte
global list_Questions       # LIST | Les valeurs de ce tableau sont les questions 
global dico_Reponses        # DICT | Dictionnaire de 0 et de 1 pour thor type {Q1:1,Q2,:0,Q3:0,...}(0 sera souvent un vieu/calme/fermier,...)
global n                    # INT | Pour faire list_Questions[n]
global btn_ok               # CTkButton | Boutton qui continue (est utilisé plusieurs fois d'où la variable globale) 
global Donnees_ville        # Donnees | Ce que l'on va traiter grâce aux autres fichiers
global erreur_maj           # Bool | Pour savoir si le téléchargement à causé des problèmes
global icone                # PhotoImage | Prend les données du logo en png pour l'afficher sur chaques pages

# Variables globales pour la nouvelle version de UPDATE - Idee de rendre ces variables globales de Nathan 
global progressbar          # CTkProgressbar | Montre l'avancée visuelle du téléchargement
global msg_aide             # STR | Renvoie l'avancée du téléchargement
global message_pourcentage  # STR | Renvoie l'avancée du téléchargement



# initialisations des images des boutons, fait par Nathan
images_boutons =nom_du_repertoire+'/systeme/icones/'

image_btn_chercher = interface.CTkImage(light_image=Image.open(images_boutons+'chercher.png'),
                                size=(50, 50))

image_btn_quitter = interface.CTkImage(light_image=Image.open(images_boutons+'fermer.png'),
                                size=(100, 100))

image_btn_parametres = interface.CTkImage(light_image=Image.open(images_boutons+'parametres.png'),
                                size=(100, 100))

image_btn_aide = interface.CTkImage(light_image=Image.open(images_boutons+'aide.png'),
                                size=(100, 100))






# Constantes (les questions sont aussi de nous)
repertoire_donnees = os.path.join(nom_du_repertoire+'/donnees') # Retourne le chemin vers le dossier 'donnees'
n = 0
list_Questions = [('Aimez vous sortir en ville ?','Activite'),           # Reproduire les questions dans le même style que la première
                ('Etes vous etudiant ?','Scolarite'),                
                ('La culture a-t-elle une place importante pour vous ?','Culture'),
                ('préférez vous la ville à la campagne ?','Citadin'),
                ("Etes vous en recherche d'emploi ?","Cherche_Emploi"),
                ("Etes vous dans une situation précaire ?","Precarite")]


dico_Reponses = {} # Traité dans coefficients.py

#icone = interface.CTkImage(light_image=Image.open(nom_du_repertoire+'/systeme/icones//logo.png'))





'''
Système de compatiblité Windows / Linux
pour les polices d'écritures & l'interface
fait par Nathan
'''

import platform
systeme_exploitation = platform.system()

if systeme_exploitation == 'Linux' :
    polices = ['Ubuntu',
               'Ubuntu']
    
else :
    polices = ['Arial',
               'Arial Black']







'''
FONCTIONS
'''
def telechargement(bouton,fenetre):
    '''
    Fonction qui lance le téléchargement à l'appui du boutton (et affiche la barre de progression)
    Puis renvoie sur le qcm ou la suite du programme

    - Page calquée sur les autres pages d'aides vues plus loin par Raphaël
    '''
    
    global erreur_maj
    change_etat_btn(bouton) # Bloque le bouton sur la page principale
    
    # Initialisation de la page
    windowDownload = interface.CTkToplevel() # Fenetre supplémentairz de tkinter
    windowDownload.title('LifeScore  |  Téléchargement')
    windowDownload.iconphoto(False, icone)
    windowDownload.minsize(width=int(510*4/3), height=384)
    windowDownload.focus() # Ajout de cette ligne pour éviter qur ça passe derrière la page principale
    windowDownload.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowDownload,bouton)) # Qu'on clique sur le btn_ok ou qu'on ferme la page on obtient le même résultat
    

    # Création des widgets
    msg_aide = interface.CTkLabel(windowDownload, text="Lancement de la vérification...", width = 1000, font =(polices[0],16), justify=LEFT)
    message_pourcentage = interface.CTkLabel(windowDownload, text="0%", width = 1000, font =(polices[0],12), justify=LEFT)
    progressbar = interface.CTkProgressBar(windowDownload,mode = 'determinate')
    progressbar.set(0)

    # Placements des widgets
    msg_aide.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    progressbar.place(relx=0.5,rely=0.6,anchor = CENTER)
    message_pourcentage.place(relx=0.5,rely=0.65,anchor = CENTER)    
    
    windowDownload.update()
    
    # Décide ensuite quelle action faire
    erreur_maj = update.executer(progressbar,windowDownload,msg_aide,message_pourcentage)
    if not erreur_maj:
        #print(len(lire_option("REPONSE_QCM")),len(list_Questions))
        retour_pages(windowDownload,bouton)
        if len(lire_option("REPONSE_QCM")) == len(list_Questions): # Si les données du questionnaires ont déja été remplies
            w_qcm(fenetre,option ="sans_qcm")
        else: # Si les données ne sont pas toutes présentes (on lance le questionnaire)
            w_qcm(fenetre)
    else: # Fenetre d'erreur en cas d'erreur dans le téléchargement
        retour_pages(windowDownload,bouton)
        w_erreur(fenetre)
        
    windowDownload.mainloop()



'''
FONCTIONS UTILISEES PLUSIEURS FOIS

'''
def efface_fenetre(fenetre,option="Classique"): # "Classique" est une valeur de base pour garder certains widgets
    """
    Fonction qui efface tous les widgets d'une fenêtre à l'autre pour pouvoir afficher d'autres choses

    - winfo_children() a été pris dans la documentation de Tkinter, les noms ont été trouvé par print() et tests par Raphaël
    """
    if option == "Classique": # On veut garder le logo, le bouton qui ouvre la page de paramètres et les pages d'aides
        for widget in fenetre.winfo_children():

            if str(widget) not in ['.!ctkbutton5','.!ctkbutton4','.!ctkbutton2','.!ctkbutton3'] and "toplevel" not in str(widget):
                widget.destroy() # .destroy() supprime le widget

    else: # On veut juste garder le logo
        for widget in fenetre.winfo_children():

            if str(widget) not in ['.!ctkbutton5','.!ctkbutton2','.!ctkbutton3'] : # Le nom du bouton où l'on met le logo (non modifiable)
                widget.destroy()


def avancer(fenetre): 
    global msg_principal
    global n # n += 1 à chaques questions
    """
    Passe à la question 1, ouvre le qcm et ajoute les deux boutons Non et Oui.
    
    Si le qcm est terminé, ouvre la seconde page

    - Idée d'utilisation des variables globales n et du message principal par Raphaël
    """
    if n != len(list_Questions):
        btn_ok.place_forget() # Le cache le temps du lancement de cette fonction
        # Création des boutons
        btn_gauche = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), command=lambda: plus(btn_gauche,btn_droite,0), text="Non",font=(polices[0],30, 'bold'))
        btn_droite = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), command=lambda: plus(btn_gauche,btn_droite,1), text="Oui",font=(polices[0],30, 'bold'))
        
        # Placements et Modifications
        btn_gauche.place(relx=0.40,rely=0.5,anchor=CENTER)
        btn_droite.place(relx=0.60,rely=0.5,anchor=CENTER)
        msg_principal.configure(text =f'{list_Questions[n][0]}') # Affiche la premiere question
    else:
        efface_fenetre(fenetre,"Efface_reste")    
        w_question(fenetre) # Ouvre la seconde page : Fin de la première


def plus(b1,b2,arg):
    '''
    Ajoute 0 ou 1 au dico de reponses (respectivement Non et Oui) En fonction de l'argument
    et passe à la question suivante

    - Idee personnelle (On avait avant une fonction plus0 et plus1, on les a combinés pour éviter la redondance) par Raphaël
    '''
    global list_Questions
    global n
    global dico_Reponses
    global msg_principal

    
    
    dico_Reponses[list_Questions[n][1]] = arg
    n +=1
    if not est_termine(b1,b2):
        msg_principal.configure(text = list_Questions[n][0])
        
    #print(n, dico_Reponses, list_Questions[n-1][1], arg) # print pour tester bug dico


def est_termine(btn_1,btn_2):
    global msg_principal
    global btn_ok
    '''
    Verifie si le QCM est terminé (dernière question répondue). Si c'est le cas, On affiche un message puis retour bouton ok 

    - Idee de Raphaël et Nathan pour terminer le qcm (une simple recherche sur les longueurs suffit)
    '''
    if n >= len(list_Questions):
        btn_1.destroy()
        btn_2.destroy()
        btn_ok.place(relx=0.5,rely=0.5,anchor =CENTER)
        msg_principal.configure(text = "Merci d'avoir répondu aux questions, Veuillez continuer")
        changer_option("REPONSE_QCM", dico_Reponses)# Rajoute les lignes au option reponses_qcm dès qu'on quitte la page de QCM
        btn_ok.configure(text="Lancer la recherche")
        return True


def retour_pages(window,btn,cle=True):
    """
    Fonction qui passe de la page actuelle à la page N°x

    - Idee de la clé de Raphaël pour pouvoir appeler cette fonction à plusieurs reprises avec des cas différents
    """
    
    if cle==True : # Si on a juste une page d'aide
        window.destroy()
        change_etat_btn(btn)
    else:
        efface_fenetre(window)
        w_question(window)


def change_etat_btn(bouton):
    '''
    Fonction qui change l'état du bouton utilisé

    - Nécessité de se renseigner sur la documentation de CustomTkinter par Tom Schimansky 
    'https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton'
    '''
    try :
        if bouton  and bouton.cget("state") == NORMAL : # Récupère l'attribut et le change
            bouton.configure(state=DISABLED)
        else:
            bouton.configure(state=NORMAL)
    except TclError: # SI le boutton n'existe plus
        return None



'''
FONCTIONS PRICIPALES
'''
# Premiere page
def w_qcm(win,option = None): # w pour window
    """
    Affiche la premiere page :
        - Si le dico REPONSE_QCM dans ./donnees/options.txt est incomplet ou vide, lance le Qcm
        - Sinon (les données sont présentes), propose de passer à la suite (fin du Qcm)

    - L'idée du Questionnaire nous est venu après une discussion entre les membres et le professeur sur un moyen de rendre 
    l'expérience unique à l'utilisateur
    Cette fenêtre était la première créée dans notre programme, cette fonction ne crée plus la fenêtre désormais
    """
    # initialisation des variables utilisées
    global msg_principal
    global btn_ok
    global list_Questions
    global n
    n = len(list_Questions) 
    
    efface_fenetre(win) # efface tout ce qui était déja présent pour rajouter ce qui nous intéresse
    
    # Création des widgets :

    msg_principal = interface.CTkLabel(win, text="Les données utilisateur sont présentes, veuillez continuer.", width = 1000, font =(polices[0],18), justify=CENTER)

    
    # Boutton :
    btn_ok = interface.CTkButton(win, height=int(win.winfo_screenheight()/10), command=lambda: avancer(win), text="Lancer la recherche",font=(polices[0],30, 'bold'),image=image_btn_chercher) # Commence le Qcm ou continue le programme

    # Placement des widgets :

    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) # anchor place relativement à un point (ici le centre) et relx/rely place avec un % de x et de y de ce point
    # bouton ok Qui continue après le premier message
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) # place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)        




    if option == None :
        msg_principal.configure(text = "Bienvenue !  Nous allons commencer par une étude de vos préférences.")
        btn_ok.configure(text = "Lancer Le Questionnaire")
        n = 0

    win.mainloop() # pour fermer la fenetre


def info(btn):

    """
    Ouvre Une fenêtre d'informations avec un texte*

    - Pour la TextBox, ce code python de Tom Schimansky nous a aidé à la reproduire
    'https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py'
    le reste vient de Raphaël
    """
    # Constante 
    texte_info=("Bonjour ! Voilà notre protoype de LifeScore où vous pourrez visualiser la note de villes."
    + " Pour commencer, nous réalisons un QCM de 8 questions afin de déterminer vos préférences."
    + " Pour chaques critères, on définit une note sur 100 ainsi qu'un coefficient propre à lui même. "
    + " Le plus de critères sont réunis afin d'avoir le plus de précision possible. "
    + "\n\nIls sont répartis en 4 catégories :"
    + "\n   - Le climat (pluie par an / pollution de l'air / température / vent / ...)"
    + "\n   - La qualité de vie (activités / patrimoine / ville fleurie / ...)"
    + "\n   - Le coût (essence / gaz / loyer / prix de la vie / salaire moyen / ...)"
    + "\n   - La sécurité (taux d'accidents / vols / risques / ...)" #Pour une meilleure clarté du code j'écrit ce str ainsi
    + "\n\nCeci n'est qu'un prototype et certaines communes (très peu d'habitants) peuvent ne pas apparaître à cause du manque de données. ")

    # Initialisation de la page
    change_etat_btn(btn)
    windowInfo = interface.CTkToplevel() # fenetre de tkinter
    windowInfo.title('LifeScore  |  Informations')
    windowInfo.iconphoto(False, icone)
    windowInfo.minsize(width=int(510*4/3), height=384) # 768

    # Création des widgets
    txt_info = interface.CTkTextbox(windowInfo, width = 580 , corner_radius=0,border_width=2,border_color='grey')
    txt_info.insert("0.0", text = texte_info)
    txt_info.configure(state = "disabled", font = (polices[0],18),
                       wrap="word") # disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_compris = interface.CTkButton(windowInfo, height=int(windowInfo.winfo_screenheight()/10), command=lambda:retour_pages(windowInfo,btn), text="Compris",font=(polices[0],30, 'bold'))

    # Placement des widgets
    txt_info.place(relx=0.05,rely=0.05)
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)

    # Protocole de fermeture
    windowInfo.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowInfo,btn)) 

    windowInfo.mainloop()


def parametres(bouton):
    """
    Fonction qui ouvre la page de paramètres avec dessus : (X  = pas fait, A = à Améliorer, V = fait)
        -Option pour modifier la fréquence de mises à jour              V
        -Volet pour changer le style de l'application                   V 
        -Un bouton pour fermer la page                                  V
        -Suprimmer donnes d'utilisateur                                 V

    - Idee de Nathan et Raphaël, application CTk par Raphaël et application des fréquences de MaJ par Thor & Nathan

    """
    change_etat_btn(bouton) # Bloque le bouton paramètre sur la page principale jusqu'à que cell-ci soit fermée
    
    # Création de la fenêtre
    
    windowParam = interface.CTkToplevel()
    windowParam.title('LifeScore  |  Paramètres')
    windowParam.iconphoto(False, icone)
    windowParam.geometry("680x650") # 768
    windowParam.resizable(False, False)

    # Création des widgets :

    # Tous les messages présents :
    msg_titre = interface.CTkLabel(windowParam, text="PARAMÈTRES", font= (polices[1], 40, 'bold'), text_color="#29A272")
    msg_frequence = interface.CTkLabel(windowParam, text="FRÉQUENCE DE MISE À JOUR", font= (polices[0], 25), text_color="#29A272")
    msg_verif = interface.CTkLabel(windowParam, text=f"Dernière Vérification: {date_derniere_verification()}", font= (polices[0], 16), text_color="#646464")
    msg_apparence = interface.CTkLabel(windowParam, text="APPARENCE DE L'APPLICATION", font= (polices[0], 25), text_color="#29A272")
    msg_donnees = interface.CTkLabel(windowParam, text="DONNÉES UTILISATEUR", font= (polices[0], 25), text_color="#29A272")
    message = interface.CTkLabel(windowParam,text="Le bouton de suppression des données fermera le programme.", width = 50, font =(polices[0],18)) # font = taille + police, justify comme sur word

    # Tous les boutons présents :
    btn_confirm_frequence = interface.CTkButton(windowParam, width = 7, 
                                            command=lambda:changer_option("FREQ_MAJ", round(abs(float(entree_frequence_maj.get()))*86400),message)
                                            if est_nombre(entree_frequence_maj.get()) \
                                            else message.configure(text = "Vous devez entrer un nombre !"), # / permet un retour à la ligne dans le code
                                            text="Confirmer") # changer_option() se trouve dans classes.py
    btn_supprimer_donnees = interface.CTkButton(windowParam, width = 134, height = 42,
                                                command=supprimer_donnees_utilisateur,
                                                text="SUPPRIMER",
                                                font=(polices[0], 18))
    btn_changements = interface.CTkButton(windowParam,height=60,
                                                        width=550,  
                                                        command=lambda:retour_pages(windowParam,bouton), 
                                                        text="FERMER LA PAGE",
                                                        font=(polices[0],30, 'bold'))
    
    # Autres (les entrées et les volets "switch") :
    
    # Pour récuperer la fréquence des màj et le transformer en jours
    frequence_maj = int(lire_option('FREQ_MAJ')/86400)
    
    entree_frequence_maj = interface.CTkEntry(windowParam, placeholder_text=frequence_maj, width=51, font= (polices[0], 18))
    switch_apparence = interface.CTkOptionMenu(windowParam, values=["Système", "Sombre", "Clair"],command=change_apparence_page)

    # Traduction en direct, pour voir directement quel mode on a selectioné 
    apparence = lire_option("APPARENCE")
    if apparence == "System" : apparence = "Système"
    elif apparence == "Light" : apparence = "Clair"
    elif apparence == "Dark" : apparence = "Sombre"
    
    switch_apparence.set(apparence) # La valeur initiale (à titre indicatif) 


    # Placement des widgets (Dans l'ordre dans lequel ils sont affichés) :
    
    msg_titre.place(relx=0.5, rely=0.064, anchor = CENTER)

    # La fréquence de mise à jour
    msg_frequence.place(relx = 0.02, rely = 0.15)
    entree_frequence_maj.place(relx = 0.06, rely = 0.20)
    btn_confirm_frequence.place(relx = 0.195, rely = 0.22, anchor = CENTER)
    msg_verif.place(relx=0.06, rely=0.24)

    # L'apparence de l'application 
    msg_apparence.place(relx = 0.02, rely = 0.33)
    switch_apparence.place(relx = 0.06, rely = 0.38)

    # La suppression des données 
    msg_donnees.place(relx=0.02, rely=0.51)
    btn_supprimer_donnees.place(relx=0.06, rely=0.56)

    # Fin de la page
    message.place(relx=0.5,rely=0.75,anchor = CENTER)
    btn_changements.place(relx = 0.5, rely = 0.87, anchor = CENTER)

    windowParam.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowParam,bouton))# Meme effet que le bouton sauf que c'est si on ferme la page manuellement
    windowParam.mainloop()


def date_derniere_verification() -> str:
    '''
    Retourne la date formatée de la dernière mise à jour
    
    - Idee de Thor avec la documentation du module Time 'https://docs.python.org/3/library/time.html'
    '''
    derniere_maj_sec = lire_option("DERNIERE_MAJ") # Cette fonction provient de classes.py
    if derniere_maj_sec == 0 :
        return "Aucune vérification."
    return strftime("%d/%m/%Y", localtime(derniere_maj_sec)) # Formate la donnée en jour mois année, heure minute


def supprimer_donnees_utilisateur():
    '''
    Efface les choix de qcm dans le fichier ./donnees/options.txt
    (Si l'utilisateur souhaite refaire le questionnaire)

    - Idee de Thor
    '''
    changer_option("REPONSE_QCM", {}) # remet les choix du qcm a vide (donc on devra le refaire)
    sys.exit() # Ferme le programme pour éviter de potentielles erreurs


def change_apparence_page(choix):
    '''
    Change l'apparence de l'interface (Sombre ou Clair)
    (Système revient à ce que l'ordinateur a pour valeur par défault)

    - Idee de transformation du texte et de l'écriture par Raphaël
    '''

    if choix in ["Système","Sombre","Clair"] : # Si on veut changer les pages
        if choix == "Système": choix = "System"
        elif choix == "Sombre": choix = "Dark"
        else:choix = "Light"

        changer_option('APPARENCE', choix)
        interface.set_appearance_mode(choix)




# Seconde page
def w_question(fenetre):
    '''
    Affiche la seconde page qui contient la requête de la ville

    - Léger calque sur w_qcm()
    '''
    fenetre.title('LifeScore  |  Requête de la commune') # Changement du titre de la fenêtre
    fenetre.iconphoto(False, icone)

    """fenetre.bind('<Return>', lambda:ville(entree,msg_ville,fenetre))
    fenetre.update()"""

    # Création des widgets
    entree = interface.CTkEntry(fenetre,placeholder_text="ex : Puissalicon ",width=int(500/3), font = (polices[0],18))
    msg_ville= interface.CTkLabel(fenetre, text="Veuillez saisir la ville recherchée", width = 1000, font =(polices[0],20), 
                                  justify=CENTER) # font = taille + police, justify comme sur word
    btn_arrondissement = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda: arrondissement(btn_arrondissement), 
                                             text="",font=(polices[0],30, 'bold'),image=image_btn_aide, fg_color='transparent',hover = False) # Boutton d'aide arrondissements
    btn_entree = interface.CTkButton(fenetre,height=int(fenetre.winfo_screenheight()/10), 
                                     command=lambda: ville(entree,msg_ville,fenetre),text="Recherche",font=(polices[0],30, 'bold'),image=image_btn_chercher)
    
    # Placement des widgets
    msg_ville.place(relx= 0.5, rely=0.45, anchor = CENTER)
    entree.place(relx=0.5, rely= 0.55, anchor=CENTER)
    btn_entree.place(relx=0.5, rely= 0.65, anchor = CENTER)
    btn_arrondissement.place(relx=0.9, rely=0.05 ,anchor = NE)


def arrondissement(btn):

    '''
    Ouvre Une fenêtre d'aide avec un texte et un bouton de retour

    - Copie de la fonction aide() remaniée pour les arrondissements par Raphaël 
    '''
    # Initialisation
    windowAide = interface.CTkToplevel()
    windowAide.title('LifeScore  |  Aide')
    windowAide.iconphoto(False, icone)
    windowAide.minsize(width=int(510*4/3), height=384)

    change_etat_btn(btn) # Bloque le bouton d'accès à cette page
    texte_aide=("Si Votre ville possède plusieurs arrondissemnts (ex : Paris) :"
    + "\n     - Si vous saisissez uniquement le nom de la ville, le premier            arrondissement sera pris comme base"
    + "\n     - Sinon, écrivez le nom de la ville comme cela : \n\n           Nom 1er Arrondissement / Nom Ne Arrondissement (ex : Paris 2e Arrondissement)")

    # Création des widgets
    txt_aide = interface.CTkTextbox(windowAide, width = 580 , corner_radius=0)
    txt_aide.insert("0.0", text = texte_aide)
    txt_aide.configure(state = "disabled", font = (polices[0],18),wrap="word") # disabled pour pas qu'on puisse écrire, "word" pour le retour a la ligne
    btn_compris = interface.CTkButton(windowAide, height=int(windowAide.winfo_screenheight()/10), command=lambda :retour_pages(windowAide,btn), text="Compris",font=(polices[0],30, 'bold'))
    
    
    # Placement des widgets
    txt_aide.place(relx=0.05,rely=0.05)
    btn_compris.place(relx = 0.5, rely = 0.7, anchor = CENTER)

    # Protocole de fermeture de page
    windowAide.protocol("WM_DELETE_WINDOW", lambda:retour_pages(windowAide,btn))
    windowAide.mainloop()





def ville(entree,msg,fenetre):

    '''
    Récupère l'entrée, vérifie si la ville existe bien:
        -Si oui, continue vers la page 3
        -Si non, affiche un message d'erreur
    
        - L'idée de créer une classe de Donnees est détaillée dans classes.py , le reste est de Raphaël
    '''
    global Donnees_ville
    ville = entree.get()
    Donnees_ville = Donnees(ville)
    if Donnees_ville.is_commune_france(msg):
        
        msg.configure(text = "Veuillez patienter ...") #Ne se voit même pas mais peut être remarqué si les calculs sont longs
        #fonction_barre_chargement = threading.Thread(target=chargement, args=(fenetre,))
        #fonction_barre_chargement.run()
        fenetre.config(cursor="arrow")
        fenetre.update()
        #Donnees_ville.note_par_habitants('sport_test.csv',['ComInsee','Nombre_equipements'],[16071.4,-3.57143],',') # Fonction présente dans classes.py
        efface_fenetre(fenetre,"Efface_reste") # Enlève même le bouton paramètre et les pages d'aide pour ne pas obstruer l'écran
        
        w_score(Donnees_ville,fenetre)






# troisieme page
def w_score(ville,win):
    '''
    affiche la dernière page qui contient le score et le bouton pour revenir
    ville est un objet de la classe Donnees précédemment créé après avoirs appuyé sur recherche

    - Reprise de w_qcm() et w_question() remaniée par Raphaël, la carte est de Thor avec l'api 'https://mt0.google.com'
    '''
    
    # Initialisation 
    win.title(f'LifeScore  |  Commune de {str(ville).capitalize()}')
    # Données PROVISOIRES !!!
    score = Donnees_ville.note_finale()
    dico = Donnees_ville.notes_finales # Un dictionnaire
    bonus,malus = avantages_inconvenients(dico) # Fonction non terminée (besoin du fichier qui fait les données)
    
    print(dico, "\n\n\n\n\n")

    # Transformation des données en texte
    msg_ville = interface.CTkLabel(win,text=str(ville).capitalize(), width = 500, font=(polices[1],taille_police(str(ville)), 'bold'), justify=CENTER)# TODO fix temporaire qui aggrandit de 2.5 pour les grosses ville à rajouter, une fonction inverse pour la taille
    msg_ville.place(relx=0.5,rely=0.1,anchor=CENTER)
    plus, moins = plus_et_moins(bonus,malus) # Récupère les données et les transforme en 2 str à Afficher
    
    # Carte de la commune 
    """
    CARTE DU VILLE

    - Source et documentation: https://github.com/TomSchimansky/TkinterMapView (la liste des cartes possibles est tout en bas du README)
    - Idée de Nathan, implémenté par Thor
    """
    if is_connected("https://mt0.google.com/"): # On verifie qu'il y a un connection au server ou on va recuperer la carte

        carte_ville = TkinterMapView(win, width=0.4*win.winfo_width(), height=0.4*win.winfo_height()) # On declare l'objet de la carte avec ces tailles respectives
        carte_ville.set_address(f"{str(ville)[:-1] if est_nombre(str(ville)[-1]) else str(ville)}, France", marker=True,text=str(ville)) # Insère la ville pour l'adresse (et format pour les arrondissements)
        carte_ville.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=22) # On decide quel carte et zoom on va utiliser
        carte_ville.place(relx=0.3, rely=0.18)
    else:
        win.iconphoto(False, icone_connexion) # Affiche l'icone d'erreur
    


    '''
    ANIMATION DU SCORE FINAL
    
    - Idée de Nathan détaillée dans fonction_animation_score()
    - Les avantages et inconvénients sont de Raphaël
    '''
    
    if score != 'N/A':
        
        # Transformations
        score_total_animation = int(score)
        score = str(score)
        
        # Mise en place du reste du texte, pour éviter une surcharge du nombre d'elements à rafraichir
        msg_bonus = interface.CTkLabel(win,text=plus, width = 200, font =(polices[0],23, 'bold'), justify=LEFT)
        msg_malus = interface.CTkLabel(win,text=moins, width = 200, font =(polices[0],23,'bold'), justify=LEFT)
        msg_note = interface.CTkLabel(win, text=0, text_color=couleur_score(0), font=(polices[1], 80, 'bold'), justify=CENTER) # On initialise

        # Placements
        msg_note.place(relx=0.9,rely=0.2, anchor=CENTER)# Nord Est
        msg_bonus.place(relx = 0.15, rely = 0.45,anchor = CENTER)
        msg_malus.place(relx=0.85,rely=0.45,anchor = CENTER)
        win.update()
        
        change_etat_btn(btn_quitter) # Pour éviter des problèmes d'animations
        change_etat_btn(btn_parametre)
        # Pour chaque entier naturel jusqu'à notre note
        for i in range(score_total_animation+1) :
                            
            couleur = couleur_score(i)

            # Informations :
            msg_annonce_note = interface.CTkLabel(win, text='Note :', font=(polices[1], 50, 'bold'), justify=CENTER)
            msg_note.configure(text=str(i), text_color=couleur)


            msg_annonce_note.place(relx=0.9,rely=0.1, anchor=CENTER)# Nord Est
            
            # Mise à jour de la page
            win.update()
            sleep(fonction_animation_score(i, score_total_animation)) 
        change_etat_btn(btn_quitter) # Pour réactiver les bouttons
        change_etat_btn(btn_parametre)
            
            

    # Si on a pas de note
    else:
        
        # Informations :
        msg_note = interface.CTkLabel(win, text=f'Note : \n' +score +'  ' ,text_color ='grey', font =(polices[1],60),
                                       justify=CENTER)
        msg_NonAttribue = interface.CTkLabel(win,text="Nous n'avons pas pu récuperer les informations de cette ville",
                                              width = 1000, font =(polices[0],30), justify=LEFT)
        
        msg_note.place(relx=0.9,rely=0.1, anchor=CENTER)# Nord Est
        msg_NonAttribue.place(relx = 0.5, rely = 0.9,anchor = CENTER)

    # Bouton retour
    btn_Retour = interface.CTkButton(win,height=int(win.winfo_screenheight()/10), command=lambda:retour_pages(win,None,False),
                                      text= "Noter une autre ville", font=(polices[0],20, "bold"),image=image_btn_chercher)
    btn_Retour.place(relx = 0.5,rely = 0.7, anchor = CENTER)
    

def taille_police(chaine):
    '''
    Fonction qui retourne une taille de police adéquate en fonction du nombre de caractères et d'une fonction f(x) = -mx+p
    idée : Raphaël avec les cours de Mathématiques et plusieurs tests sur une calculatrice graphique
    '''
    longueur = len(chaine)
    if longueur <= 4:
        return 60
    else:
        taille = 5 * (-math.log(longueur-4)+10)
    return taille


def couleur_score(note):
    '''
    Fonction qui renvoie la note en une couleur hexadécmale. Du Rouge au Vert

    - Idee de Raphaël complétée par Nathan l'idée est de modifier des valeurs de rouge et de vert en fonction de la note
    - Basé sur la fonction fonction_animation_score de Nathan
    '''
    if note != 'N/A' :
        
        if note == 0 :
            r,g,b = 100,0,0
            
        elif note <= 20:
            r = int(110 * (note/20) + 100)
            g, b = 0, 0
            
        elif note <= 60 :
            r = 210
            g = int(210 * (note-20)/40)
            b = 0
            
        else :
            r = int(210*(100-note)/40)
            g = 210
            b = 0
            
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    else :
        return '#808080'
    

def fonction_animation_score(x, total) :
    '''
    Calcule le temps entre deux entiers pour le score total (pour l'animation de la note)
    x,total sont des INT et la fonction renvoie un FLOAT pour donner la "vitesse" de changement

    - Idée et réalisation par Nathan, aidé par nos cours de mathématiques sur les fonctions et la trigo
    '''
    # Remet le total sur 100 pour avoir un ralenti à la fin de la note

    
    x = (x/total)*5
    x_pour_cos = x + 1.2
    return ((math.cos(x_pour_cos))+1.2)*0.03




def avantages_inconvenients(dic):
    '''
    Prend les 5 meilleurs aspects de la ville pour indiquer des avantages à y habiter

    - Idée de Raphaël en utilisant les algorithmes de recherche de maximum et minimum de l'année de première
    '''

    # Avantages

    liste = [''] * 10 
    cle_maxi = cle_mini = "Valeur initiale"
    
    i = j = 0

    print(dic.keys())
    while (i < 5 and i < len(dic)) or (j < 5  and j < len(dic)):
        mini = maxi = 50 # Les malus seront compris entre 0 et 50, les bonus entre 50 et 100
        
        for cle in dic.keys():
            print(cle,dic[cle],maxi,mini)
            if dic[cle] > maxi and (cle,dic[cle]) not in liste:
                maxi = dic[cle]
                cle_maxi = cle
                
            elif dic[cle] < mini and (cle,dic[cle]) not in liste:
                mini = dic[cle]
                cle_mini = cle

        liste[i], liste[-j-1] = (cle_maxi,dic[cle_maxi]), (cle_mini,dic[cle_mini])
        i += 1 # Il est interdit d'écrire i,j += 1
        j += 1
        print(liste)
                
    return liste[:4],liste[5:]


def plus_et_moins(pl,mal):
    '''
    Transforme en Str formaté les avantages et inconvénients

    - Idee de Raphaël 
    '''
    plus, moins = "Les Avantages : ", "Les Inconvénients :" # texte a retourner
    for val_plus in pl:
        plus = plus + "\n - " + val_plus[0] + f' : {int(val_plus[1])}'

    for val_moins in mal:
        moins = moins + "\n - " + val_moins[0] + f' : {int(val_moins[1])}'
        
    return plus,moins



# Page d'erreur 
def w_erreur(fenetre): # w pour window
    '''
    Affiche la page d'erreur qui signale le problème

    - Calque sur w_qcm() par Raphaël
    '''
    
    # Initialisation
    fenetre.title('LifeScore  |  Erreur')
    fenetre.iconphoto(False, icone)
    
    # Création des widgets

    msg_principal =  interface.CTkLabel(fenetre, text="Une erreur s'est produite, le programme n'a pas pu se lancer\nEssayez de vous reconnecter à internet", 
        width = 1000, font =(polices[0],18), justify=CENTER) # font = taille + police justify comme sur word
    btn_parametre = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10),command=lambda : parametres(btn_parametre), text="Paramètres",font=(polices[0],30, 'bold'))
    btn_ok = interface.CTkButton(fenetre, height=int(fenetre.winfo_screenheight()/10), command=fenetre.destroy, text="OK",font=(polices[0],30)) # Ferme la page

    # Placement des widgets
    msg_principal.place(relx= 0.5, rely=0.4, anchor = CENTER) # Anchor sert a le mettre au milieu et relx/rely le place a un % en x et en y 
    btn_parametre.place(relx=0.1, rely=0.9, anchor = SW)  
    btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) # Place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)




if not os.path.exists(repertoire_donnees):
    os.makedirs(repertoire_donnees)


'''
RECUPERATION STYLE

- Fonction lire_option fait par Thor dans classes.py

'''

# Cree les fichiers suivants et remplis par la valeur par default s'ils ne sont pas là
style = lire_option('APPARENCE')
interface.set_appearance_mode(str(style))  # Modes: system (default), light, dark
interface.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green



'''
CREATION DE La FENETRE PRINCIPALE

- Idée de Raphaël récupérée d'anciens travaux Tkinter complétés par la documentation de CustomTkinter 
'''
# Initialisation
fenetrePrincipale = interface.CTk() # fenetre de tkinter
icone = PhotoImage(file = nom_du_repertoire+'/systeme/icones/logo.png') # Icone provisoire (on doit la créer après la création de la fenêtre)
icone_connexion = PhotoImage(file = nom_du_repertoire+'/systeme/icones/pas-internet.png')

fenetrePrincipale.title('LifeScore  |  Menu principal')
fenetrePrincipale.iconphoto(False, icone)
fenetrePrincipale.minsize(width=1280  , height=848) # Taille minimum de la fenetre


#! Je dois finir la comptabilité
if systeme_exploitation == 'Windows' :
    fenetrePrincipale.state('zoomed')

else :
    fenetrePrincipale.state('normal')



credits_texte = ("                        Réalisé par :\n\n" 
+"- Nathan B    : Gestion des données, calculs & compatibilté\n" 
+"- Raphaël F   : Interface graphique          \n"
+"- Thor N        : Calcul des coefficients & API\n"
+"- Frédéric M  : Recherches pour la base de données")







# Création des widgets
btn_ok = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10), command=lambda:telechargement(btn_ok,fenetrePrincipale), text="Continuer",font=(polices[0],30, 'bold')) # appele la fonction question1
msg_principal = interface.CTkLabel(fenetrePrincipale, text="Bienvenue dans LifeScore, nous allons procéder à\nune vérification des fichiers.", width = 1000, font =(polices[0],18), justify=CENTER)
logo = interface.CTkImage(light_image=Image.open(nom_du_repertoire +'/systeme/icones/gros-logo.png'), size=(400, 200))
btn_nul = interface.CTkButton(fenetrePrincipale,image = logo,fg_color="transparent",hover = False,text =  "") # Contient le logo
btn_quitter = interface.CTkButton(fenetrePrincipale,height=int(fenetrePrincipale.winfo_screenheight()/10), command=fenetrePrincipale.destroy,
                                    text= "", font=(polices[0],30, 'bold'), image=image_btn_quitter, fg_color='transparent',hover = False)
credits = interface.CTkLabel(fenetrePrincipale, width = 450 , corner_radius=2,text = credits_texte,
                                font = (polices[0],19), pady=1,justify=LEFT)
btn_info = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10),
                                command=lambda: info(btn_info),text = '',font=(polices[0],30, 'bold'),
                                image=image_btn_aide, hover = False, fg_color='transparent') # Ouvre la page d'instructions
btn_parametre = interface.CTkButton(fenetrePrincipale, height=int(fenetrePrincipale.winfo_screenheight()/10),
                                    command=lambda : parametres(btn_parametre), text="",font=(polices[0],30, 'bold'), image=image_btn_parametres, fg_color='transparent',hover = False) # Ouvre la page de paramètres

# btn_info.bind('<Enter>',  btn_info.configure(image = (interface.CTkImage(light_image=Image.open(images_boutons+'aide.png'),
#                                 size=(100, 100)))))
# btn_info.bind('<Leave>',  btn_info.configure(image = (interface.CTkImage(light_image=Image.open(images_boutons+'test.jpg'),
#                                 size=(100, 100)))))


# Placement des widgets
btn_nul.place(relx=0.16,rely=0.16,anchor = CENTER) # Il devra rester pendant toute l'exécution du programme
btn_quitter.place(relx=0.95, rely=0.05, anchor = NE) # SouthEastaussibasster pendant toute l'exécution



# Placement des widgets
btn_nul.place(relx=0.16,rely=0.16,anchor = CENTER) # Il devra rester pendant toute l'exécution du programme
btn_quitter.place(relx=0.9, rely=0.9, anchor = SE) # Il devra aussi rester toute l'exécution
msg_principal.place(relx= 0.5, rely = 0.4,anchor = CENTER)
btn_ok.place(relx=0.5, rely=0.5,anchor=CENTER) # Place le bouton en fonction de la fenetre (quand on modifie la taille il garde sa place)        
btn_parametre.place(relx=0.1, rely=0.9, anchor = SW) # SW = SouthWest (en bas à gauche)
credits.place(relx=0.5,rely=0.9, anchor = S)
btn_info.place(relx=0.9, rely=0.05 ,anchor = NE) # NE = NorthEast (en haut à droite)

fenetrePrincipale.mainloop()

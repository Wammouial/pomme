import arborescense

if __name__ == '__main__' :
   #afficheArborescence
    print("Affiche Arborescence : ")
    normal = 4
    print(normal-1 == afficheArborescence(normal))
    
    existePas = None
    print ("Le noeud sélectionné n'existe pas" == afficheArborescence(existePas))
    
    feuille = 0
    print ("Le noeud sélectionné n'a pas de fils" == afficheArborescence(feuille))
    
    
    
    #afficheNoeud
    print("\nAffiche Noeud : ")
    print(normal == afficheNoeud(normal))
    
    print ("Le noeud sélectionné n'existe pas" == afficheNoeud(existePas))
    
    vide = 0
    print ("Le noeud sélectionné est vide" == afficheNoeud(vide))
    
    
    
    #formNoeuds
    
    #### Créer un noeud correct --> affiche noeud marche
    
    #### Créer un noeud vide --> "Veuillez remplir toutes les cases comprenants *
    
    #### MAJ noeud correctement --> affiche noeud montre un nouveau noeud
    
    #### MAJ noeud incorrectement --> "Certains champs sont incorrect"
    
    #affcihePersonnel 
    
    #### Affiche tout le monde
    
    #### Affiche avec recherche nom existant
    
    #### Affiche nom onexistant --> "Personne introuvable"
    
    #getBoss
    print("\nGet Boss : ")
    print(normal +1 == getBoss(normal))
    
    sansBoss = 0
    print(getBoss(sansBoss) is None)
    
    #AfficheBoss
    print("\nAffiche Boss :")
    print(normal+2 == afficheBoss(normal))
    
    print("Cette personne n'a pas de boss" == afficheBoss(sansBoss))
    
    #
    
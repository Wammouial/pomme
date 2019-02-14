#import BDD


def afficheArborescence(idNoeud) :
    #nodes = getAllNoeud(idNoeud)
    #if (nodes is None) :
    if(idNoeud is None) :
        return "Le noeud sélectionné n'existe pas"
    
    #Else
    #if(length(nodes) == 1) :
    if(idNoeud == 0) :
        return "Le noeud sélectionné n'a pas de fils"
    
    #Else
    #print(nodes)
    return idNoeud-1

def afficheNoeud(idNoeud) : 
    #node = getOneNoeud(idNoeud)
    #if (node is None) :
    if(idNoeud is None) :
        return "Le noeud sélectionné n'existe pas"
    
    #Else
    #if(node == 0) :
    if(idNoeud == 0) :
        return "Le noeud sélectionné est vide"
    
    #Else
    #return(node)
    return idNoeud

def formNoeud(create, champs) :
    #A faire (copier mathilde)
    return 1

def affichePersonnel() :
    #A faire (tres chiant)
    return 1

def getBoss(idPersonne) :
    #Dans la BDD
    #if (getIdBoss(idPersonne) is not None) :
    if(idPersonne > 1) :
        #return getIdBoss(idPersonne)
        return idPersonne+1
    
    return None

def afficheBoss(idPersonne) :
    if(getBoss(idPersonne) is None) :
        return "Cette personne n'a pas de boss"
    
    #return getNamePersonne(getIdBoss(idPersonne))
    return idPersonne+2

def saveBoss(idPersonne, idNoeud) :
    if (idPersonne is None) :
        return "Veuillez sélectionné un employé"
    
    if (getBoss(idPersonne) is not None) :
        return "Cet personne a déjà un boss"
    
    #if (idPersonne == Id personne qui clique)
    if (idPersonne == 0) :
        return "Cette personne ne peut pas être son propre boss"
    
    #saveNoeudBoss(idPersonne, idNoeud)
    return idPersonne+idNoeud



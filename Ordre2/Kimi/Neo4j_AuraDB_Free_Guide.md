# Neo4j AuraDB Free --- Guide de démarrage et CheatSheet

> Synthèse de la conversation.

## 1. Accéder à Aura Console

-   Console : https://console.neo4j.io
-   Se connecter avec le compte ayant créé l'instance.
-   Depuis la console :
    -   **Query** : exécuter des requêtes Cypher.
    -   **Connect** : récupérer URI, utilisateur et mot de passe.
    -   **Metrics** : consulter l'activité et le stockage.
    -   **Settings** : gérer ou supprimer l'instance.

## 2. Importer un script Cypher

### Petits scripts

Copier/coller le contenu dans **Query** puis exécuter.

### Gros scripts (recommandé)

Utiliser `cypher-shell` :

``` bash
cypher-shell \
-a neo4j+s://<instance>.databases.neo4j.io \
-u neo4j \
-p '<mot_de_passe>' \
-f import.cypher
```

### Depuis Python

Utiliser le pilote `neo4j` pour lire un fichier `.cypher` et exécuter
chaque instruction.

## 3. Visualiser le graphe

``` cypher
MATCH p=()-[]->()
RETURN p
LIMIT 100;
```

Schéma :

``` cypher
CALL db.schema.visualization();
```

Explorer :

``` cypher
MATCH (n)
RETURN n
LIMIT 100;
```

## 4. Nettoyer complètement l'environnement

Suppression de toutes les données :

``` cypher
MATCH (n)
DETACH DELETE n;
```

Vérifier :

``` cypher
MATCH (n)
RETURN count(n) AS nodes;

MATCH ()-[r]->()
RETURN count(r) AS relationships;
```

Contraintes :

``` cypher
SHOW CONSTRAINTS;
DROP CONSTRAINT nom IF EXISTS;
```

Index :

``` cypher
SHOW INDEXES;
DROP INDEX nom IF EXISTS;
```

## 5. Bonnes pratiques

-   Créer les contraintes avant les imports.
-   Importer les nœuds avant les relations.
-   Préférer `MERGE` à `CREATE` pour éviter les doublons.
-   Versionner les scripts Cypher dans Git.
-   Séparer `schema/`, `data/` et `relations/`.

## 6. Requêtes utiles

Créer :

``` cypher
CREATE (:Person {name:"Alice"});
```

Créer ou mettre à jour :

``` cypher
MERGE (p:Person {id:1})
SET p.name="Alice";
```

Compter :

``` cypher
MATCH (n)
RETURN count(n);
```

Labels :

``` cypher
CALL db.labels();
```

Relations :

``` cypher
CALL db.relationshipTypes();
```

## 7. Workflow conseillé

1.  Nettoyage (`DETACH DELETE`)
2.  Création des contraintes
3.  Création des index
4.  Import des nœuds
5.  Import des relations
6.  Vérification
7.  Visualisation

------------------------------------------------------------------------

Ce guide est adapté à un usage avec **Neo4j AuraDB Free** et des projets
Cypher versionnés.

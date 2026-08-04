Epidemiologie avec Neo4J 

## 1. Courbe épidémique — cumul de porteurs par souche dans le temps

Neo4j n'a pas de fonction de cumul native sur une série temporelle, donc on récupère les paires (souche, since) triées, puis on cumule côté client (ou avec `apoc` si tu l'as installé). Voici la version pure Cypher qui te redonne le tableau brut, prêt à cumuler dans un tableur ou un notebook :

```cypher
// Points d'infection bruts, triés par souche puis par temps
MATCH (a:Agent)-[r:CARRIES]->(s:Strain)
RETURN s.strain_id AS strain, r.since AS t, count(*) AS new_carriers
ORDER BY strain, t;
```

Si tu as APOC, tu peux obtenir directement le cumul en une requête :

```cypher
MATCH (a:Agent)-[r:CARRIES]->(s:Strain)
WITH s.strain_id AS strain, r.since AS t, count(*) AS new_carriers
ORDER BY strain, t
WITH strain, collect({t: t, n: new_carriers}) AS points
RETURN strain,
       [i IN range(0, size(points)-1) |
         {t: points[i].t,
          cumulative: apoc.coll.sum([j IN range(0, i) | points[j].n])}
       ] AS cumulative_curve
ORDER BY strain;
```

Et pour vérifier directement le moment d'extinction (corrélation avec les `Event` d'éclipse) :

```cypher
MATCH (a:Agent)-[r:CARRIES]->(s:Strain)
WHERE s.strain_id <> 'M-001'
WITH s.strain_id AS strain, max(r.since) AS last_new_carrier
MATCH (e:Event)
WHERE e.event_type CONTAINS 'ECLIPSE' OR e.description CONTAINS strain
RETURN strain, last_new_carrier, collect(e.event_id + ' @t=' + toString(e.timestamp)) AS nearby_events
ORDER BY strain;
```

## 2. Répartition zone × statut

```cypher
MATCH (a:Agent)-[:LOCATED_IN]->(z:Zone)
RETURN z.name AS zone, a.status AS status, count(*) AS n
ORDER BY zone, status;
```

Version pivotée (une ligne par zone, une colonne par statut) pour éviter de repivoter à la main :

```cypher
MATCH (a:Agent)-[:LOCATED_IN]->(z:Zone)
WITH z.name AS zone, a.status AS status, count(*) AS n
WITH zone, collect({status: status, n: n}) AS breakdown
RETURN zone,
       apoc.map.fromPairs([b IN breakdown | [b.status, b.n]]) AS status_counts
ORDER BY zone;
```

Et pour repérer directement les zones "foyers actifs" vs "cimetières mémétiques" comme on l'a fait visuellement :

```cypher
MATCH (a:Agent)-[:LOCATED_IN]->(z:Zone)
WITH z.name AS zone,
     count(*) AS total,
     count(CASE WHEN a.status IN ['EVANGELIST','RECEPTIVE'] THEN 1 END) AS active,
     count(CASE WHEN a.status = 'DISENCHANTED' THEN 1 END) AS disenchanted
RETURN zone, total, active, disenchanted,
       round(100.0 * disenchanted / total) AS pct_disenchanted
ORDER BY pct_disenchanted DESC;
```

## 3. Virulence × cohérence × influence, avec statut des porteurs silencieux

```cypher
MATCH (a:Agent)
RETURN a.id AS id,
       a.narrative_coherence AS coherence,
       a.meme_virulence AS virulence,
       a.influence_score AS influence,
       a.status AS status,
       a.is_silent_carrier AS silent,
       a.zone AS zone,
       a.guild AS guild
ORDER BY influence DESC;
```

Et la requête qui teste directement l'hypothèse de la "contagion fantôme" — comparaison statistique silencieux vs non-silencieux :

```cypher
MATCH (a:Agent)
WITH a.is_silent_carrier AS silent,
     avg(a.meme_virulence) AS avg_virulence,
     avg(a.receptivity) AS avg_receptivity,
     avg(a.influence_score) AS avg_influence,
     avg(a.narrative_coherence) AS avg_coherence,
     count(*) AS n
RETURN silent, n, avg_virulence, avg_receptivity, avg_influence, avg_coherence
ORDER BY silent DESC;
```

Enfin, pour aller plus loin que ce qu'on a vu visuellement — vérifier si les porteurs silencieux à forte influence sont concentrés dans certaines guildes ou zones (piste pour ta prochaine seed) :

```cypher
MATCH (a:Agent {is_silent_carrier: true})
WHERE a.influence_score >= 2.0
RETURN a.id, a.zone, a.guild, a.faction_id, a.influence_score, a.meme_virulence, a.glyph_symbol
ORDER BY a.influence_score DESC;
```

**Note** : les requêtes APOC (`apoc.coll.sum`, `apoc.map.fromPairs`) supposent que le plugin APOC est installé sur ton instance Neo4j — sinon les versions pures Cypher (sans agrégation cumulative/pivot automatique) suffisent, tu finis le cumul côté client comme je l'ai fait en Python.

from sqlalchemy.orm import Session
from fastapi import HTTPException
from collections import defaultdict
from server.src.models.preference_model import Ballot, PreferenceRank

# ---------------------
# 🔹 Créer un vote
# ---------------------
def create_ballot(db: Session, user_id: int, session_id: str, rankings: list[dict]) -> Ballot:
    if not rankings:
        raise HTTPException(status_code=400, detail="Classement vide.")

    # Vérifie doublons
    ranks_seen, acts_seen = set(), set()
    for r in rankings:
        if r["rank"] in ranks_seen or r["activity_id"] in acts_seen:
            raise HTTPException(status_code=400, detail="Doublon de rang ou d’activité.")
        ranks_seen.add(r["rank"])
        acts_seen.add(r["activity_id"])

    # Vérifie si l'utilisateur a déjà voté dans cette session
    existing = db.query(Ballot).filter(
        Ballot.user_id == user_id,
        Ballot.session_id == session_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vous avez déjà voté dans cette session.")

    # Crée le vote
    ballot = Ballot(user_id=user_id, session_id=session_id)
    db.add(ballot)
    db.flush()

    for r in rankings:
        db.add(PreferenceRank(ballot_id=ballot.id, activity_id=r["activity_id"], rank=r["rank"]))

    db.commit()
    db.refresh(ballot)
    return ballot


# ---------------------
# 🔹 Calcul du vainqueur Condorcet par session
# ---------------------
def compute_condorcet_winner(db: Session, session_id: str) -> dict:
    """
    Calcule le vainqueur de Condorcet pour une session donnée.
    Retourne:
    {
      "winner": <activity_id|None>,
      "pairwise": { "(a,b)": score_a_vs_b, ... }
    }
    """
    ranks = (
        db.query(PreferenceRank)
        .join(Ballot)
        .filter(Ballot.session_id == session_id)
        .all()
    )

    if not ranks:
        raise HTTPException(status_code=404, detail="Aucun vote trouvé pour cette session.")

    # Regroupe par bulletin : { ballot_id: {activity_id: rank} }
    by_ballot = defaultdict(dict)
    for r in ranks:
        by_ballot[r.ballot_id][r.activity_id] = r.rank

    # Liste unique des activités
    activity_ids = sorted({r.activity_id for r in ranks})

    # Matrice des duels
    pairwise = defaultdict(int)  # (a,b) -> nombre de bulletins où a < b
    for prefs in by_ballot.values():
        present = [aid for aid in activity_ids if aid in prefs]
        for i in range(len(present)):
            for j in range(i+1, len(present)):
                a, b = present[i], present[j]
                if prefs[a] < prefs[b]:
                    pairwise[(a, b)] += 1
                elif prefs[b] < prefs[a]:
                    pairwise[(b, a)] += 1

    # Trouver le vainqueur Condorcet (celui qui bat tous les autres)
    winner = None
    for a in activity_ids:
        wins_all = True
        for b in activity_ids:
            if a == b:
                continue
            if pairwise.get((a, b), 0) <= pairwise.get((b, a), 0):
                wins_all = False
                break
        if wins_all:
            winner = a
            break

    # Conversion en clé string pour JSON propre
    pairwise_str = {f"{a}-{b}": v for (a, b), v in pairwise.items()}

    return {"session_id": session_id, "winner": winner, "pairwise": pairwise_str}

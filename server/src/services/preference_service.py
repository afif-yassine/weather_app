from sqlalchemy.orm import Session
from fastapi import HTTPException
from collections import defaultdict
from server.src.models.preference_model import Ballot, PreferenceRank
from server.src.models.activity_model import Activity

def create_session_activities(db: Session, session_id: str, activities: list[dict]):
    for act in activities:
        db.add(Activity(name=act["name"], description=act.get("description"), session_id=session_id))
    db.commit()
    return {"message": f"{len(activities)} activités créées pour la session {session_id}"}


def create_ballot(db: Session, user_id: int, session_id: str, rankings: list[dict]) -> Ballot:
    # Vérifie si le user a déjà voté dans cette session
    existing = db.query(Ballot).filter(Ballot.user_id == user_id, Ballot.session_id == session_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vous avez déjà voté pour cette session.")

    ballot = Ballot(user_id=user_id, session_id=session_id)
    db.add(ballot)
    db.flush()

    ranks_seen, acts_seen = set(), set()
    for r in rankings:
        if r["rank"] in ranks_seen or r["activity_id"] in acts_seen:
            raise HTTPException(status_code=400, detail="Doublon de rang ou d’activité.")
        ranks_seen.add(r["rank"])
        acts_seen.add(r["activity_id"])
        db.add(PreferenceRank(ballot_id=ballot.id, activity_id=r["activity_id"], rank=r["rank"]))

    db.commit()
    db.refresh(ballot)
    return ballot


def compute_condorcet_winner(db: Session, session_id: str):
    activities = db.query(Activity).filter(Activity.session_id == session_id).all()
    activity_ids = [a.id for a in activities]
    ranks = db.query(PreferenceRank).join(Ballot).filter(Ballot.session_id == session_id).all()

    # Regroupe les préférences par vote
    by_ballot = defaultdict(dict)
    for r in ranks:
        by_ballot[r.ballot_id][r.activity_id] = r.rank

    pairwise = defaultdict(int)
    for prefs in by_ballot.values():
        present = [aid for aid in activity_ids if aid in prefs]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                a, b = present[i], present[j]
                if prefs[a] < prefs[b]:
                    pairwise[(a, b)] += 1
                elif prefs[b] < prefs[a]:
                    pairwise[(b, a)] += 1

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

    return {
        "session_id": session_id,
        "winner": winner,
        "pairwise": dict(pairwise),
    }


def attach_session_by_ids(db: Session, session_id: str, activity_ids: list[int]) -> dict:
    if not activity_ids:
        raise HTTPException(400, "activity_ids vide")

    acts = db.query(Activity).filter(Activity.id.in_(activity_ids)).all()
    if len(acts) != len(set(activity_ids)):
        missing = sorted(set(activity_ids) - {a.id for a in acts})
        raise HTTPException(400, f"Activité(s) inexistante(s): {missing}")

    # (Optionnel) Empêcher qu'une activité soit déjà dans une autre session
    clash = [a for a in acts if a.session_id and a.session_id != session_id]
    if clash:
        raise HTTPException(409, {
            "already_in_other_session": [{"id": a.id, "session_id": a.session_id} for a in clash]
        })

    for a in acts:
        a.session_id = session_id
    db.commit()

    return {"session_id": session_id, "attached_ids": [a.id for a in acts], "count": len(acts)}
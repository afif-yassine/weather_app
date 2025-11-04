from sqlalchemy.orm import Session
from fastapi import HTTPException
from collections import defaultdict
from server.src.models.preference_model import Ballot, PreferenceRank
from datetime import date as dt_date
from sqlalchemy.exc import IntegrityError

def create_ballot(db: Session, user_id: int, rankings: list[dict], context_date=None) -> Ballot:
    if not rankings:
        raise HTTPException(status_code=400, detail="Classement vide.")
    # normalise : si pas fourni, on prend aujourd’hui
    ctx = context_date.date() if hasattr(context_date, "date") else (context_date or dt_date.today())

    # check existant
    existing = db.query(Ballot).filter(Ballot.user_id == user_id, Ballot.context_date == ctx).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vous avez déjà voté pour ce jour.")

    # vérifs ranks
    ranks_seen, acts_seen = set(), set()
    for r in rankings:
        if r["rank"] in ranks_seen or r["activity_id"] in acts_seen:
            raise HTTPException(status_code=400, detail="Doublon de rang ou d’activité.")
        ranks_seen.add(r["rank"]); acts_seen.add(r["activity_id"])

    ballot = Ballot(user_id=user_id, context_date=ctx)
    db.add(ballot); db.flush()
    for r in rankings:
        db.add(PreferenceRank(ballot_id=ballot.id, activity_id=r["activity_id"], rank=r["rank"]))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Vous avez déjà voté pour ce jour.")
    db.refresh(ballot)
    return ballot

def compute_condorcet_winner(db: Session, activity_ids: list[int]) -> dict:
    if len(activity_ids) < 2:
        return {"winner": activity_ids[0] if activity_ids else None, "pairwise": {}}

    ranks = db.query(PreferenceRank).filter(PreferenceRank.activity_id.in_(activity_ids)).all()

    by_ballot = defaultdict(dict)  # ballot_id -> {activity_id: rank}
    for r in ranks:
        by_ballot[r.ballot_id][r.activity_id] = r.rank

    pairwise_counts = defaultdict(int)  # "a>b" -> count
    for prefs in by_ballot.values():
        present = [aid for aid in activity_ids if aid in prefs]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                a, b = present[i], present[j]
                if prefs[a] < prefs[b]:
                    pairwise_counts[f"{a}>{b}"] += 1
                elif prefs[b] < prefs[a]:
                    pairwise_counts[f"{b}>{a}"] += 1

    winner = None
    for a in activity_ids:
        wins_all = True
        for b in activity_ids:
            if a == b:
                continue
            ab = pairwise_counts.get(f"{a}>{b}", 0)
            ba = pairwise_counts.get(f"{b}>{a}", 0)
            if ab <= ba:
                wins_all = False
                break
        if wins_all:
            winner = a
            break

    return {"winner": winner, "pairwise": dict(pairwise_counts)}

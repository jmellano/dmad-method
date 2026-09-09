#!/usr/bin/env python3
"""Vérifie la fraîcheur des claims d'un run DMAD (phase 7, task 71).

Sans cette boucle, DMAD produit une photo qui jaunit — c'est le mécanisme même
qui a produit le legacy qu'on documente. Chaque claim porte
`freshness.verified_at_commit` et des `evidence[].ref` en `fichier:lignes` ou
`fichier#Llignes`. Ce script confronte les deux au dépôt courant.

    python3 tools/freshness.py <dossier-run> [--repo .] [--strict] [--update]

États produits (conformes à la task 71) :
  fresh    les lignes citées n'ont pas bougé
  shifted  le fichier a changé, mais pas les lignes citées
  stale    les lignes citées ont changé
  broken   le fichier n'existe plus

--update réécrit `freshness.status` dans les claims (et `verified_at_commit`
pour les seules claims `fresh`). Sortie 1 si au moins une claim est stale ou
broken et que --strict est passé.
"""
import argparse
import pathlib
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("dépendance manquante : pip install pyyaml")

REF = re.compile(r"^(?P<file>[^\s:#]+\.[A-Za-z0-9]+)(?:[:#]L?(?P<start>\d+)(?:-L?(?P<end>\d+))?)?")


def git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def parse_ref(ref):
    """`src/A.java:12-30` ou `src/A.java#L12-L30` → (fichier, début, fin)."""
    m = REF.match(ref.strip())
    if not m:
        return None, None, None
    start = int(m["start"]) if m["start"] else None
    end = int(m["end"]) if m["end"] else start
    return m["file"], start, end


def changed_lines(repo, base, path):
    """Numéros de ligne touchés dans `path` entre `base` et HEAD, côté HEAD."""
    diff = git(repo, "diff", "-U0", f"{base}..HEAD", "--", path)
    touched = set()
    for line in diff.splitlines():
        m = re.match(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if m:
            start = int(m.group(1))
            count = int(m.group(2) or 1)
            touched.update(range(start, start + max(count, 1)))
    return touched


def resolve(repo, path):
    """Un chemin complet, sinon un nom de fichier résolu via l'index git."""
    if (pathlib.Path(repo) / path).exists():
        return path
    name = path.rsplit("/", 1)[-1]
    hits = [t for t in git(repo, "ls-files").splitlines() if t.endswith("/" + name)]
    return hits[0] if len(hits) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("--repo", default=".", help="dépôt du code documenté")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--update", action="store_true")
    args = ap.parse_args()

    head = git(args.repo, "rev-parse", "HEAD")
    if not head:
        sys.exit(f"{args.repo} n'est pas un dépôt git")

    claims = sorted((args.run / "claims").glob("*.y*ml"))
    if not claims:
        print("aucune claim trouvée")
        return 0

    tally = {"fresh": 0, "shifted": 0, "stale": 0, "broken": 0}
    details = []

    for path in claims:
        claim = yaml.safe_load(path.read_text(encoding="utf-8"))
        base = (claim.get("freshness") or {}).get("verified_at_commit")
        if not base:
            details.append((path.name, "broken", "pas de verified_at_commit"))
            tally["broken"] += 1
            continue

        status, why = "fresh", ""
        for ev in claim.get("evidence", []):
            if ev.get("kind") not in ("code", "test", "schema", "migration", "config"):
                continue
            raw, start, end = parse_ref(ev.get("ref", ""))
            if not raw:
                continue
            resolved = resolve(args.repo, raw)
            if resolved is None:
                status, why = "broken", f"{raw} introuvable"
                break
            touched = changed_lines(args.repo, base, resolved)
            if not touched:
                continue
            if start is None:
                status, why = "shifted", f"{resolved} a changé (aucune ligne citée)"
                continue
            if touched & set(range(start, (end or start) + 1)):
                status, why = "stale", f"{resolved}:{start}-{end} a changé"
                break
            if status == "fresh":
                status, why = "shifted", f"{resolved} a changé hors des lignes citées"

        tally[status] += 1
        details.append((path.name, status, why))

        if args.update:
            claim.setdefault("freshness", {})["status"] = status
            if status == "fresh":
                claim["freshness"]["verified_at_commit"] = head
            path.write_text(
                yaml.safe_dump(claim, allow_unicode=True, sort_keys=False), encoding="utf-8"
            )

    icons = {"fresh": "✅", "shifted": "🔁", "stale": "⚠️ ", "broken": "❌"}
    for name, status, why in details:
        print(f"{icons[status]} {name}: {status}" + (f" — {why}" if why else ""))

    total = sum(tally.values())
    print(
        f"\n{total} claim(s) — "
        + " · ".join(f"{k} {v}" for k, v in tally.items() if v)
        + f"\nHEAD = {head[:8]}"
    )

    if tally["stale"] or tally["broken"]:
        print("\nUne claim stale ou broken doit être RELUE, pas seulement re-taguée :")
        print("le code a bougé là où reposait la preuve.")

    return 1 if args.strict and (tally["stale"] or tally["broken"]) else 0


if __name__ == "__main__":
    sys.exit(main())

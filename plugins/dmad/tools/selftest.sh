#!/usr/bin/env bash
# Selftest DMAD : prouve que les garde-fous refusent bien ce qu'ils doivent refuser.
# Un garde-fou non testé n'est pas un garde-fou.
set -uo pipefail
cd "$(dirname "$0")/.."

fail=0

echo "== 1. Les schémas sont valides (JSON Schema draft 2020-12)"
python3 - <<'PY' || fail=1
import json, glob, sys
from jsonschema import Draft202012Validator
for f in sorted(glob.glob('schemas/*.json')):
    Draft202012Validator.check_schema(json.load(open(f)))
    print(f"   ok  {f}")
PY

echo
echo "== 2. Le run de référence passe la validation"
if python3 tools/validate.py examples/atlas-billing > /dev/null; then
  echo "   ok  examples/atlas-billing"
else
  echo "   ÉCHEC : le run de référence devrait être valide"; fail=1
fi

echo
echo "== 3. Les violations connues sont TOUTES refusées (6 v0.3 + 8 v0.4)"
expected=(
  "evidence: \[\] should be non-empty"
  "confidence V sur une claim BusinessRule sans preuve exécutée"
  "intent en C sans validated_by"
  "absent du statement"
  "dépasse le plafond"
  "claim structurelle sans evidence.tool"
  # v0.4 — une décision par violation, et le message la nomme
  "D18 — artifact_version manquant au barreau 1"
  "D18 — confidence V au barreau 3"
  "D18 — contrat non résolu sans question ouverte"
  "ressemble à un identifiant de code"
  "sub_objects référence BO-FANTOME-999"
  "D17 — une SFD sans derives_from"
  "D19 — dérive de DOC-STD-FACT-001, qui n'est pas figé"
  "D20 — une SFG a pour unité"
)
out=$(python3 tools/validate.py examples/violations 2>&1)
for e in "${expected[@]}"; do
  if grep -qE "$e" <<< "$out"; then
    echo "   ok  refusé : $e"
  else
    echo "   ÉCHEC : violation non détectée : $e"; fail=1
  fi
done

echo
if [ "$fail" -eq 0 ]; then echo "✓ selftest OK"; else echo "✗ selftest en échec"; fi
exit $fail

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
echo "== 3. Les violations connues sont TOUTES refusées (6 v0.3 + 9 v0.4)"
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
  "recursive_depth 0 avec des sous-objets"
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
echo "== 4. Le corpus : les invariants v0.4 mordent sur les documents"
expected_corpus=(
  "D16 : bloc \`\`\`java"
  "D16 : bloc \`\`\`sql"
  "R1 : diagramme sans question"
  "chapitres manquants : 5"
  "bloc « Ce qui n'est pas couvert » manquant"
  "« Ce qui n'est pas couvert » est vide"
  "sans ligne de traçabilité"
  "index inverse incomplet"
  "R3 : diagramme sans marqueur de rendu"
)
out=$(python3 tools/check-corpus.py examples/violations/corpus 2>&1)
for e in "${expected_corpus[@]}"; do
  if grep -qE "$e" <<< "$out"; then
    echo "   ok  refusé : $e"
  else
    echo "   ÉCHEC : violation de corpus non détectée : $e"; fail=1
  fi
done

out=$(python3 tools/check-corpus.py examples/violations/corpus-bloque 2>&1)
if grep -qE "contradiction non résolue" <<< "$out"; then
  echo "   ok  refusé : SFG produite malgré une contradiction non résolue"
else
  echo "   ÉCHEC : la SFG aurait dû être bloquée"; fail=1
fi

out=$(python3 tools/check-corpus.py examples/violations/corpus-derive 2>&1)
if grep -qE "diverge de son plan" <<< "$out"; then
  echo "   ok  refusé : diagramme retouché après rendu"
else
  echo "   ÉCHEC : la dérive du diagramme aurait dû être détectée"; fail=1
fi

echo
echo "== 5. Les diagrammes du run de référence se rendent depuis leur plan"
if python3 tools/diagram-engine.py --all examples/atlas-billing/output \
     --thresholds examples/atlas-billing/scope.yaml > /dev/null; then
  echo "   ok  6 plans rendus sous les seuils"
else
  echo "   ÉCHEC : un plan ne se rend pas ou dépasse les seuils"; fail=1
fi

echo
echo "== 6a. Le corpus se compose depuis le bundle, et le bundle seul"
if python3 tools/okf-compose.py examples/atlas-billing/okf --all examples/atlas-billing \
     --check-only > /dev/null; then
  echo "   ok  3 documents composables, aucun concept orphelin du plan"
else
  echo "   ÉCHEC : la composition est refusée"; fail=1
fi

echo
echo "== 6. Le corpus du run de référence est conforme"
if python3 tools/check-corpus.py examples/atlas-billing > /dev/null; then
  echo "   ok  examples/atlas-billing — STD, SFD, SFG composées"
else
  echo "   ÉCHEC : le corpus du run de référence devrait être conforme"; fail=1
fi

echo
echo "== 7. La péremption remonte la cascade"
out=$(python3 tools/freshness.py examples/freshness-propagation 2>&1)
if grep -qE "DOC-SFG-PROP-001.*hérité" <<< "$out"; then
  echo "   ok  une claim périmée en STD périme jusqu'à la SFG"
else
  echo "   ÉCHEC : la propagation n'a pas atteint la SFG"; fail=1
fi
if python3 tools/freshness.py examples/atlas-billing --strict > /dev/null; then
  echo "   ok  le run de référence n'a rien de périmé"
else
  echo "   ÉCHEC : le run de référence devrait être frais"; fail=1
fi

echo
echo "== 8. La couverture se calcule"
if python3 tools/coverage.py examples/atlas-billing | grep -q "Contrats sortants résolus"; then
  echo "   ok  contrats par barreau, niveaux de preuve, corpus produit"
else
  echo "   ÉCHEC : le rapport de couverture ne se calcule pas"; fail=1
fi

echo
echo "== 9. L'evidence store s'exporte en bundle OKF conformant"
if python3 tools/okf-export.py examples/atlas-billing --out "$(mktemp -d)/okf" --check \
     --at "2026-09-08T17:00:00Z" 2>&1 | grep -q "conformant"; then
  echo "   ok  type non vide partout, aucun orphelin, aucun lien mort"
else
  echo "   ÉCHEC : le bundle exporté n'est pas conformant"; fail=1
fi

echo
if [ "$fail" -eq 0 ]; then echo "✓ selftest OK"; else echo "✗ selftest en échec"; fi
exit $fail

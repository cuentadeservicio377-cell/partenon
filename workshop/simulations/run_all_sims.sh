#!/usr/bin/env bash
# Reproduce all five Partenon workshop simulations in isolated workspaces.
# Usage: bash workshop/simulations/run_all_sims.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER=(python3 "${SCRIPT_DIR}/sim_runner.py")

cd "${SCRIPT_DIR}/../.."

run_sim() {
  local company="$1"
  local name="$2"
  local industry="$3"
  local market="$4"
  local checklist="$5"
  local product="$6"
  local amount="$7"
  local topic="$8"

  local ws="workshop/simulations/workspaces/${company}"
  mkdir -p "${ws}"
  local out="${ws}/sim_output.txt"

  echo "=== ${name} ===" | tee "${out}"

  "${RUNNER[@]}" design --company "${company}" --name "${name}" --industry "${industry}" \
    --sell "Products and services for ${industry}" \
    --who "Small business owners and operators" \
    --how "Through a structured process and clear communication" \
    --market "${market}" --tone direct --addressing "you informal" --approver Founder \
    >> "${out}" 2>&1

  "${RUNNER[@]}" project --company "${company}" --title "First ${industry} priority" --industry "${industry}" --amount 5000 \
    >> "${out}" 2>&1

  "${RUNNER[@]}" task --company "${company}" --project-id PROJ-001 --title "Kickoff action" --priority high \
    >> "${out}" 2>&1

  "${RUNNER[@]}" checklist --company "${company}" --project-id PROJ-001 --industry "${checklist}" \
    >> "${out}" 2>&1

  "${RUNNER[@]}" client --company "${company}" --name "Primary Client" --email client@example.test --category direct \
    >> "${out}" 2>&1

  "${RUNNER[@]}" vendor --company "${company}" --name "Key Vendor" --service operations --category supplier \
    >> "${out}" 2>&1

  "${RUNNER[@]}" milestone --company "${company}" --entity-id CLI-001 --description "Confirm first deliverable" --date "2026-07-10" \
    >> "${out}" 2>&1

  "${RUNNER[@]}" payment-link --company "${company}" --product "${product}" --amount "${amount}" --currency usd \
    >> "${out}" 2>&1

  "${RUNNER[@]}" invoice --company "${company}" --email client@example.test \
    --items '[{"description":"Service","amount":15000,"currency":"usd"}]' \
    >> "${out}" 2>&1

  "${RUNNER[@]}" keys --company "${company}" >> "${out}" 2>&1

  "${RUNNER[@]}" briefing --company "${company}" >> "${out}" 2>&1

  "${RUNNER[@]}" calendar --company "${company}" --topic "${topic}" >> "${out}" 2>&1

  "${RUNNER[@]}" followups --company "${company}" >> "${out}" 2>&1

  echo "Output: ${out}"
}

run_sim example "Example Coffee Roasters" coffee "Example City, EX" consulting "Cold Brew Subscription" 2800 "cold brew subscription"
run_sim envision "Example Creative Agency" consulting "Example City, EX" consulting "Brand Sprint" 5000 "brand sprint campaign"
run_sim flintrock "Example Construction LLC" construction "Example City, EX" consulting "Mobilization Fee" 25000 "construction mobilization"
run_sim greenlight "Example Bookstore" retail "Example City, EX" retail "Book Subscription" 3500 "book subscription"
run_sim plausible "Example SaaS" saas "Example City, EX" consulting "Annual Plan" 9000 "privacy-first analytics"

echo "All simulations completed."

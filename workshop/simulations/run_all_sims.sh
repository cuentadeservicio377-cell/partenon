#!/usr/bin/env bash
set -euo pipefail

RUNNER=".venv/bin/python workshop/simulations/sim_runner.py"
ROOT="workshop/simulations/workspaces"

run_business() {
  local name=$1
  shift
  rm -rf "$ROOT/$name"
  local out="$ROOT/$name/sim_output.txt"
  mkdir -p "$(dirname "$out")"
  {
    echo "=== Scenario: $name ==="
    "$@"
    echo ""
  } > "$out" 2>&1
  echo "Wrote $out"
}

coffee() {
  $RUNNER route "organize my numbers"
  $RUNNER route "create a social campaign for live music"
  $RUNNER route "invoice a catering client"
  $RUNNER route "what do I have pending this week"
  $RUNNER design oblique "Oblique Coffee Roasters" food "Portland, OR" "On-site roasted coffee and community cafe" "Portland coffee lovers and remote workers" "Roast small batches, serve classic drinks, and host local events" direct informal "Jack Chandler" instagram,facebook
  $RUNNER project oblique "Buyout fundraising campaign" "John Chandler" 2026-07-31 120000 food
  $RUNNER task oblique PROJ-001 "Launch GoFundMe update" "Jack" 2026-07-05 high
  $RUNNER checklist oblique PROJ-001 food
  $RUNNER client oblique "Building lender" "lender@example.com" lender
  $RUNNER vendor oblique "Roasters United" beans
  $RUNNER milestone oblique CLI-001 "Confirm buyout extension terms" 2026-07-10
  $RUNNER payment-link oblique "Catering deposit" 5000 usd
  $RUNNER invoice oblique "event@example.com" "Event coffee service" 25000 usd
  $RUNNER calendar oblique "summer live music series" instagram,facebook 7
  $RUNNER briefing oblique morning
  $RUNNER keys
}

agency() {
  $RUNNER route "create a campaign for Q3"
  $RUNNER route "invoice the Acumen retainer"
  $RUNNER route "what is overdue this week"
  $RUNNER design envision "Envision Creative" services "Austin, TX" "Full-service marketing and repositioning" "Growth-stage B2B companies" "Strategy, creative, paid media, and reporting" direct informal "Creative Director" linkedin,instagram
  $RUNNER project envision "Q3 rebrand - Acumen" "Acumen" 2026-09-15 45000 consulting
  $RUNNER task envision PROJ-001 "Draft brand strategy deck" "Leah" 2026-07-10 high
  $RUNNER checklist envision PROJ-001 consulting
  $RUNNER client envision "Acumen" "contact@acumen.example.com" client
  $RUNNER vendor envision "Meta Ads" advertising
  $RUNNER milestone envision CLI-001 "Present creative concepts" 2026-07-20
  $RUNNER invoice envision "finance@acumen.example.com" "July retainer" 15000 usd
  $RUNNER calendar envision "Repositioning Formula case study" linkedin 7
  $RUNNER briefing envision morning
  $RUNNER keys
}

construction() {
  $RUNNER route "track the Austin office renovation project"
  $RUNNER route "invoice a progress draw"
  $RUNNER design flintrock "Flintrock Operating" construction "Austin, TX" "Commercial general contracting and construction management" "Austin property owners and developers" "Pre-construction planning, trade coordination, and safe delivery" direct informal "Project Manager" linkedin
  $RUNNER project flintrock "Austin office renovation" "Austin Property Group" 2026-10-15 175000 construction
  $RUNNER task flintrock PROJ-001 "Submit permit application" "PM" 2026-07-05 urgent
  $RUNNER checklist flintrock PROJ-001 construction
  $RUNNER client flintrock "Austin Property Group" "apg@example.com" client
  $RUNNER vendor flintrock "Austin Electrical" electrical
  $RUNNER milestone flintrock CLI-001 "Permit approved by city" 2026-07-20
  $RUNNER payment-link flintrock "Progress draw deposit" 35000 usd
  $RUNNER invoice flintrock "billing@apg.example.com" "Milestone 1 invoice" 87500 usd
  $RUNNER briefing flintrock morning
  $RUNNER keys
}

retail() {
  $RUNNER route "plan the summer reading series"
  $RUNNER route "invoice an event sponsor"
  $RUNNER design greenlight "Greenlight Bookstore" retail "Brooklyn, NY" "Curated books, author events, and community space" "Brooklyn readers and gift shoppers" "Staff picks, events, and local partnerships" warm informal "Jessica Stockton-Bagnulo" instagram,newsletter
  $RUNNER project greenlight "Summer reading series" "Greenlight Events" 2026-08-31 18000 retail
  $RUNNER task greenlight PROJ-001 "Confirm author lineup" "Maritza" 2026-07-08 high
  $RUNNER checklist greenlight PROJ-001 retail
  $RUNNER client greenlight "Penguin Random House" "events@penguin.example.com" publisher
  $RUNNER vendor greenlight "Brooklyn caterer" catering
  $RUNNER milestone greenlight CLI-001 "Author appearance confirmed" 2026-07-15
  $RUNNER payment-link greenlight "Event ticket" 1500 usd
  $RUNNER invoice greenlight "sponsor@localbank.example.com" "Series sponsorship" 5000 usd
  $RUNNER calendar greenlight "Banned Books Week" instagram,newsletter 7
  $RUNNER briefing greenlight morning
  $RUNNER keys
}

saas() {
  $RUNNER route "audit our API keys"
  $RUNNER route "track cloud spend against runway"
  $RUNNER route "create a subscription invoice"
  $RUNNER design plausible "Plausible Analytics" technology "Tartu, Estonia (remote)" "Privacy-first, open-source web analytics" "Privacy-conscious website owners and SaaS teams" "Lightweight script, GDPR compliance, and transparent pricing" direct informal "Marko Saric" blog,github
  $RUNNER project plausible "GDPR dashboard launch" "Product" 2026-08-15 0 technology
  $RUNNER task plausible PROJ-001 "Add data export endpoint" "Uku" 2026-07-10 high
  $RUNNER checklist plausible PROJ-001 consulting
  $RUNNER client plausible "EU Enterprise Prospect" "procurement@eu.example.com" prospect
  $RUNNER milestone plausible CLI-001 "Security review completed" 2026-07-25
  $RUNNER invoice plausible "billing@eu.example.com" "Annual analytics subscription" 90000 usd
  $RUNNER calendar plausible "Why we do not use cookies" blog,github 7
  $RUNNER briefing plausible morning
  $RUNNER keys
}

run_business oblique coffee
run_business envision agency
run_business flintrock construction
run_business greenlight retail
run_business plausible saas

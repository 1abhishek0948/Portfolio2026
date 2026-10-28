---
title: "eSewa, Khalti and IME Pay Gateway APIs for Developers"
category: payments
primary: "payment gateway api nepal"
secondary:
  - "esewa api"
  - "khalti api"
  - "payment integration nepal"
description: "How a developer actually integrates eSewa, Khalti and IME Pay in Nepal: the flow, the pieces you build, the sandbox and test steps, and the mistakes that make a live integration fail."
tags: [Payments, APIs, Development, Nepal]
date: "2026-10-27"
updated: "2026-10-27"
related:
  - "payment-gateway-setup/"
  - "ecommerce-website-development-nepal/"
faqs:
  - q: "Which gateway should a Nepali store integrate first?"
    a: "The one your customers actually use. In practice that means confirming eSewa, Khalti and IME Pay against your customer base and integrating the one or two that cover the most, rather than all of them on day one. A working narrow beat a broken wide."
  - q: "What is the hard part of the integration?"
    a: "Not the API call; it is the order state and the webhook. The call is easy; proving that a paid order is really paid, and handling the confirmation that arrives later and out of band, is where stores go wrong."
  - q: "Do I need to do anything special before going live?"
    a: "Yes: test in the sandbox with a real order flow, reconcile one payment end to end, and keep the webhook handling in place before you take real money. Skipping the reconciliation is how a store ends up with paid orders that did not activate."
---

Integrating a Nepali payment gateway is not one task, it is three: the API call, the order state, and the confirmation that arrives later. Most failed integrations fail on the last two, not the first. This guide is the developer's map of all three, and the test steps that catch a broken live launch.

Gateways, their docs and their fees change, so confirm the current API and the current fee before you build. This is practical guidance, not a recommendation of any provider.

## The three pieces, not one

| Piece | What it is | Where it goes wrong |
|---|---|---|
| The call | Starting a payment, getting a redirect or token | A wrong amount or a missing return path |
| The order state | Knowing which order the payment is for | Two orders, one payment, no link |
| The confirmation | The webhook that says "paid" arrives out of band | Assuming the call's return is the proof |

The last one is the one that kills stores: the confirmation is a separate, later, out-of-band event, and a payment is not confirmed until you process it, not when the customer taps pay.

## The flow you actually build

1. **Create the order** on your side with a single source of truth for the amount.
2. **Start the gateway payment** for that order, with a return path back to your site.
3. **Listen for the confirmation**, mark the order paid *only* on that, and handle the failure and the duplicate.
4. **Reconcile**, and keep the record that a specific confirmation matched a specific order.

The "mark paid only on the confirmation" rule is the whole security model, and it is the one rule people shortcut and regret.

## The two test steps before live

Do not skip these, because they are the difference between a launch and a pile of unactivated orders:

- **Sandbox a real order flow** from start to finish, including a cancelled and a duplicate payment, not just the happy path.
- **Reconcile one live small payment end to end** before you open the tap, and confirm the confirmation matched the order.

The setup side, choosing the right gateway for your customers, is covered in [setting up eSewa and Khalti payment gateway APIs](/blog/payment-gateway-setup/), and it sits inside the bigger picture of [e-commerce website development in Nepal](/blog/ecommerce-website-development-nepal/).

## A sensible default

Integrate the one or two gateways your customers actually use, build the order state and the webhook handling as first-class parts, mark paid only on the confirmation, and run the two test steps before going live. Narrow and correct beats wide and broken, every time.

**Bottom line:** a Nepali gateway integration is a call, an order state and a late confirmation, and the confirmation is the security model. Build all three, reconcile one live payment before you open it, and the store does not quietly end up with orders that paid but never activated.

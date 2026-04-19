# Demo Checklist

## Minimum Walkthrough

- [ ] Open the project README and explain the lab objective.
- [ ] Show the live Azure Monitor alert rules screenshot.
- [ ] Show the Sentinel overview screenshot.
- [ ] Show the `AzureActivity` KQL proof of NSG write and delete activity.
- [ ] Show the fired `NSG Or Security Rule Changes` alert.
- [ ] Explain the remaining `Conditional Access` limitation as a tenant-privilege blocker, not a missing design.

## Interview Storyline

1. Start with the business need: build a secure Azure sandbox that feels like a small enterprise environment.
2. Show that the lab is real by pointing to live deployment and monitoring evidence.
3. Explain how diagnostic settings, `Log Analytics`, and scheduled query alerts work together.
4. Show the KQL evidence and the fired alert to prove the detection pipeline is live.
5. Close with the `Conditional Access` blocker note and explain that the design is documented even though the tenant privileges are limited.

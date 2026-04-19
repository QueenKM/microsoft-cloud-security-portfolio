# Sample Insights From The Generated Dataset

Use these talking points when you demo the dashboard or write a one-page insight summary.

## Department-Level Signals

- `Research Office` shows the highest sign-in failure volume in the sample data, with `23,829` failures.
- `Student Services` follows closely with `22,265` failures.
- `IT` shows the lowest average compliance score in the sample set at roughly `70.2`, which makes it a good candidate for a focused improvement story.
- `Research Office` also leads in privileged role changes, which strengthens the narrative that high activity and elevated access often travel together.

## Workload-Level Signals

- `Endpoints` shows the highest high-severity incident volume in the sample data at `826`.
- `Azure` is close behind at `774`, making it a strong companion visual in the incident-by-workload chart.
- `Microsoft Teams` stands out on governance pressure because it combines significant incident activity with a high data loss count.
- `Entra ID` has the lowest high-severity incident total in the sample set, but it still contributes meaningfully to sign-in failure volume.

## Suggested Storyline

1. Start with sign-in failures to show operational pressure.
2. Pivot to workload incident distribution to show where that pressure turns into security events.
3. Use guest-account and Teams lifecycle visuals to show that collaboration governance also affects the risk picture.
4. Finish with compliance score to show that posture and event volume need to be read together, not separately.

## Example Insight Summary

`Research Office` and `Student Services` carry the highest authentication pressure in the sample data, while `Endpoints` and `Azure` generate the largest high-severity incident volume. At the same time, `IT` trails the rest of the organization on average compliance score, which creates a useful executive narrative: the environment does not have one single weak spot, but a combination of identity pressure, endpoint load, and uneven control maturity.

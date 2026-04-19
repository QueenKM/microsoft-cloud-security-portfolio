# GIF Artifacts

Store short demo GIFs here for GitHub previews and interview walkthroughs.

## Suggested File Names

- `01-dashboard-slicer-demo.gif`
- `02-model-view-pan.gif`

## Recommended Workflow

1. Capture a short sequence of ordered screenshots while interacting with `Power BI Desktop`.
2. Save them into a temporary folder such as `frames-dashboard`.
3. Run the shared script:

```bash
python3 ../../../shared-assets/scripts/make_demo_gif.py \
  --input-dir ./frames-dashboard \
  --output ./01-dashboard-slicer-demo.gif \
  --duration-ms 700 \
  --pause-last-ms 1600 \
  --max-width 1400
```

1. Review the GIF locally before keeping it in the repo.

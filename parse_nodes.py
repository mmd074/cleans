name: Parse IP and Port

on:
  workflow_dispatch:
  schedule:
    - cron: '*/5 * * * *'

jobs:
  parse:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Run parser
        run: python parse_nodes.py

      - name: Commit and push always
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add nodes.txt
          git commit -m "Update nodes $(date +%Y-%m-%d\ %H:%M)" || true
          git push

#!/usr/bin/env bash
set -euo pipefail

echo "$ mmrl backtest"
mmrl backtest

LATEST=$(ls -t results | head -n 1)
echo "$ mmrl report results/$LATEST --out docs/assets/report.html"
mmrl report "results/$LATEST" --out docs/assets/report.html

echo "Done."


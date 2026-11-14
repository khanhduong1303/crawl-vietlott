#!/usr/bin/env bash
#
# Crawl du lieu Vietlott roi commit ket qua vao repo.
#
# set -e: ban cu KHONG co cai nay, nen script chay tiep qua moi loi va exit code
# cuoi cung lai la cua `git push`. Hau qua: crawl rong hoac render_readme crash
# van co the cho ra job MAU XANH. Gio bat ky buoc nao fail la job do ngay.
set -euo pipefail

DATA_FOLDER=data
GIT_USER="khanhduong1303"
GIT_EMAIL="khanhduong1303@gmail.com"
BRANCH="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"

echo "pwd    $(pwd)"
echo "branch $BRANCH"

export PYTHONPATH="src"
export LOGURU_LEVEL="INFO"

# Delay ngau nhien 1s - 5 phut de lech gio cron, tranh bi nhan dien la bot.
# Chi can cho lich chay that tren master; nhanh test bo qua cho nhanh vong lap.
if [[ "$BRANCH" == "master" ]]; then
  RANDOM_DELAY=$(( RANDOM % 301 + 1 ))
  echo "sleep ${RANDOM_DELAY}s"
  sleep "$RANDOM_DELAY"
fi

for product in power_655 power_645 power_535; do
  python src/vietlott/cli/crawl.py "$product"
  python src/vietlott/cli/missing.py "$product"
done

python src/render_readme.py

# ----- commit va push -----
git config user.name  "$GIT_USER"
git config user.email "$GIT_EMAIL"

git add "$DATA_FOLDER" readme.md
git status --short

if git diff --cached --quiet; then
  # Khong co ky quay moi la chuyen BINH THUONG (crawl 8 lan/ngay, quay 3 lan/tuan).
  echo "khong co du lieu moi -> bo qua commit/push"
  exit 0
fi

git commit -m "update data @ $(date +'%Y-%m-%d %H:%M:%S')"

# Remote co the da co commit moi trong luc job dang chay (vd: push tay).
# Ban cu push thang -> bi reject 'fetch first' va job do oan.
git pull --rebase origin "$BRANCH"
git push origin "$BRANCH"

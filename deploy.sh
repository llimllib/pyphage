rsync -avuz -e ssh --safe-links \
--exclude ".git" --exclude "*.conf" --exclude "static" --exclude "*.db" \
--exclude "*.pyc" \
. llimllib@boobtube.local:~/pyphage \

rsync -avuz -e ssh --safe-links \
--exclude ".git" --exclude "*.conf" --exclude "static" --exclude "*.db" \
. llimllib@boobtube.local:~/pyphage \

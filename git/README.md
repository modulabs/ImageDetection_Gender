### Global settings

- git config --global color.ui true

- git config --global core.editor nano

- git config --global alias.co checkout
- git config --global alias.br branch
- git config --global alias.ci commit
- git config --global alias.st status
- git config --global alias.unstage 'reset HEAD --'
- git config --global alias.last 'log -1 HEAD'
- git config --global alias.gr 'log --graph --oneline --decorate --all'
- git config --global alias.df diff
- git config --global alias.dt difftool

- git config --global push.default simple

- git config --global diff.mnemonicprefix true
- git config --global diff.tool vimdiff

### Local settings

- git config --local user.name "your_name"
- git config --local user.email "your_email@company.com"
- git config --local credential.helper store

# 基本环境配置

## Themes

ZSH_THEME="ys"


## Plugins

plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
)


## oh-my-zsh

### 关闭oh-my-zsh自动更新
export DISABLE_AUTO_UPDATE=true

export MY_ZSH=$MELON_ROOT/profiles/oh-my-zsh
source $MY_ZSH/oh-my-zsh.sh


## Source

[ -f ~/.bash_profile ] && source ~/.bash_profile
[ -f ~/.bashrc ] && source ~/.bashrc
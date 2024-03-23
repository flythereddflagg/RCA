unlet! skip_defaults_vim
source $VIMRUNTIME/defaults.vim

set number
set mouse=a
set shell=powershell

inoremap {<CR> {<CR>}<Esc>ko<tab>
inoremap ( ()<Esc>ha
inoremap [ []<Esc>ha
inoremap " ""<Esc>ha
inoremap ' ''<Esc>ha
inoremap ` ``<Esc>ha


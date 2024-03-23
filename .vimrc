unlet! skip_defaults_vim
source $VIMRUNTIME/defaults.vim
source $HOME/vimfiles/autoload/plug.vim
call plug#begin()

Plug 'preservim/nerdcommenter'
Plug 'junegunn/fzf.vim'
Plug 'preservim/nerdtree'

call plug#end()

set number
set mouse=a
set shell=powershell
set belloff=all

inoremap {<CR> {<CR>}<Esc>ko<tab>
inoremap ( ()<Esc>ha
inoremap [ []<Esc>ha
inoremap " ""<Esc>ha
inoremap ' ''<Esc>ha
inoremap ` ``<Esc>ha

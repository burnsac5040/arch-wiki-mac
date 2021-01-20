## `arch-wiki-docs` and `arch-wiki-lite` - MacOS Compatible

### Requirements:
  - `brew install newt ripgrep w3m`
  - `cargo install huniq`

**Alternatives**:

One can modify the `wiki-search` script if they instead would like to use:
  - `dialog` over `whiptail` (from `newt`)
    - This script uses `/usr/local/etc/dialog.d/` folder for storage
  - `grep` over `ripgrep`
  - `sort | uniq -c` over `huniq -c` / `sort | uniq` over `huniq`
  - These were chosen because it decreased the time the script took from 10.4s to 8.4s

### Installation:

```sh
git clone https://github.com/burnsac5040/arch-wiki-mac.git
cd arch-wiki-mac
make install # No sudo
```

-----------------------------------------------------------------------
### Installation by untarring:

```sh
git clone https://github.com/burnsac5040/arch-wiki-mac.git
cd arch-wiki-mac
tar -xzf arch-wiki.tar.gz -C /usr/local --strip-components 2
```

------------------------------------------------------------------------
### `arch-wiki-docs` Installation (building yourself):
```sh
pip install lxml cssselector kitchen http.cookiejar simplemediawiki
git clone https://github.com/lahwaacz/arch-wiki-docs
cd arch-wiki-docs
LANG=en_US.UTF-8 python arch-wiki-docs.py --output-directory ./build_wiki --safe-filenames
mv build_wiki /usr/local/share/doc/arch-wiki/text
```

------------------------------------------------------------------------
### `arch-wiki-docs` `pkgbuild`
```sh
brew install makepkg
git clone https://github.com/burnsac5040/arch-wiki-mac.git
cd arch-wiki-mac/docs
makepkg -d
```

Move the files to wherever you want to store the wiki.

------------------------------------------------------------------------
### `arch-wiki-lite` Installation (not sure how to install this)

```sh
brew install makepkg
git clone https://github.com/burnsac5040/arch-wiki-mac.git
cd arch-wiki-mac/lite
makepkg -d
tar -xzf arch-wiki-lite-20200527-1-any.pkg.tar.gz | installer -pkg -target /
```

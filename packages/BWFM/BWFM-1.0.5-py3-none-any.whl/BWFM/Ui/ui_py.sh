for file in BWFM/Ui/*.ui; do
    pyside2-uic -x $file > BWFM/Ui/$(basename $file .ui).py
done
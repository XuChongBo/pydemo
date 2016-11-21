# coding: utf-8
import os
import pipes
import tempfile
import tornado

p = pipes.Template()
#p.debug(True)
p.append('export WINEPREFIX=/data/xucb/.wine; export WINEDEBUG=-all;export DISPLAY=:1; wine  /usr/lib/sapi4linux/pydir/python.exe  ~/tts/speak2file.py $IN   $OUT ', 'ff')

t = tempfile.NamedTemporaryFile('w+r')
t.write('one\ntwo\nthree\nfour\nfive\nsix\n')
t.seek(0)

#p.copy(t.name, "/tmp/a.pdf")  # 'ff' $IN $OUT
p.copy("abc.wav", "/tmp/a.pdf")  # 'ff' $IN $OUT

t.close()

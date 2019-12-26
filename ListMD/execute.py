import os

os.system('python3 ~/conkyConfigs/ListMD/mdToPython.py /home/shafay/conkyConfigs/ListMD/hw.md | lynx --dump -stdin | fold -s -w 65 > /home/shafay/conkyConfigs/ListMD/hwText')
os.system('python3 ~/conkyConfigs/ListMD/mdToPython.py /home/shafay/conkyConfigs/ListMD/notes.md | lynx --dump -stdin | fold -s -w 40 > /home/shafay/conkyConfigs/ListMD/notesText')
os.system('python3 ~/conkyConfigs/ListMD/combineFiles.py /home/shafay/conkyConfigs/ListMD/notesText /home/shafay/conkyConfigs/ListMD/hwText')

# ${execi 3600  }${execi 3600 }${execpi 300  }

# ${hr 1}
# ${font Entopia:bold:size=12}${color 33E9FF}Notes${alignc}--------------------------------------------------------${alignr}${color red}HW/assignments
# $font$color${execpi 300 python3 /home/shafay/conkyConfigs/ListMD/execute.py }
import mistletoe
import sys


def main():
    f=open(sys.argv[1], "r") 
    contents =f.read()

    rendered = mistletoe.markdown(contents)
    print(rendered)


if __name__ == '__main__':
   main()

# /home/shafay/conkyConfigs/ListMD/hw.md
# ${font Droid Sans Mono:size=10}${execi 3600 python3 ~/conkyConfigs/ListMD/mdToPython.py /home/shafay/conkyConfigs/ListMD/hw.md | lynx --dump -stdin | fold -s -w 40 > /home/shafay/conkyConfigs/ListMD/hwText }${execi 3600 cat /home/shafay/conkyConfigs/ListMD/notes.md > /home/shafay/conkyConfigs/ListMD/notesText }${execpi 3600 python3 /home/shafay/conkyConfigs/ListMD/combineFiles.py /home/shafay/conkyConfigs/ListMD/hwText /home/shafay/conkyConfigs/ListMD/notesText }
import mistletoe
import sys


def main():   
    fHW=open(sys.argv[1], "r") 
    fNotes=open(sys.argv[2], "r")
    hw = fHW.read()
    notes = fNotes.read()

    hwLines = hw.split('\n')
    notesLines = notes.split('\n')

    maxLines = hw.count('\n') if hw.count('\n') > notes.count('\n') else notes.count('\n')
    rendered = ''
    i = 0

    while(i<maxLines):
        rendered += (' ' if i >= len(hwLines) else hwLines[i] ) + '${alignr}' + (' ' if i >= len(notesLines) else notesLines[i]) + '\n'
        i+=1

    fHW.close()
    fNotes.close()

    print(rendered)


if __name__ == '__main__':
   main()

# /home/shafay/conkyConfigs/ListMD/hw.md
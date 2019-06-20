import mistletoe
import sys


def main():   
    fHW=open(sys.argv[1], "r") 
    fNotes=open(sys.argv[2], "r")
    hw = fHW.read()
    notes = fNotes.read()

    hwLines = hw.split('\n')
    notesLines = notes.split('\n')

    j=0
    while(j<len(hwLines)):
        if(hwLines[j]=='\n' or hwLines[j]==' ' or hwLines[j]==''):
            del hwLines[j]
        j+=1
    j=0
    while(j<len(notesLines)):
        if(notesLines[j]=='\n' or notesLines[j]==' ' or notesLines[j]==''):
            del notesLines[j]
        j+=1

    maxLines = len(hwLines) if len(hwLines) > len(notesLines) else len(notesLines)
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
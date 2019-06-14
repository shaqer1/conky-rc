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
import picnic
import picnic_setup_grocy
import argparse
import sys

# Firt time run this. Make sure you have an empty Grocy database (or not, but prepare for conflicts then)
def installPicnicInGrocy():
    install = picnic_setup_grocy.PicnicSetupGrocy()
    install.installAll()

# To import picnic products run this, comment above setup:
def importPicnicInGrocy():
    pp = picnic.PicNic()
    pp.importLastPicnicDelivery()


parser = argparse.ArgumentParser(
    prog='main.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
###############################
Picnic Data importer into Grocy
###############################

Please change config.py to:
# point to your own Grocy instance, start with an empty Grocy (optional)
# Change some specific script settings
# setup the right username and password for picnic 

After that, run this script with:
main.py install (only first time)


When finished:
main.py import 

''')


FUNCTION_MAP = {'install': installPicnicInGrocy,
                'import': importPicnicInGrocy}

parser.add_argument('command', choices=FUNCTION_MAP.keys())

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

func = FUNCTION_MAP[args.command]
func()


# TODO
# Todo ml to Miliiters quantitiy
# Check for updated ean codes in products.list
# Check for updates recipes in recipes.list, and import


# Future ideas:
# Import 'vers na aantal dagen, minimum' picnic, count the real delivery date + numOfDays. Picnic has really short THT dates...
# Fill in kcal, product details. Loop through every product and append information (not sure how interesting this is though...)

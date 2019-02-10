#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    IS 211 Week 2 Assignment
"""

import urllib2
import csv
import datetime
import logging
import argparse

helpMesage = """\
Enter a URL linking to a .csv file.
Example URL: https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv
"""
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help=helpMesage)
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')


def downloadData(url):
    """Opens a supplied URL link.

    Args:
        url(str): A string for a website URL.

    Returns:
        datafile(various): A variable linked to an applicable datafile found at
        the supplied URL, if valid.

    Example:
        >>> downloaddata('https://s3.amazonaws.com/cuny-is211-spring2015
        /birthdays100.csv')
        <addinfourl at 3043697004L whose fp = <socket._fileobject object at
        0xb5682f6c>>
    """
    datafile = urllib2.urlopen(url)
    return datafile


def processData(datafile):
    """Processes a datafile containing information in .csv format.

    Args:
        datafile(file): A .csv file supplied by user or downloaded from a URL.

    Returns:
        newdict(dict): A dictionary containing keys comprised of the userid in
        the supplied .csv file, and the values as the name and date of birth as
        a datetime object.

    Example:
        >>> load = downloadData('https://s3.amazonaws.com/cuny-is211-spring2015
        /birthdays100.csv')
        >>> processData(load)
        {'24': ('Stewart Bond', datetime.datetime(2008, 2, 15, 0, 0)),
         '25': ('Colin Turner', datetime.datetime(1994, 6, 6, 0, 0)}
    """
    readfile = csv.DictReader(datafile)
    newdict = {}

    for num, line in enumerate(readfile):
        try:
            born = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            newdict[line['id']] = (line['name'], born)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(
                num, line['id']))

    return newdict


def displayPerson(id, personData):
    """Looks up the id number in a supplied dictionary, and returns the name and
       date of birth associated with the id number.

       Args:
           id(int, str): The number to be checked against the dictionary and
           return the associated person.
           persondata(dict): A dictionary containing a tuple of the username
           and date of birth.

        Returns:
            (str): A string displaying either the person and date of birth which
            which corresponds with the input id number, or a string indicating
            the id is not associated with anyone in the supplied dictionary.

        Examples:
            >>> displayperson(11, persondata)
            Person #11 is Angela Watson with a birthday of 1994-04-15
            >>> displayperson(1000, persondata)
            No user found with that ID.
        """
    idnum = str(id)
    if idnum in personData.keys():
        print('Person #{} is {} with a birthday of {}'.format(\
            id, personData[idnum][0],\
            datetime.datetime.strftime(personData[idnum][1], '%Y-%m-%d')))
    else:
        print('No user found with that ID.')


def main():
    """Combines downloadData, processData, and displayPerson into one program to
    be run from the command line.
    """
    if not args.url:
        raise SystemExit
    try:
        csvData = downloadData(args.url)
    except urllib2.URLError:
        print('Please enter a valid URL.')
        raise
    else:
        personData = processData(csvData)
        chooseid = raw_input('Please enter an ID# for lookup:')
        print(chooseid)
        chooseid = int(chooseid)
        if chooseid <= 0:
            print('Number equal to or less than zero entered. Exiting program.')
            raise SystemExit
        else:
            displayPerson(chooseid, personData)
            main()

if __name__ == '__main__':
    main()

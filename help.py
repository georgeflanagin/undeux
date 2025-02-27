#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pragma pylint=off
    
# Credits
__author__ =        'George Flanagin'
__copyright__ =     'Copyright 2017 George Flanagin'
__credits__ =       'None. This idea has been around forever.'
__version__ =       '1.0'
__maintainer__ =    'George Flanagin'
__email__ =         'me+undeux@georgeflanagin.com'
__status__ =        'continual development.'
__license__ =       'MIT'

import os

import gkflib as gkf

def undeux_help() -> int:
    """
    `undeux` is a utility to find suspiciously similiar files that 
    may be duplicates.

    There is a configuration file of the "Windows.ini" sort. It is 
    delivered with the program. By default it looks like this:


        [exclude]
          small_file = 4096
          big_file = 1<<28
          hidden = yes
          young_file = 30
          links = yes

        [general]
          verbose = no
          nice = 20
          
        [db]
          type = sqlite
          file = ~/undeux.db

    Taking the options in order, undeux tries to provide useful default
    values. For example, we want to exclude some files as a matter of 
    general practice:

        small_file -- They don't take up much space, and often they
            are strewn around directories because they need to
            be in particular locations. Files smaller than 4096 bytes
            will be ignored.

        big_file -- This is the "hog threshold." If a file this large
            or larger has not been accessed in quite a while, then it
            is a potential Bogarter of disc space.

        hidden -- We usually don't want to evaluate hidden files, the
            theory being that they are hidden for a reason.

        young_file -- Files younger than 30 days are still in use? Maybe?

        links -- Links can be confusing. We are going to treat them like
            links rather than evaluating the things they link to.

    All the command line arguments have defaults. If you run the program
    with no arguments, you will be reading this help, just like you are
    right now. If you want to accept all the defaults, use the single
    argument:

        undeux --just-do-it

    If you are running without --just-do-it, then the program will pause
    and ask you if it understood the options correctly. 

    undeux works by creating a score for each file that indicates the
    likelihood that it is a candidate for removal. The scoring is on
    the half open interval [0 .. 1), where zero indicates that the file
    may not be removed, and values near 1 indicate that if you don't 
    remove it fairly soon, WW III will break out somewhere near your
    disc drive[s]. Most files are somewhere between.

    To elaborate:

    - Files that you cannot remove are given a zero, and not further
        incorporated into the removal logic. The same is true of a file
        that is too new, or too small.
    - Files are penalized for not having been modified/accessed in a 
        long time.
    - Files that are large are penalized.
    - Files are penalized if their contents exactly match another
        file. This is the final step. There is no need to compare every
        file because if two files have different lengths, they 
        are obviously not the same file.
    
    So if you have an ancient file, that is a duplicate of some other
    file, with the same name, somewhere on the same mount point, and it 
    is large and hasn't been accessed in a while, then its score
    may approach 1.0. This program will then produce a list of the worst
    offenders.

    Through the options below, you will have a lot of control over
    how `undeux` works. You should read through all of them before you
    run the program for the first time, and as the author I recommend
    that you choose just one or two directories to better understand
    the effects of your choices. If you have questions you can read 
    through this help a second time, or write to me at this address:

        me+undeux@georgeflanagin.com

    THE OPTIONS:
    ==================================================================

    -? / --help / --explain :: This is it; you are here. There is no
        more.

    --big-file {int}
        The value can be a literal file size, or binary logarithm (power
        of 2). A commonsense value is something like 28, which is ~256MB.

    --dir {dir-name} [--dir {dir-name} .. ]
        This is an optional parameter to name several directories,
        mount points, or drives to include in the search. If --dir
        is not present, the default value is the user's home.

        [[ NOTE: --dir: the directory names may contain environment 
        variables. They will be correctly expanded. -- end note. ]]

    --exclude / -x {name} [ -x {name} .. ]
        Exclude matching files from consideration. This is done primarly
        for excluding things like `.git` directories, where there 
        are certainly no files that should be removed.        

    --follow-links 
        If present, symbolic links will be dereferenced for purposes
        of consideration of duplicates. Use of this switch requires
        careful consideration, and it is probably only useful in 
        cases where you think you have files in your directory of
        interest that are duplicates of things elsewhere that are
        mentioned by symbolic links that are *also* in your 
        directory of interest.

    --just-do-it
        Accept all defaults, don't ask for confirmation, and run the 
        program.  

    --nice {int} 
        Keep in mind a terabyte of disc could hold one million files 
        at one megabyte each. You should be nice, and frankly, the program
        may run faster in nice mode. The default value is 20, which
        on Linux is as nice as you can be.

    --quiet 
        I know what I am doing. Just let me know when you are finished. 
        This option is normally off, and the program does provide info
        as it runs. However, if logorrhea is your thing, then --verbose
        is what you want.

    --small-file {int} 
        Define the size of a small file in bytes. These will be ignored. 
        Many duplicate small files will indeed clutter the inode space
        in the directory system, but many projects depend on tiny and
        duplicate small .conf files being present. The default value is
        4096.

    --verbose
        Tell all.

    --version
        Print information about the version of the program and the libraries,
        and then exit.

    --young-file {int} 
        Define how new a file needs to be to be ignored from processing.
        The idea is that if you downloaded Apocalypse Now from Amazon only
        one week ago, then you probably want to keep this whale even 
        though it is 50+GB.  The default is zero (0), which means to consider
        even new files when looking for duplicates.
    """

    gkf.nicely_display(undeux_help.__doc__)
    return os.EX_OK




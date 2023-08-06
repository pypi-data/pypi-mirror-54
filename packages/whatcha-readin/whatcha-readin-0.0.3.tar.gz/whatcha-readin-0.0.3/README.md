[![Build Status](https://travis-ci.org/allisonking/whatcha-readin.svg?branch=master)](https://travis-ci.org/allisonking/whatcha-readin)

# Whatcha Readin'?
This is a small package that attempts to append the books you are reading (on Goodreads) to your commit messages using Python and Git Hooks! Ever wonder what your favorite author was reading while writing a scene? If for some reason your favorite author used git to commit their writing, now you would know! 

Example:
```
commit 6a5534290d50f1329d877dd5615aa86e880b66fe
Author: Allison King
Date:   Sun Jul 28 10:11:39 2019 -0400

    bump version number
    
    Books-reading:
    When America First Met China: An Exotic History of Tea, Drugs, and Money in the Age of Sail
    The Trainable Cat: A Practical Guide to Making Life Happier for You and Your Cat
    Fevre Dream
```

# Quick start
## Install
```
pip install whatcha-readin
whatcha-readin install
```

This copies a hook into your `.git/hooks` folder to append the books you are currently reading to your commit message. You can check the status of your install with:

```
whatcha-readin status
```

## Configure
In order to query for what you are reading, you will need to:

* Find your Goodreads user ID (the number in the URL on your profile page, i.e. https://www.goodreads.com/user/show/20891766-allison-king is `20891766`)
* Get a [Goodreads API key](https://www.goodreads.com/api/keys)

```
whatcha-readin config
```

You will be prompted to enter your user ID and your API key. Alternatively to configure without prompting:

```
whatcha-readin config --user-id [user-id] --key [api-key]
```

All set! Your commits should now automatically append the books you are reading. If you are not online while committing, the hook cannot query the Goodreads API so will not attempt to append to your commit message.

## Uninstalling
```
whatcha-readin uninstall
```

# Developing
1. Install the dev requirements using `pip install -r requirements.txt`
2. Set up the pre-commit hooks `pre-commit install`

# Thanks
Thanks to [podmena](https://github.com/bmwant/podmena) for serving as a starting point for how to write this!

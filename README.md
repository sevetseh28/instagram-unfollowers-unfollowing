# Instagram Unfollowers & Unfollowing detector

So I did this simple quick project containing Python scripts that allow you to dump your Instagram followers and following and therefore detecting 
your unfollowers and unfollowing accounts (doing some set operations).

I didnt trust those commercial mobile apps where you can't see what's really going on behind the scenes when you give them permission. 

With this you can see all the code and what is actually doing: some nice simple requests I sniffed with Chrome inspector :)

## Requirements
Python 3.6.5 (but should work on others, but not on Python 2)

## Usage
First, get logged in on Instagram web and grab the Cookie and your instagram ID (google some web to find your ID)
and paste those into the ```settings.py``` file.

The ```COOKIE``` setting must be the Cookie value (the whole string). You can get it with a Chrome extension like EditThisCookie.

Then run ```python main.py``` and that's it!

** If you want to dump your followers/following to MongoDB so you can do some intresting queries, you must enable the setting on settings.py
and don't forget to ```pip install pymongo``` before.


Any contribution or suggestion is very welcomed!

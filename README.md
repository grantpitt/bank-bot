# bank-bot


The [`Playwrite`](https://playwright.dev/python/) library is awesome. In this project, I log in to my bank account and download a bunch of statements and other data. This task would be really hard with just the requests library.

It was also fun to have another use case for `ayncio` in python. In the script, it downloads all 24 statements concurrently.

To try out the script, add an `auth.py` file and add username and password variables. Then install `Playwright` and run `playwright install`

# lib\_clickbot
This package contains the functionality to record all uconn off campus housing info into an excel spreadsheet, sorted and in order by your preferences.

* [lib\_clickbot](#lib\_clickbot)
* [Description](#package-description)
* [Usage](#usage)
* [Possible Future Improvements](#possible-future-improvements)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#licence)
* [Todo and Possible Future Improvements](#todopossible-future-improvements)
* [FAQ](#faq)
## Package Description
* [lib\_clickbot](#lib\_clickbot)

This package will simulate your clicks, typing, and scrolling in a way that is not detectable by most websites. Sorry that it's not well documented, I wrote it real quick as a one off thing and am just making this package now. Essentially, it simulates a user. You can click, type keys, and/or scroll with variable time intervals for every event. Then the clickbot will continuously run, with random time between each event based on your input, with random locations that it clicks within the parameters you provide. It is fairly self explanatory to use once you run it and see it go, so just run it.

### Usage
* [lib\_clickbot](#lib\_clickbot)

#### In a Script
You can do this but I don't feel like documenting it and it would be rare, so good luck and email me if you have questions.

#### From the Command Line

run in a terminal: ```clickbot```

Once it runs simply follow the instructions

### Installation instructions
* [lib\_clickbot](#lib\_clickbot)

Then install the package with:
```pip3 install lib_clickbot --upgrade --force```

To install from source and develop:
```
git clone https://github.com/jfuruness/lib_clickbot.git
cd lib_clickbot
pip3 install wheel --upgrade
pip3 install -r requirements.txt --upgrade
python3 setup.py sdist bdist_wheel
python3 setup.py develop
```

### System Requirements
* [lib\_clickbot](#lib\_clickbot)

None

## Testing
* [lib\_clickbot](#lib\_clickbot)

There are no tests, if you run it and it fails then it's probably broken lol. I have to write some but since it's just for fun whatevs, it has served it's purpose.

## Development/Contributing
* [lib\_clickbot](#lib\_clickbot)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because I do not check those messages often

## History
* [lib\_clickbot](#lib\_clickbot)
   * 0.1.0 - Initial commit
   * 0.1.1 - Minimal documentation

## Credits
* [lib\_clickbot](#lib\_clickbot)

Thanks to Mike. What a guy.

## License
* [lib\_clickbot](#lib\_clickbot)

BSD License

## TODO/Possible Future Improvements
* [lib\_clickbot](#lib\_clickbot)

        * How about some documentation and tests

## FAQ
* [lib\_clickbot](#lib\_clickbot)

None so far

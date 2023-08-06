from roboeye import Database


def test_json():
    db = Database('example')

    assert db['heroes']['Jinx'] == {
        "name": "Jinx",
        "colors": ["violet"],
        "team": "The Hive"
    }


def test_yaml():
    db = Database('example')

    assert db['heroes']['Robin'] == {
        "name": "Robin",
        "colors": ["red", 'green'],
        "team": "Teen Titans"
    }


def test_csv():
    db = Database('example')

    assert db['characters'] == [
        {
            'Name': 'Rick',
            'Job': 'Scientist',
            'Age': 'Unspecified',
        }, {
            'Name': 'Morty',
            'Job': 'Apprentice',
            'Age': '14',
        }, {
            'Name': 'Beth',
            'Job': 'Surgeon',
            'Age': '34',
        }, 
    ]


def test_md():
    db = Database('example')

    md = db['blog']['python-considered-harmful']

    assert md.as_html() == ('<h1>Tolle Überschrift</h1>\n'
                            '<p>Dies ist der Inhalt</p>\n')

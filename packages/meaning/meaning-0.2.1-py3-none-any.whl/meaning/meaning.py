import re
import pangu
import huepy
import argparse
import requests
import xmltodict
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, Unicode, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from meaning.version import __version__

engine = create_engine('sqlite:///words.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    
    word_id = Column(Integer(), primary_key=True)
    word_name = Column(String(15), nullable=False, unique=True)
    word_translate = Column(Unicode(), nullable=False)
    create_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
       return "Word(word_name='{self.word_name}', "\
                    "word_translate='{self.word_translate}')".format(self=self)  

Base.metadata.create_all(engine)


def get_parser():
    parser = argparse.ArgumentParser(description="Translate words via command line")
    parser.add_argument('words', metavar='WORDS', type=str, nargs='*', help='the words to translate')
    parser.add_argument('-r', '--records', action='store_true', help='spawn a records prompt shell')
    parser.add_argument('-v', '--version', action='store_true', help='displays the current version of meaning')

    return parser


def highlight(text: str, keyword: str):
    text = pangu.spacing_text(text)
    return re.sub(
        keyword,
        "\33[0m" + "\33[93m" + keyword + "\33[0m" + "\33[37m",
        text,
        flags=re.IGNORECASE
    )


def UpdateSQL(word: str, translate=None):
    if session.query(Word).filter(Word.word_name == word).first() :
        query = session.query(Word) 
        query = query.filter(Word.word_name == word) 
        query.update({Word.updated_on: datetime.now()}) 
    
        cc_word = query.first() 
    else:
        cc_word = Word(word_name=word,
                       word_translate=translate)
        session.add(cc_word)
        session.commit()


def RecordsPromptShell():
    from terminaltables import SingleTable
    from sqlalchemy import desc

    data = []
    data.append(['word', 'translate', 'date'])
    for word in session.query(Word).order_by(desc(Word.updated_on)).limit(5):
        data.append([word.word_name, word.word_translate, word.updated_on])
    table = SingleTable(data)
    print(table.table)


def TranslateWithAiCiBa(words: str):
    iciba_key = '47A83B5C4CBA453E752D056400733043'
    url = "http://dict-co.iciba.com/api/dictionary.php?key={key}&w={w}&type={type}"

    try:
        resp = requests.get(url.format(key=iciba_key, w=words, type="xml"))
        resp.encoding = 'utf-8'

        resp_dict = xmltodict.parse(resp.text).get('dict')
        ps = resp_dict.get('ps') or ''
        print(" " + words + "  " + huepy.lightred(ps) + '\n')

        pos = resp_dict.get("pos")
        acceptation = resp_dict.get("acceptation")

        if pos and acceptation:
            if not isinstance(pos, list) and not isinstance(acceptation, list):
                pos = [pos]
                acceptation = [acceptation]

            word_translate = pos[0] + ' ' + acceptation[0]
            for p, a in zip([i for i in pos], [i for i in acceptation]):
                if a and p:
                    print(" - " + huepy.lightcyan(p + " " + a))
            print()

        UpdateSQL(words, word_translate)

        index = 1
        sent = resp_dict.get("sent")
        if not sent:
            pass
        elif not isinstance(sent, list):
            sent = [sent]
        print(huepy.orange('Example:'))
        for item in sent:
            for key, value in item.items():
                if key == "orig":
                    print(highlight(huepy.grey("  {}. ".format(index) + value), words))
                    index += 1
                elif key == "trans":
                    print(huepy.cyan("      " + value))
        print()
    except Exception as e:
        print(" " + huepy.red(e))


def RunTerminal():
    parser = get_parser()
    args = vars(parser.parse_args())
        
    words = ' '.join(args['words'])

    if args['version']:
        print(huepy.cyan("meaning " + __version__))
        return 

    if args['records']:
        RecordsPromptShell()
        return 

    if not args['words']:
        parser.print_help()
        return 

    TranslateWithAiCiBa(words)


if __name__ == "__main__":
    RunTerminal()
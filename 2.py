#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple grammar checker

This grammar checker will fix grammar mistakes using Ginger.
"""

import sys
import urllib
import urlparse
from urllib2 import HTTPError
from urllib2 import URLError
import json


class ColoredText:
    """Colored text class"""
    colors = ['black', 'red', 'green', 'orange', 'blue', 'magenta', 'cyan', 'white']
    color_dict = {}
    for i, c in enumerate(colors):
        color_dict[c] = (i + 30, i + 40)

    @classmethod
    def colorize(cls, text, color=None, bgcolor=None):
        """Colorize text
        @param cls Class
        @param text Text
        @param color Text color
        @param bgcolor Background color
        """
        c = None
        bg = None
        gap = 0
        if color is not None:
            try:
                c = cls.color_dict[color][0]
            except KeyError:
                print("Invalid text color:", color)
                return(text, gap)

        if bgcolor is not None:
            try:
                bg = cls.color_dict[bgcolor][1]
            except KeyError:
                print("Invalid background color:", bgcolor)
                return(text, gap)

        s_open, s_close = '', ''
        if c is not None:
            s_open = '\033[%dm' % c
            gap = len(s_open)
        if bg is not None:
            s_open += '\033[%dm' % bg
            gap = len(s_open)
        if not c is None or bg is None:
            s_close = '\033[0m'
            gap += len(s_close)
        return('%s%s%s' % (s_open, text, s_close), gap)


def get_ginger_url(text):
    """Get URL for checking grammar using Ginger.
    @param text English text
    @return URL
    """
    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"

    scheme = "http"
    netloc = "services.gingersoftware.com"
    path = "/Ginger/correct/json/GingerTheText"
    params = ""
    query = urllib.urlencode([
        ("lang", "US"),
        ("clientVersion", "2.0"),
        ("apiKey", API_KEY),
        ("text", text)])
    fragment = ""

    return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))


def get_ginger_result(text):
    """Get a result of checking grammar.
    @param text English text
    @return result of grammar check by Ginger
    """
    url = get_ginger_url(text)

    try:
        response = urllib.urlopen(url)
    except HTTPError as e:
            print("HTTP Error:", e.code)
            quit()
    except URLError as e:
            print("URL Error:", e.reason)
            quit()
    except IOError, (errno, strerror):
        print("I/O error (%s): %s" % (errno, strerror))
        quit

    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")
        quit()

    return(result)


def main():
    """main function"""
    f1name =  " ".join(sys.argv[1:])
    f1 = open(f1name,"r")
    
    #for a in original_text:
    f2name = f1name + "_fixed"
    f2 = open(f2name,"w")
    for each_text in f1:
    #fixed_text = each_text
        results = get_ginger_result(each_text)

        #print(each_text)
        #print(fixed_text)
        #print(results)
        # Incorrect grammar
        color_gap, fixed_gap = 0, 0

        start = 0
        for result in results["LightGingerTheTextResult"]:
            if(result["Suggestions"]):
                from_index = result["From"] + color_gap
                to_index = result["To"] + 1 + color_gap
                suggest = result["Suggestions"][0]["Text"]
                 # Colorize text
              #colored_incorrect = ColoredText.colorize(each_text[from_index:to_index], 'red')[0]
               #colored_suggest, gap = ColoredText.colorize(suggest, 'green')

               # print(result["From"]) ,
               # print("  "),
               # print(result["To"]),
              # print("  "+suggest+" T")
                if start < result["From"]-1:
                    first_text = each_text[start:result["From"]].split()
                    for eachstr in first_text:
                        if ( len(eachstr) < 8 ):
                            eachstr = eachstr + (8-len(eachstr)) *" " + "!"
                        else:
                            eachstr = eachstr + + (16-len(eachstr)) *" "+ "!"
                        print(eachstr)
                        f2.write(eachstr+"\n")
    
                second_text = each_text[result["From"]:result["To"]+1]
                if ( len(second_text) < 8):
                    second_text = second_text + (8-len(second_text))*" " + "X"
                else:
                    second_text = second_text + (16-len(second_text))*" " + "X"
                print (second_text)
                f2.write(second_text+"\n")
                start = result["To"]+1

                #print(each_text)
                #print(each_text[from_index:to_index])
                #each_text = each_text[:from_index] + colored_incorrect + each_text[to_index:]
                #fixed_text = fixed_text[:from_index-fixed_gap] + fixed_text[to_index-fixed_gap:]
                #fixed_text = fixed_text[:from_index-fixed_gap] + colored_suggest + fixed_text[to_index-fixed_gap:]
                #print(fixed_text)

                #color_gap += gap
                #fixed_gap += to_index-from_index-len(suggest)

        #print(each_text)
        #print(fixed_text);
        #print("original text: \n" + each_text)
        #print("fixed text:    \n" + fixed_text)

if __name__ == '__main__':
    main()
